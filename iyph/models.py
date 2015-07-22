from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to


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
   