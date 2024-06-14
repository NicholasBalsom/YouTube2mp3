import os
import re
from zipfile import ZipFile

import spotipy
from dotenv import load_dotenv
from pytube import Playlist, Search, YouTube, exceptions
from spotipy.oauth2 import SpotifyOAuth

# test_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2x'
# test_playlist: 'https://www.youtube.com/playlist?list=PLP3kvqg_Ut86PFpWW3orO3DXiIpK-B-GI'
# test_album:'https://open.spotify.com/album/05jbNkYoEQdjVDHEHtg1gY?si=gEMXkv9TQ_OEBMBu7whr2A'
# test_playlist_spoty: "https://open.spotify.com/playlist/5OO6uyRtTv1w6rMiKdqHPV?si=2d1a8f8ee4e04c95"


# Load environment variables from .env
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

URL_REGEX_ERROR = "\n! Url does not match requested format. !"


# Used for removing temprary files in tmp/ folder
def clean_tmp():
    # Traverse songs directory
    for folder_name, sub_folders, file_names in os.walk("yt2mp3/tmp/songs"):
        # Delete each file in the songs directory
        for filename in file_names:
            file_path = os.path.join(folder_name, filename)
            os.remove(file_path)


def spotify(s_url):
    # Authorize access to the Spotify API
    auth_manager = SpotifyOAuth(scope="user-library-read")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Confifim that the imputted url is a valid spotify URL
    if re.search(r"https:\/\/open.spotify.com\/(playlist|album|track)\/[A-Za-z0-9?=_-]{22,}(?:$|\?)", s_url):
        # For Spotify Albums
        if "album" in s_url:
            for song in sp.album_tracks(s_url)["items"]:
                song_name = song["name"]  # Get song name
                artist_name = song["artists"][0]["name"]  # Get the first artists name
                vid = search_video(song_name, artist_name)
                upload_audio(vid)
            return upload_zip()

        # For Spotify Playlists
        elif "playlist" in s_url:
            for song in sp.playlist_tracks(s_url)["items"]:
                song_name = song["track"]["name"]  # Song name
                artist_name = song["track"]["artists"][0]["name"]  # Get first artists name
                vid = search_video(song_name, artist_name)
                upload_audio(vid)
            return upload_zip()

        # For  single Spotify song links
        elif "track" in s_url:
            track = sp.track(s_url)
            song_name = track["name"]  # Song name
            artist_name = track["artists"][0]["name"]  # First artist name
            vid = search_video(song_name, artist_name)
            return upload_audio(vid)

    else:
        print(URL_REGEX_ERROR)


# Searches up songs on YouTube for downloading
def search_video(song_name, artist_name):
    try:
        # Try searching the song
        s = Search(f"{song_name} {artist_name}")
    except exceptions.PytubeError:
        raise ValueError("Pytube Search Error")
    else:
        result = s.results[0]  # take first result
        return result.watch_url  # Return the url


def upload_zip():
    # If a zip folder doesnt exsist in tmp/ create one
    if not os.path.exists("yt2mp3/tmp/zip"):
        os.makedirs("yt2mp3/tmp/zip")

    with ZipFile("yt2mp3/tmp/zip/songs.zip", "w") as zip_object:
        # Traverse the songs directory
        for folder_name, sub_folders, file_names in os.walk("yt2mp3/tmp/songs"):
            for filename in file_names:
                # Create filepath
                file_path = os.path.join(folder_name, filename)
                # Add files to zip file
                zip_object.write(file_path, os.path.basename(file_path))

        # Check to make sure the zip file exists
        if os.path.exists("yt2mp3/tmp/zip/songs.zip"):
            print("ZIP file created")
            return "songs.zip"  # Return zip file name
        else:
            print("ZIP file not created")


def upload_audio(yt_url):
    # Validate the youtube url
    if re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", yt_url):
        yt = YouTube(yt_url)
        video_title = re.sub(r"[^\w\-_\. ]", "_", yt.title)  # Get title and remove and unessisary characters
        stream = yt.streams.filter(only_audio=True).first()  # Get audio from video
        mp3_filename = f"{video_title}.mp3"
        stream.download(filename=mp3_filename, output_path="yt2mp3/tmp/songs")  # Download to web server
        return mp3_filename
    else:
        print("Invlaid url:")
