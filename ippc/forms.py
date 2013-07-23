# -*- coding: utf-8 -*-
from django import forms
from .models import IppcUserProfile, PestStatus, PestReport
from django.contrib.auth.models import User

class PestReportForm(forms.ModelForm):
    class Meta:
        model = PestReport
        fields = [
            'country',
            'title', 
            'summary',
            'is_public',
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

    def __init__(self, request, *args, **kwargs):
        
        self.author = request.user
        self.author.id = request.user.id
        # country should be set automatically to logged-in country editor's country
        # report = kwargs["instance"]
        # value = report.value
        # content_object = report.content_object
        # queryset = Profile.objects.filter(user=content_object.user)
        # self.country = IppcUserProfile.objects.filter(country="country")
        # self.country = request.user.get_profile().country
        # self.country = profile_user.get_profile.country.name
        # self.country = request.country
        super(PestReportForm, self).__init__(request.POST or None, *args, **kwargs)
        # self.fields['content_markdown'].widget.attrs['class'] = 'wmd-input'
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