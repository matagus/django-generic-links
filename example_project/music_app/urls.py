from django.urls import path

from music_app.views import AlbumDetailView, ArtistDetailView, ArtistListView

app_name = "music_app"

urlpatterns = [
    path("", ArtistListView.as_view(), name="artist_list"),
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name="artist_detail"),
    path("albums/<int:pk>/", AlbumDetailView.as_view(), name="album_detail"),
]
