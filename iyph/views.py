from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404
from mezzanine.pages.models import Page, RichTextPage, Link
from django.template.defaultfilters import slugify  
from django.contrib.auth.models import User,Group
from iyph.models import IyphPost, IyphCategory,Chronology,IYPHToolBoxItem,IYPHToolBoxCategory,IYPHSteeringCommitteeResource,PhotoLibrary,Photo,IYPHPage,TransIYPHPage
from iyph.forms import ChronologyForm,PhotoForm,ChronologyFilesFormSet
from ippc.models import  IppcUserProfile, CountryPage
from iyph.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model
from django.views.generic import ListView,DetailView,TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.messages import info, error
from django.utils.translation import ugettext_lazy as _
User = get_user_model()
from django.http import HttpResponseRedirect
import random 
from django.core import mail

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
    queryset = Chronology.objects.all().order_by('-start_date', 'title')

    allow_future = False
    allow_empty = True
    paginate_by =100
    

    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ChronologyListView, self).get_context_data(**kwargs)
#        chronologies = Chronology.objects.all().order_by('-start_date', 'title')
#        if self.kwargs['type'] == '1':
#             chronologies = Chronology.objects.filter(programme_type=1).order_by('-start_date', 'title')
#        elif self.kwargs['type'] == '2':
#             chronologies = Chronology.objects.filter(programme_type=2).order_by('-start_date', 'title')
        chronologies = Chronology.objects.filter(programme_type=2).order_by('start_date', 'title')
        context['chronologies'] = chronologies
#        context['type']  =self.kwargs['type']
#        typeofview=''
#        if self.kwargs['view']!= None:
#            typeofview=self.kwargs['view']
#        else:
#            typeofview='all'
#        context['view']  =typeofview
#        
        cns= CountryPage.objects.all()
        maparray=[]

        tot_p=0
        for cn in cns:
              chronologies = Chronology.objects.filter(programme_type=2,country_id=cn.id)
              p=chronologies.count()
              tot_p+=p
              if p>0:
                  if cn>0:
                    detail_cron=''  
                    for chron in   chronologies:
                        #-
                        sM = chron.start_date.month
                        sY = chron.start_date.year

                        eM = chron.end_date.month
                        eY = chron.end_date.year
                        date_event=''
                        if sY == eY:
                            if eM==sM:
                              date_event=  str(chron.start_date.strftime('%d'))+' - '+ str(chron.end_date.strftime('%d %b %Y'))
                            else:  
                              date_event=  str(chron.start_date.strftime('%d %b'))+' - '+ str(chron.end_date.strftime('%d %b %Y'))
                        else:      
                              date_event=  str(chron.start_date.strftime('%d %b %Y'))+' - '+ str(chron.end_date.strftime('%d %b %Y'))
                        detail_cron=detail_cron+'<p style="color:#000;font-size:0.9rem">'+date_event+'<br><a href="/iyph/chronology/'+str(chron.slug)+'">'+chron.title+'</a> - '+chron.venue +'</p>'
                    
                 
                    maparray.append([str('<b>'+cn.name.encode('utf-8'))+'</b>:<br>'+str(detail_cron)+'',str(cn.cn_lat),str(cn.cn_long)])
                   
        
        context['map']=maparray    
 
#        chronologies = Chronology.objects.filter(programme_type=2)
#        text=''
#        start_d=''
#        for chronology in chronologies:
#            start_d=chronology.start_date.strftime("%d %b %Y")
#            text+='<li><div><time> '+start_d+' </time><a href="/iyph/chronology/'+chronology.slug+'">'+chronology.title+'</a><br>'+chronology.venue+', '+str(chronology.country)+'<br>'+chronology.summary+'</div></li>'
#            
#            
#        context['data']  =text
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
        
        sM = p.start_date.month
        sY = p.start_date.year

        eM = p.end_date.month
        eY = p.end_date.year
        date_event=''
        if sY == eY:
            if eM==sM:
              date_event=  str(p.start_date.strftime('%d'))+'-'+ str(p.end_date.strftime('%d %B %Y'))
            else:  
              date_event=  str(p.start_date.strftime('%d %b'))+'-'+ str(p.end_date.strftime('%d %b %Y'))
        else:      
              date_event=  str(p.start_date.strftime('%d %b %Y'))+' - '+ str(p.end_date.strftime('%d %b %Y'))

        context['date_event']=date_event             
                              
        return context
    


class Page1View(TemplateView):
    """ 
    Individual PageView  
    """
    template_name = 'iyph/resources_list_1.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
      
        iyph_resources1 = IYPHSteeringCommitteeResource.objects.published().order_by('id')
        iyph_resources = iyph_resources1.filter(res_type=1).order_by('id')
   
        context['iyph_resources']  = list(iyph_resources[:100])
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
        context['res_type']='1'
     

        return context
    


class Page2View(TemplateView):
    """ 
    Individual PageView  
    """
    template_name = 'iyph/resources_list_1.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
       
        iyph_resources1 = IYPHSteeringCommitteeResource.objects.published().order_by('id')
        iyph_resources = iyph_resources1.filter(res_type=2).order_by('id')
   
        context['iyph_resources']  = list(iyph_resources[:100])
       
       
        context['res_type']='2'
     

        return context    
    
def homeview(request, template="indexiyph.html"):
    """
    Display a list of iyph posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``iyph/iyph_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    
    context = {"iyph_posts": 'iyph_posts',}
   
    templates = []
    templates.append(template)
    return render(request, templates, context)
     

 
@login_required
@permission_required('iyph.add_chronology', login_url="/accounts/login/")
def chronology_create(request,type):
    """ Create chronology """
    user = request.user
    author = user
   
    form = ChronologyForm(request.POST,request.FILES)
       
    if request.method == "POST":
        f_form =ChronologyFilesFormSet(request.POST, request.FILES)
    
        if form.is_valid() and f_form.is_valid():
            new_chronology = form.save(commit=False)
            new_chronology.author = request.user
            new_chronology.chron_type = type
            form.save()
          
            f_form.instance = new_chronology
            f_form.save()
            
            info(request, _("Successfully created event."))
            
            return redirect("chronology-detail", slug=new_chronology.slug)
        else:
             return render_to_response('iyph/chronology_create_event.html', {'form': form,'f_form':f_form,'type':type},
             context_instance=RequestContext(request))
    else:
        form = ChronologyForm(instance=Chronology())
        f_form =ChronologyFilesFormSet(instance=Chronology())
      
    return render_to_response('iyph/chronology_create_event.html', {'form': form,'f_form':f_form,'type':type},
        context_instance=RequestContext(request))




# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('iyph.change_chronology', login_url="/accounts/login/")
def chronology_edit(request,  id=None, template_name='iyph/chronology_edit.html'):
    """ Edit chronology """
    user = request.user
    author = user
    
    if id:
        chronology = get_object_or_404(Chronology,  pk=id)
    
    else:
        chronology = Chronology(author=request.user)
       
  
    if request.POST:
      
        form =ChronologyForm(request.POST,request.FILES, instance=chronology)
        f_form =ChronologyFilesFormSet(request.POST, request.FILES,instance=chronology)
        if form.is_valid() and f_form.is_valid():
     
            form.save()
            f_form.instance = chronology
           
            f_form.save()
            info(request, _("Successfully updated event."))
            return redirect("chronology-detail",  slug=chronology.slug)
    else:
        form = ChronologyForm(instance=chronology)
        f_form =ChronologyFilesFormSet(instance=chronology)
        
    return render_to_response(template_name, {
        'form': form,'f_form':f_form, "chronology": chronology
    }, context_instance=RequestContext(request))

        

class PhotoLibraryView(DetailView):
    """
    PhotoLibraryView
        http://stackoverflow.com/questions/8547880/listing-object-with-specific-tag-using-django-taggit
        http://stackoverflow.com/a/7382708/412329
    """
    context_object_name = 'photolibrary'
    model = PhotoLibrary
    date_field = 'publish_date'
    template_name = 'iyph/photolibrary.html'
    queryset = PhotoLibrary.objects.all().order_by('-modify_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 500
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PhotoLibraryView, self).get_context_data(**kwargs)
        slug=self.kwargs['slug']
        if slug == 'pending-approval':
            queryset =Photo.objects.filter(status=1).order_by('-modify_date', 'title')
        else: 
            library=get_object_or_404(PhotoLibrary, slug=self.kwargs['slug'])
            print(library.id)
            if library.id == 2:
                 queryset =Photo.objects.filter(status=2,library_id=1, agree=1,exibition=1).order_by('-modify_date', 'title')
            elif library.id == 3:
                 queryset =Photo.objects.filter(status=2,library_id=1, agree=1,finalist=1).order_by('-prize', 'title')
            else:
                queryset =Photo.objects.filter(status=2,library_id=1, agree=1).order_by('-modify_date', 'title')
        
        context['photos']=queryset
        return context
    
class PhotoListView(ListView):
    """    UserAutoRegistration List view """
    context_object_name = 'latest'
    model = Photo
    date_field = 'date'
    template_name = 'iyph/photo_pendinglist.html'
    queryset = Photo.objects.all().order_by('-publish_date')
  
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PhotoListView, self).get_context_data(**kwargs)
        queryset =Photo.objects.filter(status=1).order_by('-modify_date', 'title')
        context['photos']=queryset
        return context   
    
class PhotoDetailView(DetailView):
    """ Photo detail page """
    model = Photo
    context_object_name = 'photo'
    template_name = 'iyphpages/photo_detail.html'
    queryset = Photo.objects.filter(status=2)
    
class PhotoHiddenDetailView(DetailView):
    """ Photo detail page """
    model = Photo
    context_object_name = 'photo'
    template_name = 'iyphpages/photo_detail.html'
    queryset = Photo.objects.filter()

#@login_required
#@permission_required('iyph.add_photo', login_url="/accounts/login/")
def photo_create(request):
    """ Create photo """
    form = PhotoForm(request.POST,request.FILES)
    if request.method == "POST":
        if form.is_valid() and request.POST['captcha'] ==  request.POST['result_element']:
            new_photo = form.save(commit=False)
            if new_photo.email == new_photo.emailconfirmation:
                new_photo.owner = request.user
                new_photo.status = 1
                new_photo.library_id=1

                form.save()

                info(request, _("Successfully submitted photo."))
                return HttpResponseRedirect("/iyph/photo-contest/")
            else: 
               return render_to_response('iyph/photo_create.html', {'form': form,'message':"ERROR: the 'Email address' and 'Email address confirmation' do not match."},
               context_instance=RequestContext(request))  
        else:
            error_captcha=''
            if not(request.POST['captcha'] == request.POST['result_element'] ) :
                error_captcha='error'
                  
            return render_to_response('iyph/photo_create.html', {'form': form,'x_element': request.POST['x_element'],'y_element': request.POST['y_element'],'result_element': request.POST['result_element'] ,'error_captcha':error_captcha},
             context_instance=RequestContext(request))
    else:
         x_element=random.randint(1,10)   
         y_element=random.randint(1,10)
         result_element=x_element+y_element
         
         form = PhotoForm(instance=Photo())
      
    return render_to_response('iyph/photo_create.html', {'form': form,'x_element':x_element,'y_element':y_element,'result_element':result_element},
        context_instance=RequestContext(request))

              

class IYPHPageView(DetailView):
    """
    IYPHPageView
        http://stackoverflow.com/questions/8547880/listing-object-with-specific-tag-using-django-taggit
        http://stackoverflow.com/a/7382708/412329
    """
    context_object_name = 'iyphpage'
    model = IYPHPage
    date_field = 'publish_date'
    template_name = 'iyph/iyphpage_detail.html'
    queryset = IYPHPage.objects.all().order_by('-modify_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 500
    #queryset = DraftProtocol.objects.all()
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(IYPHPageView, self).get_context_data(**kwargs)
        slug=self.kwargs['slug']
        langsel=self.request.LANGUAGE_CODE
       
        page=get_object_or_404(IYPHPage, slug=self.kwargs['slug'])
        page_title=page.title
        page_descr=page.short_description
        
        if  langsel!='en' and langsel!='':
                page_tra=TransIYPHPage.objects.filter(translation_id=page.id,lang=langsel)
                if page_tra:
                    page_title=page_tra[0].title
                    page_descr=page_tra[0].short_description
                
             
        context['page_title']=page_title
        context['page_descr']=page_descr
    
        return context
    