import os
import re
from zipfile import ZipFile

import spotipy
from dotenv import load_dotenv
from pytube import Playlist, Search, YouTube, exceptions
from spotipy.oauth2 import SpotifyOAuth

# from tabulate import tabulate

# test_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2x'
# test_playlist: 'https://www.youtube.com/playlist?list=PLP3kvqg_Ut86PFpWW3orO3DXiIpK-B-GI'
# test_album:'https://open.spotify.com/album/05jbNkYoEQdjVDHEHtg1gY?si=gEMXkv9TQ_OEBMBu7whr2A'
# test_playlist_spoty: "https://open.spotify.com/playlist/5OO6uyRtTv1w6rMiKdqHPV?si=2d1a8f8ee4e04c95"

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SUCCESS = "Success"
FAILED = "Failed"
URL_REGEX_ERROR = "\n! Url does not match requested format. !"


def youtube_playlist(p_url, song_list):
    playlist = Playlist(p_url)
    for url in playlist.video_urls:
        upload_audio(url)
    return song_list


def clean_tmp():
    for folder_name, sub_folders, file_names in os.walk("yt2mp3/tmp/songs"):
        for filename in file_names:
            file_path = os.path.join(folder_name, filename)
            os.remove(file_path)


def spotify(s_url):
    auth_manager = SpotifyOAuth(scope="user-library-read")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    if re.search(r"https:\/\/open.spotify.com\/(playlist|album)\/[A-Za-z0-9?=_-]{22,}(?:$|\?)", s_url):
        if "album" in s_url:
            for song in sp.album_tracks(s_url)["items"]:
                song_name = song["name"]
                artist_name = song["artists"][0]["name"]
                vid = search_video(song_name, artist_name)
                upload_audio(vid)

        elif "playlist" in s_url:
            for song in sp.playlist_tracks(s_url)["items"]:
                song_name = song["track"]["name"]
                artist_name = song["track"]["artists"][0]["name"]
                vid = search_video(song_name, artist_name)
                upload_audio(vid)

        upload_zip()
    else:
        print(URL_REGEX_ERROR)


def search_video(song_name, artist_name):
    try:
        s = Search(f"{song_name} {artist_name}")
    except exceptions.PytubeError:
        raise ValueError("Pytube Search Error")
    else:
        result = s.results[0]
        return result.watch_url


def upload_zip():
    with ZipFile("yt2mp3/tmp/zip/songs.zip", "w") as zip_object:
        # Traverse all files in directory
        for folder_name, sub_folders, file_names in os.walk("yt2mp3/tmp/songs"):
            for filename in file_names:
                # Create filepath of files in directory
                file_path = os.path.join(folder_name, filename)
                # Add files to zip file
                zip_object.write(file_path, os.path.basename(file_path))

        if os.path.exists("yt2mp3/tmp/zip/songs.zip"):
            print("ZIP file created")
            return "songs.zip"
        else:
            print("ZIP file not created")


# !! This is the only utils function in use at the current version !!
def upload_audio(yt_url):
    if re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", yt_url):
        yt = YouTube(yt_url)
        video_title = yt.title
        stream = yt.streams.filter(only_audio=True).first()
        mp3_filename = f"{video_title}.mp3"
        stream.download(filename=mp3_filename, output_path="yt2mp3/tmp/songs")
        return mp3_filename
    else:
        print("Invlaid url:")
