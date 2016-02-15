# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stakeholders'
        db.create_table(u'pce_stakeholders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.PceVersion'])),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Stakeholders'])

        # Adding model 'StakeholdersFields'
        db.create_table(u'pce_stakeholdersfields', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('satkeholder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Stakeholders'])),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('interest', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('influence', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('importance', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('participant', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['StakeholdersFields'])


    def backwards(self, orm):
        # Deleting model 'Stakeholders'
        db.delete_table(u'pce_stakeholders')

        # Deleting model 'StakeholdersFields'
        db.delete_table(u'pce_stakeholdersfields')


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
            'Meta': {'object_name': 'User'},
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
        u'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        u'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.countrypage': {
            'Meta': {'ordering': "['name']", 'object_name': 'CountryPage', '_ormbases': [u'pages.Page']},
            'accepted_epporeport': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepted_epporeport_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cn_flag': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'cn_lat': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cn_long': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cn_map': ('django.db.models.fields.CharField', [], {'max_length': '550'}),
            'contact_point': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'country_slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cp_ncp_t_type': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '3'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'countryeditors+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'send_reminder': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'pages.page': {
            'Meta': {'ordering': "('titles',)", 'object_name': 'Page'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(2,)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        },
        u'pce.answerbase': {
            'Meta': {'object_name': 'AnswerBase'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Question']"}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Response']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'pce.answerinteger': {
            'Meta': {'object_name': 'AnswerInteger', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answerradio': {
            'Meta': {'object_name': 'AnswerRadio', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answerselect': {
            'Meta': {'object_name': 'AnswerSelect', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answerselectmultiple': {
            'Meta': {'object_name': 'AnswerSelectMultiple', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.answertext': {
            'Meta': {'object_name': 'AnswerText', '_ormbases': [u'pce.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pce.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'pce.membership1': {
            'Meta': {'object_name': 'Membership1'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.membership2': {
            'Meta': {'object_name': 'Membership2'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module': {
            'Meta': {'object_name': 'Module'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'pce.module1': {
            'Meta': {'object_name': 'Module1'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mod1_country'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_13': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_14': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_15': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_16': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_17': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_18': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_19': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_22': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'Membership_+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['pce.Membership1']"}),
            'm_23': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'Membership_+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['pce.Membership2']"}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_9': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module1aid': {
            'Meta': {'object_name': 'Module1Aid'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'donoragency': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"}),
            'titleprj': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module1majorcrops': {
            'Meta': {'object_name': 'Module1MajorCrops'},
            'consumption': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crops': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'germplasm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industrial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'propagation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wooden': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pce.module1majorexports': {
            'Meta': {'object_name': 'Module1MajorExports'},
            'consumption': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crops': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'germplasm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industrial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'propagation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wooden': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pce.module1majorimports': {
            'Meta': {'object_name': 'Module1MajorImports'},
            'consumption': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crops': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'germplasm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industrial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'propagation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wooden': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pce.module1majorpartenerexport': {
            'Meta': {'object_name': 'Module1MajorPartenerExport'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"})
        },
        u'pce.module1majorpartenerimport': {
            'Meta': {'object_name': 'Module1MajorPartenerImport'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module1']"})
        },
        u'pce.modulecategory': {
            'Meta': {'object_name': 'ModuleCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'pce.pceversion': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'PceVersion'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pceversion_author'", 'to': u"orm['auth.User']"}),
            'chosen_modules': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'modules'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['pce.Module']"}),
            'completed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pceversion_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'email_facilitator': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'email_pcemanager': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'file_designation': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            'firstname_facilitator': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_facilitated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastname_facilitator': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name_authority': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_pcemanager': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'projet_date_completation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title_pcemanager': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'version_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'pce.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Category']", 'null': 'True', 'blank': 'True'}),
            'choices': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module']"}),
            'question_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '200'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'pce.response': {
            'Meta': {'object_name': 'Response'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.CountryPage']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.TextField', [], {})
        },
        u'pce.stakeholders': {
            'Meta': {'object_name': 'Stakeholders'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.stakeholdersfields': {
            'Meta': {'object_name': 'StakeholdersFields'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'influence': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'interest': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'participant': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'role': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'satkeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Stakeholders']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pce']