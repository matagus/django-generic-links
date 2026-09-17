"""Seed the example project with artists, albums and generic links."""

from datetime import date
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Model

from generic_links.models import GenericLink
from music_app.models import Album, Artist


class Command(BaseCommand):
    help = "Create demo artists, albums and links so the example pages and the admin have something to show."

    def handle(self, *args: Any, **options: Any) -> None:
        user = self._demo_user()
        lou_reed = Artist.objects.get_or_create(
            name="Lou Reed",
            defaults={"bio": "American singer, songwriter and guitarist (1942-2013)."},
        )[0]
        nico = Artist.objects.get_or_create(
            name="Nico",
            defaults={"bio": "German singer, songwriter, actress and model."},
        )[0]

        transformer = Album.objects.get_or_create(
            title="Transformer",
            artist=lou_reed,
            defaults={"release_date": date(1972, 11, 28)},
        )[0]
        desert_hollows = Album.objects.get_or_create(
            title="The Marble Index",
            artist=nico,
            defaults={"release_date": date(1968, 11, 1)},
        )[0]

        self._add_link(
            lou_reed,
            title="Wikipedia Page",
            url="https://en.wikipedia.org/wiki/Lou_Reed",
            description="Biography, discography and references.",
            user=user,
        )
        self._add_link(
            lou_reed,
            title="Encyclopaedia Britannica",
            url="https://www.britannica.com/biography/Lou-Reed",
            user=user,
        )
        self._add_link(
            lou_reed,
            title="Lou Reed Archive (internal)",
            url="https://example.com/archives/lou-reed",
            description="Internal link: is_external is left unchecked, like in AddLinkForm.",
            is_external=False,
            user=user,
        )
        self._add_link(
            transformer,
            title="AllMusic review",
            url="https://www.allmusic.com/album/transformer-mw0000351728",
            user=user,
        )
        self._add_link(
            nico,
            title="Wikipedia Page",
            url="https://en.wikipedia.org/wiki/Nico",
            user=user,
        )
        self._add_link(
            desert_hollows,
            title="AllMusic review",
            url="https://www.allmusic.com/album/the-marble-index-mw0000196319",
            user=user,
        )

        self.stdout.write(self.style.SUCCESS("Demo data ready:"))
        for artist in Artist.objects.all():
            self.stdout.write(f"  {artist.name}: {artist.generic_links.count()} links")
        for album in Album.objects.all():
            self.stdout.write(f"  {album.title}: {album.generic_links.count()} links")

    def _demo_user(self) -> Any:
        user_model = get_user_model()
        user = user_model.objects.filter(username="admin").first()
        if user is None:
            user = user_model.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.WARNING("Created superuser admin/admin"))
        return user

    def _add_link(
        self,
        obj: Model,
        title: str,
        url: str,
        description: str = "",
        is_external: bool = True,
        user: Any = None,
    ) -> GenericLink:
        link, created = GenericLink.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            url=url,
            defaults={
                "title": title,
                "description": description,
                "is_external": is_external,
                "user": user,
            },
        )
        if not created:
            link.title = title
            link.description = description
            link.is_external = is_external
            link.user = user
            link.save()
        return link
