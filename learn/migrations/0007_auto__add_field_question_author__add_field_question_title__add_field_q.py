# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.author'
        db.add_column(u'learn_question', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='question_author', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Question.title'
       # db.add_column(u'learn_question', 'title',
       #               self.gf('django.db.models.fields.CharField')(max_length=250, null=True),
       #               keep_default=False)

        # Adding field 'Question.results'
       # db.add_column(u'learn_question', 'results',
       #               self.gf('django.db.models.fields.TextField')(null=True, blank=True),
#                      keep_default=False)


        # Changing field 'Question.q_summary'
  #      db.alter_column(u'learn_question', 'q_summary', self.gf('django.db.models.fields.TextField')(null=True))
 #       # Deleting field 'Quiz.lessontext'
   #     db.delete_column(u'learn_quiz', 'lessontext')

        # Adding field 'Quiz.quiztext'
    #    db.add_column(u'learn_quiz', 'quiztext',
     #                 self.gf('django.db.models.fields.TextField')(null=True, blank=True),
      #                keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.author'
        db.delete_column(u'learn_question', 'author_id')

        # Deleting field 'Question.title'
        db.delete_column(u'learn_question', 'title')

        # Deleting field 'Question.results'
        db.delete_column(u'learn_question', 'results')


        # Changing field 'Question.q_summary'
        db.alter_column(u'learn_question', 'q_summary', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))
        # Adding field 'Quiz.lessontext'
        db.add_column(u'learn_quiz', 'lessontext',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Quiz.quiztext'
        db.delete_column(u'learn_quiz', 'quiztext')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'ordering': "['username']", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'learn.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'learn_category'", 'to': u"orm['learn.Category']"}),
            'coursesummary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'enrolledusers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'enrolledusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.lesson': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Lesson'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'learnmod_course'", 'to': u"orm['learn.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessontext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'learn_module'", 'to': u"orm['learn.Module']"}),
            'nextpage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previouspage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'learn.module': {
            'Meta': {'object_name': 'Module'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'learn_course'", 'to': u"orm['learn.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulesummary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'nextmodule': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previousmodule': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.question': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Question'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_author'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'q_summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'q_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'que_answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz'", 'to': u"orm['learn.Quiz']"}),
            'results': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'learn.quiz': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Quiz'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz_course'", 'to': u"orm['learn.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz_module'", 'to': u"orm['learn.Module']"}),
            'quiztext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'learn.resource': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Resource'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resmod_course'", 'to': u"orm['learn.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reslearn_module'", 'to': u"orm['learn.Module']"}),
            'resourcetext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'learn.transcategory': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransCategory'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['learn.Category']"})
        },
        u'learn.transcourse': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransCourse'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['learn.Course']"})
        },
        u'learn.translesson': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransLesson'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tlessontext': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['learn.Lesson']"})
        },
        u'learn.transmodule': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransModule'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['learn.Module']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['learn']