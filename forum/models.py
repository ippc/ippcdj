from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User, Group

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from django.core.exceptions import ValidationError

from mezzanine.utils.models import get_user_model_name
from mezzanine.blog.models import BlogPost
import os.path

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


class ForumPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A forum post.
    """
    categories = models.ManyToManyField("ForumCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="forumposts")
    
    
    allow_comments = models.BooleanField(verbose_name=_("Forum discussion OPEN for comments (to CLOSE the discussion un-check this)."),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("forum.ForumPost.featured_image", "forum"),
        format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)
    
    admin_thumb_field = "featured_image"
    
    users = models.ManyToManyField(User,
        verbose_name=_("Users this forum post is accessible to"),
        related_name='forumusers', blank=True, null=True)
    groups = models.ManyToManyField(Group,
        verbose_name=_("Groups this forum post is accessible to"),
        related_name='forumgroups', blank=True, null=True)
    login_required = models.BooleanField(verbose_name=_("Login required"),
                                         default=True)
    

    class Meta:
        verbose_name = _("Forum post")
        verbose_name_plural = _("Forum posts")
        ordering = ("-publish_date",)
        # south overrides syncdb, so the following perms are not created
        # unless we are starting the project from scratch.
        # solution: python manage.py syncdb --all
        # or
        # manage.py datamigration myapp add_perm_foo --freeze=contenttypes --freeze=auth
        # http://stackoverflow.com/questions/1742021/adding-new-custom-permissions-in-django
        permissions = ( 
            ("can_view", "View Forum Post"),
        )

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

def validate_file_extension(value):
    if not (value.name.endswith('.pdf') or value.name.endswith('.doc')or value.name.endswith('.txt')
        or value.name.endswith('.xls')   or value.name.endswith('.ppt') or value.name.endswith('.jpg')
        or value.name.endswith('.png') or value.name.endswith('.gif') or value.name.endswith('.xlsx')
        or value.name.endswith('.docx')or value.name.endswith('.pptx') or value.name.endswith('.zip')
        or value.name.endswith('.rar')):
        raise ValidationError(u'You can only upload files:  txt pdf ppt doc xls jpg png docx xlsx pptx zip rar.')
        
class ForumPost_Files(models.Model):
    forum_post = models.ForeignKey(ForumPost)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/forum/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]    
    
