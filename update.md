# 업데이트 기록 (Update Log)

이 문서는 화성시 보조금 신청서 OCR 웹 서비스 프로젝트의 주차별 업데이트 내역을 기록합니다.
가장 최신 업데이트가 가장 위에 표시됩니다.

---

## [3주차 후반] 2026-05-19 — v0.6.0

### 추가된 기능
- **이미지 자동 축소 기능 추가** (v0.5.0)
  - 큰 이미지(3000px 이상)는 자동으로 1600px 이하로 비율 유지 축소
  - Qwen 모델의 메모리 부족 문제(124GB 요구) 해결
  - 모든 OCR 모델의 처리 안정성 향상
  - 결과 응답에 원본/축소 크기 정보 포함
- **모델 선택 UI 5종 → 4종 정리** (v0.6.0)
  - PaddleOCR 제거 (라이브러리 충돌 이슈)
  - 4종 모델 + 앙상블로 최종 정리
  - 클릭으로 모든 모델 선택 가능

### 시행착오 및 발견 (캡스톤 발표 콘텐츠)
- **PaddleOCR ↔ PyTorch 라이브러리 충돌 발견**
  - paddlepaddle 설치 시 PyTorch 환경 손상 확인
  - TrOCR, Donut, Qwen 모델 모두 작동 불가
  - PaddleOCR 제거 + PyTorch 강제 재설치(`--force-reinstall`)로 해결
- **PaddleOCR API 변경 발견**
  - PaddleOCR 최신 버전(3.x)에서 `cls` 인자 제거됨
  - 옛 코드(`paddle.ocr(image, cls=True)`) 동작 안 함
- **각 OCR 모델별 한계 직접 확인**
  - EasyOCR: 인쇄물 강함, 손글씨 약함
  - TrOCR-Korean: 한 줄 단위 입력 특화, 전체 문서 처리 약함
  - Donut: 영문 양식 학습 위주, 한국어 양식 한계
  - Qwen2-VL-2B: OCR 거부 응답 (모델 크기 한계)
  - 손글씨 OCR의 본질적 어려움 확인 (pre-trained 한계)

### 코드 변경
- `backend/main.py`: v0.4.0 → v0.6.0
  - 이미지 자동 축소 함수 `preprocess_image()` 추가
  - PaddleOCR 관련 코드 제거
  - 모델 4종 + 앙상블로 정리
- `backend/requirements.txt`: PaddleOCR 라이브러리 제거
- `frontend/index.html`: 모델 선택 UI 5종 → 4종 정리, 이미지 축소 정보 표시 추가

### 환경 이슈
- JupyterHub 환경: 세션 종료 시 라이브러리 초기화됨 확인
- 매번 `pip install -r requirements.txt` 재실행 필요
- localhost.run 6시간 자동 종료 + URL 매번 변경 (예상된 제약)

---

## [3주차] 2026-05-17 — v0.4.0

### 추가된 기능
- **OCR 모델 5종 통합**: 손글씨 특화 모델 포함하여 사용자가 선택 가능
  - `easyocr`: 범용 OCR (한/영)
  - `paddleocr`: 한국어 인쇄물 강함 (※추후 제거됨)
  - `qwen`: Qwen2-VL-2B 비전 모델 (범용)
  - `trocr_korean`: 한국어 손글씨 특화 (team-lucid/trocr-small-korean)
  - `donut`: 양식 문서 특화 (Naver Clova)
  - `ensemble`: EasyOCR + PaddleOCR 앙상블
- **API 버전 0.4.0 업데이트**: 모델 선택 옵션 6가지로 확장

### 환경 구축
- **JupyterHub 환경 셋업 완료**: PyTorch 2.3 환경에서 프로젝트 실행
- **RTX 4090 GPU 인식 확인**: nvidia-smi로 24GB GPU 메모리 사용 가능 확인
- **라이브러리 설치 완료**: FastAPI, EasyOCR, transformers, accelerate 등

### 외부 접속 환경
- **localhost.run 터널링 적용**: SSH 포트 포워딩으로 외부 접속 가능한 URL 생성
- **시행착오 기록**:
  - cloudflared quick tunnel 시도 → 500 에러로 실패
  - cloudflared Named Tunnel 시도 → 도메인 등록 필요로 진행 불가
  - 최종적으로 localhost.run 채택 → 교수님 승인 받음
- **제약사항**: 6시간 자동 종료, URL 매번 변경 (발표 시 재실행 필요)

### 코드 변경
- `backend/main.py`: 모델 5종 통합 코드 작성 (182줄 추가)
- `backend/requirements.txt`: transformers, torch, torchvision, accelerate 추가

---

## [2주차] 2026-05-12

### 추가된 기능
- **모델 교체 인터페이스 추가**: OCR 모델을 쉽게 선택·교체할 수 있는 UI 구현
- **서버 선택 UI 추가**: Local 서버 / JupyterHub의 4090 GPU 서버 중 클릭으로 선택 가능
- **테스트 데이터 미리 로딩**: 난이도별 테스트 데이터 5개를 클릭 한 번으로 로드
- **테스트 데이터셋 구축**: 화성시 보조금 신청서 양식 기반, 글씨체별 5장 (인쇄본 / 정자체 / 보통 손글씨 / 흘림체 / 악필)
- **정답 데이터(JSON) 구축**: 자동 정확도 측정용 ground truth 데이터 추가 (`frontend/samples/test_data.json`)

### 개선된 기능
- **FastAPI 백엔드 안정화**: 서버 동작 안정성 개선

---

## [1주차] 2026-05-02

### 추가된 기능
- **프로젝트 초기 구성**: backend (FastAPI) + frontend (HTML) 기본 구조 생성
- **이미지 업로드 기능**: 신청서 이미지를 업로드하면 화면에 표시되는 기본 인터페이스
- **GitHub 저장소 구축**: 협업을 위한 버전 관리 시작

### 기술 스택
- Backend: Python 3.x + FastAPI
- Frontend: HTML / CSS / JavaScript

---
