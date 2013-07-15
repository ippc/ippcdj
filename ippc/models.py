from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

class IppcUserProfile(models.Model):
    """ User profiles for IPPC"""
    
    GENDER_CHOICES = (
        (1, _("Male")),
        (2, _("Female")),
    )
    
    user = models.OneToOneField("auth.User")
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    email_address = models.EmailField(_("email"), max_length=75)

    gender = models.PositiveSmallIntegerField(_("gender"), choices=GENDER_CHOICES, blank=True, null=True)
    profile_photo = models.FileField(_("profile photo"), upload_to="profile_photos", blank=True)
    bio = models.TextField()

    address1 = models.CharField(_("address1"), blank=True, max_length=100)
    address2 = models.CharField(_("address2"), blank=True, max_length=100)
    city = models.CharField(_("city"), blank=True, max_length=100)
    state = models.CharField(_("state"), blank=True, max_length=100, help_text="or Province")
    zipcode = models.CharField(_("zipcode"), blank=True, max_length=20)
    # country = models.CharField(_("country"), blank=True, max_length=100)
    country = CountryField(_("country"))

    phone = models.CharField(_("phone"), blank=True, max_length=30)
    fax = models.CharField(_("fax"), blank=True, max_length=30)
    mobile = models.CharField(_("mobile"), blank=True, max_length=30)