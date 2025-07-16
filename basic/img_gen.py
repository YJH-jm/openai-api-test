import os
import io
import base64
from PIL import Image

import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)



def get_image(prompt):
    response = draw_image(prompt)
    img_data = base64.b64decode(response)
    img = Image.open(io.BytesIO(img_data))
    return img



def draw_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality='standard',
        response_format="b64_json",
        n=1
    )

    return response.data[0].b64_json

st.title("Dall-E 이미지 그리기")
st.image('https://wikidocs.net/images/page/215361/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%ED%99%94%EA%B0%80.png')

st.text("🎨 원하는 그림 설명해줘. 묘사가 자세할 수록 더 좋아")
input_text = st.text_area("원하는 이미지의 설명을 영어 또는 한글로 기입.", height=200)

if st.button("Generate"):

    if input_text:
        try:
            image = get_image(input_text)
            st.image(image)
        except:
            st.error("요청 오류 발생")
    else:
        st.warning("텍스트 입력!")


# response = client.images.generate(
#     model="dall-e-3", # 이 버전부터 한글로도 작동 함
#     prompt = "귀여운 하얀색 샴 고양이",
#     size='1024x1024',
#     quality='standard',
#     response_format='b64_json', # base64로 encoding 된 데이터 
#     n=1
# )


# img_data = base64.b64decode(response.data[0].b64_json)
# img = Image.open(io.BytesIO(img_data))
# img.show()