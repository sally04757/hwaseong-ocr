from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io

app = FastAPI(
    title="화성시 보조금 신청서 OCR API",
    description="손글씨 보조금 신청서를 자동 판독하는 API (5종 모델 + 이미지 자동 축소)",
    version="0.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 이미지 전처리 설정 ──────────────────────────────────────
# OCR 모델이 잘 처리할 수 있는 최대 크기 (가로/세로 중 긴 쪽 기준)
MAX_IMAGE_DIMENSION = 1600  # 핸드폰 사진은 보통 3000~4000이라 이걸로 줄임


def preprocess_image(image: Image.Image, max_dim: int = MAX_IMAGE_DIMENSION) -> Image.Image:
    """
    이미지를 OCR 모델에 적합한 크기로 자동 축소 (비율 유지)
    - 큰 이미지: 자동 축소
    - 작은 이미지: 그대로 유지
    - 메모리 사용량 감소 + OCR 정확도 향상
    """
    width, height = image.size
    
    # 이미 충분히 작으면 그대로 반환
    if max(width, height) <= max_dim:
        return image
    
    # 비율 유지하면서 축소
    if width > height:
        new_width = max_dim
        new_height = int(height * (max_dim / width))
    else:
        new_height = max_dim
        new_width = int(width * (max_dim / height))
    
    resized = image.resize((new_width, new_height), Image.LANCZOS)
    return resized


# ── 모델 지연 로딩 (처음 요청 시 로드) ──────────────────────
_easyocr_reader = None
_paddleocr_reader = None
_qwen_model = None
_qwen_processor = None
_trocr_kor_model = None
_trocr_kor_processor = None
_donut_model = None
_donut_processor = None


def get_easyocr():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        _easyocr_reader = easyocr.Reader(["ko", "en"], gpu=False)
    return _easyocr_reader


def get_paddleocr():
    global _paddleocr_reader
    if _paddleocr_reader is None:
        from paddleocr import PaddleOCR
        _paddleocr_reader = PaddleOCR(use_angle_cls=True, lang="korean")
    return _paddleocr_reader


def get_qwen():
    """Qwen2-VL-2B 모델 (범용 비전, 약 4GB)"""
    global _qwen_model, _qwen_processor
    if _qwen_model is None:
        from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
        import torch

        model_name = "Qwen/Qwen2-VL-2B-Instruct"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if device == "cuda" else torch.float32

        _qwen_processor = AutoProcessor.from_pretrained(model_name)
        _qwen_model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_name, torch_dtype=torch_dtype, device_map=device
        )
    return _qwen_processor, _qwen_model


def get_trocr_korean():
    """TrOCR Korean (한국어 손글씨 특화, 약 200MB)"""
    global _trocr_kor_model, _trocr_kor_processor
    if _trocr_kor_model is None:
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        import torch

        model_name = "team-lucid/trocr-small-korean"
        device = "cuda" if torch.cuda.is_available() else "cpu"

        _trocr_kor_processor = TrOCRProcessor.from_pretrained(model_name)
        _trocr_kor_model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)
    return _trocr_kor_processor, _trocr_kor_model


def get_donut():
    """Donut (Naver Clova 양식 문서 특화, 약 800MB)"""
    global _donut_model, _donut_processor
    if _donut_model is None:
        from transformers import DonutProcessor, VisionEncoderDecoderModel
        import torch

        model_name = "naver-clova-ix/donut-base"
        device = "cuda" if torch.cuda.is_available() else "cpu"

        _donut_processor = DonutProcessor.from_pretrained(model_name)
        _donut_model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)
    return _donut_processor, _donut_model


@app.get("/")
def root():
    return {
        "message": "화성시 보조금 신청서 OCR API",
        "version": "0.5.0",
        "features": {
            "auto_resize": f"큰 이미지는 자동으로 {MAX_IMAGE_DIMENSION}px 이하로 축소"
        },
        "models": ["easyocr", "paddleocr", "qwen", "trocr_korean", "donut", "ensemble"],
        "model_descriptions": {
            "easyocr": "범용 OCR (한/영)",
            "paddleocr": "한국어 인쇄물 강함",
            "qwen": "Qwen2-VL-2B 비전 모델",
            "trocr_korean": "한국어 손글씨 특화",
            "donut": "양식 문서 특화 (Naver Clova)",
            "ensemble": "EasyOCR + PaddleOCR 앙상블"
        }
    }


@app.post("/ocr")
async def ocr_image(
    file: UploadFile = File(...),
    model: str = Form(default="easyocr")
):
    """
    이미지 업로드 → 자동 축소 → OCR 결과 반환
    - model: easyocr / paddleocr / qwen / trocr_korean / donut / ensemble
    - 큰 이미지는 자동으로 1600px 이하로 축소되어 처리됨
    """
    allowed_types = ["image/jpeg", "image/png", "image/bmp", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="파일 크기는 10MB 이하여야 합니다.")

    try:
        # 1) 원본 이미지 로드
        original_image = Image.open(io.BytesIO(contents)).convert("RGB")
        original_size = original_image.size
        
        # 2) 자동 축소 (큰 이미지만)
        image = preprocess_image(original_image)
        resized_size = image.size
        was_resized = original_size != resized_size
        
        # 3) numpy 배열로도 변환 (EasyOCR/PaddleOCR용)
        image_np = np.array(image)

        if model == "paddleocr":
            results = run_paddleocr(image_np)
        elif model == "qwen":
            results = run_qwen(image)
        elif model == "trocr_korean":
            results = run_trocr_korean(image)
        elif model == "donut":
            results = run_donut(image)
        elif model == "ensemble":
            results = run_ensemble(image_np)
        else:
            results = run_easyocr(image_np)

        full_text = "\n".join([r["text"] for r in results])

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "model_used": model,
            "full_text": full_text,
            "details": results,
            "total_items": len(results),
            "image_info": {
                "original_size": list(original_size),
                "processed_size": list(resized_size),
                "was_resized": was_resized
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 처리 중 오류: {str(e)}")


def run_easyocr(image_np):
    reader = get_easyocr()
    raw = reader.readtext(image_np)
    return [
        {
            "text": text,
            "confidence": round(conf, 3),
            "bbox": [[int(p[0]), int(p[1])] for p in bbox]
        }
        for bbox, text, conf in raw
    ]


def run_paddleocr(image_np):
    try:
        paddle = get_paddleocr()
        raw = paddle.ocr(image_np, cls=True)
        results = []
        if raw and raw[0]:
            for line in raw[0]:
                bbox, (text, conf) = line
                results.append({
                    "text": text,
                    "confidence": round(conf, 3),
                    "bbox": [[int(p[0]), int(p[1])] for p in bbox]
                })
        return results
    except ImportError:
        raise HTTPException(
            status_code=400,
            detail="PaddleOCR가 설치되지 않았습니다. pip install paddleocr paddlepaddle"
        )


def run_qwen(image):
    """Qwen2-VL을 이용한 OCR (이미지 축소된 상태로 처리)"""
    try:
        processor, model = get_qwen()
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": "이미지에 있는 모든 한국어 텍스트를 정확하게 추출해주세요. 줄바꿈을 유지하면서 텍스트만 출력해주세요."}
                ]
            }
        ]

        text_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text_prompt], images=[image], padding=True, return_tensors="pt")

        import torch
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        output_ids = model.generate(**inputs, max_new_tokens=1024)
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(inputs["input_ids"], output_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        lines = [line.strip() for line in output_text.split("\n") if line.strip()]
        return [{"text": line, "confidence": 1.0, "bbox": []} for line in lines]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qwen OCR 처리 오류: {str(e)}")


def run_trocr_korean(image):
    """TrOCR Korean - 한국어 손글씨 특화 (한 줄 단위 인식)"""
    try:
        processor, model = get_trocr_korean()
        import torch

        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        if torch.cuda.is_available():
            pixel_values = pixel_values.to("cuda")

        generated_ids = model.generate(pixel_values, max_length=512)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        lines = [line.strip() for line in generated_text.split("\n") if line.strip()]
        if not lines:
            lines = [generated_text.strip()]

        return [{"text": line, "confidence": 1.0, "bbox": []} for line in lines if line]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TrOCR Korean 처리 오류: {str(e)}")


def run_donut(image):
    """Donut - Naver Clova 양식 문서 특화"""
    try:
        processor, model = get_donut()
        import torch

        task_prompt = "<s_synthdog>"
        decoder_input_ids = processor.tokenizer(
            task_prompt, add_special_tokens=False, return_tensors="pt"
        ).input_ids

        pixel_values = processor(image, return_tensors="pt").pixel_values

        device = "cuda" if torch.cuda.is_available() else "cpu"
        pixel_values = pixel_values.to(device)
        decoder_input_ids = decoder_input_ids.to(device)

        outputs = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=512,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        sequence = processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(processor.tokenizer.eos_token, "")
        sequence = sequence.replace(processor.tokenizer.pad_token, "")
        sequence = sequence.replace(task_prompt, "").strip()

        lines = [line.strip() for line in sequence.split("\n") if line.strip()]
        if not lines:
            lines = [sequence]

        return [{"text": line, "confidence": 1.0, "bbox": []} for line in lines if line]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Donut 처리 오류: {str(e)}")


def run_ensemble(image_np):
    """EasyOCR + PaddleOCR 앙상블"""
    easy_results = run_easyocr(image_np)
    try:
        paddle_results = run_paddleocr(image_np)
    except Exception:
        return easy_results

    combined = easy_results + paddle_results
    combined.sort(key=lambda x: x["confidence"], reverse=True)

    seen = set()
    final = []
    for item in combined:
        if item["text"] not in seen:
            seen.add(item["text"])
            final.append(item)

    return final
