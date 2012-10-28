# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.http import Http404
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType

from generic_links.forms import AddLinkForm


def add_link(request, app_model, object_id):

    app, model = app_model.split(".")
    Model = get_model(app, model)

    try:
        an_object = Model.objects.get(pk=object_id)
    except Model.DoesNotExist:
        raise Http404

    content_type = ContentType.objects.get(app_label=app, model=model)

    if request.method == "POST":
        form = AddLinkForm(request.user, content_type, object_id, data=request.POST)
        if form.is_valid():
            link = form.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = AddLinkForm(request.user, content_type, object_id)

    return render_to_response("generic_links/add.html",
        {"object": an_object, "app_model": app_model, "form": form},
        context_instance=RequestContext(request))
