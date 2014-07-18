
from django import forms

from forum.models import ForumPost
from mezzanine.core.models import CONTENT_STATUS_DRAFT


# These fields need to be in the form, hidden, with default values,
# since it posts to the forum post admin, which includes these fields
# and will use empty values instead of the model defaults, without
# these specified.
hidden_field_defaults = ("status", "gen_description", "allow_comments")


class ForumPostForm(forms.ModelForm):
    """
    Model form for ``ForumPost`` that provides the quick forum panel in the
    admin dashboard.
    """

    class Meta:
        model = ForumPost
        fields = ("title", "content") + hidden_field_defaults

    def __init__(self):
        initial = {}
        for field in hidden_field_defaults:
            initial[field] = ForumPost._meta.get_field(field).default
        initial["status"] = CONTENT_STATUS_DRAFT
        super(ForumPostForm, self).__init__(initial=initial)
        for field in hidden_field_defaults:
            self.fields[field].widget = forms.HiddenInput()
