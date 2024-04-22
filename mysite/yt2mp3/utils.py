import os
import re
from pathlib import Path

import spotipy
from dotenv import load_dotenv
from pytube import Playlist, Search, YouTube, exceptions
from spotipy.oauth2 import SpotifyOAuth


def download_audio(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    stream = yt.streams.filter(only_audio=True).first()
    mp3_filename = f"{video_title}.mp3"
    stream.download(filename=mp3_filename, output_path="tmp")
    return mp3_filename
