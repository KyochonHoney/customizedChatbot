# 🤖 RAG 기반 AI 챗봇

이 프로젝트는 Retrieval-Augmented Generation (RAG) 기술을 사용하여 구현된 AI 챗봇입니다. 사용자의 질문에 대해 미리 구축된 데이터베이스에서 관련 정보를 찾아내고, 이를 기반으로 대규모 언어 모델(LLM)이 답변을 생성합니다.

## 🌟 주요 기능

- **Streamlit 기반 웹 인터페이스**: 사용자와 챗봇이 대화할 수 있는 직관적인 웹 UI를 제공합니다.
- **RAG 파이프라인**: `LangChain`을 사용하여 RAG 파이프라인을 구축했습니다.
  - **Retriever**: `Chroma DB`에 저장된 벡터 데이터베이스에서 사용자의 질문과 관련된 문서를 검색합니다.
  - **Generator**: `Ollama`를 통해 `LlamaCpp` 또는 `OllamaLLM` 모델을 사용하여 검색된 문서를 바탕으로 답변을 생성합니다.
- **데이터베이스 관리**:
  - `insertDB.py`: Excel 파일 (`part3.xlsx`)의 데이터를 Chroma DB에 임베딩하여 저장합니다.
  - `checkDB.py`: Chroma DB의 상태를 확인하고 저장된 데이터를 조회합니다.

## 🛠️ 기술 스택

- **언어**: Python
- **프레임워크**: Streamlit, LangChain
- **LLM**: LlamaCpp, Ollama
- **벡터 데이터베이스**: Chroma DB
- **임베딩 모델**: `intfloat/multilingual-e5-large-instruct` (Hugging Face)

## 🚀 시작하기

### 1. 사전 준비

- Python 3.8 이상
- Ollama 및 필요한 LLM 모델 설치 (예: `ollama pull gemma:2b`)

### 2. 프로젝트 클론 및 종속성 설치

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
pip install -r requirements.txt
```

### 3. 데이터베이스 설정

1.  `part3.xlsx` 파일을 프로젝트 루트 디렉토리에 준비합니다. 이 파일에는 챗봇이 답변할 정보가 들어있습니다.
2.  다음 스크립트를 실행하여 데이터를 Chroma DB에 저장합니다.

    ```bash
    python insertDB.py
    ```

3.  (선택 사항) 다음 스크립트를 실행하여 데이터가 잘 저장되었는지 확인합니다.

    ```bash
    python checkDB.py
    ```

### 4. 챗봇 실행

다음 명령어를 사용하여 Streamlit 웹 애플리케이션을 실행합니다.

```bash
streamlit run chat.py
```

이제 웹 브라우저에서 챗봇과 대화를 시작할 수 있습니다!

## 📁 파일 구조

```
.
├── .gitignore
├── chat.py           # Streamlit 챗봇 애플리케이션
├── checkDB.py        # Chroma DB 데이터 확인 스크립트
├── insertDB.py       # 데이터를 Chroma DB에 삽입하는 스크립트
├── llm_utils.py      # LangChain 및 LLM 관련 유틸리티 함수
├── requirements.txt  # Python 종속성 목록
└── part3.xlsx        # (예시) 데이터 소스 파일
```

