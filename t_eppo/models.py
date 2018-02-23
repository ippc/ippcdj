from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to


class Authorities(models.Model):
    """ Eppo EPPT Authorities """
    idauthor = models.IntegerField(_("id"), blank=True, null=True)
    authdesc = models.CharField(_("Authority description"), max_length=250)
   
    def __unicode__(self):
        return self.authdesc

class Datatypes(models.Model):
    """ Eppo EPPT Datatypes """
    datatype = models.CharField(_("datatype code"), max_length=3)
    libdatatype = models.CharField(_("libdatatype"), max_length=250)

    def __unicode__(self):
        return self.country 
        
class Countries(models.Model):
    """ Eppo EPPT Countries """
    isocountry = models.CharField(_("iso2 code"), max_length=3)
    country = models.CharField(_("Country"), max_length=250)

    def __unicode__(self):
        return self.country
        
class Langs(models.Model):
    """ Eppo EPPT Langs """
    isolang = models.CharField(_("isolang"), max_length=1)
    language = models.CharField(_("language"), max_length=250)

    def __unicode__(self):
        return self.language
        
class Vars(models.Model):
    """ Eppo EPPT Langs """
    varkey = models.CharField(_("isolang"), max_length=32)
    varval = models.CharField(_("language"), max_length=250)

    def __unicode__(self):
        return self.varkey
 

        
class Codes(models.Model):
    """ Eppo EPPT Authorities """
    eppocode = models.CharField(_("Eppo code"), max_length=8)
    datatype =models.CharField(_("datatype"), max_length=3)
    status = models.CharField(_("status"), max_length=1)
    c_date = models.DateTimeField(_("Creation date"),  blank=True, null=True, editable=True)
    m_date = models.DateTimeField(_("Modified date"), blank=True, null=True, editable=True)

    def __unicode__(self):
        return self.eppocode
        
  
        
class Names(models.Model):
    """ Eppo EPPT Names """
    #idname integer NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
    eppocode=models.CharField(_("Eppo code"), max_length=8)
    codename = models.CharField(_("Full name + Eppo code"), max_length=250)
    idauthor=models.IntegerField(_("id author"), blank=True, null=True)
    isolang=models.CharField(_("isolang"), max_length=2)
    isocountry=models.CharField(_("isolang"), max_length=3)
    fullname=models.CharField(_("Full Name"), max_length=250)
    preferred = models.BooleanField(verbose_name=_("Preferred"), default=False)
    c_date = models.DateTimeField(_("Creation date"),  blank=True, null=True, editable=True)
    m_date = models.DateTimeField(_("Modified date"),  blank=True, null=True, editable=True)
    status = models.CharField(_("isolang"), max_length=1)


    def __unicode__(self):
        return self.codename

    def getName(self):
        eppocodeid=self.id
        code =''
        latin=''
        family =''
        order =''
        common=''
        if eppocodeid != None:
            code=str(Names.objects.filter(id=eppocodeid)[0].eppocode)
            if code!= '':    
                if Names.objects.filter(eppocode=code,isolang='la', preferred="true").count()>0:
                    latin=Names.objects.filter(eppocode=code,isolang='la', preferred="true")[0].fullname
                if Names.objects.filter(eppocode=code,isolang='en').count()>0:
                    common=Names.objects.filter(eppocode=code,isolang='en')[0].fullname

                cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+code+"';")
                str1= cursor.fetchall()
                codeparent=''
                for row in str1:
                    codeparent=str1[0][0]
                codeparentlabel = Names.objects.filter(eppocode=codeparent,isolang='la', preferred="true")

                cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+codeparent+"';")
                codeparent2=''
                str2= cursor.fetchall()
                for row in str2:
                    codeparent2=str2[0][0]
                if  Names.objects.filter(eppocode=codeparent2,isolang='la', preferred="true").count()>0:
                    family = Names.objects.filter(eppocode=codeparent2,isolang='la', preferred="true")[0].fullname

                cursor.execute("SELECT eppocode_parent FROM t_eppo_links WHERE eppocode = '"+codeparent2+"';")
                codeparent3=''
                str3= cursor.fetchall()
                if len(str3)>0:
                      codeparent3=str3[0][0]


                if Names.objects.filter(eppocode=codeparent3,isolang='la', preferred="true").count()>0:
                    order = Names.objects.filter(eppocode=codeparent3,isolang='la', preferred="true")[0].fullname
                #print("*******************************")
                #print(latin+" : "+ order +" : "+ family+" : "+ common )
                #print("*******************************")
        if  latin!='':
            pestidentity=pestidentity+'<i>'+latin+"</i>"
        if  family!='':
            pestidentity=pestidentity+ "<br>"+ family
        if  order!='':
            pestidentity=pestidentity+  " : "+ order
        if  common!='':
            pestidentity=pestidentity+  "<br>"+ common
        pestidentity=pestidentity+ "<br>"+ str(code)+"<br><br>"
        return   pestidentity    
                     
    
    

class Links(models.Model):
    """ Eppo EPPT Links """
 #    idlink integer NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
 
    eppocode = models.CharField(_("eppocode"), max_length=8)
    eppocode_parent= models.CharField(_("eppocode_parent"), max_length=8)
    c_date = models.DateTimeField(_("Creation date"),  blank=True, null=True, editable=True)
    m_date = models.DateTimeField(_("Modified date"),  blank=True, null=True, editable=True)
    
    typelink=models.CharField(_("typelink"), max_length=1)
    def __unicode__(self):
        return self.eppocode   

