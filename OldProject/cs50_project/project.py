
'''
Title: Audio Extractor/Downloader
Name: Nicholas Balsom
From: Corner Brook, Newfoundland, Canada
'''


# test_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2x'
# test_playlist: 'https://www.youtube.com/playlist?list=PLP3kvqg_Ut86PFpWW3orO3DXiIpK-B-GI'
# test_album:'https://open.spotify.com/album/05jbNkYoEQdjVDHEHtg1gY?si=gEMXkv9TQ_OEBMBu7whr2A'
# test_playlist_spoty: "https://open.spotify.com/playlist/5OO6uyRtTv1w6rMiKdqHPV?si=2d1a8f8ee4e04c95"


from pytube import YouTube
from pytube import Playlist
from pytube import Search
from pytube import exceptions
from pathlib import Path
from tabulate import tabulate
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import re
import os


load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SUCCESS = "Success"
FAILED = "Failed"
URL_REGEX_ERROR = "\n! Url does not match requested format. !"

COMMANDS = [
    ["Download Options", "key"],
    ["Single Video", "1"],
    ["YouTube Playlist", "2"],
    ["Spotify", "3"],
    ["Exit", "x"]
    ]


def main():
    print("\n!!!WARNING: DOWNLOADING AUDIO WILL OVERWRITE ANY AUDIO FILE WITH THE SAME NAME IN DOWNLOADS FOLDER")
    while True:
        downloaded_songs = [["Video name", "Status"]]
        print("\nDownload Audio from YouTube and Spotify")
        print(tabulate(COMMANDS, headers="firstrow", tablefmt="rounded_outline"))
        cmd = input(">Option: ").lower().strip()
        if cmd == "1":
            print("\n\n" + tabulate(video(input(">Video Url: "), downloaded_songs), headers="firstrow", showindex="always") + "\n" )
        elif cmd == "2":
            try:
                print("\n\n" + tabulate(youtube_playlist(input(">Playlist Url: "), downloaded_songs), headers="firstrow", showindex="always") + "\n" )
            except KeyError:
                print("\n! Download Failed. Check url and try again !")
        elif cmd == "3":
            print("\n\n" + tabulate(spotify(input(">Spotify Playlist/Album Url: "), downloaded_songs), headers="firstrow", showindex="always") + "\n" )
        elif cmd == "x":
            break
        else:
            print("! Enter a valid key !")

        if input("\n>Press Enter to continue (x to quit): ").lower().strip() == "x":
            break
        print()


def video(url, song_list):
    data = download_audio(url)
    song_list.append(data)
    return song_list


def youtube_playlist(p_url, song_list):
    playlist = Playlist(p_url)
    for url in playlist.video_urls:
        data = download_audio(url)
        song_list.append(data)
    return song_list


def spotify(s_url, song_list):
    auth_manager = SpotifyOAuth(scope="user-library-read")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    if re.search(r"https:\/\/open.spotify.com\/(playlist|album)\/[A-Za-z0-9?=_-]{22,}(?:$|\?)", s_url):
        if "album" in s_url:
            for song in sp.album_tracks(s_url)['items']:
                song_name =  song['name']
                artist_name = song['artists'][0]['name']
                vid = search_video(song_name, artist_name)
                data = download_audio(vid)
                song_list.append(data)

        elif "playlist" in s_url:
            for song in sp.playlist_tracks(s_url)['items']:
                song_name = song['track']['name']
                artist_name = song['track']['artists'][0]['name']
                vid = search_video(song_name, artist_name)
                data = download_audio(vid)
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


def download_audio(yt_url):
    if re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", yt_url):
        print(f"\n>Downloading audio: {yt_url}", end="")
        try:
            yt = YouTube(yt_url)
        except exceptions.VideoUnavailable:
            print(f"Video: {yt_url} is unavailable")
        else:
            audio = yt.streams.filter(only_audio=True).first()
            d_file = audio.download(output_path="Downloads")
            file_name = os.path.basename(d_file)
            if " " in file_name:
                new_file_name = file_name.replace(" ", "_")
                new_file = Path(f"{os.path.dirname(d_file)}/{new_file_name}")
                os.rename(d_file, new_file)

            if Path(d_file).exists() or Path(new_file).exists():
                return [yt.title, SUCCESS]
            else:
                return [yt.title, FAILED]
    else:
        print(URL_REGEX_ERROR)
    return [yt_url, FAILED]


if __name__ == "__main__":
    main()