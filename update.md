# 업데이트 기록 (Update Log)

이 문서는 화성시 보조금 신청서 OCR 웹 서비스 프로젝트의 주차별 업데이트 내역을 기록합니다.
가장 최신 업데이트가 가장 위에 표시됩니다.

---

## [3주차] 2026-05-17

### 추가된 기능
- **OCR 모델 5종 통합**: 손글씨 특화 모델 포함하여 사용자가 선택 가능
  - `easyocr`: 범용 OCR (한/영)
  - `paddleocr`: 한국어 인쇄물 강함
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
