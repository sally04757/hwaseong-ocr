# 화성시 보조금 신청서 OCR 웹 서비스

> 손글씨 보조금 신청서를 AI가 자동으로 판독해주는 공무원 전용 웹 서비스

화성시청 담당 공무원이 손글씨로 작성된 보조금 신청서를 빠르고 정확하게 디지털화할 수 있도록 돕는 OCR 기반 웹 서비스입니다. 본 프로젝트는 캡스톤디자인 수업의 "AI 서비스 개발 또는 데이터분석을 통한 화성시 현안 해결" 공모전 출품작입니다.

---

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | 화성시 보조금 신청서 OCR 웹 서비스 |
| **목적** | 손글씨 보조금 신청서의 자동 디지털화 |
| **대상 사용자** | 화성시청 복지·농업·주민지원 담당 공무원 |
| **개발 환경** | Local CPU / JupyterHub (RTX 4090 GPU) |
| **현재 버전** | v0.2.0 |

---

## ✨ 주요 기능

### 1. 이미지 업로드 및 OCR 처리
- 보조금 신청서 이미지를 업로드하면 자동으로 텍스트 추출
- 지원 이미지 형식: JPG, PNG, BMP, TIFF
- 파일 크기 제한: 10MB 이하

### 2. OCR 모델 선택
사용자가 상황에 맞게 OCR 모델을 선택할 수 있습니다.

| 모델 | 특징 |
|------|------|
| **EasyOCR** (기본) | 가볍고 빠른 OCR 엔진, 한국어 지원 |
| **PaddleOCR** | 정확도 높은 OCR 엔진 (별도 설치 필요) |
| **Ensemble** | EasyOCR + PaddleOCR 결합, 신뢰도 기반 결과 선택 |

### 3. 서버 환경 선택
- **Local 서버**: 본인 컴퓨터(CPU)에서 실행
- **JupyterHub 서버**: 학교 GPU 서버(RTX 4090)에서 실행 (cloudflared 터널링 적용 예정)

### 4. 테스트 데이터 미리 로딩
- 난이도별 테스트 신청서 5장을 클릭 한 번으로 로드
- 인쇄본 → 정자체 → 보통 손글씨 → 흘림체 → 악필 순서
- 정답 데이터(JSON) 포함으로 자동 정확도 측정 가능

---

## 🛠 기술 스택

### Backend
- **Python 3.x**
- **FastAPI** 0.110.0 — 비동기 웹 프레임워크
- **Uvicorn** 0.29.0 — ASGI 서버
- **EasyOCR** 1.7.1 — OCR 엔진 (한국어/영어)
- **Pillow** 10.3.0 — 이미지 처리
- **NumPy** 1.26.4 — 배열 연산

### Frontend
- **HTML / CSS / JavaScript** — 사용자 인터페이스

### 협업 도구
- **Git / GitHub** — 버전 관리

---

## 📁 프로젝트 구조

```
hwaseong-ocr/
├── backend/                  # FastAPI 백엔드 서버
│   ├── main.py              # API 엔드포인트 및 OCR 로직
│   └── requirements.txt     # Python 패키지 목록
│
├── frontend/                 # 웹페이지 (사용자 인터페이스)
│   ├── samples/             # 테스트 데이터
│   │   ├── sample_01.jpg    # 인쇄본 (Easy)
│   │   ├── sample_02.jpg    # 정자체 (Easy-Medium)
│   │   ├── sample_03.jpg    # 보통 손글씨 (Medium)
│   │   ├── sample_04.jpg    # 흘림체 (Hard)
│   │   ├── sample_05.jpg    # 악필 (Very Hard)
│   │   └── test_data.json   # 정답 데이터 (ground truth)
│   ├── index.html           # 메인 웹페이지
│   ├── README.md            # 프론트엔드 설명
│   └── .gitignore
│
├── README.md                 # 프로젝트 전체 설명 (이 파일)
└── update.md                 # 주차별 업데이트 기록
```

---

## 🚀 설치 및 실행 방법

### 사전 준비
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 1단계: 저장소 클론

```bash
git clone https://github.com/sally04757/hwaseong-ocr.git
cd hwaseong-ocr
```

### 2단계: 백엔드 라이브러리 설치

```bash
cd backend
pip install -r requirements.txt
```

> 💡 **PaddleOCR 추가 설치 (선택사항)**: 앙상블 또는 PaddleOCR 모델을 사용하려면 별도로 설치하세요.
> ```bash
> pip install paddleocr paddlepaddle
> ```

### 3단계: 백엔드 서버 실행

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버가 정상 실행되면 다음 메시지가 표시됩니다:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 4단계: 프론트엔드 열기

`frontend/index.html` 파일을 브라우저로 엽니다. 더블클릭하거나 브라우저에 드래그하면 됩니다.

---

## 📖 사용법

### 1. 신청서 이미지 업로드

1. 웹페이지에서 **"이미지 선택"** 버튼 클릭
2. 보조금 신청서 이미지 선택 (JPG, PNG, BMP, TIFF / 10MB 이하)
3. **"업로드"** 버튼 클릭

### 2. OCR 모델 선택

업로드 전 사용할 모델을 선택할 수 있습니다.
- **EasyOCR**: 빠른 결과가 필요할 때 (기본값)
- **PaddleOCR**: 정확도가 중요할 때
- **Ensemble**: 두 모델을 모두 사용하여 가장 신뢰할 수 있는 결과 얻기

### 3. 서버 환경 선택

- **Local**: 본인 컴퓨터의 CPU 사용 (기본값, 속도 느림)
- **JupyterHub GPU**: 학교 GPU 서버 사용 (속도 빠름, 설정 필요)

### 4. 결과 확인

OCR 처리가 완료되면 화면에 다음 정보가 표시됩니다.
- 추출된 전체 텍스트
- 각 텍스트 영역의 신뢰도 점수
- 처리된 항목 수

### 5. 테스트 데이터로 빠르게 확인

`frontend/samples/` 폴더의 테스트 데이터를 사용하면 미리 준비된 5장의 신청서로 시스템을 테스트할 수 있습니다.

---

## 🧪 테스트 데이터셋

본 프로젝트는 OCR 모델의 글씨체별 인식 성능을 비교 측정하기 위해 자체 구축한 테스트 데이터셋을 사용합니다.

| 샘플 | 난이도 | 글씨체 |
|------|--------|--------|
| sample_01.jpg | Easy | 인쇄본 (기준점) |
| sample_02.jpg | Easy-Medium | 정자체 손글씨 |
| sample_03.jpg | Medium | 보통 손글씨 |
| sample_04.jpg | Hard | 흘림체 |
| sample_05.jpg | Very Hard | 악필 |

5장 모두 동일한 내용을 다른 글씨체로 작성하여, OCR 모델의 정확도 차이가 순전히 글씨체에 의한 것임을 측정할 수 있도록 통제 변수 방식으로 설계했습니다.

정답 데이터는 `frontend/samples/test_data.json` 에 저장되어 있으며, OCR 결과와 자동 비교하여 정확도를 측정할 수 있습니다.

---

## 🔌 API 명세

### 기본 정보
- **Base URL**: `http://localhost:8000`
- **API 문서 (자동 생성)**: `http://localhost:8000/docs`

### 엔드포인트

#### `GET /`
API 상태 및 지원 모델 정보 반환

**응답 예시:**
```json
{
  "message": "화성시 보조금 신청서 OCR API",
  "version": "0.2.0",
  "models": ["easyocr", "paddleocr", "ensemble"]
}
```

#### `POST /ocr`
이미지 업로드 후 OCR 처리

**요청 파라미터:**
- `file` (필수): 업로드할 이미지 파일
- `model` (선택): `easyocr` (기본) / `paddleocr` / `ensemble`

**응답 예시:**
```json
{
  "success": true,
  "filename": "sample_01.jpg",
  "model_used": "easyocr",
  "full_text": "추출된 전체 텍스트...",
  "details": [
    {
      "text": "탄소중립 마을 환경 개선 사업",
      "confidence": 0.987,
      "bbox": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ],
  "total_items": 15
}
```

---

## 🗺 로드맵

### ✅ 완료
- [x] 프로젝트 초기 구성 (FastAPI + HTML)
- [x] 이미지 업로드 및 OCR 처리 기능
- [x] 모델 선택 인터페이스 (EasyOCR / PaddleOCR / Ensemble)
- [x] 서버 선택 UI (Local / JupyterHub)
- [x] 테스트 데이터 5장 + 정답 JSON 구축

### 🟡 진행 중
- [ ] JupyterHub GPU 서버 적용 (cloudflared 터널링)
- [ ] 테스트 데이터 30장으로 확대
- [ ] 모델 평가 인터페이스 구축

### ⬜ 예정
- [ ] 허깅페이스 OCR 모델 추가 적용
- [ ] 정확도 자동 측정 기능 강화
- [ ] 최종 사용자 인터페이스 개선

---

## 📝 업데이트 기록

주차별 업데이트 내역은 [update.md](./update.md) 에서 확인할 수 있습니다.

---

## 👥 팀 정보

화성시 보조금 신청서 OCR 프로젝트 팀
- 캡스톤디자인 수업
- "AI 서비스 개발 또는 데이터분석을 통한 화성시 현안 해결" 공모전 출품

---

## 📄 라이선스

본 프로젝트는 학술 연구 및 캡스톤디자인 수업 목적으로 개발되었습니다.
