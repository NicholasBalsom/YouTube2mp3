import os
import re

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
        data = upload_audio(url)
        song_list.append(data)
    return song_list


def spotify(s_url, song_list):
    auth_manager = SpotifyOAuth(scope="user-library-read")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    if re.search(r"https:\/\/open.spotify.com\/(playlist|album)\/[A-Za-z0-9?=_-]{22,}(?:$|\?)", s_url):
        if "album" in s_url:
            for song in sp.album_tracks(s_url)["items"]:
                song_name = song["name"]
                artist_name = song["artists"][0]["name"]
                vid = search_video(song_name, artist_name)
                data = upload_audio(vid, True)
                song_list.append(data)

        elif "playlist" in s_url:
            for song in sp.playlist_tracks(s_url)["items"]:
                song_name = song["track"]["name"]
                artist_name = song["track"]["artists"][0]["name"]
                vid = search_video(song_name, artist_name)
                data = upload_audio(vid, True)
                song_list.append(data)
    else:
        print(URL_REGEX_ERROR)
        return [["Url", "Status"], [s_url, FAILED]]

    return song_list


def search_video(song_name, artist_name):
    try:
        s = Search(f"{song_name} {artist_name}")
    except exceptions.PytubeError:
        raise ValueError("Pytube Search Error")
    else:
        result = s.results[0]
        return result.watch_url


# !! This is the only utils function in use at the current version !!
def upload_audio(yt_url):
    if re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", yt_url):
        print(f"\n>Downloading audio: {yt_url}", end="")
        yt = YouTube(yt_url)
        video_title = yt.title
        stream = yt.streams.filter(only_audio=True).first()
        mp3_filename = f"{video_title}.mp3"
        stream.download(filename=mp3_filename, output_path="yt2mp3/tmp")
        return mp3_filename
    else:
        print("Invlaid url:")
