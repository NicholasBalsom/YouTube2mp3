import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from . import utils
from .forms import NewSpotipyForm, NewYouTubeForm


def index(request):
    return render(request, "yt2mp3/index.html")


def youtube(request):
    if request.method == "POST":
        utils.clean_tmp()
        # Create a form with the post data
        form = NewYouTubeForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data["url"]
            mp3_filename = utils.upload_audio(url)
            print(mp3_filename)
            return render(request, "yt2mp3/youtube.html", {"file": mp3_filename})
        else:
            return render(request, "yt2mp3/youtube.html", {"message": "Video was unable to be downloaded."})

    else:
        form = NewYouTubeForm()
        return render(request, "yt2mp3/youtube.html", {"form": form})


def spotify(request):
    if request.method == "POST":
        utils.clean_tmp()
        form = NewSpotipyForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            filename = utils.spotify(url)
            return render(request, "yt2mp3/spotify.html", {"file": filename})
    else:
        form = NewSpotipyForm()
        return render(request, "yt2mp3/spotify.html", {"form": form})


def download(request, filename: str):
    if filename.endswith(".mp3"):
        path = os.path.join(settings.MEDIA_ROOT, "yt2mp3/tmp/songs", filename)
        content_type = "audio/mpeg"
    else:
        path = os.path.join(settings.MEDIA_ROOT, "yt2mp3/tmp/zip", filename)
        content_type = "application/zip"

    if os.path.exists(path):
        with open(path, "rb") as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
            return response
    else:
        return HttpResponse("File not found", status=404)
