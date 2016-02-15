# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PceVersion'
        db.create_table(u'pce_pceversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pceversion_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pceversion_author', to=orm['auth.User'])),
            ('version_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('completed_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('projet_date_completation', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name_authority', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('file_designation', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
            ('name_pcemanager', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_pcemanager', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('email_pcemanager', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('is_facilitated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('firstname_facilitator', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('lastname_facilitator', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('email_facilitator', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('chosen_modules', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed1_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed1_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed1_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed2_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed2_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed2_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed3_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed3_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed3_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed4_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed4_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed4_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed5_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed5_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed5_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed6_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed6_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed6_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed7_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed7_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed7_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed8_firstname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed8_lastname', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ed8_email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['PceVersion'])

        # Adding model 'Membership1'
        db.create_table(u'pce_membership1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['Membership1'])

        # Adding model 'Membership2'
        db.create_table(u'pce_membership2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['Membership2'])

        # Adding model 'Module1'
        db.create_table(u'pce_module1', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mod1_country', to=orm['ippc.CountryPage'])),
            ('region', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_9', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_13', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_14', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_15', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_16', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_17', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_18', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_19', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module1'])

        # Adding M2M table for field m_22 on 'Module1'
        m2m_table_name = db.shorten_name(u'pce_module1_m_22')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module1', models.ForeignKey(orm[u'pce.module1'], null=False)),
            ('membership1', models.ForeignKey(orm[u'pce.membership1'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module1_id', 'membership1_id'])

        # Adding M2M table for field m_23 on 'Module1'
        m2m_table_name = db.shorten_name(u'pce_module1_m_23')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module1', models.ForeignKey(orm[u'pce.module1'], null=False)),
            ('membership2', models.ForeignKey(orm[u'pce.membership2'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module1_id', 'membership2_id'])

        # Adding model 'Module1Aid'
        db.create_table(u'pce_module1aid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('donoragency', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('titleprj', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module1Aid'])

        # Adding model 'Module1MajorCrops'
        db.create_table(u'pce_module1majorcrops', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('crops', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('propagation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('germplasm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consumption', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wooden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('industrial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module1MajorCrops'])

        # Adding model 'Module1MajorImports'
        db.create_table(u'pce_module1majorimports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('crops', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('propagation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('germplasm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consumption', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wooden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('industrial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module1MajorImports'])

        # Adding model 'Module1MajorExports'
        db.create_table(u'pce_module1majorexports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('crops', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('propagation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('germplasm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consumption', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wooden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('industrial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module1MajorExports'])

        # Adding model 'Module1MajorPartenerImport'
        db.create_table(u'pce_module1majorpartenerimport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module1MajorPartenerImport'])

        # Adding model 'Module1MajorPartenerExport'
        db.create_table(u'pce_module1majorpartenerexport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module1'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module1MajorPartenerExport'])

        # Adding model 'Module2'
        db.create_table(u'pce_module2', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_7', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_8', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_9', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_10', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_11', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_12', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_13', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_14', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_15', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_24', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_25', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_31', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_33', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_34', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_35', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_36', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_37', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_38', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_39', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_40', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_41', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_42', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_43', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_44', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_45', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_46', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_47', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_48', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_49', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_50', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_51', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_52', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_53', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_54', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_55', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_56', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_57', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_58', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_59', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_60', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_61', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_62', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_63', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_64', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_65', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_66', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_67', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_68', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_69', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_70', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_71', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_72', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_73', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_74', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_75', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_76', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_77', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_78', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_79', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_80', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_81', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_82', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_83', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_84', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_85', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_86', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_87', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_88', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_89', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_90', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_91', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_92', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_93', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_94', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_95', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_96', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_97', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_98', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_99', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_100', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_101', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_102', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_103', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_104', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_105', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_106', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_107', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_108', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_109', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_110', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_111', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_112', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_113', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_114', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_115', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_116', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_117', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_118', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_119', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_120', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_121', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_122', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module2'])

        # Adding model 'Module2Weaknesses'
        db.create_table(u'pce_module2weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module2', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module2'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module2Weaknesses'])

        # Adding model 'M3_1'
        db.create_table(u'pce_m3_1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_1'])

        # Adding model 'M3_3'
        db.create_table(u'pce_m3_3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_3'])

        # Adding model 'M3_9'
        db.create_table(u'pce_m3_9', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_9'])

        # Adding model 'M3_10'
        db.create_table(u'pce_m3_10', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_10'])

        # Adding model 'M3_14'
        db.create_table(u'pce_m3_14', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_14'])

        # Adding model 'M3_15'
        db.create_table(u'pce_m3_15', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_15'])

        # Adding model 'M3_16'
        db.create_table(u'pce_m3_16', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_16'])

        # Adding model 'M3_17'
        db.create_table(u'pce_m3_17', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M3_17'])

        # Adding model 'Module3'
        db.create_table(u'pce_module3', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_7', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_8', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_11', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_12', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_13', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_18', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_19', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_20', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_22', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_23', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_32', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module3'])

        # Adding M2M table for field m_1 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_1')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_1', models.ForeignKey(orm[u'pce.m3_1'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_1_id'])

        # Adding M2M table for field m_3 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_3')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_3', models.ForeignKey(orm[u'pce.m3_3'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_3_id'])

        # Adding M2M table for field m_9 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_9')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_9', models.ForeignKey(orm[u'pce.m3_9'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_9_id'])

        # Adding M2M table for field m_10 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_10')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_10', models.ForeignKey(orm[u'pce.m3_10'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_10_id'])

        # Adding M2M table for field m_14 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_14')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_14', models.ForeignKey(orm[u'pce.m3_14'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_14_id'])

        # Adding M2M table for field m_15 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_15')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_15', models.ForeignKey(orm[u'pce.m3_15'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_15_id'])

        # Adding M2M table for field m_16 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_16')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_16', models.ForeignKey(orm[u'pce.m3_16'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_16_id'])

        # Adding M2M table for field m_17 on 'Module3'
        m2m_table_name = db.shorten_name(u'pce_module3_m_17')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module3', models.ForeignKey(orm[u'pce.module3'], null=False)),
            ('m3_17', models.ForeignKey(orm[u'pce.m3_17'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module3_id', 'm3_17_id'])

        # Adding model 'Module3Grid'
        db.create_table(u'pce_module3grid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module3', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module3'])),
            ('verylow', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('low', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('medium', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('high', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('veryhigh', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module3Grid'])

        # Adding model 'Module3Weaknesses'
        db.create_table(u'pce_module3weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module3', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module3'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module3Weaknesses'])

        # Adding model 'Module4'
        db.create_table(u'pce_module4', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_4', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_5', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_6', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_11', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_12', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_13', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_25', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_28', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_31', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_33', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module4'])

        # Adding model 'Module4Weaknesses'
        db.create_table(u'pce_module4weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module4', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module4'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module4Weaknesses'])

        # Adding model 'M5_3'
        db.create_table(u'pce_m5_3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M5_3'])

        # Adding model 'Module5'
        db.create_table(u'pce_module5', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_17', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_18', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_19', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_20', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_21', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module5'])

        # Adding M2M table for field m_3 on 'Module5'
        m2m_table_name = db.shorten_name(u'pce_module5_m_3')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module5', models.ForeignKey(orm[u'pce.module5'], null=False)),
            ('m5_3', models.ForeignKey(orm[u'pce.m5_3'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module5_id', 'm5_3_id'])

        # Adding model 'Module5Weaknesses'
        db.create_table(u'pce_module5weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module5', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module5'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module5Weaknesses'])

        # Adding model 'Module6'
        db.create_table(u'pce_module6', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_9', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_17', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_22', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_23', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_28', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_29', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_30', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_31', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_32', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_33', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_34', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_35', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_36', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module6'])

        # Adding model 'Module6Weaknesses'
        db.create_table(u'pce_module6weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module6', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module6'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module6Weaknesses'])

        # Adding model 'Module7'
        db.create_table(u'pce_module7', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_12', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_22', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_26', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_27', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_31', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_33', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_34', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_35', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_36', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_38', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_40', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_42', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_44', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_46', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_47', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_48', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_49', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_50', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_51', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_52', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_53', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_54', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_55', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_56', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_57', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_58', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_59', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_60', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_61', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_62', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_63', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_64', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_65', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_66', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_67', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_68', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module7'])

        # Adding model 'Module7Grid'
        db.create_table(u'pce_module7grid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('salaries', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('equipment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('supplies', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('materials', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('fixedcosts', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('operationalcosts', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module7Grid'])

        # Adding model 'Module7Matrix23'
        db.create_table(u'pce_module7matrix23', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('averagelab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('managers', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module7Matrix23'])

        # Adding model 'Module7Matrix37'
        db.create_table(u'pce_module7matrix37', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('navailable', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('qaulity', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('required', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module7Matrix37'])

        # Adding model 'Module7Matrix39'
        db.create_table(u'pce_module7matrix39', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('navailable', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('qaulity', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('required', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module7Matrix39'])

        # Adding model 'Module7Matrix41'
        db.create_table(u'pce_module7matrix41', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('navailable', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('qaulity', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('required', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module7Matrix41'])

        # Adding model 'Module7Matrix43'
        db.create_table(u'pce_module7matrix43', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('navailable', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('qaulity', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('required', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module7Matrix43'])

        # Adding model 'Module7Matrix45'
        db.create_table(u'pce_module7matrix45', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('navailable', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('qaulity', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('required', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module7Matrix45'])

        # Adding model 'Module7Weaknesses'
        db.create_table(u'pce_module7weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module7', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module7'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module7Weaknesses'])

        # Adding model 'M8_17'
        db.create_table(u'pce_m8_17', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'pce', ['M8_17'])

        # Adding model 'Module8'
        db.create_table(u'pce_module8', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_9', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_26', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_27', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_31', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_32', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_33', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_34', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_35', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_36', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_37', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_38', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_39', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_40', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_41', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_42', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_43', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_44', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module8'])

        # Adding M2M table for field m_17 on 'Module8'
        m2m_table_name = db.shorten_name(u'pce_module8_m_17')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module8', models.ForeignKey(orm[u'pce.module8'], null=False)),
            ('m8_17', models.ForeignKey(orm[u'pce.m8_17'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module8_id', 'm8_17_id'])

        # Adding model 'Module8Grid3'
        db.create_table(u'pce_module8grid3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module8', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module8'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module8Grid3'])

        # Adding model 'Module8Grid18'
        db.create_table(u'pce_module8grid18', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module8', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module8'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c6', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module8Grid18'])

        # Adding model 'Module8Matrix30'
        db.create_table(u'pce_module8matrix30', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module8', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module8'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('averagelab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('managers', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module8Matrix30'])

        # Adding model 'Module8Weaknesses'
        db.create_table(u'pce_module8weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module8', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module8'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module8Weaknesses'])

        # Adding model 'Module9'
        db.create_table(u'pce_module9', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_25', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_33', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_34', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_36', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_37', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_38', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_39', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_40', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_41', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_42', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_43', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_44', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_45', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_46', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module9'])

        # Adding model 'Module9Grid1'
        db.create_table(u'pce_module9grid1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module9', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module9'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module9Grid1'])

        # Adding model 'Module9Grid5'
        db.create_table(u'pce_module9grid5', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module9', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module9'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module9Grid5'])

        # Adding model 'Module9Grid31'
        db.create_table(u'pce_module9grid31', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module9', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module9'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module9Grid31'])

        # Adding model 'Module9Matrix35'
        db.create_table(u'pce_module9matrix35', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module9', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module9'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('averagelab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('managers', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module9Matrix35'])

        # Adding model 'Module9Weaknesses'
        db.create_table(u'pce_module9weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module9', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module9'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module9Weaknesses'])

        # Adding model 'Module10'
        db.create_table(u'pce_module10', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_9', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_25', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_34', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_35', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_36', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_38', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_39', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_40', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_41', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_42', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_43', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_44', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_48', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_49', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_50', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_51', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_52', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_53', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_54', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_55', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_56', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_57', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_58', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_59', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_60', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module10'])

        # Adding model 'Module10Grid23'
        db.create_table(u'pce_module10grid23', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module10Grid23'])

        # Adding model 'Module10Grid31'
        db.create_table(u'pce_module10grid31', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module10Grid31'])

        # Adding model 'Module10Grid33'
        db.create_table(u'pce_module10grid33', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module10Grid33'])

        # Adding model 'Module10Grid37'
        db.create_table(u'pce_module10grid37', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c8', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module10Grid37'])

        # Adding model 'Module10Grid45'
        db.create_table(u'pce_module10grid45', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module10Grid45'])

        # Adding model 'Module10Grid46'
        db.create_table(u'pce_module10grid46', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module10Grid46'])

        # Adding model 'Module10Matrix_47'
        db.create_table(u'pce_module10matrix_47', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('averagelab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('supstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('technical', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('managers', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module10Matrix_47'])

        # Adding model 'Module10Weaknesses'
        db.create_table(u'pce_module10weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module10', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module10'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module10Weaknesses'])

        # Adding model 'Module11'
        db.create_table(u'pce_module11', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_8', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_22', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_25', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_29', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_30', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_31', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_34', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_35', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_36', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_37', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_38', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_39', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_40', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_41', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_43', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_44', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_45', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_46', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_47', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_48', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_49', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_50', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_51', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_52', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_53', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_54', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_55', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_56', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_57', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_58', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_59', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_60', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_61', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_62', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_63', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_65', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_66', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_67', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module11'])

        # Adding model 'Module11Grid2'
        db.create_table(u'pce_module11grid2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module11Grid2'])

        # Adding model 'Module11Grid3'
        db.create_table(u'pce_module11grid3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module11Grid3'])

        # Adding model 'Module11Grid12'
        db.create_table(u'pce_module11grid12', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c4', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c5', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module11Grid12'])

        # Adding model 'Module11Grid14'
        db.create_table(u'pce_module11grid14', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c4', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c5', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c6', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module11Grid14'])

        # Adding model 'Module11Grid33'
        db.create_table(u'pce_module11grid33', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c4', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module11Grid33'])

        # Adding model 'Module11Matrix42'
        db.create_table(u'pce_module11matrix42', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module11Matrix42'])

        # Adding model 'Module11Weaknesses'
        db.create_table(u'pce_module11weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module11', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module11'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module11Weaknesses'])

        # Adding model 'Module12'
        db.create_table(u'pce_module12', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_8', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_23', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_26', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_27', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_31', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_32', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_33', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module12'])

        # Adding model 'Module12Grid2'
        db.create_table(u'pce_module12grid2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module12', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module12'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module12Grid2'])

        # Adding model 'Module12Grid3'
        db.create_table(u'pce_module12grid3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module12', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module12'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module12Grid3'])

        # Adding model 'Module12Grid_29'
        db.create_table(u'pce_module12grid_29', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Module12', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module12'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c4', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module12Grid_29'])

        # Adding model 'Module12Matrix22'
        db.create_table(u'pce_module12matrix22', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module12', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module12'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('averagelab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('managers', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module12Matrix22'])

        # Adding model 'Module12Weaknesses'
        db.create_table(u'pce_module12weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module12', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module12'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module12Weaknesses'])

        # Adding model 'Module13'
        db.create_table(u'pce_module13', (
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
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('m_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_7', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_8', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_9', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_10', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_11', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_12', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_13', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_14', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_15', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_16', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_17', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_19', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_20', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_21', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_23', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_24', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_25', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_26', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_27', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_28', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_30', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_32', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_33', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_34', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_35', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_36', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_37', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_38', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_39', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_40', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_41', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_42', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_43', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_44', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_45', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_46', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_48', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_49', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_50', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_51', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_52', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_53', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_54', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_55', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_56', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_57', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_58', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_59', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_60', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_61', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_62', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_63', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('m_64', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_65', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['Module13'])

        # Adding model 'Module13Grid2'
        db.create_table(u'pce_module13grid2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module13Grid2'])

        # Adding model 'Module13Grid3'
        db.create_table(u'pce_module13grid3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('c1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('c4', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pce', ['Module13Grid3'])

        # Adding model 'Module13Grid22'
        db.create_table(u'pce_module13grid22', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module13Grid22'])

        # Adding model 'Module13Grid29'
        db.create_table(u'pce_module13grid29', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c4', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c5', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c6', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c7', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c8', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c9', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c10', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c11', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c12', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module13Grid29'])

        # Adding model 'Module13Grid31'
        db.create_table(u'pce_module13grid31', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('c1', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c2', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c3', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c4', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('c5', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module13Grid31'])

        # Adding model 'Module13Matrix47'
        db.create_table(u'pce_module13matrix47', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('nstaff', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('average', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('nstafflab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('averagelab', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('managers', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('support', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['Module13Matrix47'])

        # Adding model 'Module13Weaknesses'
        db.create_table(u'pce_module13weaknesses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module13', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Module13'])),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w4', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('w5', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['Module13Weaknesses'])

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
            ('stakeholder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.Stakeholders'])),
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

        # Adding model 'ProblemAnalysis'
        db.create_table(u'pce_problemanalysis', (
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
            ('cause_a_1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_b_1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('w_1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_a_1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_b_1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_a_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_b_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('w_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_a_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_b_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_a_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_b_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('w_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_a_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_b_3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_a_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_b_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('w_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_a_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_b_4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_a_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cause_b_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('w_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_a_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('consequence_b_5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['ProblemAnalysis'])

        # Adding model 'SwotAnalysis'
        db.create_table(u'pce_swotanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.PceVersion'])),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['SwotAnalysis'])

        # Adding model 'SwotAnalysis1'
        db.create_table(u'pce_swotanalysis1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('swotanalysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.SwotAnalysis'])),
            ('strengths', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opportunities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('threats', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('actions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['SwotAnalysis1'])

        # Adding model 'SwotAnalysis2'
        db.create_table(u'pce_swotanalysis2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('swotanalysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.SwotAnalysis'])),
            ('strengths', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opportunities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('threats', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('actions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['SwotAnalysis2'])

        # Adding model 'SwotAnalysis3'
        db.create_table(u'pce_swotanalysis3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('swotanalysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.SwotAnalysis'])),
            ('strengths', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opportunities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('threats', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('actions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['SwotAnalysis3'])

        # Adding model 'SwotAnalysis4'
        db.create_table(u'pce_swotanalysis4', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('swotanalysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.SwotAnalysis'])),
            ('strengths', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opportunities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('threats', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('actions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['SwotAnalysis4'])

        # Adding model 'SwotAnalysis5'
        db.create_table(u'pce_swotanalysis5', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('swotanalysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.SwotAnalysis'])),
            ('strengths', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opportunities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('threats', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('actions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=None)),
        ))
        db.send_create_signal(u'pce', ['SwotAnalysis5'])

        # Adding model 'LogicalFramework'
        db.create_table(u'pce_logicalframework', (
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
            ('objective', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keyindicator', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('verification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assumptions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('output1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keyindicator1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('verification1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assumptions1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('output2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keyindicator2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('verification2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assumptions2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('output3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keyindicator3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('verification3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assumptions3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('output4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keyindicator4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('verification4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assumptions4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('output5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keyindicator5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('verification5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assumptions5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'pce', ['LogicalFramework'])

        # Adding model 'LogicalFrameworkAct1'
        db.create_table(u'pce_logicalframeworkact1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logicalframework', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.LogicalFramework'])),
            ('activity1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sourcverification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['LogicalFrameworkAct1'])

        # Adding model 'LogicalFrameworkAct2'
        db.create_table(u'pce_logicalframeworkact2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logicalframework', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.LogicalFramework'])),
            ('activity2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sourcverification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['LogicalFrameworkAct2'])

        # Adding model 'LogicalFrameworkAct3'
        db.create_table(u'pce_logicalframeworkact3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logicalframework', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.LogicalFramework'])),
            ('activity3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sourcverification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['LogicalFrameworkAct3'])

        # Adding model 'LogicalFrameworkAct4'
        db.create_table(u'pce_logicalframeworkact4', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logicalframework', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.LogicalFramework'])),
            ('activity4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sourcverification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['LogicalFrameworkAct4'])

        # Adding model 'LogicalFrameworkAct5'
        db.create_table(u'pce_logicalframeworkact5', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logicalframework', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pce.LogicalFramework'])),
            ('activity5', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sourcverification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pce', ['LogicalFrameworkAct5'])


    def backwards(self, orm):
        # Deleting model 'PceVersion'
        db.delete_table(u'pce_pceversion')

        # Deleting model 'Membership1'
        db.delete_table(u'pce_membership1')

        # Deleting model 'Membership2'
        db.delete_table(u'pce_membership2')

        # Deleting model 'Module1'
        db.delete_table(u'pce_module1')

        # Removing M2M table for field m_22 on 'Module1'
        db.delete_table(db.shorten_name(u'pce_module1_m_22'))

        # Removing M2M table for field m_23 on 'Module1'
        db.delete_table(db.shorten_name(u'pce_module1_m_23'))

        # Deleting model 'Module1Aid'
        db.delete_table(u'pce_module1aid')

        # Deleting model 'Module1MajorCrops'
        db.delete_table(u'pce_module1majorcrops')

        # Deleting model 'Module1MajorImports'
        db.delete_table(u'pce_module1majorimports')

        # Deleting model 'Module1MajorExports'
        db.delete_table(u'pce_module1majorexports')

        # Deleting model 'Module1MajorPartenerImport'
        db.delete_table(u'pce_module1majorpartenerimport')

        # Deleting model 'Module1MajorPartenerExport'
        db.delete_table(u'pce_module1majorpartenerexport')

        # Deleting model 'Module2'
        db.delete_table(u'pce_module2')

        # Deleting model 'Module2Weaknesses'
        db.delete_table(u'pce_module2weaknesses')

        # Deleting model 'M3_1'
        db.delete_table(u'pce_m3_1')

        # Deleting model 'M3_3'
        db.delete_table(u'pce_m3_3')

        # Deleting model 'M3_9'
        db.delete_table(u'pce_m3_9')

        # Deleting model 'M3_10'
        db.delete_table(u'pce_m3_10')

        # Deleting model 'M3_14'
        db.delete_table(u'pce_m3_14')

        # Deleting model 'M3_15'
        db.delete_table(u'pce_m3_15')

        # Deleting model 'M3_16'
        db.delete_table(u'pce_m3_16')

        # Deleting model 'M3_17'
        db.delete_table(u'pce_m3_17')

        # Deleting model 'Module3'
        db.delete_table(u'pce_module3')

        # Removing M2M table for field m_1 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_1'))

        # Removing M2M table for field m_3 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_3'))

        # Removing M2M table for field m_9 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_9'))

        # Removing M2M table for field m_10 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_10'))

        # Removing M2M table for field m_14 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_14'))

        # Removing M2M table for field m_15 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_15'))

        # Removing M2M table for field m_16 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_16'))

        # Removing M2M table for field m_17 on 'Module3'
        db.delete_table(db.shorten_name(u'pce_module3_m_17'))

        # Deleting model 'Module3Grid'
        db.delete_table(u'pce_module3grid')

        # Deleting model 'Module3Weaknesses'
        db.delete_table(u'pce_module3weaknesses')

        # Deleting model 'Module4'
        db.delete_table(u'pce_module4')

        # Deleting model 'Module4Weaknesses'
        db.delete_table(u'pce_module4weaknesses')

        # Deleting model 'M5_3'
        db.delete_table(u'pce_m5_3')

        # Deleting model 'Module5'
        db.delete_table(u'pce_module5')

        # Removing M2M table for field m_3 on 'Module5'
        db.delete_table(db.shorten_name(u'pce_module5_m_3'))

        # Deleting model 'Module5Weaknesses'
        db.delete_table(u'pce_module5weaknesses')

        # Deleting model 'Module6'
        db.delete_table(u'pce_module6')

        # Deleting model 'Module6Weaknesses'
        db.delete_table(u'pce_module6weaknesses')

        # Deleting model 'Module7'
        db.delete_table(u'pce_module7')

        # Deleting model 'Module7Grid'
        db.delete_table(u'pce_module7grid')

        # Deleting model 'Module7Matrix23'
        db.delete_table(u'pce_module7matrix23')

        # Deleting model 'Module7Matrix37'
        db.delete_table(u'pce_module7matrix37')

        # Deleting model 'Module7Matrix39'
        db.delete_table(u'pce_module7matrix39')

        # Deleting model 'Module7Matrix41'
        db.delete_table(u'pce_module7matrix41')

        # Deleting model 'Module7Matrix43'
        db.delete_table(u'pce_module7matrix43')

        # Deleting model 'Module7Matrix45'
        db.delete_table(u'pce_module7matrix45')

        # Deleting model 'Module7Weaknesses'
        db.delete_table(u'pce_module7weaknesses')

        # Deleting model 'M8_17'
        db.delete_table(u'pce_m8_17')

        # Deleting model 'Module8'
        db.delete_table(u'pce_module8')

        # Removing M2M table for field m_17 on 'Module8'
        db.delete_table(db.shorten_name(u'pce_module8_m_17'))

        # Deleting model 'Module8Grid3'
        db.delete_table(u'pce_module8grid3')

        # Deleting model 'Module8Grid18'
        db.delete_table(u'pce_module8grid18')

        # Deleting model 'Module8Matrix30'
        db.delete_table(u'pce_module8matrix30')

        # Deleting model 'Module8Weaknesses'
        db.delete_table(u'pce_module8weaknesses')

        # Deleting model 'Module9'
        db.delete_table(u'pce_module9')

        # Deleting model 'Module9Grid1'
        db.delete_table(u'pce_module9grid1')

        # Deleting model 'Module9Grid5'
        db.delete_table(u'pce_module9grid5')

        # Deleting model 'Module9Grid31'
        db.delete_table(u'pce_module9grid31')

        # Deleting model 'Module9Matrix35'
        db.delete_table(u'pce_module9matrix35')

        # Deleting model 'Module9Weaknesses'
        db.delete_table(u'pce_module9weaknesses')

        # Deleting model 'Module10'
        db.delete_table(u'pce_module10')

        # Deleting model 'Module10Grid23'
        db.delete_table(u'pce_module10grid23')

        # Deleting model 'Module10Grid31'
        db.delete_table(u'pce_module10grid31')

        # Deleting model 'Module10Grid33'
        db.delete_table(u'pce_module10grid33')

        # Deleting model 'Module10Grid37'
        db.delete_table(u'pce_module10grid37')

        # Deleting model 'Module10Grid45'
        db.delete_table(u'pce_module10grid45')

        # Deleting model 'Module10Grid46'
        db.delete_table(u'pce_module10grid46')

        # Deleting model 'Module10Matrix_47'
        db.delete_table(u'pce_module10matrix_47')

        # Deleting model 'Module10Weaknesses'
        db.delete_table(u'pce_module10weaknesses')

        # Deleting model 'Module11'
        db.delete_table(u'pce_module11')

        # Deleting model 'Module11Grid2'
        db.delete_table(u'pce_module11grid2')

        # Deleting model 'Module11Grid3'
        db.delete_table(u'pce_module11grid3')

        # Deleting model 'Module11Grid12'
        db.delete_table(u'pce_module11grid12')

        # Deleting model 'Module11Grid14'
        db.delete_table(u'pce_module11grid14')

        # Deleting model 'Module11Grid33'
        db.delete_table(u'pce_module11grid33')

        # Deleting model 'Module11Matrix42'
        db.delete_table(u'pce_module11matrix42')

        # Deleting model 'Module11Weaknesses'
        db.delete_table(u'pce_module11weaknesses')

        # Deleting model 'Module12'
        db.delete_table(u'pce_module12')

        # Deleting model 'Module12Grid2'
        db.delete_table(u'pce_module12grid2')

        # Deleting model 'Module12Grid3'
        db.delete_table(u'pce_module12grid3')

        # Deleting model 'Module12Grid_29'
        db.delete_table(u'pce_module12grid_29')

        # Deleting model 'Module12Matrix22'
        db.delete_table(u'pce_module12matrix22')

        # Deleting model 'Module12Weaknesses'
        db.delete_table(u'pce_module12weaknesses')

        # Deleting model 'Module13'
        db.delete_table(u'pce_module13')

        # Deleting model 'Module13Grid2'
        db.delete_table(u'pce_module13grid2')

        # Deleting model 'Module13Grid3'
        db.delete_table(u'pce_module13grid3')

        # Deleting model 'Module13Grid22'
        db.delete_table(u'pce_module13grid22')

        # Deleting model 'Module13Grid29'
        db.delete_table(u'pce_module13grid29')

        # Deleting model 'Module13Grid31'
        db.delete_table(u'pce_module13grid31')

        # Deleting model 'Module13Matrix47'
        db.delete_table(u'pce_module13matrix47')

        # Deleting model 'Module13Weaknesses'
        db.delete_table(u'pce_module13weaknesses')

        # Deleting model 'Stakeholders'
        db.delete_table(u'pce_stakeholders')

        # Deleting model 'StakeholdersFields'
        db.delete_table(u'pce_stakeholdersfields')

        # Deleting model 'ProblemAnalysis'
        db.delete_table(u'pce_problemanalysis')

        # Deleting model 'SwotAnalysis'
        db.delete_table(u'pce_swotanalysis')

        # Deleting model 'SwotAnalysis1'
        db.delete_table(u'pce_swotanalysis1')

        # Deleting model 'SwotAnalysis2'
        db.delete_table(u'pce_swotanalysis2')

        # Deleting model 'SwotAnalysis3'
        db.delete_table(u'pce_swotanalysis3')

        # Deleting model 'SwotAnalysis4'
        db.delete_table(u'pce_swotanalysis4')

        # Deleting model 'SwotAnalysis5'
        db.delete_table(u'pce_swotanalysis5')

        # Deleting model 'LogicalFramework'
        db.delete_table(u'pce_logicalframework')

        # Deleting model 'LogicalFrameworkAct1'
        db.delete_table(u'pce_logicalframeworkact1')

        # Deleting model 'LogicalFrameworkAct2'
        db.delete_table(u'pce_logicalframeworkact2')

        # Deleting model 'LogicalFrameworkAct3'
        db.delete_table(u'pce_logicalframeworkact3')

        # Deleting model 'LogicalFrameworkAct4'
        db.delete_table(u'pce_logicalframeworkact4')

        # Deleting model 'LogicalFrameworkAct5'
        db.delete_table(u'pce_logicalframeworkact5')


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
        u'pce.logicalframework': {
            'Meta': {'object_name': 'LogicalFramework'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'assumptions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assumptions1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assumptions2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assumptions3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assumptions4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assumptions5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keyindicator': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keyindicator1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keyindicator2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keyindicator3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keyindicator4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keyindicator5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'objective': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'output1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'output2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'output3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'output4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'output5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'verification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'verification1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'verification2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'verification3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'verification4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'verification5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.logicalframeworkact1': {
            'Meta': {'object_name': 'LogicalFrameworkAct1'},
            'activity1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logicalframework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.LogicalFramework']"}),
            'responsible': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sourcverification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.logicalframeworkact2': {
            'Meta': {'object_name': 'LogicalFrameworkAct2'},
            'activity2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logicalframework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.LogicalFramework']"}),
            'responsible': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sourcverification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.logicalframeworkact3': {
            'Meta': {'object_name': 'LogicalFrameworkAct3'},
            'activity3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logicalframework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.LogicalFramework']"}),
            'responsible': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sourcverification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.logicalframeworkact4': {
            'Meta': {'object_name': 'LogicalFrameworkAct4'},
            'activity4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logicalframework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.LogicalFramework']"}),
            'responsible': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sourcverification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.logicalframeworkact5': {
            'Meta': {'object_name': 'LogicalFrameworkAct5'},
            'activity5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logicalframework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.LogicalFramework']"}),
            'responsible': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sourcverification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pce.m3_1': {
            'Meta': {'object_name': 'M3_1'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_10': {
            'Meta': {'object_name': 'M3_10'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_14': {
            'Meta': {'object_name': 'M3_14'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_15': {
            'Meta': {'object_name': 'M3_15'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_16': {
            'Meta': {'object_name': 'M3_16'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_17': {
            'Meta': {'object_name': 'M3_17'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_3': {
            'Meta': {'object_name': 'M3_3'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m3_9': {
            'Meta': {'object_name': 'M3_9'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m5_3': {
            'Meta': {'object_name': 'M5_3'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.m8_17': {
            'Meta': {'object_name': 'M8_17'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
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
        u'pce.module10': {
            'Meta': {'object_name': 'Module10'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_25': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_30': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_34': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_35': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_36': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_38': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_39': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_40': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_41': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_42': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_43': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_44': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_48': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_49': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_50': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_51': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_52': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_53': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_54': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_55': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_56': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_57': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_58': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_59': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_60': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_9': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module10grid23': {
            'Meta': {'object_name': 'Module10Grid23'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"})
        },
        u'pce.module10grid31': {
            'Meta': {'object_name': 'Module10Grid31'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"})
        },
        u'pce.module10grid33': {
            'Meta': {'object_name': 'Module10Grid33'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"})
        },
        u'pce.module10grid37': {
            'Meta': {'object_name': 'Module10Grid37'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"})
        },
        u'pce.module10grid45': {
            'Meta': {'object_name': 'Module10Grid45'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"})
        },
        u'pce.module10grid46': {
            'Meta': {'object_name': 'Module10Grid46'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"})
        },
        u'pce.module10matrix_47': {
            'Meta': {'object_name': 'Module10Matrix_47'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'averagelab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'supstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'technical': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module10weaknesses': {
            'Meta': {'object_name': 'Module10Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module10': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module10']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module11': {
            'Meta': {'object_name': 'Module11'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_25': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_30': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_31': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_34': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_35': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_36': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_37': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_38': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_39': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_40': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_41': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_43': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_44': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_45': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_46': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_47': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_48': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_49': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_50': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_51': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_52': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_53': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_54': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_55': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_56': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_57': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_58': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_59': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_60': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_61': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_62': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_63': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_65': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_66': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_67': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module11grid12': {
            'Meta': {'object_name': 'Module11Grid12'},
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c5': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"})
        },
        u'pce.module11grid14': {
            'Meta': {'object_name': 'Module11Grid14'},
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c5': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c6': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"})
        },
        u'pce.module11grid2': {
            'Meta': {'object_name': 'Module11Grid2'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"})
        },
        u'pce.module11grid3': {
            'Meta': {'object_name': 'Module11Grid3'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"})
        },
        u'pce.module11grid33': {
            'Meta': {'object_name': 'Module11Grid33'},
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"})
        },
        u'pce.module11matrix42': {
            'Meta': {'object_name': 'Module11Matrix42'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module11weaknesses': {
            'Meta': {'object_name': 'Module11Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module11': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module11']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module12': {
            'Meta': {'object_name': 'Module12'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_26': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_27': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_30': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_31': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_32': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_33': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module12grid2': {
            'Meta': {'object_name': 'Module12Grid2'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module12': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module12']"})
        },
        u'pce.module12grid3': {
            'Meta': {'object_name': 'Module12Grid3'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module12': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module12']"})
        },
        u'pce.module12grid_29': {
            'Meta': {'object_name': 'Module12Grid_29'},
            'Module12': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module12']"}),
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pce.module12matrix22': {
            'Meta': {'object_name': 'Module12Matrix22'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'averagelab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'module12': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module12']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module12weaknesses': {
            'Meta': {'object_name': 'Module12Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module12': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module12']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module13': {
            'Meta': {'object_name': 'Module13'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_23': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_30': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_33': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_34': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_35': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_36': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_37': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_38': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_39': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_40': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_41': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_42': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_43': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_44': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_45': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_46': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_48': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_49': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_50': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_51': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_52': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_53': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_54': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_55': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_56': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_57': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_58': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_59': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_60': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_61': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_62': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_63': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_64': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_65': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module13grid2': {
            'Meta': {'object_name': 'Module13Grid2'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"})
        },
        u'pce.module13grid22': {
            'Meta': {'object_name': 'Module13Grid22'},
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"})
        },
        u'pce.module13grid29': {
            'Meta': {'object_name': 'Module13Grid29'},
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c10': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c11': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c12': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c5': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c6': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c7': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c8': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c9': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"})
        },
        u'pce.module13grid3': {
            'Meta': {'object_name': 'Module13Grid3'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"})
        },
        u'pce.module13grid31': {
            'Meta': {'object_name': 'Module13Grid31'},
            'c1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'c5': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"})
        },
        u'pce.module13matrix47': {
            'Meta': {'object_name': 'Module13Matrix47'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'averagelab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module13weaknesses': {
            'Meta': {'object_name': 'Module13Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module13': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module13']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
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
        u'pce.module2': {
            'Meta': {'object_name': 'Module2'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_10': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_100': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_101': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_102': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_103': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_104': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_105': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_106': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_107': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_108': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_109': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_110': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_111': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_112': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_113': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_114': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_115': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_116': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_117': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_118': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_119': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_120': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_121': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_122': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_14': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_15': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_24': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_25': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_30': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_31': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_33': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_34': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_35': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_36': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_37': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_38': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_39': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_40': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_41': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_42': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_43': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_44': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_45': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_46': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_47': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_48': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_49': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_50': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_51': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_52': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_53': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_54': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_55': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_56': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_57': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_58': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_59': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_60': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_61': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_62': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_63': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_64': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_65': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_66': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_67': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_68': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_69': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_70': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_71': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_72': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_73': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_74': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_75': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_76': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_77': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_78': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_79': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_80': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_81': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_82': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_83': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_84': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_85': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_86': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_87': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_88': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_89': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_9': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_90': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_91': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_92': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_93': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_94': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_95': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_96': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_97': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_98': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_99': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module2weaknesses': {
            'Meta': {'object_name': 'Module2Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module2': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module2']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module3': {
            'Meta': {'object_name': 'Module3'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_1']", 'null': 'True', 'blank': 'True'}),
            'm_10': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_10']", 'null': 'True', 'blank': 'True'}),
            'm_11': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_12': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_13': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_14': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_14']", 'null': 'True', 'blank': 'True'}),
            'm_15': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_15']", 'null': 'True', 'blank': 'True'}),
            'm_16': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_16']", 'null': 'True', 'blank': 'True'}),
            'm_17': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_17']", 'null': 'True', 'blank': 'True'}),
            'm_18': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_19': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_20': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_22': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_23': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_3']", 'null': 'True', 'blank': 'True'}),
            'm_30': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_32': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_8': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_9': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M3_9']", 'null': 'True', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module3grid': {
            'Meta': {'object_name': 'Module3Grid'},
            'high': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'medium': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module3': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module3']"}),
            'veryhigh': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verylow': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pce.module3weaknesses': {
            'Meta': {'object_name': 'Module3Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module3': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module3']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module4': {
            'Meta': {'object_name': 'Module4'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_10': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_11': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_12': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_13': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_25': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_28': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_30': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_31': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_33': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_5': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_6': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module4weaknesses': {
            'Meta': {'object_name': 'Module4Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module4': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module4']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module5': {
            'Meta': {'object_name': 'Module5'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_17': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_18': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_19': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_2': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_20': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_21': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M5_3']", 'null': 'True', 'blank': 'True'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module5weaknesses': {
            'Meta': {'object_name': 'Module5Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module5': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module5']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module6': {
            'Meta': {'object_name': 'Module6'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_17': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_22': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_23': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_28': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_29': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_30': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_31': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_32': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_33': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_34': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_35': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_36': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_4': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_9': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module6weaknesses': {
            'Meta': {'object_name': 'Module6Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module6': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module6']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module7': {
            'Meta': {'object_name': 'Module7'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_12': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_22': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_26': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_27': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_30': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_31': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_33': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_34': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_35': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_36': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_38': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_40': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_42': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_44': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_46': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_47': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_48': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_49': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_50': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_51': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_52': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_53': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_54': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_55': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_56': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_57': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_58': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_59': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_60': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_61': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_62': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_63': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_64': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_65': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_66': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_67': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_68': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module7grid': {
            'Meta': {'object_name': 'Module7Grid'},
            'equipment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'fixedcosts': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'operationalcosts': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'salaries': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'supplies': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module7matrix23': {
            'Meta': {'object_name': 'Module7Matrix23'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'averagelab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module7matrix37': {
            'Meta': {'object_name': 'Module7Matrix37'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'navailable': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'qaulity': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'required': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module7matrix39': {
            'Meta': {'object_name': 'Module7Matrix39'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'navailable': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'qaulity': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'required': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module7matrix41': {
            'Meta': {'object_name': 'Module7Matrix41'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'navailable': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'qaulity': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'required': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module7matrix43': {
            'Meta': {'object_name': 'Module7Matrix43'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'navailable': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'qaulity': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'required': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module7matrix45': {
            'Meta': {'object_name': 'Module7Matrix45'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'navailable': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'qaulity': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'required': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module7weaknesses': {
            'Meta': {'object_name': 'Module7Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module7': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module7']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module8': {
            'Meta': {'object_name': 'Module8'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pce.M8_17']", 'null': 'True', 'blank': 'True'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_25': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_26': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_27': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_31': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_32': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_33': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_34': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_35': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_36': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_37': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_38': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_39': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_40': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_41': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_42': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_43': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_44': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_9': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module8grid18': {
            'Meta': {'object_name': 'Module8Grid18'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module8': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module8']"})
        },
        u'pce.module8grid3': {
            'Meta': {'object_name': 'Module8Grid3'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module8': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module8']"})
        },
        u'pce.module8matrix30': {
            'Meta': {'object_name': 'Module8Matrix30'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'averagelab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'module8': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module8']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module8weaknesses': {
            'Meta': {'object_name': 'Module8Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module8': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module8']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.module9': {
            'Meta': {'object_name': 'Module9'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'm_10': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_11': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_12': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_13': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_14': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_15': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_16': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_17': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_19': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_20': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_21': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_22': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_23': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_24': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_25': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_26': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_27': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_29': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_30': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_32': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_33': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_34': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_36': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_37': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_38': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_39': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_40': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_41': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_42': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_43': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_44': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_45': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_46': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'm_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'm_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'pce.module9grid1': {
            'Meta': {'object_name': 'Module9Grid1'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module9': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module9']"})
        },
        u'pce.module9grid31': {
            'Meta': {'object_name': 'Module9Grid31'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module9': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module9']"})
        },
        u'pce.module9grid5': {
            'Meta': {'object_name': 'Module9Grid5'},
            'c1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module9': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module9']"})
        },
        u'pce.module9matrix35': {
            'Meta': {'object_name': 'Module9Matrix35'},
            'average': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'averagelab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'module9': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module9']"}),
            'nstaff': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'nstafflab': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'support': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.module9weaknesses': {
            'Meta': {'object_name': 'Module9Weaknesses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module9': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Module9']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w4': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'w5': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'pce.pceversion': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'PceVersion'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pceversion_author'", 'to': u"orm['auth.User']"}),
            'chosen_modules': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'completed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pceversion_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed1_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed1_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed1_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed2_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed2_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed2_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed3_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed3_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed3_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed4_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed4_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed4_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed5_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed5_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed5_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed6_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed6_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed6_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed7_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed7_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed7_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed8_email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed8_firstname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ed8_lastname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
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
        u'pce.problemanalysis': {
            'Meta': {'object_name': 'ProblemAnalysis'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'cause_a_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_a_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_a_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_a_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_a_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_b_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_b_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_b_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_b_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cause_b_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_a_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_a_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_a_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_a_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_a_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_b_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_b_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_b_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_b_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consequence_b_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'w_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'w_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'w_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'w_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'w_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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
            'stakeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.Stakeholders']"})
        },
        u'pce.swotanalysis': {
            'Meta': {'object_name': 'SwotAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.PceVersion']"})
        },
        u'pce.swotanalysis1': {
            'Meta': {'object_name': 'SwotAnalysis1'},
            'actions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opportunities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'strengths': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'swotanalysis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.SwotAnalysis']"}),
            'threats': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.swotanalysis2': {
            'Meta': {'object_name': 'SwotAnalysis2'},
            'actions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opportunities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'strengths': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'swotanalysis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.SwotAnalysis']"}),
            'threats': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.swotanalysis3': {
            'Meta': {'object_name': 'SwotAnalysis3'},
            'actions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opportunities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'strengths': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'swotanalysis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.SwotAnalysis']"}),
            'threats': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.swotanalysis4': {
            'Meta': {'object_name': 'SwotAnalysis4'},
            'actions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opportunities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'strengths': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'swotanalysis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.SwotAnalysis']"}),
            'threats': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'pce.swotanalysis5': {
            'Meta': {'object_name': 'SwotAnalysis5'},
            'actions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opportunities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'strengths': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'swotanalysis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pce.SwotAnalysis']"}),
            'threats': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pce']