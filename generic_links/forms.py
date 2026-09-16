from django import forms

from generic_links.models import GenericLink


class AddLinkForm(forms.ModelForm):
    # The model default is True, so unbound forms render the checkbox checked.
    # Note: HTML checkboxes are absent from POST data when unchecked, so a
    # submitted form without the checkbox saves is_external=False.
    is_external = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = GenericLink
        fields = ("title", "url", "description", "is_external")

    def __init__(self, content_object, user, *args, **kwargs):
        self.content_object = content_object
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        link = super().save(commit=False)
        link.content_object = self.content_object
        link.user = self.user
        if commit:
            link.save()
        return link
