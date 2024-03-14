from django import forms


class NewYouTubeForm(forms.Form):
    url = forms.URLField(label="Video URL")


class NewSpotipyForm(forms.Form):
    url = forms.URLField(label="Spotify Album/Playlist URL")
