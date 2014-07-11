from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to


class ForumPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A forum post.
    """

    categories = models.ManyToManyField("ForumCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="forumposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("forum.ForumPost.featured_image", "forum"),
        format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Forum post")
        verbose_name_plural = _("Forum posts")
        ordering = ("-publish_date",)

    @models.permalink
    def get_absolute_url(self):
        """
        URLs for forum posts can either be just their slug, or prefixed
        with a portion of the post's publish date, controlled by the
        setting ``FORUM_URLS_DATE_FORMAT``, which can contain the value
        ``year``, ``month``, or ``day``. Each of these maps to the name
        of the corresponding urlpattern, and if defined, we loop through
        each of these and build up the kwargs for the correct urlpattern.
        The order which we loop through them is important, since the
        order goes from least granualr (just year) to most granular
        (year/month/day).
        """
        url_name = "forum_post_detail"
        kwargs = {"slug": self.slug}
        date_parts = ("year", "month", "day")
        if settings.FORUM_URLS_DATE_FORMAT in date_parts:
            url_name = "forum_post_detail_%s" % settings.FORUM_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.FORUM_URLS_DATE_FORMAT:
                    break
        return (url_name, (), kwargs)

    # These methods are deprecated wrappers for keyword and category
    # access. They existed to support Django 1.3 with prefetch_related
    # not existing, which was therefore manually implemented in the
    # forum list views. All this is gone now, but the access methods
    # still exist for older templates.

    def category_list(self):
        from warnings import warn
        warn("forum_post.category_list in templates is deprecated"
             "use forum_post.categories.all which are prefetched")
        return getattr(self, "_categories", self.categories.all())

    def keyword_list(self):
        from warnings import warn
        warn("forum_post.keyword_list in templates is deprecated"
             "use the keywords_for template tag, as keywords are prefetched")
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords


class ForumCategory(Slugged):
    """
    A category for grouping forum posts into a series.
    """

    class Meta:
        verbose_name = _("Forum Category")
        verbose_name_plural = _("Forum Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("forum_post_list_category", (), {"category": self.slug})
