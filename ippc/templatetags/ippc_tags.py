from django.template import Library, Node
from django.db.models import get_model
from .translate_tags import get_object_translation
register = Library()

# http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/     
class LatestContentNode(Node):
    """
    Template tag, which lets us fetch any number of objects 
    from any installed model and store them in any 
    context variable we want. 
     
    Call it like this:

    {% get_latest ApplicationName.ModelName 5 as some_variable_name %}

    Eg1:

    {% get_latest weblog.Entry 10 as latest_entries %}

    Eg2:

    {% get_latest comments.Comment 5 as recent_comments %}
    
    """
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)


from mezzanine.pages.models import Page, RichTextPage
from mezzanine.core.templatetags.mezzanine_tags import richtext_filter
from ippc.templatetags.ippc_tags import get_object_translation
from ippc.models import TransRichTextPage
# http://stackoverflow.com/a/13927772
# show specific page in template
@register.simple_tag
def get_page(slug, attr):
    # page = richtext_filter(get_object_translation(getattr(RichTextPage.objects.get(pk=int(pk)), attr)))
    page = get_object_translation(RichTextPage.objects.get(slug=slug))
    return richtext_filter(page.content)

# https://groups.google.com/forum/#!topic/mezzanine-users/UJsHUtv8FUg
# http://stackoverflow.com/questions/4577513/how-do-i-change-a-django-template-based-on-the-users-group#answer-8826722
# https://github.com/lukaszb/django-guardian
# @register.filter
# def can_view(user, page):
#     content_model = page.get_content_model()
#     return user.has_perm('can_view', content_model)