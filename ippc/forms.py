# -*- coding: utf-8 -*-

from django import forms
from .models import IppcUserProfile, PestStatus, PestReport, CountryPage
from django.contrib.auth.models import User

class PestReportForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PestReport
        fields = [
            'country',
            'title', 
            'summary',
            # 'is_public',
            'status',
            # 'slug', 
            # 'publish_date', 
            'report_status', 
            'file',
            'pest_status',
            'pest_identity',
            'hosts',
            'geographical_distribution',
            'nature_of_danger',
            'contact_for_more_information',
            'url_for_more_information'
            ]
        exclude = ('author', 'slug', 'publish_date', 'modify_date')
        widgets = {
            'country': forms.HiddenInput()
        }
            


    # def __init__(self, request, *args, **kwargs):
    #     author=request.user
    #     self.country=author.get_profile().country
    #     # self.author = request.user
    #     # self.author.id = request.user.id
    #     # self.author = request.User.username
    #     
    #     super(PestReportForm, self).__init__(request, *args, **kwargs)
    #     # 
    #     self.fields['country'].initial = request.country
        
        # self.fields['country'].queryset = IppcUserProfile.objects.filter(country=country)
        
        # self.country = forms.IntegerField(widget=forms.HiddenInput(), initial=123)
        # self.fields['country'].widget = forms.HiddenInput()
        # self.fields['country'].required = True
        # self.fields["country"].queryset = IppcUserProfile.objects.filter(country=country)
        
        # country should be set automatically to logged-in country editor's country
        # report = kwargs["instance"]
        # value = report.value
        # content_object = report.content_object
        # queryset = Profile.objects.filter(user=content_object.user)
        # self.country = IppcUserProfile.objects.filter(country="country")
        # self.country = request.user.get_profile().country
        # self.country = profile_user.get_profile.country.name
        # self.fields['country'].widget


        # self.fields['content_markdown'].widget.attrs['id'] = 'wmd-input'
        # only active users should appear in observers field
        # self.fields['observers'].queryset = User.objects.filter(is_active=True).order_by('username')

        # @receiver(post_save, sender=Rating)
        # def karma(sender, **kwargs):
        #     report = kwargs["instance"]
        #     value = report.value
        # 
        #     content_object = report.content_object
        #     queryset = Profile.objects.filter(user=content_object.user)
        #     queryset.update(karma=models.F("karma") + value)