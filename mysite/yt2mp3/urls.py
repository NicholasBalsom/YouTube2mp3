# Write URLs here
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("download/youtube", views.youtube, name="youtube"),
    path("download/spotify", views.spotify, name="spotify"),
    path("download_mp3/<str:mp3_filename>", views.download_mp3, name="download_mp3"),
]
