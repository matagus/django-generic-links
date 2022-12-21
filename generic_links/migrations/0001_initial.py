from __future__ import annotations

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GenericLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("object_id", models.PositiveIntegerField(db_index=True)),
                ("url", models.URLField()),
                ("title", models.CharField(max_length=200)),
                (
                    "description",
                    models.TextField(max_length=1000, null=True, blank=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("is_external", models.BooleanField(default=True, db_index=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        to="contenttypes.ContentType", on_delete=models.CASCADE
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Generic Link",
                "verbose_name_plural": "Generic Links",
            },
        ),
    ]
