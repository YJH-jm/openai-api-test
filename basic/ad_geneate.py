import os 
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

def ask_chatgpt(prompt):
    response = client.chat.completions.create(
        model= "gpt-4",
        messages=[
            {
                "role" : "system",
                "content" : prompt
            },
            {
                "role" : "user",
                "content" : "광고 문구 작성해줘"
            }
        ]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="광고 문구 생성 프로그램")
st.header("광고 문구 생성")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("제품명", placeholder=" ")
    strength = st.text_input("제품 특징", placeholder=" ")
    keyword = st.text_input("필수 포함 키워드", placeholder=" ")

with col2:
    com_name = st.text_input("브랜드 명", placeholder='Apple, Samsung, ...')
    tone_manner = st.text_input("톤 & 매너", placeholder="발랄하게, 감성적으로, ...")
    value = st.text_input("브랜드 핵심 가치", placeholder="option")



# 광고 문구 생성 버튼을 클릭하면 아래의 prompt ask_chatgpt 에 전달 
if st.button("광고 문구 생성"):
    prompt = f'''
    아래 내용을 참고해서 광고 문구를 1~2줄짜리 광고 문구 5개를 작성해줘.
    - 제품명 : {name}
    - 브랜드 명 : {com_name}
    - 브랜드 핵심 가치 : {value}
    - 제품 특징 : {strength}
    - 톤 엔 매너 : {tone_manner}
    - 필수 포함 키워드 : {keyword}
    '''
    st.info(ask_chatgpt(prompt)) # 하늘색 배경으로 출력