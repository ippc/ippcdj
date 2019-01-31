
from django import forms

from iyph.models import IyphPost,Chronology
from mezzanine.core.models import CONTENT_STATUS_DRAFT
from django.contrib.admin.widgets import AdminDateWidget 

# These fields need to be in the form, hidden, with default values,
# since it posts to the blog post admin, which includes these fields
# and will use empty values instead of the model defaults, without
# these specified.
hidden_field_defaults = ("status", "gen_description", "allow_comments")


class IyphPostForm(forms.ModelForm):
    """
    Model form for ``IyphPost`` that provides the quick Iyph panel in the
    admin dashboard.
    """

    class Meta:
        model = IyphPost
        fields = ("title", "content") + hidden_field_defaults

    def __init__(self):
        initial = {}
        for field in hidden_field_defaults:
            initial[field] = IyphPost._meta.get_field(field).default
        initial["status"] = CONTENT_STATUS_DRAFT
        super(IyphPostForm, self).__init__(initial=initial)
        for field in hidden_field_defaults:
            self.fields[field].widget = forms.HiddenInput()


class ChronologyForm(forms.ModelForm):
    class Meta:
        model = Chronology
        fields = [
            'title', 
            'programme_type',
            'chron_type',
            'summary',
            'start_date', 
            'end_date', 
            'venue',
            'contact',
            'url_website', 
            ]
        exclude = ('author', 'status', 'publish_date', 'modify_date','chron_type')
        widgets = {
            'start_date': AdminDateWidget(), 
            'end_date': AdminDateWidget(), 
        }
        
       