from django.views.generic import DetailView, ListView

from music_app.models import Album, Artist


class ArtistListView(ListView):
    model = Artist
    template_name = "music_app/artist_list.html"
    context_object_name = "artists"


class ArtistDetailView(DetailView):
    model = Artist
    template_name = "music_app/artist_detail.html"
    context_object_name = "artist"


class AlbumDetailView(DetailView):
    model = Album
    template_name = "music_app/album_detail.html"
    context_object_name = "album"
