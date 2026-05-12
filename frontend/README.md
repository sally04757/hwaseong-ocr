# 화성시 보조금 신청서 OCR 웹 서비스

> 캡스톤디자인 | AI 서비스 개발을 통한 화성시 현안 해결

손글씨 보조금 신청서 이미지를 업로드하면 AI(EasyOCR)가 자동으로 텍스트를 판독하는 웹 서비스입니다.

---

## 프로젝트 구조

```
project/
├── backend/
│   ├── main.py          # FastAPI 서버 (OCR API)
│   └── requirements.txt
├── frontend/
│   └── index.html       # 업로드 + 결과 표시 화면
├── .gitignore
└── README.md
```

---

## 실행 방법

### 1. 백엔드 실행

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload --port 8000
```

서버가 실행되면 `http://localhost:8000` 에서 접근 가능합니다.  
API 문서: `http://localhost:8000/docs` (Swagger UI 자동 제공)

### 2. 프론트엔드 실행

`frontend/index.html` 파일을 브라우저에서 바로 열거나,  
아래 명령어로 간단한 로컬 서버를 띄웁니다.

```bash
cd frontend
python -m http.server 3000
# 브라우저에서 http://localhost:3000 접속
```

> **주의:** `index.html`을 파일로 직접 열면 CORS 오류가 날 수 있으므로 로컬 서버를 권장합니다.

---

## GPU 사용 (RTX 5090)

`backend/main.py`에서 아래 줄을 수정하세요.

```python
# 변경 전 (CPU)
reader = easyocr.Reader(["ko", "en"], gpu=False)

# 변경 후 (GPU)
reader = easyocr.Reader(["ko", "en"], gpu=True)
```

---

## API 명세

| Method | 엔드포인트 | 설명 |
|--------|-----------|------|
| `GET`  | `/`       | 서버 상태 확인 |
| `POST` | `/ocr`    | 이미지 업로드 → OCR 결과 반환 |

### POST `/ocr` 응답 예시

```json
{
  "success": true,
  "filename": "신청서.jpg",
  "full_text": "성명 홍길동\n주민등록번호 850312-1234567",
  "details": [
    { "text": "성명 홍길동", "confidence": 0.95, "bbox": [[10,20],[200,20],[200,50],[10,50]] },
    { "text": "주민등록번호 850312-1234567", "confidence": 0.78, "bbox": [[10,60],[300,60],[300,90],[10,90]] }
  ],
  "total_items": 2
}
```

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.11, FastAPI, EasyOCR |
| 프론트엔드 | HTML5, CSS3, Vanilla JS |
| GPU | NVIDIA RTX 5090 (선택) |

---

## 팀

캡스톤디자인 팀 | 2026년 5월
