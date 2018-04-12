from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404
from mezzanine.pages.models import Page, RichTextPage, Link
from iyph.models import IyphPost, IyphCategory,Chronology,IYPHToolBoxItem,IYPHToolBoxCategory,IYPHSteeringCommitteeResource
from iyph.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model
from django.views.generic import ListView,DetailView,TemplateView
User = get_user_model()


def iyph_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="iyph/iyph_post_list.html"):
    """
    Display a list of iyph posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``iyph/iyph_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    print(' --- SON qui!!!!!!!!!!')
    settings.use_editable()
    templates = []
    iyph_posts = IyphPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        iyph_posts = iyph_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        iyph_posts = iyph_posts.filter(publish_date__year=year)
        if month is not None:
            iyph_posts = iyph_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(IyphCategory, slug=category)
        iyph_posts = iyph_posts.filter(categories=category)
        templates.append(u"iyph/iyph_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        iyph_posts = iyph_posts.filter(user=author)
        templates.append(u"iyph/iyph_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    iyph_posts = iyph_posts.select_related("user").prefetch_related(*prefetch)
    iyph_posts = paginate(iyph_posts, request.GET.get("page", 1),
                          settings.IYPH_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
#    chronologies = Chronology.objects.all().order_by('publish_date', 'title')
#    data= ''
#    i=1
#    start_m=''
#    start_y=''
#    for chronology in chronologies:
#        start_d=chronology.publish_date.strftime("%d")
#        start_b=chronology.publish_date.strftime("%b")
#        if chronology.publish_date.strftime("%Y")==start_y and chronology.publish_date.strftime("%m") ==start_m:
#            i=i+1  
#        else: 
#            i=1    
#        start_m=chronology.publish_date.strftime("%m")
#        
#        start_y= chronology.publish_date.strftime("%Y")
#        end_d=int(start_d)+15
#        start=start_y+"-"+start_m+"-"+start_d
#        end=start_y+"-"+start_m+"-"+str(end_d)
#        title=start_b+' '+start_y
#        
#        chronology.publish_date.strftime("%b")
#        text="<a href='/iyph/chronology/list/"+chronology.slug+"'><b>"+chronology.title+"</b></a><br>"+chronology.summary
#        data= data+'{"start": "'+start+'","instant": false, "title": "'+title+'", "color": "045FB4","textColor": "red", "icon":"/static/img/dark-red-circle.png","caption": "'+chronology.title+'",  "trackNum": '+str(i)+',  "classname": "special_event2 aquamarine", "description": "'+text+'"},'                         
#        
#    data = data[:-1]
    
    context = {"iyph_posts": iyph_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author,}#"data": data
    templates.append(template)
    return render(request, templates, context)


def iyph_post_detail(request, slug, year=None, month=None, day=None,
                     template="iyph/iyph_post_detail.html"):
    """. Custom templates are checked for using the name
    ``iyph/iyph_post_detail_XXX.html`` where ``XXX`` is the iyph
    posts's slug.
    """
    iyph_posts = IyphPost.objects.published(
                                     for_user=request.user).select_related()
    iyph_post = get_object_or_404(iyph_posts, slug=slug)
    context = {"iyph_post": iyph_post, "editable_obj": iyph_post}
    templates = [u"iyph/iyph_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def iyph_post_feed(request, format, **kwargs):
    """
    iyph posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()



class ChronologyListView(ListView):
    """    chronology  """
    context_object_name = 'latest'
    
    model = Chronology
    date_field = 'publish_date'
    template_name = 'iyph/chronology_list.html'
    queryset = Chronology.objects.all().order_by('-publish_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 50
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ChronologyListView, self).get_context_data(**kwargs)

        chronologies = Chronology.objects.all().order_by('publish_date', 'title')
        data= ''
        i=1
        start_m=''
        start_y=''
        print(chronologies)
        for chronology in chronologies:
            start_d=chronology.publish_date.strftime("%d")
            start_b=chronology.publish_date.strftime("%b")
            if chronology.publish_date.strftime("%Y")==start_y and chronology.publish_date.strftime("%m") ==start_m:
                i=i+1  
            else: 
                i=1    
            start_m=chronology.publish_date.strftime("%m")

            start_y= chronology.publish_date.strftime("%Y")
            end_d=int(start_d)+15
            start=start_y+"-"+start_m+"-"+start_d
            end=start_y+"-"+start_m+"-"+str(end_d)
            title=start_b+' '+start_y

            chronology.publish_date.strftime("%b")
            text="<a href='/iyph/chronology/list/"+chronology.slug+"'><b>"+chronology.title+"</b></a><br>"+chronology.summary
            data= data+'{"start": "'+start+'","instant": false, "title": "'+title+'", "color": "045FB4","textColor": "red", "icon":"/static/img/dark-red-circle.png","caption": "'+chronology.title+'",  "trackNum": '+str(i)+',  "classname": "special_event2 aquamarine", "description": "'+text+'"},'                         

        data = data[:-1]
        context['data']  =data
        return context


class ChronologyDetailView(DetailView):
    """ chronology_detail page """
    model = Chronology
    context_object_name = 'chronology'
    template_name = 'iyph/chronology_detail.html'
    queryset = Chronology.objects.filter()
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ChronologyDetailView, self).get_context_data(**kwargs)
        p = get_object_or_404(Chronology, slug=self.kwargs['slug'])
        return context
    



class Page1View(TemplateView):
    """ 
    Individual PageView  
    """
    #template_name = 'iyphpages/richtextpage.html'
    template_name = 'iyph/resources_list.html'
    
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
        # page = get_object_or_404(RichTextPage, page_ptr_id=1065)
        #context['content']  =page.content
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

      
            aaa='<div><div class="span1" ><img src="/static/img/iyph-stc/elements/'+imgsrc+'.png" > </div>'
            aaa+='<div class="span11 docs">'
            aaa+='<p><strong>'+str(c)+'</strong></p>'
            items = iyphtoolboxitem.filter(categories=c).order_by('id')
            
            for itm in items:
                url=''
                if itm.url != "":
                    url=itm.url
                else:
                    url='/static/media/'+str(itm.file)
                aaa+="<p> <a href='"+str(url)+"'>"+str(itm.title)+"</a></p>"
            aaa+='</div></div>'
            
            results.append(aaa)
       
        context['results']  =results
        iyph_resources = IYPHSteeringCommitteeResource.objects.published().order_by('id')
        context['iyph_resources']  = list(iyph_resources[:100])

           

        return context

class Page2View(TemplateView):
    """ 
    Individual PageView  
    """
    template_name = 'iyph/resources_list_1.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
        iyph_resources = IYPHSteeringCommitteeResource.objects.published().order_by('id')
        context['iyph_resources']  = list(iyph_resources[:100])

        return context
    
def homeview(request, template="indexiyph.html"):
    """
    Display a list of iyph posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``iyph/iyph_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    print(' --- SON qui!!!!!!!!!!')
    context = {"iyph_posts": 'iyph_posts',}
   
    templates = []
    templates.append(template)
    return render(request, templates, context)
     
        