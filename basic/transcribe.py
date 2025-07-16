import os
import subprocess
# from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

# mp3 파일로부터 자막 파일(srt) 형식의 문자열을 반환
def get_transcribe(file_path):
    with open(file_path,"rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="srt",
            file=audio_file
        )

        return response


def convert_to_mp3(input_path, output_path):
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path, "-vn", "-acodec", "libmp3lame", output_path
    ])


# Youtube 주소 입력받으면 동영상 (mp4), 음성 (mp3) 추출하는 함수
def get_video_audio(url):

    yt = YouTube(url, on_progress_callback=on_progress)

    # 음성 추출
    audio = yt.streams.filter(only_audio=True).first()
    audio_file = audio.download(output_path='.')
    base, ext = os.path.splitext(audio_file)
    new_audio_file = base + ".mp3"
    # os.rename(audio_file, new_audio_file)
    convert_to_mp3(audio_file, new_audio_file)
    os.remove(audio_file)

    # 영상 추출
    video = yt.streams.filter(file_extension="mp4").get_highest_resolution()
    video_file = video.download(output_path='.')

    # 파일 크기 측정하기 위한 코드
    audio_file_stats = os.stat(new_audio_file)
    video_file_stats = os.stat(video_file)
    logging.info(f"Size of audio file in Bytes : {audio_file_stats.st_size}")
    logging.info(f"Size of vidoe file in Bytes : {video_file_stats.st_size}")

    return new_audio_file, video_file


st.title("Youtube Vidoe and Subtitle Downloader")
url = st.text_input("Enter the Youtude URL")

if st.button("Download"):
    if url:
        try:
            audio_file, video_file = get_video_audio(url)
            result = get_transcribe(audio_file)
            subtitle_file = os.path.join(os.path.dirname(__file__), "result" ,"subtitle.srt")
            with open(subtitle_file, "w", encoding="utf-8") as file:
                file.write(result)

            st.success("Transcribe Success")

            video_file_path = os.path.abspath(video_file)
            st.markdown(f"** 비디오 파일이 저장됨 : ** `{video_file_path}`")
            st.video(video_file)


            subtitle_file_path = os.path.abspath(subtitle_file)
            st.markdown(f'**자막 파일이 저장됨 :** `{subtitle_file_path}`')
            with open(subtitle_file, "r", encoding="utf-8") as file:
                subtitles = file.read()
                st.info(subtitles)
        except Exception as e:
            st.error(f'Error ; {e}')


