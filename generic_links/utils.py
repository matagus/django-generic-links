from django.db.models import Model, QuerySet

from generic_links.models import GenericLink


def get_links_for(obj: Model, is_external: bool | None = None) -> QuerySet[GenericLink]:
    """
    Returns a queryset with all instances of GenericLink for a given object

    Pass ``is_external`` to narrow the queryset down to external (``True``) or
    internal (``False``) links only.
    """

    params: dict[str, object] = {
        "object_id": obj.pk,
        "content_type__app_label": obj._meta.app_label,
        "content_type__model": obj._meta.model_name,
    }

    if is_external is not None:
        params["is_external"] = is_external

    return GenericLink.objects.filter(**params).select_related("user")
