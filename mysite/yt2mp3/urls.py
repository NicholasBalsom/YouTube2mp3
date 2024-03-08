# Write URLs here
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("download/youtube", views.youtue, nmae="youtube"),
    path("download/spotify", views.spotify, name="spotify"),
]
