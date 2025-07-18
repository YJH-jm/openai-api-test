import os 
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)


def ask_chatgpt(prompt):
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {
                "role" : "system", 
                "content" : prompt
            },
            {
                "role" : "user",
                "content" : text
            }
        ]
    )
    return response.choices[0].message.content


st.set_page_config(page_title="요약 프로그램")
st.header("Summarize")
st.markdown("-----")

# 글 입력받기
text = st.text_area("요악을 원하는 글 입력")

# 버튼 클릭하면 ask_chatgpt 에 아래 요약 요청하는 prompt 전달
if st.button("summarize"):
    prompt = f'''
    **Instruction** :
    - You are an expert assistant that summarizes text into **Korean language**.
    - Your task is to summarize the **text** sentences in **Korean language**.
    - Your summaries should include the following :
        - Omit duplicate content, but increase the summary weight of duplicate content.
        - Summarize by emphasizing concepts and arguments rather than case evidence.
        - Summarize in 3 lines.
        - Use the format of a bullet point.
    -text : {text}
    '''

    st.info(ask_chatgpt(prompt))



