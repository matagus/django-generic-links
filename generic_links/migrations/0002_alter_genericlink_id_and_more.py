# Generated by Django 5.0.1 on 2024-02-10 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("generic_links", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="genericlink",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AddIndex(
            model_name="genericlink",
            index=models.Index(fields=["content_type", "object_id"], name="generic_lin_content_569ecc_idx"),
        ),
    ]
