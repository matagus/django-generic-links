# -*- coding: UTF-8 -*-
from django import forms

from generic_links.models import GenericLink


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = GenericLink
        fields = ("title", "url", "description", "is_external")

    def __init__(self, user, content_type, object_id, *args, **kwargs):
        self.user = user
        self.content_type = content_type
        self.object_id = object_id
        super(AddLinkForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance = GenericLink.objects.create(
            content_type=self.content_type, object_id=self.object_id,
            url=self.cleaned_data["url"].strip(),
            title=self.cleaned_data["title"], user=self.user,
            is_external=self.cleaned_data["is_external"])

        return self.instance

