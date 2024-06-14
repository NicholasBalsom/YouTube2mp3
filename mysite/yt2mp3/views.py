import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from . import utils
from .forms import NewSpotipyForm, NewYouTubeForm


# Home page
def index(request):
    return render(request, "yt2mp3/index.html")


def youtube(request):
    if request.method == "POST":
        utils.clean_tmp()

        # Create a form with the post data
        form = NewYouTubeForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data["url"]  # get the url
            mp3_filename = utils.upload_audio(url)  # upload the mp3 and get the filename
            return render(request, "yt2mp3/youtube.html", {"file": mp3_filename})
        else:
            return render(request, "yt2mp3/youtube.html", {"message": "Video was unable to be downloaded."})

    else:
        # Create new form
        form = NewYouTubeForm()
        return render(request, "yt2mp3/youtube.html", {"form": form})


def spotify(request):
    if request.method == "POST":
        utils.clean_tmp()
        # # Create a form object with the post data
        form = NewSpotipyForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]  # get url
            filename = utils.spotify(url)  # download the audio(s) using spotify utils
            return render(request, "yt2mp3/spotify.html", {"file": filename})
    else:
        # Create a new form
        form = NewSpotipyForm()
        return render(request, "yt2mp3/spotify.html", {"form": form})


# Not a view, is used to download files from your browser
def download(request, filename: str):
    if filename.endswith(".mp3"):
        # get path to uploaded files (web server)
        path = os.path.join(settings.MEDIA_ROOT, "yt2mp3/tmp/songs", filename)
        content_type = "audio/mpeg"
    else:
        # get path to uploaded files (web server)
        path = os.path.join(settings.MEDIA_ROOT, "yt2mp3/tmp/zip", filename)
        content_type = "application/zip"

    if os.path.exists(path):
        with open(path, "rb") as file:
            # Create a response to download the file
            response = HttpResponse(file.read(), content_type=content_type)
            response["Content-Disposition"] = f"attachment; filename='{filename}'"
            return response
    else:
        return HttpResponse("File not found", status=404)
