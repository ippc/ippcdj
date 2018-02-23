from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event, Occurrence, EventFile,EventUrl,EventParticipants
from ippc.models import IssueKeywordsRelate
from django.contrib.admin.widgets import AdminDateWidget 
import autocomplete_light
import ippc.autocomplete_light_registry
from ippc.forms import IssueKeywordsRelateForm
from ippc.models import Topic

from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory

class SpanForm(forms.ModelForm):
#    start = forms.DateTimeField(label=_("start"),
#                                widget=forms.SplitDateTimeWidget)
#    end = forms.DateTimeField(label=_("end"),
#                              widget=forms.SplitDateTimeWidget,
#                              help_text=_(u"The end time must be later than start time."))

    def clean(self):
        if 'end' in self.cleaned_data and 'start' in self.cleaned_data:
            if self.cleaned_data['end'] < self.cleaned_data['start']:
                raise forms.ValidationError(_(u"The end time must be later than start time."))
        return self.cleaned_data


class EventForm(SpanForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

    #end_recurring_period = forms.DateTimeField(label=_(u"End recurring period"),
                                               #help_text=_(u"This date is ignored for one time only events."),
                                               #required=False)

    class Meta:
        model = Event
        exclude = ('creator', 'created_on', 'calendar','rule','end_recurring_period','country')
        widgets = {
            'start': AdminDateWidget(),
            'end': AdminDateWidget(),
            'end_register_date': AdminDateWidget(),
        #    'topic_numbers': forms.SelectMultiple(attrs={'class':'yyy1'}),
            'topic_numbers': autocomplete_light.MultipleChoiceWidget ('TopicAutocomplete'),   
     
        }
EventFileFormSet = inlineformset_factory(Event,  EventFile,extra=1)
EventUrlFormSet  = inlineformset_factory(Event,  EventUrl, extra=1)




class EventParticipantsForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = EventParticipants
        fields = [
            'user',
            'role',
            'attended' ,
            'registered' ,
            'registered_date',
           # 'funding',
            'representing_country',
            'representing_organization',
            'representing_region',
        ]
        exclude = ( 'event', )
        
        widgets = {
              'user': autocomplete_light.ChoiceWidget('UserAutocomplete'),
        }


EventParticipantsFormSet = inlineformset_factory(Event, EventParticipants,  form=EventParticipantsForm, extra=2)


#ventParticipantsFormSet  = inlineformset_factory(Event,  EventParticipants, extra=1)



class OccurrenceForm(SpanForm):
    class Meta:
        model = Occurrence
        exclude = ('original_start', 'original_end', 'event', 'cancelled')