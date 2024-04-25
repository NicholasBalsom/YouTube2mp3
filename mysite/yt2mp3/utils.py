import os
import re

import spotipy
from dotenv import load_dotenv
from pytube import Playlist, Search, YouTube, exceptions
from spotipy.oauth2 import SpotifyOAuth
from tabulate import tabulate

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
# gets the user directory using expanduser, and replaces all \ with / (for ease of access)
USER_DIRECTORY = os.path.expanduser("~").replace("\\", "/")

COMMANDS = [
    ["Download Options", "key"],
    ["Single Video", "1"],
    ["YouTube Playlist", "2"],
    ["Spotify", "3"],
    ["Exit", "x"],
]


def main():
    # main loop for inputting commands
    while True:
        # defines a list with placeholder video name and status
        downloaded_songs = [["Video name", "Status"]]
        print("\nDownload from YouTube and Spotify")
        # creates a table with possible commands
        print(tabulate(COMMANDS, headers="firstrow", tablefmt="rounded_outline"))
        cmd = input(">Option: ").lower().strip()
        # calls the video function and creates a table with the titles and statuses of downloaded songs
        if cmd == "1":
            print(
                "\n\n"
                + tabulate(
                    video(input(">Video Url: "), downloaded_songs), headers="firstrow", showindex="always"
                )
                + "\n"
            )
        # calls the youtube_playlist function and creates a table with the titles and statuses of downloaded songs
        elif cmd == "2":
            try:
                print(
                    "\n\n"
                    + tabulate(
                        youtube_playlist(input(">Playlist Url: "), downloaded_songs),
                        headers="firstrow",
                        showindex="always",
                    )
                    + "\n"
                )
            except KeyError:
                print("\n! Download Failed. Check url and try again !")
        # calls the spotify function and creates a table with the titles and statuses of downloaded songs
        elif cmd == "3":
            print(
                "\n\n"
                + tabulate(
                    spotify(input(">Spotify Playlist/Album Url: "), downloaded_songs),
                    headers="firstrow",
                    showindex="always",
                )
                + "\n"
            )
        elif cmd == "x":
            break
        else:
            print("! Enter a valid key !")

        if input("\n>Press Enter to continue (x to quit): ").lower().strip() == "x":
            break
        print()


# custom exceptions for handling incorrect inputs
class InputError(Exception):
    pass


def video(url, song_list):
    try:
        data = download_audio(url)
        song_list.append(data)
        return song_list
    except InputError:
        pass


# def youtube_playlist(p_url, song_list):

#             filter_choice = False
#         playlist = Playlist(p_url)
#         for url in playlist.video_urls:
#             data = download_audio(url, filter_choice)
#             song_list.append(data)
#         return song_list
#     except InputError:
#         pass


def spotify(s_url, song_list):
    auth_manager = SpotifyOAuth(scope="user-library-read")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    if re.search(r"https:\/\/open.spotify.com\/(playlist|album)\/[A-Za-z0-9?=_-]{22,}(?:$|\?)", s_url):
        if "album" in s_url:
            for song in sp.album_tracks(s_url)["items"]:
                song_name = song["name"]
                artist_name = song["artists"][0]["name"]
                vid = search_video(song_name, artist_name)
                data = download_audio(vid, True)
                song_list.append(data)

        elif "playlist" in s_url:
            for song in sp.playlist_tracks(s_url)["items"]:
                song_name = song["track"]["name"]
                artist_name = song["track"]["artists"][0]["name"]
                vid = search_video(song_name, artist_name)
                data = download_audio(vid, True)
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


# defines a function for downloading from yt, takes url and video/audio choice as input
def download_audio(yt_url):
    if re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", yt_url):
        print(f"\n>Downloading audio: {yt_url}", end="")
        yt = YouTube(yt_url)
        video_title = yt.title
        stream = yt.streams.filter(only_audio=True).first()
        mp3_filename = f"{video_title}.mp3"
        stream.download(filename=mp3_filename, output_path="tmp")
        return mp3_filename
    else:
        print("Did NOT WORK GAGAGGW")


if __name__ == "__main__":
    main()
