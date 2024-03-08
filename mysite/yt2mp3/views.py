from django.shortcuts import render


def index(request):
    return render(request, "yt2mp3/index.html", {})


def youtube(request):
    return render(request, "yt2mp3/youtube.html")


def spotify(request):
    return render(request, "yt2mp3/spotify.html")
