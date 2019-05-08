# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table(u'learn_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resmod_course', to=orm['learn.Course'])),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reslearn_module', to=orm['learn.Module'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('resourcetext', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'learn', ['Resource'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'learn_resource')


    models = {
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