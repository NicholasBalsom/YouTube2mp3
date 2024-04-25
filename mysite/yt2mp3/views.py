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
        # Create a form with the post data
        form = NewYouTubeForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data["url"]
            mp3_filename = utils.download_audio(url)
            print(mp3_filename)
            return render(request, "yt2mp3/youtube.html", {"file": mp3_filename})
        else:
            return render(request, "yt2mp3/youtube.html", {"message": "Video was unable to be downloaded."})

    else:
        form = NewYouTubeForm()
        return render(request, "yt2mp3/youtube.html", {"form": form})


def spotify(request):
    if request.method == "POST":
        form = NewSpotipyForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            # fileset = utils.spotify(url)
            # return render()
    else:
        form = NewSpotipyForm()
        return render(request, "yt2mp3/spotify.html", {"form": form})


def download(request, mp3_filename):
    mp3_path = os.path.join(settings.MEDIA_ROOT, "tmp", mp3_filename)
    if os.path.exists(mp3_path):
        with open(mp3_path, "rb") as mp3_file:
            response = HttpResponse(mp3_file.read(), content_type="audio/mpeg")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(mp3_filename)
            return response
    else:
        return HttpResponse("MP3 file not found", status=404)
