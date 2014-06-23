# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicationLibrary'
        db.create_table(u'ippc_publicationlibrary', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
        ))
        db.send_create_signal(u'ippc', ['PublicationLibrary'])

        # Adding M2M table for field users on 'PublicationLibrary'
        m2m_table_name = db.shorten_name(u'ippc_publicationlibrary_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publicationlibrary', models.ForeignKey(orm[u'ippc.publicationlibrary'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['publicationlibrary_id', 'user_id'])

        # Adding M2M table for field groups on 'PublicationLibrary'
        m2m_table_name = db.shorten_name(u'ippc_publicationlibrary_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publicationlibrary', models.ForeignKey(orm[u'ippc.publicationlibrary'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['publicationlibrary_id', 'group_id'])

        # Adding model 'Publication'
        db.create_table(u'ippc_publication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('library', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publications', to=orm['ippc.PublicationLibrary'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('file_en', self.gf('django.db.models.fields.files.FileField')(max_length=204, null=True, blank=True)),
            ('file_es', self.gf('django.db.models.fields.files.FileField')(max_length=204, null=True, blank=True)),
            ('file_fr', self.gf('django.db.models.fields.files.FileField')(max_length=204, null=True, blank=True)),
            ('file_ru', self.gf('django.db.models.fields.files.FileField')(max_length=204, null=True, blank=True)),
            ('file_ar', self.gf('django.db.models.fields.files.FileField')(max_length=204, null=True, blank=True)),
            ('file_zh', self.gf('django.db.models.fields.files.FileField')(max_length=204, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('agenda_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('document_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['Publication'])

        # Adding model 'WorkAreaPage'
        db.create_table(u'ippc_workareapage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
        ))
        db.send_create_signal(u'ippc', ['WorkAreaPage'])

        # Adding M2M table for field users on 'WorkAreaPage'
        m2m_table_name = db.shorten_name(u'ippc_workareapage_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workareapage', models.ForeignKey(orm[u'ippc.workareapage'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workareapage_id', 'user_id'])

        # Adding M2M table for field groups on 'WorkAreaPage'
        m2m_table_name = db.shorten_name(u'ippc_workareapage_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workareapage', models.ForeignKey(orm[u'ippc.workareapage'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workareapage_id', 'group_id'])

        # Adding model 'CountryPage'
        db.create_table(u'ippc_countrypage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2, unique=True, null=True, blank=True)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3, unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('country_slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True)),
            ('contact_point', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['CountryPage'])

        # Adding M2M table for field editors on 'CountryPage'
        m2m_table_name = db.shorten_name(u'ippc_countrypage_editors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('countrypage', models.ForeignKey(orm[u'ippc.countrypage'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['countrypage_id', 'user_id'])

        # Adding model 'PestStatus'
        db.create_table(u'ippc_peststatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'ippc', ['PestStatus'])

        # Adding model 'IppcUserProfile'
        db.create_table(u'ippc_ippcuserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email_address_alt', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('profile_photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('address_country', self.gf('django_countries.fields.CountryField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_country_page', null=True, to=orm['ippc.CountryPage'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('date_account_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'ippc', ['IppcUserProfile'])

        # Adding model 'PestReport'
        db.create_table(u'ippc_pestreport', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pest_report_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pest_report_author', to=orm['auth.User'])),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('report_status', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('pest_identity', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hosts', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geographical_distribution', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('nature_of_danger', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['PestReport'])

        # Adding M2M table for field pest_status on 'PestReport'
        m2m_table_name = db.shorten_name(u'ippc_pestreport_pest_status')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pestreport', models.ForeignKey(orm[u'ippc.pestreport'], null=False)),
            ('peststatus', models.ForeignKey(orm[u'ippc.peststatus'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pestreport_id', 'peststatus_id'])

        # Adding model 'ReportingObligation'
        db.create_table(u'ippc_reportingobligation', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reporting_obligation_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reporting_obligation_author', to=orm['auth.User'])),
            ('report_obligation_type', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['ReportingObligation'])

        # Adding model 'EventReporting'
        db.create_table(u'ippc_eventreporting', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_reporting_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event__reporting_author', to=orm['auth.User'])),
            ('event_rep_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['EventReporting'])

        # Adding model 'PestFreeArea'
        db.create_table(u'ippc_pestfreearea', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pestfreearea_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pestfreearea_author', to=orm['auth.User'])),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('pfa_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['PestFreeArea'])

        # Adding model 'ImplementationISPMVersion'
        db.create_table(u'ippc_implementationispmversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'ippc', ['ImplementationISPMVersion'])

        # Adding model 'ImplementationISPM'
        db.create_table(u'ippc_implementationispm', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='implementationispm_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='implementationispm_author', to=orm['auth.User'])),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('implementimport_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('implementexport_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('mark_registered_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['ImplementationISPM'])

        # Adding M2M table for field implementimport_version on 'ImplementationISPM'
        m2m_table_name = db.shorten_name(u'ippc_implementationispm_implementimport_version')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('implementationispm', models.ForeignKey(orm[u'ippc.implementationispm'], null=False)),
            ('implementationispmversion', models.ForeignKey(orm[u'ippc.implementationispmversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['implementationispm_id', 'implementationispmversion_id'])

        # Adding M2M table for field implementexport_version on 'ImplementationISPM'
        m2m_table_name = db.shorten_name(u'ippc_implementationispm_implementexport_version')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('implementationispm', models.ForeignKey(orm[u'ippc.implementationispm'], null=False)),
            ('implementationispmversion', models.ForeignKey(orm[u'ippc.implementationispmversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['implementationispm_id', 'implementationispmversion_id'])

        # Adding model 'TransRichTextPage'
        db.create_table(u'ippc_transrichtextpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['pages.RichTextPage'])),
        ))
        db.send_create_signal(u'ippc', ['TransRichTextPage'])

        # Adding unique constraint on 'TransRichTextPage', fields ['lang', 'translation']
        db.create_unique(u'ippc_transrichtextpage', ['lang', 'translation_id'])

        # Adding model 'TransLinkPage'
        db.create_table(u'ippc_translinkpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['pages.Link'])),
        ))
        db.send_create_signal(u'ippc', ['TransLinkPage'])

        # Adding unique constraint on 'TransLinkPage', fields ['lang', 'translation']
        db.create_unique(u'ippc_translinkpage', ['lang', 'translation_id'])

        # Adding model 'TransForm'
        db.create_table(u'ippc_transform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['forms.Form'])),
            ('button_text', self.gf('django.db.models.fields.CharField')(default=u'Submit', max_length=50)),
            ('response', self.gf('mezzanine.core.fields.RichTextField')()),
        ))
        db.send_create_signal(u'ippc', ['TransForm'])

        # Adding unique constraint on 'TransForm', fields ['lang', 'translation']
        db.create_unique(u'ippc_transform', ['lang', 'translation_id'])

        # Adding model 'TransField'
        db.create_table(u'ippc_transfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['forms.Field'])),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('choices', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['TransField'])

        # Adding model 'TransGallery'
        db.create_table(u'ippc_transgallery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['galleries.Gallery'])),
        ))
        db.send_create_signal(u'ippc', ['TransGallery'])

        # Adding model 'TransGalleryImage'
        db.create_table(u'ippc_transgalleryimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['galleries.GalleryImage'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['TransGalleryImage'])

        # Adding model 'TransPublicationLibraryPage'
        db.create_table(u'ippc_transpublicationlibrarypage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translation', to=orm['ippc.PublicationLibrary'])),
        ))
        db.send_create_signal(u'ippc', ['TransPublicationLibraryPage'])

        # Adding unique constraint on 'TransPublicationLibraryPage', fields ['lang', 'translation']
        db.create_unique(u'ippc_transpublicationlibrarypage', ['lang', 'translation_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TransPublicationLibraryPage', fields ['lang', 'translation']
        db.delete_unique(u'ippc_transpublicationlibrarypage', ['lang', 'translation_id'])

        # Removing unique constraint on 'TransForm', fields ['lang', 'translation']
        db.delete_unique(u'ippc_transform', ['lang', 'translation_id'])

        # Removing unique constraint on 'TransLinkPage', fields ['lang', 'translation']
        db.delete_unique(u'ippc_translinkpage', ['lang', 'translation_id'])

        # Removing unique constraint on 'TransRichTextPage', fields ['lang', 'translation']
        db.delete_unique(u'ippc_transrichtextpage', ['lang', 'translation_id'])

        # Deleting model 'PublicationLibrary'
        db.delete_table(u'ippc_publicationlibrary')

        # Removing M2M table for field users on 'PublicationLibrary'
        db.delete_table(db.shorten_name(u'ippc_publicationlibrary_users'))

        # Removing M2M table for field groups on 'PublicationLibrary'
        db.delete_table(db.shorten_name(u'ippc_publicationlibrary_groups'))

        # Deleting model 'Publication'
        db.delete_table(u'ippc_publication')

        # Deleting model 'WorkAreaPage'
        db.delete_table(u'ippc_workareapage')

        # Removing M2M table for field users on 'WorkAreaPage'
        db.delete_table(db.shorten_name(u'ippc_workareapage_users'))

        # Removing M2M table for field groups on 'WorkAreaPage'
        db.delete_table(db.shorten_name(u'ippc_workareapage_groups'))

        # Deleting model 'CountryPage'
        db.delete_table(u'ippc_countrypage')

        # Removing M2M table for field editors on 'CountryPage'
        db.delete_table(db.shorten_name(u'ippc_countrypage_editors'))

        # Deleting model 'PestStatus'
        db.delete_table(u'ippc_peststatus')

        # Deleting model 'IppcUserProfile'
        db.delete_table(u'ippc_ippcuserprofile')

        # Deleting model 'PestReport'
        db.delete_table(u'ippc_pestreport')

        # Removing M2M table for field pest_status on 'PestReport'
        db.delete_table(db.shorten_name(u'ippc_pestreport_pest_status'))

        # Deleting model 'ReportingObligation'
        db.delete_table(u'ippc_reportingobligation')

        # Deleting model 'EventReporting'
        db.delete_table(u'ippc_eventreporting')

        # Deleting model 'PestFreeArea'
        db.delete_table(u'ippc_pestfreearea')

        # Deleting model 'ImplementationISPMVersion'
        db.delete_table(u'ippc_implementationispmversion')

        # Deleting model 'ImplementationISPM'
        db.delete_table(u'ippc_implementationispm')

        # Removing M2M table for field implementimport_version on 'ImplementationISPM'
        db.delete_table(db.shorten_name(u'ippc_implementationispm_implementimport_version'))

        # Removing M2M table for field implementexport_version on 'ImplementationISPM'
        db.delete_table(db.shorten_name(u'ippc_implementationispm_implementexport_version'))

        # Deleting model 'TransRichTextPage'
        db.delete_table(u'ippc_transrichtextpage')

        # Deleting model 'TransLinkPage'
        db.delete_table(u'ippc_translinkpage')

        # Deleting model 'TransForm'
        db.delete_table(u'ippc_transform')

        # Deleting model 'TransField'
        db.delete_table(u'ippc_transfield')

        # Deleting model 'TransGallery'
        db.delete_table(u'ippc_transgallery')

        # Deleting model 'TransGalleryImage'
        db.delete_table(u'ippc_transgalleryimage')

        # Deleting model 'TransPublicationLibraryPage'
        db.delete_table(u'ippc_transpublicationlibrarypage')


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
        u'forms.field': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Field'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['forms.Form']"}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'placeholder_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'forms.form': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Form', '_ormbases': [u'pages.Page']},
            'button_text': ('django.db.models.fields.CharField', [], {'default': "u'Submit'", 'max_length': '50'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'email_copies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email_from': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('mezzanine.core.fields.RichTextField', [], {}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'galleries.gallery': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Gallery', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'zip_import': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'galleries.galleryimage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'GalleryImage'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '200'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['galleries.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'contact_point': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'country_slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'countryeditors+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'ippc.eventreporting': {
            'Meta': {'object_name': 'EventReporting'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event__reporting_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_reporting_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_rep_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.implementationispm': {
            'Meta': {'object_name': 'ImplementationISPM'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'implementationispm_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'implementationispm_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'implementexport_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'implementexport_version': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'implementexport_version+'", 'default': 'None', 'to': u"orm['ippc.ImplementationISPMVersion']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'implementimport_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'implementimport_version': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'implementimport_version+'", 'default': 'None', 'to': u"orm['ippc.ImplementationISPMVersion']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'mark_registered_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.implementationispmversion': {
            'Meta': {'object_name': 'ImplementationISPMVersion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'ippc.ippcuserprofile': {
            'Meta': {'object_name': 'IppcUserProfile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_country_page'", 'null': 'True', 'to': u"orm['ippc.CountryPage']"}),
            'date_account_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email_address_alt': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'profile_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'ippc.pestfreearea': {
            'Meta': {'object_name': 'PestFreeArea'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pestfreearea_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pestfreearea_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pfa_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.pestreport': {
            'Meta': {'object_name': 'PestReport'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pest_report_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pest_report_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'geographical_distribution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hosts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nature_of_danger': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pest_identity': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pest_status': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pest_status+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ippc.PestStatus']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'report_status': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.peststatus': {
            'Meta': {'object_name': 'PestStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.publication': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Publication'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'agenda_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'document_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'file_ar': ('django.db.models.fields.files.FileField', [], {'max_length': '204', 'null': 'True', 'blank': 'True'}),
            'file_en': ('django.db.models.fields.files.FileField', [], {'max_length': '204', 'null': 'True', 'blank': 'True'}),
            'file_es': ('django.db.models.fields.files.FileField', [], {'max_length': '204', 'null': 'True', 'blank': 'True'}),
            'file_fr': ('django.db.models.fields.files.FileField', [], {'max_length': '204', 'null': 'True', 'blank': 'True'}),
            'file_ru': ('django.db.models.fields.files.FileField', [], {'max_length': '204', 'null': 'True', 'blank': 'True'}),
            'file_zh': ('django.db.models.fields.files.FileField', [], {'max_length': '204', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publications'", 'to': u"orm['ippc.PublicationLibrary']"}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.publicationlibrary': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'PublicationLibrary', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publicationlibrarygroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publicationlibraryusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'ippc.reportingobligation': {
            'Meta': {'object_name': 'ReportingObligation'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reporting_obligation_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reporting_obligation_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'report_obligation_type': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.transfield': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransField'},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['forms.Field']"})
        },
        u'ippc.transform': {
            'Meta': {'ordering': "('lang',)", 'unique_together': "(('lang', 'translation'),)", 'object_name': 'TransForm'},
            'button_text': ('django.db.models.fields.CharField', [], {'default': "u'Submit'", 'max_length': '50'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'response': ('mezzanine.core.fields.RichTextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['forms.Form']"})
        },
        u'ippc.transgallery': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransGallery'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['galleries.Gallery']"})
        },
        u'ippc.transgalleryimage': {
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransGalleryImage'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['galleries.GalleryImage']"})
        },
        u'ippc.translinkpage': {
            'Meta': {'ordering': "('lang',)", 'unique_together': "(('lang', 'translation'),)", 'object_name': 'TransLinkPage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['pages.Link']"})
        },
        u'ippc.transpublicationlibrarypage': {
            'Meta': {'ordering': "('lang',)", 'unique_together': "(('lang', 'translation'),)", 'object_name': 'TransPublicationLibraryPage'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['ippc.PublicationLibrary']"})
        },
        u'ippc.transrichtextpage': {
            'Meta': {'ordering': "('lang',)", 'unique_together': "(('lang', 'translation'),)", 'object_name': 'TransRichTextPage'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translation'", 'to': u"orm['pages.RichTextPage']"})
        },
        u'ippc.workareapage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'WorkAreaPage', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'workareapagegroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'workareapageusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'pages.link': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Link', '_ormbases': [u'pages.Page']},
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
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
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        u'pages.richtextpage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'RichTextPage', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['ippc']