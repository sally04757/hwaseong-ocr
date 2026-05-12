from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io

app = FastAPI(
    title="화성시 보조금 신청서 OCR API",
    description="손글씨 보조금 신청서를 자동 판독하는 API (모델 선택 지원)",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 모델 지연 로딩 (처음 요청 시 로드) ──────────────────────
_easyocr_reader = None
_paddleocr_reader = None

def get_easyocr():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        # GPU 사용 시 gpu=True로 변경 (RTX 4090 / RTX 5090)
        _easyocr_reader = easyocr.Reader(["ko", "en"], gpu=False)
    return _easyocr_reader

def get_paddleocr():
    global _paddleocr_reader
    if _paddleocr_reader is None:
        from paddleocr import PaddleOCR
        _paddleocr_reader = PaddleOCR(use_angle_cls=True, lang="korean", )
    return _paddleocr_reader


@app.get("/")
def root():
    return {
        "message": "화성시 보조금 신청서 OCR API",
        "version": "0.2.0",
        "models": ["easyocr", "paddleocr", "ensemble"]
    }


@app.post("/ocr")
async def ocr_image(
    file: UploadFile = File(...),
    model: str = Form(default="easyocr")  # easyocr / paddleocr / ensemble
):
    """
    이미지 업로드 → OCR 결과 반환
    - model: easyocr (기본) / paddleocr / ensemble
    - GPU 사용 시 각 모델 초기화에서 gpu=True로 변경
    """

    allowed_types = ["image/jpeg", "image/png", "image/bmp", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="파일 크기는 10MB 이하여야 합니다.")

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)

        if model == "paddleocr":
            results = run_paddleocr(image_np)
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
            "total_items": len(results)
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
            detail="PaddleOCR가 설치되지 않았습니다. pip install paddleocr"
        )


def run_ensemble(image_np):
    """EasyOCR + PaddleOCR 앙상블: 두 결과를 합쳐서 반환"""
    easy_results = run_easyocr(image_np)
    try:
        paddle_results = run_paddleocr(image_np)
    except Exception:
        # PaddleOCR 없으면 EasyOCR만 반환
        return easy_results

    # 신뢰도 기준으로 높은 것 선택 (간단한 앙상블)
    combined = easy_results + paddle_results
    combined.sort(key=lambda x: x["confidence"], reverse=True)

    # 중복 제거 (같은 텍스트면 신뢰도 높은 것만)
    seen = set()
    final = []
    for item in combined:
        if item["text"] not in seen:
            seen.add(item["text"])
            final.append(item)

    return final
