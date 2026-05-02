from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import easyocr
import numpy as np
from PIL import Image
import io

app = FastAPI(
    title="화성시 보조금 신청서 OCR API",
    description="손글씨 보조금 신청서를 자동 판독하는 API",
    version="0.1.0"
)

# CORS 설정 (프론트엔드에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용 - 배포 시 실제 도메인으로 변경
    allow_methods=["*"],
    allow_headers=["*"],
)

# EasyOCR 리더 초기화 (한국어 + 영어)
# GPU가 있으면 gpu=True로 변경 (RTX 5090 사용 시)
reader = easyocr.Reader(["ko", "en"], gpu=False)


@app.get("/")
def root():
    return {"message": "화성시 보조금 신청서 OCR API 서버가 실행 중입니다."}


@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """
    이미지를 업로드하면 OCR 결과를 반환합니다.
    - 지원 형식: JPG, PNG, BMP, TIFF
    - 한국어 + 영어 인식
    """

    # 파일 형식 체크
    allowed_types = ["image/jpeg", "image/png", "image/bmp", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. (지원: JPG, PNG, BMP, TIFF)"
        )

    # 파일 크기 체크 (10MB 제한)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="파일 크기는 10MB 이하여야 합니다.")

    try:
        # PIL로 이미지 열기 → numpy 배열 변환
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)

        # EasyOCR 실행
        results = reader.readtext(image_np)

        # 결과 정리
        extracted_texts = []
        full_text_lines = []

        for (bbox, text, confidence) in results:
            extracted_texts.append({
                "text": text,
                "confidence": round(confidence, 3),
                "bbox": [
                    [int(pt[0]), int(pt[1])] for pt in bbox
                ]
            })
            full_text_lines.append(text)

        full_text = "\n".join(full_text_lines)

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "full_text": full_text,
            "details": extracted_texts,
            "total_items": len(extracted_texts)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 처리 중 오류 발생: {str(e)}")
