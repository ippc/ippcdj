# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QuestionMultiVal.answer'
        db.add_column(u'learn_questionmultival', 'answer',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'QuestionMultiVal.answer'
        db.delete_column(u'learn_questionmultival', 'answer')


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
            'certificategrade': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'coursesummary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'enrolledusers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'enrolledusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'has_certificate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'modulesummary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'nextmodule': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previousmodule': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.question': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Question'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nextq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previousq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'q_summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'q_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz'", 'to': u"orm['learn.Quiz']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'learn.questionfield': {
            'Meta': {'object_name': 'QuestionField'},
            'answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['learn.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.questionm': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'QuestionM'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nextq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previousq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'q_summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'q_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quizm'", 'to': u"orm['learn.Quiz']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'learn.questionmultifield': {
            'Meta': {'object_name': 'QuestionMultiField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['learn.QuestionM']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.questionmultival': {
            'Meta': {'object_name': 'QuestionMultiVal'},
            'answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['learn.QuestionMultiField']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'learn.questionresult': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'QuestionResult'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'q_latest_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['learn.Question']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'userquestion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_user'", 'to': u"orm['auth.User']"})
        },
        u'learn.quiz': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Quiz'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz_course'", 'to': u"orm['learn.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz_module'", 'to': u"orm['learn.Module']"}),
            'quizgrade': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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