from typing import Any

from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Model

from generic_links.models import GenericLink


class AddLinkForm(forms.ModelForm):
    # The model default is True, so unbound forms render the checkbox checked.
    # Note: HTML checkboxes are absent from POST data when unchecked, so a
    # submitted form without the checkbox saves is_external=False.
    is_external = forms.BooleanField(initial=True, required=False)

    content_object: Model
    user: AbstractBaseUser | None

    class Meta:
        model = GenericLink
        fields = ("title", "url", "description", "is_external")

    def __init__(self, content_object: Model, user: AbstractBaseUser | None, *args: Any, **kwargs: Any) -> None:
        self.content_object = content_object
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> GenericLink:
        link: GenericLink = super().save(commit=False)
        link.content_object = self.content_object
        link.user = self.user
        if commit:
            link.save()
        return link
