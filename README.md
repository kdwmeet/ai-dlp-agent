# AI DLP Agent (기업 정보유출 감시 에이전트)

## 1. 프로젝트 개요

AI DLP(Data Loss Prevention) Agent는 직원이 외부로 발송하는 이메일 본문과 첨부파일을 실시간으로 스캔하여, 기업의 핵심 기술 및 고객 개인정보 유출을 사전에 차단하는 지능형 보안 솔루션입니다.

기존의 정규식(Regex) 기반 보안 솔루션은 키워드가 정확히 일치하지 않거나 변형된 형태의 데이터 유출을 탐지하는 데 한계가 있었습니다. 본 시스템은 OpenAI의 **gpt-5-mini** 모델을 활용하여 텍스트의 맥락(Context)을 완벽하게 이해하고, 기밀문서(소스코드, 설계도), 재무 데이터, 개인정보(PII)의 외부 유출 시도를 탐지하여 위험도에 따라 발송 차단(BLOCK) 또는 경고(WARN) 조치를 수행합니다.

### 주요 기능
* **Contextual Content Scanning:** 단순 키워드 매칭을 넘어 이메일 본문의 문맥을 파악하여 정보 유출 의도 분석.
* **Attachment Parsing:** PDF 및 TXT 형식의 첨부파일 텍스트를 자동으로 추출하여 검열 파이프라인에 병합.
* **Intelligent Routing:** CISO(수석 보안 담당자) 페르소나가 적용된 AI가 정책에 따라 차단(BLOCK), 승인 필요(WARN), 통과(PASS)로 액션 분류.
* **Structured Security Reporting:** 탐지된 민감 정보의 유형(Category)과 차단 사유(Reason)를 명확한 정형 데이터(JSON)로 반환하여 보안 감사 로그로 활용 가능.

## 2. 시스템 아키텍처

본 시스템은 자연어 처리 추론 모듈과 문서 파싱 모듈이 결합된 구조를 가집니다.

1.  **Input Interception:** 사용자가 작성한 이메일 본문과 첨부파일(PDF, TXT) 데이터 획득.
2.  **Document Parsing:** 첨부파일이 존재할 경우 `PyPDFLoader` 등을 활용하여 텍스트 데이터 추출 및 병합.
3.  **Threat Analysis:** **gpt-5-mini** 모델이 입력된 전체 텍스트를 검열 가이드(PII, Financial, Confidential)와 대조 분석.
4.  **Decision Making:** 유출 리스크를 산정하고 최종 조치(Action) 및 판단 근거 도출.
5.  **Output & UI:** 분석 결과를 JSON 구조로 파싱한 후, Streamlit 대시보드에 보안 리포트 형태로 렌더링.

## 3. 기술 스택

* **Language:** Python 3.10 이상
* **LLM:** OpenAI **gpt-5-mini**
* **Orchestration:** LangChain
* **Document Processing:** pypdf
* **Web Framework:** Streamlit
* **Environment Management:** python-dotenv

## 4. 프로젝트 구조

보안 정책 프롬프트와 검열 비즈니스 로직을 분리하여 설계되었습니다.

```text
ai-dlp-agent/
├── .env                  # 환경 변수 설정 (API Key)
├── requirements.txt      # 의존성 패키지 목록
├── main.py               # 메일 발송 시뮬레이터 및 보안 대시보드 UI
└── app/
    ├── __init__.py
    ├── config.py         # 보안 정책 가이드, CISO 페르소나 및 JSON 스키마 정의
    └── dlp_agent.py      # LLM 콘텐츠 스캔 및 유출 리스크 분석 로직
```
## 5. 설치 및 실행 가이드
### 5.1. 사전 준비
Python 환경이 구성된 상태에서 저장소를 복제하고 프로젝트 디렉토리로 이동하십시오.

```Bash
git clone [레포지토리 주소]
cd ai-dlp-agent
```
### 5.2. 의존성 설치
LangChain, 문서 파싱 패키지 등을 설치합니다.

```Bash
pip install -r requirements.txt
```
### 5.3. 환경 변수 설정
프로젝트 루트 경로에 .env 파일을 생성하고 OpenAI API 키를 입력하십시오.

```Ini, TOML
OPENAI_API_KEY=sk-your-api-key-here
```
### 5.4. 실행
Streamlit 애플리케이션을 실행합니다.

```Bash
streamlit run main.py
```
## 6. 출력 데이터 사양 (JSON Schema)
보안 검열 결과는 다음의 JSON 구조로 반환되며, 향후 사내 통합 보안 관제 시스템(SIEM) 등과의 API 연동에 용이합니다.

```JSON
{
  "category": "Confidential",
  "action": "BLOCK",
  "detected_content": "def generate_admin_token(user_id): secret_key = 'CORP_***'...",
  "reason": "사내 시스템 인증에 사용되는 핵심 모듈 소스코드 및 시크릿 키가 포함되어 있어 심각한 보안 침해 리스크가 존재합니다."
}
```

## 7. 실행 화면
<img width="1288" height="658" alt="스크린샷 2026-02-23 143604" src="https://github.com/user-attachments/assets/5d11f007-186c-48fe-9445-5cfa536f1f82" />

