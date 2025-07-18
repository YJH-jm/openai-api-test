import os 
import uuid
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)


#####

def auth():
    os.environ['OPENAI_API_KEY'] = st.session_state.openai_api_key
    st.session_state.genreBox_state = False
    st.session_state.apiBox_state = True



def get_story_and_image(user_choice):
    '''
    user_choice: str
        이전 선택지에서 사용자가 선택한 보기

    '''
    client = OpenAI() # Dalle 사용
    llm_model = get_llm() # 스토리 전개를위해 ChatGPT 셋팅하는 함수, 프롬프트도 작성 되어있음

    llm_generation_result = llm_model.predict(input=user_choice)

    response_list = llm_generation_result.split("\n")

    # if len(response_list) != 1: # Dalle prompt 추출


######
st.set_page_config(
    page_title = 'NovelGPT',
    layout='wide',
    menu_items={
          'About': "NovelGPT is an interactive storybook experience using ChatGPT and Dalle"
    },
    initial_sidebar_state='expanded'
)

st.title(f"NovelGPT")



# 1. st.session 초기화


## 스토리 전개 시 각 part의 데이터를 저장할 리스트
if 'data_dict' not in st.session_state:
    st.session_state['data_dict'] = {}


## 문자열 난수를 저장할 문자열 리스트. 스토리전개 시 각 난수는 각 part의 key 역할을 함
if 'oid_list' not in st.session_state:
    st.session_state['oid_list'] = []

## 사용자가 OpenAI API Key 값 작성하면 저장될 변수
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''

## 사용자가 OpenAI API Key 값을 작성하는 칸의 활성화 여부, API Key 입력되기 전까지는 비활성화
if 'apiBox_state' not in st.session_state:
    st.session_state['apiBox_state'] = False

## 사용자가 첫 시작 시 주인공 또는 줄거리를 작성하면 저장 될 변수, 기본 값은 '아기 펭귄 보물이의 모험'
if 'genre_input' not in st.session_state:
    st.session_state['genre_input'] = '아기 펭귄 보물이의 모험'

## 사용자가 첫 시작 시 주인공 또는 줄거리를 작성하는 칸의 활성화 여부, OpenAI API 값이 입력되기 전까지 비활성화 (True)
if 'genreBox_state' not in st.session_state:
    st.session_state['genreBox_state'] = True


with st.sidebar:
    st.header("NovelGPT")

    st.markdown(
        '''
        NovelGPT는 소설을 작성하는 인공지능입니다. GPT-4와 Dalle를 사용하여 스토리가 진행됩니다.
        '''
    )
    st.info('**Note:** OpenAI API Key를 입력하세요.')

    with st.form(key='API KEYS'):
        openai_key = st.text_input(
            label="OpenAI API Key",
            key = "openai_api_key", # 입력 필드의 값을 st.session_state["openai_api_key"] 으로 저장
            type='password',
            disabled = st.session_state.apiBox_state, 
            help='OpenAI API key은 https://platform.openai.com/account/api-keys 에서 발급 가능합니다.'
        )

        btn = st.form_submit_button(label='Submit', on_click=auth)


    with st.expander('더 많은 예시 보러 가기'):
        st.write('[OpenAI API 강의](https://www.example.example_com)')


    
# 시작 시 OpenAI API Key값이 입력되지 않은 경우 경고 문구를 출력합니다.
if not openai_key.startswith('sk-'):
    st.warning("OpenAI API Key가 입력되지 않았습니다.", icon='⚠')


