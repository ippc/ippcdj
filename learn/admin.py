
# https://gist.github.com/renyi/3596248
from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.models import Page, RichTextPage, Link
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import TabularDynamicInlineAdmin, StackedDynamicInlineAdmin,DisplayableAdmin, OwnableAdmin
from settings import ALLOWED_HOSTS 

from .models import Category, Course,Lesson,Module,Resource,Question,Quiz,QuestionField,QuestionMultiField,QuestionMultiVal,QuestionM


from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User,Group
from django import forms
from django.core import mail
from django.core.mail import send_mail

from django_markdown.admin import MarkdownModelAdmin

from django.shortcuts import get_object_or_404

import autocomplete_light
#import autocomplete_light_registry

from django_markdown.widgets import MarkdownWidget



class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title',  )
    list_filter = ('title', )
    search_fields = ('title', )
    #prepopulated_fields = { 'title': ['title'] }
  
admin.site.register(Category, CategoryAdmin)

class CourseAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'category', 'datecreated' )
    list_filter = ('title', 'category', )
    search_fields = ('title', 'category', )
    #prepopulated_fields = { 'title': ['title'] }
admin.site.register(Course, CourseAdmin)

   
class ModuleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id','title', 'course','previousmodule','nextmodule' )
   
    list_filter = ('title', 'course',  )
    search_fields = ('title', 'course', )
   # prepopulated_fields = { 'title': ['title'] }
 
admin.site.register(Module, ModuleAdmin)


class LessonAdmin(admin.ModelAdmin):
    save_on_top = True
    
    list_display = ('id','title', 'course', 'module','previouspage','nextpage' )
 
    list_filter = ('title', 'course', 'module', )
    search_fields = ('title', 'course', 'module', )
    #prepopulated_fields = { 'title': ['title'] }
   
admin.site.register(Lesson, LessonAdmin)

class ResourceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'course', 'module',)
   
    list_filter = ('title', 'course', 'module', )
    search_fields = ('title', 'course', 'module', )
   
admin.site.register(Resource, ResourceAdmin)

class QuizAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'module',)
   
    list_filter = ('title', 'module', )
    search_fields = ('title',  'module', )
   
admin.site.register(Quiz, QuizAdmin)



class QuestionFieldInline(admin.TabularInline):
    model = QuestionField
    formset = inlineformset_factory(Question,  QuestionField,extra=1)
   


class QuestionAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [QuestionFieldInline, ]
    list_display = ('title','quiz','id','previousq','nextq' )
   
    list_filter = ('title', 'quiz', )
    search_fields = ('title',  'quiz', )
   
admin.site.register(Question, QuestionAdmin)

                    

class QuestionMultiValInline(admin.TabularInline):
    model = QuestionMultiVal
    formset = inlineformset_factory(QuestionMultiField,  QuestionMultiVal,extra=1)
  
   
   
class QuestionMultiFieldAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [QuestionMultiValInline, ]
    list_display = ('text' ,'id')
   
    list_filter = ('text', )
    search_fields = ('text', )
   
admin.site.register(QuestionMultiField, QuestionMultiFieldAdmin)

    
    
class QuestionMultiFieldInline(admin.TabularInline):
    model = QuestionMultiField
    formset = inlineformset_factory(QuestionM,  QuestionMultiField,extra=1)
   




class QuestionMAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [QuestionMultiFieldInline, ]
    list_display = ('title','quiz' )
   
    list_filter = ('title', 'quiz', )
    search_fields = ('title',  'quiz', )
   
admin.site.register(QuestionM, QuestionMAdmin)

    

                    







