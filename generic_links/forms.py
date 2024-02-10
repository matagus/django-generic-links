from __future__ import annotations

from django import forms

from generic_links.models import GenericLink


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = GenericLink
        fields = ("title", "url", "description", "is_external")

    def __init__(self, content_object, user, *args, **kwargs):
        self.content_object = content_object
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance = GenericLink.objects.create(
            content_object=self.content_object,
            url=self.cleaned_data["url"].strip(),
            title=self.cleaned_data["title"],
            user=self.user,
            is_external=self.cleaned_data["is_external"],
        )
        self.instance.save()
        return self.instance
