from django.shortcuts import render

def index(request):
    return render(request, "yt2mp3/index.html", {
        
    })
