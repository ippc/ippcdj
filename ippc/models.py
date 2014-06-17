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

class PublicationLibrary(Page, RichText):
    """
        Page bucket for publications. Here's the expect folder layout:
        - WorkAreaPage or Page
            - PublicationLibrary
                - Table listing multiple Publications which contain...
                    ...multiple Files
    """
    users = models.ManyToManyField(User, 
        verbose_name=_("Users this library is accessible to"), 
        related_name='publicationlibraryusers', blank=True, null=True)
    groups = models.ManyToManyField(Group, 
        verbose_name=_("Groups this library is accessible to"), 
        related_name='publicationlibrarygroups', blank=True, null=True)

    class Meta:
        verbose_name = _("Publication Library")
        verbose_name_plural = _("Publication Libraries")
        # south overrides syncdb, so the following perms are not created
        # unless we are starting the project from scratch.
        # solution: python manage.py syncdb --all
        # or
        # manage.py datamigration myapp add_perm_foo --freeze=contenttypes --freeze=auth
        # http://stackoverflow.com/questions/1742021/adding-new-custom-permissions-in-django
        permissions = ( 
            ("can_view", "View Publication Library"),
        )

# used by Publications
IS_HIDDEN = 1
IS_PUBLIC = 2
PUBLICATION_STATUS_CHOICES = (
    (IS_HIDDEN, _("Hidden - does not appear publically on ippc.int. Choose this instead of deleting.")), 
    (IS_PUBLIC, _("Public - visible on ippc.int")),
)


class Publication(Orderable):
    """Single publication to add in a publication library."""

    class Meta:
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")
        
    library = models.ForeignKey("PublicationLibrary", 
        related_name="publications") # related_name=publications...
        # ..is used in publicationlibrary template
    title = models.CharField(_("Title"), blank=True, null=True, max_length=100)
    # author = models.ForeignKey(User, related_name="publication_author")
    file_en = models.FileField(_("File - English"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/en/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_es = models.FileField(_("File - Spanish"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/es/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_fr = models.FileField(_("File - French"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/fr/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_ru = models.FileField(_("File - Russian"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/ru/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_ar = models.FileField(_("File - Arabic"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/ar/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_zh = models.FileField(_("File - Chinese"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/zh/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    slug = models.SlugField(max_length=200, blank=True, null=True,
            unique_for_date='modify_date')
    status = models.IntegerField(_("Status"), choices=PUBLICATION_STATUS_CHOICES, default=IS_PUBLIC)
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False, auto_now=True)
    agenda_number = models.CharField(_("Agenda Item Number"), max_length=100,
                                   blank=True)
    document_number = models.CharField(_("Document Number"), max_length=100,
                                  blank=True)
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If no title is given when created, create one from the
        file name.
        """
        if not self.id and not self.title:
            name = unquote(self.file.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.title = name
        super(Publication, self).save(*args, **kwargs)

    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Publication."""
        return ('publication-detail', (), {
                            # 'country': self.country.name, # =todo: get self.country.name working
                            # 'year': self.publish_date.strftime("%Y"),
                            # 'month': self.publish_date.strftime("%m"),
                            # 'day': self.pub_date.strftime("%d"),
                            'pk': self.pk})


class WorkAreaPage(Page, RichText):
    """ Work Area Pages with definable users and groups """
    users = models.ManyToManyField(User, 
        verbose_name=_("Users this page is accessible to"), 
        related_name='workareapageusers', blank=True, null=True)
    groups = models.ManyToManyField(Group, 
        verbose_name=_("Groups this page is accessible to"), 
        related_name='workareapagegroups', blank=True, null=True)

    class Meta:
        verbose_name = "Work Area Page"
        verbose_name_plural = "Work Area Pages"
        permissions = (
            ("can_view", "View Work Area Page"),
        )

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
            verbose_name=_("Country Chief Contact Point"), blank=True, null=True)
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
    title = models.CharField(_("Professional Title"), blank=True, null=True, max_length=100)
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


# this is in mezzanine.core.models.displayable
# CONTENT_STATUS_DRAFT = 1
# CONTENT_STATUS_PUBLISHED = 2
# CONTENT_STATUS_CHOICES = (
#     (CONTENT_STATUS_DRAFT, _("Draft")),
#     (CONTENT_STATUS_PUBLISHED, _("Published")),
# )

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


# used by Basic Reporting type
BASIC_REP_1 = 1
BASIC_REP_2 = 2
BASIC_REP_3 = 3
BASIC_REP_4 = 4
BASIC_REP_TYPE_CHOICES = (
    (BASIC_REP_1, _("Description of the NPPO (Art. IV.4)")), 
    (BASIC_REP_2, _("Entry points (Art. VII.2d)")),
    (BASIC_REP_3, _("List of regulated pests (Art. VII.2i)")),
    (BASIC_REP_4, _("Phytosanitary Restrictions/Legislation")),
)
   
class BasicReporting(Displayable, models.Model):
    """ Basic Reporting"""
    country = models.ForeignKey(CountryPage, related_name="basic_reporting_country_page")
    author = models.ForeignKey(User, related_name="basic_reporting_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    basic_rep_type = models.IntegerField(_("Basic Reporting"), choices=BASIC_REP_TYPE_CHOICES, default=BASIC_REP_3)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    file = models.FileField(_("Report Document"), upload_to="basic_reporting/%Y/%m/", blank=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
   
  

    # =todo:
    # commodity_groups = 
    # keywords / tags = 
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Basic Reportings")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('basic-reporting-detail', (), {
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
        super(BasicReporting, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def basic_rep_type_verbose(self):
        return dict(BASIC_REP_TYPE_CHOICES)[self.basic_rep_type]

# used by Basic Reporting type
EVT_REP_1 = 1
EVT_REP_2 = 2
EVT_REP_3 = 3
EVT_REP_4 = 4
EVT_REP_5 = 5
EVT_REP_TYPE_CHOICES = (
    (EVT_REP_1, _("Emergency Actions (Art. VII 6)")), 
    (EVT_REP_2, _("Non-compliance")),
    (EVT_REP_3, _("Organizational Arrangements of Plant Protection")),
    (EVT_REP_4, _("Pest status")),
    (EVT_REP_5, _("Rationale for Phytosanitary Requirements")),
)
   

class EventReporting(Displayable, models.Model):
    """ Event Reporting"""
    country = models.ForeignKey(CountryPage, related_name="event_reporting_country_page")
    author = models.ForeignKey(User, related_name="event__reporting_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    event_rep_type = models.IntegerField(_("Event Reporting"), choices=EVT_REP_TYPE_CHOICES, default=EVT_REP_1)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    file = models.FileField(_("Report Document"), upload_to="event_reporting/%Y/%m/", blank=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
   
  

    # =todo:
    # commodity_groups = 
    # keywords / tags = 
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Event Reportings")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('event-reporting-detail', (), {
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
        super(EventReporting, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def event_rep_type_verbose(self):
        return dict(EVT_REP_TYPE_CHOICES)[self.event_rep_type]

PFA_TYPE_1 = 1
PFA_TYPE_2 = 2
PFA_TYPE_1_CHOICES = (
    (PFA_TYPE_1, _("PFA")), 
    (PFA_TYPE_2, _("ALPP")),
)
class PestFreeArea(Displayable, models.Model):
    """ Pest Free Area"""
    country = models.ForeignKey(CountryPage, related_name="pestfreearea_country_page")
    author = models.ForeignKey(User, related_name="pestfreearea_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    short_description = models.TextField(_("Location and description of the area"),  blank=True, null=True)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    pfa_type = models.IntegerField(_("Type of recognition"), choices=PFA_TYPE_1_CHOICES, default=None)
    file = models.FileField(_("Additional information and Documentation"), upload_to="pestfreearea/%Y/%m/", blank=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    # =todo:
    # commodity_groups = 
    # keywords / tags = 
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Pest Free Areas")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('pfa-detail', (), {
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
        super(PestFreeArea, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def pfa_type_verbose(self):
        return dict(PFA_TYPE_1_CHOICES)[self.pfa_type]


YES_1 = 1
NO_2 = 2
DONTKNOW_3 = 3
YES_NO_CHOICES = (
    (YES_1, _("Yes")), 
    (NO_2, _("No")),
)


YES_NO_DONTKNOW_CHOICES = (
    (YES_1, _("Yes")), 
    (NO_2, _("No")), 
    (DONTKNOW_3, _("Don't know")), 
)
VERS_1 = "2002"
VERS_2 = "2009"
VERS_CHOICES = (
    (VERS_1, _("2002")), 
    (VERS_1, _("2009")),
)
class ImplementationISPMVersion(models.Model):
    """ ImplementationISPMVersions """
    version = models.CharField(_("Implementation of ISPM Version"), max_length=4)
    
    def __unicode__(self):
        return self.version
        
    class Meta:
        verbose_name_plural = _("Implementation of ISPM Versions ")
    pass

class ImplementationISPM(Displayable, models.Model):
    """ Implementationof ISPM 15"""
    country = models.ForeignKey(CountryPage, related_name="implementationispm_country_page")
    author = models.ForeignKey(User, related_name="implementationispm_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    implementimport_type = models.IntegerField(_("Has your country implemented ISPM 15 for imports?"), choices=YES_NO_CHOICES, default=None)
    implementimport_version = models.ManyToManyField(ImplementationISPMVersion,
        verbose_name=_("If yes, which version (click all that apply): "),
        related_name='implementimport_version+', blank=True, null=True, default=None)
    implementexport_type = models.IntegerField(_("  Has your country implemented ISPM 15 for exports?"), choices=YES_NO_CHOICES, default=None)
    implementexport_version = models.ManyToManyField(ImplementationISPMVersion,
        verbose_name=_("If yes, which version (click all that apply): "),
        related_name='implementexport_version+', blank=True, null=True, default=None)
    file = models.FileField(_("Additional information and Documentation"), upload_to="implemenationispm/%Y/%m/", blank=True)
    mark_registered_type = models.IntegerField(_(" Is the ISPM No.15 mark registered as a trade mark in your country??"), choices=YES_NO_DONTKNOW_CHOICES, default=None)
    image = models.ImageField(_("Image of mark"), upload_to="implemenationispm/images/%Y/%m/", blank=True)
    
    # =todo Image
    short_description = models.TextField(_("Enter a description of mark"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    # =todo:
    # commodity_groups = 
    # keywords / tags = 
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Implementationof ISPMs")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('implementationispm-detail', (), {
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
        super(ImplementationISPM, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def imagename(self):
        return os.path.basename(self.image.name)
    def implementimport_type_verbose(self):
        return dict(YES_NO_CHOICES)[self.implementimport_type]
    def implementexport_type_verbose(self):
        return dict(YES_NO_CHOICES)[self.implementexport_type]
    def mark_registered_type_verbose(self):
        return dict(YES_NO_DONTKNOW_CHOICES)[self.mark_registered_type]



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
