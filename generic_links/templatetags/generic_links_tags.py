# -*- coding: utf-8 -*-
"""
Several usefull template tags!
"""
from django import template

from generic_links import utils


register = template.Library()


class RelatedLinksNode(template.Node):

    def __init__(self, context_var, obj, is_external):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)
        self.is_external = is_external

    def render(self, context):
        obj = self.obj_var.resolve(context)
        context[self.context_var] = utils.get_links_for(obj).select_related("user").filter(is_external=self.is_external)
        return u""


@register.tag
def get_links_for(parser, token):
    """
    Usage: {% get_links_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return RelatedLinksNode(bits[3], bits[1], True)
