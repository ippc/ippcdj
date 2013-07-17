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
    # main email address already provided by auth.User
    email_address_alt = models.EmailField(_("alternate email"), max_length=75)

    gender = models.PositiveSmallIntegerField(_("gender"), choices=GENDER_CHOICES, blank=True, null=True)
    profile_photo = models.FileField(_("profile photo"), upload_to="profile_photos", blank=True)
    bio = models.TextField()

    address1 = models.CharField(_("address1"), blank=True, max_length=100)
    address2 = models.CharField(_("address2"), blank=True, max_length=100)
    city = models.CharField(_("city"), blank=True, max_length=100)
    state = models.CharField(_("state"), blank=True, max_length=100, help_text="or Province")
    zipcode = models.CharField(_("zipcode"), blank=True, max_length=20)
    # country will be the 'tag' to mark permissions for Country Main Contact Points and Country Editors
    country = CountryField(_("country"))

    phone = models.CharField(_("phone"), blank=True, max_length=30)
    fax = models.CharField(_("fax"), blank=True, max_length=30)
    mobile = models.CharField(_("mobile"), blank=True, max_length=30)


# Translations of site pages content
# https://gist.github.com/renyi/3596248
from mezzanine.conf import settings
from mezzanine.core.models import Slugged, MetaData, Displayable, Orderable, RichText
from mezzanine.core.fields import RichTextField

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