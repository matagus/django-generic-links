# -*- coding: UTF-8 -*-
from generic_links.models import GenericLink


def get_links_for(obj, is_external=None):
    """
    Returns a queryset with all instances of GenericLink for a given object
    """

    params = dict(object_id=obj.id, content_type__app_label=obj._meta.app_label,
        content_type__model=obj._meta.model_name)

    if not (is_external is None):
        params["is_external"] = is_external

    return GenericLink.objects.filter(**params)
