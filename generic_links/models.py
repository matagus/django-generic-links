from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import GenericLinkQuerySet

DESCRIPTION_MAX_LENGTH = 1000


class GenericLink(models.Model):
    """
    Relates an object with an url and its data
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        # TextField does not add a MaxLengthValidator the way CharField does, so
        # without this the declared max_length is only enforced by ModelForms and
        # full_clean() would accept arbitrarily long values.
        validators=[MaxLengthValidator(DESCRIPTION_MAX_LENGTH)],
        null=True,
        blank=True,
    )

    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    is_external = models.BooleanField(default=True, db_index=True)

    objects = GenericLinkQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Generic Link")
        verbose_name_plural = _("Generic Links")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} :: {self.url}"
