from django.shortcuts import render

from .forms import NewSpotipyForm, NewYouTubeForm


def index(request):
    return render(request, "yt2mp3/index.html")


def youtube(request):
    if request.method == "POST":
        form = NewYouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            # file = util.youtube(url)
            # return render(request, "yt2mp3/youtube.html", {"file": file})
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
            # fileset = util.spotify(url)
            # return render()
    else:
        form = NewSpotipyForm()
        return render(request, "yt2mp3/spotify.html", {"form": form})
