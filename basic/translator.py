import os
import time
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv


load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

#####

def trans(text, option):
    prompt = f'''
    당신은 번역기입니다. 사용자의 입력을 {option}로 번역하세요. 반드시 {option}로 번역해야 합니다. 이것은 반드시 지켜져야 합니다.
    '''
    response = client.chat.completions.create(
        model="gpt-4",
        messages = [
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


##### 
st.header("Translator")
st.image('images/ai.png', width=200)

lang_list = ("영어", "중국어", "일본어", "한국어")

col1, col2 = st.columns(2)

with col1:
    option = st.selectbox("Target Languagea", lang_list)

    response = ' '


    text = st.text_area("From")
    
    if text:
        response = trans(text, option)
    


with col2:
    st.text_area("To", value=response)


# if st.button("translate") and text:
#     response = trans(text, option)