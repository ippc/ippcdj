
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
from ippc.models import CountryPage



def user_unicode_patch(self):
    return '%s %s' % (self.first_name, self.last_name)



def validate_file_extension(value):
    if not (value.name.endswith('.pdf') or value.name.endswith('.doc')or value.name.endswith('.txt')
        or value.name.endswith('.xls')   or value.name.endswith('.ppt') or value.name.endswith('.jpg')
        or value.name.endswith('.png') or value.name.endswith('.gif') or value.name.endswith('.xlsx')
        or value.name.endswith('.docx')or value.name.endswith('.ppt') or value.name.endswith('.pptx') or value.name.endswith('.zip')
        or value.name.endswith('.rar')):
        raise ValidationError(u'You can only upload files:  txt pdf ppt doc xls jpg png docx xlsx pptx zip rar.')



# used by PceVersion
CURRENT = 1
CLOSED = 2
COMPLETED =3
PCEVERSION_STATUS_CHOICES = (
    (CURRENT, _("current")), 
    (CLOSED, _("closed")),
    (COMPLETED, _("completed")),
)
# used by MODULES status
OPEN = 1
SENT = 3
VALIDATED =4
MODULES_STATUS_CHOICES = (
    (OPEN, _("open")), 
    (SENT, _("sent to validator")),
    (VALIDATED, _("validates")),
)
BOOL_CHOICES_0 = None
BOOL_CHOICES_1 = True
BOOL_CHOICES_2 = False
BOOL_CHOICES = (
    (BOOL_CHOICES_1, _("Yes")),
    (BOOL_CHOICES_2, _("No")),
)
BOOL_CHOICES_M_0 =0
BOOL_CHOICES_M_1 = 1
BOOL_CHOICES_M_2 = 2
BOOL_CHOICESM_M = (
    (BOOL_CHOICES_M_0, _("-- select --")),
    (BOOL_CHOICES_M_1, _("Yes")),
    (BOOL_CHOICES_M_2, _("No")),
)  

class Crops(models.Model):
    """ Crops  """
    crop = models.CharField(_("Crop"), max_length=500)
    def __unicode__(self):
        return self.crop

class PceVersion(Orderable):
    """Single version of the pce for a country."""

    class Meta:
        verbose_name = _("Version")
        verbose_name_plural = _("Versions")
  
    country = models.ForeignKey(CountryPage, related_name="pceversion_country_page")
    author = models.ForeignKey(User, related_name="pceversion_author")
    version_number = models.CharField(_("Session"), blank=True, null=True, max_length=100)
    status = models.IntegerField(_("Status"), choices=PCEVERSION_STATUS_CHOICES, default=CURRENT)
    modify_date = models.DateTimeField(_("Last updated"), blank=True, null=True, editable=False, auto_now=True)
    completed_date = models.DateTimeField(_("Date Completed"), blank=True, null=True, editable=False, auto_now=True)    
    projet_date_completation = models.DateTimeField(_("Projected Date of Completion"),  blank=False, null=True, editable=True)
    name_authority = models.CharField(_("Name of authority requesting implementation of PCE"), blank=False, null=True, max_length=250)
    designation = models.CharField(_("Designation"), blank=False, null=True, max_length=250)
    file_designation = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload scanned copy', upload_to='files/pceversion/%Y/%m/%d/', validators=[validate_file_extension])
    name_pcemanager = models.CharField(_("Name of PCE Manager/ Validator "), blank=False, null=True, max_length=250)
    title_pcemanager = models.CharField(_("PCE Manager/ Validator Work Title   "), blank=False, null=True, max_length=250)
    email_pcemanager = models.CharField(_("PCE Manager/ Validator Email  "), blank=False, null=True, max_length=250)
    is_facilitated = models.BooleanField(verbose_name=_("Is this session being facilitated?  "),choices=BOOL_CHOICES,default=False) 
    firstname_facilitator = models.CharField(_("Facilitator first name"), blank=True, null=True, max_length=250)
    lastname_facilitator = models.CharField(_("Facilitator last name"), blank=True, null=True, max_length=250)
    email_facilitator = models.CharField(_("Facilitator email"), blank=True, null=True, max_length=250)
    chosen_modules = models.CharField(_("Modules"), blank=True, null=True, max_length=250)
    
    ed1_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed1_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed1_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed2_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed2_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed2_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed3_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed3_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed3_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed4_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed4_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed4_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed5_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed5_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed5_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed6_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed6_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed6_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed7_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed7_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed7_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
    
    ed8_firstname=models.CharField(_("First name"), blank=True, null=True, max_length=250)
    ed8_lastname=models.CharField(_("Last name"), blank=True, null=True, max_length=250)
    ed8_email=models.CharField(_("Email"), blank=True, null=True, max_length=250)
  
    def __unicode__(self):
        return self.version_number
 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(PceVersion, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})
            
REGION_0 = 0
REGION_1 = 1
REGION_2 = 2
REGION_3 = 3
REGION_4 = 4
REGION_5 = 5
REGION_6 = 6
REGION_7 = 7
REGIONS = (
    (REGION_0, _("--- Please select ---")),
    (REGION_1, _("Africa")),
    (REGION_2, _("Asia")),
    (REGION_3, _("Europe")),
    (REGION_4, _("Latin America and Caribbean")),
    (REGION_5, _("Near East")),
    (REGION_6, _("North America")),
    (REGION_7, _("South West Pacific")),
)
VAL_IMP_0 = 0
VAL_IMP_1 = 1
VAL_IMP_2 = 2
VAL_IMP_3 = 3
VAL_IMP_4 = 4
VAL_IMP_5 = 5
VAL_IMP_6 = 6
VAL_IMP_7 = 7
VAL_IMP_8 = 8
VAL_IMP_9 = 9
VAL_IMP = (
    (VAL_IMP_0, _("--- Please select ---")),
    (VAL_IMP_1, _("Not known")),
    (VAL_IMP_2, _("0 to $100,000")),
    (VAL_IMP_3, _("$100,000 to $500,000")),
    (VAL_IMP_4, _("$500,000 to $1M")),
    (VAL_IMP_5, _("$1M to $10M")),
    (VAL_IMP_6, _("$10M to $25M")),
    (VAL_IMP_7, _("$25M to $50M")),
    (VAL_IMP_8, _("$50M to $100M")),
    (VAL_IMP_9, _("Greater than $100M ")),
)

VAL_EXP_0 = 0
VAL_EXP_1 = 1
VAL_EXP_2 = 2
VAL_EXP_3 = 3
VAL_EXP_4 = 4
VAL_EXP_5 = 5
VAL_EXP_6 = 6
VAL_EXP_7 = 7
VAL_EXP_8 = 8
VAL_EXP_9 = 9
VAL_EXP = (
     (VAL_EXP_0, _("--- Please select ---")),
     (VAL_EXP_1, _("Unknown")),
    (VAL_EXP_2, _("0 to $100,000")),
    (VAL_EXP_3, _("$100,000 to $500,000")),
    (VAL_EXP_4, _("$500,000 to $1M")),
    (VAL_EXP_5, _("$1M to $10M")),
    (VAL_EXP_6, _("$10M to $50M")),
    (VAL_EXP_7, _("$25M to $50M")),
    (VAL_EXP_8, _("greater than $50M")),
)

VAL_PERCENT_00 = 0
VAL_PERCENT_0 = 1
VAL_PERCENT_1 = 2
VAL_PERCENT_2 = 3
VAL_PERCENT_3 = 4
VAL_PERCENT_4 = 5
VAL_PERCENT_5 = 6
VAL_PERCENT_6 = 7
VAL_PERCENT_7 = 8
VAL_PERCENT_8 = 9
VAL_PERCENT_9 = 10
VAL_PERCENT_10 = 11

VAL_PERCENT = (
    (VAL_PERCENT_00, _("--- Please select ---")),
    (VAL_PERCENT_0, _("0")),
    (VAL_PERCENT_1, _("10")),
    (VAL_PERCENT_2, _("20")),
    (VAL_PERCENT_3, _("30")),
    (VAL_PERCENT_4, _("40")),
    (VAL_PERCENT_5, _("50")),
    (VAL_PERCENT_6, _("60")),
    (VAL_PERCENT_7, _("70")),
    (VAL_PERCENT_8, _("80")),
    (VAL_PERCENT_9, _("90")),
    (VAL_PERCENT_10, _("100")),
)

NUMPLANT_0=0
NUMPLANT_1=1
NUMPLANT_2=2
NUMPLANT_3=3
NUMPLANT_4=4
NUMPLANT_5=5
NUMPLANT_6=6
NUMPLANT_7=7
NUMPLANT_8=8
NUMPLANT_9=9
NUMPLANT = (
    (NUMPLANT_0, _("--- Please select ---")),
    (NUMPLANT_1, _("0")),
    (NUMPLANT_2, _("1")),
    (NUMPLANT_3, _("2")),
    (NUMPLANT_4, _("3")),
    (NUMPLANT_5, _("4")),
    (NUMPLANT_6, _("5")),
    (NUMPLANT_7, _("10 +")),
    (NUMPLANT_8, _("20 +")),
    (NUMPLANT_9, _("50 +")),
)
NUM_BILATERAL_0=0
NUM_BILATERAL_1=1
NUM_BILATERAL_2=2
NUM_BILATERAL_3=3
NUM_BILATERAL_4=4
NUM_BILATERAL = (
    (NUM_BILATERAL_0, _("--- Please select ---")),
    (NUM_BILATERAL_1, _("1-3")),
    (NUM_BILATERAL_2, _("4-6")),
    (NUM_BILATERAL_3, _("7-10")),
    (NUM_BILATERAL_4, _("greater than 10")),
)
ROLE_0=0
ROLE_1=1
ROLE_2=2
ROLE_3=3
ROLE_4=4
ROLE = (
    (ROLE_0, _("--- Please select ---")),
    (ROLE_1, _("Group leader")),
    (ROLE_2, _("Client")),
    (ROLE_3, _("Oversight")),
    (ROLE_4, _("Advocate")),
)
INTEREST_0=0
INTEREST_1=1
INTEREST_2=2
INTEREST = (
    (INTEREST_0, _("--- Please select ---")),
    (INTEREST_1, _("Low")),
    (INTEREST_2, _("High")),
 
)            


IMPORTANCE_0=0
IMPORTANCE_1=1
IMPORTANCE_2=2
IMPORTANCE_3=3
IMPORTANCE_4=4
IMPORTANCE_5=5
IMPORTANCE = (
    (IMPORTANCE_0, _("--- Please select ---")),
    (IMPORTANCE_1, _("0")),
    (IMPORTANCE_2, _("1")),
    (IMPORTANCE_3, _("2")),
    (IMPORTANCE_4, _("3")),
    (IMPORTANCE_5, _("4")),
)   
PARTICIPANT_0=0
PARTICIPANT_1=1
PARTICIPANT_2=2
PARTICIPANT_3=3
PARTICIPANT_4=4
PARTICIPANT_5=5
PARTICIPANT = (
    (PARTICIPANT_0, _("--- Please select ---")),
    (PARTICIPANT_1, _("0")),
    (PARTICIPANT_2, _("1")),
    (PARTICIPANT_3, _("2")),
    (PARTICIPANT_4, _("3")),
    (PARTICIPANT_5, _("4")),
) 
LEVEL_0=0
LEVEL_1=1
LEVEL_2=2
LEVEL_3=3
LEVEL_4=4
LEVEL = (
    (LEVEL_0, _("--- Please select ---")),
    (LEVEL_1, _("WORKSHOP PARTICIPANT")),
    (LEVEL_2, _("SURVEY PARTICIPANT")),
    (LEVEL_3, _("FOCUS GROUP MEMBER")),
    (LEVEL_4, _("KEEP INFORMED")),
)        
PRIORITY_0 =0
PRIORITY_1 = 1
PRIORITY_2 = 2
PRIORITY_3 = 3
PRIORITY_4 = 4
PRIORITY_5 = 5
PRIORITY = (
    (PRIORITY_0, _("--- Please select ---")),
    (PRIORITY_1, _("Very Low")),
    (PRIORITY_2, _("Low")),
    (PRIORITY_3, _("Medium")),
    (PRIORITY_4, _("High")),
    (PRIORITY_5, _("Very high")),
)
TYPE_0=0
TYPE_1=1
TYPE_2=2
TYPE_3=3
TYPE = (
    (TYPE_0, _("--- Please select ---")),
    (TYPE_1, _("A) National coordination and political willigness")),
    (TYPE_2, _("B) Like A plus small technical assisstance")),
    (TYPE_3, _("C) Like A plus significant investments")),
)        

STABLE_0=0
STABLE_1=1
STABLE_2=2
STABLE_3=3
STABLE_4=4
STABLE_5=5
STABLE = (
    (STABLE_0, _("--- Please select ---")),
    (STABLE_1, _("Very unstable")),
    (STABLE_2, _("Unstable")),
    (STABLE_3, _("Slightly Stable")),
    (STABLE_4, _("Stable")),
    (STABLE_5, _("Very Stable")),
) 

CONDITIONS_0=0
CONDITIONS_1=1
CONDITIONS_2=2
CONDITIONS_3=3
CONDITIONS_4=4
CONDITIONS_5=5
CONDITIONS = (
    (CONDITIONS_0, _("--- Please select ---")),
    (CONDITIONS_1, _("Not at all (poor conditions and salaries)")),
    (CONDITIONS_2, _("Somewhat adequate (conditions fine but not salaries)")),
    (CONDITIONS_3, _("Almost (salaries fine but not conditions)")),
    (CONDITIONS_4, _("Adequate (reasonable salaries and conditions acceptable to the standard of living)")),
    (CONDITIONS_5, _("Totally (salaries and conditions are competitive)")),
) 
RATE_0=0
RATE_1=1
RATE_2=2
RATE_3=3
RATE_4=4
RATE_5=5
RATE = (
    (RATE_0, _("--- Please select ---")),
    (RATE_1, _("None")),
    (RATE_2, _("Insufficient")),
    (RATE_3, _("Moderate")),
    (RATE_4, _("Good")),
    (RATE_5, _("Excellent")),
) 
RATE1_0=0
RATE1_1=1
RATE1_2=2
RATE1_3=3
RATE1_4=4
RATE1_5=5
RATE1 = (
    (RATE1_0, _("--- Please select ---")),
    (RATE1_1, _("Capacity None existent")),
    (RATE1_2, _("Insufficient")),
    (RATE1_3, _("Moderate")),
    (RATE1_4, _("Good")),
    (RATE1_5, _("Excellent")),
)
SUPPORT_0=0
SUPPORT_1=1
SUPPORT_2=2
SUPPORT_3=3
SUPPORT_4=4
SUPPORT_5=5
SUPPORT = (
    (SUPPORT_0, _("--- Please select ---")),
    (SUPPORT_1, _("Not at all")),
    (SUPPORT_2, _("Minimal support")),
    (SUPPORT_3, _("Supportive")),
    (SUPPORT_4, _("Moderately supportive")),
    (SUPPORT_5, _("Very supportive")),
) 

PARTIAL_0=0
PARTIAL_1=1
PARTIAL_2=2
PARTIAL_3=3
PARTIAL_4=4
PARTIAL_5=5
PARTIAL = (
    (PARTIAL_0, _("--- Please select ---")),
    (PARTIAL_1, _("Not at all")),
    (PARTIAL_2, _("Partially")),
    (PARTIAL_3, _("Selectively")),
    (PARTIAL_4, _("Mostly")),
    (PARTIAL_5, _("All")),
) 
RATHER_0=0
RATHER_1=1
RATHER_2=2
RATHER_3=3
RATHER_4=4
RATHER_5=5
RATHER = (
    (RATHER_0, _("--- Please select ---")),
    (RATHER_1, _("Not at all")),
    (RATHER_2, _("Rather low")),
    (RATHER_3, _("Intermediate")),
    (RATHER_4, _("Much")),
    (RATHER_5, _("Very much so")),
) 

SERVICE_0=0
SERVICE_1=1
SERVICE_2=2
SERVICE_3=3
SERVICE_4=4
SERVICE_5=5
SERVICE = (
    (SERVICE_0, _("--- Please select ---")),
    (SERVICE_1, _("None existent")),
    (SERVICE_2, _("Formative stages")),
    (SERVICE_3, _("Limited to a specific sub-area")),
    (SERVICE_4, _("Developed but targeted")),
    (SERVICE_5, _("Well developed and broad")),
) 

STATEMENT_0=0
STATEMENT_1=1
STATEMENT_2=2
STATEMENT_3=3
STATEMENT_4=4
STATEMENT_5=5
STATEMENT = (
    (STATEMENT_0, _("--- Please select ---")),
    (STATEMENT_1, _("No statement exists")),
	(STATEMENT_2,_("Under consideration")),
	(STATEMENT_3,_("In a draft document")),
	(STATEMENT_4,_("In an internal strategic plan")),
	(STATEMENT_5,_("In a published strategic plan ")),
)



MODERATE_0=0
MODERATE_1=1
MODERATE_2=2
MODERATE_3=3
MODERATE_4=4
MODERATE_5=5
MODERATE = (
    (MODERATE_0, _("--- Please select ---")),
	(MODERATE_1,_("Not at all")),
	(MODERATE_2,_("Slightly")),
	(MODERATE_3,_("Moderately")),
	(MODERATE_4,_("Very much")),
	(MODERATE_5,_("Completely")),
)

HQ_0=0
HQ_1=1
HQ_2=2
HQ_3=3
HQ_4=4
HQ_5=5
HQ = (
	(HQ_0, _("--- Please select ---")),
	(HQ_1,_("Not at all")),
	(HQ_2,_("Very few")),
	(HQ_3,_("Only staff at HQ")),
	(HQ_4,_("HQ and some in the field")),
	(HQ_5,_("Yes, all staff")),
)

WRITTEN_0=0
WRITTEN_1=1
WRITTEN_2=2
WRITTEN_3=3
WRITTEN = (
(WRITTEN_0, _("--- Please select ---")),
(WRITTEN_1,_("Not at all")),
(WRITTEN_2,_("Yes, informal")),
(WRITTEN_3,_("Yes, written")),
)


INPUTSTAKE_0=0
INPUTSTAKE_1=1
INPUTSTAKE_2=2
INPUTSTAKE_3=3
INPUTSTAKE = (
	(INPUTSTAKE_0, _("--- Please select ---")),
	(INPUTSTAKE_1,_("No input by stakeholders")),
	(INPUTSTAKE_2,_("Stakeholders comment on plans submitted by NPPO after they are developed")),
	(INPUTSTAKE_3,_("Stakeholders actively involved in the planning process")),
)
TERM_0=0
TERM_1=1
TERM_2=2
TERM_3=3
TERM_4=4
TERM_5=5
TERM = (
	(TERM_0, _("--- Please select ---")),
	(TERM_1,_("Never")),
	(TERM_2,_("Rarely")),
	(TERM_3,_("Sometimes, no fixed term ")),
	(TERM_4,_("Accordingly with an established term ")),
	(TERM_5,_("Annually")),
)

THEM_0=0
THEM_1=1
THEM_2=2
THEM_3=3
THEM_4=4
THEM_5=5
THEM = (
	(THEM_0, _("--- Please select ---")),
	(THEM_1,_("None at all")),
	(THEM_2,_("A few of them")),
	(THEM_3,_("Some of them")),
	(THEM_4,_("Most of them")),
	(THEM_5,_("All of them")),
)
THEM1_0=0
THEM1_1=1
THEM1_2=2
THEM1_3=3
THEM1_4=4
THEM1 = (
	(THEM1_0, _("--- Please select ---")),
	(THEM1_1,_("None of them")),
	(THEM1_2,_("One of them")),
	(THEM1_3,_("Two of them")),
	(THEM1_4,_("All of them")),
)
DEGREE_0=0
DEGREE_1=1
DEGREE_2=2
DEGREE_3=3
DEGREE_4=4
DEGREE_5=5
DEGREE = (
(DEGREE_0, _("--- Please select ---")),
(DEGREE_1,_("Not at all")),
(DEGREE_2,_("To a small degree")),
(DEGREE_3,_("To a medium degree")),
(DEGREE_4,_("To a large degree")),
(DEGREE_5,_("Completely")),
) 

ACHIEVE_0=0
ACHIEVE_1=1
ACHIEVE_2=2
ACHIEVE_3=3
ACHIEVE_4=4
ACHIEVE = (
    (ACHIEVE_0, _("--- Please select ---")),
    (ACHIEVE_1,_("Very difficult")),
    (ACHIEVE_2,_("Somewhat difficult")),
    (ACHIEVE_3,_("Easy")),
    (ACHIEVE_4,_("Very easy")),
)
CARRY_AC_0=0
CARRY_AC_1=1
CARRY_AC_2=2
CARRY_AC_3=3
CARRY_AC_4=4
CARRY_AC_5=5
CARRY_AC = (
	(CARRY_AC_0, _("--- Please select ---")),
	(CARRY_AC_1,_("None at all")),
	(CARRY_AC_2,_("Lacking in many areas")),
	(CARRY_AC_3,_("Partially")),
	(CARRY_AC_4,_("Mostly")),
	(CARRY_AC_5,_("Completely")),
)

DEFINED_0=0
DEFINED_1=1
DEFINED_2=2
DEFINED_3=3
DEFINED_4=4
DEFINED_5=5
DEFINED = (
	(DEFINED_0, _("--- Please select ---")),
	(DEFINED_1,_("No roles definition")),
	(DEFINED_2,_("Poorly defined")),
	(DEFINED_3,_("Defined satisfactorily")),
	(DEFINED_4,_("Well defined")),
	(DEFINED_5,_("Well defined and flexible")),
)
CLEAR_0=0
CLEAR_1=1
CLEAR_2=2
CLEAR_3=3
CLEAR_4=4
CLEAR_5=5
CLEAR = (
	(CLEAR_0, _("--- Please select ---")),
	(CLEAR_1,_("Not at all")),
	(CLEAR_2,_("Unsatisfactory")),
	(CLEAR_3,_("With difficulty")),
	(CLEAR_4,_("Satisfactory")),
	(CLEAR_5,_("Very clear and at all levels")),
)

EXPEDI_0=0
EXPEDI_1=1
EXPEDI_2=2
EXPEDI_3=3
EXPEDI_4=4
EXPEDI_5=5
EXPEDI = (
	(EXPEDI_0, _("--- Please select ---")),
	(EXPEDI_1,_("Not at all")),
	(EXPEDI_2,_("Poorly")),
	(EXPEDI_3,_("Satisfactorily")),
	(EXPEDI_4,_("Good")),
	(EXPEDI_5,_("Fully")),
)

LINKAGE_0=0
LINKAGE_1=1
LINKAGE_2=2
LINKAGE_3=3
LINKAGE_4=4
LINKAGE_5=5
LINKAGE = (
	(LINKAGE_0, _("--- Please select ---")),
	(LINKAGE_1,_("Not at all")),
	(LINKAGE_2,_("Unsatisfactory")),
	(LINKAGE_3,_("With difficulty")),
	(LINKAGE_4,_("Satisfactory")),
	(LINKAGE_5,_("Easily")),
)
POLICY_0=0
POLICY_1=1
POLICY_2=2
POLICY_3=3
POLICY_4=4
POLICY = (
	(POLICY_0, _("--- Please select ---")),
	(POLICY_1,_("Not at all")),
	(POLICY_2,_("Somewhat")),
	(POLICY_3,_("Substantive")),
	(POLICY_4,_("Totally")),
)




BUDGET_0 = 0
BUDGET_1 = 1
BUDGET_2 = 2
BUDGET_3 = 3
BUDGET_4 = 4
BUDGET_5 = 5
BUDGET = (

(BUDGET_0, _("--- Please select ---")),
(BUDGET_1, _("less than 10 % of the NPPO budget")),
(BUDGET_2, _("between 11 - 20 %")),
(BUDGET_3, _("between 21 - 40 %")),
(BUDGET_4, _("between 41 - 50 %")),
(BUDGET_5, _("More than 51 %")),
)

FUNDING_0 = 0
FUNDING_1 = 1
FUNDING_2 = 2
FUNDING_3 = 3
FUNDING = (
(FUNDING_0, _("--- Please select ---")),
(FUNDING_1, _("Depends on Ministerial allocation ")),
(FUNDING_2, _("Specific line in the national budget ")),
(FUNDING_3, _("Specific line in the national budget plus fees and fines")),
)

ACQUIRE_0 = 0
ACQUIRE_1 = 1
ACQUIRE_2 = 2
ACQUIRE_3 = 3
ACQUIRE_4 = 4
ACQUIRE_5 = 5
ACQUIRE = (
(ACQUIRE_0, _("--- Please select ---")),
(ACQUIRE_1, _("no effort")),
(ACQUIRE_2, _("International Grants")),
(ACQUIRE_3, _("International Grants and National Resources")),
(ACQUIRE_4, _("International Loans")),
(ACQUIRE_5, _("National Resources")),
)

ADEQUATELY_0 = 0
ADEQUATELY_1 = 1
ADEQUATELY_2 = 2
ADEQUATELY_3 = 3
ADEQUATELY_4 = 4
ADEQUATELY = (
(ADEQUATELY_0, _("--- Please select ---")),
(ADEQUATELY_1, _("Not at all")),
(ADEQUATELY_2, _("marginally")),
(ADEQUATELY_3, _("sufficiently")),
(ADEQUATELY_4, _("well staff")),
)

APPOINTED_0 = 0
APPOINTED_1 = 1
APPOINTED_2 = 2
APPOINTED_3 = 3
APPOINTED_4 = 4
APPOINTED_5 = 5

APPOINTED = (
(APPOINTED_0, _("--- Please select ---")),
(APPOINTED_1, _("All the staff appointed are not competitively sourced")),
(APPOINTED_2, _("The Head and managers are not competitively sourced ")),
(APPOINTED_3, _("Only the Head is appointed without being competitively sourced")),
(APPOINTED_4, _("All management positions are competitively sourced and appointed")),
(APPOINTED_5, _("All the positions in the NPPO are competitively sourced and appointed")),
)

TURNOVER_0 = 0
TURNOVER_1 = 1
TURNOVER_2 = 2
TURNOVER_3 = 3
TURNOVER_4 = 4
TURNOVER_5 = 5
TURNOVER_6 = 6
TURNOVER_7 = 7
TURNOVER = (
(TURNOVER_0, _("--- Please select ---")),
(TURNOVER_1, _("very low")),
(TURNOVER_2, _("low")),
(TURNOVER_3, _("intermediate")),
(TURNOVER_4, _("high")),
(TURNOVER_5, _("very high")),
)
TRAINING_0 = 0
TRAINING_1 = 1
TRAINING_2 = 2
TRAINING_3 = 3
TRAINING_4 = 4
TRAINING_5 = 5
TRAINING = (
(TRAINING_0, _("--- Please select ---")),
(TRAINING_1, _("Not at all")),
(TRAINING_2, _("Training is done only when there are external project resources to do so")),
(TRAINING_3, _("Training is done adhoc/when needed")),
(TRAINING_4, _("Limited or targeted training is done")),
(TRAINING_5, _("In all areas")),
)

PROPORTION_0 = 0
PROPORTION_1 = 1
PROPORTION_2 = 2
PROPORTION_3 = 3
PROPORTION_4 = 4
PROPORTION_5 = 5

PROPORTION = (
(PROPORTION_0, _("--- Please select ---")),
(PROPORTION_1, _("Less than 10 %")),
(PROPORTION_2, _("10 - 25 %")),
(PROPORTION_3, _("26 - 50 %")),
(PROPORTION_4, _("51 - 75 %")),
(PROPORTION_5, _("More than 75%")),
)
COMM_SKILLS_0 = 0
COMM_SKILLS_1 = 1
COMM_SKILLS_2 = 2
COMM_SKILLS_3 = 3
COMM_SKILLS_4 = 4
COMM_SKILLS_5 = 5
COMM_SKILLS  = (
(COMM_SKILLS_0, _("--- Please select ---")),
(COMM_SKILLS_1, _("very poor ")),
(COMM_SKILLS_2, _("poor")),
(COMM_SKILLS_3, _("average")),
(COMM_SKILLS_4, _("good")),
(COMM_SKILLS_5, _("very good")),
)
POOR_0 = 0
POOR_1 = 1
POOR_2 = 2
POOR_3 = 3
POOR_4 = 4
POOR_5 = 5
POOR  = (
(POOR_0, _("--- Please select ---")),
(POOR_1, _("very poor ")),
(POOR_2, _("poor")),
(POOR_3, _("adequate")),
(POOR_4, _("good")),
(POOR_5, _("very good")),
)

LANG_SKILLS_0 = 0
LANG_SKILLS_1 = 1
LANG_SKILLS_2 = 2
LANG_SKILLS_3 = 3
LANG_SKILLS_4 = 4
LANG_SKILLS_5 = 5

LANG_SKILLS = (
(LANG_SKILLS_0, _("--- Please select ---")),
(LANG_SKILLS_1, _("very poor")),
(LANG_SKILLS_2, _("basic")),
(LANG_SKILLS_3, _("average")),
(LANG_SKILLS_4, _("good")),
(LANG_SKILLS_5, _("advanced")),
)
RESOURCES_0 = 0
RESOURCES_1 = 1
RESOURCES_2 = 2
RESOURCES_3 = 3
RESOURCES_4 = 4
RESOURCES_5 = 5

RESOURCES = (
(RESOURCES_0, _("--- Please select ---")),
(RESOURCES_1, _("Not at all")),
(RESOURCES_2, _("unsatisfactory resource allocation")),
(RESOURCES_3, _("insufficient resource allocation")),
(RESOURCES_4, _("adequate resource allocation")),
(RESOURCES_5, _("More than adequatate")),
)
RECORD_0 = 0
RECORD_1 = 1
RECORD_2 = 2
RECORD_3 = 3
RECORD_4 = 4
RECORD_5 = 5

RECORD = (
(RECORD_0, _("--- Please select ---")),
(RECORD_1, _("No record keeping system")),
(RECORD_2, _("unsatisfactory system (incongruous)")),
(RECORD_3, _("satisfactory system (mostly hardcopy based)")),
(RECORD_4, _("very good system (combination electronic and hardcopy)")),
(RECORD_5, _("Computerized record keeping, central dbase, on line system")),
)
CAPACITY_0 = 0
CAPACITY_1 = 1
CAPACITY_2 = 2
CAPACITY_3 = 3
CAPACITY_4 = 4
CAPACITY_5 = 5

CAPACITY = (
(CAPACITY_0, _("--- Please select ---")),
(CAPACITY_1, _("very low")),
(CAPACITY_2, _("low")),
(CAPACITY_3, _("intermediate")),
(CAPACITY_4, _("high")),
(CAPACITY_5, _("very high")),
)

ACCESS_0 = 0
ACCESS_1 = 1
ACCESS_2 = 2
ACCESS_3 = 3
ACCESS_4 = 4
ACCESS_5 = 5

ACCESS = (
(ACCESS_0, _("--- Please select ---")),
(ACCESS_1, _("No access at all")),
(ACCESS_2, _("Only when external resources are available (e.g. projects)")),
(ACCESS_3, _("Limited access to paper based and internet resources")),
(ACCESS_4, _("Good access to paper based and internet sources of information")),
(ACCESS_4, _("Excellent, no limitations")),
)

BAD_0 = 0
BAD_1 = 1
BAD_2 = 2
BAD_3 = 3
BAD_4 = 4
BAD_5 = 5

BAD = (
(BAD_0, _("--- Please select ---")),
(BAD_1, _("Very bad")),
(BAD_2, _("Bad")),
(BAD_3, _("Not so bad")),
(BAD_4, _("Good")),
(BAD_5, _("Very good")),
)
BAD1_0 = 0
BAD1_1 = 1
BAD1_2 = 2
BAD1_3 = 3
BAD1_4 = 4
BAD1_5 = 5

BAD1 = (
(BAD1_0, _("--- Please select ---")),
(BAD1_1, _("Very bad")),
(BAD1_2, _("Bad")),
(BAD1_3, _("Satisfactory")),
(BAD1_4, _("Adequate")),
(BAD1_5, _("Very good")),
)

BAD2_0 = 0
BAD2_1 = 1
BAD2_2 = 2
BAD2_3 = 3
BAD2_4 = 4
BAD2_5 = 5
BAD2 = (
(BAD2_0, _("--- Please select ---")),
(BAD2_1, _("Very badly")),
(BAD2_2, _("Badly")),
(BAD2_3, _("Intermediate")),
(BAD2_4, _("Well")),
(BAD2_5, _("Very well")),
)

VAL_0 = 0
VAL_1 = 1
VAL_2 = 2
VAL_3 = 3
VAL_4 = 4
VAL_5 = 5
VAL_6 = 6

VAL = (
    (VAL_0, _("--- Please select ---")),
    (VAL_1, _("0")),
    (VAL_2, _("1")),
    (VAL_3, _("2")),
    (VAL_4, _("3")),
    (VAL_5, _("4")),
    (VAL_6, _("5")),
)
VAL_AV_0 = 0
VAL_AV_1 = 1
VAL_AV_2 = 2
VAL_AV_3 = 3
VAL_AV_4 = 4
VAL_AV = (
    (VAL_AV_0, _("--- Please select ---")),
    (VAL_AV_1, _("0-5")),
    (VAL_AV_2, _("5-10")),
    (VAL_AV_3, _("10-20")),
    (VAL_AV_4, _(">20")),
) 

DEFINITIONS_0 = 0
DEFINITIONS_1 = 1
DEFINITIONS_2 = 2
DEFINITIONS_3 = 3
DEFINITIONS_4 = 4
DEFINITIONS_5 = 5
DEFINITIONS = (
    (DEFINITIONS_0, _("--- Please select ---")),
    (DEFINITIONS_1, _("Not at all")),
    (DEFINITIONS_2, _("Major improvements required")),
    (DEFINITIONS_3, _("Mostly")),
    (DEFINITIONS_4, _("Minor modifications needed")),
    (DEFINITIONS_5, _("Totally")),
) 
DEFINITIONS1_0 = 0
DEFINITIONS1_1 = 1
DEFINITIONS1_2 = 2
DEFINITIONS1_3 = 3
DEFINITIONS1_4 = 4
DEFINITIONS1_5 = 5
DEFINITIONS1 = (
    (DEFINITIONS1_0, _("--- Please select ---")),
    (DEFINITIONS1_1, _("Not at all")),
    (DEFINITIONS1_2, _("Major improvements required")),
    (DEFINITIONS1_3, _("Mostly")),
    (DEFINITIONS1_4, _("Minor improvements needed")),
    (DEFINITIONS1_5, _("Totally")),
) 
ACT_0 = 0
ACT_1 = 1
ACT_2 = 2
ACT_3 = 3
ACT_4 = 4
ACT_5 = 5
ACT = (
    (ACT_0, _("--- Please select ---")),
    (ACT_1, _("Not updated")),
    (ACT_2, _("Under revision")),
    (ACT_3, _("For Cabinet consideration")),
    (ACT_4, _("For consideration at Parliament")),
    (ACT_5, _("Updated to IPPC 1997")),
)
CIVIL_0 = 0
CIVIL_1 = 1
CIVIL_2 = 2
CIVIL_3 = 3
CIVIL_4 = 4

CIVIL = (
    (CIVIL_0, _("--- Please select ---")),
    (CIVIL_1, _("Civil law system")),
    (CIVIL_2, _("Common law system")),
    (CIVIL_3, _("Religious law")),
    (CIVIL_4, _("Pluralistic system")),
) 
YEAR_0 = 0
YEAR_1 = 1
YEAR_2 = 2
YEAR_3 = 3
YEAR_4 = 4
YEAR_5 = 5
YEAR_6 = 6
YEAR_7 = 7
YEAR_8 = 8
YEAR_9 = 9
YEAR_10 = 10
YEAR_11 = 11
YEAR_12 = 12
YEAR_13 = 13
YEAR_14 = 14
YEAR_15 = 15
YEAR_16 = 16
YEAR_17 = 17
YEAR_18 = 18
YEAR_19 = 19
YEAR_20 = 20
YEAR_21 = 21
YEAR_22 = 22
YEAR_23 = 23
YEAR_24 = 24
YEAR_25 = 25
YEAR_26 = 26
YEAR_27 = 27
YEAR_28 = 28
YEAR_29 = 29
YEAR_30 = 30
YEAR_31 = 31
YEAR_32 = 32
YEAR_33 = 33
YEAR_34 = 34
YEAR_35 = 35
YEAR_36 = 36
YEAR_37 = 37
YEAR_38 = 38
YEAR_39 = 39
YEAR_40 = 40
YEAR_41 = 41
YEAR_42 = 42
YEAR_43 = 43
YEAR_44 = 44
YEAR_45 = 45
YEAR_46 = 46
YEAR_47 = 47
YEAR_48 = 48
YEAR_49 = 49
YEAR_50 = 50
YEAR_51 = 51
YEAR_52 = 52
YEAR_53 = 53
YEAR_54 = 54
YEAR_55 = 55
YEAR_56 = 56
YEAR_57 = 57
YEAR_58 = 58
YEAR_59 = 59
YEAR_60 = 60
YEAR_61 = 61
YEAR_62 = 62
YEAR_63 = 63
YEAR_64 = 64
YEAR_65 = 65
YEAR_66 = 66
YEAR_67 = 67
YEAR_68 = 68
YEAR_69 = 69
YEAR_70 = 70
YEAR_71 = 71
YEAR_72 = 72
YEAR_73 = 73
YEAR_74 = 74
YEAR_75 = 75
YEAR_76 = 76
YEAR_77 = 77
YEAR_78 = 78
YEAR_79 = 79
YEAR_80 = 80
YEAR_81 = 81
YEAR_82 = 82
YEAR_83 = 83
YEAR_84 = 84
YEAR_85 = 85
YEAR_86 = 86
YEAR_87 = 87
YEAR_88 = 88
YEAR_89 = 89
YEAR_90 = 90
YEAR_91 = 91
YEAR_92 = 92
YEAR_93 = 93
YEAR_94 = 94
YEAR_95 = 95
YEAR_96 = 96
YEAR_97 = 97
YEAR_98 = 98
YEAR_99 = 99
YEAR_100 = 100
YEAR_101 = 101
YEAR_102 = 102
YEAR_103 = 103
YEAR_104 = 104
YEAR_105 = 105
YEAR_106 = 106
YEAR_107 = 107
YEAR_108 = 108
YEAR_109 = 109
YEAR_110 = 110
YEAR_111 = 111
YEAR_112 = 112
YEAR_113 = 113
YEAR_114 = 114
YEAR_115 = 115
YEAR = (
(YEAR_0, _("--Please Select--")),
(YEAR_1, _("1901")),
(YEAR_2, _("1902")),
(YEAR_3, _("1903")),
(YEAR_4, _("1904")),
(YEAR_5, _("1905")),
(YEAR_6, _("1906")),
(YEAR_7, _("1907")),
(YEAR_8, _("1908")),
(YEAR_9, _("1909")),
(YEAR_10, _("1910")),
(YEAR_11, _("1911")),
(YEAR_12, _("1912")),
(YEAR_13, _("1913")),
(YEAR_14, _("1914")),
(YEAR_15, _("1915")),
(YEAR_16, _("1916")),
(YEAR_17, _("1917")),
(YEAR_18, _("1918")),
(YEAR_19, _("1919")),
(YEAR_20, _("1920")),
(YEAR_21, _("1921")),
(YEAR_22, _("1922")),
(YEAR_23, _("1923")),
(YEAR_24, _("1924")),
(YEAR_25, _("1925")),
(YEAR_26, _("1926")),
(YEAR_27, _("1927")),
(YEAR_28, _("1928")),
(YEAR_29, _("1929")),
(YEAR_30, _("1930")),
(YEAR_31, _("1931")),
(YEAR_32, _("1932")),
(YEAR_33, _("1933")),
(YEAR_34, _("1934")),
(YEAR_35, _("1935")),
(YEAR_36, _("1936")),
(YEAR_37, _("1937")),
(YEAR_38, _("1938")),
(YEAR_39, _("1939")),
(YEAR_40, _("1940")),
(YEAR_41, _("1941")),
(YEAR_42, _("1942")),
(YEAR_43, _("1943")),
(YEAR_44, _("1944")),
(YEAR_45, _("1945")),
(YEAR_46, _("1946")),
(YEAR_47, _("1947")),
(YEAR_48, _("1948")),
(YEAR_49, _("1949")),
(YEAR_50, _("1950")),
(YEAR_51, _("1951")),
(YEAR_52, _("1952")),
(YEAR_53, _("1953")),
(YEAR_54, _("1954")),
(YEAR_55, _("1955")),
(YEAR_56, _("1956")),
(YEAR_57, _("1957")),
(YEAR_58, _("1958")),
(YEAR_59, _("1959")),
(YEAR_60, _("1960")),
(YEAR_61, _("1961")),
(YEAR_62, _("1962")),
(YEAR_63, _("1963")),
(YEAR_64, _("1964")),
(YEAR_65, _("1965")),
(YEAR_66, _("1966")),
(YEAR_67, _("1967")),
(YEAR_68, _("1968")),
(YEAR_69, _("1969")),
(YEAR_70, _("1970")),
(YEAR_71, _("1971")),
(YEAR_72, _("1972")),
(YEAR_73, _("1973")),
(YEAR_74, _("1974")),
(YEAR_75, _("1975")),
(YEAR_76, _("1976")),
(YEAR_77, _("1977")),
(YEAR_78, _("1978")),
(YEAR_79, _("1979")),
(YEAR_80, _("1980")),
(YEAR_81, _("1981")),
(YEAR_82, _("1982")),
(YEAR_83, _("1983")),
(YEAR_84, _("1984")),
(YEAR_85, _("1985")),
(YEAR_86, _("1986")),
(YEAR_87, _("1987")),
(YEAR_88, _("1988")),
(YEAR_89, _("1989")),
(YEAR_90, _("1990")),
(YEAR_91, _("1991")),
(YEAR_92, _("1992")),
(YEAR_93, _("1993")),
(YEAR_94, _("1994")),
(YEAR_95, _("1995")),
(YEAR_96, _("1996")),
(YEAR_97, _("1997")),
(YEAR_98, _("1998")),
(YEAR_99, _("1999")),
(YEAR_100, _("2000")),
(YEAR_101, _("2001")),
(YEAR_102, _("2002")),
(YEAR_103, _("2003")),
(YEAR_104, _("2004")),
(YEAR_105, _("2005")),
(YEAR_106, _("2006")),
(YEAR_107, _("2007")),
(YEAR_108, _("2008")),
(YEAR_109, _("2009")),
(YEAR_110, _("2010")),
(YEAR_111, _("2011")),
(YEAR_112, _("2012")),
(YEAR_113, _("2013")),
(YEAR_114, _("2014")),
(YEAR_115, _("2015")),
)


GEO_0=0
GEO_1=1
GEO_2=2
GEO_3=3
GEO_4=4
GEO_5=5
GEO =(
(GEO_0, _("--- Please select ---")),
(GEO_1, _("Not at all")),
(GEO_2, _("Poor geographic coverage of services")),
(GEO_3, _("Most areas not serviced adequately")),
(GEO_4, _("Most areas adequately serviced")),
(GEO_5, _("Totally")),
)


SUFFICIENT_0=0
SUFFICIENT_1=1
SUFFICIENT_2=2
SUFFICIENT_3=3
SUFFICIENT_4=4
SUFFICIENT_5=5
SUFFICIENT=(
(SUFFICIENT_0, _("--- Please select ---")),
(SUFFICIENT_1, _("Not at all sufficient")),
(SUFFICIENT_2, _("Lacking a lot")),
(SUFFICIENT_3, _("Neither insufficient or sufficient")),
(SUFFICIENT_4, _("Needs to be improved")),
(SUFFICIENT_5, _("Very sufficient")),

)
OUT_0=0
OUT_1=1
OUT_2=2
OUT_3=3
OUT=(
(OUT_0, _("--- Please select ---")),
(OUT_1,_("all outsourced")),
(OUT_2,_("Partially outsourced")),
(OUT_3,_("All done in house")),
)



LIM_0=0
LIM_1=1
LIM_2=2
LIM_3=3
LIM_4=4
LIM_5=5
LIM=(
(LIM_0, _("--- Please select ---")),
(LIM_1,_("Not at all")),
(LIM_2,_("Severe limitations")),
(LIM_3,_("Limited")),
(LIM_4,_("Few limitations")),
(LIM_5,_("Completely sufficient")),
)

LIM1_0=0
LIM1_1=1
LIM1_2=2
LIM1_3=3
LIM1_4=4
LIM1_5=5
LIM1=(
(LIM1_0, _("--- Please select ---")),
(LIM1_1,_("Totally insufficient")),
(LIM1_2,_("Insufficient")),
(LIM1_3,_("With strong limitations")),
(LIM1_4,_("With some limitations")),
(LIM1_5,_("Without limitations")),
)

WELL_0=0
WELL_1=1
WELL_2=2
WELL_3=3
WELL_4=4
WELL_5=5
WELL=(
(WELL_0, _("--- Please select ---")),
(LIM_1,_("Very badly")),
(LIM_2,_("Badly")),
(LIM_3,_("Intermediate")),
(LIM_4,_("Well")),
(LIM_5,_("Very well")),
)
#SATIST_0=0
#SATIST_1=1
#SATIST_2=2
#SATIST_3=3
#SATIST_4=4
#SATIST_5=5
#SATIST=(
#(SATIST_0, _("--- Please select ---")),
#(SATIST_1, _("Very bad ")),
#(SATIST_2, _("Bad")),
#(SATIST_3, _("Satisfactory")),
#(SATIST_4, _("Adequate")),
#(SATIST_5, _("Very good")),
#)
INSUFF_0=0
INSUFF_1=1
INSUFF_2=2
INSUFF_3=3
INSUFF_4=4
INSUFF_5=5
INSUFF=(
(INSUFF_0, _("--- Please select ---")),
(INSUFF_1, _("Insufficient ")),
(INSUFF_2, _("Lacking in most areas")),
(INSUFF_3, _("Satisfactory (key areas addressed)")),
(INSUFF_4, _("Lacking in areas for comprehensive coverage")),
(INSUFF_5, _("Sufficient")),
)
INSUFF0_0=0
INSUFF0_1=1
INSUFF0_2=2
INSUFF0_3=3
INSUFF0_4=4
INSUFF0_5=5
INSUFF0=(
(INSUFF0_0, _("--- Please select ---")),
(INSUFF0_1, _("Totally Insufficient")),
(INSUFF0_2, _("Insufficient")),
(INSUFF0_3, _("Enough")),
(INSUFF0_4, _("Not enough")),
(INSUFF0_5, _("Very sufficient")),
)

INSUFF1_0=0
INSUFF1_1=1
INSUFF1_2=2
INSUFF1_3=3
INSUFF1_4=4
INSUFF1_5=5
INSUFF1=(
(INSUFF1_0, _("--- Please select ---")),
(INSUFF1_1, _("Insufficient")),
(INSUFF1_2, _("Some basic skills")),
(INSUFF1_3, _("Basic skills")),
(INSUFF1_4, _("Adequate training in key areas")),
(INSUFF1_5, _("Very sufficient")),
)

TRAINING1_0=0
TRAINING1_1=1
TRAINING1_2=2
TRAINING1_3=3
TRAINING1_4=4
TRAINING1_5=5
TRAINING1=(
(TRAINING1_0, _("--- Please select ---")),
(TRAINING1_1, _("No training at all")),
(TRAINING1_2, _("Internal training")),
(TRAINING1_3, _("External training")),
(TRAINING1_4, _("Regular training programmes")),
(TRAINING1_5, _("Special training programmes")),
)


EQUIP_0=0
EQUIP_1=1
EQUIP_2=2
EQUIP_3=3
EQUIP_4=4
EQUIP=(
(EQUIP_0, _("--- Please select ---")),
(EQUIP_1, _("Not at all for both")),
(EQUIP_2, _("We maintain equipment internally")),
(EQUIP_3, _("We outsource maintenance (no internal capacity)")),
(EQUIP_4, _("We have capacity for both (internal and outsource)")),
)

CONDICIVE_0=0
CONDICIVE_1=1
CONDICIVE_2=2
CONDICIVE_3=3
CONDICIVE_4=4
CONDICIVE_5=5
CONDICIVE=(
(CONDICIVE_0, _("--- Please select ---")),
(CONDICIVE_1, _("Totally not conducive")),
(CONDICIVE_2, _("Unsatisfactory")),
(CONDICIVE_3, _("Adequate")),
(CONDICIVE_4, _("Good")),
(CONDICIVE_5, _("Very good")),
)

WEAK_0=0
WEAK_1=1
WEAK_2=2
WEAK_3=3
WEAK_4=4
WEAK_5=5
WEAK=(
(WEAK_0, _("--- Please select ---")),
(WEAK_1, _("Very weak")),
(WEAK_2, _("Weak")),
(WEAK_3, _("Intermediate")),
(WEAK_4, _("Good")),
(WEAK_5, _("Very good")),
)



WEAK1_0=0
WEAK1_1=1
WEAK1_2=2
WEAK1_3=3
WEAK1_4=4
WEAK1_5=5
WEAK1=(
(WEAK1_0, _("--- Please select ---")),
(WEAK1_1, _("Very weak relevance")),
(WEAK1_2, _("Weak")),
(WEAK1_3, _("Intermediate")),
(WEAK1_4, _("Good relevance")),
(WEAK1_5, _("Excellent")),
)

WEAK2_0=0
WEAK2_1=1
WEAK2_2=2
WEAK2_3=3
WEAK2_4=4
WEAK2_5=5
WEAK2=(
(WEAK2_0, _("--- Please select ---")),
(WEAK2_1, _("Very weak perfomance")),
(WEAK2_2, _("Weak")),
(WEAK2_3, _("Intermediate")),
(WEAK2_4, _("Good performance")),
(WEAK2_5, _("Excellent")),
)
WEAK3_0=0
WEAK3_1=1
WEAK3_2=2
WEAK3_3=3
WEAK3_4=4
WEAK3_5=5
WEAK3=(
(WEAK3_0, _("--- Please select ---")),
(WEAK3_1, _("Very weak")),
(WEAK3_2, _("Weak")),
(WEAK3_3, _("Average")),
(WEAK3_4, _("Good")),
(WEAK3_5, _("Very strong")),
)

RANGE1_0=0
RANGE1_1=1
RANGE1_2=2
RANGE1_3=3
RANGE1_4=4
RANGE1_5=5
RANGE1=(
(RANGE1_0, _("--- Please select ---")),
(RANGE1_1,_("0")),
(RANGE1_2, _("1-25")),
(RANGE1_3,_("26-50")),
(RANGE1_4, _("51-75")),
(RANGE1_5, _(">75")),
)

INSUFF3_0=0
INSUFF3_1=1
INSUFF3_2=2
INSUFF3_3=3
INSUFF3_4=4
INSUFF3_5=5
INSUFF3=(
(INSUFF3_0, _("--- Please select ---")),
(INSUFF3_1,_("Not at all")),
(INSUFF3_2,_("Insufficient")),
(INSUFF3_3,_("With difficulty")),
(INSUFF3_4,_("Almost")),
(INSUFF3_5,_("Completely")),
)

INSUFF4_0=0
INSUFF4_1=1
INSUFF4_2=2
INSUFF4_3=3
INSUFF4_4=4
INSUFF4_5=5
INSUFF4=(
(INSUFF4_0, _("--- Please select ---")),
(INSUFF4_1, _("Totally insufficient")),
(INSUFF4_2, _("Weak")),
(INSUFF4_3, _("Intermediate")),
(INSUFF4_4, _("Strong")),
(INSUFF4_5, _("Completely sufficient")),
)
INSUFF5_0=0
INSUFF5_1=1
INSUFF5_2=2
INSUFF5_3=3
INSUFF5_4=4
INSUFF5_5=5
INSUFF5=(
(INSUFF5_0, _("--- Please select ---")),
(INSUFF5_1, _("Totally insufficient")),
(INSUFF5_2, _("Insufficient")),
(INSUFF5_3, _("Not enough")),
(INSUFF5_4, _("Enough")),
(INSUFF5_5, _("More than enough")),
)
INSUFF6_0=0
INSUFF6_1=1
INSUFF6_2=2
INSUFF6_3=3
INSUFF6_4=4
INSUFF6_5=5
INSUFF6=(
(INSUFF6_0, _("--- Please select ---")),
(INSUFF6_1, _("Totally insufficient")),
(INSUFF6_2, _("insufficient")),
(INSUFF6_3, _("Not enough")),
(INSUFF6_4, _("Not so bad")),
(INSUFF6_5, _("Totally")),
)
INSUFF7_0=0
INSUFF7_1=1
INSUFF7_2=2
INSUFF7_3=3
INSUFF7_4=4
INSUFF7_5=5
INSUFF7=(
(INSUFF7_0, _("--- Please select ---")),
(INSUFF7_1, _("Totally insufficient")),
(INSUFF7_2, _("insufficient")),
(INSUFF7_3, _("Huge limitations")),
(INSUFF7_4, _("Minor limitations")),
(INSUFF7_5, _("Without limitations")),
)
INSUFF8_0=0
INSUFF8_1=1
INSUFF8_2=2
INSUFF8_3=3
INSUFF8_4=4
INSUFF8_5=5
INSUFF8=(
(INSUFF8_0, _("--- Please select ---")),
(INSUFF8_1, _("Totally insufficient")),
(INSUFF8_2, _("Insufficient")),
(INSUFF8_3, _("Intermediate")),
(INSUFF8_4, _("Not enough")),
(INSUFF8_5, _("Very sufficien")),
)
PROGRAMMED_0=0
PROGRAMMED_1=1
PROGRAMMED_2=2
PROGRAMMED_3=3
PROGRAMMED_4=4
PROGRAMMED_5=5
PROGRAMMED=(
(PROGRAMMED_0, _("--- Please select ---")),
(PROGRAMMED_1,_("No programmed training")),
(PROGRAMMED_2,_("Once every five years")),
(PROGRAMMED_3,_("Once every three years")),
(PROGRAMMED_4,_("Once every two years")),
(PROGRAMMED_5,_("At least once per year")),

)

NOTATALL_0=0
NOTATALL_1=1
NOTATALL_2=2
NOTATALL_3=3
NOTATALL_4=4
NOTATALL_5=5
NOTATALL=(
(NOTATALL_0, _("--- Please select ---")),
(NOTATALL_1,_("Not at all")),
(NOTATALL_2,_("0.25")),
(NOTATALL_3,_("0.5")),
(NOTATALL_4,_("0.75")),
(NOTATALL_5,_("1")),
)
NOTATALL1_0=0
NOTATALL1_1=1
NOTATALL1_2=2
NOTATALL1_3=3
NOTATALL1_4=4
NOTATALL1_5=5
NOTATALL1=(
(NOTATALL1_0, _("--- Please select ---")),
(NOTATALL1_1,_("Not at all")),
(NOTATALL1_2,_("Marginally")),
(NOTATALL1_3,_("Intermediate")),
(NOTATALL1_4,_("Sufficient")),
(NOTATALL1_5,_("More than Sufficient")),
)
NOTATALL2_0=0
NOTATALL2_1=1
NOTATALL2_2=2
NOTATALL2_3=3
NOTATALL2_4=4
NOTATALL2_5=5
NOTATALL2=(
(NOTATALL2_0, _("--- Please select ---")),
(NOTATALL2_1,_("Not at all")),
(NOTATALL2_2,_("0.25")),
(NOTATALL2_3,_("0.5")),
(NOTATALL2_4,_("0.75")),
(NOTATALL2_5,_("Totally")),
)
NOTATALL3_0=0
NOTATALL3_1=1
NOTATALL3_2=2
NOTATALL3_3=3
NOTATALL3_4=4
NOTATALL3_5=5
NOTATALL3=(
(NOTATALL3_0, _("--- Please select ---")),
(NOTATALL3_1,_("Totally inefficient")),
(NOTATALL3_2,_("0.25")),
(NOTATALL3_3,_("0.5")),
(NOTATALL3_4,_("0.75")),
(NOTATALL3_5,_("Very efficient")),
)
WEAK4_0=0
WEAK4_1=1
WEAK4_2=2
WEAK4_3=3
WEAK4_4=4
WEAK4_5=5
WEAK4=(
(WEAK4_0, _("--- Please select ---")),
(WEAK4_1,_("Very weak")),
(WEAK4_2,_("0.25")),
(WEAK4_3,_("0.5")),
(WEAK4_4,_("0.75")),
(WEAK4_5,_("1")),
)
WEAK5_0=0
WEAK5_1=1
WEAK5_2=2
WEAK5_3=3
WEAK5_4=4
WEAK5_5=5
WEAK5=(
(WEAK5_0, _("--- Please select ---")),
(WEAK5_1,_("Very weak")),
(WEAK5_2,_("0.25")),
(WEAK5_3,_("0.5")),
(WEAK5_4,_("0.75")),
(WEAK5_5,_("Very strong")),
)
PERC0_0=0
PERC0_1=1
PERC0_2=2
PERC0_3=3
PERC0_4=4
PERC0_5=5
PERC0=(
(PERC0_0, _("--- Please select ---")),
(PERC0_1, _("None")),
(PERC0_2, _("25%")),
(PERC0_3, _("50%")),
(PERC0_4, _("75%")),
(PERC0_5, _("All")),
)
PERC1_0=0
PERC1_1=1
PERC1_2=2
PERC1_3=3
PERC1_4=4
PERC1_5=5
PERC1=(
(PERC1_0, _("--- Please select ---")),
(PERC1_1,_("0")),
(PERC1_2, _("1-25")),
(PERC1_3,_("26-50")),
(PERC1_4, _("51-75")),
(PERC1_5, _(">75")),
)
PERC2_0=0
PERC2_1=1
PERC2_2=2
PERC2_3=3
PERC2_4=4
PERC2_5=5
PERC2=(
(PERC2_0, _("--- Please select ---")),
(PERC2_1,_("None")),
(PERC2_2, _("20-30%")),
(PERC2_3,_("31-50%")),
(PERC2_4, _("51-75%")),
(PERC2_5, _(">75%")),
)
PERC3_0=0
PERC3_1=1
PERC3_2=2
PERC3_3=3
PERC3_4=4
PERC3_5=5
PERC3=(
(PERC3_0, _("--- Please select ---")),
(PERC3_1,_("None")),
(PERC3_2, _("5%")),
(PERC3_3,_("20%")),
(PERC3_4, _("40%")),
(PERC3_5, _(">40%")),
)
TRAIN_0=0
TRAIN_1=1
TRAIN_2=2
TRAIN_3=3
TRAIN_4=4
TRAIN_5=5
TRAIN=(
(TRAIN_0, _("--- Please select ---")),
(TRAIN_1,_("No regular training")),
(TRAIN_2, _("Once every 5 years")),
(TRAIN_3,_("Once every 3 years")),
(TRAIN_4, _("Once every 2 years")),
(TRAIN_5, _("At least once per year")),
)
TRAIN2_0=0
TRAIN2_1=1
TRAIN2_2=2
TRAIN2_3=3
TRAIN2_4=4
TRAIN2_5=5
TRAIN2=(
(TRAIN2_0, _("--- Please select ---")),
(TRAIN2_1,_("No programmed training")),
(TRAIN2_2, _("Once in 5 years")),
(TRAIN2_3,_("Once in 3 years")),
(TRAIN2_4, _("Once in 2 years")),
(TRAIN2_5, _("Once per year")),
)


SUFF1_0=0
SUFF1_1=1
SUFF1_2=2
SUFF1_3=3
SUFF1_4=4
SUFF1_5=5
SUFF1=(
(SUFF1_0, _("--- Please select ---")),
(SUFF1_1,_("Not at all")),
(SUFF1_2,_("Marginally sufficient")),
(SUFF1_3,_("Somewhat sufficient")),
(SUFF1_4,_("Sufficient")),
(SUFF1_5,_("More than sufficient")),
)


EFF_0=0
EFF_1=1
EFF_2=2
EFF_3=3
EFF_4=4
EFF_5=5
EFF=(
(EFF_0, _("--- Please select ---")),
(EFF_1,_("Very ineffective")),
(EFF_2,_("Ineffective")),
(EFF_3,_("Intermediate")),
(EFF_4,_("Effective")),
(EFF_5,_("Very effective")),
)

INSP_0=0
INSP_1=1
INSP_2=2
INSP_3=3
INSP_4=4
INSP_5=5
INSP=(
(INSP_0, _("--- Please select ---")),
(INSP_1,_("Pest diagnostic")),
(INSP_2,_("Treatment")),
(INSP_3,_("Field inspection")),
(INSP_4,_("Packing inspection")),
(INSP_5,_("Inspection and storage facilities")),
)
PHY_0=0
PHY_1=1
PHY_2=2
PHY_3=3

PHY=(
(PHY_0, _("--- Please select ---")),
(PHY_1,_("None")),
(PHY_2,_("Phytosanitary certificate")),
(PHY_3,_("Re-export certificate")),
)
LIMIT_0=0
LIMIT_1=1
LIMIT_2=2
LIMIT_3=3
LIMIT_4=4
LIMIT_5=5
LIMIT=(
(LIMIT_0, _("--- Please select ---")),
(LIMIT_1,_("Totally insufficient")),
(LIMIT_2,_("Insufficient")),
(LIMIT_3,_("With strong limitations")),
(LIMIT_4,_("With some limitations")),
(LIMIT_5,_("Without limitations")),
)


FEW_0=0
FEW_1=1
FEW_2=2
FEW_3=3
FEW_4=4
FEW_5=5
FEW=(
(FEW_0, _("--- Please select ---")),
(FEW_1,_("None")),
(FEW_2,_("Few")),
(FEW_3,_("Some")),
(FEW_4,_("Most")),
(FEW_5,_("All")),
)

class Membership1(models.Model):
    """ TradePartneners1 """
    partner = models.CharField(_("Partner"), max_length=500)
    def __unicode__(self):
        return self.partner
    class Meta:
        verbose_name_plural = _("Memberships")
    pass

class Membership2(models.Model):
    """ TradePartneners1 """
    partner = models.CharField(_("Partner"), max_length=500)

    def __unicode__(self):
        return self.partner
        
    class Meta:
        verbose_name_plural = _("Memberships")
    pass

class Module1(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 1 - Country Profile")
        verbose_name_plural = _("Module 1 - Country Profile")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    country = models.ForeignKey(CountryPage,related_name="mod1_country",help_text=_("Enter the official name of the Country if not already assigned."),)
    region = models.IntegerField(_("2. Region"), choices=REGIONS, default=None,help_text=_("FAO has 7 regions defined. Use the FAO country grouping,i.e. Africa, Asia, Latin America and the Caribbean, Europe, Near East, North America and Southwest Pacific. "),)
    m_3 = models.TextField(_("3. Population and year of estimate"), blank=True, null=True,help_text='Include the Month and Year e.g. (July 2008 est.) ')
    m_4 = models.TextField(_("4. Total Land Area - sq. km."), blank=True, null=True,help_text='Please convert units to sq. km.')
    m_5= models.TextField(_("5. Total Arable Land - sq. km."), blank=True, null=True,help_text='Includes Agriculural land and Arable and permanent crop land' )
    m_6= models.TextField(_("6. Total Natural Vegetation - sq. Km"), blank=True, null=True,help_text='This includes forest and other areas ')
    #m_7
    #m_8
    m_9 = models.IntegerField(_("9. Total Value of imports of plant and plant products (includes Forestry)in US Dollars"), choices=VAL_IMP, default=None,help_text=_("Enter most recent data "),)
    m_10 = models.NullBooleanField(_("10. Do imported plants and plant products often arrive in your country after being in transit in another country?"), choices=BOOL_CHOICES,blank=True, null=True,help_text=_("Select no if the activity is not significant "),)
    #m_11
    m_12 = models.IntegerField(_("12. Total Value of Exports of plant and plant products (includes Forestry) in US Dollars"), choices=VAL_EXP, default=None,help_text=_("Enter most recent data "),)
    m_13 = models.IntegerField(_("13. Approximately what percentage of total exports (includes Forestry) are re-export consignments i.e. products that originated from another country?"), choices=VAL_PERCENT, default=None,help_text=_("Enter most recent data or best estimate"),)
    m_14 = models.TextField(_("14. World Bank Economic Classification (GNI - Gross National Income per capita)"), blank=True, null=True,help_text='Visit the website of the worldbank for this kind of information (<a href="http://www.worldbank.org">www.worldbank.org</a>) . ')
    m_15 = models.TextField(_("15. Latest GDP in US Dollars (World Bank)"), blank=True, null=True,help_text='include year GDP was recorded e.g. 8,526 (2008) ')
    m_16 = models.IntegerField(_("16. Percentage contribution of Agriculture (including Forestry) to GDP"), choices=VAL_PERCENT, default=None,help_text=_("Please round up the value "),)
    m_17 = models.IntegerField(_("17. What percentage of GDP contributed by agriculture can be attributed to the value of plant and plant products (including Forestry)"), choices=VAL_PERCENT, default=None,help_text=_("Enter most reecent data "),)
    m_18 = models.IntegerField(_("18. List the agricultural labor force (including Forestry) as a percent of total labor force."), choices=VAL_PERCENT, default=None,help_text=_("Please round up the value "),)
    m_19 = models.IntegerField(_("19. What percentage of the agricultural labour force is directly employed in the production of plant and plant products (including Forestry)?"), choices=VAL_PERCENT, default=None,help_text=_("Enter most reecent data "),)
    #m_20
    #m_21
    m_22 = models.ManyToManyField(Membership1,verbose_name=_("22. Membership / Signatory to:"),related_name='Membership_+', blank=True, null=True,help_text=_("Select all that apply."))
    m_23 = models.ManyToManyField(Membership2,verbose_name=_("23. Member of Regional Economic Integration/Co-operation Organizations:"),related_name='Membership_+', blank=True, null=True,help_text=_("Tick all that apply."))
    m_24 = models.IntegerField(_("24. Number of Bilateral phytosanitary arrangements - Operational"), choices=NUM_BILATERAL, default=None,help_text=_("These are arrangements that have been negotiated and are actively being implemented. "),)
    m_25 = models.IntegerField(_("25. Number of bilateral phytosanitary arrangements - Negotiations in Progress"), choices=NUM_BILATERAL, default=None,help_text=_("This refers to ongoing negotiations for establishing phytosanitary arrangements. "),)
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_country = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_region = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_3 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_4 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_5 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_6 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_7 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_8 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_9 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_10 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_11 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_12 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_13 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_14 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_15 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_16 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_17 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_18 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_19 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_20 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_21 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_22 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_23 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_24 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_25 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
    c_m_26 = models.TextField(_("Comment"), blank=True, null=True,help_text='')
     
    def __unicode__(self):
        return self.title

 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module1, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})
            
class Module1Aid(models.Model):
    module1 = models.ForeignKey(Module1)
    donoragency = models.CharField(_("Donor Agency"), blank=True, null=True, max_length=250,)
    titleprj = models.CharField(_("Title of Project"), blank=True, null=True,max_length=250,)
    date = models.CharField(_("Date Commenced"), blank=True, null=True,max_length=250,)
    duration = models.CharField(_("Duration"), blank=True, null=True,max_length=250,)
    amount = models.CharField(_("Amount (US)"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.titleprj
    def name(self):
        return self.titleprj
    
class Module1MajorCrops(models.Model):
    module1 = models.ForeignKey(Module1)
    crops = models.CharField(_("Crops"), blank=True, null=True,max_length=250,)
    propagation = models.BooleanField(verbose_name=_("Propagation"), default=None) 
    germplasm = models.BooleanField(verbose_name=_("Germplasm"), default=None) 
    consumption = models.BooleanField(verbose_name=_("Consumption"), default=None) 
    wooden = models.BooleanField(verbose_name=_("Wooden and Cane Products"), default=None) 
    industrial = models.BooleanField(verbose_name=_("ndustrial Products"), default=None) 
    other = models.BooleanField(verbose_name=_("Other Uses"), default=None) 
   
    def __unicode__(self):
        return self.crops
    def name(self):
        return self.crops

class Module1MajorImports(models.Model):
    module1 = models.ForeignKey(Module1)
    crops = models.CharField(_("Crops"), blank=True, null=True,max_length=250,)
    propagation = models.BooleanField(verbose_name=_("Propagation"), default=None) 
    germplasm = models.BooleanField(verbose_name=_("Germplasm"), default=None) 
    consumption = models.BooleanField(verbose_name=_("Consumption"), default=None) 
    wooden = models.BooleanField(verbose_name=_("Wooden and Cane Products"), default=None) 
    industrial = models.BooleanField(verbose_name=_("ndustrial Products"), default=None) 
    other = models.BooleanField(verbose_name=_("Other Uses"), default=None) 
   
    def __unicode__(self):  
        return self.crops
    def name(self):
        return self.crops
    
class Module1MajorExports(models.Model):
    module1 = models.ForeignKey(Module1)
    crops = models.CharField(_("Crops"), blank=True, null=True,max_length=250,)
    propagation = models.BooleanField(verbose_name=_("Propagation"), default=None) 
    germplasm = models.BooleanField(verbose_name=_("Germplasm"), default=None) 
    consumption = models.BooleanField(verbose_name=_("Consumption"), default=None) 
    wooden = models.BooleanField(verbose_name=_("Wooden and Cane Products"), default=None) 
    industrial = models.BooleanField(verbose_name=_("ndustrial Products"), default=None) 
    other = models.BooleanField(verbose_name=_("Other Uses"), default=None) 
   
    def __unicode__(self):  
        return self.crops
    def name(self):
        return self.crops
    
class Module1MajorPartenerImport(models.Model):
    module1 = models.ForeignKey(Module1)
    country = models.CharField(_("country"), blank=True, null=True,max_length=250,)
   
    def __unicode__(self):  
        return self.country
    def name(self):
        return self.country
    
class Module1MajorPartenerExport(models.Model):
    module1 = models.ForeignKey(Module1)
    country = models.CharField(_("country"), blank=True, null=True,max_length=250,)
   
    def __unicode__(self):  
        return self.country
    def name(self):
        return self.country
 
class Module2(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 2 -  National phytosanitary legislation")
        verbose_name_plural = _("Module 2 -  National phytosanitary legislation")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.IntegerField(_("1.1. What is the legal system of the country?"), choices=CIVIL, default=None,help_text=_("Civil legislation system, which has its roots in Roman legislation and which is based on written legal codes. Napoleonic Code: Based on the primacy of statutes enacted by the legislature. These statutes are integrated into a comprehensive code designed to be applied by the courts with a minimum of judicial interpretation.Common Legislation: A system of legislation that is derived from judges' decisions (which arise from the judicial branch of government), rather than statutes or constitutions (which are derived from the legislative branch of government).  Source: <a href='https://www.law.berkeley.edu/library/robbins/pdf/CommonLawCivilLawTraditions.pdf'>click here</a> for Common Legislation. Islamic Llegislation, which is derived from the Koran and can be found in the Middle East and in some African countries Source: <a href='http://www.islamicsupremecouncil.org/understanding-islam/legal-rulings/52-understanding-islamic-law.html'>click here</a> for the Islamic legislation, which is derived from the Koran and can be found in the Middle East and in some African countries. "),)
    m_2 = models.TextField(_("1.2. How is legislation and regulations developed and enacted?"), blank=True, null=True,help_text=_("List the major steps (drafting to enactment) for a piece of legislation to be approved nationally for implementation."),)
    m_3 = models.TextField(_("1.3. How are legislative and executive functions and responsibilities distributed with government institutions and at different levels?"), blank=True, null=True,help_text=_(" "),)
    m_4 = models.TextField(_("1.4. Which existing policy frameworks (agriculture, decentralization, privatization, globalization, biosecurity, trade etc.) provide context for the development of the national phytosanitary legislation?"), blank=True, null=True,help_text=_(" "),)
    m_5 = models.NullBooleanField(_("1.5. Does the present legislation have overlaps or conflict of institutional responsibilities in phytosanitary matters?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.TextField(_("1.6. List the main gaps concerning institutional responsibilities on phytosanitary matters."), blank=True, null=True,help_text=_(" "),)
    m_7 = models.TextField(_("1.7. List other existing laws and regulations that reference any current phytosanitary legislation or regulations."), blank=True, null=True,help_text=_(" "),)
    m_8 = models.NullBooleanField(_("2.1. Is there a National Plant Protection Organization mandated in National Legislation, in accordance with provisions of IPPC Art.IV para.1?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This may be stated in the national Phytosanitary Law/Act or in subsidiary legislation or other legal instruments or documented procedures."),)
    m_9 = models.TextField(_("2.2. Enter the name, address and contact details of the national plant protection organization."), blank=True, null=True,help_text=_(" "),)
    m_10 = models.TextField(_("2.3. Name the Act that established the NPPO."), blank=True, null=True,help_text=_(" "),)
    m_11 = models.IntegerField(_("2.4. Year the Act was enacted."), choices=YEAR, default=None,help_text=_(" "),)
    m_12 = models.IntegerField(_("2.5. Year of the most recent revision of Act."), choices=YEAR, default=None,help_text=_(" "),)
    m_13 = models.IntegerField(_("2.6. Current status of the Act"), choices=ACT, default=None,help_text=_("The ideal situation is that the legislation is updated to the last revision of the IPPC. "),)
    m_14 = models.TextField(_("2.7. List any implementing or enabling legislation, with date of enactment, which relate to implementation of the Phytosanitary Law/Act."), blank=True, null=True,help_text=_("This includes phytosanitary regulations. "),)
    m_15 = models.IntegerField(_("3.1. Is the scope of the present Legislation (Act and Regulations) consistent with all the provisions of the Art.1 par. 1 of the revised text of the IPPC (1997) and with those of <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> secs. 1.1 and 1.2 ?"), choices=DEFINITIONS, default=None,help_text=_("IPPC (1997), Art.1 par. 1, With the purpose of securing common and effective action to prevent the spread and introduction of pests of plants and plant products, and to promote appropriate measures for their control, the contracting parties undertake to adopt the legislative, technical and administrative measures specified in this Convention and in supplementary agreements pursuant to Article XVI. <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> Sec.1&2, Basic principles concerning sovereignty and necessity. "),)
    m_16 = models.NullBooleanField(_("3.2. Does the legislation provide for the control of all plant pests (including weeds, forestry pests, LMOs, Biological Control Agents, IAS) as well as all plant, plant products and other regulated articles (including wood packaging materials and conveyance)?"), choices=BOOL_CHOICES,blank=True, null=True,help_text=_("This refers to not just regulated pests or quarantine pests - it is all plant pests. "),)
    m_17 = models.NullBooleanField(_("3.3. Does the legislation cover both locally produced and imported plants, plant products and other regulated articles?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_18 = models.IntegerField(_("4.1. Are the definitions utilized in the Legislation and Regulations, consistent with the ones established in the SPS Annex A and in the IPPC Art II, and <a href='https://www.ippc.int/en/publications/622/' target='_blank'>ISPM No.5</a>?"), choices=DEFINITIONS1, default=None,help_text=_(" "),)
    m_19 = models.NullBooleanField(_("4.2. Does the definitions section of the Legislation include a general statement specifying that any term not specifically defined shall have its normally accepted meaning, except that any term which also appears in the IPPC shall be defined by reference to that Convention and its associated documentation?"), choices=BOOL_CHOICES,blank=True, null=True,help_text=_("Note that the ISPM 5 Glossary of phytosanitary terms is updated annually. "),)
    m_20 = models.NullBooleanField(_("5.1. Is the NPPO responsible for the issuance of phytosanitary certificates to comply with the phytosanitary regulations of the importing country for consignments of plants, plant products and other regulated articles? (IPPC Art IV.2(a), <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> Section 2.8 and 2.9)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Also see ISPMs <a href='https://www.ippc.int/en/publications/613/' target='_blank'>7</a> and <a href='https://www.ippc.int/en/publications/609/' target='_blank'>12</a>  "),)
    m_21 = models.NullBooleanField(_("5.2. Is the NPPO responsible for arranging for phytosanitary certification, in conformity with the certifying statement to be made pursuant to paragraph 2(b) of Article V of the New Revised Text of the IPPC?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Refers to the model phytosanitary certificate in the annex of the IPPC convention text "),)
    m_22 = models.NullBooleanField(_("5.3. Is the NPPO responsible for the surveillance for plant pests on growing plants, including both areas under cultivation (e.g. fields, plantations, nurseries, gardens, greenhouses and laboratories) and wild flora, and of plants and plant products in storage or in transportation, particularly with the object of reporting the occurrence, outbreak and spread of pests, and of controlling those pests? (IPPC Art. IV.2b, and 2e and VII.2j and <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> Section 2.6 and ISPMs:<a href='https://www.ippc.int/en/publications/615/' target='_blank'>No. 6</a> and <a href='https://www.ippc.int/en/publications/612/' target='_blank'>No. 8</a> )."), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("List the current mandate of the agency designated to carry out the functions of the NPPO. Identify the responsibilities in terms of surveillance by other agencies other than the NPPO in the next question below. <br> <br> <br><i>If answer is <b>Yes</b> go to question <b>5.5.</b></i>"),)
    m_23 = models.TextField(_("5.4. If no, is there another government department or agency responsible for pest surveillance activities? If so, name the organization and its relationship to the NPPO."), blank=True, null=True,help_text=_("If the relationship is formal and has legislation or documented procedure to reinforce it please enter the title of the reinforcing legislation in Question 2.7 above. "),)
    m_24 = models.NullBooleanField(_("5.5. Is the NPPO responsible for the inspection of consignments of plants and plant products moving in international traffic and, where appropriate, the inspection of other regulated articles , particularly with the object of preventing the introduction and/or spread of pests? (IPPC Art.IV.2c <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> and ISPM No.20)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_25 = models.NullBooleanField(_("5.6. Is the NPPO responsible for the disinfestation or disinfection of consignments of plants, plant products and other regulated articles moving in international traffic, to ensure phytosanitary requirements are met? IPPC Art.IV.2d"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_26 = models.NullBooleanField(_("5.7. Is the NPPO responsible for the protection of endangered areas and the designation, maintenance and surveillance of pest free areas and areas of low pest prevalence? (IPPC IV.2.e and <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> (2.3) and ISMP 4,8,10 and 22)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_27 = models.NullBooleanField(_("5.8. Is the NPPO responsible for conducting pest risk analysis? (IPPC IV.2f and VII.2g, and ISPMs: <a href='https://www.ippc.int/en/publications/592/' target='_blank'>No.2</a>, <a href='https://www.ippc.int/en/publications/622/' target='_blank'>No. 5</a> (including supplement No. 2), No.11 and No.21."), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_28 = models.NullBooleanField(_("5.9. Is the NPPO responsible for ensuring through appropriate procedures that the phytosanitary security of consignments after certification regarding composition, substitution and re-infestation is maintained prior to export? (IPPC IV.2g. Art. V and <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> Section 2.9 and ISPMs 7 and 12"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_29 = models.NullBooleanField(_("5.10. Is the NPPO responsible for training and development of staff? (IPPC Art IV.2h)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_30 = models.NullBooleanField(_("5.11. Is the NPPO responsible for the distribution of information, within the territory of the contracting party, regarding regulated pests and the means of their prevention and control? (IPPC IV.3a)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("within the territory of the contracting party refers to your country."),)
    m_31 = models.NullBooleanField(_("5.12. Is the NPPO involved in research and investigation in the field of plant protection? (IPPC Art. IV.3)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_32 = models.NullBooleanField(_("5.13. Is the NPPO responsible for the issuance of phytosanitary regulations? (IPPC Art IV.3c)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_33 = models.NullBooleanField(_("5.14. Is the NPPO directly responsible for submission of a description of its official national plant protection organization and of changes in such organization to the Secretary of the IPPC? (IPPC Art IV.4)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_34 = models.NullBooleanField(_("5.15. Does the legislation mandate the Phytosanitary Authority to designate a contact point for the IPPC? (IPPC Article VIII.2, <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> Section. 2.16)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_35 = models.NullBooleanField(_("5.16. Does the legislation specify the NPPOs responsibility for providing justification concerning phytosanitary measures to other countries, if required? (IPPC Article VII.2c)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_36 = models.NullBooleanField(_("5.17. Does the legislation specify the NPPO responsibility for providing information, where requested, by national, regional or international organizations regarding import and export regulations in force and regarding the technical requirements for plant material and other regulated articles? (IPPC Article VII.2c; <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> Section 1.5)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_37 = models.NullBooleanField(_("6.1. Does the legislation contain a provision for stakeholder participation in NPPO matters?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Stakeholders include persons or agencies or groups that are beneficiaries of the services of the NPPO or function as partners in the delivery of services or in decision making.  <br> <br> <br><i>If answer is <b>No</b> go to question <b>7.1</b></i>"),)
    m_38 = models.NullBooleanField(_("6.2. Are stakeholders' roles, responsibilities and rights defined in the legislation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Stakeholders include persons or agencies or groups that are beneficiaries of the services of the NPPO or function as partners in the delivery of services or in decision making. "),)
    m_39 = models.TextField(_("6.3. What arrangements are in place to ensure stakeholder participation in NPPO matters?"), blank=True, null=True,help_text=_("Particularly if there is no provision in the legislation for ensuring appropriate stakeholder participation. Stakeholders include persons or agencies or groups that are beneficiaries of the services of the NPPO or function as partners in the delivery of services or in decision making. "),)
    m_40 = models.NullBooleanField(_("7.1. Does the law, or its subsidiary legislation, establish the minimum requirements in terms of qualifications and skills of inspectors? <a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a>  Section 5.2.1 and <a href='https://www.ippc.int/en/publications/613/' target='_blank'>ISPM 7</a> Section 3.1"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_41 = models.NullBooleanField(_("7.2. Does the legislation allow the responsible ministry or agency to use not only its own employees but also employees of other authorities (public - or private, so long as there is no conflict of interest)? <a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a> Section 5.1.7"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This does not include the function of issuance of phytosanitary certificates, refer to the IPPC (1997) Art V 2a. "),)
    m_42 = models.NullBooleanField(_("7.3. Does the legislation require that, whenever the NPPO authorizes other government services, non-governmental organizations, agencies or persons, to act on its behalf, the NPPO must maintain its responsibility and establish operational and audit procedures, for, corrective actions, system review and withdrawal of authorization?.(<a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a> 5.1.7)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_43 = models.NullBooleanField(_("7.4. Is the mandate of an appointed or designated inspector subject to limitations set out in the written instrument of appointment?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_44 = models.NullBooleanField(_("7.5. Does the legislation explicitly assign the issuance of phytosanitary certificates for export, to NPPO inspectors appointed or designated only? (IPPC Art V 2a.)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_45 = models.NullBooleanField(_("8.1. Does the legislation specify that the inspector has a duty to perform inspection of plants or plant products under cultivation, in the wild, in storage or in transit in order to report the existence, outbreak and spread of pests? (IPPC Art IV. 2b and VIII 1a)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Pests refers to all pests and not just those regulated or identified as quarantine pests. "),)
    m_46 = models.NullBooleanField(_("8.2. Does the legislation specify the duty of the inspectors to perform the inspection, test or take samples (including for analysis which may result in the destruction of the sample) of consignments of plants, plant products or other regulated articles designated for import or export from the country? <a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a> Section 4.6, <a href='https://www.ippc.int/en/publications/598/' target='_blank'>ISPM 23</a> sec. 1.3"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_47 = models.NullBooleanField(_("8.3. Does the legislation specify the duties of the inspectors to perform the inspection of storage and transport facilities? <a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a> Section 4.6"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_48 = models.NullBooleanField(_("8.4. Does the legislation specify the duty of the inspectors to perform the disinfection of consignments (either directly or through direct supervision of the NPPO)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_49 = models.NullBooleanField(_("8.5. Does the legislation specify the duty of the inspectors to detain, treat or require treatment, refuse or take emergency action on imported consignments of plants, plant products or other regulated articles? <a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a> Section 4.6"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_50 = models.NullBooleanField(_("8.6. Does the legislation specify the duty of the inspectors to perform the control of waste being disposed of from aircraft and ships or from premises which process or wash imported plant material to reduce phytosanitary risk (includes forestry)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_51 = models.NullBooleanField(_("8.7. Does the legislation specify the duty of the inspectors to issue phytosanitary certificates (on behalf of the NPPO)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_52 = models.NullBooleanField(_("8.8. Does the legislation make clear the respective roles of the minister, the head of the NPPO and the inspectors and others?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_53 = models.NullBooleanField(_("9.1. Does the phytosanitary legislation clearly outline the scope of the inspectors' powers?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_54 = models.NullBooleanField(_("9.2. Does the phytosanitary legislation grant the inspectors power to enter and search any area or premises and require any person to produce any supporting documentation required by legislation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_55 = models.NullBooleanField(_("9.3. Does the phytosanitary legislation grant the inspectors power to inspect, examine and make copies of such documentation, or take extracts of registers or records and seize the same?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_56 = models.NullBooleanField(_("9.4. Does the phytosanitary legislation grant the inspectors power to stop and search any person, baggage, packaging, conveyance or any other regulated article, upon entry into, movement within or exit from the country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_57 = models.NullBooleanField(_("9.5. Does the phytosanitary legislation grant the inspectors power to stop the distribution, sale or use of any plant, plant product or any other regulated article, which the inspector has reason to believe is harboring a regulated pest, for a specific time period?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_58 = models.NullBooleanField(_("9.6. Does the phytosanitary legislation grant the inspectors power to seize, destroy, detain, treat or otherwise dispose of any plants, plant products or other regulated articles, or order that any such action be taken?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_59 = models.NullBooleanField(_("10.1. Are inspectors protected from personal liability for official decisions made pursuant to the enforcement of the phytosanitary legislation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_60 = models.NullBooleanField(_("11.1. Does the legislation grant the NPPO the power to prescribe and adopt phytosanitary measures concerning the importation of plants, plant products and other regulated articles, including for example, inspection, prohibition on importation, or treatment?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_61 = models.NullBooleanField(_("11.2. Does the legislation specify that the phytosanitary measures shall not be applied for non-regulated pests?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_62 = models.NullBooleanField(_("11.3. Does the legislation specify that the phytosanitary measures prescribed by the NPPO shall be technically justified through pest risk analysis or based on international standards?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_63 = models.NullBooleanField(_("11.4. Does the legislation establish that phytosanitary measures shall be adopted in accordance with the international phytosanitary principles in <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a>?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Refer to <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a> "),)
    m_64 = models.NullBooleanField(_("11.5. Does the NPPO have legal authority to refuse entry or detain, or require treatment, destruction or removal from the country of plants, plant products and other regulated articles or consignments thereof, that do not comply with the prescribed phytosanitary measures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_65 = models.NullBooleanField(_("11.6. Has the NPPO the legal power to prohibit or restrict the movement of regulated pest, including those LMOs and IAS that are pests of plants?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_66 = models.NullBooleanField(_("11.7. Does the legislation give the power to the NPPO to prohibit or restrict the movement of biological control agents and other organisms of phytosanitary concern, claimed to be beneficial?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_67 = models.NullBooleanField(_("11.8. Is the NPPO the sole official service responsible for the operation and/or organization and management of the phytosanitary import regulatory system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_68 = models.NullBooleanField(_("12.1. Does the legislation confer powers to require that importers know and comply with the import phytosanitary requirements established by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This extends also to passengers that may be carrying plant material and arriving at a point of entry.  "),)
    m_69 = models.NullBooleanField(_("12.2. Does the legislation establish that plants, plant products and regulated articles may only be imported at official points of entry designated by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Note that contracting parties are obligated to publish and communicate official points of entry for specified consignments, see IPPC (1997) Art VII 2d.  "),)
    m_70 = models.NullBooleanField(_("12.3. Does the legislation establish that all consignments of plant, plant products or other regulated articles that arrive to the country are under phytosanitary detention until officially released by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_71 = models.NullBooleanField(_("12.4. Does the legislation give the NPPO the power to approve/accredit transitional facilities owned and operated by third parties (official or private), to be used for inspection, treatment, or storage of consignments of plant, plant products and other regulated articles that still are pending phytosanitary release?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_72 = models.NullBooleanField(_("12.5. Does the legislation allow the NPPO to, after assessment of the phytosanitary risk and operational feasibility, authorize that consignments of plants, plant products or other regulated articles can be inspected at their final destination or in a transitional facility, instead of the point of entry, If requested by the importer, and if consignments are properly sealed and marked?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_73 = models.NullBooleanField(_("12.6. Does the legislation provide for the adoption of emergency actions that may be necessary if the inspector detects a pest which is determined by the NPPO to be regulated and not listed as being associated with the commodity from the exporting country, or if the inspector detects other organisms posing a potential phytosanitary threat?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_74 = models.NullBooleanField(_("12.7. In case of emergency actions or pest interception, does the legislation provide for the notification of the pest interception or the emergency actions to the exporting contracting party (IPPC Art. VII.6; <a href='https://www.ippc.int/en/publications/608/' target='_blank'>ISPM 13</a>)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_75 = models.NullBooleanField(_("12.8. In case of the importation of infected plants or plant products, does the legislation specify who pays for reshipment, destruction, treatment and disinfection?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_76 = models.NullBooleanField(_("13.1. Does the legislation address the situation of consignments of plant, plant products or other regulated articles that enter into the country in transit to another?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_77 = models.NullBooleanField(_("14.1. Does the legislation address the obligation of persons entering into the country to declare plants, plant products or other regulated articles?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_78 = models.NullBooleanField(_("14.2. Does the legislation define the functions and duties of employees of the postal service, private shipping agents, officials of customs department and port authorities or law enforcement who are involved or have responsibilities to exercise when plants or plant products arrive in the country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_79 = models.NullBooleanField(_("14.3. Does the legislation include the requirement to inform the NPPO of the arrival of plants or plant products in the country, and to store consignments of plants or plant products until phytosanitary inspectors can take custody of them?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_80 = models.NullBooleanField(_("15.1. Does the legislation require that the NPPO only provides certification of plant, plant products and other regulated articles after verification of compliance with the phytosanitary requirements of the importing country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_81 = models.NullBooleanField(_("15.2. Does the legislation require a phytosanitary certificate to be issued in accordance with the IPPC model? <a href='https://www.ippc.int/en/publications/613/' target='_blank'>ISPM 7</a> sec. 4"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_82 = models.NullBooleanField(_("15.3. Does the legislation specify who pays for any treatment required by the NPPO as a condition to issue the PC?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_83 = models.NullBooleanField(_("15.4. Does the legislation identify the exporter obligation and the NPPO's responsibility to guarantee the phytosanitary security of a consignment after certification and until it actually leaves the country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_84 = models.NullBooleanField(_("15.5. Does the legislation allow the NPPO to approve/accredit phytosanitary service providers to act under the responsibility of the NPPO in diverse functions/steps of the certification process?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Phytosanitary service providers are those agencies whether public or private that have been contracted or delegated to perform functions of the NPPO except issuance of the phytosanitary certificate. "),)
    m_85 = models.NullBooleanField(_("15.6. Does the legislation establish that the public officers in charge of the issuance of phytosanitary certificates shall be technically qualified and dully authorized by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_86 = models.NullBooleanField(_("15.7. Does the legislation provide the NPPO with the authority to establish and enforce the application of phytosanitary procedures necessary for the assurance of the identity and traceability to the place of origin (e.g. Pest Free Areas), of export consignments when this is required by the importing country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_87 = models.NullBooleanField(_("15.8. Does the legislation specify that a re-export certificate, following the model of the IPPC, should be used when an imported consignment that has been exposed to infestation or split up, or combined with other consignments or repackaged, is re-exported?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_88 = models.NullBooleanField(_("16.1. Does the phytosanitary legislation provide for the determination and identification of PFA?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_89 = models.NullBooleanField(_("16.2. Does the phytosanitary legislation provide for the determination and identification of Areas of Low Pest Prevalence (ALPP)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_90 = models.NullBooleanField(_("17.1. Does the phytosanitary legislation provide for pest surveillance to be undertaken by the NPPO? (IPPC Art. IV 2.b)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Refer also to<a href='https://www.ippc.int/en/publications/615/' target='_blank'>ISPM 6</a>  for details regarding pest surveillance.  "),)
    m_91 = models.NullBooleanField(_("17.2. Does the phytosanitary legislation require phytosanitary inspectors, other national and local government agencies, research institutions, universities, scientific societies (including amateur specialists), producers, consultants, museums,and the general public to report the appearance of new pests or certain pests as required by the NPPO? (<a href='https://www.ippc.int/en/publications/615/' target='_blank'>ISPM 6</a> Section 1.1)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("to cooperate with one another to the fullest practicable extent in achieving the aims of this Convention (Article VIII.1), and in particular to cooperate in the exchange of information on plant pests, particularly the reporting of the occurrence, outbreak or spread of pests that may be of immediate or potential danger, in accordance with such procedures as may be established by the Commission ...(Article VIII.1a). "),)
    m_92 = models.NullBooleanField(_("17.3. Does the phytosanitary legislation require anyone who publishes the occurrence of a new pest in the country to concurrently submit that publication to the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This is not a provision for the NPPO to approve or discredit a publication but a procedure to be informed duly in order to take measures to mitigate risks or perform surveillance to verify occurrence of a pest as soon as possible.  "),)
    m_93 = models.NullBooleanField(_("18.1. Does the NPPO have the legal authority to declare an area to be under quarantine, and impose temporary restrictions on the exercise of rights by citizens and legal entities and impose additional phytosanitary measures (e.g. limiting the movement of plant, plant products and other regulated articles, destruction, treatments, etc)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_94 = models.NullBooleanField(_("18.2. Does the phytosanitary legislation establish a procedure for review of areas under quarantine and the lifting of quarantine where the situation has changed?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_95 = models.NullBooleanField(_("18.3. Does the phytosanitary legislation impose a duty on the owner or occupier, and if necessary on owners or occupiers of nearby land, ordering them to take whatever measures the inspector considers appropriate to control a pest?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_96 = models.NullBooleanField(_("18.4. Does the legislation establish that where a land owner does not carry out the ordered treatment within the required time period, the NPPO may carry out the treatment, but the land owner retains the obligation to pay?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_97 = models.NullBooleanField(_("19.1. Does the legislation specify what can be considered as a phytosanitary emergency situation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_98 = models.NullBooleanField(_("19.2. Does the legislation specify who the competent authority is to declare an emergency phytosanitary situation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Competent authority: Refer to <a href='https://www.ippc.int/en/publications/622/' target='_blank'>ISPM 5</a> Supplement 1 Para. 5.7 "),)
    m_99 = models.NullBooleanField(_("19.3. Does the legislation establish the obligation of other government agencies to collaborate with the NPPO under a phytosanitary emergency situation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_100 = models.NullBooleanField(_("19.4. Does the legislation contain provisions for economic compensation to the owners affected by eradication procedures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_101 = models.NullBooleanField(_("19.5. Does the legislation allow for the destruction of plants that may not be infested but that have been exposed to the pest infestation, in buffer zones surrounding the infested plants?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_102 = models.NullBooleanField(_("19.6. Does the legislation create a Phytosanitary Emergency Fund to be solely utilized in case of a declaration of a phytosanitary emergency?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_103 = models.NullBooleanField(_("20.1. Does the legislation establish the collection of fees by the NPPO services?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Fees are generally charged to recover costs of services offered by NPPOs. These fees may be charged by some NPPOs to cover costs of sampling, inspection, PRA, Export certification, pest diagnostics, as well as to owners of Pest free places or sites of production among other possible services.   <br> <br> <br><i>If answer is <b>No</b> go to question <b>21.1.</b></i> "),)
    m_104 = models.NullBooleanField(_("20.2. Does the legislation allow for the NPPO to access the fees and fines collected, to improve its services?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_105 = models.NullBooleanField(_("20.3. Are the NPPO fees non-discriminatory and non-protectionist?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Fees should follow the principle of national treatment and not become impediments to trade. Refer to Agreement on Sanitary and Phytosanitary Meaures of the WTO Annex C. 1f.  "),)
    m_106 = models.NullBooleanField(_("20.4. Are the NPPOs fees based on the actual cost of the services?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Refer to Agreement on Sanitary and Phytosanitary Meaures of the WTO Annex C. 1f. "),)
    m_107 = models.NullBooleanField(_("20.5. Does the legislation allow for the fees charged by the NPPO to be openly and transparently accessible to the general public?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_108 = models.NullBooleanField(_("21.1. Does the legislation identify as an offense importing or exporting plants or plant products without the proper documentation or through an unapproved port of entry?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_109 = models.NullBooleanField(_("21.2. Does the legislation identify as an offense obstructing or hindering an inspector in the performance of his or her official functions or failing to comply with an inspector's instruction?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_110 = models.NullBooleanField(_("21.3. Does the legislation identify as an offense knowingly or recklessly providing false information to an official of the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Official of the NPPO includes an employee for the NPPO or any officer delegated by the NPPO to perform its official functions."),)
    m_111 = models.NullBooleanField(_("21.4. Does the legislation identify as an offense breaking the seal on a sealed container containing plants, plant products or other regulated articles except in the presence of an inspector?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_112 = models.NullBooleanField(_("21.5. Does the legislation identify as an offense intentionally permitting or causing the introduction or spread of a pest?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_113 = models.NullBooleanField(_("21.6. Does the legislation identify as an offense failing to safeguard the phytosanitary security of a consignment after issuance of a phytosanitary certificate?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_114 = models.IntegerField(_("21.7. Does the legislation identify as an offense if committed by inspectors or other representatives of the NPPO:seizing plants or plant products for any reason other than that they are likely to introduce or spread a pest - disclosing to any other person any information acquired in the exercise of official functions under the legislation;-directly or indirectly asking for or taking any personal payment or other reward, or abstaining from doing an official action for improper reasons."), choices=THEM1, default=None,help_text=_(" "),)
    m_115 = models.NullBooleanField(_("21.8. Does the phytosanitary legislation include provisions for the seizure of plants, plant products and regulated articles where an offence has been committed, as well as anything else that may be have been used in the commission of an offence?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_116 = models.NullBooleanField(_("21.9. Is there provisions in the legislation for penalties to be updated and applied proportionally to the offence and according to a neutral economic parameter?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_117 = models.NullBooleanField(_("21.10. Does the legislation have a system of fixed penalties or 'spot fines,' which can be imposed immediately by inspectors according to the established procedures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_118 = models.NullBooleanField(_("21.11. Does the legislation include a system of administrative penalties (e.g. suspension of the operators register, or cancelling the accreditation as phytosanitary service provider)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_119 = models.NullBooleanField(_("22.1. Does the phytosanitary legislation specify the duty of other organizations and persons (e.g. customs, policy, etc) to cooperate with the NPPO, for the enforcement of the legislation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_120 = models.NullBooleanField(_("22.2. Does the legislation give the Phytosanitary Authority the power to issue and amend subsidiary instruments and thus to act upon new developments and as conditions change either within or outside the country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("For example where pest status has altered, and the phytosanitary requirements must change accordingly.  "),)
    m_121 = models.NullBooleanField(_("22.3. Does the legislation give the NPPO the power to establish and maintain its own internal operation manuals?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_122 = models.NullBooleanField(_("22.4. Does the legislation give the NPPO the power to establish and maintain registers of operators (importers, exporters, farmers, phytosanitary service providers)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_123
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_46= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_47= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_48= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_49= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_50= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_51= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_52= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_53= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_54= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_55= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_56= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_57= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_58= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_59= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_60= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_61= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_62= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_63= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_64= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_65= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_66= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_67= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_68= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_69= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_70= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_71= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_72= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_73= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_74= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_75= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_76= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_77= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_78= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_79= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_80= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_81= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_82= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_83= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_84= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_85= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_86= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_87= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_88= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_89= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_90= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_91= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_92= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_93= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_94= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_95= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_96= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_97= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_98= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_99= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_100= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_101= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_102= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_103= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_104= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_105= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_106= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_107= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_108= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_109= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_110= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_111= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_112= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_113= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_114= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_115= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_116= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_117= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_118= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_119= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_120= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_121= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_122= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_123= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');   
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module2, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})
                            
class Module2Weaknesses(models.Model):
    module2 = models.ForeignKey(Module2)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1       
    
    
class M3_1(models.Model):
    """ M3_1 """
    name = models.CharField(_("name"), max_length=500)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = _("Name")
    pass



class M3_10(models.Model):
    """ M3_10 """
    name = models.CharField(_("name"), max_length=500)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = _("Name")
    pass


class M3_17(models.Model):
    """ M3_1 """
    name = models.CharField(_("name"), max_length=500)
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = _("Name")
    pass
VAL_M3_3_0 = 0
VAL_M3_3_1 = 1
VAL_M3_3_2 = 2
VAL_M3_3_3 = 3
VAL_M3_3_4 = 4
VAL_M3_3_5 = 5
VAL_M3_3 = (
    (VAL_M3_3_0, _("--- Please select ---")),
    (VAL_M3_3_1, _("No involvement")),
    (VAL_M3_3_2, _("Partial involvement (provide comments)")),
    (VAL_M3_3_3, _("Consulted only on phytosanitary issues")),
    (VAL_M3_3_4, _("Consulted generally on all matters (as a partner)")),
    (VAL_M3_3_5, _("Active stakeholder in the process")),
   
)

VAL_M3_9_0 = 0
VAL_M3_9_1 = 1
VAL_M3_9_2 = 2
VAL_M3_9_3 = 3
VAL_M3_9_4 = 4
VAL_M3_9_5 = 5
VAL_M3_9 = (
    (VAL_M3_9_0, _("--- Please select ---")),
    (VAL_M3_9_1, _("absent from the process")),
    (VAL_M3_9_2, _("limited involvement")),
    (VAL_M3_9_3, _("mostly")),
    (VAL_M3_9_4, _("involved")),
    (VAL_M3_9_5, _("Highly involved")),
   
)
VAL_M3_14_0 = 0
VAL_M3_14_1 = 1
VAL_M3_14_2 = 2
VAL_M3_14_3 = 3
VAL_M3_14_4 = 4
VAL_M3_14_5 = 5
VAL_M3_14 = (
    (VAL_M3_14_0, _("--- Please select ---")),
    (VAL_M3_14_1, _("Severe limitations")),
    (VAL_M3_14_2, _("Limited")),
    (VAL_M3_14_3, _("Marginally adequate")),
    (VAL_M3_14_4, _("Good")),
    (VAL_M3_14_5, _("Excellent")),
   
)
VAL_M3_15_0 = 0
VAL_M3_15_1 = 1
VAL_M3_15_2 = 2
VAL_M3_15_3 = 3
VAL_M3_15_4 = 4
VAL_M3_15_5 = 5
VAL_M3_15 = (
    (VAL_M3_15_0, _("--- Please select ---")),
    (VAL_M3_15_1, _("Very")),
    (VAL_M3_15_2, _("High")),
    (VAL_M3_15_3, _("Medium")),
    (VAL_M3_15_4, _("Low")),
   
)

VAL_M3_16_0 = 0
VAL_M3_16_1 = 1
VAL_M3_16_2 = 2
VAL_M3_16_3 = 3
VAL_M3_16_4 = 4
VAL_M3_16_5 = 5
VAL_M3_16 = (
    (VAL_M3_16_0, _("--- Please select ---")),
    (VAL_M3_16_1, _("Not at all")),
    (VAL_M3_16_2, _("Very slightly")),
    (VAL_M3_16_3, _("Slightly")),
    (VAL_M3_16_4, _("Supportive")),
    (VAL_M3_16_5, _("Very supportive")),
   
)


class Module3(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 3 - Environmental forces assessment")
        verbose_name_plural = _("Module 3 - Environmental forces assessment")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.ManyToManyField(M3_1,verbose_name=_("1. What specifically characterizes the country's phytosanitary policy?"),blank=True, null=True,)
    m_2 = models.IntegerField(_("2. How much support is given to the agricultural and forestry sectors?"), choices=PRIORITY, default=None,help_text=_("Consider at least the aggregated financial, legislative and political aspects. "),)
    #m_3 = models.ManyToManyField(M3_3,verbose_name=_("3. How involved is the NPPO in national or sectoral policies?"), blank=True, null=True,)
    m_3 = models.IntegerField(_("3. How involved is the NPPO in national or sectoral policies?"), choices=VAL_M3_3, default=None,help_text=_(" "),)
    m_4 = models.NullBooleanField(_("4. Is there a written phytosanitary policy?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("List titles of any supporting documentation, e.g. National Phytosanitary Policy, etc. "),)
    #m_4_1 = models.TextField(_("4.1. List titles of any supporting documentation:"), blank=True, null=True,)
    m_5 = models.NullBooleanField(_("5. Have any relevant phytosanitary policy reviews been carried out within the last ten years?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>6.</b></i>"),)
    m_6 = models.TextField(_("5.1. What were the key recommendations?"), blank=True, null=True,)
    m_7 = models.TextField(_("5.2. What is the status of their implementation?"), blank=True, null=True,)
    m_8 = models.TextField(_("6. Which other agricultural related policies contain goals, objectives and priorities of phytosanitary relevance?"), blank=True, null=True,)
    #m_9 = models.ManyToManyField(M3_9,verbose_name=_("7. To what degree have stakeholders been involved in the formulation of phytosanitary aspects of agricultural policies."), blank=True, null=True,help_text=_("Includes phytosanitary policy and others with phytosanitary implications "))
    m_9 = models.IntegerField(_("7. To what degree have stakeholders been involved in the formulation of phytosanitary aspects of agricultural policies."), choices=VAL_M3_9, default=None,help_text=_("Includes phytosanitary policy and others with phytosanitary implications "),)
    m_10 = models.ManyToManyField(M3_10,verbose_name=_("8. How have they been involved?"), blank=True, null=True,help_text=_("E.g. as planners, implementers, enforcers, monitors, providers of funding, etc. "))
    m_11 = models.IntegerField(_("9. To what extent is the country's legislative system stable and functional?"), choices=STABLE, default=None,)
    m_12 = models.TextField(_("10. List the main laws relating to acceptable conditions of work and salary structures in the environment which directly affect the institution"), blank=True, null=True,)
    m_13 = models.IntegerField(_("11. Are the NPPO's conditions of service including salaries competitive to enable staff retention?"), choices=CONDITIONS, default=None,)
   # m_14 = models.ManyToManyField(M3_14,verbose_name=_("12. To what degree is he infrastructural environment supportive of the NPPOs ability to execute its mandate?"), blank=True, null=True,help_text=_("Consider infrastructure and equipment maintenance programmes, road systems, commuications systems, etc. "))
    #m_15 = models.ManyToManyField(M3_15,verbose_name=_("13. Are decisions about resource allocation heavily politicized?"), blank=True, null=True,help_text=_("Consider the degree to which the decisions concerning resource allocation to the agriculture and forestry sectors are politically influenced and affect the operation of the NPPO. "))
    m_14 = models.IntegerField(_("12. To what degree is he infrastructural environment supportive of the NPPOs ability to execute its mandate?"), choices=VAL_M3_14, default=None,help_text=_("Consider infrastructure and equipment maintenance programmes, road systems, commuications systems, etc. "),)
    m_15 = models.IntegerField(_("13. Are decisions about resource allocation heavily politicized?"), choices=VAL_M3_15, default=None,help_text=_("Consider the degree to which the decisions concerning resource allocation to the agriculture and forestry sectors are politically influenced and affect the operation of the NPPO. "),)
    #m_16 = models.ManyToManyField(M3_16,verbose_name=_("14. Is the national trade policy supportive of the improvement of the NPPOs performance?"), blank=True, null=True,)
    m_16 = models.IntegerField(_("14. Is the national trade policy supportive of the improvement of the NPPOs performance?"), choices=VAL_M3_16, default=None,help_text=_(" "),)
    m_17 = models.ManyToManyField(M3_17,verbose_name=_("15. Do the cultural aspects of the society support the NPPO's activities such as implementation of phytosanitary controls, pest eradication, etc?"), blank=True, null=True,)
    m_18 = models.IntegerField(_("16. Rate the country's human resource capacity to support the technical work of the NPPO."), choices=RATE, default=None,help_text=_("Consider the overall skills needed for core areas such as pest diagnostics, pest risk analysis etc. A more in-depth analysis will be done in corresponding PCE modules concerning core technical activities. "),)
    m_19 = models.IntegerField(_("17. Rate the educational programs capacity to provide the professional skills desired by the NPPO."), choices=RATE1, default=None,help_text=_("This question relates to the in-country educational system in terms of providing basic or advance training on phytosanitary issues, e.g. Agricultural colleges etc. "),)
    m_20 = models.IntegerField(_("18. Are the national research programs of the country supportive of the NPPOs functions?"), choices=SUPPORT, default=None,)
    m_21 = models.NullBooleanField(_("19. Do stakeholders provide feedback and make demands of the NPPO about its progress in carrying out its mission?"), choices=BOOL_CHOICES,blank=True, null=True,)
    m_22 = models.IntegerField(_("20. Do strategic decision makers in the NPPO take into account the specific demands that each stakeholder group is making on the organization?"), choices=PARTIAL, default=None,)
    m_23 = models.IntegerField(_("21. Rate the potential for constructive collaboration and other partnerships that might enhance the NPPOs output?"), choices=PRIORITY, default=None,help_text=_("For example with Universities or Research Centers... "),)
    m_24 = models.IntegerField(_("22. To what extent are networks and systems in place linking the NPPO to other organizations so as to enhance/support of the NPPO's services?"), choices=SERVICE, default=None,)
    m_25 = models.NullBooleanField(_("23. Is the country a member of the WTO?"), choices=BOOL_CHOICES,blank=True, null=True,)
    m_26 = models.NullBooleanField(_("24. Is the country a contracting party of the IPPC?"), choices=BOOL_CHOICES,blank=True, null=True,)
    m_27 = models.NullBooleanField(_("25. Is the country a signatory of the CBD?"), choices=BOOL_CHOICES,blank=True, null=True,)
    m_28 = models.NullBooleanField(_("26. Is the country a signatory of the Cartagena Protocol?"), choices=BOOL_CHOICES,blank=True, null=True,)
    m_29 = models.NullBooleanField(_("27. Is the country a member of any Regional Plant Protection Organization?"), choices=BOOL_CHOICES,blank=True, null=True,help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>28.</b></i>"))
    m_30 = models.TextField(_("27.1. If yes indicate the name(s)"), blank=True, null=True,)
    #m_31
    m_32 = models.TextField(_("28.1. Other"), blank=True, null=True,)
    #m_33
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
   
   
   
    def __unicode__(self):
        return self.title

 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module3, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})
class Module3Grid(models.Model):
    module3 = models.ForeignKey(Module3)
    verylow = models.BooleanField(verbose_name=_("Very low"), default=None) 
    low = models.BooleanField(verbose_name=_("Low"), default=None) 
    medium = models.BooleanField(verbose_name=_("Medium"), default=None) 
    high = models.BooleanField(verbose_name=_("High"), default=None) 
    veryhigh = models.BooleanField(verbose_name=_("Very high"), default=None) 
   
   
    def __unicode__(self):  
        return self.verylow
    def name(self):
        return self.verylow       
    
class Module3Weaknesses(models.Model):
    module3 = models.ForeignKey(Module3)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4= models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5= models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1
    
class Module4(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 4 - NPPO's mission and strategy")
        verbose_name_plural = _("Module 4 - NPPO's mission and strategy")
  
    session = models.ForeignKey(PceVersion)
    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    
    m_1 = models.IntegerField(_("1. To what degree does a formal mission statement exist which guides the NPPO's operational strategy?"), choices=STATEMENT, default=None,help_text=_("The mission statement is the written expression of the basic goals, characteristics, values, and philosophy that shape the organization and give it purpose. "),)
    m_2 = models.NullBooleanField(_("2. Is the mission linked to a set of goals and targets with clear indicators to measure progress?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_3 = models.IntegerField(_("3. How does the NPPO's mission and strategic directions relate to the IPPC's goals?"), choices=MODERATE, default=None,help_text=_(" "),)
    m_4 = models.IntegerField(_("4. Does NPPO Staff know what the mission is?"), choices=HQ, default=None,help_text=_(" "),)
    m_5 = models.IntegerField(_("5. Is there a process for clarifying and revising the NPPO's mission and beliefs, for working on its goals, and for understanding its stakeholders?"), choices=WRITTEN, default=None,help_text=_(" "),)
    m_6 = models.IntegerField(_("6. Is there a process for monitoring the NPPO's external environment in order to consider potential threats and opportunities?"), choices=WRITTEN, default=None,help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Does the NPPO's strategic plan identify the opportunities and constraints regarding core resource areas?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8 = models.IntegerField(_("8. What are the mechanisms for input by stakeholders into the development of strategic plans?"), choices=INPUTSTAKE, default=None,help_text=_("Stakeholders include industry groups, major importers, exporters etc."),)
    m_9 = models.NullBooleanField(_("9. Have the mission and goals been updated in recent years?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10 = models.IntegerField(_("10. How frequently are the NPPO's strategic plans reassessed?"), choices=TERM, default=None,help_text=_(" "),)
    m_11 = models.IntegerField(_("11. Is there a process for monitoring the implementation of the strategic plan?"), choices=WRITTEN, default=None,help_text=_(" "),)
    m_12 = models.IntegerField(_("12. Are the top level administrators (NPPO Managers) trained in organizational management including strategic management, financial management, human resource management etc?"), choices=THEM, default=None,help_text=_(" "),)
    m_13 = models.IntegerField(_("13. Has the strategy helped clarify priorities thus giving the NPPO a way to assess its performance?"), choices=DEGREE, default=None,help_text=_("Organization's performance is reflected in its effectiveness, efficiency, and sustainability. Effectiveness refers to the degree to which the organization achieves its goals. Efficiency refers to the degree it manages to minimizes costs. Sustainability refers to the organization's continuing relevance and the ability to acquire the financial and other resources needed for its operations. Strategic management is the deployment and implementation of the strategic plan and measurement and evaluation of the results.  "),)
    m_14 = models.NullBooleanField(_("14. Is the strategy an impediment to capacity-building or improved performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Strategic measures are operational definitions of the outcomes of mission effectiveness now and into the future. "),)
    m_15 = models.NullBooleanField(_("15. Has the NPPO a system of performance indicators?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Performance indicators are derived from the strategic measures "),)
    m_16 = models.NullBooleanField(_("16. Has the NPPO a system of organizational incentives including rewards and punishments, to encourage or discourage its staff member's behaviors?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.IntegerField(_("17. Does the NPPO provide the possibility for career advancement?"), choices=DEGREE, default=None,help_text=_(" "),)
    m_18 = models.NullBooleanField(_("18. Has the NPPO a strategy to execute core phytosanitary activities that includes the use of third parties in some NPPO's functions while maintaining the overall NPPO responsibility?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Use of third parties include sub-contracting some services to the private or governmental entities, approval or accreditation mechanisms, complete privatization  <br> <br> <br><i>If answer is <b>No</b> go to question <b>19.</b></i> "),)
    m_19 = models.NullBooleanField(_("18.1. Has the NPPO legal authority and clear rules and regulations in place for this purpose?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("19. Has the NPPO a strategy for the application of a cost recovery model?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("With dwindling financial resources in national budgets a number of plant protection/health services worldwide have explored and begun to apply cost recovery models to ensure that the programmes they implemnt are relevant and respond to the needs of their stakeholders. The fees charged however are based on the actual or real costs of the services provided. Cost recovery models adopted by NPPOs tend to be supplemented from the national budget to varying degrees depending on the services being charged. Few if any have 100% cost recovery programmes. Annex C 2F of the WTO-SPS agreement is generally adhered to when considering implementation of a cost recovery fee structure.  <br> <br> <br><i>If answer is <b>No</b> go to question <b>23.</b></i> "),)
    m_21 = models.NullBooleanField(_("20. Does the legal system allow the NPPO to apply, collect and keep fees for particular services?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_22 = models.NullBooleanField(_("21. Do all the stakeholders have the ability to pay fees?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_23 = models.NullBooleanField(_("22. Do the fees differ for different stakeholders according to their ability to pay?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_24 = models.NullBooleanField(_("23. Has the NPPO a strategy to improve core phytosanitary activities that include sharing infrastructure?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("For example, sharing of laboratories or inspection facilities or expertise. <br> <br> <br><i>If answer is <b>No</b> go to question <b>24.</b></i> "),)
    m_25 = models.TextField(_("23.1. If Yes, specify with whom"), blank=True, null=True,help_text=_(" "),)
    m_26 = models.NullBooleanField(_("24. Has the NPPO a strategy to improve core phytosanitary activities that include sharing information systems?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Such as might be the case with pest surveillance systems, etc.  <br> <br> <br><i>If answer is <b>No</b> go to question <b>25.</b></i> "),)
    m_27 = models.NullBooleanField(_("24.1. Have Inter-agency collaborative agreements been established specifying which information will be shared, what resources will be contributed, operational rules, users rights, etc?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_28 = models.TextField(_("24.2. If Yes, specify with which agencies and year of commencement"), blank=True, null=True,help_text=_(" "),)
    m_29 = models.NullBooleanField(_("24.3. Have compatible data systems been developed to this end?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_30 = models.NullBooleanField(_("25. Has the NPPO a strategy to improve core phytosanitary activities that includes the implementation of total quality assurance systems?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_31 = models.NullBooleanField(_("26. Has the NPPO an efficient written set of operational procedures or manuals?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>Section II.</b></i>  "),)
    m_32 = models.TextField(_("26.1. If Yes, provide the date and name of those manuals"), blank=True, null=True,help_text=_(" "),)
    m_33 = models.NullBooleanField(_("27. Does the operational procedure include internal technical audit procedures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_34
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module4, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
                            
class Module4Weaknesses(models.Model):
    module4 = models.ForeignKey(Module4)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1

class M5_3(models.Model):
    """ M3_1 """
    name = models.CharField(_("name"), max_length=500)

    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = _("Name")
    pass    
class Module5(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 5 - NPPO's structure and processes")
        verbose_name_plural = _("Module 5 - NPPO's structure and processes")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.IntegerField(_("1. How easy would it be for the NPPO to achieve its mission and goals within the current organizational structures?"),choices=ACHIEVE, default=None,help_text=_(" "),)
    m_2 = models.IntegerField(_("2. Is the structure of the NPPO based on the required institutional needs to carry out core phytosanitary activities such as surveillance, pest diagnosis, pest eradication, import verification, exports certification, pest risk analysis, risk communication, public awareness programs, international liaison activities, staff training etc?"),choices=CARRY_AC, default=None,help_text=_("Core phytosanitary activities, are outputs or functions that are carried out directly or supervised by the NPPO to support its mission/strategy"),)
    m_3 = models.ManyToManyField(M5_3,verbose_name=_("3. Does the NPPO have established a system for international liaison with:"), blank=True, null=True,help_text=_("Select all that apply."),)
    m_4 = models.NullBooleanField(_("4. Does the NPPO have a designated unit/manager responsible for progressing and/or supervising PRA?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Does the NPPO have a unit/manager responsible for pest surveillance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("6. Does the NPPO have a unit/manager responsible for pest diagnostic?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Does the NPPO have a unit/manager responsible for import verification?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8 = models.NullBooleanField(_("8. Does the NPPO have a unit/manager responsible for export certification activities including collection of import requirements of trade partners?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_9 = models.NullBooleanField(_("9. Does the NPPO have a unit/manager responsible for internal quarantine, pest control/eradication programs, and maintenance of pest free areas?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10 = models.NullBooleanField(_("10. Does the NPPO have a unit/manager responsible for strategic planning/management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11 = models.NullBooleanField(_("11. Does the NPPO have a unit/manager responsible to assist with managing contact with the news media and events which may impact on the general public?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_12 = models.NullBooleanField(_("12. Does the NPPO have a unit/manager responsible for staff training?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_13 = models.NullBooleanField(_("13. Does the NPPO have a unit/manager responsible for the technical audit program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_14 = models.NullBooleanField(_("14. Does the NPPO have a unit/manager responsible for performance assessment of the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_15 = models.NullBooleanField(_("15. Is there a person/unit assigned with the responsibility for the operational manual system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.IntegerField(_("16. Are roles within the organization clearly defined and flexible enough to adapt to changing needs?"),choices=DEFINED, default=None,help_text=_(" "),)
    m_17 = models.IntegerField(_("17. Are there clear lines of accountability (individual, group and organizational)?"),choices=CLEAR, default=None,help_text=_(" "),)
    m_18 = models.IntegerField(_("18. Does the NPPO structure allow for expediting the decision making and implementation process?"),choices=EXPEDI, default=None,help_text=_(" "),)
    m_19 = models.IntegerField(_("19. Does the NPPO structure have linkages that allow staff from different units to collaborate and share information easily?"),choices=LINKAGE, default=None,help_text=_(" "),)
    m_20 = models.IntegerField(_("20. To what extent does the NPPO implement a policy of participative management?"),choices=POLICY, default=None,help_text=_(" "),)
    m_21 = models.IntegerField(_("21. Has the NPPO a system of operational manuals covering the core activities?"),choices=THEM, default=None,help_text=_(" "),)
    m_22 = models.NullBooleanField(_("22. Is there a written procedure to develop and keep the operational manuals updated?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_23 = models.NullBooleanField(_("23. Is there an internal technical audit procedure in place to check and improve the quality of the core services provided by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_24 = models.NullBooleanField(_("24. Is there a requirement for regular external audits of the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
   #m_25
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
 
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module5, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
                            
class Module5Weaknesses(models.Model):
    module5 = models.ForeignKey(Module5)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1    
    
class Module6(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 6 - NPPO's Resourcess")
        verbose_name_plural = _("Module 6 - NPPO's Resources")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.NullBooleanField(_("1. Does the NPPO have sufficient financial resources for meeting its mission and goals?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>2.</b></i>  "),)
    m_2 = models.NullBooleanField(_("1.1. Does the NPPO have sufficient financial resources for meeting all of its fixed costs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Fixed costs are those expenses or costs that are unvarying. These include staff salaries, rental costs, lease etc.<br> <br> <br><i>If answer is <b>No</b> go to question <b>2.</b></i> "),)
    m_3 = models.NullBooleanField(_("1.2. Does the NPPO have sufficient financial resources for meeting all of its variable costs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Variable costs are those costs that vary with the change of volume of output. Also known as operating costs and may include labour costs, cost sof materials and supplies, fuel costs etc. <br> <br> <br><i>If answer is <b>Yes</b> go to question <b>3.</b></i>  "),)
    m_4 = models.IntegerField(_("2. If insufficient, approximately what percentage increase in the NPPO budget would be required?"),choices=BUDGET, default=None,help_text=_(" "),)
    m_5 = models.NullBooleanField(_("3. Does the NPPO have its own program of finance including planning; managing and monitoring expenditure, cash flow and budget; ensuring an accountable and auditable financial system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("4. Does the NPPO charge for the service it provides?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Some NPPO 's may charge for all or certain of its services such as issuing certificates, inspection activities etc.  <br> <br> <br><i>If answer is <b>No</b> go to question <b>6.</b></i> "),)
    m_7 = models.NullBooleanField(_("5. Are the charges levied on a cost recovery basis?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Cost recovery means to recover all of the costs associated with a programme or service to ensure long-term sustainability. These charges are calculated on level of inputs provided by NPPO staff as well as associated costs of the service such as materials and supplies used. "),)
    m_8 = models.IntegerField(_("6. What are the NPPOs funding sources for the regular budget?"),choices=FUNDING, default=None,help_text=_(" "),)
    m_9 = models.IntegerField(_("7. How does the NPPO acquire resources to invest in the improvement of phytosanitary services?"),choices=ACQUIRE, default=None,help_text=_(" "),)
    m_10 = models.NullBooleanField(_("8. Does the NPPO have written job descriptions for the functions, responsibilities and specific requirements for all of its staff?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11 = models.IntegerField(_("9. How adequately is the NPPO staffed to carry out all the required functions?"),choices=ADEQUATELY, default=None,help_text=_(" "),)
    m_12 = models.NullBooleanField(_("10. Does the NPPO have direct control over the appointment of staff?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_13 = models.IntegerField(_("11. How are the NPPO's staff appointed?"),choices=APPOINTED, default=None,help_text=_(" "),)
    m_14 = models.NullBooleanField(_("12. Does the NPPO have an HR strategy plan for staff development?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_15 = models.NullBooleanField(_("13. Is the promotion system for NPPO staff based primarily on performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.IntegerField(_("14. Rate the NPPO staff turnover per year?"),choices=TURNOVER, default=None,help_text=_(" "),)
    m_17 = models.TextField(_("14.1. If unacceptably high, state the main reasons for staff leaving in the comment box."), blank=True, null=True,help_text=_(" "),)
    m_18 = models.NullBooleanField(_("15. Do senior technical staff (e.g. entomologist) generally move to management positions primarily because of the level of remuneration (i.e. higher pay)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_19 = models.IntegerField(_("16. Does the NPPO have an on-going program for staff training to improve skills at various levels?"),choices=TRAINING, default=None,help_text=_("This applies to both management and technical areas and to training that is either external or internal. It is most important however that the training programme is an ongoing one.  "),)
    m_20 = models.NullBooleanField(_("17. Does the NPPOs have a partnership agreement with other NPPOs or Universities, for the professional development of staff?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("These agreeemnts can be at the local, regional or international levels. "),)
    m_21 = models.IntegerField(_("18. What proportion of the personnel is trained and qualified to carry out the functions of their position in the NPPO?"),choices=PROPORTION, default=None,help_text=_(" "),)
    m_22 = models.IntegerField(_("19. Rate the average level of communication skills of NPPO staff?"),choices=COMM_SKILLS, default=None,help_text=_("This refers to the skills needed to convey phytosanitary information to the general public, in the political areana and during discussions and negotiations concerning import / export issues in particular with phytosanitary officials in other countries (trading partners). "),)
    m_23 = models.IntegerField(_("20. Rate the average level of required linguistic skills of NPPO staff?"),choices=LANG_SKILLS, default=None,help_text=_("This includes language skills e.g. English/Spanish/French etc.) to discuss and negotiate import / export issues with phytosanitary officials in other countries (trading partners). "),)
    m_24 = models.IntegerField(_("21. Does the NPPO have the information management resources (hardware, software, communications and technical skills) to link the processes of core activities among the headquarters and regional offices?"),choices=RESOURCES, default=None,help_text=_(" "),)
    m_25 = models.IntegerField(_("22. Does the NPPO have a comprehensive record keeping and information retrieval system for all the core activities which enables it to provide appropriate information to relevant parties (e.g. commodities imported or exported, number of non-compliances, pest intercepted etc) on request?"),choices=RECORD, default=None,help_text=_(" "),)
    m_26 = models.NullBooleanField(_("23. Does the NPPO publish a summary of phytosanitary activities (e.g. annual report) for stakeholders?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_27 = models.IntegerField(_("24. What is the level of the NPPOs capacity to inform its stakeholders at the national and international levels, of its activities and other relevant phytosanitary issues in an effective and timely manner?"),choices=CAPACITY, default=None,help_text=_(" "),)
    m_28 = models.IntegerField(_("25. Does the NPPO's technical staff have good access to scientific and international sources of information?"),choices=ACCESS, default=None,help_text=_(" "),)
    m_29 = models.IntegerField(_("26. Rate the NPPO's headquarters building facilities:"),choices=BAD, default=None,help_text=_(" "),)
    m_30 = models.IntegerField(_("27. Rate the NPPO's regional offices building facilities:"),choices=BAD, default=None,help_text=_(" "),)
    m_31 = models.IntegerField(_("28. Rate the NPPOs infrastructure resources at border inspection points:"),choices=BAD, default=None,help_text=_(" "),)
    m_32 = models.IntegerField(_("29. Rate the NPPOs resources for telecommunications:"),choices=BAD, default=None,help_text=_(" "),)
    m_33 = models.IntegerField(_("30. Rate the NPPOs vehicle resources:"),choices=BAD, default=None,help_text=_(" "),)
    m_34 = models.IntegerField(_("31. Rate the NPPOs resources for office equipment (computer, printers, projectors, etc)"),choices=BAD, default=None,help_text=_(" "),)
    m_35 = models.IntegerField(_("32. Rate the NPPOs maintenance systems resources:"),choices=BAD, default=None,help_text=_(" "),)
    m_36 = models.IntegerField(_("33. Rate the NPPOs technical and scientific library resources:"),choices=BAD, default=None,help_text=_(" "),)
   #m_37
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module6, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    

class Module6Weaknesses(models.Model):
    module6 = models.ForeignKey(Module6)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1    
    
class Module7(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 7 - NPPO's structure and processes")
        verbose_name_plural = _("Module 7 - NPPO's structure and processes")
  
    session = models.ForeignKey(PceVersion)
    
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    
    m_1 = models.NullBooleanField(_("1. Is the mandate of the pest diagnostic laboratories consistent with the NPPO's mission?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_2 = models.NullBooleanField(_("2. Does the pest diagnostic laboratory have a strategic and operational plan?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_3 = models.NullBooleanField(_("3. Does the laboratory have a procedure to review its performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_4 = models.NullBooleanField(_("4. Is there a set of good indicators for measure the effectiveness of the pest diagnostic program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Is there a set of good indicators to measure the efficacy of the Pest diagnostic Program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6= models.TextField(_("6. What indicators could be used to measure the status of the pest diagnostic program's relevance to the NPPO's mission?"), blank=True, null=True,help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Is there a national manager responsible for the NPPO's pest diagnostic laboratories at national level?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8 = models.IntegerField(_("8. Are the pest diagnostic laboratories optimally situated across the country taking into account the geographic demand for laboratory services?"),choices=GEO, default=None,help_text=_(" "),)
    m_9 = models.NullBooleanField(_("9. Is there an organizational chart for the pest diagnostic laboratories?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10 = models.NullBooleanField(_("10. Are there written documents establishing the job description, mandates, functions and responsibilities of the pest diagnostic laboratory staff?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11= models.TextField(_("11. Which other laboratories carryout pest diagnostics in the country?"), blank=True, null=True,help_text=_(" "),)
    m_12 = models.IntegerField(_("12. How sufficient is the budget allocated to the NPPO laboratories?"),choices=SUFFICIENT, default=None,help_text=_("In considering whether the budget allocated to the laboratories is sufficient or not take into account the two dimensions of its financial operation, i.e. operational and fixed costs. Operational costs are those variable costs associated to the operation of the laboratory depending on the demands placed on its services by stakeholders. These may include costs for materials, reagents, supplies, labour (non-staff) etc. Fixed costs are those that do not vary significantly year on year and may include staff emoluments, lease, and other capital costs and assets."),)
    m_13 = models.NullBooleanField(_("13. Are the laboratory services provided based on a cost recovery policy?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_14
    m_15 = models.NullBooleanField(_("15. Are there efficient procedures to allow the purchase of specialized supplies, biological kits, primers and equipment spare parts, in the case their importation is required?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.NullBooleanField(_("16. Are there documented quality control procedures (e.g. to ISO 17, 025 or 9000 series standards) or good laboratory practices for laboratory operations of the NPPO's laboratory?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.NullBooleanField(_("17. Does the laboratory compare its performance/results with other pest diagnostic laboratories inside or outside the country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_18 = models.NullBooleanField(_("18. Is the NPPO's pest diagnostic laboratory approved or accredited by national or international bodies?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_19 = models.NullBooleanField(_("19. Has the quality system and validation work of the NPPO's pest diagnostic laboratory ever been assessed by an accredited agency, third party authority or one or more collaborating laboratories?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("20. Is there a regulatory framework or standards for the approval/accreditation of external (non-NPPO) laboratories from the public or private sector, as service providers, including audit protocols?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This may include national accreditation schemes not usually run by the NPPO such as those of the National Standards Body. In some instances NPPOs may accredit external (regional or international) reference laboratories to perform specific pest diagnostics. These cases may require specific legislative provisions and other procedures to be undertaken for accreditation and audits. "),)
    m_21 = models.NullBooleanField(_("21. Does the NPPO's laboratory cooperate through formal arrangements with other laboratories or institutions for routine diagnostics?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("NPPO laboratories may not have the capacity to conduct all the functions required for plant pest diagnostics. In some cases, such as where advanced molecular techniques are needed, and where the NPPO may not have the skills or the equipment to perform the test, it may rely on a partner institution to do so. The institution may be either public or private or may reside in the country or located in another country. Such routine work may require the shipment or transfer of a fixed or variable quantity of samples and a formal arrangement may be required to ensure that the time and resources are allocated by the collaborating laboratories or institution to perform the diagnosis on a regular basis. This may also be the case where the NPPOs own laboratories are not suitably situated geographically. <br> <br> <br><i>If answer is <b>No</b> go to question <b>23.</b></i> "),)
    m_22= models.TextField(_("22. If so, with which institutions, how and on what?"), blank=True, null=True,help_text=_(" "),)
    #m_23 matrix
    m_24 = models.IntegerField(_("24. Rate the NPPO's Pest diagnostic laboratory current human resources capacity in terms of qualifications and skills:"),choices=BAD1, default=None,help_text=_(" "),)
    m_25 = models.IntegerField(_("25. Rate the NPPO's Pest diagnostic laboratory current human resources in terms of numbers required to carry out its functions and activities:"),choices=INSUFF, default=None,help_text=_(" "),)
    m_26 = models.IntegerField(_("26. Are staff sufficiently qualified and trained to perform pest diagnostics and use relevant laboratory equipment, analytical methods, etc?"),choices=INSUFF1, default=None,help_text=_(" "),)
    m_27 = models.IntegerField(_("27. What types of relevant training have staff of the laboratory participated in during the last five years?"),choices=TRAINING1, default=None,help_text=_(" "),)
    m_28 = models.NullBooleanField(_("28. Are the laboratory managers trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_29 = models.NullBooleanField(_("29. Are there documented procedures for: sampling, sample delivery, intermediate storage and disposal?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_30= models.TextField(_("29.1. If not, identify the procedures or steps that are not documented."), blank=True, null=True,help_text=_(" "),)
    m_31 = models.NullBooleanField(_("30. Are all samples managed in accordance with those procedures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_32 = models.NullBooleanField(_("31. Does the laboratory provide collection kits for different types of specimens and samples?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_33 = models.NullBooleanField(_("32. Does the laboratory have a written description of its laboratory information management system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_34 = models.NullBooleanField(_("33. Is the reporting and information management system computerized?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_35 = models.NullBooleanField(_("34. Do analysts and managers in the laboratory have access to e-mail, and internet?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_36 = models.NullBooleanField(_("35. Are the methods and protocols for pest diagnostic documented in a form that is available to diagnosticians?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    # m_37 matrix
    m_38 = models.IntegerField(_("36.1. Use the information entered in the matrix to rate how well equipped are the NPPO's laboratories in terms of entomological equipment:"),choices=POOR, default=None,help_text=_(" "),)
    # m_39 matrix
    m_40 = models.IntegerField(_("37.1. Use the information entered in the matrix to rate how well equipped are the NPPO's laboratories in terms of virology equipment:"),choices=POOR, default=None,help_text=_(" "),)
    # m_41 matrix
    m_42 = models.IntegerField(_("38.1. Use the information entered in the matrix to rate how well equipped are the NPPO's laboratories in terms of mycology and bacteriology equipment:"),choices=POOR, default=None,help_text=_(" "),)
    # m_43 matrix
    m_44 = models.IntegerField(_("39.1. Use the information entered in the matrix to rate how well equipped are the NPPO's laboratories in terms of weed science equipment:"),choices=POOR, default=None,help_text=_(" "),)
    # m_45 matrix
    m_46 = models.IntegerField(_("40.1. Use the information entered in the matrix to rate how well equipped are the NPPO's laboratories in terms of nematology equipment:"),choices=POOR, default=None,help_text=_(" "),)
    m_47 = models.NullBooleanField(_("41. Does the laboratory maintain an inventory of its equipment?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_48 = models.NullBooleanField(_("42. Are instructions available for the use and maintenance of equipment?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This also applies to equipment lent to or outsourced from other laboratories or institutions "),)
    m_49 = models.IntegerField(_("43. Does the NPPO laboratory service/programme or system have its own capacity to maintain and/or outsource maintenance of all its specialised equipment?"),choices=EQUIP, default=None,help_text=_(" "),)
    m_50 = models.NullBooleanField(_("44. Are performance checks carried out regularly on equipment and instruments?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_51 = models.NullBooleanField(_("45. Are there any uncontrolled environmental or biological stresses on the laboratory?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" Stresses can include dust, temperature, wind, odors, etc "),)
    m_52 = models.NullBooleanField(_("46. Are there functional safety devices available in the laboratory(ies)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Examples of safety devices can include fume hoods, emergency showers, eye douche, fire extinguishers, fire blank, first aid kits, etc. "),)
    m_53 = models.IntegerField(_("47. Overall, considering the layout, size, age and structural conditions of the laboratory building(s), how conducive is it to fulfilling its mission?"),choices=CONDICIVE, default=None,help_text=_("Including testing areas and office space "),)
    m_54 = models.NullBooleanField(_("48. Is there currently adequate space for carrying out lab functions?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Functions can be associated to bench testing, equipment, administrative activities, general storage, reactive storage and glass wash among others. "),)
    m_55 = models.NullBooleanField(_("49. Is there a secure area, with appropriate environmental controls, for receipt and storage of samples and specimens?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_56 = models.NullBooleanField(_("50. Does the laboratory have an uninterruptible power supply (UPS)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_57 = models.NullBooleanField(_("51. Does the laboratory have an adequate and constant water supply system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_58 = models.NullBooleanField(_("52. Does the laboratory have adequate resources to respond to a pest outbreak?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Resources include staff, Scientific equipment, Communication equipment, supplies, etc. "),)
    m_59 = models.NullBooleanField(_("53. Do the NPPO's phytosanitary contingency plans take into account the required laboratory support?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>Section III.</b></i> "),)
    m_60 = models.NullBooleanField(_("54. Does the laboratory staff participate in the preparation of the NPPO's phytosanitary contingency plans?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_61 = models.IntegerField(_("1. How effective is the pest diagnostic service considering the NPPO's mission"),choices=WEAK, default=None,help_text=_(" "),)
    m_62 = models.NullBooleanField(_("2. Is there a set of good indicators for measuring the effectiveness of the pest diagnostic service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_63 = models.IntegerField(_("3. With what efficacy are the pest diagnostic service's resources utilized?"),choices=WEAK, default=None,help_text=_(" "),)
    m_64 = models.NullBooleanField(_("4. Is there a set of good indicators to measure the efficacy of the pest diagnostic service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_65 = models.IntegerField(_("5. With what efficacy are the pest diagnostic servie's resources utilized?"),choices=WEAK, default=None,help_text=_(" "),)
    m_66 = models.IntegerField(_("6. Has the pest diagnostic service kept its relevance over time?"),choices=WEAK1, default=None,help_text=_(" "),)
    m_67= models.TextField(_("7. What indicators could be used to measure the status or the pest diagnostic service's relevance?"), blank=True, null=True,help_text=_(" "),)
    m_68 = models.IntegerField(_("8. How well is the NPPO's pest diagnostic service performing?"),choices=WEAK2, default=None,help_text=_(" "),)
    #m_69
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_46= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_47= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_48= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_49= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_50= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_51= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_52= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_53= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_54= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_55= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_56= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_57= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_58= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_59= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_60= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_61= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_62= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_63= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_64= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_65= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_66= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_67= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_68= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_69= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
   
    def __unicode__(self):
        return self.title
 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module7, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
                            
class Module7Grid(models.Model):
    module7 = models.ForeignKey(Module7)
    salaries = models.CharField(_("Salaries"), blank=True, null=True, max_length=250,)
    equipment = models.CharField(_("Equipment"), blank=True, null=True, max_length=250,)
    supplies = models.CharField(_("Supplies"), blank=True, null=True, max_length=250,)
    materials = models.CharField(_("Materials"), blank=True, null=True, max_length=250,)
    fixedcosts = models.CharField(_("Other fixed costs"), blank=True, null=True, max_length=250,)
    operationalcosts = models.CharField(_("Other operational costs"), blank=True, null=True, max_length=250,)
    
    def __unicode__(self):  
        return self.salaries
    def name(self):
        return self.salaries  
    
class Module7Matrix23(models.Model):
    module7 = models.ForeignKey(Module7)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=None,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=None,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=None,help_text=_(" "),)
    averagelab = models.IntegerField(_("averagelab"),choices=VAL_AV, default=None,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    managers = models.IntegerField(_("managers"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff    
    
class Module7Matrix37(models.Model):
    module7 = models.ForeignKey(Module7)
    navailable = models.IntegerField(_("navailable"),choices=VAL, default=None,help_text=_(" "),)
    qaulity = models.IntegerField(_("qaulity"),choices=VAL, default=None,help_text=_(" "),)
    required = models.IntegerField(_("required"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
     
    def __unicode__(self):  
        return self.navailable
    def name(self):
        return self.navailable

class Module7Matrix39(models.Model):
    module7 = models.ForeignKey(Module7)
    navailable = models.IntegerField(_("navailable"),choices=VAL, default=None,help_text=_(" "),)
    qaulity = models.IntegerField(_("qaulity"),choices=VAL, default=None,help_text=_(" "),)
    required = models.IntegerField(_("required"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
     
    def __unicode__(self):  
        return self.navailable
    def name(self):
        return self.navailable    
    
class Module7Matrix41(models.Model):
    module7 = models.ForeignKey(Module7)
    navailable = models.IntegerField(_("navailable"),choices=VAL, default=None,help_text=_(" "),)
    qaulity = models.IntegerField(_("qaulity"),choices=VAL, default=None,help_text=_(" "),)
    required = models.IntegerField(_("required"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
     
    def __unicode__(self):  
        return self.navailable
    def name(self):
        return self.navailable   
class Module7Matrix43(models.Model):
    module7 = models.ForeignKey(Module7)
    navailable = models.IntegerField(_("navailable"),choices=VAL, default=None,help_text=_(" "),)
    qaulity = models.IntegerField(_("qaulity"),choices=VAL, default=None,help_text=_(" "),)
    required = models.IntegerField(_("required"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
     
    def __unicode__(self):  
        return self.navailable
    def name(self):
        return self.navailable   
class Module7Matrix45(models.Model):
    module7 = models.ForeignKey(Module7)
    navailable = models.IntegerField(_("navailable"),choices=VAL, default=None,help_text=_(" "),)
    qaulity = models.IntegerField(_("qaulity"),choices=VAL, default=None,help_text=_(" "),)
    required = models.IntegerField(_("required"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
     
    def __unicode__(self):  
        return self.navailable
    def name(self):
        return self.navailable          
class Module7Weaknesses(models.Model):
    module7 = models.ForeignKey(Module7)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1  
    
class M8_17(models.Model):
    """ M8_17 """
    name = models.CharField(_("name"), max_length=500)

    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = _("Name")
    pass 

class Module8(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 8 - NPPO pest surveillance and pest reporting capacity")
        verbose_name_plural = _("Module 8 - NPPO pest surveillance and pest reporting capacity")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.NullBooleanField(_("1. Does the NPPO conduct pest surveillance activities in a coordinated manner?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("It is recommended that NPPOs develop a system whereby appropriate information on the particular pest(s) of concern is collected, verified and compiled (<a href='https://www.ippc.int/en/publications/615/' target='_blank'>ISPM 6</a> Section 1.2). "),)
    m_2 = models.NullBooleanField(_("2. Are there written documents establishing the mandates, functions and responsibilities of the pest surveillance service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_3 =
    m_4 = models.NullBooleanField(_("4. Does the pest surveillance programme or service have a strategic and operational plan?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Does the pest surveillance programme or service have procedures to review its performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("6. Is there a set of good indicators for measure the effectiveness of the pest eradication program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Is there a set of good indicators to measure the efficacy of the pest eradication program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8= models.TextField(_("8. What indicators could be used to measure the status of the pest eradication program's relevance to the NPPO's mission?"), blank=True, null=True,help_text=_(" "),)
    m_9= models.TextField(_("9. Which organizations carryout pest surveillance in the country?"), blank=True, null=True,help_text=_(" "),)
    m_10 = models.NullBooleanField(_("10. Are the NPPO's pest surveillance functions centralized under a national manager?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11 = models.NullBooleanField(_("11. Does the NPPO have formal linkages with external sources (non-NPPO) of information on pest surveillance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_12 = models.NullBooleanField(_("12. Does the placement of pest surveillance activities within the NPPO structure make sense and facilitate the work?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_13 = models.NullBooleanField(_("13. Is there an organizational chart of the pest surveillance service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_14 = models.NullBooleanField(_("14. Does the NPPO engage relevant stakeholders to support and improve the quality of the pest surveillance service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>15.</b></i> "),)
    m_15= models.TextField(_("14.1. If so, with which stakeholders and how?"), blank=True, null=True,help_text=_(" "),)
    m_16 = models.NullBooleanField(_("15. Does the NPPO's pest surveillance programs have well developed and compatible data systems to collect, store and report pest surveillance information?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.ManyToManyField(M8_17,verbose_name=_("16. Is the surveillance responsibilities of the NPPO limited to quarantine pests, regulated non-quarantine pests, and/or regulated pests, or does it also include non-regulated pests of national concern?"), blank=True, null=True,help_text=_(" "),)
   #m_18 =
    m_19 = models.NullBooleanField(_("18. Is there a computerized retrieval system for this information in use by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("19. Are GIS coordinates used to specify the location of pests detected during pest surveys?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("GIS - geographic information system (GIS), or geographical information system: Any system that captures, stores, analyzes, manages, and presents data in relation to location (merges cartography and database technology). Coordinates are used in this context to refer to the system of marking geographical locations using a Geographic Positioning System (GPS) tool/device for use in GIS. "),)
    m_21 = models.NullBooleanField(_("20. Is there an NPPO's operational manual for general pest surveillance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_22 = models.NullBooleanField(_("21. Is there a national database of plant pest records?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("This a general/comprehensive list of pests and not a regulated pest list. <br> <br> <br><i>If answer is <b>No</b> go to question <b>25.</b></i> "),)
    m_23 = models.NullBooleanField(_("22. Are databases of plant pest records easily accessible by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_24 = models.IntegerField(_("23. What proportion of the records can be verified from insect or culture collections?"),choices=RANGE1, default=None,help_text=_(" "),)
    m_25= models.TextField(_("24. Indicate the information sources from which plant pest records have been compiled."), blank=True, null=True,help_text=_("These sources may include: NPPOs, other national and local government agencies, research institutions, universities, scientific societies (including amateur specialists), producers, consultants, museums, the general public, scientific and trade journals, unpublished data and contemporary observations. In addition, the NPPO may obtain information from international sources such as FAO, Regional Plant Protection Organizations (RPPOs), etc. "),)
    #m_26= models.TextField(_("25. How many plant species or plant products grown in the country are officially surveyed for pests on a regular basis?"), blank=True, null=True,help_text=_("These are official surveys and should follow a plan which is approved by the NPPO. See <a href='https://www.ippc.int/en/publications/615/' target='_blank'>ISPM 6</a>, Section 2."),)
    m_26 = models.IntegerField(_("25. How many plant species or plant products grown in the country are officially surveyed for pests on a regular basis?"),choices=NUMPLANT, default=None,help_text=_("These are official surveys and should follow a plan which is approved by the NPPO. See <a href='https://www.ippc.int/en/publications/615/' target='_blank'>ISPM 6</a>, Section 2."),)
    m_27= models.TextField(_("26. List the plant species using scientific names (genus and species) in the comment box."), blank=True, null=True,help_text=_(" "),)
    m_28 = models.NullBooleanField(_("27. Are the specific pest surveys procedures described in an operational manual?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_29 = models.NullBooleanField(_("28. Are the performance, efficiency, efficacy and relevance of those plans periodically evaluated?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
   #m_30 =
    m_31 = models.IntegerField(_("30. Rate NPPO's pest surveillance program current human resources capacity in terms of numbers:"),choices=WEAK3, default=None,help_text=_("What is the NPPO's pest surveillance program current human resource capacity in terms of numbers? "),)
    m_32 = models.IntegerField(_("31. Rate NPPO's pest surveillance program current human resources capacity in terms of qualifications and skills:"),choices=WEAK3, default=None,help_text=_(" "),)
    m_33 = models.IntegerField(_("32. Are those human resources sufficient to carry out the activities according to the NPPO's requirements for pest surveillance?"),choices=INSUFF3, default=None,help_text=_(" "),)
    m_34 = models.IntegerField(_("33. What proportion of the staff assigned to carry out pest surveillance have been specifically trained to do so?"),choices=PERC0, default=None,help_text=_("Tasks associated with pest surveillance include sampling, collecting specimens, preservation techniques, and record keeping. "),)
    m_35 = models.IntegerField(_("34. How frequent are training programs for staff involved in pest surveillance?"),choices=PROGRAMMED, default=None,help_text=_("Tasks associated with pest surveillance include sampling, collecting specimens, preservation techniques, and record keeping. "),)
    m_36 = models.NullBooleanField(_("35. Is the pest surveillance manager trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_37 = models.IntegerField(_("36. Rate the sufficiency of other resources (vehicles, traps, lures, samplers, GPS, etc) required to operate the pest surveillance program:"),choices=NOTATALL1, default=None,help_text=_(" "),)
    m_38 = models.IntegerField(_("1. How effective is the pest surveillance service considering the NPPO's mission?"),choices=WEAK, default=None,help_text=_(" "),)
    m_39 = models.NullBooleanField(_("2. Is there a set of good indicators for measuring the effectiveness of the pest surveillance service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_40 = models.IntegerField(_("3. With what efficacy are the pest surveillance service's resources utilized?"),choices=WEAK, default=None,help_text=_(" "),)
    m_41 = models.NullBooleanField(_("4. Is there a set of good indicators for measuring the efficacy of the pest surveillance service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_42 = models.IntegerField(_("5. Has the pest surveillance service kept its relevance over time?"),choices=NOTATALL, default=None,help_text=_(" "),)
    m_43= models.TextField(_("6. What indicators could be used to measure the status or the pest surveillance service's relevance?"), blank=True, null=True,help_text=_(" "),)
    m_44 = models.IntegerField(_("7. How well is the NPPO's pest surveillance service performing?"),choices=WEAK4, default=None,help_text=_(" "),)
    #m_45
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module8, self).save(*args, **kwargs)
    
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
                            
                            
class Module8Grid3(models.Model):
    module8 = models.ForeignKey(Module8)
    c1 = models.NullBooleanField(_("Specific so that they are clear and easy to understand?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Measurable and able to be quantified so that is possible to measure progress?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Achievable and realistic given the circumstances in which they are set and the resources available?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Relevant to the country's needs and to the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Time bound with realistic deadlines for achievement"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
  
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  

class Module8Grid18(models.Model):
    module8 = models.ForeignKey(Module8)
    c1 = models.NullBooleanField(_("Scientific name of pest"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Scientific name of host,plant part affected and means of collection"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Date and name of collector"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Date and name of identifier"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Date and name of verifier"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c6 = models.NullBooleanField(_("Geographical location"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
  
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
    
        
class Module8Matrix30(models.Model):
    module8 = models.ForeignKey(Module8)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=VAL_0,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=VAL_AV_0,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=VAL_0,help_text=_(" "),)
    averagelab = models.IntegerField(_("averagelab"),choices=VAL_AV, default=VAL_AV_0,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    managers = models.IntegerField(_("managers"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff     
    
class Module8Weaknesses(models.Model):
    module8 = models.ForeignKey(Module8)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1        
                            
class Module9(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 9- Pest eradication capacity")
        verbose_name_plural = _("Module 9- Pest eradication capacity")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    #m_1 =
    m_2 = models.NullBooleanField(_("2. Is the mandate of the pest eradication programme or service consistent with the NPPO's mission?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_3 = models.NullBooleanField(_("3. Does the NPPO conduct pest eradication activities in a coordinated manner?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_4 = models.NullBooleanField(_("4. Are there written documents establishing the mandates, functions and responsibilities of the pest eradication programme or service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_5 =
    m_6 = models.NullBooleanField(_("6. Does the pest eradication program have a strategic and operational plan?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Does the pest eradication program have procedures to review its performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8 = models.NullBooleanField(_("8. Is there a set of good indicators for measure the effectiveness of the pest eradication program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_9 = models.NullBooleanField(_("9. Is there a set of good indicators to measure the efficacy of the pest eradication program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10= models.TextField(_("10. What indicators could be used to measure the status of the pest eradication program 's relevance to the NPPO's mission?"), blank=True, null=True,help_text=_(" "),)
    m_11 = models.NullBooleanField(_("11. Does the national legislation provide for emergency action following the introduction of a quarantine pest?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_12 = models.NullBooleanField(_("12. Does the national legislation provide a mechanism for obtaining emergency funds for pest eradication?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_13 = models.NullBooleanField(_("13. Does the legislation contain provisions for economic compensation to the owners affected by eradication?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_14 = models.NullBooleanField(_("14. Are the NPPO's pest eradication activities centralized under a national manager?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_15 = models.NullBooleanField(_("15. Is there a management team established to provide direction and co-ordination to pest eradication activities?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>17.</b></i>  "),)
    m_16 = models.NullBooleanField(_("16. Does the management team have written responsibilities to carry out its functions effectively and in accordance with the International Standard"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.NullBooleanField(_("17. Does the placement of the pest eradication activities within the NPPO structure make sense and facilitate the work?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_18 = models.NullBooleanField(_("18. Is there an organizational chart of the pest eradication program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_19 = models.NullBooleanField(_("19. Are there job descriptions establishing the mandates, functions and responsibilities of the Pest eradication staff?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("20. Does the NPPO engage relevant stakeholders to support and improve the quality of the pest eradication programme?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>22.</b></i>  "),)
    m_21= models.TextField(_("21. If so, with which stakeholders and how?"), blank=True, null=True,help_text=_(" "),)
    m_22 = models.NullBooleanField(_("22. Is there an operational manual or a set of guidelines for pest eradication?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>26.</b></i> "),)
    m_23 = models.NullBooleanField(_("23. If yes, are the national guidelines for pest eradication consistent with the international standard?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_24= models.TextField(_("24. List the pests for which national standards or guidelines for pest eradication have been developed?"), blank=True, null=True,help_text=_(" "),)
    m_25= models.TextField(_("25. List the pests for which national standards or guidelines for pest eradication are currently being conducted?"), blank=True, null=True,help_text=_(" "),)
    m_26 = models.NullBooleanField(_("26. Are GIS coordinates used to specify the location of pests detected during pest eradication?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("GIS - geographic information system (GIS), or geographical information system: Any system that captures, stores, analyzes, manages, and presents data in relation to location (merges cartography and database technology). Coordinates are used in this context to refer to the system of marking geographical locations using a Geographic Positioning System (GPS) tool/device for use in GIS. "),)
    m_27 = models.NullBooleanField(_("27. Does the NPPO's pest eradication programs have well developed and compatible data systems to collect, store and report pest distribution and eradication information?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_28 = models.NullBooleanField(_("28. Does the NPPO have contingency plans to address specific pests or pest groups that have a high potential for introduction, and for which an eradication plan is deemed to be both feasible and necessary, before the pest is found in an area."), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>30.</b></i>  "),)
    m_29 = models.NullBooleanField(_("29. Do the contingency plans identify the stakeholders that must be involved in case of an emergency, and its roles and responsibilities?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_30 = models.NullBooleanField(_("30. Are the responsibilities and roles of other NPPO's programs considered and incorporated in the eradication plans?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("Other relevant NPPO programmes or elements that could impact on the efficiency and effectiveness of the pest eradication programme or plans could include pest diagnostic, surveillance, internal quarantine, and human resources such as phytosanitary inspectors. "),)
    #m_31 =
    m_32 = models.NullBooleanField(_("32. Is the efficiency, efficacy and relevance of those plans periodically evaluated?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_33 = models.NullBooleanField(_("33. Can resources be quickly deployed to undertake pest eradication activities if outbreaks occur?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_34 = models.NullBooleanField(_("34. Are there qualified staff available to assess the feasibility of an appropriate eradication program (including cost/benefit analysis)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_35
    m_36 = models.IntegerField(_("36. Rate the current NPPO pest eradication program's current human resources capacity in terms of numbers:"),choices=WEAK, default=None,help_text=_(" "),)
    m_37 = models.IntegerField(_("37. Rate the current NPPO pest eradiciation program's current human resources capacity in terms of qualifications and skills:"),choices=INSUFF1, default=None,help_text=_(" "),)
    m_38 = models.IntegerField(_("38. Are those human resources sufficient to carry out the activities according to the NPPO's requirements for pest eradication?"),choices=INSUFF4, default=None,help_text=_(" "),)
    m_39 = models.IntegerField(_("39. How many people have been specifically trained to carry out pest eradication?"),choices=PERC2, default=None,help_text=_(" "),)
    m_40 = models.IntegerField(_("40. How frequent are training programs for staff involved in pest eradication?"),choices=TRAIN, default=None,help_text=_(" "),)
    m_41 = models.NullBooleanField(_("41. Are the pest eradication program managers trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_42 = models.IntegerField(_("42. Rate the sufficiency of the equipment, materials and transport used in the NPPO's eradication program:"),choices=SUFF1, default=None,help_text=_(" "),)
    m_43 = models.IntegerField(_("1. How effective is the pest eradication service in moving to the NPPO's mission"),choices=WEAK5, default=None,help_text=_(" "),)
    m_44 = models.IntegerField(_("2. How efficient are the pest eradication resources utilized?"),choices=NOTATALL3, default=None,help_text=_(" "),)
    m_45 = models.IntegerField(_("3. Has the pest eradication service kept its relevance over time?"),choices=NOTATALL2, default=None,help_text=_(" "),)
    m_46 = models.IntegerField(_("4. How well is the NPPO's pest eradication service performing?"),choices=WEAK5, default=None,help_text=_(" "),)
   #m_47 =
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_46= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_47= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module9, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})   
                            
class Module9Grid1(models.Model):
    module9 = models.ForeignKey(Module9)
    c1 = models.NullBooleanField(_("What is the purpose of pest eradication?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("What the pest eradication program seeks to accomplish?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("What services are performed in order to accomplish this purpose?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("What principles (e.g. risk based, science based) and values (e.g. honesty, integrity, technical independence) guide the work of pest eradication program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
  
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
class Module9Grid5(models.Model):
    module9 = models.ForeignKey(Module9)
    c1 = models.NullBooleanField(_("Specific so that they are clear and easy to understand?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Measurable and able to be quantified so that is possible to measure progress?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Achievable and realistic given the circumstances in which they are set and the resources available?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Relevant to the country's needs and to the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Time bound with realistic deadlines for achievement"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
  
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
class Module9Grid31(models.Model):
    module9 = models.ForeignKey(Module9)
    c1 = models.NullBooleanField(_("Surveillance: to fully investigate the distribution of the pest?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Containment: to prevent the spread of the pest?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Treatment: to eradicate the pest when it is found?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Verification of eradication"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Declaration of eradication"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
  
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  

class Module9Matrix35(models.Model):
    module9 = models.ForeignKey(Module9)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=None,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=None,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=None,help_text=_(" "),)
    averagelab = models.IntegerField(_("averagelab"),choices=VAL_AV, default=None,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    managers = models.IntegerField(_("managers"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff    

class Module9Weaknesses(models.Model):
    module9 = models.ForeignKey(Module9)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1   
    
  
class Module10(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 10 - Phytosanitary import regulatory system")
        verbose_name_plural = _("Module 10 - Phytosanitary import regulatory system")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.NullBooleanField(_("1. Does the legislation grant authority to the NPPO's inspectors to enter premises, conveyances, and other places where imported commodities, regulated pests or other regulated articles may be present?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_2 = models.NullBooleanField(_("2. Does the legislation grant authority to the NPPO's inspectors to inspect or test imported commodities and other regulated articles?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_3 = models.NullBooleanField(_("3. Does the legislation grant authority to the NPPO's inspectors to take and remove samples from imported commodities or other regulated articles, or from places where regulated pest may be present (including for analysis which may result in the destruction of the sample)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_4 = models.NullBooleanField(_("4. Does the legislation grant authority to the NPPO's inspectors to detain imported consignments or other regulated articles?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Does the legislation grant authority to the NPPO's inspectors to treat or require treatment of imported consignments or other regulated articles including conveyances, or refuse the entry of consignments, order their reshipment or destruction?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("6. Does the legislation grant authority to take emergency action?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Does the legislation grant authority to the NPPO's inspectors to set and collect fees for import-related activities or associated with penalties?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8 = models.NullBooleanField(_("8. Is the NPPO the sole official service responsible for the operation and/or organization and management of the phytosanitary import regulatory system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>Yes</b> go to question <b>9.</b></i> "),)
    m_9= models.TextField(_("8.1. If not, clearly identify who performs this function and how it is conducted."), blank=True, null=True,help_text=_(" "),)
    m_10 = models.NullBooleanField(_("9. Are there other public or private services or agencies cooperating with the NPPO in the phytosanitary control of imported commodities?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>13.</b></i>  "),)
    m_11 = models.NullBooleanField(_("10. Are the roles of those public or private services or agencies clearly specified with distinct separation of responsibilities and functions?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_12 = models.NullBooleanField(_("11. Are effective liaison mechanisms with those public or private services or agencies clearly identified?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_13 = models.NullBooleanField(_("12. Does the NPPO have procedures to facilitate cooperation, information sharing and joint clearance activities with other relevant public or private services or agencies as appropriate?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_14 = models.NullBooleanField(_("13. Is the import regulatory system in conformity with the rights, obligations and responsibilities arising from relevant international treaties, conventions or agreements?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_15 = models.NullBooleanField(_("14. In particular, is the import regulatory system in conformity with the basic and operational principles as established by <a href='https://www.ippc.int/en/publications/596/' target='_blank'>ISPM 1</a>?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.NullBooleanField(_("15. Is the import regulatory system in conformity with national legislation and policies?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.NullBooleanField(_("16. Is the import regulatory system harmonized at the regional level?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_18 = models.NullBooleanField(_("17. Does the NPPO have the authority and procedures to require import phytosanitary measures, to imported plants, plant products and other regulated articles including means of conveyance, wood packaging materials, etc?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_19 = models.NullBooleanField(_("18. Does the import regulatory system use transparent and defined procedures with specified time frames for the implementation of regulations, including their entry into force?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("19. Do the import regulatory system procedures or regulations specify that phytosanitary measures can not be applied to non regulated pests?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_21 = models.NullBooleanField(_("20. Does the import regulatory system indicate that plant or plant products destined for consumption cannot be regulated as regulated non-quarantine pests?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_22 = models.NullBooleanField(_("21. Does the import regulatory system specify that the list of regulated pest shall be made publicly available and kept updated?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
 # m_23
    m_24 = models.NullBooleanField(_("23. Does the import regulatory system cover consignments in transit and allows the NPPO to adopt technically justified measures as indicated in <a href='https://www.ippc.int/en/publications/595/' target='_blank'>ISPM 25</a>?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_25 = models.NullBooleanField(_("24. Does the import regulatory system include provisions for action to be taken in the case of non-compliance or for emergency action as specified in <a href='https://www.ippc.int/en/publications/608/' target='_blank'>ISPM 13</a>?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_26 = models.NullBooleanField(_("25. Does the import regulatory system include provisions for revision of regulations and documentation?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_27 = models.NullBooleanField(_("26. Is there a national manager responsible for the operation and/or oversight (organization and management) of the import regulatory system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_28 = models.NullBooleanField(_("27. Does the import regulatory staff have written job descriptions to carry out its function effectively and in accordance with <a href='https://www.ippc.int/en/publications/602/' target='_blank'>ISPM 20</a> Sec 5.and other relevant ISPMs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_29 = models.NullBooleanField(_("28. Does the NPPO's import regulatory system structure make organizational sense and facilitate the work?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_30 = models.NullBooleanField(_("29. Is there an organizational chart linking the elements of the import regulatory system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
 # m_31
    m_32 = models.NullBooleanField(_("31. Are NPPO's phytosanitary service providers who have been approved/or accredited by the NPPO involved in the import process?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>32.</b></i> "),)
  # m_33
    m_34 = models.NullBooleanField(_("32. Does the NPPO have a management system for the development, maintenance and revision of the import regulatory system and the phytosanitary regulations?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_35 = models.NullBooleanField(_("33. Is there a written procedure for making available and keeping updated lists of regulated pests, as per <a href='https://www.ippc.int/en/publications/603/' target='_blank'>ISPM 19</a>?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_36 = models.NullBooleanField(_("34. Does the import regulatory system provide for the NPPO to audit the relevant components of the export certification system in the country of origin?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("The relevant components may include production systems, treatments, inspection procedures, phytosanitary management, accreditation procedures, testing, surveillance, etc. "),)
 # m_37
    m_38 = models.NullBooleanField(_("36. Does the NPPO have written procedures for reporting the interception, instances of non-compliance and emergency actions?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_39 = models.NullBooleanField(_("37. Does the NPPO have written procedures to promptly notify concerned exporting countries about any changes in the phytosanitary regulations or emergency or provisional measures that change the entry procedures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_40 = models.NullBooleanField(_("38. Does the NPPO have written procedures for the authorization under NPPO's control and responsibility, of organizations, agencies or persons to act on its behalf for certain defined functions?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_41 = models.NullBooleanField(_("38.1. Do those written procedures include also provisions for the demonstration and audits, corrective actions, system review and withdrawal of authorizations?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_42 = models.NullBooleanField(_("39. Has the NPPO established mechanisms for the dissemination of the phytosanitary regulations, electronically?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_43 = models.NullBooleanField(_("40. Does the NPPO have written procedures to review cases of non-compliance and emergency action?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_44 = models.NullBooleanField(_("41. In cases of non-compliance of imports, does the NPPO have written procedures for consultation, exchange of information and dispute settlement, with other NPPOs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    # m_45
    # m_46 
    # m_47 matrix
    m_48 = models.IntegerField(_("45. Rate the NPPO's import regulatory system current human resources capacity in terms of numbers"),choices=INSUFF5, default=None,help_text=_(" "),)
    m_49 = models.IntegerField(_("46. Rate the NPPO's import regulatory system current human resources capacity in terms of qualifications and skills"),choices=INSUFF5, default=None,help_text=_(" "),)
    m_50 = models.NullBooleanField(_("47. Do the inspection regulatory system personnel receive adequate training to ensure competency in their areas of responsibilities?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_51 = models.IntegerField(_("48. How frequent are training programs for staff involved in the import regulatory system?"),choices=TRAIN2, default=None,help_text=_(" "),)
    m_52 = models.NullBooleanField(_("49. Are the import regulatory system's managers trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_53 = models.IntegerField(_("50. Assess the availability of equipment and transport in the NPPO's import regulatory system"),choices=INSUFF6, default=None,help_text=_(" "),)
    m_54 = models.IntegerField(_("51. Assess the availability of communications equipment in the NPPO's import regulatory system"),choices=INSUFF6, default=None,help_text=_(" "),)
    m_55 = models.IntegerField(_("52. Assess the availability of adequate office and inspection facilities in the NPPO's import regulatory system"),choices=INSUFF6, default=None,help_text=_(" "),)
    m_56 = models.IntegerField(_("53. Assess the availability of adequate computers and tailored software in the NPPO's import regulatory system"),choices=INSUFF6, default=None,help_text=_(" "),)
    m_57 = models.IntegerField(_("1. How effective is the import regulatory system in consideration of the NPPO's mission"),choices=EFF, default=None,help_text=_(" "),)
    m_58 = models.IntegerField(_("2. With what efficacy are the import regulatory system's resources utilized?"),choices=EFF, default=None,help_text=_(" "),)
    m_59 = models.IntegerField(_("3. With what efficacy are the import regulatory system's resources utilized?"),choices=CAPACITY, default=None,help_text=_(" "),)
    m_60 = models.IntegerField(_("4. How well is the NPPO's import regulatory system performing?"),choices=BAD, default=None,help_text=_(" "),)
   #61
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_46= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_47= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_48= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_49= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_50= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_51= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_52= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_53= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_54= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_55= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_56= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_57= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_58= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_59= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_60= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_61= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module10, self).save(*args, **kwargs)
    
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
class Module10Grid23(models.Model):
    module10 = models.ForeignKey(Module10)
    c1 = models.NullBooleanField(_("Import permits?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Limitations on the points of entry?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("The requirement that importer notify in advance the arrival of consignments?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Audit of procedures in the exporting country?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Pre-clearance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
    
class Module10Grid31(models.Model):
    module10 = models.ForeignKey(Module10)
    c1 = models.NullBooleanField(_("Import phytosanitary requirements?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Pest status and geographical distribution?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Operational procedures"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
class Module10Grid33(models.Model):
    module10 = models.ForeignKey(Module10)
    c1 = models.NullBooleanField(_("Pest diagnostic"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Inspection and detention facilities"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Treatment"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Pre-clearance"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
class Module10Grid37(models.Model):
    module10 = models.ForeignKey(Module10)
    c1 = models.NullBooleanField(_("Documentary checks"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Consignment identity checks"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Phytosanitary inspection"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Sampling"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Testing"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c6 = models.NullBooleanField(_("Instances of non-compliance"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c7 = models.NullBooleanField(_("Action in case of non compliance"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c8 = models.NullBooleanField(_("Emergency actions"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
class Module10Grid45(models.Model):
    module10 = models.ForeignKey(Module10)
    c1 = models.NullBooleanField(_("Non-compliance and emergency actions?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Consignments with specific end-uses?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Consignments subject to post-entry quarantine or treatments?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Consignments requiring follow up action (including trace back)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Other records as necessary to manage the import regulatory traceability system"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
class Module10Grid46(models.Model):
    module10 = models.ForeignKey(Module10)
    c1 = models.NullBooleanField(_("Monitoring the effectiveness of phytosanitary measures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Internal audit of the NPPO activities and authorized organizations or persons?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Modifying the phytosanitary legislation, regulation and procedures"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
    
class Module10Matrix_47(models.Model):
    module10 = models.ForeignKey(Module10)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=None,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=None,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=None,help_text=_(" "),)
    averagelab = models.IntegerField(_("averagelab"),choices=VAL_AV, default=None,help_text=_(" "),)
    supstafflab = models.IntegerField(_("supnstafflab"),choices=VAL, default=None,help_text=_(" "),)
    technical = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    managers = models.IntegerField(_("managers"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff    

class Module10Weaknesses(models.Model):
    module10 = models.ForeignKey(Module10)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1   

class Module11(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 11 - Pest risk analysis")
        verbose_name_plural = _("Module 11 - Pest risk analysis")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.NullBooleanField(_("1. Is there a mission statement specifying that all the NPPO's phytosanitary measures shall be technically justified?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>3.</b></i> "),)
    #m_2  
    #m_3   
    m_4 = models.NullBooleanField(_("4. Does the PRA unit have a strategic and operational plan?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Is there a set of good indicators for measuring the effectiveness of the PRA programme?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("6. Is there a set of good indicators for measuring the efficacy of the PRA programme?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7= models.TextField(_("7. What indicators could be used for measuring the status of the PRA programme's relevance?"), blank=True, null=True,help_text=_(" "),)
    m_8 = models.NullBooleanField(_("8. Does the PRA unit have procedures to review its performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_9 = models.NullBooleanField(_("9. Does the NPPO have the mandate by legislative or administrative means to technically justify all the phytosanitary measures adopted by the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10 = models.NullBooleanField(_("10. Does the NPPO have the authority to approve/ accredit/ contract phytosanitary service providers from the official or private sectors to collaborate in some of the PRA stages?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11 = models.NullBooleanField(_("11. Does the legislation allow the NPPO to charge fees for the PRAs performed?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_12 
    m_13 = models.NullBooleanField(_("13. Does the legislation grant regulatory powers to the NPPO to directly adopt the import phytosanitary measures/requirements as far as they are based on PRA, and are consistent with the relevant international agreements and ISPMs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
   #m_14
    m_15 = models.NullBooleanField(_("15. Does the legislation require that prior to their adoption, the proposed mitigation measures and uncertainties shall be communicated to stakeholders and other interested parties, including other contracting parties, RPPOs and NPPOs, as appropriate?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.NullBooleanField(_("16. Does the legislation require that the adopted phytosanitary requirements, restrictions or prohibitions, shall be immediately published and transmitted to contracting parties that NPPO believes may be directly affected? (according to IPPC Article VII.2b)"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.NullBooleanField(_("17. Does the legislation require the importer to request a Phytosanitary Import Permit, in order to allow the NPPO to establish the phytosanitary measures in advance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>19.</b></i> "),)
    m_18 = models.NullBooleanField(_("18. If yes, does the legislation grant authority to reject consignments arriving without a phytosanitary import permit if required?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_19 = models.NullBooleanField(_("19. Can the recommendations of a PRA conducted on technical grounds be over-ruled by the government because of other than technical considerations?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("20. Does the legislation establish the NPPO obligation to promptly review the PRA, when there is new relevant information available?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_21 = models.IntegerField(_("21. Is PRA performed by the NPPO or outsourced?"),choices=OUT, default=None,help_text=_(" "),)
    m_22 = models.NullBooleanField(_("22. Is there a national manager/unit responsible for the PRA process?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_23 = models.NullBooleanField(_("23. Does the PRA staff have written job descriptions to carry out their functions effectively and in accordance with international phytosanitary standards?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_24 = models.NullBooleanField(_("24. Does the NPPO's PRA service's structure make organizational sense and facilitate the work?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_25 = models.NullBooleanField(_("25. Is there an organizational chart of the PRA service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_26 = models.NullBooleanField(_("26. Does the NPPO have linkages with the relevant stakeholders to get support and improve the quality of the PRA service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>28.</b></i>  "),)
    m_27= models.TextField(_("27. If so, with which stakeholders and for what ?"), blank=True, null=True,help_text=_(" "),)
    m_28 = models.NullBooleanField(_("28. Are NPPO's phytosanitary service providers approved/ accredited or contracted by the NPPO, involved in some steps of the PRA process?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("<br> <br> <br><i>If answer is <b>No</b> go to question <b>30.</b></i>  "),)
    m_29= models.TextField(_("29. If yes, in which steps?"), blank=True, null=True,help_text=_(" "),)
    m_30 = models.NullBooleanField(_("30. Does the NPPO have a management system that ensures that all requirements, including, legislative, technical and administrative requirements, are satisfied for PRA to be performed?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_31 = models.NullBooleanField(_("31. Does the NPPO's PRA process have an operational manual?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>33.</b></i> "),)
    m_32 = models.NullBooleanField(_("32. If yes, is the PRA operational manual consistent with the relevant ISPMs and periodically reviewed?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_33
    m_34 = models.NullBooleanField(_("34. Is this information stored in a computerized retrieval system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_35 = models.NullBooleanField(_("35. Does the NPPO have a written procedure to liaison with the relevant stakeholders for communicate the identified phytosanitary measures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_36 = models.NullBooleanField(_("36. Does the NPPO have a written procedure to immediately publish and transmit the adopted phytosanitary measures to contracting parties that it believes may be directly affected (according to IPPC Article VII.2b) and on request make the rationale available to any contracting party (according to IPPC Article VII.2c)."), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_37 = models.NullBooleanField(_("37. Are the linkages with other NPPO's programs (pest surveillance, import inspection) well established in the PRA operational manual?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_38 = models.NullBooleanField(_("38. Has the NPPO established procedures for PRA of LMOs in accordance with <a href='https://www.ippc.int/en/publications/639/' target='_blank'>ISPM 11</a> ?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_39 = models.NullBooleanField(_("39. Does the NPPO have a written procedure to perform PRA of consignments in transit?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_40 = models.NullBooleanField(_("40. Does the NPPO have an internal technical review and audit program to improve the quality of the PRA process?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_41 = models.NullBooleanField(_("41. Is the type and level of inspection based on pest risk analysis?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_42 matrix
    m_43 = models.IntegerField(_("43. Rate the NPPO's PRA units' current human resources capacity, in terms of numbers"),choices=WEAK, default=None,help_text=_(" "),)
    m_44 = models.IntegerField(_("44. Rate the NPPO's PRA units' current human resources capacity, in terms of qualifications and skills"),choices=WEAK, default=None,help_text=_(" "),)
    m_45 = models.IntegerField(_("45. Are those HR sufficient to carry out the activities required by the NPPO' s requirements in pest risk analysis?"),choices=LIM, default=None,help_text=_(" "),)
    m_46 = models.IntegerField(_("46. Is the PRA staff sufficiently qualified and trained to perform PRA?"),choices=THEM, default=None,help_text=_(" "),)
    m_47 = models.NullBooleanField(_("47. For pest categorization purposes (see <a href='https://www.ippc.int/en/publications/639/' target='_blank'>ISPM 11</a> ) is there expertise in the country to determine the potential for entry, establishment and spread of quarantine or regulated non-quarantine pest? "), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_48 = models.NullBooleanField(_("48. Does the NPPO have the ability to conduct climatic analysis using tools such as CLIMEX and others?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_49 = models.NullBooleanField(_("49. For pest categorization purposes, is there expertise in the country to determine whether the pest could cause an unacceptable economic impact?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_50 = models.NullBooleanField(_("50. Does the NPPO have (or have ready access to) economic impact assessment expertise to estimate potential economic impacts of regulated pest(s), both direct and indirect pest effects, using economic analysis techniques?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_51 = models.NullBooleanField(_("51. Does the NPPO have (or have ready access to) economic data on crop production, pest control costs etc?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_52 = models.NullBooleanField(_("52. Does the NPPO have the expertise to determine whether risk management measures are dependent or independent events, estimate level of uncertainty and confidence levels?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_53 = models.NullBooleanField(_("53. Does the NPPO have ready access to expertise to assess qualitatively or quantitatively the efficacy of pest risk management measures for single measures (e.g. fumigation) and combined measures (e.g. fumigation, inspection and cold storage)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_54 = models.NullBooleanField(_("54. Does the NPPO have ready access to expertise for determining under what circumstances integrated pest management measures (systems approach) can be used and can they evaluate the measures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_55 = models.NullBooleanField(_("55. Does the NPPO have ready access to expertise to evaluate the integrated risk management measures proposed by trading partners?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_56 = models.NullBooleanField(_("56. Does the NPPO currently accept integrated pest risk management measures developed by trading partners on imported commodities?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_57 = models.NullBooleanField(_("57. Does the NPPO undertake any research on various integrated pest risk management measures?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>Yes</b> go to question <b>59.</b></i> "),)
    m_58 = models.NullBooleanField(_("58. If no, are there any other institutions or agencies (government and private) within the country undertaking such research?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_59 = models.IntegerField(_("59. How many people have been sufficiently trained to carry out PRA?"),choices=PERC1, default=None,help_text=_(" "),)
    m_60 = models.IntegerField(_("60. How frequent are training programs for staff involved in PRA?"),choices=TRAIN2, default=None,help_text=_(" "),)
    m_61 = models.NullBooleanField(_("61. Are the PRA managers trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_62 = models.IntegerField(_("62. Assess the availability and requirements of internet access in the NPPO's PRA program"),choices=INSUFF7, default=None,help_text=_(" "),)
    m_63 = models.IntegerField(_("63. Assess the availability and requirements of adequate computers and tailored software in the NPPO's PRA unit"),choices=INSUFF7, default=None,help_text=_(" "),)
    m_64 = models.IntegerField(_("1. How effective is the PRA programme in consideration of the NPPO's mission?"),choices=WEAK, default=None,help_text=_(" "),)
    m_65 = models.IntegerField(_("2. How efficient are the PRA's Unit resources utilised"),choices=EFF, default=None,help_text=_(" "),)
    m_66 = models.IntegerField(_("3. Has the PRA programme kept its relevance over time?"),choices=RATHER, default=None,help_text=_(" "),)
    m_67 = models.IntegerField(_("4. How well is the NPPO's PRA programme performing?"),choices=BAD2, default=None,help_text=_(" "),)
    #m68
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_46= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_47= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_48= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_49= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_50= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_51= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_52= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_53= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_54= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_55= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_56= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_57= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_58= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_59= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_60= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_61= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_62= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_63= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_64= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_65= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_66= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_67= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_68= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
   
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module11, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number}) 
                            
class Module11Grid2(models.Model):
    module11 = models.ForeignKey(Module11)
    c1 = models.NullBooleanField(_("What is the purpose of PRA? What the PRA unit seeks to accomplish?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("What services are performed in order to accomplish this purpose?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("What principles (e.g. risk based, science based) and values (e.g. honesty, integrity, technical independence) guide the work of PRA unit?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    
    
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
    
class Module11Grid3(models.Model):
    module11 = models.ForeignKey(Module11)
    c1 = models.NullBooleanField(_("Specific so that they are clear and easy to understand?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Measurable and able to be quantified so that is possible to measure progress"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Achievable and realistic given the circumstances in which they are set and the resources available?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Relevant to the country's needs and to the NPPO?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Time bound with realistic deadlines for achievement?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
    
class Module11Grid12(models.Model):
    module11 = models.ForeignKey(Module11)
    c1 = models.NullBooleanField(_("Pathways (including transit)?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c2 = models.NullBooleanField(_("Pests (including weed)?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c3 = models.NullBooleanField(_("Biological Control Agents?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c4 = models.NullBooleanField(_("Living Modified Organisms?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c5 = models.NullBooleanField(_("Invasive Alien Species?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 

class Module11Grid14(models.Model):
    module11 = models.ForeignKey(Module11)
    c1 = models.NullBooleanField(_("'minimal impact'"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c2 = models.NullBooleanField(_("'equivalence'"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c3 = models.NullBooleanField(_("'non-discrimination'"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c4 = models.NullBooleanField(_("avoidance of undue delay"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c5 = models.NullBooleanField(_("harmonization"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c6 = models.NullBooleanField(_("transparency"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1     
class Module11Grid33(models.Model):
    module11 = models.ForeignKey(Module11)
    c1 = models.NullBooleanField(_("PRA initiation?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c2 = models.NullBooleanField(_("Pest risk assessment?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c3 = models.NullBooleanField(_("Pest risk management?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c4 = models.NullBooleanField(_("PRA documentation?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1      
class Module11Matrix42(models.Model):
    module11 = models.ForeignKey(Module11)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=None,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=None,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=None,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff    
 

class Module11Weaknesses(models.Model):
    module11 = models.ForeignKey(Module11)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1   
    
class Module12(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 12 - Pest free areas, places and sites, low pest prevalence areas")
        verbose_name_plural = _("Module 12 - Pest free areas, places and sites, low pest prevalence areas")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.NullBooleanField(_("1. Is the mandate of the PFA,ALPP,PFPP or PFPS programmes consistent with the NPPO's mission?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>3.</b></i> "),)
    #m_2
    #m_3
    m_4 = models.NullBooleanField(_("4. Is there a strategic and operational plan for the establishment and maintenance of PFA,ALPP,PFPP or PFPS?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Is there a set of good indicators to measure the effectiveness of the PFA,ALPP,PFPP or PFPS programs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("6. Is there a set of good indicators to measure the efficacy of the PFA,ALPP,PFPP or PFPS programs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7= models.TextField(_("7. What indicators could be used to measure the status of the PFA,ALPP,PFPP or PFPS programme's relevance?"), blank=True, null=True,help_text=_(" "),)
    m_8 = models.NullBooleanField(_("8. Does the PFA,ALPP,PFPP or PFPS unit have procedures to review its performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_9 = models.NullBooleanField(_("9. Does the national legislation allow the NPPO to establish, declare, maintain and seek recognition of PFA,ALPP,PFPP or PFPS, in compliance with the international guidelines?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10 = models.NullBooleanField(_("10. Is there a legal provision for the charge of a cost recovery fee to the owners of PFPP or PFPS?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11 = models.NullBooleanField(_("11. In case of a pest outbreak in a PFA,ALPP,PFPP or PFPS, does the legislation allow the NPPO to adopt the eradication/suppression measures required to re-establish the pest status in the area of concern?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_12 = models.NullBooleanField(_("12. Does the legislation allow the NPPO to establish internal procedures to assure the traceability of consignments from a PFA,ALPP,PFPP or PFPS towards the port of export?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("  <br> <br> <br><i>If answer is <b>No</b> go to question <b>14.</b></i>"),)
    m_13 = models.NullBooleanField(_("13. Does the legislation allow the NPPO to establish internal procedures to assure the traceability of consignments from a PFA,ALPP,PFPP or PFPS towards the port of export?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_14 = models.NullBooleanField(_("14. Are the NPPO's PFA,ALPP,PFPP or PFPS programs, centralized under a national manager?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_15 = models.NullBooleanField(_("15. Do NPPO's PFA,ALPP,PFPP or PFPS program's structures make organizational sense and facilitate the work?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.NullBooleanField(_("16. Is there an organizational chart of the PFA,ALPP,PFPP or PFPS program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.NullBooleanField(_("17. Are there written job descriptions establishing the mandates, functions and responsibilities of the PFA,ALPP,PFPP or PFPS program staff?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_18 = models.NullBooleanField(_("18. Does the NPPO have linkages with the relevant stakeholders (non NPPO) to get support for the PFA,ALPP,PFPP or PFPS programs?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>20</b></i> "),)
    m_19= models.TextField(_("19. If yes, with which stakeholders and for what?"), blank=True, null=True,help_text=_(" "),)
    m_20 = models.NullBooleanField(_("20. Is there a national standard or set of guidelines or Operational Manual for PFA,ALPP,PFPP or PFPS programs, including procedures for establishment, declaration, maintenance, re-establishment, recognition, etc?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_21 = models.NullBooleanField(_("21. Does the NPPO have the human resources to monitor the establishment and maintenance of pest freedom and appropriate buffer zones?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_22
    m_23 = models.IntegerField(_("23. Rate the NPPO's PFA,ALPP,PFPP or PFPS program current human resources capacity in terms of numbers, qualifications and skills"),choices=WEAK, default=None,help_text=_(" "),)
    m_24 = models.IntegerField(_("24. Are those HR sufficient to carry out the activities required by the NPPO's requirements in PFA,ALPP,PFPP or PFPS programs?"),choices=INSUFF8, default=None,help_text=_(" "),)
    m_25 = models.IntegerField(_("25. Are staff sufficiently qualified and trained to perform PFA,ALPP,PFPP or PFPS activities?"),choices=THEM, default=None,help_text=_(" "),)
    m_26 = models.IntegerField(_("26. How many people have been specifically trained to carry out PFA,ALPP,PFPP or PFPS programs"),choices=PERC3, default=None,help_text=_(" "),)
    m_27 = models.IntegerField(_("27. How frequent are training programs for staff involved in PFA,ALPP,PFPP or PFPS?"),choices=TRAIN2, default=None,help_text=_(" "),)
    m_28 = models.NullBooleanField(_("28. Are the PFA,ALPP,PFPP or PFPS program managers trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
   #m_29
    m_30 = models.IntegerField(_("1. How effective is the PFA,ALPP,PFP or PFPS programme in consideration of the NPPO's mission?"),choices=WEAK, default=None,help_text=_(" "),)
    m_31 = models.IntegerField(_("2. How efficient are the PFA,ALPP,PFP or PFPS's resources utilized?"),choices=EFF, default=None,help_text=_(" "),)
    m_32 = models.IntegerField(_("3. Has the PFA,ALPP,PFP or PFPS programme kept its relevance over time?"),choices=RATHER, default=None,help_text=_(" "),)
    m_33 = models.IntegerField(_("4. How well is the NPPO's PFA,ALPP,PFP or PFPS programme performing?"),choices=BAD2, default=None,help_text=_(" "),)
   #m34
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
   
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module12, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
class Module12Grid2(models.Model):
    module12 = models.ForeignKey(Module12)
    c1 = models.NullBooleanField(_("What is the purpose of PFA,ALPP,PFPP or PFPS?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("What services are performed in order to accomplish this purpose?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("What principles (e.g. risk based, science based) and values (e.g. honesty, integrity, technical independence) guide the work of PFA,ALPP,PFPP or PFPS program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
    
class Module12Grid3(models.Model):
    module12 = models.ForeignKey(Module12)
    c1 = models.NullBooleanField(_("Specific so that they are clear and easy to understand?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Measurable and able to be quantified so that is possible to measure progress"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Achievable and realistic given the circumstances in which they are set and the resources available?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Relevant to the country's needs and to the NPPO"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c5 = models.NullBooleanField(_("Time bound with realistic deadlines for achievement?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
    
class Module12Grid_29(models.Model):
    module12 = models.ForeignKey(Module12)
    c1 = models.IntegerField(_("PFA"),choices=INSUFF0, default=None,help_text=_(" "),)
    c2 = models.IntegerField(_("ALPP"),choices=INSUFF0, default=None,help_text=_(" "),)
    c3 = models.IntegerField(_("PFPP"),choices=INSUFF0, default=None,help_text=_(" "),)
    c4 = models.IntegerField(_("PFPS"),choices=INSUFF0, default=None,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
    
class Module12Matrix22(models.Model):
    module12 = models.ForeignKey(Module12)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=None,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=None,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=None,help_text=_(" "),)
    averagelab = models.IntegerField(_("averagelab"),choices=VAL_AV, default=None,help_text=_(" "),)
    managers = models.IntegerField(_("managers"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff    

class Module12Weaknesses(models.Model):
    module12 = models.ForeignKey(Module12)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1   
    

class Module13(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Module 13 - Export certification, re-export, transit")
        verbose_name_plural = _("Module 13 - Export certification, re-export, transit")
  
    session = models.ForeignKey(PceVersion)
    modify_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=False)
    m_1 = models.NullBooleanField(_("1. Is the mandate of the export certification program activities consistent with the NPPO's mission?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("  <br> <br> <br><i>If answer is <b>No</b> go to question <b>3.</b></i>"),)
    #m_2  
    #m_3   
    m_4 = models.NullBooleanField(_("4. Is there a strategic and operational plan for the export certification activities?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_5 = models.NullBooleanField(_("5. Does the export certification program have procedures to review its performance?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_6 = models.NullBooleanField(_("6. Is there a set of good indicators to measure the effectiveness of the export certification service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_7 = models.NullBooleanField(_("7. Is there a set of good indicators to measure the efficacy of the certification service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_8= models.TextField(_("8. What indicators could be used to measure the status or the export certification services relevance"), blank=True, null=True,help_text=_(" "),)
    m_9 = models.NullBooleanField(_("9. Does the NPPO have the sole authority by legislative or administrative means for control and issuance of phytosanitary certificates?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_10 = models.NullBooleanField(_("10. Does the present legislation comply with the model phytosanitary and re-export certificates as described in the annex of the revised text of the IPPC (1997)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_11 = models.NullBooleanField(_("11. Does the NPPO have the authority to refuse the issuance of the phytosanitary certificate for the export of consignments which do not meet an importing country's requirements?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_12 = models.NullBooleanField(_("12. Does the NPPO have the authority to approve/accredit phytosanitary service providers from the official or private sectors to collaborate in the export certification program (field inspection, packing inspection, treatment, inspection and storage facilities, etc)?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_13 = models.NullBooleanField(_("13. Does the legislation allow NPPO to charge fees for the services provided by the export certification program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("  <br> <br> <br><i>If answer is <b>No</b> go to question <b>16.</b></i>"),)
    m_14 = models.NullBooleanField(_("14. If yes, are those fees charged on a cost recovery base?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("  <br> <br> <br><i>If answer is <b>No</b> go to question <b>16.</b></i>"),)
    m_15 = models.NullBooleanField(_("15. If yes, are those fees updated as needed?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_16 = models.NullBooleanField(_("16. Is there a national manager responsible for the export certification system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_17 = models.NullBooleanField(_("17. Does the export certification staff have written job descriptions to carry out its function effectively and in accordance with the International Standards?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_18 = models.NullBooleanField(_("18. Does NPPO's export certification program's structure make organizational sense and facilitate the work?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_19 = models.NullBooleanField(_("19. Is there an organizational chart of the export certification program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_20 = models.NullBooleanField(_("20. Does the NPPO have linkages with the relevant stakeholders to get support and improve the quality of the export certification program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>23.</b></i>"),)
    m_21= models.TextField(_("21. If so, with which stakeholders and for what?"), blank=True, null=True,help_text=_(" "),)
   #m_22
    m_23 = models.NullBooleanField(_("23. Are NPPO's phytosanitary service providers approved/accredited by the NPPO involved in some steps of the export certification process?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("  <br> <br> <br><i>If answer is <b>No</b> go to question <b>25.</b></i>"),)
    m_24 = models.IntegerField(_("24. If yes, in which steps?"),choices=INSP, default=None,help_text=_(" "),)
    m_25 = models.NullBooleanField(_("25. Does the NPPO have a management system that ensures that all requirements, including certification, legislative and technical requirements and administrative requirements, are satisfied for each certificate issued?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_26 = models.NullBooleanField(_("26. Does the NPPO's export certification have an operational manual?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_27 = models.NullBooleanField(_("27. Does the NPPO maintain up-to-date information on the import requirements of importing countries?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>29.</b></i>"),)
    m_28 = models.NullBooleanField(_("28. Is this information stored in a computerized retrieval system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    #m_29
    m_30 = models.NullBooleanField(_("30. Is a copy of each phytosanitary certificate retained (hard copy or electronic version) for purposes of validation and trace back?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_("  <br> <br> <br><i>If answer is <b>No</b> go to question <b>33.</b></i>"),)
   #m_31
    m_32 = models.NullBooleanField(_("32. Is this information stored in a computerized retrieval system?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_33 = models.NullBooleanField(_("33. If required by the imported country, are all consignments and their certification traceable through all stages of production, handling and transport to the point of export?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_34 = models.NullBooleanField(_("34. Does the NPPO's export certification program have a procedure to ensure the phytosanitary security and the consignment's integrity, after the certification until export?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_35 = models.NullBooleanField(_("35. Are the linkages with other NPPO's programs (pest diagnostic, surveillance, internal quarantine, and phytosanitary inspectors) well established in the export certification manual?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_36 = models.NullBooleanField(_("36. Does the NPPO have a system for liaising effectively with the importing countries NPPO's to discuss phytosanitary requirements?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_37 = models.NullBooleanField(_("37. Has the NPPO made available an IPPC contact point for the importing country's NPPO to which cases of non-compliance can be reported?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_38 = models.NullBooleanField(_("38. Has the NPPO established procedures for investigating reports from importing countries of non-compliant consignments covered by a phytosanitary certificate?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_39 = models.NullBooleanField(_("39. Does the NPPO have an internal technical audit program to improve the quality of the export certification program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_40 = models.NullBooleanField(_("40. Are the phytosanitary and re-export certificates issued by the NPPO in accordance with the model certificates in the IPPC annex?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" <br> <br> <br><i>If answer is <b>No</b> go to question <b>42.</b></i>"),)
    m_41 = models.NullBooleanField(_("41. Are those certificates issued in accordance with the good practices for certification's issuance as established in <a href='https://www.ippc.int/en/publications/609/' target='_blank'>ISPM 12</a>?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_42 = models.IntegerField(_("42. If an imported consignment is then exported to another country, and it has not been exposed to infestation or contamination by pests without loss of its integrity or identity, what model certificate is used by the NPPO?"),choices=PHY, default=None,help_text=_(" "),)
    m_43 = models.IntegerField(_("43. If an imported or in transit consignment has not been exposed to infestation or contamination by pests, but has lost its integrity or identity, or has been processed to change its nature, what model certificate is used by the NPPO?"),choices=PHY, default=None,help_text=_(" "),)
    m_44 = models.NullBooleanField(_("44. Is the country of origin indicated on the certificate?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_45 = models.NullBooleanField(_("45. If the consignment has been grown for a specific time (depending on the commodity concerned, but usually one growing season or more) is the consignment considered to have changed its country of origin?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_46 = models.IntegerField(_("46. If a consignment is not imported, but is in transit through the country without being exposed to infestation or contamination by pests, what type of certificate is issued by NPPO?"),choices=PHY, default=None,help_text=_(" "),)
    #m_47 matrix
    m_48 = models.IntegerField(_("48. Rank the NPPO's export certification program current human resources capacity, in terms of numbers, qualifications and skills"),choices=WEAK, default=None,help_text=_(" "),)
    m_49 = models.IntegerField(_("49. Are those HR sufficient to carry out the activities required by the NPPO's export certification program?"),choices=LIM1, default=None,help_text=_(" "),)
    m_50 = models.IntegerField(_("50. Are inspectors specifically qualified and trained to perform export certification?"),choices=FEW, default=None,help_text=_(" "),)
    m_51 = models.IntegerField(_("51. How many of the staff have been specifically trained to carry out export certification?"),choices=FEW, default=None,help_text=_(" "),)
    m_52 = models.IntegerField(_("52. How frequent are training programs for staff involved in export certification?"),choices=TRAIN2, default=None,help_text=_(" "),)
    m_53 = models.NullBooleanField(_("53. Are the export certification program's managers trained in management?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_54 = models.IntegerField(_("54. Assess the availability and requirements of equipment and transport in the NPPO's export certification program"),choices=LIM1, default=None,help_text=_(" "),)
    m_55 = models.IntegerField(_("55. Assess the availability and requirements of communications in the NPPO's export certification program"),choices=LIM1, default=None,help_text=_(" "),)
    m_56 = models.IntegerField(_("56. Assess the availability and requirements of adequate office and inspection facilities in the NPPO's export certification program"),choices=LIM1, default=None,help_text=_(" "),)
    m_57 = models.IntegerField(_("57. Assess the availability and requirements of adequate computers and tailored software in the NPPO's export certification program"),choices=LIM1, default=None,help_text=_(" "),)
    m_58 = models.IntegerField(_("1. How effective is the export certification service considering the NPPO's mission"),choices=WEAK, default=None,help_text=_(" "),)
    m_59 = models.NullBooleanField(_("2. Is there a set of good indicators to measure the effectiveness of the export certification service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_60  = models.IntegerField(_("3. With what efficacy are the export certification's resources utilized?"),choices=WEAK, default=None,help_text=_(" "),)
    m_61 = models.NullBooleanField(_("4. Is there a set of good indicators to measure the efficacy of the certification service?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    m_62 = models.IntegerField(_("5. With what efficacy are the export certification service's resources utilized?"),choices=WEAK, default=None,help_text=_(" "),)
    m_63 = models.IntegerField(_("6. Has the export certification service kept its relevance over time?"),choices=WEAK, default=None,help_text=_(" "),)
    m_64= models.TextField(_("7. What indicators could be used to measure the status or the export certification services relevance"), blank=True, null=True,help_text=_(" "),)
    m_65 = models.IntegerField(_("8. How well is the NPPO's export certification service performing?"),choices=WEAK, default=None,help_text=_(" "),)
    #m66
    #m_comment = models.TextField(_("Comment"), blank=True, null=True,help_text='Please put your comments here.')
    c_m_1= models.TextField(_("Comment"), blank=True, null=True,help_text=' ')
    c_m_2= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_3= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_4= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_5= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_6= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_7= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_8= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_9= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_10= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_11= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_12= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_13= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_14= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_15= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_16= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_17= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_18= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_19= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_20= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_21= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_22= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_23= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_24= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_25= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_26= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_27= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_28= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_29= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_30= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_31= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_32= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_33= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_34= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_35= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_36= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_37= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_38= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_39= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_40= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_41= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_42= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_43= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_44= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_45= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_46= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_47= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_48= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_49= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_50= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_51= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_52= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_53= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_54= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_55= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_56= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_57= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_58= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_59= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_60= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_61= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_62= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_63= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_64= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_65= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    c_m_66= models.TextField(_("Comment"), blank=True, null=True,help_text=' ');
    
   
    def __unicode__(self):
        return self.title
 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Module13, self).save(*args, **kwargs)
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})    
class Module13Grid2(models.Model):
    module13 = models.ForeignKey(Module13)
    c1 = models.NullBooleanField(_("What is the purpose of export certification?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("What does the export certification program seek to accomplish?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("What services are performed in order to accomplish this purpose?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("What principles (e.g. risk based, science based) and values (e.g. honesty, integrity, technical independence) guide the work of export certification program?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    
    
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1  
    
class Module13Grid3(models.Model):
    module13 = models.ForeignKey(Module13)
    c1 = models.NullBooleanField(_("Specific so that they are clear and easy to understand?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c2 = models.NullBooleanField(_("Measurable and able to be quantified so that is possible to measure progress"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c3 = models.NullBooleanField(_("Achievable and realistic given the circumstances in which they are set and the resources available?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    c4 = models.NullBooleanField(_("Time bound with realistic deadlines for achievement?"), choices=BOOL_CHOICES,blank=True, null=True, help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 
    
class Module13Grid22(models.Model):
    module13 = models.ForeignKey(Module13)
    c1 = models.NullBooleanField(_("importing country phytosanitary requirements?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c2 = models.NullBooleanField(_("pest status and geographical distribution?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c3 = models.NullBooleanField(_("operational procedures?"),choices=BOOL_CHOICES, default=None,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1 

class Module13Grid29(models.Model):
    module13 = models.ForeignKey(Module13)
    c1 = models.NullBooleanField(_("Control over issuance (manual or electronic)?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c2 = models.NullBooleanField(_("Identification of issuing officers?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c3 = models.NullBooleanField(_("Inclusion of additional declarations?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c4 = models.NullBooleanField(_("Completion of the treatment section of the certificates?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c5 = models.NullBooleanField(_("Certified alterations?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c6 = models.NullBooleanField(_("Completion of phytosanitary certificates?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c7 = models.NullBooleanField(_("Signature and delivery of phytosanitary certificates?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c8 = models.NullBooleanField(_("Procedures for working with industry?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c9 = models.NullBooleanField(_("Sampling, inspection and verification procedures?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c10 = models.NullBooleanField(_("Security over official seals/marks?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c11 = models.NullBooleanField(_("Consignment identification, trace ability, and security?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c12 = models.NullBooleanField(_("Record keeping?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1     
class Module13Grid31(models.Model):
    module13 = models.ForeignKey(Module13)
    c1 = models.NullBooleanField(_("Any inspection, testing, treatment or other verification which was conducted on a consignment basis?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c2 = models.NullBooleanField(_("The names of the personnel who undertook these tasks?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c3 = models.NullBooleanField(_("The date on which the activity was undertaken?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c4 = models.NullBooleanField(_("The results obtained?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    c5 = models.NullBooleanField(_("Any samples taken?"),choices=BOOL_CHOICES,blank=True, null=True,help_text=_(" "),)
    def __unicode__(self):  
        return self.c1
    def name(self):
        return self.c1      
class Module13Matrix47(models.Model):
    module13 = models.ForeignKey(Module13)
    nstaff = models.IntegerField(_("nstaff"),choices=VAL, default=None,help_text=_(" "),)
    average = models.IntegerField(_("average"),choices=VAL_AV, default=None,help_text=_(" "),)
    nstafflab = models.IntegerField(_("nstafflab"),choices=VAL, default=None,help_text=_(" "),)
    averagelab = models.IntegerField(_("averagelab"),choices=VAL_AV, default=None,help_text=_(" "),)
    managers = models.IntegerField(_("managers"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
    support = models.IntegerField(_("support"),choices=BOOL_CHOICESM_M,default=None,help_text=_(" "),)
   
    def __unicode__(self):  
        return self.nstaff
    def name(self):
        return self.nstaff    
  

class Module13Weaknesses(models.Model):
    module13 = models.ForeignKey(Module13)
    w1 = models.CharField(_("1"), blank=True, null=True, max_length=250,)
    w2 = models.CharField(_("2"), blank=True, null=True,max_length=250,)
    w3 = models.CharField(_("3"), blank=True, null=True,max_length=250,)
    w4 = models.CharField(_("4"), blank=True, null=True,max_length=250,)
    w5 = models.CharField(_("5"), blank=True, null=True,max_length=250,)

    def __unicode__(self):  
        return self.w1
    def name(self):
        return self.w1   
            
class Stakeholders(Displayable, models.Model):
    """Single version of the pce module for a country."""
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("Stakeholders")
        verbose_name_plural = _("Stakeholders")
  
    session = models.ForeignKey(PceVersion)
    module = models.CharField(_("Module"), blank=True, null=True,max_length=250,)
    
    def __unicode__(self):
        return self.title+'.'

 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(Stakeholders, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})
                            
class StakeholdersFields(models.Model):
    stakeholder = models.ForeignKey(Stakeholders)
    firstname = models.CharField(_("First name"), blank=True, null=True,max_length=250,)
    lastname = models.CharField(_("Last name"), blank=True, null=True,max_length=250,)
    email = models.CharField(_("Email"), blank=True, null=True,max_length=250,)
    organisation = models.CharField(_("Organisation/division"), blank=True, null=True,max_length=250,)
    
    role = models.IntegerField(_("Role"), choices=ROLE, default=ROLE_0 ,blank=True)
    interest = models.IntegerField(_("Interest"), choices=INTEREST, default=INTEREST_0,blank=True)
    influence = models.IntegerField(_("Influence"), choices=INTEREST, default=INTEREST_0,blank=True)
    level = models.IntegerField(_("Level"), choices=LEVEL, default=LEVEL_0,blank=True)

    def __unicode__(self):  
        return self.lastname+self.firstname+'.'
    def name(self):
        return self.lastname


   
    
class ProblemAnalysis(Displayable, models.Model):
    """ ProblemAnalysis """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("ProblemAnalysis")
        verbose_name_plural = _("ProblemAnalysis")
  
    session = models.ForeignKey(PceVersion)
    module = models.CharField(_("Module"), blank=True, null=True,max_length=250,)
    
    cause_a_1= models.TextField(_("Primary"), blank=True, null=True,)
    cause_b_1= models.TextField(_("Secondary"), blank=True, null=True,)
    #w_1= models.TextField(_("Major weaknesses needing to be addressed"), blank=True, null=True,)
    consequence_a_1= models.TextField(_("Primary"), blank=True, null=True,)
    consequence_b_1= models.TextField(_("Secondary"), blank=True, null=True,)
   
    cause_a_2= models.TextField(_("Primary"), blank=True, null=True,)
    cause_b_2= models.TextField(_("Secondary"), blank=True, null=True,)
    #w_2= models.TextField(_("Major weaknesses needing to be addressed"), blank=True, null=True,)
    consequence_a_2= models.TextField(_("Primary"), blank=True, null=True,)
    consequence_b_2= models.TextField(_("Secondary"), blank=True, null=True,)
   
    cause_a_3= models.TextField(_("Primary"), blank=True, null=True,)
    cause_b_3= models.TextField(_("Secondary"), blank=True, null=True,)
    #w_3= models.TextField(_("Major weaknesses needing to be addressed"), blank=True, null=True,)
    consequence_a_3= models.TextField(_("Primary"), blank=True, null=True,)
    consequence_b_3= models.TextField(_("Secondary"), blank=True, null=True,)
   
    cause_a_4= models.TextField(_("Primary"), blank=True, null=True,)
    cause_b_4= models.TextField(_("Secondary"), blank=True, null=True,)
    #w_4= models.TextField(_("Major weaknesses needing to be addressed"), blank=True, null=True,)
    consequence_a_4= models.TextField(_("Primary"), blank=True, null=True,)
    consequence_b_4= models.TextField(_("Secondary"), blank=True, null=True,)
   
    cause_a_5= models.TextField(_("Primary"), blank=True, null=True,)
    cause_b_5= models.TextField(_("Secondary"), blank=True, null=True,)
    #w_5= models.TextField(_("Major weaknesses needing to be addressed"), blank=True, null=True,)
    consequence_a_5= models.TextField(_("Primary"), blank=True, null=True,)
    consequence_b_5= models.TextField(_("Secondary"), blank=True, null=True,)
   
    def __unicode__(self):
        return self.title

 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(ProblemAnalysis, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})



                            
class SwotAnalysis(models.Model):
    session = models.ForeignKey(PceVersion)
    module = models.CharField(_("Module"), blank=True, null=True,max_length=250,)
    
    def __unicode__(self):
        return self.title

 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(SwotAnalysis, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = _("SwotAnalysis")
        verbose_name_plural = _("SwotAnalysis")
  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})
                            
class SwotAnalysis1(models.Model):
    swotanalysis = models.ForeignKey(SwotAnalysis)
    strengths= models.TextField(_("Strengths"), blank=True, null=True,)
    opportunities= models.TextField(_("Opportunities"), blank=True, null=True,)
    threats= models.TextField(_("Threats"), blank=True, null=True,)	
    actions= models.TextField(_("Actions"), blank=True, null=True,)
    priority = models.IntegerField(_("Priority"), choices=PRIORITY, default=None)
    type = models.IntegerField(_("Type"), choices=TYPE, default=None)
    
    def __unicode__(self):
        return self.weaknesses

class SwotAnalysis2(models.Model):
    swotanalysis = models.ForeignKey(SwotAnalysis)
    strengths= models.TextField(_("Strengths"), blank=True, null=True,)
    opportunities= models.TextField(_("Opportunities"), blank=True, null=True,)
    threats= models.TextField(_("Threats"), blank=True, null=True,)	
    actions= models.TextField(_("Actions"), blank=True, null=True,)
    priority = models.IntegerField(_("Priority"), choices=PRIORITY, default=None)
    type = models.IntegerField(_("Type"), choices=TYPE, default=None)
    
    def __unicode__(self):
        return self.weaknesses
    
class SwotAnalysis3(models.Model):
    swotanalysis = models.ForeignKey(SwotAnalysis)
    strengths= models.TextField(_("Strengths"), blank=True, null=True,)
    opportunities= models.TextField(_("Opportunities"), blank=True, null=True,)
    threats= models.TextField(_("Threats"), blank=True, null=True,)	
    actions= models.TextField(_("Actions"), blank=True, null=True,)
    priority = models.IntegerField(_("Priority"), choices=PRIORITY, default=None)
    type = models.IntegerField(_("Type"), choices=TYPE, default=None)
    
    def __unicode__(self):
        return self.weaknesses

class SwotAnalysis4(models.Model):
    swotanalysis = models.ForeignKey(SwotAnalysis)
    strengths= models.TextField(_("Strengths"), blank=True, null=True,)
    opportunities= models.TextField(_("Opportunities"), blank=True, null=True,)
    threats= models.TextField(_("Threats"), blank=True, null=True,)	
    actions= models.TextField(_("Actions"), blank=True, null=True,)
    priority = models.IntegerField(_("Priority"), choices=PRIORITY, default=None)
    type = models.IntegerField(_("Type"), choices=TYPE, default=None)
    
    def __unicode__(self):
        return self.weaknesses
    
class SwotAnalysis5(models.Model):
    swotanalysis = models.ForeignKey(SwotAnalysis)
    strengths= models.TextField(_("Strengths"), blank=True, null=True,)
    opportunities= models.TextField(_("Opportunities"), blank=True, null=True,)
    threats= models.TextField(_("Threats"), blank=True, null=True,)	
    actions= models.TextField(_("Actions"), blank=True, null=True,)
    priority = models.IntegerField(_("Priority"), choices=PRIORITY, default=None)
    type = models.IntegerField(_("Type"), choices=TYPE, default=None)
    
    def __unicode__(self):
        return self.weaknesses


   
    
class LogicalFramework(Displayable, models.Model):
    """ LogicalFramework """
    # slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # title - provided by mezzanine.core.models.slugged (subclassed by displayable)
    # status - provided by mezzanine.core.models.displayable
    # publish_date - provided by mezzanine.core.models.displayable
    
    class Meta:
        verbose_name = _("LogicalFramework")
        verbose_name_plural = _("LogicalFramework")
  
    session = models.ForeignKey(PceVersion)
    module = models.CharField(_("Module"), blank=True, null=True,max_length=250,)
    overobjective= models.TextField(_("Overall Objective"), blank=True, null=True,)
    keyindicator0= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification0= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions0= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
  
    objective= models.TextField(_("Objective"), blank=True, null=True,)
    keyindicator= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
    
    output1= models.TextField(_("Output 1"), blank=True, null=True,)
    keyindicator1= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification1= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions1= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
    output2= models.TextField(_("Output 2"), blank=True, null=True,)
    keyindicator2= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification2= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions2= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
    
    output3= models.TextField(_("Output 3"), blank=True, null=True,)
    keyindicator3= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification3= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions3= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
    
    output4= models.TextField(_("Output 4"), blank=True, null=True,)
    keyindicator4= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification4= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions4= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
    
    output5= models.TextField(_("Output 1"), blank=True, null=True,)
    keyindicator5= models.TextField(_("Key Indicator"), blank=True, null=True,)
    verification5= models.TextField(_("Means of Verification"), blank=True, null=True,)
    assumptions5= models.TextField(_("Assumptions / Risk"), blank=True, null=True,)
    
   
   
    def __unicode__(self):
        return self.title

 
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.publish_date = datetime.today()
        self.modify_date = datetime.now()
        super(LogicalFramework, self).save(*args, **kwargs)
        
   
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a PCE Version."""
        return ('pceversion-detail', (), {
                            'country': self.country.name, # =todo: get self.country.name working
                            'year': self.publish_date.strftime("%Y"),
                            'session': self.version_number})

class LogicalFrameworkAct1(models.Model):
    logicalframework = models.ForeignKey(LogicalFramework)
    activity1 = models.TextField(_("Activity 1"), blank=True, null=True,)
    #target= models.TextField(_("Target"), blank=True, null=True,)
    #sourcverification= models.TextField(_("Source of verification"), blank=True, null=True,)	
    #external= models.TextField(_("External factors and conditions to be addressed"), blank=True, null=True,)
    cost= models.TextField(_("Estimated cost"), blank=True, null=True,)
    responsible= models.TextField(_("Identify a Responsible person"), blank=True, null=True,)
    deadline= models.TextField(_("Specify a deadline"), blank=True, null=True,)
    def __unicode__(self):
        return self.activity1
    
class LogicalFrameworkAct2(models.Model):
    logicalframework = models.ForeignKey(LogicalFramework)
    activity2 = models.TextField(_("Activity 2"), blank=True, null=True,)
    #target= models.TextField(_("Target"), blank=True, null=True,)
    #sourcverification= models.TextField(_("Source of verification"), blank=True, null=True,)	
   # external= models.TextField(_("External factors and conditions to be addressed"), blank=True, null=True,)
    cost= models.TextField(_("Estimated cost"), blank=True, null=True,)
    responsible= models.TextField(_("Identify a Responsible person"), blank=True, null=True,)
    deadline= models.TextField(_("Specify a deadline"), blank=True, null=True,)
    def __unicode__(self):
        return self.activity2
class LogicalFrameworkAct3(models.Model):
    logicalframework = models.ForeignKey(LogicalFramework)
    activity3 = models.TextField(_("Activity 3"), blank=True, null=True,)
   # target= models.TextField(_("Target"), blank=True, null=True,)
  #  sourcverification= models.TextField(_("Source of verification"), blank=True, null=True,)	
   # external= models.TextField(_("External factors and conditions to be addressed"), blank=True, null=True,)
    cost= models.TextField(_("Estimated cost"), blank=True, null=True,)
    responsible= models.TextField(_("Identify a Responsible person"), blank=True, null=True,)
    deadline= models.TextField(_("Specify a deadline"), blank=True, null=True,)
    def __unicode__(self):
        return self.activity3    
class LogicalFrameworkAct4(models.Model):
    logicalframework = models.ForeignKey(LogicalFramework)
    activity4 = models.TextField(_("Activity 4"), blank=True, null=True,)
   # target= models.TextField(_("Target"), blank=True, null=True,)
   # sourcverification= models.TextField(_("Source of verification"), blank=True, null=True,)	
   # external= models.TextField(_("External factors and conditions to be addressed"), blank=True, null=True,)
    cost= models.TextField(_("Estimated cost"), blank=True, null=True,)
    responsible= models.TextField(_("Identify a Responsible person"), blank=True, null=True,)
    deadline= models.TextField(_("Specify a deadline"), blank=True, null=True,)
    def __unicode__(self):
        return self.activity4
class LogicalFrameworkAct5(models.Model):
    logicalframework = models.ForeignKey(LogicalFramework)
    activity5 = models.TextField(_("Activity 5"), blank=True, null=True,)
   # target= models.TextField(_("Target"), blank=True, null=True,)
   ## sourcverification= models.TextField(_("Source of verification"), blank=True, null=True,)	
   # external= models.TextField(_("External factors and conditions to be addressed"), blank=True, null=True,)
    cost= models.TextField(_("Estimated cost"), blank=True, null=True,)
    responsible= models.TextField(_("Identify a Responsible person"), blank=True, null=True,)
    deadline= models.TextField(_("Specify a deadline"), blank=True, null=True,)
    def __unicode__(self):
        return self.activity5
   