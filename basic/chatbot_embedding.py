import os
import pandas as pd
import numpy as np
import ast
from openai import OpenAI
import streamlit as st
from streamlit_chat import message
from tqdm import tqdm
from dotenv import load_dotenv

tqdm.pandas()
load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

def get_embedding(text):
    response = client.embeddings.create(
        model = "text-embedding-ada-002",
        input = text,
    )

    return response.data[0].embedding



file_path = os.path.join(os.path.dirname(__file__), "data", "embedding.csv")

if os.path.isfile(file_path):
    print(f"{os.path.basename(file_path)} 파일 존재")
    df = pd.read_csv(file_path)
    df['embedding'] = df["embedding"].progress_apply(ast.literal_eval)
else: 
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data", "ChatBotData.csv"))
    df["embedding"] = df.progress_apply(lambda row: get_embedding(row.Q), axis=1)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')


def cos_sim(A, B):
    return np.dot(A, B) / (np.linalg.norm(A)*np.linalg.norm(B))

def get_sim_answer(input):
    embedding = get_embedding(input)
    df["score"] = df.progress_apply(lambda x : cos_sim(x["embedding"], embedding), axis=1)
    return df.loc[df["score"].idxmax()]['A']


st.title("고민 해결 대화 😀")
st.image(os.path.join(os.path.dirname(__file__),"images","ask_me_chatbot_logo.png"))

if 'generated' not in st.session_state: # 화면에 보여주기 위해 챗봇 답변을 저장할 공간 할당
    st.session_state["generated"] = []

if "past" not in st.session_state: # 화면에 보여주기 위해 사용자의 질문? 답변 저장할 공간 할당
    st.session_state["past"] = []


with st.form("form", clear_on_submit=True): # 사용자의 입력이 들어오면 user_input에 저장하고, Send 버튼 클릭하면 submitted 값 True 변환
    user_input = st.text_input("대화를 시작해보세요!", "", key="input")
    submitted = st.form_submit_button("Send")



if submitted and user_input: 
    chatbot_response = get_sim_answer(user_input)
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(chatbot_response)


if st.session_state['generated']:
    for i in reversed(range(len(st.session_state["generated"]))):
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(st.session_state['generated'][i], key=f"{i}")