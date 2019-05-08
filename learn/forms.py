# -*- coding: utf-8 -*-

#import autocomplete_light_registry
import autocomplete_light
#autocomplete_light.autodiscover()

from django import forms
import datetime

from django.contrib.auth.models import User,Group
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.admin.widgets import AdminDateWidget 

from django import forms
from django.forms import models


from .models import Question, eLearnAutoRegistration
 



from django.utils.safestring import mark_safe
import uuid

    
              
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'quiz',  
            'q_type',
            
        ]
        exclude = ('userquestion', 'title', 'q_summary',  'results' )
        widgets = {
}


class eLearnAutoRegistrationForm(forms.ModelForm):
    class Meta:
        model =  eLearnAutoRegistration
        fields = [
                'firstname',
                'lastname',
                'email',
                'organisation',
                'country',
                'summary'
        ]
        exclude = ( 'status', 'publish_date')

        