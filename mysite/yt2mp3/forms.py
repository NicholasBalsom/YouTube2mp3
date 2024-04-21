from django import forms


# Django form for YouTube URLs
class NewYouTubeForm(forms.Form):
    url = forms.URLField(label="Video URL", widget=forms.URLInput(attrs={"class": "form"}))


# Django form for Spotify URLs
class NewSpotipyForm(forms.Form):
    url = forms.URLField(label="Spotify Album/Playlist URL")
