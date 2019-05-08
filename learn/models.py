
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

from mezzanine.utils.models import get_user_model_name
from mezzanine.generic.models import ThreadedComment
from t_eppo.models import Names




def user_unicode_patch(self):
    return '%s %s' % (self.first_name, self.last_name)



#  status
IS_HIDDEN = 1
IS_PUBLIC = 2
STATUS_CHOICES = (
    (IS_HIDDEN, _("Hidden - does not appear publically")), 
    (IS_PUBLIC, _("Public - visible ")),
)
    
class Category(models.Model):
    """ Category  """
    title = models.CharField(_("Category"), max_length=500)
   
    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    
class Course(models.Model):
    """ Course  """
    title = models.CharField(_("Course"), max_length=500)
    category = models.ForeignKey(Category, related_name="learn_category")
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, default=IS_PUBLIC)
    datecreated = models.DateTimeField(_("Date created"), blank=True, null=True, editable=False, auto_now=True)    
    coursesummary = models.TextField(_("Course summary"),  blank=True, null=True)
    enrolledusers = models.ManyToManyField(User, 
        verbose_name=_("Users enrolled"), 
        related_name='enrolledusers', blank=True, null=True)
    has_certificate = models.BooleanField(_("Generate a certificate of achivment "), help_text=_("True/False"), default=False)        
    certificategrade = models.CharField(_("Certificate grade"), max_length=50)
   
    def __unicode__(self):
        return self.title

class Module(models.Model):
    """ Module  """
    title = models.CharField(_("Title"), max_length=500)
    course = models.ForeignKey(Course, related_name="learn_course")
    image = models.ImageField(_("Image of background"), upload_to="files/mediakitdocument/images/", blank=True)
    modulesummary = models.TextField(_("Module summary"),  blank=True, null=True)
    previousmodule=  models.IntegerField(_("Previous"),default=0)
    nextmodule=  models.IntegerField(_("Next"),default=0)
 
    def __unicode__(self):
        return self.title

class Lesson(Orderable):
    """Lesson."""

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")
  
    course = models.ForeignKey(Course, related_name="learnmod_course")
    module = models.ForeignKey(Module, related_name="learn_module")
    title = models.CharField(_("Title"), blank=False, null=True, max_length=250)
    lessontext = models.TextField(_("Short Description"),  blank=True, null=True)
    previouspage=  models.IntegerField(_("Previous"),default=0)
    nextpage=  models.IntegerField(_("Next"),default=0)
   
  
    def __unicode__(self):
        return self.title
 
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('lesson-detail', (), {
                            'id': self.id.name, # =todo: get self.country.name working
                            
                            })

class Quiz(Orderable):
    """Lesson."""

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
  
    course = models.ForeignKey(Course, related_name="quiz_course")
    module = models.ForeignKey(Module, related_name="quiz_module")
    title = models.CharField(_("Title"), blank=False, null=True, max_length=250)
    quiztext = models.TextField(_("Short Description"),  blank=True, null=True)
    quizgrade = models.CharField(_("Quiz grade"), max_length=50)
   
  
    def __unicode__(self):
        return self.title
 
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('quiz-detail', (), {
                            'id': self.id.name, # =todo: get self.country.name working
                            
                            })
QUESTION_TYPE_1 = 1
QUESTION_TYPE_2 = 2
QUESTION_TYPE_3 = 3

QUESTION_TYPE_CHOICES = (
    (QUESTION_TYPE_1, _("Check boxes")), 
    (QUESTION_TYPE_2, _("Radio")),
    (QUESTION_TYPE_3, _("Multi choice select")),
)

QUESTIONNEXTPREV_TYPE_1 = 1
QUESTIONNEXTPREV_TYPE_2 = 2

QUESTIONNEXTPREV = (
    (QUESTIONNEXTPREV_TYPE_1, _("Question")), 
    (QUESTIONNEXTPREV_TYPE_2, _("QuestionM")),
  
)


                    
class Question(Orderable):
    """Question."""

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
  
    title = models.CharField(_("Title"), blank=False, null=True, max_length=250)
    q_summary = models.TextField(_("Summary"),  blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name="quiz")
    q_type= models.IntegerField(_("Question type"), choices=QUESTION_TYPE_CHOICES, default=QUESTION_TYPE_1)      
    previousq=  models.IntegerField(_("Previous"),default=0)
    nextq=  models.IntegerField(_("Next"),default=0)
    previousq_type= models.IntegerField(_("Question prev type"), choices=QUESTIONNEXTPREV, default=QUESTIONNEXTPREV_TYPE_1)    
    nextq_type= models.IntegerField(_("Question next type"), choices=QUESTIONNEXTPREV, default=QUESTIONNEXTPREV_TYPE_1)      
 
  
    def __unicode__(self):
        return self.title

class QuestionField(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=500)
    answer = models.BooleanField(verbose_name=_("True/False"), default=False)

    def __unicode__(self):  
        return self.text  


class QuestionM(Orderable):
    """Question."""

    class Meta:
        verbose_name = _("QuestionM")
        verbose_name_plural = _("QuestionMs")
  
    title = models.CharField(_("Title"), blank=False, null=True, max_length=250)
    q_summary = models.TextField(_("Summary"),  blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name="quizm")
    q_type= models.IntegerField(_("Question type"), choices=QUESTION_TYPE_CHOICES, default=QUESTION_TYPE_1)      
    previousq=  models.IntegerField(_("Previous"),default=0)
    nextq=  models.IntegerField(_("Next"),default=0)
    previousq_type= models.IntegerField(_("Question prev type"), choices=QUESTIONNEXTPREV, default=QUESTIONNEXTPREV_TYPE_1)    
    nextq_type= models.IntegerField(_("Question next type"), choices=QUESTIONNEXTPREV, default=QUESTIONNEXTPREV_TYPE_1)      
 
   
  
    def __unicode__(self):
        return self.title
    
class QuestionMultiField(models.Model):
    question = models.ForeignKey(QuestionM)
    text = models.CharField(max_length=500)
  
    def __unicode__(self):  
        return self.text 
class QuestionMultiVal(models.Model):
    question = models.ForeignKey(QuestionMultiField)
    value = models.CharField(max_length=500)
    answer = models.BooleanField(verbose_name=_("True/False"), default=False)

    def __unicode__(self):  
        return self.value 
    
class QuestionResult(Orderable):
    """Lesson."""

    class Meta:
        verbose_name = _("Question Result")
        verbose_name_plural = _("Question Results")
    question = models.ForeignKey(Question)
    quiz = models.ForeignKey(Quiz)
    userquestion = models.ForeignKey(User, related_name="question_user")
    result = models.CharField(_("result"), blank=False, null=True, max_length=250)
    q_latest_date = models.DateTimeField(_("Publication date"), blank=True, null=True, editable=True)
    
  
    def __unicode__(self):
        return self.question
 
                            
                            
                            
class Resource(Orderable):
    """Lesson."""

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
  
    course = models.ForeignKey(Course, related_name="resmod_course")
    module = models.ForeignKey(Module, related_name="reslearn_module")
    title = models.CharField(_("Title"), blank=False, null=True, max_length=250)
    resourcetext = models.TextField(_("Resources Description"),  blank=True, null=True)
    
  
    def __unicode__(self):
        return self.title                                                        
AUTOREGISTER_1 = 1
AUTOREGISTER_2 = 2
AUTOREGISTER_3 = 3
AUTOREGISTER_CHOICES = (
    (AUTOREGISTER_1, _("Pending approval")), 
    (AUTOREGISTER_2, _("Approved")),
    (AUTOREGISTER_3, _("Rejected")),
)

class eLearnAutoRegistration(models.Model):
    firstname = models.CharField(_("First name"), blank=True, null=True,max_length=250,)
    lastname = models.CharField(_("Last name"), blank=True, null=True,max_length=250,)
    email = models.CharField(_("Email"), blank=True, null=True,max_length=250,)
    organisation = models.CharField(_("Organisation"), blank=True, null=True,max_length=250,)
    country = models.CharField(_("Country"), blank=True, null=True,max_length=250,)
    summary =  models.CharField(_("describe why you need access to e-learning courses"), blank=True, null=True,max_length=500,)
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
        super(eLearnAutoRegistration, self).save(*args, **kwargs)
