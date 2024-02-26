from project import video, youtube_playlist, spotify, search_video, download_audio
import pytest
import warnings


url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2x'
bad_url = 'https://www.youtube.com/watch?v=dQw4w9Wg'

playlist = 'https://www.youtube.com/playlist?list=PLP3kvqg_Ut86PFpWW3orO3DXiIpK-B-GI'
bad_playlist = 'https://www.youtube.com/playlist?list='

album_spotify = 'https://open.spotify.com/album/05jbNkYoEQdjVDHEHtg1gY?si=gEMXkv9TQ_OEBMBu7whr2A'
playlist_spotify = 'https://open.spotify.com/playlist/5OO6uyRtTv1w6rMiKdqHPV?si=2d1a8f8ee4e04c95'

song_name = "Never gonna give you up"
artist_name = "Rick Astley"

song_list = [["Video name", "Status"]]



def test_video():
    results = video(url, song_list)
    assert len(results) == 2
    assert results[1][1] == "Success"


def test_playlist():
    results = youtube_playlist(playlist, song_list)
    assert len(results) >= 2
    for i in results[1:]:
        assert i[1] == "Success"
    with pytest.raises(KeyError):
        youtube_playlist(bad_playlist, song_list)



def test_spotify():
    warnings.filterwarnings("ignore")
    a_results_success = spotify(album_spotify, song_list)
    p_results_success = spotify(playlist_spotify, song_list)
    results_fail = spotify("https://open.spotify.com/playlist/", song_list)
    assert len(a_results_success) >= 2
    assert len(p_results_success) >= 2
    for i in a_results_success[1:]:
        assert i[1] == "Success"
    for i in p_results_success[1:]:
        assert i[1] == "Success"
    assert results_fail[1][1] == "Failed"



def test_search_video():
    result = search_video(song_name, artist_name)
    assert result is not None
    assert type(result) == str


def test_downdload_audio():
    result = download_audio(url)
    assert len(result) > 0
    assert result[1] == "Success"
    assert download_audio(bad_url) == [bad_url, "Failed"]
    assert download_audio("a") == ["a", "Failed"]
