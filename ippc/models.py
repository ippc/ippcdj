
from string import punctuation
from urllib import unquote

from django.db import models
#from django.contrib.gis.db import models as gismodels

from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField


from django.contrib.auth.models import User, Group


from django.template.defaultfilters import slugify
from datetime import datetime
import os.path
from django.utils import timezone
from mezzanine.pages.models import Page, RichTextPage
from mezzanine.conf import settings
from mezzanine.core.models import Slugged, MetaData, Displayable, Ownable, Orderable, RichText
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.core.managers import SearchableManager

from mezzanine.generic.fields import CommentsField

from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.models import upload_to


from django.contrib.contenttypes import generic
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from django.core.exceptions import ValidationError
from django.core import mail
from django.core.mail import send_mail

from mezzanine.utils.models import get_user_model_name
from mezzanine.generic.models import ThreadedComment
from django.shortcuts import  get_object_or_404
import MySQLdb
from settings import  DATABASES
from t_eppo.models import Names


User._meta.ordering=["username"]

def user_unicode_patch(self):
    return '%s %s' % (self.first_name, self.last_name)


class PublicationLibrary(Page, RichText):
    """
        Page bucket for publications. Here's the expect folder layout:
        - WorkAreaPage or Page
            - PublicationLibrary
                - Table listing multiple Publications which contain...
                    ...multiple Files
    """
    pagefeatured_image = models.ImageField(_("Page Featured Image"),help_text=_("Image size 730px x 240px"), upload_to="files/largefiles/", blank=True)
    embedded_image = models.ImageField(_("Page Embedded Image"), upload_to="files/largefiles/", blank=True)
    embeddedimage_small =  models.BooleanField( verbose_name=_("Show small Embedded Image"),default=False)
    embedded_image_caption = models.CharField(_("Embedded Image Caption"), blank=True, null=True, max_length=250)
    users = models.ManyToManyField(User, 
        verbose_name=_("Users this library is accessible to"), 
        related_name='publicationlibraryusers', blank=True, null=True)
    groups = models.ManyToManyField(Group, 
        verbose_name=_("Groups this library is accessible to"), 
        related_name='publicationlibrarygroups', blank=True, null=True)
    old_id = models.CharField(max_length=50, blank=True, null=True)
    show_agenda_colums =  models.BooleanField( verbose_name=_("Show column for 'Agenda number'."),default=True)
    show_doc_colums =  models.BooleanField( verbose_name=_("Show column for 'Document number'."),default=True)
    show_topicnumber_colums =  models.BooleanField( verbose_name=_("Show column for 'Topic number'."),default=False)
    fullpage =  models.BooleanField( verbose_name=_("Show full page"),default=False)
    side_box = models.TextField(_("Side box"),  blank=True, null=True)
    
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
   
        
        
class IssueKeyword(models.Model):
    """ IssueKeyword  """
    name = models.CharField(_("Issue Keyword"), max_length=500)
    def __unicode__(self):
        return self.name
class CommodityKeyword(models.Model):
    """ CommodityKeyword """
    name = models.CharField(_("Commodity Keyword"), max_length=500)
    def __unicode__(self):
        return self.name



        
class IssueKeywordsRelate(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    issuename = models.ManyToManyField(IssueKeyword,
        verbose_name=_("Issue Keywords"),
        blank=True, null=True, 
        help_text=_("Type at least two letters, then select and \
        press enter to input existing keywords, or write new ones\
         separated by a comma."))

class CommodityKeywordsRelate(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    commname = models.ManyToManyField(CommodityKeyword,
        verbose_name=_("Commodity Keywords"),
        blank=True, null=True,
        help_text=_("Type at least two letters, then select and \
        press enter to input existing keywords, or write new ones\
         separated by a comma."))

        



CP_NCP_T_TYPE_0 = 'N/A'
CP_NCP_T_TYPE_1 = 'CP'
CP_NCP_T_TYPE_2 = 'NCP'
CP_NCP_T_TYPE_3 = 'T'
CP_NCP_TYPE_CHOICES = (
    (CP_NCP_T_TYPE_1, _("Contracting party")),
    (CP_NCP_T_TYPE_2, _("Non-Contracting party")),
    (CP_NCP_T_TYPE_3, _("Territory")),
)
REGION_1 = 1
REGION_2 = 2
REGION_3 = 3
REGION_4 = 4
REGION_5 = 5
REGION_6 = 6
REGION_7 = 7
REGIONS = (
    (REGION_1, _("Africa")),
    (REGION_2, _("Asia")),
    (REGION_3, _("Europe")),
    (REGION_4, _("Latin America and Caribbean")),
    (REGION_5, _("Near East")),
    (REGION_6, _("North America")),
    (REGION_7, _("South West Pacific")),
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
    cp_ncp_t_type = models.CharField(_("Contracting or Non-Contracting party"),max_length=3, choices=CP_NCP_TYPE_CHOICES, default=CP_NCP_T_TYPE_0)
    region = models.IntegerField(_("Region"), choices=REGIONS, default=None)
    cn_flag = models.ImageField(_("Country flag"), upload_to="flags/", blank=True)
    cn_lat = models.CharField(_("Country latitude"), max_length=100, unique=True, blank=True, null=True)
    cn_long = models.CharField(_("Country longitute"),max_length=100, unique=True, blank=True, null=True)
    cn_map = models.CharField(_("Country Map"), max_length=550)
    cn_map = models.CharField(_("Country Map"), max_length=550)
    accepted_epporeport = models.BooleanField(verbose_name=_("Report through EPPO"),
                                         default=False)
    accepted_epporeport_date = models.DateTimeField(_("Report through EPPO accepted date "), blank=True, null=True, editable=True)
    send_reminder = models.BooleanField(verbose_name=_("Send reminder"),
                                         default=True)
                                         
        # =todo: 
    # contracting_party = boolean
    # territory_of = foreignkey to other country
    # flag

    def __unicode__(self):
        return u'%s' % (self.name,)
    
class OCPHistory(models.Model):
    countrypage = models.ForeignKey(CountryPage)
   # contact_point = models.OneToOneField("auth.User",             verbose_name=_("Country Chief Contact Point"), blank=True, null=True)
    contact_point = models.ForeignKey("auth.User",verbose_name=_("Country Chief Contact Point"), blank=True, null=True)
    start_date = models.DateTimeField(_("Nomination start date"), blank=True, null=True, editable=True)
    end_date = models.DateTimeField(_("Nomination end date"), blank=True, null=True, editable=True)
    
class CnEditorsHistory(models.Model):
    countrypage = models.ForeignKey(CountryPage)
    editor = models.ForeignKey("auth.User",verbose_name=_("Country Editor"), blank=True, null=True)
    #editor = models.OneToOneField("auth.User",             verbose_name=_("Country Editor"), blank=True, null=True)
    start_date = models.DateTimeField(_("Nomination start date"), blank=True, null=True, editable=True)
    end_date = models.DateTimeField(_("Nomination end date"), blank=True, null=True, editable=True)
    
        
COOPTYPE_0 = 0    
COOPTYPE_1 = 1
COOPTYPE_2 = 2
COOPTYPE_3 = 3
COOPTYPE_4 = 4
COOPTYPE_5 = 5


COOPTYPE_CHOICES = (
    (COOPTYPE_0, _("N/A")),
    (COOPTYPE_1, _("UN Organizations")),
    (COOPTYPE_2, _("International Organizations")),
    (COOPTYPE_3, _("Industry/NGOs")),
    (COOPTYPE_4, _("Academia/Research")),
    (COOPTYPE_5, _("Resource Organizations")),
  
)

    
class PartnersPage(Page, RichText):
    """ PartnersPage with definable names, slugs, editors and rppo contact point"""
    class Meta:
        verbose_name = _('Partners Page')
        verbose_name_plural = _('Partners Pages')
        ordering = ['name']

    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    short_description = models.CharField(_("Text"), max_length=550)
    partner_slug = models.CharField(_("URL Slug"), max_length=100, 
            unique=True, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))
    contact_point = models.OneToOneField("auth.User", 
            verbose_name=_("RPPO Chief Contact Point"), blank=True, null=True)
    editors = models.ManyToManyField(User, verbose_name=_("RPPO Editors"), 
        related_name='rppoeditors+', blank=True, null=True)
    modify_date = models.DateTimeField(_("Modify date"), blank=True, null=True, editable=True)
    edituser = models.CharField(max_length=50, unique=True, blank=True, null=True)
    #responsable_sec = models.ManyToManyField(User, verbose_name=_("Responsable IPPC Secretariat"), 
    #    related_name='resp_sec+', blank=True, null=True)
 
  
   # coop_type = models.IntegerField(_("Cooperation type"),
    #choices=COOPTYPE_CHOICES, default=COOPTYPE_0)
   # table_id = models.PositiveIntegerField()
   # acronym = models.CharField(max_length=50, unique=True, blank=True, null=True)
 
     
   
    def __unicode__(self):
        return u'%s' % (self.name,)
    
    
class PartnersContactPointHistory(models.Model):
    partnerspage = models.ForeignKey(PartnersPage)
    #contact_point = models.OneToOneField("auth.User",    verbose_name=_("RPPO/Organization Contact Point"), blank=True, null=True)
    contact_point = models.ForeignKey("auth.User",verbose_name=_("RPPO/Organization Contact Point"), blank=True, null=True)
   
    start_date = models.DateTimeField(_("Nomination start date"), blank=True, null=True, editable=True)
    end_date = models.DateTimeField(_("Nomination end date"), blank=True, null=True, editable=True)
    
class PartnersEditorHistory(models.Model):
    partnerspage = models.ForeignKey(PartnersPage)
    #editor = models.OneToOneField("auth.User",             verbose_name=_("Country Editor"), blank=True, null=True)
    editor = models.ForeignKey("auth.User",verbose_name=_("RPPO/Organization Editor"), blank=True, null=True)
    start_date = models.DateTimeField(_("Nomination start date"), blank=True, null=True, editable=True)
    end_date = models.DateTimeField(_("Nomination end date"), blank=True, null=True, editable=True)
          
        
class NotificationMessageRelate(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    countries = models.ManyToManyField(CountryPage,
        verbose_name=_("Country you want to notify"),
        related_name='notificatiocountries', blank=True, null=True)
    partners = models.ManyToManyField(PartnersPage,
        verbose_name=_("Partners: RPPOs, IOs, Liasons you want to notify"),
        related_name='notificatiopartners', blank=True, null=True)
    notifysecretariat =  models.BooleanField( verbose_name=_("Notify Secretariat"),help_text=_("check if you want to notify Secretariat"),)
    notify =  models.BooleanField( verbose_name=_("Notify"),help_text=_("check if you want to send out the notification"))
    link = models.CharField(_("Link"), blank=True, null=True, max_length=250)
    new_or_updated = models.CharField(_("New or Updated"), blank=True, null=True, max_length=250)
    updated_last = models.DateTimeField(_("Last updated"), blank=True, null=True, editable=True)
    sent_date = models.DateTimeField(_("Sent date"), blank=True, null=True, editable=True)
        

def validate_file_extension(value):
    if not (value.name.endswith('.pdf') or value.name.endswith('.doc')or value.name.endswith('.txt')
        or value.name.endswith('.xls')   or value.name.endswith('.ppt') or value.name.endswith('.jpg')
        or value.name.endswith('.png') or value.name.endswith('.gif') or value.name.endswith('.xlsx')
        or value.name.endswith('.docx')or value.name.endswith('.ppt') or value.name.endswith('.pptx') or value.name.endswith('.zip')
        or value.name.endswith('.rar')):
        raise ValidationError(u'You can only upload files:  txt pdf ppt doc xls jpg png docx xlsx pptx zip rar.')
           
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
    title = models.CharField(_("Title"), blank=True, null=True, max_length=250)
    title_es = models.CharField(_("Title ES"), blank=True, null=True, max_length=250)
    title_fr = models.CharField(_("Title FR"), blank=True, null=True, max_length=250)
    title_ru = models.CharField(_("Title RU"), blank=True, null=True, max_length=250)
    title_ar = models.CharField(_("Title AR"), blank=True, null=True, max_length=250)
    title_zh = models.CharField(_("Title ZH"), blank=True, null=True, max_length=250)
    # author = models.ForeignKey(User, related_name="publication_author")
    file_en = models.FileField(_("File - English"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/en/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_es = models.FileField(_("File - Spanish"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/es/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_fr = models.FileField(_("File - French"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/fr/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_ru = models.FileField(_("File - Russian"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/ru/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_ar = models.FileField(_("File - Arabic"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/ar/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_zh = models.FileField(_("File - Chinese"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/zh/%Y/%m/"),
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
    topic_number = models.CharField(_("Topic Number"), max_length=100,
                                  blank=True)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    old_id = models.CharField(max_length=50, blank=True, null=True)  
    groups = models.ManyToManyField(Group, 
        verbose_name=_("Groups this publication is NOT accessible to"), 
        related_name='publicationgroups', blank=True, null=True)
    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                         default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If no title is given when created, create one from the
        file name.
        """
        if not self.id and not self.title:
            name = unquote(self.file_en.url).split("/")[-1].rsplit(".", 1)[0]
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
class PublicationFile(models.Model):
    publication = models.ForeignKey(Publication)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/publication/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class PublicationUrl(models.Model):
    publication = models.ForeignKey(Publication)
    description = models.CharField(_("Description"),max_length=100, blank=True)
    url_for_more_information = models.URLField(blank=True, null=True)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information

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

# do we need a table for this? or do http://djangosnippets.org/snippets/2753/ ?
class PestStatus(models.Model):
    """ Pest Statuses """
    status = models.CharField(_("Pest Status"), max_length=500)

    def __unicode__(self):
        return self.status
        
    class Meta:
        verbose_name_plural = _("Pest Statuses")
    pass

class PreferredLanguages(models.Model):
    """ PreferredLanguages """
    preferredlanguage = models.CharField(_("Preferred Languages"), max_length=500)

    def __unicode__(self):
        return self.preferredlanguage
        
    class Meta:
        verbose_name_plural = _("Preferred Languages")
    pass

class EppoCode(models.Model):
    """ Eppo Code """
    codename = models.CharField(_("Eppo code"), max_length=250)
    codedescr = models.CharField(_("description"), max_length=250)
    code = models.CharField(_("Code"), max_length=100)
    codeparent = models.CharField(_("Parent code"), max_length=100)
    lang = models.CharField(_("Language"), max_length=100)
    preferred = models.CharField(_("Preferred language"), max_length=100)
    authority = models.CharField(_("Authority"), max_length=250)
    creationdate = models.DateTimeField(_("creationdate"), default=datetime.now, editable=False)

    def __unicode__(self):
        return self.codename

        




class ContactType(models.Model):
    """ Contact Types """
    contacttype = models.CharField(_("Contact Type"), max_length=500)

    def __unicode__(self):
        return self.contacttype
        
    class Meta:
        verbose_name_plural = _("Contact Types")
    pass

class IppcUserProfile(models.Model):
    """ User Profiles for IPPC"""
    
    GENDER_CHOICES = (
        (1, _("Mr.")),
        (2, _("Ms.")),
        (3, _("Mrs.")),
        (4, _("Professor.")),
        (5, _("M.")),
        (6, _("Mme.")),
        (7, _("Dr.")),
        (8, _("Sr.")),
        (9, _("Sra.")),
        
    )
    UNITS_CHOICES = (
        (1, _("IPPC Secretary's Office")),
        (2, _("Standard Setting Unit")),
        (3, _("Implementation Facilitation Unit")),
        (4, _("Integration and Support Team")),
        (5, _("ePhyto Group")),
    )


    user = models.OneToOneField("auth.User")
    title = models.CharField(_("Professional Title"), blank=True, null=True, max_length=100)
    first_name = models.CharField(_("First Name"), max_length=30)
    last_name = models.CharField(_("Last Name"), max_length=30)
    # main email address already provided by auth.User
    email_address_alt = models.EmailField(_("Alternate Email"), default="", max_length=75, blank=True, null=True)
    contact_type = models.ManyToManyField(ContactType,
        verbose_name=_("Contact Type"),
        related_name='contact_type+', blank=True, null=True,
        )
    gender = models.PositiveSmallIntegerField(_("Prefix"), choices=GENDER_CHOICES, blank=True, null=True)
    profile_photo = models.FileField(_("Profile Photo"), upload_to="profile_photos", blank=True)
    bio = models.TextField(_("Brief Biography"), default="", blank=True, null=True)
    # should be expertise, but we can just change the label for now
    expertise = models.TextField(_("Description/expertise"), default="", blank=True, null=True)
    
    address1 = models.CharField(_("Organization"), blank=True, max_length=250)
    address2 = models.TextField(_("Address"), default="", blank=True, null=True)
    #city = models.CharField(_("City"), blank=True, max_length=100)
    #state = models.CharField(_("State"), blank=True, max_length=100, help_text="or Province")
    #zipcode = models.CharField(_("Zip Code"), blank=True, max_length=20)
    #address_country = CountryField(_("Address Country"), blank=True, null=True)
    # country is the 'tag' marking permissions for Contact Point and Editors
    country = models.ForeignKey(CountryPage, related_name="user_country_page", blank=True, null=True)
    partner = models.ForeignKey(PartnersPage, related_name="user_partner_page", blank=True, null=True)

    phone = models.CharField(_("Phone"), blank=True, max_length=80)
    fax = models.CharField(_("Fax"), blank=True, max_length=80)
    mobile = models.CharField(_("Mobile"), blank=True, max_length=80)
 
    preferredlanguage = models.ManyToManyField(PreferredLanguages,
        verbose_name=_("Preferred Languages"),
        related_name='preferredlanguages+', blank=True, null=True,
        )
    website = models.URLField(_("Website"),blank=True, null=True)
    date_account_created = models.DateTimeField(_("IPP Member Since"), default=datetime.now, editable=False)
    date_contact_registration = models.DateTimeField(_("Date contact registration"), blank=True, null=True, default=datetime.now, editable=True)
    modify_date = models.DateTimeField(_("modify_date"), blank=True, null=True, default=None, editable=True)
    staff_oder = models.IntegerField(_("order"),  blank=True, null=True)
    unit_team = models.PositiveSmallIntegerField(_("Unit/Team"), choices=UNITS_CHOICES, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.modify_date = datetime.now()
#        group_1=Group.objects.get(name="FAO Regional Plant Protection Officers")
#        users_1 = group_1.user_set.all()
#        for u in users_1:
#           user_obj=User.objects.get(username=u)
#           print(user_obj == self.user)   
#         
#        emailto_all = []
#        group=Group.objects.get(name="FAO Regional Officers Notification group")
#        users = group.user_set.all()
#        for u in users:
#           user_obj=User.objects.get(username=u)
#           user_email=user_obj.email
#           print(user_email)   
#           emailto_all.append(str(user_email))
#           subject='IPPC Notification of updates in FAO Regional Plant Protection Officers'       
#           text='<html><body><p>Dear IPPC user,</p><p>a FAO Regional Plant Protection Officers has updated his profile:<br><b>'+ str(self.user)+'</p><br/><br/>-- International Plant Protection Convention team </p></body></html>'
#           notifificationmessage = mail.EmailMessage(subject,text,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
#           notifificationmessage.content_subtype = "html"  
#           sent =notifificationmessage.send()
            
        super(IppcUserProfile, self).save(*args, **kwargs)
        
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
    report_number = models.CharField(_("Report Number"), blank=True, null=True, max_length=100)
    #file = models.FileField(_("Pest Report Document"), upload_to="pest_reports/%Y/%m/", blank=True)
    pest_status = models.ManyToManyField(PestStatus,
        verbose_name=_("Pest Status"),
        related_name='pest_status+', blank=True, null=True,
        help_text=_("Under ISPM 8 -"))
    pest_identity = models.ForeignKey(Names, null=True, blank=True)
    #pest_identity = models.ForeignKey(EppoCode, null=True, blank=True)
    #pest_identity = models.TextField(_("Identity of Pest"),    blank=True, null=True)
    hosts = models.TextField(_("Hosts or Articles concerned"),
        blank=True, null=True)
    geographical_distribution = models.TextField(_("Geographical Distribution"),
        blank=True, null=True)
    nature_of_danger = models.TextField(_("Nature of Immediate or potential danger"),
        blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"),
        blank=True, null=True)
    #url_for_more_information = models.URLField(blank=True, null=True)
    
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    notification=generic.GenericRelation(NotificationMessageRelate)
    old_id = models.CharField(max_length=50)
    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                         default=False)
    importedfromeppo = models.BooleanField(verbose_name=_("Imported from Eppo"),
                                         default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)
    verified_date = models.DateTimeField(_("Verified date"),
        blank=True, null=True, editable=False)
    to_verify = models.BooleanField(verbose_name=_("to verify"),
                                         default=False)    
    # =todo:
    # commodity_groups = 
    # keywords / tags = 
    # objects = models.Manager()

    objects = SearchableManager()
    # attachments = AttachmentManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("Pest Reports")
        # abstract = True

    def __unicode__(self):
        return self.title

    def country_code(self):
        return self.country
    
    def filename(self):
        return os.path.basename(self.file.name)
        
        
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

class PestReportFile(models.Model):
    pestreport = models.ForeignKey(PestReport)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/pestreport/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]


class PestReportUrl(models.Model):
    pestreport = models.ForeignKey(PestReport)
    url_for_more_information = models.URLField(blank=True, null=True)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information
    

class DraftProtocol(Displayable, models.Model):
    """ DraftProtocol"""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
 
    users = models.ManyToManyField(User, 
        verbose_name=_("Users this DP is accessible to"), 
        related_name='dpusers', blank=True, null=True)
    groups = models.ManyToManyField(Group, 
        verbose_name=_("Groups this DP is accessible to"), 
        related_name='dpgroups', blank=True, null=True)
    
    closing_date = models.DateTimeField(_("Closing date"), blank=True, null=True)
    summary = models.TextField(_("Summary or Short Description"), blank=True, null=True)
    filetext = models.FileField(_("Attachment (comments on protocol text)"), upload_to="files/dp/%Y/%m/", blank=True)
    filefig = models.FileField(_("Attachment (comments on protocol figures)"), upload_to="files/dp/%Y/%m/", blank=True)
    old_id = models.CharField(max_length=50, blank=True, null=True)
  
    objects = SearchableManager()
    # attachments = AttachmentManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("Draft Protocols")
        # abstract = True

    def __unicode__(self):
        return self.title

    def filetextname(self):
        return os.path.basename(self.filetext.name)
    def filefigname(self):
        return os.path.basename(self.filefig.name)
   
    def is_past_due(self):
        if timezone.now() > self.closing_date:
            return True
        else: 
            return False   
        
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a DraftProtocol."""
        return ('draftprotocol-detail', (), {
                            'year': self.publish_date.strftime("%Y"),
                            'month': self.publish_date.strftime("%m"),
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(DraftProtocol, self).save(*args, **kwargs)

class DraftProtocolFile(models.Model):
    draftprotocol = models.ForeignKey(DraftProtocol)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload Additional background documents', upload_to='files/dp/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]


class DraftProtocolComments(Displayable, models.Model):
    author = models.ForeignKey(User, related_name="draftprotocolcomments_author")
    draftprotocol = models.ForeignKey(DraftProtocol)
    expertise = models.TextField(_("Your Expertise On This Pest"), blank=True, null=True)
    institution = models.TextField(_("Your Institution"), blank=True, null=True)
    comment = models.TextField(_("Your Comment"), blank=True, null=True)
    filetext = models.FileField(_("Attachment (comments on protocol text)"), upload_to="files/dp/comm/%Y/%m/", blank=True)
    filefig = models.FileField(_("Attachment (comments on protocol figures)"), upload_to="files/dp/comm/%Y/%m/", blank=True)
  
    def __unicode__(self):  
        return self.comment  
    def name(self):
        return self.comment    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(DraftProtocolComments, self).save(*args, **kwargs)
    def filetextname(self):
        return os.path.basename(self.filetext.name)
    def filefigname(self):
        return os.path.basename(self.filefig.name)
    
    
    
# used by Reporting Obligation type
BASIC_REP_1 = 1
BASIC_REP_2 = 2
BASIC_REP_3 = 3
BASIC_REP_4 = 4
BASIC_REP_TYPE_CHOICES = (
    (BASIC_REP_1, _("Description of the NPPO")), 
    (BASIC_REP_4, _("Legislation: Phytosanitary Requirements/Restrictions/Prohibitions")),
    (BASIC_REP_2, _("Entry Points")),
    (BASIC_REP_3, _("List of Regulated Pests")),
)



      
class ReportingObligation(Displayable, models.Model):
    """ ReportingObligation"""
    country = models.ForeignKey(CountryPage, related_name="reporting_obligation_country_page")
    author = models.ForeignKey(User, related_name="reporting_obligation_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable

    reporting_obligation_type = models.IntegerField(_("Reporting Obligation"), choices=BASIC_REP_TYPE_CHOICES, default=BASIC_REP_3)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    #file = models.FileField(_("Report Document"), upload_to="reporting_obligation/%Y/%m/", blank=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    #url_for_more_information = models.URLField(max_length=500,blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    notification=generic.GenericRelation(NotificationMessageRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
  
    
    old_id = models.CharField(max_length=50)
    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                         default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)
    verified_date = models.DateTimeField(_("Verified date"),
        blank=True, null=True, editable=False)
    to_verify = models.BooleanField(verbose_name=_("to verify"),
                                         default=False) 
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Reporting Obligations")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('reporting-obligation-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'month': self.publish_date.strftime("%m"),
                            # 'day': self.pub_date.strftime("%d"),
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.publication_date = datetime.today()
            #self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(ReportingObligation, self).save(*args, **kwargs)
  
    def reporting_obligation_type_verbose(self):
        return dict(BASIC_REP_TYPE_CHOICES)[self.reporting_obligation_type]
    
#c
class ReportingObligation_File(models.Model):
    reportingobligation = models.ForeignKey(ReportingObligation)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/reportingobligation/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class ReportingObligationUrl(models.Model):
    reportingobligation = models.ForeignKey(ReportingObligation)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information   

class CnPublication(Displayable, models.Model):
    """ CnPublication"""
    country = models.ForeignKey(CountryPage, related_name="cnpublication_country_page")
    author = models.ForeignKey(User, related_name="cnpublicatio_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    agenda_number = models.CharField(_("Agenda Item Number"), max_length=100, blank=True)
    document_number = models.CharField(_("Document Number"), max_length=100,  blank=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    old_id = models.CharField(max_length=50)
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Publications from Countries")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a country publication."""
        return ('country-publication', (), {
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
        super(CnPublication, self).save(*args, **kwargs)
 
    
class CnPublicationFile(models.Model):
    cnpublication = models.ForeignKey(CnPublication)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/cn_publication/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class CnPublicationUrl(models.Model):
    cnpublication = models.ForeignKey(CnPublication)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information   

class PartnersPublication(Displayable, models.Model):
    """ PartnerPublication"""
    partners = models.ForeignKey(PartnersPage, related_name="partnerspublication_country_page")
    author = models.ForeignKey(User, related_name="partnerspublication_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    agenda_number = models.CharField(_("Agenda Item Number"), max_length=100, blank=True)
    document_number = models.CharField(_("Document Number"), max_length=100,  blank=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    old_id = models.CharField(max_length=50)
    # objects = models.Manager()
    objects = SearchableManager()
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Publications from Partners")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a partner publication."""
        return ('partner-publication', (), {
                            'partners': self.partners.name, # =todo: get self.country.name working
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
        super(PartnersPublication, self).save(*args, **kwargs)
 
    
class PartnersPublicationFile(models.Model):
    partnerspublication = models.ForeignKey(PartnersPublication)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/partner_publication/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class PartnersPublicationUrl(models.Model):
    partnerspublication = models.ForeignKey(PartnersPublication)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information   


EVT_REP_1 = 1
EVT_REP_2 = 2
EVT_REP_3 = 3
EVT_REP_4 = 4
EVT_REP_5 = 5
EVT_REP_TYPE_CHOICES = (
    (EVT_REP_3, _("Organizational Arrangements of Plant Protection")),
    (EVT_REP_5, _("Rationale for Phytosanitary Requirements")),
    (EVT_REP_2, _("Non-compliance")),
    (EVT_REP_4, _("Pest status")),
    (EVT_REP_1, _("Emergency Actions")), 
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
    #file = models.FileField(_("Report Document"), upload_to="event_reporting/%Y/%m/", blank=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    #url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    notification=generic.GenericRelation(NotificationMessageRelate)
    old_id = models.CharField(max_length=50)
    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                         default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)
    verified_date = models.DateTimeField(_("Verified date"),
        blank=True, null=True, editable=False)
    to_verify = models.BooleanField(verbose_name=_("to verify"),
                                         default=False)
    objects = SearchableManager()
    
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Contact for Info")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    #@models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    #def get_absolute_url(self): # "view on site" link will be visible in admin interface
    ##    """Construct the absolute URL for a Pest Report."""
    #    return ('event-reporting-detail', (), {
    #                        'country': self.country.name, # =todo: get self.country.name working
    #                       'year': self.publish_date.strftime("%Y"),
    #                        'month': self.publish_date.strftime("%m"),
    #                        # 'day': self.pub_date.strftime("%d"),
    #                        'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.publication_date = datetime.today()
           
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(EventReporting, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def event_rep_type_verbose(self):
        return dict(EVT_REP_TYPE_CHOICES)[self.event_rep_type]
  
    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )


class EventreportingFile(models.Model):
    eventreporting = models.ForeignKey(EventReporting)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/eventreporting/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class EventreportingUrl(models.Model):
    eventreporting = models.ForeignKey(EventReporting)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information

WEB_1 = 1
WEB_2 = 2
WEB_3 = 3
WEB_4 = 4
WEB_5 = 5
WEB_TYPE_CHOICES = (
    (WEB_1, _("NPPO")), 
    (WEB_2, _("RPPO")),
    (WEB_3, _("International Organization")),
    (WEB_4, _("Research Institute")),
    (WEB_5, _("Other")),
)
     
class Website(Displayable, models.Model):
    """ Event Reporting"""
    country = models.ForeignKey(CountryPage, related_name="website_country_page")
    author = models.ForeignKey(User, related_name="website__reporting_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    web_type = models.IntegerField(_("Type of Website"), choices=WEB_TYPE_CHOICES, default=None)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    old_id = models.CharField(max_length=50)
    objects = SearchableManager()
    
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Websites")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    #@models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    #def get_absolute_url(self): # "view on site" link will be visible in admin interface
    ##    """Construct the absolute URL for a Pest Report."""
    #    return ('event-reporting-detail', (), {
    #                        'country': self.country.name, # =todo: get self.country.name working
    #                       'year': self.publish_date.strftime("%Y"),
    #                        'month': self.publish_date.strftime("%m"),
    #                        # 'day': self.pub_date.strftime("%d"),
    #                        'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(Website, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def event_rep_type_verbose(self):
        return dict(WEB_TYPE_CHOICES)[self.web_type]
  
    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )



class WebsiteUrl(models.Model):
    website = models.ForeignKey(Website)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information            

class PartnersWebsite(Displayable, models.Model):
    """ Event Reporting"""
    partners = models.ForeignKey(PartnersPage, related_name="partnerswebsite_partner_page")
    author = models.ForeignKey(User, related_name="partnerswebsite__reporting_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    web_type = models.IntegerField(_("Type of Website"), choices=WEB_TYPE_CHOICES, default=None)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    old_id = models.CharField(max_length=50)
    objects = SearchableManager()
    
    search_fields = ("title", "short_description")

    class Meta:
        verbose_name_plural = _("Websites")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    #@models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    #def get_absolute_url(self): # "view on site" link will be visible in admin interface
    ##    """Construct the absolute URL for a Pest Report."""
    #    return ('event-reporting-detail', (), {
    #                        'country': self.country.name, # =todo: get self.country.name working
    #                       'year': self.publish_date.strftime("%Y"),
    #                        'month': self.publish_date.strftime("%m"),
    #                        # 'day': self.pub_date.strftime("%d"),
    #                        'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(PartnersWebsite, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
    def event_rep_type_verbose(self):
        return dict(WEB_TYPE_CHOICES)[self.web_type]
  
    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )



class PartnersWebsiteUrl(models.Model):
    partnerswebsite = models.ForeignKey(PartnersWebsite)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information    
    
    
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
    pest_under_consideration = models.TextField(_("Pest under consideration"), blank=True, null=True)    
    pfa_type = models.IntegerField(_("Type of recognition"), choices=PFA_TYPE_1_CHOICES, default=None)
    #file = models.FileField(_("Additional information and Documentation"), upload_to="pestfreearea/%Y/%m/", blank=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    #url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    
    
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    notification=generic.GenericRelation(NotificationMessageRelate)
    old_id = models.CharField(max_length=50)
    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                         default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)
    verified_date = models.DateTimeField(_("Verified date"),
        blank=True, null=True, editable=False)
    
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

class PestFreeAreaFile(models.Model):
    pfa = models.ForeignKey(PestFreeArea)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/pfa/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class PestFreeAreaUrl(models.Model):
    pfa = models.ForeignKey(PestFreeArea)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information
    
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
    #file = models.FileField(_("Additional information and Documentation"), upload_to="implemenationispm/%Y/%m/", blank=True)
    mark_registered_type = models.IntegerField(_(" Is the ISPM No.15 mark registered as a trade mark in your country??"), choices=YES_NO_DONTKNOW_CHOICES, default=None)
    image = models.ImageField(_("Image of mark"), upload_to="implemenationispm/images/%Y/%m/", blank=True)
    
    # =todo Image
    short_description = models.TextField(_("Enter a description of mark"),  blank=True, null=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    #url_for_more_information = models.URLField(blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    
    
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    notification=generic.GenericRelation(NotificationMessageRelate)
    old_id = models.CharField(max_length=50)
    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                         default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)
    verified_date = models.DateTimeField(_("Verified date"),
        blank=True, null=True, editable=False)
    
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

class ImplementationISPMFile(models.Model):
    implementationispm = models.ForeignKey(ImplementationISPM)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/implementationispm/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
  
class ImplementationISPMUrl(models.Model):
    implementationispm = models.ForeignKey(ImplementationISPM)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information

class CountryNews(Displayable, models.Model):
    """ CountryNews"""
    country = models.ForeignKey(CountryPage, related_name="countrynews_country_page")
    author = models.ForeignKey(User, related_name="countrynews_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    short_description = models.TextField(_("Text"),  blank=True, null=True)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    image = models.ImageField(_("Image"), upload_to="countrynews/images/%Y/%m/", blank=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    objects = SearchableManager()
    search_fields = ("title", "short_description")
    old_id = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = _("Country News")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL """
        return ('country_news-detail', (), {
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
        super(CountryNews, self).save(*args, **kwargs)

 
    def imagename(self):
        return os.path.basename(self.image.name)

class CountryNewsFile(models.Model):
    countrynews = models.ForeignKey(CountryNews)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/countrynews/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
  
class CountryNewsUrl(models.Model):
    countrynews = models.ForeignKey(CountryNews)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information
    
    
class PartnersNews(Displayable, models.Model):
    """ partnersNews"""
    partners = models.ForeignKey(PartnersPage, related_name="partnersnews_partner_page")
    author = models.ForeignKey(User, related_name="partnersnews_author")
    
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    short_description = models.TextField(_("Text"),  blank=True, null=True)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    image = models.ImageField(_("Image"), upload_to="countrynews/images/%Y/%m/", blank=True)
    contact_for_more_information = models.TextField(_("Contact for more information"), blank=True, null=True)    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    commname=generic.GenericRelation(CommodityKeywordsRelate)
    old_id = models.CharField(max_length=50)
    objects = SearchableManager()
    search_fields = ("title", "short_description")
     
    class Meta:
        verbose_name_plural = _("Country News")
        # abstract = True

    def __unicode__(self):
        return self.title

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL """
        return ('partnersnews-detail', (), {
                            'partners': self.partners.name, # =todo: get self.country.name working
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
        super(PartnersNews, self).save(*args, **kwargs)

 
    def imagename(self):
        return os.path.basename(self.image.name)

class PartnersNewsFile(models.Model):
    partnersnews = models.ForeignKey(PartnersNews)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/partnersnews/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
  
class PartnersNewsUrl(models.Model):
    partnersnews = models.ForeignKey(PartnersNews)
    url_for_more_information = models.URLField(blank=True, null=True,max_length=500)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information
    
    
class Poll(models.Model):
    question = models.CharField(max_length=200)
    polltext = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    closing_date = models.DateTimeField('close date',blank=True, null=True,)
    
    userspoll = models.ManyToManyField(User,
        verbose_name=_("Users this forum post is accessible to"),
        related_name='pollusers', blank=True, null=True)
    groupspoll = models.ManyToManyField(Group,
        verbose_name=_("Groups this forum post is accessible to"),
        related_name='pollgroups', blank=True, null=True)
    login_required = models.BooleanField(verbose_name=_("Login required"),
                                         default=True)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def is_past_due(self):
        if timezone.now() > self.closing_date:
            return True
        else: 
            return False
        
class CommentFile(models.Model):
    comment = models.ForeignKey(ThreadedComment)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/forum/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]


class Poll_Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text

class PollVotes(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    choice= models.CharField(max_length=50)
    comment= models.CharField(max_length=200)
  
class EmailUtilityMessage(models.Model):
    emailfrom = models.CharField(_("From: "),max_length=200,default=_("ippc@fao.org"),help_text=_("The email will be sent from ippc@fao.org, if you want you can specify an other sender email address."))
    emailto = models.TextField(_("Send to users that are not registered in IPPC: "),default=_("ippc@fao.org"),help_text=_("Please leave ippc@fao.org for the form to work, and enter email addresses of addition recipients, separated by comma. Example: ippc@fao.org, someone@somewhere.tld, etc@etc.tld"))
    subject = models.CharField(_("Subject: "),max_length=200)
    messagebody = models.TextField(_("Message: "),max_length=500,blank=True, null=True)
    date = models.DateTimeField('date')
    sent =  models.BooleanField()
    
    #User.__unicode__ = user_unicode_patch
    users = models.ManyToManyField(User,
            verbose_name=_("Send to single users:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='emailusers', blank=True, null=True)
    groups = models.ManyToManyField(Group,
            verbose_name=_("Send to groups:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='emailgroups', blank=True, null=True)
    
    def __unicode__(self):  
         return self.subject 
    
class EmailUtilityMessageFile(models.Model):
    emailmessage = models.ForeignKey(EmailUtilityMessage)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Attach a file', upload_to='files/email/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
    
BOOL_CHOICES_0 = 0  
BOOL_CHOICES_1 = 1
BOOL_CHOICES_2 = 2
BOOL_CHOICES = (
    (BOOL_CHOICES_0, _("MASS EMAIL")),
    (BOOL_CHOICES_1, _("MERGE Email")),
    (BOOL_CHOICES_2, _("Forum Notification")),
) 
def validate_csvfile_extension(value):
    if not (value.name.endswith('.xls')   or value.name.endswith('.csv') or value.name.endswith('.xlsx')):
        raise ValidationError(u'You can only upload files:  csv xls  xlsx')
  
  
class MassEmailUtilityMessage(models.Model):
    emailfrom = models.CharField(_("From: "),max_length=200,default=_("ippc@fao.org"),help_text=_("The email will be sent from ippc@fao.org, if you want you can specify an other sender email address."))
    emailto = models.CharField(_("Send to users that are not registered in IPPC: "),max_length=500,default=_("ippc@fao.org"),blank=True, null=True,help_text=_("Enter email addresses of additional recipients, separated by comma. Example: ippc@fao.org, someone@somewhere.tld, etc@etc.tld"))
    #emailto = models.TextField(_("Send to users that are not registered in IPPC: "),default=_("ippc@fao.org"),help_text=_("Please leave ippc@fao.org for the form to work, and enter email addresses of addition recipients, separated by comma. Example: ippc@fao.org, someone@somewhere.tld, etc@etc.tld"))
    emailtoISO3 = models.TextField(_("TO: "),default=_(""),help_text=_(""))
    emailcc = models.CharField(_("CC: "),default=_("ippc@fao.org"),max_length=500,blank=True, null=True, help_text=_("enter email addresses of CC recipients, separated by comma. Example: ippc@fao.org,someone@somewhere.tld,etc@etc.tld"))
    subject = models.CharField(_("Subject: "),max_length=200)
    messagebody = models.TextField(_("Message: "),max_length=500,blank=True, null=True)
    date = models.DateTimeField('date')
    sent =  models.BooleanField()
    status =  models.BooleanField()
    not_sentto = models.TextField(_("notsent: "),blank=True, null=True)
    sentto = models.TextField(_("sent: "),blank=True, null=True)
    not_senttoISO3 = models.TextField(_("notsent: "),blank=True, null=True)
    senttoISO3 = models.TextField(_("sent: "),blank=True, null=True)
    author = models.ForeignKey(User, related_name="author")
    
    csv_file = models.FileField(_("Attach CSV file conteining the specific entries"), upload_to='files/email/', validators=[validate_csvfile_extension], blank=True,help_text=_("Follow the instructions on top of this page."))
    #mass_merge = models.NullBooleanField(_("Select if this is a MASS or MERGE mail"), choices=BOOL_CHOICES,default=0, help_text=_(" "),)
    massmerge = models.IntegerField(_("Select if this is a MASS or MERGE mail"), choices=BOOL_CHOICES, default=BOOL_CHOICES_0, help_text=_(" "),)
    #User.__unicode__ = user_unicode_patch
    users = models.ManyToManyField(User,
            verbose_name=_("Send to single users:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='massemailusers', blank=True, null=True)
    groups = models.ManyToManyField(Group,
            verbose_name=_("Send to groups:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='massemailgroups', blank=True, null=True)
    def __unicode__(self):  
         return self.subject 
     
     
     
    
class MassEmailUtilityMessageFile(models.Model):
    emailmessage = models.ForeignKey(MassEmailUtilityMessage)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Attach a file', upload_to='files/email/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
    
QA_STATUS_1 = 1
QA_STATUS_2 = 2
QA_STATUS_3 = 3
QA_STATUS_CHOICES = (
    (QA_STATUS_1, _("None")), 
    (QA_STATUS_2, _("Published")),
    (QA_STATUS_3, _("Rejected")),
)
     
class QAQuestion(Displayable, models.Model):
    """ Q A Question """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    search_fields = ("title", "short_description")
    short_description = models.TextField("Description",blank=True, null=True)
    questionopen = models.BooleanField(verbose_name=_("Open"), default=True)
    questiondiscard = models.IntegerField(_("Publish or Reject"), choices=QA_STATUS_CHOICES, default=QA_STATUS_1)
 
    user = models.ForeignKey(User) 
    class Meta:
        verbose_name_plural = _("QAQuestion")
        # abstract = True
#
    def __unicode__(self):
        return self.title
         
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(QAQuestion, self).save(*args, **kwargs)




class QAAnswer(Displayable, models.Model):
    """ Q A Answer """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    search_fields = ("title", "short_description")
    #description = models.TextField("OPTIONAL: Provide more background",blank=True, null=True)
    user = models.ForeignKey(User) 
    question = models.ForeignKey(QAQuestion)
    bestanswer =  models.BooleanField( verbose_name=_("Best answer"),)
    answertext= models.TextField("",blank=True, null=True)
    answerdiscard = models.IntegerField(_("Publish or Reject"), choices=QA_STATUS_CHOICES, default=QA_STATUS_1)
 
    
    class Meta:
        verbose_name_plural = _("QAAnswer")
        # abstract = True

    def __unicode__(self):
        return self.title
         
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(QAAnswer, self).save(*args, **kwargs)
        
               
 
class AnswerVotes(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(QAAnswer)
    up= models.CharField(max_length=50)

class ReminderMessage(models.Model):
    emailfrom = models.CharField(_("From: "),max_length=200,default=_("ippc@fao.org"),help_text=_("The email will be sent from ippc@fao.org, if you want you can specify an other sender email address."))
    emailto = models.TextField(_("Send to:"),default=_("ippc@fao.org"),help_text=_("Please leave ippc@fao.org for the form to work, and enter email addresses of addition recipients, separated by comma. Example: ippc@fao.org, someone@somewhere.tld, etc@etc.tld"))
    subject = models.CharField(_("Subject: "),max_length=200)
    messagebody = models.TextField(_("Message: "),max_length=500,blank=True, null=True)
    date = models.DateTimeField('date')
    sent =  models.BooleanField()
    
    def __unicode__(self):  
         return self.subject 


CONTACTUS_TYPE_1 = 1
CONTACTUS_TYPE_2 = 2
CONTACTUS_TYPE_3 = 3
CONTACTUS_TYPE_4 = 4
CONTACTUS_TYPE_5 = 5
CONTACTUS_TYPE_6 = 6
CONTACTUS_TYPE_7 = 7
CONTACTUS_TYPE_8 = 8
CONTACTUS_TYPE_9 = 9
CONTACTUS_TYPE_10 = 10
CONTACTUS_TYPE_11 = 11
CONTACTUS_TYPE_CHOICES = (
    (CONTACTUS_TYPE_1, _("General enquiries")), 
    (CONTACTUS_TYPE_2, _("Implementation / Capacity Development")),
    (CONTACTUS_TYPE_3, _("Registration of ISPM 15 symbol")),
    (CONTACTUS_TYPE_4, _("National Reporting Obligations (NROs)")),
    (CONTACTUS_TYPE_5, _("News / Communications")),
    (CONTACTUS_TYPE_6, _("ePhyto")),
    (CONTACTUS_TYPE_7, _("Online Comment System (OCS)")),
    (CONTACTUS_TYPE_8, _("Resource Mobilization")),
    (CONTACTUS_TYPE_9, _("Standard Setting")),
    (CONTACTUS_TYPE_10, _("Technical assistance (IT/bugs) ")),
    (CONTACTUS_TYPE_11, _("International Year of Plant Health (IYPH)")), 
)

class ContactUsEmailMessage(models.Model):
    emailfrom = models.CharField(_("From: "),max_length=200,help_text=_("Specify sender email address."))
    contact_us_type = models.IntegerField(_("Aera of Interest"), choices=CONTACTUS_TYPE_CHOICES, default=CONTACTUS_TYPE_1)
    subject = models.CharField(_("Subject: "),max_length=200)
    messagebody = models.TextField(_("Message: "),max_length=500,blank=True, null=True)
    date = models.DateTimeField('date')
    sent =  models.BooleanField()
    
    def __unicode__(self):  
         return self.subject 
     
    def contact_us_type_verbose(self):
        return dict(CONTACTUS_TYPE_CHOICES)[self.contact_us_type]


class FAQsCategory(Displayable, models.Model):
    """ FAQs Category"""
#    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
#    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
#    # status - provided by mezzanine.core.models.displayable
#    # publish_date - provided by mezzanine.core.models.displayable
    faqcat_oder = models.IntegerField(_("order"),  blank=True, null=True)
 
    class Meta:
        verbose_name_plural = _("FAQsCategory")
        
#
    def __unicode__(self):
        return self.title
         
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(FAQsCategory, self).save(*args, **kwargs)
        
class FAQsItem(Displayable, models.Model):
    """ FAQs Item"""
     #slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
#    # status - provided by mezzanine.core.models.displayable
#    # publish_date - provided by mezzanine.core.models.displayable
    faqcategory = models.ForeignKey(FAQsCategory, related_name="faqscategory")
    faq_description = models.TextField(_("Description"),  blank=True, null=True)
    faq_anchor = models.CharField(_("Anchor"),max_length=200)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    search_fields = ("title", "short_description")
     
    class Meta:
        verbose_name_plural = _("FAQsItem")
        #abstract = True
#
    def __unicode__(self):
        return self.title
         
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(FAQsItem, self).save(*args, **kwargs)
        
AUTOREGISTER_1 = 1
AUTOREGISTER_2 = 2
AUTOREGISTER_3 = 3
AUTOREGISTER_CHOICES = (
    (AUTOREGISTER_1, _("Pending approval")), 
    (AUTOREGISTER_2, _("Approved")),
    (AUTOREGISTER_3, _("Rejected")),
)
class UserAutoRegistration(models.Model):
    firstname = models.CharField(_("First name"), blank=True, null=True,max_length=250,)
    lastname = models.CharField(_("Last name"), blank=True, null=True,max_length=250,)
    email = models.CharField(_("Email"), blank=True, null=True,max_length=250,)
    organisation = models.CharField(_("Organisation"), blank=True, null=True,max_length=250,)
    country = models.ForeignKey(CountryPage, blank=True, null=True)
    status = models.IntegerField(_("Publish or Reject"), choices=AUTOREGISTER_CHOICES, default=AUTOREGISTER_1)
    publish_date = models.DateTimeField(_("Publish date"), blank=True, null=True, editable=True)
    def __unicode__(self):  
        return self.lastname+self.firstname+'.'
    def name(self):
        return self.lastname
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        super(UserAutoRegistration, self).save(*args, **kwargs)

IRSS_ACT_TYPE_1 = 1
IRSS_ACT_TYPE_2 = 2
IRSS_ACT_TYPE_3 = 3
IRSS_ACT_TYPE_4 = 4
IRSS_ACT_TYPE_5 = 5
IRSS_ACT_TYPE_6 = 6
IRSS_ACT_TYPE_CHOICES = (
    (IRSS_ACT_TYPE_1, _("-- select --")), 
    (IRSS_ACT_TYPE_2, _("Study")),
    (IRSS_ACT_TYPE_3, _("Workshop & Symposium")),
    (IRSS_ACT_TYPE_4, _("Survey")),
    (IRSS_ACT_TYPE_5, _("Other")),
)
    
class IRSSActivity(Displayable, models.Model):
    """ IRSS Activity"""
     #slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
     # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
     # status - provided by mezzanine.core.models.displayable
     # publish_date - provided by mezzanine.core.models.displayable
    
    activitytype = models.IntegerField(_("Type of activity"), choices=IRSS_ACT_TYPE_CHOICES, default=IRSS_ACT_TYPE_1)
    authoreditor = models.CharField(_("Author/Editor"),max_length=200)
    short_description = models.TextField(_("Description"),  blank=True, null=True)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    image = models.ImageField(_("Image of document"), upload_to="irss/images/%Y/%m/", blank=True)
  
    search_fields = ("title", "short_description")
     
    class Meta:
        verbose_name_plural = _("IRSSActivitys")
        #abstract = True
#
    def irssctivity_type_verbose(self):
        return dict(IRSS_ACT_TYPE_CHOICES)[self.activitytype]
    
    def __unicode__(self):
        return self.title
         
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(IRSSActivity, self).save(*args, **kwargs)
        
class IRSSActivityFile(models.Model):
    irssactivity = models.ForeignKey(IRSSActivity)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/irss/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
   
FUND_TYPE_0 =0
FUND_TYPE_1 = 1
FUND_TYPE_2 =2
FUNDS = (
    (FUND_TYPE_0, _("No funding")),
    (FUND_TYPE_1, _("Airfare funding")),
    (FUND_TYPE_2, _("Airfare and DSA funding")),
)  

    
class UserMembershipHistory(models.Model):
    user = models.ForeignKey("auth.User",verbose_name=_("User"), blank=True, null=True)
    group = models.ForeignKey(Group,  blank=True, null=True)
    start_date = models.DateTimeField(_("Nomination start date"), blank=True, null=True, editable=True)
    end_date = models.DateTimeField(_("Nomination end date"), blank=True, null=True, editable=True)
    funding =  models.IntegerField(_("Funding"), choices=FUNDS, default=None,blank=True, null=True)
    countrypage = models.ForeignKey(CountryPage,blank=True, null=True )
    partnerpage = models.ForeignKey(PartnersPage,blank=True, null=True)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/membership/%Y/%m/%d/', validators=[validate_file_extension])









# used by MediaKitDocument type
#MEDIAKIT_TYPE_1 = 1
#MEDIAKIT_TYPE_2 = 2
#MEDIAKIT_TYPE_3 = 3
#MEDIAKIT_TYPE_4 = 4
#MEDIAKIT_TYPE_5 = 5
#MEDIAKIT_TYPE_6 = 6
#MEDIAKIT_TYPE_7 = 7
#MEDIAKIT_TYPE_CHOICES = (
#    (MEDIAKIT_TYPE_1, _("Brochures")), 
#    (MEDIAKIT_TYPE_2, _("Manual & Reports")),
#    (MEDIAKIT_TYPE_3, _("Posters")),
#    (MEDIAKIT_TYPE_4, _("Factsheets")),
#    (MEDIAKIT_TYPE_5, _("Calendars")),
#    (MEDIAKIT_TYPE_6, _("E-Learning")),
#    (MEDIAKIT_TYPE_7, _("Logos")),
#)



class MediaKitCategory(models.Model):
    """ Participant Role """
    category = models.CharField(_("Category"), max_length=500)

    def __unicode__(self):
        return self.category
        
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        app_label = 'ippc'
    pass   
  
class MediaKitDocument(Orderable):
    """Single publication to add in a publication library."""

    class Meta:
        verbose_name = _("MediaKitDocument")
        verbose_name_plural = _("MediaKitDocuments")
        
    title = models.CharField(_("Title"), blank=True, null=True, max_length=250)
    #mediakit_type = models.IntegerField(_("MediaKit Document  Type"), choices=MEDIAKIT_TYPE_CHOICES, default=None)
    mediakit_type = models.ForeignKey(MediaKitCategory,verbose_name=_("Type"), blank=True, null=True,default=-1)
   
    image = models.ImageField(_("Image of document"), upload_to="files/mediakitdocument/images/%Y/%m/", blank=True)
    file_en = models.FileField(_("File - English"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/mediakitdocument/en/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)  
    file_es = models.FileField(_("File - Spanish"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/mediakitdocument/es/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_fr = models.FileField(_("File - French"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/mediakitdocument/fr/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_ru = models.FileField(_("File - Russian"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/mediakitdocument/ru/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_ar = models.FileField(_("File - Arabic"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/mediakitdocument/ar/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    file_zh = models.FileField(_("File - Chinese"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/mediakitdocument/zh/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
   
    link_en = models.URLField(verbose_name=_("Link En"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
    link_es = models.URLField(verbose_name=_("Link Es"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
    link_fr = models.URLField(verbose_name=_("Link Fr"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
    link_ru = models.URLField(verbose_name=_("Link Ru"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
    link_ar = models.URLField(verbose_name=_("Link Ar"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
    link_zh = models.URLField(verbose_name=_("Link Zh"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
           
            
    slug = models.SlugField(max_length=200, blank=True, null=True,
            unique_for_date='modify_date')
    status = models.IntegerField(_("Status"), choices=PUBLICATION_STATUS_CHOICES, default=IS_PUBLIC)
    
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False, auto_now=True)
   
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If no title is given when created, create one from the
        file name.
        """
        if not self.id and not self.title:
            name = unquote(self.file_en.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.title = name
        super(MediaKitDocument, self).save(*args, **kwargs)

    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Publication."""
        return ('mediakitdocument-detail', (), {
                        
                            'pk': self.pk})
                            
    def mediakit_type_verbose(self):
        return dict(MEDIAKIT_TYPE_CHOICES)[self.mediakit_type]
                         

TREATMENT_STATUS_1 = 1
TREATMENT_STATUS_2 = 2
TREATMENT_STATUS_CHOICES = (
    (TREATMENT_STATUS_1, _("Adopted")),
    (TREATMENT_STATUS_2, _("NON Adopted")),
)



         
         
class PhytosanitaryTreatmentType(models.Model):
    """ Phytosanitary Treatment Type"""
    typecode=models.CharField(_("Treatment type code"), max_length=8)
    typename = models.CharField(_("Treatment Full name + Treatment code"), max_length=250)
    typefullname=models.CharField(_("Treatment Full name"), max_length=250)
   
    def __unicode__(self):
        return self.typefullname
    
class PhytosanitaryTreatment(Displayable, models.Model):
    """  Phytosanitary Treatment """

    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False)
    summary = models.TextField(_("Summary or Short Description"),
        blank=True, null=True)

    treatment_type = models.ForeignKey(PhytosanitaryTreatmentType, null=True, blank=True)
    treatment_status =models.IntegerField(_("Treatment status"),
        choices=TREATMENT_STATUS_CHOICES, default=TREATMENT_STATUS_1)
    treatment_pestidentity_other = models.CharField(_("Other pest"),help_text=_("type the text for the pest here if not found in the DB"),max_length=500,  blank=True, null=True)
    treatment_commodityidentity_other = models.CharField(_("Other commodity"),help_text=_("type the text for the commodity here if not found in the DB"),max_length=500,blank=True, null=True)
    
    treatmentschedule = models.TextField(_("Treatment schedule: additional Information"),
        blank=True, null=True)
        
    chemical=models.CharField(_("Chemical (active ingredient)"), max_length=250 ,blank=True, null=True)
    duration=models.CharField(_("Duration and Temperature"), max_length=250, blank=True, null=True)
    temperature=models.CharField(_("Temperature"), max_length=250, blank=True, null=True)
    concentration=models.CharField(_("Concentration"), max_length=250, blank=True, null=True)
        
    countries = models.ManyToManyField(CountryPage, 
        verbose_name=_("Countries"), 
        related_name='pythotreatment_country_page', blank=True, null=True)
    internationally_approved = models.BooleanField(verbose_name=_("Internationally approved"),help_text=_("click on the checkbox if the Phytosanitary treatment is Internationally approved"),
                                         default=False)
    treatmeant_link = models.URLField(verbose_name=_("Link"), help_text=_("type the correct URL e.g. http://www.test.com"),blank=True, null=True)
    objects = SearchableManager()
    # attachments = AttachmentManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("Phytosanitary Treatments")
        # abstract = True

    def __unicode__(self):
        return self.title

    def country_code(self):
        return self.country
    
    def filename(self):
        return os.path.basename(self.file.name)
        
    
    def treatment_status_verbose(self):
        return dict(TREATMENT_STATUS_CHOICES)[self.treatment_status]
      
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Pest Report."""
        return ('pythosanitary-treatment-detail', (), {
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(PhytosanitaryTreatment, self).save(*args, **kwargs)

class PhytosanitaryTreatmentPestsIdentity(models.Model):
    phytosanitarytreatment= models.ForeignKey(PhytosanitaryTreatment)
    pest = models.ForeignKey(Names, null=True, blank=True)
    pestidentitydescr = models.CharField(_("pestidentitydescr"), max_length=250, blank=True, null=True)
   
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.pest:
            eppocodeid=self.pest.id
            code =''
            latin=''
            family =''
            order =''
            common=''
            pestidentity=''
            if eppocodeid != None:
                db = MySQLdb.connect(DATABASES["default"]["HOST"],DATABASES["default"]["USER"],DATABASES["default"]["PASSWORD"],DATABASES["default"]["NAME"])
                cursor = db.cursor()

                code=get_object_or_404(Names, id=eppocodeid).eppocode
                if code!= '':    
                    latin=get_object_or_404(Names, eppocode=code,isolang='la', preferred="true").fullname
                    commonname=Names.objects.filter(eppocode=code,isolang='en',status='A').order_by('-m_date')
                    if commonname.count()>0:
                        common=commonname[0].fullname

                    cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+code+"';")
                    str1= cursor.fetchall()
                    codeparent=''
                    for row in str1:
                        codeparent=str1[0][0]
                    cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+codeparent+"';")
                    codeparent2=''
                    str2= cursor.fetchall()
                    for row in str2:
                        codeparent2=str2[0][0]
                    family = get_object_or_404(Names, eppocode=codeparent2,isolang='la', preferred="true").fullname

                    cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+codeparent2+"';")
                    codeparent3=''
                    str3= cursor.fetchall()
                    if len(str3)>0:
                          codeparent3=str3[0][0]
                    order = get_object_or_404(Names, eppocode=codeparent3,isolang='la', preferred="true").fullname
            db.close()     
            if  latin!='':
                pestidentity=pestidentity+'<i>'+latin+"</i>"
            if  family!='':
                pestidentity=pestidentity+ "<br>"+ family
            if  order!='':
                pestidentity=pestidentity+  " : "+ order
            if  common!='':
                pestidentity=pestidentity+  "<br>"+ common
            pestidentity=pestidentity+ "<br>"+ str(code)+"<br><br>"
            self.pestidentitydescr=  pestidentity  
        super(PhytosanitaryTreatmentPestsIdentity, self).save(*args, **kwargs)
   # def __unicode__(self):  
   #     return self  
#    def name(self):
#        return self.pest
#    
class PhytosanitaryTreatmentCommodityIdentity(models.Model):
    phytosanitarytreatment= models.ForeignKey(PhytosanitaryTreatment)
    commodity = models.ForeignKey(Names, null=True, blank=True)
    commoditydescr = models.CharField(_("pestidentitydescr"), max_length=250, blank=True, null=True)
   
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.commodity:
            eppocodeid=self.commodity.id
            code =''
            latin=''
            family =''
            order =''
            common=''
            commoditydescr=''
            if eppocodeid != None:
                db = MySQLdb.connect(DATABASES["default"]["HOST"],DATABASES["default"]["USER"],DATABASES["default"]["PASSWORD"],DATABASES["default"]["NAME"])
                cursor = db.cursor()

                code=get_object_or_404(Names, id=eppocodeid).eppocode
                if code!= '':    
                    latin=get_object_or_404(Names, eppocode=code,isolang='la', preferred="true").fullname
                    commonname=Names.objects.filter(eppocode=code,isolang='en',status='A').order_by('-m_date')
                    if commonname.count()>0:
                        common=commonname[0].fullname

                    cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+code+"';")
                    str1= cursor.fetchall()
                    codeparent=''
                    for row in str1:
                        codeparent=str1[0][0]
                    cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+codeparent+"';")
                    codeparent2=''
                    str2= cursor.fetchall()
                    for row in str2:
                        codeparent2=str2[0][0]
                    family = get_object_or_404(Names, eppocode=codeparent2,isolang='la', preferred="true").fullname

                    cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+codeparent2+"';")
                    codeparent3=''
                    str3= cursor.fetchall()
                    if len(str3)>0:
                          codeparent3=str3[0][0]
                    order = get_object_or_404(Names, eppocode=codeparent3,isolang='la', preferred="true").fullname
            db.close()     
            if  latin!='':
                commoditydescr=commoditydescr+'<i>'+latin+"</i>"
            if  family!='':
                commoditydescr=commoditydescr+ "<br>"+ family
            if  order!='':
                commoditydescr=commoditydescr+  " : "+ order
            if  common!='':
                commoditydescr=commoditydescr+  "<br>"+ common
            commoditydescr=commoditydescr+ "<br>"+ str(code)+"<br><br>"
            self.commoditydescr=  commoditydescr  
        super(PhytosanitaryTreatmentCommodityIdentity, self).save(*args, **kwargs)
        
    def __unicode__(self):  
        return self.commodity  
    def name(self):
        return self.commodity



            
class DraftingBodyType(models.Model):
    """ TOPIC DraftingBody Type"""
    draftingbody=models.CharField(_("Drafting Body"), max_length=250)
    draftingbody_fr = models.CharField(_("draftingbody fr"), max_length=500)
    draftingbody_es = models.CharField(_("draftingbody es"), max_length=500)
    draftingbody_ar = models.CharField(_("draftingbody ar"), max_length=500)
    draftingbody_ru = models.CharField(_("draftingbody ru"), max_length=500)
    draftingbody_zh = models.CharField(_("draftingbody zh"), max_length=500)
    
    def __unicode__(self):
        return self.draftingbody
#    
#TOPIC_STATUS_01 = -1
#TOPIC_STATUS_0 = 0
#TOPIC_STATUS_1 = 1
#TOPIC_STATUS_2 = 2
#TOPIC_STATUS_3 = 3
#TOPIC_STATUS_4 = 4
#TOPIC_STATUS_5 = 5
#TOPIC_STATUS_6 = 6
#TOPIC_STATUS_7 = 7
#TOPIC_STATUS_8 = 8
#TOPIC_STATUS_9 = 9
#TOPIC_STATUS_10 = 10
#TOPIC_STATUS_11 = 11
#TOPIC_STATUS_12 = 12
#TOPIC_STATUS_13 = 13
#TOPIC_STATUS_14 = 14
#TOPIC_STATUS_15 = 15
#TOPIC_STATUS_16 = 16
#TOPIC_STATUS_17 = 17
#TOPIC_STATUS_18 = 18
#TOPIC_STATUS_19 = 18
#TOPIC_STATUS_20 = 20
#TOPIC_STATUS_21 = 21
#TOPIC_STATUS_22 = 22
#TOPIC_STATUS_23 = 23
#TOPIC_STATUS_24 = 24
#TOPIC_STATUS_25 = 25
#TOPIC_STATUS_26 = 26
#TOPIC_STATUS_27 = 27
#TOPIC_STATUS_28 = 28
#TOPIC_STATUS_29 = 29
#TOPIC_STATUS_30 = 30
#TOPIC_STATUS_31 = 31
#TOPIC_STATUS_32 = 32
#TOPIC_STATUS_33 = 33
#TOPIC_STATUS_34 = 34
#TOPIC_STATUS_35 = 35
#TOPIC_STATUS_36 = 36
#TOPIC_STATUS_37 = 37
#TOPIC_STATUS_38 = 38
#TOPIC_STATUS_39 = 39
#TOPIC_STATUS_40 = 40
#TOPIC_STATUS_41 = 41
#TOPIC_STATUS_42 = 42
#TOPIC_STATUS_43 = 43
#TOPIC_STATUS_44 = 44
#TOPIC_STATUS_45 = 45
#TOPIC_STATUS_46 = 46



	
	


#REMOVE:
#    (TOPIC_STATUS_2, _("01. Added to the List of Topics by CPM")),
#      (TOPIC_STATUS_18, _("01. Added to list of topics")),
#   (TOPIC_STATUS_3, _("02. Draft specification approved by SC for Consultation")),
#    (TOPIC_STATUS_19, _("02. Draft PT under development ")),
#    (TOPIC_STATUS_20, _("02. Author selected")),
#    (TOPIC_STATUS_5, _("03. Draft term to SC for removal from list of topics")),
#   
#    (TOPIC_STATUS_7, _("03. Draft DP under  development")),
#    (TOPIC_STATUS_21, _("03. Draft PT approved by SC for first consultation")),
#(TOPIC_STATUS_8, _("04. Experts selected")),
#    (TOPIC_STATUS_23, _("04. Draft PT to second consultation")),
#    (TOPIC_STATUS_24, _("04. Draft DP under Expert Consultation")),
#    (TOPIC_STATUS_25, _("04. Draft term to SC for first consultation")),
#  (TOPIC_STATUS_9, _("05. Draft ISPM under development by Drafting Group / review by steward")), 
#    (TOPIC_STATUS_10, _("05. Draft DP to SC for first consultation")),
#    (TOPIC_STATUS_11, _("05. Draft term approved by SC for first consultation")),
#    (TOPIC_STATUS_27, _("05. Draft PT member comments being reviewed by TPPT ")),
#    
  
#    (TOPIC_STATUS_12, _("06. Draft ISPM approved by SC for first consultation")), 
#    (TOPIC_STATUS_28, _("06. Draft ISPM to second or subsequent consultation ")),
#    (TOPIC_STATUS_29, _("06. Draft PT with TPPT comments to SC for recommendation to CPM ")),
#    (TOPIC_STATUS_30, _("06. Draft term consultation comments being reviewed by TPG  ")),
#   
    
#    (TOPIC_STATUS_15, _("07. Draft term to second consultation")),
#    (TOPIC_STATUS_31, _("07. Draft ISPM recommended for adoption")),  
#    (TOPIC_STATUS_32, _("07. Draft PT recommended by SC to CPM")),  
#    (TOPIC_STATUS_33, _("07. Draft DP, member comments being reviewed by TPDP")),   
#
#
#     (TOPIC_STATUS_34, _("08. ISPM adopted")),
#
#    (TOPIC_STATUS_35, _("08. Draft DP recommended by TPDP to SC for adoption on behalf of the CPM")),
#    (TOPIC_STATUS_36, _("08. Draft term to additional consultation")),
    
#    (TOPIC_STATUS_37, _("09. Topic removed from the List of topics")),
#    (TOPIC_STATUS_38, _("09. PT adopted")),
#    (TOPIC_STATUS_39, _("09. Draft term to SC for recommendation to CPM")),
#  
#    (TOPIC_STATUS_40, _("10. DP adopted by SC on behalf of CPM")),
#    (TOPIC_STATUS_41, _("10. Draft term recommended by SC to CPM for adoption")),
      
	
#    
#
#    (TOPIC_STATUS_42, _("11. SC / TPDP reviewing objection")),
#    (TOPIC_STATUS_43, _("11. Draft term to CPM for a vote")),
#
#    (TOPIC_STATUS_44, _("12. TPG to do a across ISPM review")),
#    (TOPIC_STATUS_45, _("13. TPG noted term in the general recommendations on consistency")),
#    (TOPIC_STATUS_46, _("14. Term adopted")),
TOPIC_STATUS_01 = -1
TOPIC_STATUS_0 = 0
TOPIC_STATUS_1 = 1
TOPIC_STATUS_4 = 4
TOPIC_STATUS_6 = 6
TOPIC_STATUS_13 = 13
TOPIC_STATUS_14 = 14
TOPIC_STATUS_16 = 16
TOPIC_STATUS_17 = 17
TOPIC_STATUS_22 = 22
TOPIC_STATUS_26 = 26

TOPIC_STATUS_CHOICES = (
   (TOPIC_STATUS_01, _("-- select --")),
   (TOPIC_STATUS_0, _("00. Pending")),
   (TOPIC_STATUS_1, _("01. Topic added to the List of topics")),
   (TOPIC_STATUS_4, _("02. Draft specification to consultation")),
   (TOPIC_STATUS_6, _("03. Specification approved")),
   (TOPIC_STATUS_22, _("04. Draft ISPM under development")),
   (TOPIC_STATUS_26, _("05. Draft DP to expert consultation")),
   (TOPIC_STATUS_13, _("06. Draft ISPM to first consultation")),
   (TOPIC_STATUS_14, _("07. Draft ISPM to second or subsequent consultation")),   
   (TOPIC_STATUS_16, _("08. Draft ISPM recommended for adoption")),
   (TOPIC_STATUS_17, _("09. ISPM adopted")),
    )












TOPIC_PRIORITY_01 = -1
TOPIC_PRIORITY_0 = 0
TOPIC_PRIORITY_1 = 1
TOPIC_PRIORITY_2 = 2
TOPIC_PRIORITY_3 = 3
TOPIC_PRIORITY_4 = 4


TOPIC_PRIORITY_CHOICES = (
    (TOPIC_PRIORITY_01, _("-- please select --")),
    (TOPIC_PRIORITY_0, _("N/A")),    
    (TOPIC_PRIORITY_1, _("1")),
    (TOPIC_PRIORITY_2, _("2")),
    (TOPIC_PRIORITY_3, _("3")),
    (TOPIC_PRIORITY_4, _("4")),
    
)
 
TOPIC_TYPE_0 = 0
TOPIC_TYPE_1 = 1
TOPIC_TYPE_2 = 2
TOPIC_TYPE_CHOICES = (
    (TOPIC_TYPE_0, _("Technical Area for TPs and Topics for TPDP")),
    (TOPIC_TYPE_1, _("Topics for EWGs, TPFF, TPFQ, TPPT")),
    (TOPIC_TYPE_2, _("Subjects for  TPs")),
)


CPM_0=0
CPM_1998 = 1998
CPM_1999 = 1999
CPM_2001 = 2001
CPM_2002 = 2002
CPM_2003 = 2003
CPM_2004 = 2004
CPM_2005 = 2005
CPM_2006 = 2006
CPM_2007 = 2007
CPM_2008 = 2008
CPM_2009 = 2009
CPM_2010 = 2010
CPM_2011 = 2011
CPM_2012 = 2012
CPM_2013 = 2013
CPM_2014 = 2014
CPM_2015 = 2015
CPM_2016 = 2016
CPM_2017 = 2017
CPM_2018 = 2018
CPM_2019 = 2019
CPM_2020 = 2020
CPM_2021 = 2021
CPM_2022 = 2022
CPM_1994 = 1994
CPMS = (
    (CPM_0, _("-- select --")),
    (CPM_1994, ("1994")),
    (CPM_1998, ("ICPM 01")),
    (CPM_1999, _("ICPM 02")),
    (CPM_2001, _("ICPM 03")),
    (CPM_2002, _("ICPM 04")),
    (CPM_2003, _("ICPM 05")),
    (CPM_2004, _("ICPM 06")),
    (CPM_2005, _("ICPM 07")),
    (CPM_2006, _("CPM 01")),
    (CPM_2007, _("CPM 02")),
    (CPM_2008, _("CPM 03")),
    (CPM_2009, _("CPM 04")),
    (CPM_2010, _("CPM 05")),
    (CPM_2011, _("CPM 06")),
    (CPM_2012, _("CPM 07")),
    (CPM_2013, _("CPM 08")),
    (CPM_2014, _("CPM 09")),
    (CPM_2015, _("CPM 10")),
    (CPM_2016, _("CPM 11")),
    (CPM_2017, _("CPM 12")),
    (CPM_2018, _("CPM 13")),
    (CPM_2019, _("CPM 14")),
    (CPM_2020, _("CPM 15")),
    (CPM_2021, _("CPM 16")),
    (CPM_2022, _("CPM 17")),
)

SC_TYPE_0 = 0
SC_TYPE_1 = 1
SC_TYPE_2 = 2
SC_TYPE_3 = 3
SC_TYPE_4 = 4
SC_TYPE_5 = 5
SC_TYPE_6 = 6
SC_TYPE_7 = 7
SC_TYPE_8 = 8
SC_TYPE_9 = 9
SC_TYPE_10 = 10
SC_TYPE_11 = 11
SC_TYPE_12 = 12
SC_TYPE_13 = 13
SC_TYPE_14 = 14
SC_TYPE_15 = 15
SC_TYPE_16 = 16
SC_TYPE_17 = 17
SC_TYPE_18 = 18
SC_TYPE_19 = 19
SC_TYPE_20 = 20
SC_TYPE_21 = 21
SC_TYPE_22 = 22
SC_TYPE_23 = 23
SC_TYPE_24 = 24
SC_TYPE_25 = 25
SC_TYPE_26 = 26
SC_TYPE_27 = 27
SC_TYPE_28 = 28
SC_TYPE_29 = 29
SC_TYPE_30 = 30
SC_TYPE_31 = 31
SC_TYPE_32 = 32
SC_TYPE_33 = 33
SC_TYPE_34 = 34
SC_TYPE_35 = 35
SC_TYPE_36 = 36
SC_TYPE_37 = 37
SC_TYPE_38 = 38
SC_TYPE_CHOICES = (
    (SC_TYPE_0, _("-- select --")),
    (SC_TYPE_1, _("2004-05 SC")),
    (SC_TYPE_2, _("2004-11 SC")),
    (SC_TYPE_3, _("2005-04 SC")),
    (SC_TYPE_4, _("2005-11 SC")),
    (SC_TYPE_5, _("2006-05 SC")),
    (SC_TYPE_6, _("2006-11 SC")),
    (SC_TYPE_7, _("2007-04 SC")),
    (SC_TYPE_8, _("2007-11 SC")),
    (SC_TYPE_9, _("2008-04 SC")),
    (SC_TYPE_10, _("2008-11 SC")),
    (SC_TYPE_11, _("2009-04 SC")),
    (SC_TYPE_12, _("2009-11 SC")),
    (SC_TYPE_13, _("2010-04 SC")),
    (SC_TYPE_14, _("2010-11 SC")),
    (SC_TYPE_15, _("2011-04 SC")),
    (SC_TYPE_16, _("2011-11 SC")),
    (SC_TYPE_17, _("2012-04 SC")),
    (SC_TYPE_18, _("2013-11 SC")),
    (SC_TYPE_19, _("2013-05 SC")),
    (SC_TYPE_20, _("2013-11 SC")),
    (SC_TYPE_21, _("2014-05 SC")),
    (SC_TYPE_22, _("2014-11 SC")),
    (SC_TYPE_23, _("2015-05 SC")),
    (SC_TYPE_24, _("2015-11 SC")),
    (SC_TYPE_25, _("2016-05 SC")),
    (SC_TYPE_26, _("2016-11 SC")),
    (SC_TYPE_27, _("2017-05 SC")),
    (SC_TYPE_28, _("2017-11 SC")),
    (SC_TYPE_29, _("2018-05 SC")),
    (SC_TYPE_30, _("2018-11 SC")),
    (SC_TYPE_31, _("2019-05 SC")),
    (SC_TYPE_32, _("2019-11 SC")),
    (SC_TYPE_33, _("2020-05 SC")),
    (SC_TYPE_34, _("2020-11 SC")),
    (SC_TYPE_35, _("2021-05 SC")),
    (SC_TYPE_36, _("2021-11 SC")),
    (SC_TYPE_37, _("2022-05 SC")),
    (SC_TYPE_38, _("2022-11 SC")),
    
)
class StratigicObjective(models.Model):
    """ StratigicObjective """
    strategicobj = models.CharField(_("Stratigic objective"), max_length=500)
    description = models.CharField(_("Description"), max_length=500)
    strategicobj_fr = models.CharField(_("strategicobj fr"), max_length=500)
    strategicobj_es = models.CharField(_("strategicobj es"), max_length=500)
    strategicobj_ar = models.CharField(_("strategicobj ar"), max_length=500)
    strategicobj_ru = models.CharField(_("strategicobj ru"), max_length=500)
    strategicobj_zh = models.CharField(_("strategicobj zh"), max_length=500)
    def __unicode__(self):
        return self.strategicobj
        
    class Meta:
        verbose_name_plural = _("StratigicObjectives")
    pass    

class Topic(Displayable, models.Model):
    """  Topic """

    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False)
    summary = models.TextField(_("Summary or Short Description"),
        blank=True, null=True)

    topicnumber = models.CharField(_("Topic number"),help_text=_("Topic number (e.g. 2008-01)"),max_length=50,  blank=False, null=False,unique=True)
    
    topic_type =models.IntegerField(_("Topic type"),choices=TOPIC_TYPE_CHOICES, default=TOPIC_TYPE_0,help_text=_("Choose:\nTechnical Area for TPs and Topics for TPDP [Table 1]\rTopics for EWGs, TPFF, TPFQ, TPPT [Table 2: select Drafting body 'EWG' or 'TPFF' or 'TPFQ' or 'TPPT']<br>Subjects for  TPs [Table 3: select Drafting body 'TPDP' | Table 4: select Drafting body 'TPPT' | Table 5: select Drafting body 'TPG']"))
    #topic_sub_type =models.IntegerField(_("Subject"),choices=TOPIC_SUB_CHOICES, default=TOPIC_TYPE_0,help_text=_("Chose a topic sub-type such as 'Subject' for the Table 3,4 and 5 of topics"))
    
    drafting_body = models.ManyToManyField(DraftingBodyType,
        verbose_name=_("Drafting Body"),
        related_name='drafting_body+', blank=True, null=True,
        help_text=_("Select all that apply."))
    priority =models.IntegerField(_("Priority"),choices=TOPIC_PRIORITY_CHOICES, default=TOPIC_PRIORITY_0)
    topicstatus =models.IntegerField(_("Status"), choices=TOPIC_STATUS_CHOICES, default=TOPIC_STATUS_0)
    strategicobj = models.ManyToManyField(StratigicObjective,verbose_name=_("Stratigic Objectives"), blank=True, null=True,help_text=_("Select all that apply."),)
    addedtolist =models.IntegerField(_("Added to the list at CPM"),  choices=CPMS, default=None)
    addedtolist_sc =models.IntegerField(_("Added to the list at SC"),choices=SC_TYPE_CHOICES, default=SC_TYPE_0)
    
    specification_number = models.CharField(_("Specification number"),max_length=500,  blank=True, null=True)
    topic_under = models.CharField(_("Topic under technical area (if applicable)"), max_length=500,  blank=True, null=True)
    

    is_version = models.BooleanField(verbose_name=_("oldversion"),
                                        default=False)
    parent_id = models.CharField(max_length=50,blank=True, null=True,)  
    topicnumber_version = models.CharField(_("Topic number Version"),max_length=50,  blank=True, null=True)
    
    objects = SearchableManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("Topics")
    #abstract = True

    def __unicode__(self):
        return self.topicnumber
       
   
    def priority_verbose(self):
        return dict(TOPIC_PRIORITY_CHOICES)[self.priority]
    def topicstatus_verbose(self):
        return dict(TOPIC_STATUS_CHOICES)[self.topicstatus]
    def addedtolist_verbose(self):
        return dict(CPMS)[self.addedtolist]
    def topic_type_verbose(self):
        return dict(TOPIC_TYPE_CHOICES)[self.topic_type]
    def addedtolist_sc_verbose(self):
        return dict(SC_TYPE_CHOICES)[self.addedtolist_sc]

      
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a it."""
        return ('topic-detail', (), {
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(Topic, self).save(*args, **kwargs)
        
class TopicLeads(models.Model):
    topic = models.ForeignKey(Topic, verbose_name=_("topic"))
    
    user = models.ForeignKey(User,verbose_name=_("User"), blank=True, null=True)
    representing_country = models.ForeignKey(CountryPage,  verbose_name=_("Representing Country "), blank=True, null=True )
    meetingassistantassigned = models.CharField(_("Date assigned"), max_length=500,  blank=True, null=True)
  
    class Meta:
        verbose_name = _("TopicLeads")
        verbose_name_plural = _("TopicLeads")
    
 
        
    
    def __unicode__(self):
        name=''
        if self.user!=None:
            userippc = get_object_or_404(IppcUserProfile, user_id=self.user.id)
            val=userippc.gender
            gender=''
            if val!= None:
                if val == 1:
                    gender= "Mr."
                elif val==2: 
                    gender= "Ms."
                elif val==3:    
                    gender= "Mrs."
                elif val==4:    
                    gender= "Professor."
                elif val==5:    
                    gender= "M."
                elif val==6:    
                    gender= "Mme."
                elif val==7:    
                    gender= "Dr."
                elif val==8:    
                    gender= "Sr."
                elif val==9:    
                    gender= "Sra."
        
            name=gender+' '+userippc.first_name+' '+(userippc.last_name).upper()
       
        return name
         
        
class TopicAssistants(models.Model):
    topic = models.ForeignKey(Topic, verbose_name=_("topic"))
    
    user = models.ForeignKey(User,verbose_name=_("User"), blank=True, null=True)
    representing_country = models.ForeignKey(CountryPage,  verbose_name=_("Representing Country "), blank=True, null=True )
    meetingassistantassigned = models.CharField(_("Date assigned"), max_length=500,  blank=True, null=True)
  
    class Meta:
        verbose_name = _("TopicAssistants")
        verbose_name_plural = _("TopicAssistants")
        
    def __unicode__(self):
        name=''
        if self.user!=None:
            userippc = get_object_or_404(IppcUserProfile, user_id=self.user.id)
            val=userippc.gender
            gender=''
            if val!= None:
                if val == 1:
                    gender= "Mr."
                elif val==2: 
                    gender= "Ms."
                elif val==3:    
                    gender= "Mrs."
                elif val==4:    
                    gender= "Professor."
                elif val==5:    
                    gender= "M."
                elif val==6:    
                    gender= "Mme."
                elif val==7:    
                    gender= "Dr."
                elif val==8:    
                    gender= "Sr."
                elif val==9:    
                    gender= "Sra."
        
            name=gender+' '+userippc.first_name+' '+(userippc.last_name).upper()
       
        return name  
          
class WorkshopCertificatesTool(models.Model):
    title = models.CharField(_("Title"),help_text=_("title of the workshop certificates tool item "), blank=True, null=True, max_length=250)
    workshoptitle = models.CharField(_("Workshop title"), max_length=200,help_text=_("Text that will appear in the Certitificate"))
    creation_date = models.DateTimeField('Creation date')
    filezip = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/w_certificates/%Y/%m/%d/', validators=[validate_file_extension])
    author = models.ForeignKey(User, related_name="authorwcertificate")
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.creation_date = datetime.today()
            
        super(WorkshopCertificatesTool, self).save(*args, **kwargs)
    
 
            
class CertificatesTool(models.Model):
    title = models.CharField(_("Title"), help_text=_("Text appearing in the certificate in the TITLE place"), blank=True, null=True, max_length=250)
    topicnumber = models.ForeignKey(Topic,help_text=_("Select from the list the 'Topic' of discussion in meetings"),blank=True, null=True)
    date = models.DateTimeField('date')
    creation_date = models.DateTimeField('creationdate')
    filezip = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/certificates/%Y/%m/%d/', validators=[validate_file_extension])
    author = models.ForeignKey(User, related_name="authorcertificate")
    
               
    users = models.ManyToManyField(User,
            verbose_name=_("Select  single users:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='certificatesusers', blank=True, null=True)
    groups = models.ManyToManyField(Group,
            verbose_name=_("Select groups:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='certificatesgroups', blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date = datetime.today()
            self.creation_date = datetime.today()
            
        super(CertificatesTool, self).save(*args, **kwargs)

            
class B_CertificatesTool(models.Model):
    title = models.CharField(_("Title"), help_text=_("Text appearing in the certificate"), blank=True, null=True, max_length=250)
    date = models.DateTimeField('date')
    filezip = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/b_certificates/%Y/%m/%d/', validators=[validate_file_extension])
    author = models.ForeignKey(User, related_name="authorbcertificate")

    user_name = models.CharField(_("User name"), help_text=_("Text of the user appearing in the certificate"), blank=True, null=True, max_length=250)
    role = models.CharField(_("Role"), help_text=_("Text of the role appearing in the certificate"), blank=True, null=True, max_length=250)
    text3 = models.CharField(_("Meeting/Committee name"), help_text=_("Text of the Meeting/Committee appearing in the certificate"), blank=True, null=True, max_length=250)
               
    groups = models.ManyToManyField(Group,
            verbose_name=_("Select groups:"),help_text=_("CTRL/Command+mouseclick for more than 1 selection"),
            related_name='cbertificatesgroups', blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date = datetime.today()
            
        super(B_CertificatesTool, self).save(*args, **kwargs)
        
class MyTool(models.Model):
    title = models.CharField(_("Title"), help_text=_("Text appearing in the certificate"), blank=True, null=True, max_length=250)
    mytext = models.TextField(_("mytext"), blank=True, null=True)
    
class MyTool2(models.Model):
    title = models.CharField(_("Title"), help_text=_("Text appearing in the certificate"), blank=True, null=True, max_length=250)
    nameh = models.CharField(_("NAMEh"), help_text=_("Text appearing in the certificate"), blank=True, null=True, max_length=250)
    name = models.CharField(_("NAME"), help_text=_("Text appearing in the certificate"), blank=True, null=True, max_length=250)
    
    mytext = models.TextField(_("mytext"), blank=True, null=True)
    
        
class NROStats(models.Model):
    title = models.CharField(_("Title"), help_text=_("Title-"), blank=True, null=True, max_length=250)
    date = models.DateTimeField('Until the date')
    datetraining = models.DateTimeField('Date of the Workshop/Training')
    datetraining_checked = models.BooleanField(verbose_name=_('check this if you inserted a date of a workshop/training'),
                                        default=False)
    selcns= models.CharField(_("Selected cns"), max_length=550)        
    class Meta:
        verbose_name = _("NROStats")
        verbose_name_plural = _("NROStats")
        app_label = 'ippc'        

                
#
## used by Resource
NONE = 0
NPPO = 1
RPPO = 2
OTHER = 3
TYPE_CONTACT_CHOICES = (
    (NONE, _("-- none --")), 
    (NPPO, _("NPPO")), 
    (RPPO, _("RPPO")),
    (OTHER, _("Other")),
)

class ProvidedBy(models.Model):
    """ ProvidedBy """
    provider = models.CharField(_("Provided By"), max_length=500)

    def __unicode__(self):
        return self.provider
        
    class Meta:
        verbose_name_plural = _("Provided By")
      
        
    pass

class ContributedResourceTag(models.Model):
    """ tag """
    tag = models.CharField(_("tag"), max_length=500)
    def __unicode__(self):
        return self.tag
        
    class Meta:
        verbose_name_plural = _("ContributedResource Tags")
      
    pass 

class ContributedResource(Displayable, models.Model):
    """Single Resource to add in a Resources library."""
  
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
         
    owner = models.ForeignKey(User, related_name="resourceowner")
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    publication_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    modify_date = models.DateTimeField(_("Modified date"),       blank=True, null=True, editable=False, auto_now=True)
    organization_providing = models.CharField(_("Organization providing Contributed Resource"), max_length=100,                                   blank=True)
    type_of_contact = models.IntegerField(_("Type of contact"), choices=TYPE_CONTACT_CHOICES, default=NONE)
    contact_email= models.CharField(_("Email of contact"), max_length=100, blank=True)
    author = models.TextField(_("Author/Editor name and address"),  blank=True, null=True)
    agree =  models.BooleanField( verbose_name=_("I agree to have these Phytosanitary Technical Resources published in public'."),default=False)
    ippc_resource =  models.BooleanField( verbose_name=_("Resource provided by the IPPC'."),default=False)
    resource_provide_by = models.ManyToManyField(ProvidedBy, 
        verbose_name=_("Resource provided by"), 
        related_name='resprovidedby', blank=True, null=True)
    featured =  models.BooleanField( verbose_name=_("Featured"),default=False)
    tag = models.ManyToManyField(ContributedResourceTag, 
        verbose_name=_("Tags"), 
        related_name='restags', blank=True, null=True)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    submittedby = models.TextField(_("Submitted by"),  blank=True, null=True)
  
   
    objects = SearchableManager()
    # attachments = AttachmentManager()
    search_fields = ("title", "short_description")
    
    class Meta:
        verbose_name = _("Contributed Resource")
        verbose_name_plural = _("Contributed Resources")
    
    def type_of_contact_verbose(self):
        return dict(TYPE_CONTACT_CHOICES)[self.type_of_contact]
  
    def __unicode__(self):
        return self.title
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Resource."""
        return ('resource-detail', (), {
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        super(ContributedResource, self).save(*args, **kwargs)

class ContributedResourceFile(models.Model):
    resource = models.ForeignKey(ContributedResource)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='uploads/resources/%Y/%m/%d/', validators=[validate_file_extension])

    class Meta:
        verbose_name = _("ContributedResourceFile")
        verbose_name_plural = _("ContributedResourceFiles")
       
    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]

class ContributedResourcePhoto(models.Model):
    resource = models.ForeignKey(ContributedResource)
    image = models.ImageField(_("Photo"), upload_to="files/resources/photos/%Y/%m/", blank=True)
    class Meta:
        verbose_name = _("ContributedResourcePhoto")
        verbose_name_plural = _("ContributedResourcePhotos")
        
    def __unicode__(self):  
        return self.image.name  
    def name(self):
        return self.image.name
    def filename(self):
        return os.path.basename(self.image.name) 
    def fileextension(self):
        return os.path.splitext(self.image.name)[1]


class ContributedResourceUrl(models.Model):
    resource = models.ForeignKey(ContributedResource)
    url_for_more_information = models.URLField(blank=True, null=True)
    class Meta:
        verbose_name = _("ContributedResourceUrl")
        verbose_name_plural = _("ContributedResourceUrls")
        
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information


####---new strut

class CommitteeMeeting(Orderable):
    """Single CommitteeMeeting to add in a publication library."""

    class Meta:
        verbose_name = _("CommitteeMeeting")
        verbose_name_plural = _("CommitteeMeetings")
        
    library = models.ForeignKey("PublicationLibrary", 
        related_name="committeemeeting") # related_name=committeemeeting...
        # ..is used in publicationlibrary template
    title = models.CharField(_("Title"), blank=True, null=True, max_length=250)
    title_es = models.CharField(_("Title ES"), blank=True, null=True, max_length=250)
    title_fr = models.CharField(_("Title FR"), blank=True, null=True, max_length=250)
    title_ru = models.CharField(_("Title RU"), blank=True, null=True, max_length=250)
    title_ar = models.CharField(_("Title AR"), blank=True, null=True, max_length=250)
    title_zh = models.CharField(_("Title ZH"), blank=True, null=True, max_length=250)
    link_to_page = models.CharField(_("Link to page"), blank=True, null=True,max_length=250)
    city = models.CharField(_("City"), blank=True, null=True, max_length=250)
    country  = models.ForeignKey(CountryPage)
    start_date  = models.DateTimeField(_("From"), blank=True, null=True, editable=True)
    end_date = models.DateTimeField(_("To"), blank=True, null=True, editable=True)
    agenda_link_en = models.CharField(_("Agenda link - English"),blank=True, null=True, max_length=250)
    agenda_link_es = models.CharField(_("Agenda link - Spanish"),blank=True, null=True, max_length=250)
    agenda_link_fr = models.CharField(_("Agenda link - French"),blank=True, null=True, max_length=250)
    agenda_link_ru = models.CharField(_("Agenda link - Russian"),blank=True, null=True, max_length=250)
    agenda_link_ar = models.CharField(_("Agenda link - Arabic"),blank=True, null=True, max_length=250)
    agenda_link_zh = models.CharField(_("Agenda link - Chinese"),blank=True, null=True, max_length=250)
 
    report_en = models.FileField(_("Report - English"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/en/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    report_es = models.FileField(_("Report - Spanish"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/es/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    report_fr = models.FileField(_("Report - French"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/fr/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    report_ru = models.FileField(_("Report - Russian"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/ru/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    report_ar = models.FileField(_("Report - Arabic"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/ar/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    report_zh = models.FileField(_("Report - Chinese"), 
            upload_to=upload_to("galleries.GalleryImage.file", "files/publication/zh/%Y/%m/"),
            unique_for_date='modify_date', max_length=204, 
            blank=True, null=True)        
    
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False, auto_now=True)
 
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If no title is given when created, create one from the
        file name.
        """
        if not self.id and not self.title:
            name = unquote(self.file_en.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.title = name
        super(CommitteeMeeting, self).save(*args, **kwargs)

    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Publication."""
        return ('publication-detail', (), {
                            # 'country': self.country.name, # =todo: get self.country.name working
                            # 'year': self.publish_date.strftime("%Y"),
                            # 'month': self.publish_date.strftime("%m"),
                            # 'day': self.pub_date.strftime("%d"),
                            'pk': self.pk})
                            
class CollapseContent(Orderable):
    """Single CollapseContent to add in a publication library."""

    class Meta:
        verbose_name = _("CollapseContent")
        verbose_name_plural = _("CollapseContents")
        
    library = models.ForeignKey("PublicationLibrary", 
        related_name="collapsecontent") # related_name=committeemeeting...
        # ..is used in publicationlibrary template
    title = models.CharField(_("Title"), blank=True, null=True, max_length=250)
    title_es = models.CharField(_("Title ES"), blank=True, null=True, max_length=250)
    title_fr = models.CharField(_("Title FR"), blank=True, null=True, max_length=250)
    title_ru = models.CharField(_("Title RU"), blank=True, null=True, max_length=250)
    title_ar = models.CharField(_("Title AR"), blank=True, null=True, max_length=250)
    title_zh = models.CharField(_("Title ZH"), blank=True, null=True, max_length=250)
    text_en = models.TextField(_("Text en"),  blank=True, null=True)
    text_es = models.TextField(_("Text es"),  blank=True, null=True)
    text_fr = models.TextField(_("Text fr"),  blank=True, null=True)
    text_ar = models.TextField(_("Text ar"),  blank=True, null=True)
    text_ru = models.TextField(_("Text ru"),  blank=True, null=True)
    text_zh = models.TextField(_("Text en"),  blank=True, null=True)
    collapsed =  models.BooleanField( verbose_name=_("Collapsed"),default=True)
    html =  models.BooleanField( verbose_name=_("in HTML"),default=True)
    bg_color_div =  models.CharField(_("Background Color DIV"), blank=True, null=True, max_length=50)
    
 
    
    modify_date = models.DateTimeField(_("Modified date"),
        blank=True, null=True, editable=False, auto_now=True)
 
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If no title is given when created, create one from the
        file name.
        """
#        if not self.id and not self.title:
#            name = unquote(self.file_en.url).split("/")[-1].rsplit(".", 1)[0]
#            name = name.replace("'", "")
#            name = "".join([c if c not in punctuation else " " for c in name])
#            # str.title() doesn't deal with unicode very well.
#            # http://bugs.python.org/issue6412
#            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
#                            for i, s in enumerate(name)])
#            self.title = name
        super(CollapseContent, self).save(*args, **kwargs)
        
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Publication."""
        return ('publication-detail', (), {
                            # 'country': self.country.name, # =todo: get self.country.name working
                            # 'year': self.publish_date.strftime("%Y"),
                            # 'month': self.publish_date.strftime("%m"),
                            # 'day': self.pub_date.strftime("%d"),
                            'pk': self.pk})
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


class TransPublicationLibraryPage(Translatable, RichText, Slugged):
    translation = models.ForeignKey(PublicationLibrary, related_name="translation")
    side_box = models.TextField( blank=True, null=True)
    class Meta:
        verbose_name = _("Translated Publication Library")
        verbose_name_plural = _("Translated Publication Libraries")
        ordering = ("lang",)
        #unique_together = ("lang", "translation")

class TransFAQsCategory(Translatable, RichText, Slugged):
    translation = models.ForeignKey(FAQsCategory, related_name="translation")

    class Meta:
        verbose_name = _("Translated FAQsCategory")
        verbose_name_plural = _("Translated FAQsCategorys")
        ordering = ("lang",)
       

class TransFAQsItem(Translatable, RichText, Slugged):
    translation = models.ForeignKey(FAQsItem, related_name="translation")
    faq_description = models.TextField(max_length=1000, blank=True)
    faq_anchor= models.CharField(max_length=1000, blank=True)
    
    class Meta:
        verbose_name = _("Translated FAQsItem")
        verbose_name_plural = _("Translated FAQsItems")
        ordering = ("lang",)


#
class TransTopic(Translatable,   Slugged):
    translation = models.ForeignKey(Topic, related_name="translation")
    topic_under = models.CharField(max_length=1000, blank=True)
    specification_number = models.CharField(max_length=1000, blank=True)

    class Meta:
        verbose_name = _("Translated Topic")
        verbose_name_plural = _("Translated Topics")
        ordering = ("lang",)

#
#class TransReportingObligation(Translatable,   Slugged):
#    translation = models.ForeignKey(ReportingObligation, related_name="translation")
#    short_description = models.CharField(max_length=1000, blank=True)
#
#    class Meta:
#        verbose_name = _("Translated ReportingObligation")
#        verbose_name_plural = _("Translated ReportingObligations")
#        ordering = ("lang",)
#        #unique_together = ("lang", "translation")
#        
