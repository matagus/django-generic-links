from typing import TYPE_CHECKING, Self

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

if TYPE_CHECKING:
    # Only referenced by the string forward reference in the base class below, hence the noqa:
    # ruff's F401 does not see that usage, and importing it at runtime would be circular.
    from generic_links.models import GenericLink  # noqa: F401


class GenericLinkQuerySet(models.QuerySet["GenericLink"]):
    """Queryset with the link oriented helpers exposed through ``GenericLink.objects``."""

    def internal(self) -> Self:
        """Links that are not flagged as external."""
        return self.exclude(is_external=True)

    def external(self) -> Self:
        """Links that point outside of the site."""
        return self.filter(is_external=True)

    def by_user(self, user: AbstractBaseUser | None) -> Self:
        """Links created by a given user."""
        return self.filter(user=user)
