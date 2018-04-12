from datetime import datetime

from django.db.models import Count, Q

from iyph.forms import IyphPostForm
from iyph.models import IyphPost, IyphCategory, IYPHSteeringCommitteeResource,IYPHToolBoxItem,IYPHToolBoxCategory,Chronology
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = template.Library()


@register.as_tag
def iyph_months(*args):
    """
    Put a list of dates for iyph posts into the template context.
    """
    dates = IyphPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def iyph_categories(*args):
    """
    Put a list of categories for iyph posts into the template context.
    """
    posts = IyphPost.objects.published()
    categories = IyphCategory.objects.filter(iyphposts__in=posts)
    return list(categories.annotate(post_count=Count("iyphposts")))


@register.as_tag
def iyph_authors(*args):
    """
    Put a list of authors (users) for iyph posts into the template context.
    """
    iyph_posts = IyphPost.objects.published()
    authors = User.objects.filter(iyphposts__in=iyph_posts)
    return list(authors.annotate(post_count=Count("iyphposts")))


@register.as_tag
def iyph_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published iyph posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% iyph_recent_posts 5 as recent_posts %}
        {% iyph_recent_posts limit=5 tag="django" as recent_posts %}
        {% iyph_recent_posts limit=5 category="python" as recent_posts %}
        {% iyph_recent_posts 5 username=admin as recent_posts %}

    """
    iyph_posts = IyphPost.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            iyph_posts = iyph_posts.filter(keywords__in=tag.assignments.all())
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = IyphCategory.objects.get(title_or_slug(category))
            iyph_posts = iyph_posts.filter(categories=category)
        except IyphCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            iyph_posts = iyph_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(iyph_posts[:limit])

@register.as_tag
def iyph_recent_resources():
    """
    Put a list of recently published iyph_recent_resources   into the template
    context. 

    Usage::

        {% iyph_recent_resources 5 as iyph_recent_resources %}
     
    """
    iyph_resources = IYPHSteeringCommitteeResource.objects.published().order_by('id')
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    
    return list(iyph_resources[:100])

@register.as_tag
def iyph_recent_toolboxitem():
    """
    Put a list of recently published iyph_recent_resources   into the template
    context. 

    Usage::

        {% iyph_recent_toolboxitem 5 as sss %}
     
    """
    iyph_toolboxitem = IYPHToolBoxItem.objects.published()
    
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
   
    return list(iyph_resources[:100])
@register.as_tag
def iyph_tool_categories(*args):
    """
    Put a list of categories for iyph posts into the template context.
    """
    results=[]
    aaa=''
    iyphtoolboxitem = IYPHToolBoxItem.objects.published()
    categories = IYPHToolBoxCategory.objects.all().order_by('id')
    h=0
    for c in categories:
        imgsrc=''
        if c.title=='Advocacy':
            imgsrc='3docs'
        elif c.title=='Presentations':
            imgsrc='4presentation'
        elif c.title=='Videos':
            imgsrc='5videos'
        elif c.title=='Articles':
            imgsrc='6articles'
         
        if h==0:
           aaa='<div class="span6 resources box" style="background-color: #efefef; margin-left:0;" >'
        elif h ==1:
            aaa='<div class="span6 resources box" style="background-color: #efefef;" >'
        elif h ==2:
            aaa='<div class="span6 resources box" style="background-color: #efefef; margin-left:0;" >'
        elif h ==3:
            aaa='<div class="span6 resources box" style="background-color: #efefef;" >'
        
        aaa+='<div class="span2" ><img src="/static/img/iyph-stc/elements/'+imgsrc+'.png" > </div>'
        aaa+='<div class="span10 docs">'
        aaa+='<p><strong>'+str(c)+'</strong></p>'
        items = iyphtoolboxitem.filter(categories=c).order_by('id')
        y=0
        for itm in items:
            url=''
            if itm.url != "":
                url=itm.url
            else:
                url='/static/media/'+str(itm.file)
            if y<3:
                aaa+="<p> <a href='"+str(url)+"'>"+str(itm.title)+"</a></p>"
            y+=1
             
        aaa=aaa+'<p class="more"><a href="/iyph/iyph-toolbox/">[... more]</a></p></div> '
        results.append(aaa)
        h+=1
    return results

@register.as_tag
def iyph_recent_chronology():
    """
    Put a list of recently published iyph_recentchronology   into the template
    context. 

    Usage::

        {% iyph_recent_resources 5 as iyph_recent_resources %}
     
    """
    iyph_chronology = Chronology.objects.published().order_by('id')
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
   
    return list(iyph_chronology[:3])

@register.inclusion_tag("admin/includes/quick_iyph.html", takes_context=True)
def quick_iyph(context):
    """
    Admin dashboard tag for the quick iyph form.
    """
    context["form"] = IyphPostForm()
    return context
# https://gist.github.com/renyi/3596248
from django import template
from django.utils import translation

from mezzanine.conf import settings


@register.filter
def get_object_translation(obj):
    # get current language
    lang = translation.get_language()

    try:
        # returns object with current translation
        for i in obj.translation.all():
            if i.lang == lang:
                return i
    except:
        pass

    # returns object without translation
    return obj