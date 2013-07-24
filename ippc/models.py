from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

from datetime import datetime

import os.path

from mezzanine.pages.models import Page

from mezzanine.conf import settings
from mezzanine.core.models import Slugged, MetaData, Displayable, Orderable, RichText
from mezzanine.core.fields import RichTextField

class IppcUserProfile(models.Model):
    """ User profiles for IPPC"""
    
    GENDER_CHOICES = (
        (1, _("Mr")),
        (2, _("Ms")),
    )
    
    user = models.OneToOneField("auth.User")
    title = models.CharField(_("Title"), blank=True, null=True, max_length=100)
    first_name = models.CharField(_("First Name"), max_length=30)
    last_name = models.CharField(_("Last Name"), max_length=30)
    # main email address already provided by auth.User
    email_address_alt = models.EmailField(_("Alternate Email"), default="", max_length=75, blank=True, null=True)

    gender = models.PositiveSmallIntegerField(_("Gender"), choices=GENDER_CHOICES, blank=True, null=True)
    profile_photo = models.FileField(_("Profile Photo"), upload_to="profile_photos", blank=True)
    bio = models.TextField(_("Brief Biography"), default="", blank=True, null=True)

    address1 = models.CharField(_("Address 1"), blank=True, max_length=100)
    address2 = models.CharField(_("Address 2"), blank=True, max_length=100)
    city = models.CharField(_("City"), blank=True, max_length=100)
    state = models.CharField(_("State"), blank=True, max_length=100, help_text="or Province")
    zipcode = models.CharField(_("Zip Code"), blank=True, max_length=20)
    address_country = CountryField(_("Address Country"), blank=True, null=True)
    # country will be the 'tag' to mark permissions for Country Main Contact Points and Country Editors
    country = CountryField(_("IPPC Country"))

    phone = models.CharField(_("Phone"), blank=True, max_length=30)
    fax = models.CharField(_("Fax"), blank=True, max_length=30)
    mobile = models.CharField(_("Mobile"), blank=True, max_length=30)
    
    date_account_created = models.DateTimeField(_("Member Since"), default=datetime.now, editable=False)

    # def country(self):
    #     return self.country


# class CountryPage(Page):
#     country = CountryField(_("Country"))

# do we need a table for this? or do http://djangosnippets.org/snippets/2753/ ?
class PestStatus(models.Model):
    status = models.CharField(_("Pest Status"), max_length=500)

    def __unicode__(self):
        return self.status
        
    class Meta:
        verbose_name_plural = _("Pest Statuses")
    pass

IS_HIDDEN = 1
IS_PUBLIC = 2
PUBLISHING_CHOICES = (
    (IS_HIDDEN, _("Hidden - does not appear publically on ippc.int. Choose this instead of deleting.")), 
    (IS_PUBLIC, _("Public - visible on ippc.int")),
)

REPORT_STATUS_NA = 1
REPORT_STATUS_PRELIMINARY = 2
REPORT_STATUS_FINAL = 3
REPORT_STATUS_CHOICES = (
    (REPORT_STATUS_NA, _("N/A")),
    (REPORT_STATUS_PRELIMINARY, _("Preliminary")),
    (REPORT_STATUS_FINAL, _("Final")),
)

class PestReport(models.Model):
    country = CountryField(_("Country"))
    author = models.ForeignKey(User, related_name="pest_report_author")
    title = models.CharField(_("Title"), max_length=500)
    is_public = models.IntegerField(_("Visibility"), 
        choices=PUBLISHING_CHOICES, default=IS_PUBLIC,
        help_text=_("Choose 'Hidden' instead of deleting reports.")
        )
    slug = models.CharField(_("URL"), max_length=2000, blank=True, null=True,
            unique_for_date='publish_date',
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))
    publish_date = models.DateTimeField(_("Published date"),
        help_text=_("Leave blank to have date set for today."),
        blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False)
    summary = models.TextField(_("Summary or Short Description"),
        blank=True, null=True)
    report_status = models.IntegerField(_("Report Status"),
        choices=REPORT_STATUS_CHOICES, default=REPORT_STATUS_FINAL)
    file = models.FileField(_("Pest Report Document"), upload_to="pest_reports/%Y/%m/", blank=True)
    pest_status = models.ManyToManyField(PestStatus,
        verbose_name=_("Pest Status"),
        related_name='pest_status+', blank=True, null=True,
        help_text=_("Under <a href='#'>ISPM 8</a> -"))
    pest_identity = models.TextField(_("Identity of Pest"),
        blank=True, null=True)
    hosts = models.TextField(_("Hosts or Articles concerned"),
        blank=True, null=True)
    geographical_distribution = models.TextField(_("Geographical Distribution"),
        blank=True, null=True)
    nature_of_danger = models.TextField(_("Nature of Immediate or potential danger"),
        blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"),
        blank=True, null=True)
    url_for_more_information = models.URLField(blank=True, null=True)
    # =todo:
    # commodity_groups = 
    # keywords = 

    class Meta:
        verbose_name_plural = _("Pest Reports")

    def __unicode__(self):
        return self.title

    def filename(self):
        return os.path.basename(self.file.name)
        
    def country_name(self):
        return self.country.name
        
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('pest-report-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'month': self.publish_date.strftime("%m"),
                            # 'day': self.pub_date.strftime("%d"),
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.datetime.now()
        super(PestReport, self).save(*args, **kwargs)





# Translations of user-generated content - https://gist.github.com/renyi/3596248
class Translatable(models.Model):
    lang = models.CharField(max_length=5, choices=settings.LANGUAGES)

    class Meta:
        abstract = True
        ordering = ("lang",)

if "mezzanine.pages" in settings.INSTALLED_APPS:
    from mezzanine.pages.models import RichTextPage, Link

    class TransRichTextPage(Translatable, RichText, Slugged):
        translation = models.ForeignKey(RichTextPage, related_name="translation")

        class Meta:
            verbose_name = _("Translated Page")
            verbose_name_plural = _("Translated Pages")
            ordering = ("lang",)
            unique_together = ("lang", "translation")

    class TransLinkPage(Translatable, Slugged):
        translation = models.ForeignKey(Link, related_name="translation")

        class Meta:
            verbose_name = _("Translated Link")
            verbose_name_plural = _("Translated Links")
            ordering = ("lang",)
            unique_together = ("lang", "translation")

if "mezzanine.forms" in settings.INSTALLED_APPS:
    from mezzanine.forms import fields
    from mezzanine.forms.models import Form, FieldManager, Field

    class TransForm(Translatable, RichText, Slugged):
        translation = models.ForeignKey(Form, related_name="translation")

        button_text = models.CharField(_("Button text"), max_length=50, default=_("Submit"))
        response = RichTextField(_("Response"))

        class Meta:
            verbose_name = _("Translated Form")
            verbose_name_plural = _("Translated Forms")
            ordering = ("lang",)
            unique_together = ("lang", "translation")

    class TransField(Translatable):
        translation = models.ForeignKey(Field, related_name="translation")
        original    = models.CharField(_("Label (Original)"), max_length=settings.FORMS_LABEL_MAX_LENGTH)
        label       = models.CharField(_("Label"), max_length=settings.FORMS_LABEL_MAX_LENGTH)

        choices     = models.CharField(_("Choices"), max_length=1000, blank=True,
                                       help_text=_("Comma separated options where applicable. "
                                                   "If an option itself contains commas, surround the option with `backticks`."))
        default     = models.CharField(_("Default value"), blank=True,
                                       max_length=settings.FORMS_FIELD_MAX_LENGTH)
        help_text   = models.CharField(_("Help text"), blank=True, max_length=100)

        class Meta:
            verbose_name = _("Translated Field")
            verbose_name_plural = _("Translated Fields")
            ordering = ("lang",)

if "mezzanine.galleries" in settings.INSTALLED_APPS:
    from mezzanine.galleries.models import Gallery, GalleryImage

    class TransGallery(Translatable, Slugged, RichText):
        translation = models.ForeignKey(Gallery, related_name="translation")

        class Meta:
            verbose_name = _("Translated Gallery")
            verbose_name_plural = _("Translated Galleries")
            ordering = ("lang",)

    class TransGalleryImage(Translatable, Slugged):
        translation = models.ForeignKey(GalleryImage, related_name="translation")
        description = models.CharField(max_length=1000, blank=True)

        class Meta:
            verbose_name = _("Translated Image")
            verbose_name_plural = _("Translated Images")
            ordering = ("lang",)









from django import forms
from .models import IppcUserProfile, PestStatus, PestReport
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

        super(PestReportForm, self).__init__(request.POST or None, *args, **kwargs)
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
        # self.fields['country'].queryset = IppcUserProfile.objects.filter(country=country)

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