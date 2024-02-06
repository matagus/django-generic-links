from __future__ import annotations

from generic_links.models import GenericLink


def get_links_for(obj, is_external=None):
    """
    Returns a queryset with all instances of GenericLink for a given object
    """

    params = {
        "object_id": obj.id,
        "content_type__app_label": obj._meta.app_label,
        "content_type__model": obj._meta.model_name,
    }

    if is_external is not None:
        params["is_external"] = is_external

    return GenericLink.objects.filter(**params).select_related("user")
