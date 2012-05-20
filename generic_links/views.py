# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

from generic_links.forms import AddLinkForm


def add_link(request, app_model, object_id):

    app, model = app_model.split(".")
    Model = get_model(app, model)

    try:
        an_object = Model.objects.get(pk=object_id)
    except Model.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = AddForm(request.user, content_type, object_id, data=request.POST)
        if form.is_valid():
            link = form.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = AddForm(request.user, content_type, object_id)

    return render_to_response("generic_links/links/add.html",
        {"object": object, "app_model": app_model, "form": form},
        context_instance=RequestContext(request))
