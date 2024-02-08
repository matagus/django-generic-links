"""
Several useful template tags!
"""

from __future__ import annotations

from django import template
from django.db.models import Model, QuerySet

from generic_links import utils

register = template.Library()


@register.simple_tag
def get_links_for(obj: Model, is_external: bool | None = None) -> QuerySet:
    """
    Usage:

    {% get_links_for <obj> as <some_var> %}

    or

    {% get_links_for <obj> <boolean> as <some_var> %}
    """

    return utils.get_links_for(obj, is_external=is_external)
