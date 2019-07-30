from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group


from mezzanine.conf import settings

from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from datetime import datetime
from django.template.defaultfilters import slugify, lower
from ippc.models import CountryPage

class IyphPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A Iyph  post.
    """

    categories = models.ManyToManyField("IyphCategory",
                                        verbose_name=_("Categories"), 
                                        blank=True, related_name="iyphposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("iyph.IyphPost.featured_image", "iyph"),
        format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Iyph")
        verbose_name_plural = _("Iyph")
        ordering = ("-publish_date",)

    @models.permalink
    def get_absolute_url(self):
        """
        URLs for iyph posts can either be just their slug, or prefixed
        with a portion of the post's publish date, controlled by the
        setting ``Iyph_URLS_DATE_FORMAT``, which can contain the value
        ``year``, ``month``, or ``day``. Each of these maps to the name
        of the corresponding urlpattern, and if defined, we loop through
        each of these and build up the kwargs for the correct urlpattern.
        The order which we loop through them is important, since the
        order goes from least granualr (just year) to most granular
        (year/month/day).
        """
        url_name = "iyph_post_detail"
        kwargs = {"slug": self.slug}
        date_parts = ("year", "month", "day")
        if settings.IYPH_URLS_DATE_FORMAT in date_parts:
            url_name = "iyph_post_detail_%s" % settings.IYPH_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.IYPH_URLS_DATE_FORMAT:
                    break
        return (url_name, (), kwargs)

    # These methods are deprecated wrappers for keyword and category
    # access. They existed to support Django 1.3 with prefetch_related
    # not existing, which was therefore manually implemented in the
    # iyph list views. All this is gone now, but the access methods
    # still exist for older templates.

    def category_list(self):
        from warnings import warn
        warn("iyph_post.category_list in templates is deprecated"
             "use iyph_post.categories.all which are prefetched")
        return getattr(self, "_categories", self.categories.all())

    def keyword_list(self):
        from warnings import warn
        warn("iyph_post.keyword_list in templates is deprecated"
             "use the keywords_for template tag, as keywords are prefetched")
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords


class IyphCategory(Slugged):
    """
    A category for grouping iyph posts into a series.
    """

    class Meta:
        verbose_name = _("Iyph Category")
        verbose_name_plural = _("Iyph Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("iyph_post_list_category", (), {"category": self.slug})
    
    
CHRON_1 = 1
CHRON_2 = 2
CHRON_3 = 3
CHRONS = (

    (CHRON_1, _("Global")),
    (CHRON_2, _("Regional")),
    (CHRON_3, _("National")),
)
PROGRAM_1 = 1
PROGRAM_2 = 2

PROGRAMME = (

    (PROGRAM_1, _("IYPH preparation events")),
    (PROGRAM_2, _("IYPH 2020 programme of events")),
)



    
class Chronology (Displayable, models.Model):
    """ Chronology """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    image = models.ImageField(_("Image of page of Event"), upload_to="uploads/iyph/%Y/%m/", blank=True)
    summary = models.TextField(_("Summary or Short Description"), blank=True, null=True)
    author = models.ForeignKey(User, related_name="chron_author")
    venue_description = models.TextField(_("Venue Description and map"), blank=True, null=True)
    
    start_date = models.DateTimeField(_("Start date"), blank=True, null=True, default=datetime.now, editable=True)
    end_date = models.DateTimeField(_("End date"), blank=True, null=True, default=datetime.now, editable=True)

    
    
    chron_type = models.IntegerField(_("Type of events"), choices=CHRONS, default=CHRON_1)
    programme_type = models.IntegerField(_("Programme Type"), choices=PROGRAMME, default=PROGRAM_1)
    venue = models.CharField(_("Venue"), max_length=250, blank=True, null=True)
    country = models.ForeignKey(CountryPage, related_name="country", default=-1)
  
    contact = models.CharField(_("Contact"),max_length=250, blank=True, null=True)
    url_website = models.URLField(_("Website URL"),blank=True, null=True)
    inhomepage =  models.BooleanField( verbose_name=_("Show in HOMPAGE"),default=False)
    is_key_event =  models.BooleanField( verbose_name=_("is Key Event"),default=False)
   
    # attachments = AttachmentManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("Chronologies")
        # abstract = True

    def __unicode__(self):
        return self.title
     
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Chronology."""
        print( 'year'+ self.publish_date.strftime("%Y"))
        print( 'month'+ self.publish_date.strftime("%m"))
        print( 'slug'+ self.slug)
        return ('chronology-detail', (), {
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
        super(Chronology, self).save(*args, **kwargs)
    
    def chron_type_verbose(self):
        typeverbose=''
        if self.chron_type == 1:
            typeverbose='G'
        elif self.chron_type == 2:
            typeverbose='R'
        elif self.chron_type == 3:
            typeverbose='N'
            
        return typeverbose
    

def validate_file_extension(value):
    if not (value.name.endswith('.pdf') or value.name.endswith('.doc')or value.name.endswith('.txt')
        or value.name.endswith('.xls')   or value.name.endswith('.ppt') or value.name.endswith('.jpg')
        or value.name.endswith('.png') or value.name.endswith('.gif') or value.name.endswith('.xlsx')
        or value.name.endswith('.docx')or value.name.endswith('.ppt') or value.name.endswith('.pptx') or value.name.endswith('.zip')
        or value.name.endswith('.rar')):
        raise ValidationError(u'You can only upload files:  txt pdf ppt doc xls jpg png docx xlsx pptx zip rar.')
    
class ChronologyFiles(models.Model):
    chronology = models.ForeignKey(Chronology)
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='uploads/iyph/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
    
    
RES_TYPE_1 = 1
RES_TYPE_2 = 2
RES_TYPE_3 = 3
RES_TYPE = (

    (RES_TYPE_1, _("IYPH Technical Advisory Board")),
    (RES_TYPE_2, _("IYPH International Steering Committee")),
    (RES_TYPE_3, _("General")),
)   

class IYPHSteeringCommitteeResource (Displayable, models.Model):
    """ IYPHSteeringCommitteeResource """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    summary = models.TextField(_("Summary or Short Description"), blank=True, null=True)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='uploads/iyph/%Y/%m/%d/', validators=[validate_file_extension])
    link = models.URLField(blank=True, null=True,)
    res_type = models.IntegerField(_("Type of Resource"), choices=RES_TYPE, default=RES_TYPE_1)
    image = models.ImageField(_("Image of document"), upload_to="uploads/iyph/%Y/%m/", blank=True)
    start_date = models.DateTimeField(_("Start date"), blank=True, null=True, default=datetime.now, editable=True)
    end_date = models.DateTimeField(_("End date"), blank=True, null=True, default=datetime.now, editable=True)
    venue = models.CharField(_("Venue"), max_length=250, blank=True, null=True)
 
 # attachments = AttachmentManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("IYPHSteeringCommitteeResources")
        # abstract = True

    def __unicode__(self):
        return self.title
     
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a IYPHSteeringCommitteeResource."""
        print( 'year'+ self.publish_date.strftime("%Y"))
        print( 'month'+ self.publish_date.strftime("%m"))
        print( 'slug'+ self.slug)
        return ('iyphsteeringcommitteeResource-detail', (), {
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
        super(IYPHSteeringCommitteeResource, self).save(*args, **kwargs)

class IYPHToolBoxCategory(Slugged):
    """
    A category for grouping iyph IYPHToolBox into a series.
    """

    class Meta:
        verbose_name = _("IYPHToolBox Category")
        verbose_name_plural = _("IYPHToolBox Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("iyphtoolbox_category", (), {"category": self.slug})
    
    

class IYPHToolBoxItem (Displayable, models.Model):
    """ IYPHToolBoxItem """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    summary = models.TextField(_("Summary or Short Description"), blank=True, null=True)
    categories = models.ManyToManyField("IYPHToolBoxCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="iyphtoolbox")
  
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='uploads/iyph/%Y/%m/%d/', validators=[validate_file_extension])
    url = models.URLField(blank=True, null=True,max_length=500)
   
    # attachments = AttachmentManager()
    search_fields = ("title", "summary")

    class Meta:
        verbose_name_plural = _("IYPHToolBoxItems")
        # abstract = True

    def __unicode__(self):
        return self.title
     
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a IYPHToolBoxItem."""
        print( 'year'+ self.publish_date.strftime("%Y"))
        print( 'month'+ self.publish_date.strftime("%m"))
        print( 'slug'+ self.slug)
        return ('iyphtoolboxitem-detail', (), {
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
        super(IYPHToolBoxItem, self).save(*args, **kwargs)

class PhotoLibrary(Displayable, models.Model):
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
 
  
        
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    def __unicode__(self):
        return self.title
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Photo."""
        return ('photo-library-detail', (), {
                            'slug': self.slug})
    class Meta:
        verbose_name = _("Photo Library")
        verbose_name_plural = _("Photo Libraries")
        # south overrides syncdb, so the following perms are not created
        # unless we are starting the project from scratch.
        # solution: python manage.py syncdb --all
        # or
        # manage.py datamigration myapp add_perm_foo --freeze=contenttypes --freeze=auth
        # http://stackoverflow.com/questions/1742021/adding-new-custom-permissions-in-django
        app_label = 'iyph'
        
        permissions = ( 
            ("can_view", "View Photo Library"),
        )  
from django.utils.html import format_html
        
class Photo(Displayable, models.Model):
    """Single Photo to add in a Photo library."""
  
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    modify_date = models.DateTimeField(_("Modified date"),       blank=True, null=True, editable=False, auto_now=True)
    library = models.ForeignKey("PhotoLibrary", related_name="photos") 
    photographer_first_name= models.CharField(_("Your first name"), max_length=100, blank=False, null=False)
    photographer_last_name = models.CharField(_("Your last name"), max_length=100, blank=False, null=False)
    email= models.CharField(_("Email address"), max_length=100, blank=False,null=False,)   
    emailconfirmation= models.CharField(_("Email address confirmation"), max_length=100, blank=False,null=False,)   
    country = models.ForeignKey(CountryPage, related_name="countryphotographer", default=-1)
    age =  models.CharField(_("Age (years)"), max_length=100, blank=False,null=False,) 
    image = models.ImageField(_("Photo"), upload_to="uploads/photocontest/", blank=False)
    date_taken = models.DateTimeField(_("Date Taken"), blank=False, null=False, editable=True)
    place_taken = models.CharField(_("Place/Country Taken"), max_length=100,   blank=False)
    short_description = models.TextField(_("Description/Caption"),  blank=False, null=False)
    agree =  models.BooleanField( verbose_name=_("By submitting a photo I agree to the Photo Contest Terms and Conditions."),default=False, blank=False)
    finalist =  models.BooleanField( verbose_name=_("Finalist"),default=False)
    exibition =  models.BooleanField( verbose_name=_("Selected for exibition"),default=False)
    prize= models.CharField(_("Prize"), max_length=100, blank=True)
    
    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
        app_label = 'iyph'
        
    def __unicode__(self):
        return self.title
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a photo."""
        return ('photo-detail', (), {
                            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        self.modify_date = datetime.now()
        self.status = 1
        super(Photo, self).save(*args, **kwargs)     


    def image_img(self):
        if self.image:
            return  format_html(' <a href="/static/'+str(self.image)+'"><img src="/static/'+str(self.image)+'" width="250px" ></a>'  )
       
       

AUTOREGISTER_1 = 1
AUTOREGISTER_2 = 2
AUTOREGISTER_3 = 3
AUTOREGISTER_CHOICES = (
    (AUTOREGISTER_1, _("Pending approval")), 
    (AUTOREGISTER_2, _("Approved")),
    
)

class PhotoAutoRegistration(models.Model):
    firstname = models.CharField(_("First name"), blank=True, null=True,max_length=250,)
    lastname = models.CharField(_("Last name"), blank=True, null=True,max_length=250,)
    email = models.CharField(_("Email"), blank=True, null=True,max_length=250,)
    summary =  models.CharField(_("Describe why you want to partecipate to the photo contest"), blank=True, null=True,max_length=500,)
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
        super(PhotoAutoRegistration, self).save(*args, **kwargs)

class IYPHPage(Displayable, models.Model):
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
 
  
        
    short_description = models.TextField(_("Short Description"),  blank=True, null=True)
    def __unicode__(self):
        return self.title
    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a Photo."""
        return ('iyphpage-detail', (), {
                            'slug': self.slug})
    class Meta:
        verbose_name = _("IYPHPage")
        verbose_name_plural = _("IYPHPages")
        # south overrides syncdb, so the following perms are not created
        # unless we are starting the project from scratch.
        # solution: python manage.py syncdb --all
        # or
        # manage.py datamigration myapp add_perm_foo --freeze=contenttypes --freeze=auth
        # http://stackoverflow.com/questions/1742021/adding-new-custom-permissions-in-django
        app_label = 'iyph'
        
                   
class Translatable(models.Model):
    """ Translations of user-generated content - https://gist.github.com/renyi/3596248"""
    lang = models.CharField(max_length=5, choices=settings.LANGUAGES)
    
    class Meta:
        abstract = True
        ordering = ("lang",)
        
class TransIyphPost(Translatable,   Slugged):
    translation = models.ForeignKey(IyphPost, related_name="translation")
    content = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Translated Iyph")
        verbose_name_plural = _("Translated Iyph")
        ordering = ("lang",)

   
class TransChronology(Translatable,   Slugged):
    translation = models.ForeignKey(Chronology, related_name="translation")
    summary = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Translated Chronology")
        verbose_name_plural = _("Translated Chronology")
        ordering = ("lang",)


   
class TransIYPHPage(Translatable,   Slugged):
    translation = models.ForeignKey(IYPHPage, related_name="translation")
    short_description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Translated IYPHPage")
        verbose_name_plural = _("Translated IYPHPage")
        ordering = ("lang",)

      