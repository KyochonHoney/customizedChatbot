import os
import streamlit as st
from llm_utils import get_ai_response

st.set_page_config(page_title="RAG PART3", page_icon="🤖")

st.title("🤖맞춤배움길 AI 어시스턴트")
st.caption("맞춤배움길 챗봇 구현(ollama gpt-oss:20b)")

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input(placeholder="질문을 입력해주세요!"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    with st.spinner("답변을 생성하는 중입니디"):
        ai_generator = get_ai_response(user_question)

        with st.chat_message("ai"):
            full_answer = ""
            placeholder = st.empty()

            for chunk in ai_generator:
                if "answer" in chunk:
                    full_answer += chunk["answer"]
                    placeholder.markdown(full_answer)

            st.session_state.message_list.append({
                "role": "ai",
                "content": full_answer
            })
