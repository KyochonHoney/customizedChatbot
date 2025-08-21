import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_community.llms import LlamaCpp
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain.chains import create_retrieval_chain

load_dotenv()

# ===== (A) 세션 히스토리 =====
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_llm():
    """
    LangChain 체인(create_stuff_documents_chain 등)에 바로 꽂히는 llama.cpp LLM 래퍼.
    """
    return LlamaCpp(
        model_path="/home/ollama/gptoss/models/OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",  # 경로 확인 필수
        n_ctx=4096,            # 프롬프트/히스토리 길이 여유
        n_threads=8,           # CPU 코어 수에 맞게 조정 (예: os.cpu_count())
        temperature=0.7,       # 기존과 동일
        # 선택 옵션:
        # n_batch=64,          # CPU면 32~128 사이에서 성능-안정 타협
        # n_gpu_layers=0,      # GPU 없으면 0(기본)
        # mlock=True,          # 메모리 잠금(스와핑 감소, 권한 필요)
        # verbose=False,
    )
# ===== (B) LLM =====
#llm = get_llm()

llm = OllamaLLM(
    model="gpt-oss:20b",
    base_url="http://localhost:11434",
    temperature=0.8,
)

# ===== (C) Retriever (Chroma 로드) =====
# 인덱싱 때 쓴 임베딩과 동일해야 함
embedding = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large-instruct",
    encode_kwargs={"normalize_embeddings": True},   # 권장
    # model_kwargs={"device": "cpu"}  # 필요 시 장치 지정
)

vectordb = Chroma(
    collection_name="cures",
    persist_directory="./chroma_huggingface",
    embedding_function=embedding,
)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})  # 필요시 k 조절

# ===== (D) 프롬프트 & 체인 =====
SYSTEM_PROMPT = (
    "당신은 맞춤배움길 전용 AI 챗봇입니다. "
    "반드시 DB({context})에 있는 내용으로만 간단히 답변하세요. "
    "DB에 해당 내용이 없으면 '죄송합니다. 제가 모르는 질문입니다 :)'라고만 답하세요. "
    "불필요한 설명 없이 짧고 명확하게 답변하세요."
    "답변은 500자 내로만 해주세요"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# 검색된 문서를 {context}로 그대로 넣어 답하도록 하는 stuff chain
question_answer_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=qa_prompt,
    output_parser=StrOutputParser()  # 최종 문자열
)

# retriever → stuff chain
rag_chain = create_retrieval_chain(
    retriever=retriever,
    combine_docs_chain=question_answer_chain
)

# 대화 히스토리 포함
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",  # ※ create_retrieval_chain의 기본 출력키는 "answer"
)

def get_ai_response(user_message: str, session_id: str = "abc123"):
    # create_retrieval_chain은 {"answer": "..."}를 출력으로 내보냄
    gen = conversational_rag_chain.stream(
        {"input": user_message},
        config={"configurable": {"session_id": session_id}}
    )
    print("RAG collection count:", vectordb._collection.count())
    # UI 코드가 dict의 "answer" 키를 조건부로 읽거나, 여기서 표준화해서 넘겨도 됨
    for chunk in gen:
        # 표준화: 항상 {'answer': token} 형태로 내보내기
        if isinstance(chunk, dict) and "answer" in chunk:
            yield {"answer": chunk["answer"]}
        elif isinstance(chunk, str):
            yield {"answer": chunk}
        elif isinstance(chunk, dict):
            # 다른 키로 오면 무시/보정
            token = chunk.get("answer")
            if token:
                yield {"answer": token}
