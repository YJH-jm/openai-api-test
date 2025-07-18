import os
import time
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv


load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

with st.sidebar:
    thread_id = st.text_input('thread_id', value='thread_D8c5lXrrdiMcMiXMTddHbaMQ')

    button_click =st.button("새로운 thread_id 생성")

    if button_click:
        thread = client.beta.threads.create()
        thread_id = thread.id
    st.info('현재 스레드 id는' + str(thread_id))

st.title("💬 청년 정책 chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

# 대화 내역 관리
if "message" not in st.session_state:
    st.session_state["message"] = [
        {
            "role": "assistant",
            "content" : "대화를 시작해볼까요?"
        }
    ]


# 화면에 과거의 모든 채팅 출력
for msg in st.session_state["message"]:
    st.chat_message(msg['role']).write(msg['content'])


# 새로운 입력과 답변 관리
if prompt := st.chat_input():
    if not thread_id:
        st.info("스레드 ID 입력 필요")
        st.stop()


    # 사용자 입력이 있는 경우 message 에 추가
    st.session_state.message.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )    

    # 사용자의 입력이 있는 경우 화면에 출력
    st.chat_message("user").write(prompt)

    # 스레드 메세지 생성 (run 하기 전)
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=prompt
    )

    # run
    run = client.beta.threads.runs.create(
        thread_id= thread_id,
        assistant_id = "asst_IJ8hZT640QKxrg4DI18pNUdx"  # 미리 만들어와야...
    )

    # run.status queued > in_process > completed
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id = run.id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(3)


    messages = client.beta.threads.messages.list(thread_id)

    # run.id를 이용하여 방금 나온 ChatGPT의 답변을 추출
    current_data = [message for message in messages.data if message.run_id == run.id] # 방금 질문한 run_id 기준으로 답변 추출
    msg = current_data[0].content[0].text.value

    # ChatGPT 답변 => message에 내역 추가
    st.session_state.message.append({
        "role" :"assistant",
        "content" : msg
    })

    # ChatGPT의 답변 => 화면에 출력
    st.chat_message("assistant").write(msg)
    