
from django import forms

from iyph.models import IyphPost,Chronology,Photo,ChronologyFiles
from mezzanine.core.models import CONTENT_STATUS_DRAFT
from django.contrib.admin.widgets import AdminDateWidget 
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
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
            'image', 
            'programme_type',
            'chron_type',
            'start_date', 
            'end_date', 
            'summary',
            'venue',
            'country',
            'venue_description',
            'contact',
            'url_website', 
            ]
        exclude = ('author', 'status', 'publish_date', 'modify_date','chron_type','inhomepage','is_key_event')
        widgets = {
            'start_date': AdminDateWidget(), 
            'end_date': AdminDateWidget(), 
        }
ChronologyFilesFormSet = inlineformset_factory(Chronology,  ChronologyFiles,extra=1)

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            'photographer_first_name',
            'photographer_last_name',
            'email',
            'emailconfirmation', 
            'country',
            'age',
            'title',
            'image', 
            'date_taken',
            'place_taken',
            'short_description', 
            'agree', 
            ]
        exclude = ('modify_date','library', 'status', 'publish_date', 'finalist','exibition','prize')
        widgets = {
            'photographer_first_name': forms.TextInput(attrs={'class':'zzz'}),
            'photographer_last_name': forms.TextInput(attrs={'class':'zzz'}),
            'email': forms.TextInput(attrs={'class':'zzz'}),
            'emailconfirmation': forms.TextInput(attrs={'class':'zzz'}),
            'country': forms.Select(attrs={'class':'zzz'}),
            'age': forms.TextInput(attrs={'class':'zzz'}),
            'title': forms.TextInput(attrs={'class':'zzz'}),
            'date_taken': AdminDateWidget(), 
            'place_taken': forms.TextInput(attrs={'class':'zzz'}),
            'short_description': forms.Textarea(attrs={'class':'zzz'}),
        }        
    
