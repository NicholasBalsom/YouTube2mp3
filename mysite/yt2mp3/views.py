from django.shortcuts import render

from . import utils
from .forms import NewSpotipyForm, NewYouTubeForm


# Home page view
def index(request):
    return render(request, "yt2mp3/index.html")


# YouTube download view
def youtube(request):
    # If form is submitted with methood = 'post'
    if request.method == "POST":
        # Create a form with the post data
        form = NewYouTubeForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data["url"]
            # file = utils.youtube(url)
            # return render(request, "yt2mp3/youtube.html", {"file": file})
        else:
            return render(request, "yt2mp3/youtube.html", {"message": "Video was unable to be downloaded."})

    else:
        # Create a new blank form object
        form = NewYouTubeForm()
        return render(request, "yt2mp3/youtube.html", {"form": form})


# Spotify download view
def spotify(request):
    # If form is submitted with methood = 'post'
    if request.method == "POST":
        form = NewSpotipyForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            # fileset = utils.spotify(url)
            # return render()
    else:
        # Create a new blank spotipyform object
        form = NewSpotipyForm()
        return render(request, "yt2mp3/spotify.html", {"form": form})
