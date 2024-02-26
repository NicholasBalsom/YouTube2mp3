# pip install pytube
from pytube import YouTube
import os
from pathlib import Path


def get_title(url):
    try:
        yt = YouTube(url)
        return yt.title
    except:
        return url


def convert(urlist, outdir):
    for url in urlist:
        yt = YouTube(url)
        
        # Extract audio            Quality vv
        video = yt.streams.filter(only_audio=True, abr="160kbps").last()

        # Download file
        out_file = video.download(output_path=outdir)
        base, ext = os.path.splitext(out_file)                   
        new_file = Path(f"{base}.mp3")
        os.rename(out_file, new_file)
        # check that the file was created
        if new_file.exists():
            print(f"{yt.title} has been successfully downloaded.")
        else:
            print(f"{yt.title}could not be downloaded.")
            raise ValueError("File could not be downloaded")


def main():
    urlist = []
    outdir = input("Enter download directory (leave empty for default): ")
    if outdir == "":
        outdir = "YouTube2mp3/Songs"

    while True:
        url = input("Enter YouTube url (leave empty to continue): ")
        if url == "":
            break
        else:
            urlist.append(url)

    convert(urlist, outdir)



if __name__ == "__main__":
    main()
