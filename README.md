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
| **현재 버전** | v0.6.0 |

---

## ✨ 주요 기능

### 1. 이미지 업로드 및 OCR 처리
- 보조금 신청서 이미지를 업로드하면 자동으로 텍스트 추출
- 지원 이미지 형식: JPG, PNG, BMP, TIFF
- 파일 크기 제한: 10MB 이하
- **이미지 자동 축소**: 큰 이미지(3000px 이상)는 자동으로 1600px 이하로 비율 유지 축소

### 2. OCR 모델 4종 선택 가능
사용자가 상황에 맞게 OCR 모델을 선택할 수 있습니다.

| 모델 | 특화 영역 | 비고 |
|------|----------|------|
| **EasyOCR** | 범용 한/영 OCR | 빠른 기본 모델 |
| **TrOCR-Korean** ⭐ | 한국어 손글씨 특화 | 손글씨 신청서 핵심 모델 (200MB) |
| **Donut** ⭐ | 양식 문서 특화 | Naver Clova 개발 (800MB) |
| **Qwen2-VL-2B** | 범용 비전 모델 | 다국어 (4GB) |
| **Ensemble** | EasyOCR 기반 | 안전한 기본 옵션 |

### 3. 서버 환경 선택
- **Local 서버**: 본인 컴퓨터(CPU)에서 실행
- **JupyterHub 서버**: 학교 GPU 서버(RTX 4090)에서 실행 (localhost.run 터널링)

### 4. 테스트 데이터 미리 로딩
- 난이도별 테스트 신청서 5장을 클릭 한 번으로 로드
- 인쇄본 → 정자체 → 보통 손글씨 → 흘림체 → 악필 순서
- 정답 데이터(JSON) 포함으로 자동 정확도 측정 가능

### 5. 결과 정보 상세 표시
- 추출된 전체 텍스트
- 각 텍스트 영역의 신뢰도 점수
- 이미지 축소 정보 (원본 → 처리 크기)
- 사용된 모델 정보

---

## 🛠 기술 스택

### Backend
- **Python 3.x**
- **FastAPI** 0.110.0 — 비동기 웹 프레임워크
- **Uvicorn** 0.29.0 — ASGI 서버
- **EasyOCR** 1.7.1 — OCR 엔진 (한국어/영어)
- **transformers** 4.45+ — 허깅페이스 모델 로딩
- **PyTorch** 2.x — 딥러닝 프레임워크
- **accelerate** — GPU 가속
- **sentencepiece, protobuf** — Donut 모델 의존성

### OCR Models
- **EasyOCR** — 전통적 OCR
- **TrOCR (team-lucid/trocr-small-korean)** — 한국어 손글씨 특화
- **Donut (naver-clova-ix/donut-base)** — Naver Clova 양식 특화
- **Qwen2-VL-2B-Instruct** — 알리바바 비전 모델

### Frontend
- **HTML / CSS / JavaScript**

### Infrastructure
- **JupyterHub** (RTX 4090 GPU 24GB)
- **localhost.run** — SSH 포트 포워딩 기반 외부 접속

### 협업 도구
- **Git / GitHub**

---

## 📁 프로젝트 구조

```
hwaseong-ocr/
├── backend/                  # FastAPI 백엔드 서버
│   ├── main.py              # API 엔드포인트 + 4종 OCR 모델 + 자동 축소
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
│   ├── index.html           # 메인 웹페이지 (4종 모델 UI)
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
- (선택) NVIDIA GPU + CUDA 12.x

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

> ⚠️ **PaddleOCR 사용 시 주의**: PaddleOCR(paddlepaddle)는 PyTorch와 의존성 충돌이 발생하여 본 프로젝트에서는 제거되었습니다. 추가 설치 시 다른 모델이 동작하지 않을 수 있습니다.

### 3단계: 백엔드 서버 실행

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

서버가 정상 실행되면 다음 메시지가 표시됩니다:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 4단계: 프론트엔드 열기

`frontend/index.html` 파일을 브라우저로 엽니다.

---

## 🌐 외부 접속 (JupyterHub 환경)

학교 JupyterHub의 GPU 서버를 외부에서 접근 가능하게 하려면 `localhost.run`을 사용합니다.

### 외부 접속 설정

**터미널 1 — FastAPI 서버 켜기**
```bash
cd ~/hwaseong-ocr/backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**터미널 2 — 외부 터널 켜기**
```bash
ssh -R 80:localhost:8000 nokey@localhost.run
```

실행 결과로 `https://xxxxx.lhr.life` 형태의 외부 URL이 발급됩니다.

### 제약사항
- 6시간 후 자동 종료 (재실행 필요)
- 외부 URL이 매번 변경됨
- JupyterHub 세션 종료 시 라이브러리 재설치 필요

### 트러블슈팅

| 에러 | 원인 | 해결 |
|------|------|------|
| `address already in use` | 기존 서버 살아있음 | `pkill -f "uvicorn main:app"` |
| `uvicorn: command not found` | 라이브러리 초기화됨 | `pip install -r requirements.txt` |
| `connect_to localhost port 8000: failed` | FastAPI 서버 죽음 | uvicorn 재실행 |
| `no tunnel here` | localhost.run URL 만료 | ssh 명령어 재실행 |
| `Failed to fetch` | URL 잘못 입력 / 보안 페이지 안 통과 | URL 직접 접속해서 확인 |

---

## 📖 사용법

### 1. 신청서 이미지 업로드

1. 웹페이지에서 **"이미지 선택"** 버튼 클릭 또는 드래그 앤 드롭
2. 보조금 신청서 이미지 선택 (JPG, PNG, BMP, TIFF / 10MB 이하)
3. **"OCR 분석 시작"** 버튼 클릭

### 2. OCR 모델 선택

용도에 맞는 모델 선택:

| 상황 | 추천 모델 |
|------|----------|
| 빠른 결과가 필요할 때 | **EasyOCR** |
| 손글씨 신청서 ⭐ | **TrOCR-Korean** |
| 양식 문서 (보조금 신청서) | **Donut** |
| 다양한 비전 분석 | **Qwen2-VL** |
| 안정적 기본값 | **Ensemble** |

### 3. 서버 환경 선택

- **Local**: 본인 컴퓨터의 CPU 사용 (기본값, 속도 느림)
- **JupyterHub GPU**: 학교 GPU 서버 사용 (속도 빠름, URL 입력 필요)

### 4. 결과 확인

OCR 처리가 완료되면 화면에 다음 정보가 표시됩니다.
- 추출된 전체 텍스트
- 각 텍스트 영역의 신뢰도 점수
- 처리된 항목 수
- 이미지 축소 정보

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

> 📝 **확장 계획**: 통계적 유의성 확보를 위해 30장으로 확대 예정

정답 데이터는 `frontend/samples/test_data.json` 에 저장되어 있으며, OCR 결과와 자동 비교하여 정확도를 측정할 수 있습니다.

---

## 🔌 API 명세

### 기본 정보
- **Base URL**: `http://localhost:8000` 또는 `https://xxxxx.lhr.life`
- **API 문서 (자동 생성)**: `http://localhost:8000/docs`

### 엔드포인트

#### `GET /`
API 상태 및 지원 모델 정보 반환

**응답 예시:**
```json
{
  "message": "화성시 보조금 신청서 OCR API",
  "version": "0.6.0",
  "features": {
    "auto_resize": "큰 이미지는 자동으로 1600px 이하로 축소"
  },
  "models": ["easyocr", "qwen", "trocr_korean", "donut", "ensemble"],
  "model_descriptions": {
    "easyocr": "범용 OCR (한/영)",
    "qwen": "Qwen2-VL-2B 비전 모델",
    "trocr_korean": "한국어 손글씨 특화",
    "donut": "양식 문서 특화 (Naver Clova)",
    "ensemble": "EasyOCR 기반 (안전한 기본값)"
  }
}
```

#### `POST /ocr`
이미지 업로드 후 OCR 처리

**요청 파라미터:**
- `file` (필수): 업로드할 이미지 파일
- `model` (선택): `easyocr` / `qwen` / `trocr_korean` / `donut` / `ensemble`

**응답 예시:**
```json
{
  "success": true,
  "filename": "sample_01.jpg",
  "model_used": "trocr_korean",
  "full_text": "추출된 전체 텍스트...",
  "details": [
    {
      "text": "탄소중립 마을 환경 개선 사업",
      "confidence": 0.987,
      "bbox": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ],
  "total_items": 15,
  "image_info": {
    "original_size": [4032, 3024],
    "processed_size": [1600, 1199],
    "was_resized": true
  }
}
```

---

## 🗺 로드맵

### ✅ 완료
- [x] 프로젝트 초기 구성 (FastAPI + HTML)
- [x] 이미지 업로드 및 OCR 처리 기능
- [x] 모델 선택 인터페이스 (4종 OCR + 앙상블)
- [x] 서버 선택 UI (Local / JupyterHub)
- [x] 테스트 데이터 5장 + 정답 JSON 구축
- [x] JupyterHub GPU 환경 구축 (RTX 4090)
- [x] localhost.run 외부 터널링 적용
- [x] 손글씨 특화 모델 추가 (Qwen, TrOCR-Korean, Donut)
- [x] **이미지 자동 축소** (v0.5.0)
- [x] **라이브러리 호환성 정리** (PaddleOCR 제거, v0.6.0)

### 🟡 진행 중
- [ ] 테스트 데이터 30장으로 확대 (글씨체별 다양화)
- [ ] 모델 평가 인터페이스 구축 (자동 정확도 측정)
- [ ] 최종 목표 및 세부 기능 설정

### ⬜ 예정
- [ ] 정확도 자동 측정 기능 강화
- [ ] 최종 사용자 인터페이스 개선 (공무원 시연용)
- [ ] 모델 비교 대시보드 (모델별 정확도 시각화)
- [ ] (향후) Fine-tuning 데이터 수집 및 적용

---

## 📝 업데이트 기록

주차별 업데이트 내역은 [update.md](./update.md) 에서 확인할 수 있습니다.

### 주요 버전 히스토리
- **v0.6.0** (2026-05-19): PaddleOCR 제거, 4종 모델 안정화
- **v0.5.0** (2026-05-19): 이미지 자동 축소 기능 추가
- **v0.4.0** (2026-05-17): 5종 OCR 모델 통합 (Qwen, TrOCR-Korean, Donut 추가)
- **v0.3.0** (2026-05-17): Qwen2-VL-2B 모델 첫 통합
- **v0.2.0** (2026-05-12): EasyOCR + PaddleOCR + 모델 선택 UI

---

## 👥 팀 정보

화성시 보조금 신청서 OCR 프로젝트 팀
- 캡스톤디자인 수업
- "AI 서비스 개발 또는 데이터분석을 통한 화성시 현안 해결" 공모전 출품

---

## 📄 라이선스

본 프로젝트는 학술 연구 및 캡스톤디자인 수업 목적으로 개발되었습니다.
