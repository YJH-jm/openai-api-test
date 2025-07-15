import os 
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key = API_KEY)




def describe(image_url):
    response = client.chat.completions.create(
    # model="gpt-4-vision-preview", 
    model = "gpt-4o", 
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": "이 이미지에 대해서 알려줘" # gpt-4o에 요청하는 prompt, 이 부분 수정 가능
                },
                {
                    "type" : "image_url",
                    "image_url" : {"url": image_url}
                }
            ]
        }
    ],
   
    max_tokens=1024,
    )
    return response.choices[0].message.content

st.title("gpt-4o : 이미지 설명") # 웹 사이트 상단에서 사용

input_url = st.text_area("여기에 이미지 주소 입력 하세요: ", height=68) # 사용자 입력을 받는 text 칸

if st.button("이미지 설명"): # st.button()을 클릭하는 순간 st.button()의 값은 True

    if input_url: # st.text_area() 값이 존재하면 input_url의 값이 True
        try:
            st.image(input_url, width=300) # # st.image()는 기본적으로 이미지 주소로부터 이미지를 웹 사이트 화면에 생성
            
            result = describe(input_url)

            st.success(result) # st.success()는 텍스트를 웹 사이트 화면에 출력, 초록색 배경
        except:
            st.error("요청 오류가 발생")
    else:
        st.warning("텍스트 입력 필요!") # 화면 상으로 노란색 배경으로 출력