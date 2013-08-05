from string import punctuation
from urllib import unquote

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from django.contrib.auth.models import User, Group

from django.template.defaultfilters import slugify
from datetime import datetime
import os.path

from mezzanine.pages.models import Page, RichTextPage
from mezzanine.conf import settings
from mezzanine.core.models import Slugged, MetaData, Displayable, Orderable, RichText
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.core.managers import SearchableManager

from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.models import upload_to


# class PublicationLibrary(Page, RichText):
#     """
#         Page bucket for publications. Here's the expect folder layout:
#         - WorkAreaPage or Page
#             - PublicationLibrary
#                 - Table listing multiple Publications which contain...
#                     ...multiple Files
#     """
# 
#     class Meta:
#         verbose_name = _("Publication Library")
#         verbose_name_plural = _("Publication Libraries")
# 
# 
# class Publication(Displayable, models.Model):
#     """Single publication to add in a publication library."""
# 
#     library = models.ForeignKey("PublicationLibrary", related_name="publication_libraries")
#     author = models.ForeignKey(User, related_name="publication_author")
#     # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
#     # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
#     # status - provided by mezzanine.core.models.displayable
#     # publish_date - provided by mezzanine.core.models.displayable
#     modify_date = models.DateTimeField(_("Modified date"),
#         blank=True, null=True, editable=False, auto_now=True)
#     agenda_number = models.CharField(_("Description"), max_length=100,
#                                    blank=True)
#     document_number = models.CharField(_("Description"), max_length=100,
#                                   blank=True)
# 
#     class Meta:
#         verbose_name = _("Publication")
#         verbose_name_plural = _("Publications")
# 
#     def __unicode__(self):
#         return self.title
# 
# 
# class File(models.Model):
#     """Single file to add in a publication."""
# 
#     publication = models.ForeignKey("Publication", related_name="publications")
#     # file = FileField(_("File"), max_length=200,
#     #         upload_to=upload_to("galleries.GalleryImage.file", "galleries"))
#     # http://reinout.vanrees.org/weblog/2012/04/13/django-filefield-limitation.html
#     file = models.FileField(_("File"), 
#             upload_to=upload_to("galleries.GalleryImage.file", "galleries"),
#             unique_for_date='last_change', max_length=204)
#     # file = models.ImageField(upload_to="pictures")
#     slug = models.SlugField(max_length=200, blank=True, 
#             unique_for_date='last_change')
#     lang = models.CharField(max_length=5, choices=settings.LANGUAGES)
#     last_change = models.DateTimeField(auto_now=True)
# 
#     class Meta:
#         verbose_name = _("File")
#         verbose_name_plural = _("Files")
# 
#     def __unicode__(self):
#         return self.file.name
# 
#     def filename(self):
#             return os.path.basename(self.file.name)
# 
#     def save(self, *args, **kwargs):
#         self.id = self.id
#         self.slug = self.file.name
#         # self.uploaded_by = self.request.user
#         if not self.id:
#             # Newly created object, so set slug
#             self.slug = slugify(self.file.name)
#         self.last_change = datetime.datetime.now()
#         super(File, self).save(*args, **kwargs)













class WorkAreaPage(Page, RichText):
    """ Work Area Pages with definable users and groups """
    users = models.ManyToManyField(User, verbose_name=_("Work Area Page Users"), 
        related_name='workareapageusers+', blank=True, null=True)
    groups = models.ManyToManyField(Group, verbose_name=_("Work Area Page Groups"), 
        related_name='workareapagegroups+', blank=True, null=True)

    class Meta:
        verbose_name = "Work Area Page"
        verbose_name_plural = "Work Area Pages"

class CountryPage(Page):
    """ Country Pages with definable names, slugs, editors and contact point"""
    class Meta:
        verbose_name = _('Country Page')
        verbose_name_plural = _('Country Pages')
        ordering = ['name']

    iso = models.CharField(max_length=2, unique=True, blank=True, null=True)
    iso3 = models.CharField(max_length=3, unique=True, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    country_slug = models.CharField(_("Country URL Slug"), max_length=100, 
            unique=True, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))
    contact_point = models.OneToOneField("auth.User", 
            verbose_name=_("Chief Contact Point"), blank=True, null=True)
    editors = models.ManyToManyField(User, verbose_name=_("Country Editors"), 
        related_name='countryeditors+', blank=True, null=True)
    # =todo: 
    # contracting_party = boolean
    # territory_of = foreignkey to other country
    # flag

    def __unicode__(self):
        return u'%s' % (self.name,)

# do we need a table for this? or do http://djangosnippets.org/snippets/2753/ ?
class PestStatus(models.Model):
    """ Pest Statuses """
    status = models.CharField(_("Pest Status"), max_length=500)

    def __unicode__(self):
        return self.status
        
    class Meta:
        verbose_name_plural = _("Pest Statuses")
    pass

class IppcUserProfile(models.Model):
    """ User Profiles for IPPC"""
    
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
    # country is the 'tag' marking permissions for Contact Point and Editors
    country = models.ForeignKey(CountryPage, related_name="user_country_page", blank=True, null=True)

    phone = models.CharField(_("Phone"), blank=True, max_length=30)
    fax = models.CharField(_("Fax"), blank=True, max_length=30)
    mobile = models.CharField(_("Mobile"), blank=True, max_length=30)
    
    date_account_created = models.DateTimeField(_("Member Since"), default=datetime.now, editable=False)


# Keeping this outside PestReport class so we can call IS_PUBLIC in view
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

class PestReport(Displayable, models.Model):
    """ Pest Reports"""
    country = models.ForeignKey(CountryPage, related_name="pest_report_country_page")
    author = models.ForeignKey(User, related_name="pest_report_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
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
        help_text=_("Under ISPM 8 -"))
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
    # keywords / tags = 
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("Pest Reports")
        # abstract = True

    def __unicode__(self):
        return self.title

    def country_code(self):
        return self.country
        
        
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
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(PestReport, self).save(*args, **kwargs)













class Translatable(models.Model):
    """ Translations of user-generated content - https://gist.github.com/renyi/3596248"""
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
