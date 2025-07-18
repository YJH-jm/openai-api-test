import os
import subprocess
# from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import logging

def convert_to_mp3(input_path, output_path):
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path, "-vn", "-acodec", "libmp3lame", output_path
    ])


def repackage_video_safe(input_path):
    base, _ = os.path.splitext(input_path)
    output_path = base + ".mp4"
    tmp_path = base + "_tmp.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-c", "copy",
        "-movflags", "+faststart",
        tmp_path
    ])
    os.remove(input_path)
    os.rename(tmp_path, output_path)
    return output_path
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


url = "https://www.youtube.com/watch?v=wc58c20T8SI"
get_video_audio(url)