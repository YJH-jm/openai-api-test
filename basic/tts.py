import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

st.title("TTS-1 Model Response")

st.image("https://wikidocs.net/images/page/215361/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%84%B1%EC%9A%B0.jpg", width=200)

voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
selected = st.selectbox("목소리 선택 : ", voices)

default_text = "오늘 날씨가 너무 좋네요!"
user_prompt = st.text_area("음성으로 변환할 텍스트 입력 : ", value=default_text, height=200)


if st.button("Generate Audio"):
    response = client.audio.speech.create(
        model="tts-1", # "gpt-4o-mini-tts", "tts-1-hd"
        voice=selected,
        input = user_prompt
    )

    audio_content = response.content

    with open("temp_audio.mp3", "wb") as audio_file:
        audio_file.write(audio_content)

    # mp3 파일을 재생.
    st.audio("temp_audio.mp3", format="audio/mp3")



# response = client.audio.speech.create(
#     model="tts-1", # "gpt-4o-mini-tts", "tts-1-hd"
#     voice="alloy",
#     # input = "Today is a wonderful day to build something people love!"
#     input = "오늘은 7월 16일 수요일입니다."

# )

# with open("output_kor.mp3", "wb") as f:
#     f.write(response.content)

# save_path = "output_kor_.mp3"
# with client.audio.speech.with_streaming_response.create(
#     model="tts-1",
#     voice="alloy",
#     # input = "Today is a wonderful day to build something people love!"
#     input = "오늘은 7월 16일 수요일입니다."
# ) as response:
#     response.stream_to_file(save_path)
