# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicationLibrary'
        db.create_table(u'ippc_publicationlibrary', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
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

        # Adding model 'IssueKeyword'
        db.create_table(u'ippc_issuekeyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'ippc', ['IssueKeyword'])

        # Adding model 'CommodityKeyword'
        db.create_table(u'ippc_commoditykeyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'ippc', ['CommodityKeyword'])

        # Adding model 'IssueKeywordsRelate'
        db.create_table(u'ippc_issuekeywordsrelate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ippc', ['IssueKeywordsRelate'])

        # Adding M2M table for field issuename on 'IssueKeywordsRelate'
        m2m_table_name = db.shorten_name(u'ippc_issuekeywordsrelate_issuename')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issuekeywordsrelate', models.ForeignKey(orm[u'ippc.issuekeywordsrelate'], null=False)),
            ('issuekeyword', models.ForeignKey(orm[u'ippc.issuekeyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['issuekeywordsrelate_id', 'issuekeyword_id'])

        # Adding model 'CommodityKeywordsRelate'
        db.create_table(u'ippc_commoditykeywordsrelate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ippc', ['CommodityKeywordsRelate'])

        # Adding M2M table for field commname on 'CommodityKeywordsRelate'
        m2m_table_name = db.shorten_name(u'ippc_commoditykeywordsrelate_commname')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('commoditykeywordsrelate', models.ForeignKey(orm[u'ippc.commoditykeywordsrelate'], null=False)),
            ('commoditykeyword', models.ForeignKey(orm[u'ippc.commoditykeyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['commoditykeywordsrelate_id', 'commoditykeyword_id'])

        # Adding model 'CountryPage'
        db.create_table(u'ippc_countrypage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2, unique=True, null=True, blank=True)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3, unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('country_slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True)),
            ('contact_point', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('cp_ncp_t_type', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=3)),
            ('region', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('cn_flag', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('cn_lat', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True)),
            ('cn_long', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True)),
            ('cn_map', self.gf('django.db.models.fields.CharField')(max_length=550)),
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

        # Adding model 'PartnersPage'
        db.create_table(u'ippc_partnerspage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=550)),
            ('partner_slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True)),
            ('contact_point', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersPage'])

        # Adding M2M table for field editors on 'PartnersPage'
        m2m_table_name = db.shorten_name(u'ippc_partnerspage_editors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partnerspage', models.ForeignKey(orm[u'ippc.partnerspage'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partnerspage_id', 'user_id'])

        # Adding model 'NotificationMessageRelate'
        db.create_table(u'ippc_notificationmessagerelate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('notifysecretariat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ippc', ['NotificationMessageRelate'])

        # Adding M2M table for field countries on 'NotificationMessageRelate'
        m2m_table_name = db.shorten_name(u'ippc_notificationmessagerelate_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notificationmessagerelate', models.ForeignKey(orm[u'ippc.notificationmessagerelate'], null=False)),
            ('countrypage', models.ForeignKey(orm[u'ippc.countrypage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notificationmessagerelate_id', 'countrypage_id'])

        # Adding M2M table for field partners on 'NotificationMessageRelate'
        m2m_table_name = db.shorten_name(u'ippc_notificationmessagerelate_partners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notificationmessagerelate', models.ForeignKey(orm[u'ippc.notificationmessagerelate'], null=False)),
            ('partnerspage', models.ForeignKey(orm[u'ippc.partnerspage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notificationmessagerelate_id', 'partnerspage_id'])

        # Adding model 'Publication'
        db.create_table(u'ippc_publication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('library', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publications', to=orm['ippc.PublicationLibrary'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
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
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['Publication'])

        # Adding model 'PublicationFile'
        db.create_table(u'ippc_publicationfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.Publication'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PublicationFile'])

        # Adding model 'PublicationUrl'
        db.create_table(u'ippc_publicationurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.Publication'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PublicationUrl'])

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

        # Adding model 'PestStatus'
        db.create_table(u'ippc_peststatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'ippc', ['PestStatus'])

        # Adding model 'PreferredLanguages'
        db.create_table(u'ippc_preferredlanguages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'ippc', ['PreferredLanguages'])

        # Adding model 'EppoCode'
        db.create_table(u'ippc_eppocode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('codedescr', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('codeparent', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('preferred', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('authority', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('creationdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'ippc', ['EppoCode'])

        # Adding model 'ContactType'
        db.create_table(u'ippc_contacttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contacttype', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'ippc', ['ContactType'])

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
            ('expertize', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('address2', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('address_country', self.gf('django_countries.fields.CountryField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_country_page', null=True, to=orm['ippc.CountryPage'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_partner_page', null=True, to=orm['ippc.PartnersPage'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('date_account_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'ippc', ['IppcUserProfile'])

        # Adding M2M table for field contact_type on 'IppcUserProfile'
        m2m_table_name = db.shorten_name(u'ippc_ippcuserprofile_contact_type')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ippcuserprofile', models.ForeignKey(orm[u'ippc.ippcuserprofile'], null=False)),
            ('contacttype', models.ForeignKey(orm[u'ippc.contacttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ippcuserprofile_id', 'contacttype_id'])

        # Adding M2M table for field preferredlanguage on 'IppcUserProfile'
        m2m_table_name = db.shorten_name(u'ippc_ippcuserprofile_preferredlanguage')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ippcuserprofile', models.ForeignKey(orm[u'ippc.ippcuserprofile'], null=False)),
            ('preferredlanguages', models.ForeignKey(orm[u'ippc.preferredlanguages'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ippcuserprofile_id', 'preferredlanguages_id'])

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
            ('report_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pest_identity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.EppoCode'], null=True, blank=True)),
            ('hosts', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geographical_distribution', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('nature_of_danger', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
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

        # Adding model 'PestReportFile'
        db.create_table(u'ippc_pestreportfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pestreport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PestReport'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PestReportFile'])

        # Adding model 'PestReportUrl'
        db.create_table(u'ippc_pestreporturl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pestreport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PestReport'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PestReportUrl'])

        # Adding model 'DraftProtocol'
        db.create_table(u'ippc_draftprotocol', (
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
            ('closing_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('filetext', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('filefig', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['DraftProtocol'])

        # Adding M2M table for field users on 'DraftProtocol'
        m2m_table_name = db.shorten_name(u'ippc_draftprotocol_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('draftprotocol', models.ForeignKey(orm[u'ippc.draftprotocol'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['draftprotocol_id', 'user_id'])

        # Adding M2M table for field groups on 'DraftProtocol'
        m2m_table_name = db.shorten_name(u'ippc_draftprotocol_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('draftprotocol', models.ForeignKey(orm[u'ippc.draftprotocol'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['draftprotocol_id', 'group_id'])

        # Adding model 'DraftProtocolFile'
        db.create_table(u'ippc_draftprotocolfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('draftprotocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.DraftProtocol'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['DraftProtocolFile'])

        # Adding model 'DraftProtocolComments'
        db.create_table(u'ippc_draftprotocolcomments', (
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
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='draftprotocolcomments_author', to=orm['auth.User'])),
            ('draftprotocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.DraftProtocol'])),
            ('expertise', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('institution', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('filetext', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('filefig', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['DraftProtocolComments'])

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
            ('reporting_obligation_type', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['ReportingObligation'])

        # Adding model 'ReportingObligation_File'
        db.create_table(u'ippc_reportingobligation_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reportingobligation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.ReportingObligation'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['ReportingObligation_File'])

        # Adding model 'ReportingObligationUrl'
        db.create_table(u'ippc_reportingobligationurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reportingobligation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.ReportingObligation'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['ReportingObligationUrl'])

        # Adding model 'CnPublication'
        db.create_table(u'ippc_cnpublication', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cnpublication_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cnpublicatio_author', to=orm['auth.User'])),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('agenda_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('document_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['CnPublication'])

        # Adding model 'CnPublicationFile'
        db.create_table(u'ippc_cnpublicationfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cnpublication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.CnPublication'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['CnPublicationFile'])

        # Adding model 'CnPublicationUrl'
        db.create_table(u'ippc_cnpublicationurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cnpublication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.CnPublication'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['CnPublicationUrl'])

        # Adding model 'PartnersPublication'
        db.create_table(u'ippc_partnerspublication', (
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
            ('partners', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partnerspublication_country_page', to=orm['ippc.PartnersPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partnerspublication_author', to=orm['auth.User'])),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('agenda_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('document_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersPublication'])

        # Adding model 'PartnersPublicationFile'
        db.create_table(u'ippc_partnerspublicationfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partnerspublication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PartnersPublication'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersPublicationFile'])

        # Adding model 'PartnersPublicationUrl'
        db.create_table(u'ippc_partnerspublicationurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partnerspublication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PartnersPublication'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersPublicationUrl'])

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
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['EventReporting'])

        # Adding model 'EventreportingFile'
        db.create_table(u'ippc_eventreportingfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eventreporting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.EventReporting'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['EventreportingFile'])

        # Adding model 'EventreportingUrl'
        db.create_table(u'ippc_eventreportingurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eventreporting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.EventReporting'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['EventreportingUrl'])

        # Adding model 'Website'
        db.create_table(u'ippc_website', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='website_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='website__reporting_author', to=orm['auth.User'])),
            ('web_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['Website'])

        # Adding model 'WebsiteUrl'
        db.create_table(u'ippc_websiteurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.Website'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['WebsiteUrl'])

        # Adding model 'PartnersWebsite'
        db.create_table(u'ippc_partnerswebsite', (
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
            ('partners', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partnerswebsite_partner_page', to=orm['ippc.PartnersPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partnerswebsite__reporting_author', to=orm['auth.User'])),
            ('web_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersWebsite'])

        # Adding model 'PartnersWebsiteUrl'
        db.create_table(u'ippc_partnerswebsiteurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partnerswebsite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PartnersWebsite'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersWebsiteUrl'])

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
            ('pest_under_consideration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pfa_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['PestFreeArea'])

        # Adding model 'PestFreeAreaFile'
        db.create_table(u'ippc_pestfreeareafile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pfa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PestFreeArea'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PestFreeAreaFile'])

        # Adding model 'PestFreeAreaUrl'
        db.create_table(u'ippc_pestfreeareaurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pfa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PestFreeArea'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PestFreeAreaUrl'])

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
            ('mark_registered_type', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
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

        # Adding model 'ImplementationISPMFile'
        db.create_table(u'ippc_implementationispmfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('implementationispm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.ImplementationISPM'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['ImplementationISPMFile'])

        # Adding model 'ImplementationISPMUrl'
        db.create_table(u'ippc_implementationispmurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('implementationispm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.ImplementationISPM'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['ImplementationISPMUrl'])

        # Adding model 'CountryNews'
        db.create_table(u'ippc_countrynews', (
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
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='countrynews_country_page', to=orm['ippc.CountryPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='countrynews_author', to=orm['auth.User'])),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['CountryNews'])

        # Adding model 'CountryNewsFile'
        db.create_table(u'ippc_countrynewsfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('countrynews', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.CountryNews'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['CountryNewsFile'])

        # Adding model 'CountryNewsUrl'
        db.create_table(u'ippc_countrynewsurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('countrynews', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.CountryNews'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['CountryNewsUrl'])

        # Adding model 'PartnersNews'
        db.create_table(u'ippc_partnersnews', (
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
            ('partners', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partnersnews_partner_page', to=orm['ippc.PartnersPage'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partnersnews_author', to=orm['auth.User'])),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('contact_for_more_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersNews'])

        # Adding model 'PartnersNewsFile'
        db.create_table(u'ippc_partnersnewsfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partnersnews', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PartnersNews'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersNewsFile'])

        # Adding model 'PartnersNewsUrl'
        db.create_table(u'ippc_partnersnewsurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partnersnews', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.PartnersNews'])),
            ('url_for_more_information', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['PartnersNewsUrl'])

        # Adding model 'Poll'
        db.create_table(u'ippc_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('polltext', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('closing_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('login_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ippc', ['Poll'])

        # Adding M2M table for field userspoll on 'Poll'
        m2m_table_name = db.shorten_name(u'ippc_poll_userspoll')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm[u'ippc.poll'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['poll_id', 'user_id'])

        # Adding M2M table for field groupspoll on 'Poll'
        m2m_table_name = db.shorten_name(u'ippc_poll_groupspoll')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm[u'ippc.poll'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['poll_id', 'group_id'])

        # Adding model 'Poll_Choice'
        db.create_table(u'ippc_poll_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.Poll'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'ippc', ['Poll_Choice'])

        # Adding model 'PollVotes'
        db.create_table(u'ippc_pollvotes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.Poll'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'ippc', ['PollVotes'])

        # Adding model 'EmailUtilityMessage'
        db.create_table(u'ippc_emailutilitymessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emailfrom', self.gf('django.db.models.fields.CharField')(default=u'ippc@fao.org', max_length=200)),
            ('emailto', self.gf('django.db.models.fields.CharField')(default=u'ippc@fao.org', max_length=200)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('messagebody', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ippc', ['EmailUtilityMessage'])

        # Adding M2M table for field users on 'EmailUtilityMessage'
        m2m_table_name = db.shorten_name(u'ippc_emailutilitymessage_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('emailutilitymessage', models.ForeignKey(orm[u'ippc.emailutilitymessage'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['emailutilitymessage_id', 'user_id'])

        # Adding M2M table for field groups on 'EmailUtilityMessage'
        m2m_table_name = db.shorten_name(u'ippc_emailutilitymessage_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('emailutilitymessage', models.ForeignKey(orm[u'ippc.emailutilitymessage'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['emailutilitymessage_id', 'group_id'])

        # Adding model 'EmailUtilityMessageFile'
        db.create_table(u'ippc_emailutilitymessagefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emailmessage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ippc.EmailUtilityMessage'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ippc', ['EmailUtilityMessageFile'])

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


    def backwards(self, orm):
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

        # Deleting model 'IssueKeyword'
        db.delete_table(u'ippc_issuekeyword')

        # Deleting model 'CommodityKeyword'
        db.delete_table(u'ippc_commoditykeyword')

        # Deleting model 'IssueKeywordsRelate'
        db.delete_table(u'ippc_issuekeywordsrelate')

        # Removing M2M table for field issuename on 'IssueKeywordsRelate'
        db.delete_table(db.shorten_name(u'ippc_issuekeywordsrelate_issuename'))

        # Deleting model 'CommodityKeywordsRelate'
        db.delete_table(u'ippc_commoditykeywordsrelate')

        # Removing M2M table for field commname on 'CommodityKeywordsRelate'
        db.delete_table(db.shorten_name(u'ippc_commoditykeywordsrelate_commname'))

        # Deleting model 'CountryPage'
        db.delete_table(u'ippc_countrypage')

        # Removing M2M table for field editors on 'CountryPage'
        db.delete_table(db.shorten_name(u'ippc_countrypage_editors'))

        # Deleting model 'PartnersPage'
        db.delete_table(u'ippc_partnerspage')

        # Removing M2M table for field editors on 'PartnersPage'
        db.delete_table(db.shorten_name(u'ippc_partnerspage_editors'))

        # Deleting model 'NotificationMessageRelate'
        db.delete_table(u'ippc_notificationmessagerelate')

        # Removing M2M table for field countries on 'NotificationMessageRelate'
        db.delete_table(db.shorten_name(u'ippc_notificationmessagerelate_countries'))

        # Removing M2M table for field partners on 'NotificationMessageRelate'
        db.delete_table(db.shorten_name(u'ippc_notificationmessagerelate_partners'))

        # Deleting model 'Publication'
        db.delete_table(u'ippc_publication')

        # Deleting model 'PublicationFile'
        db.delete_table(u'ippc_publicationfile')

        # Deleting model 'PublicationUrl'
        db.delete_table(u'ippc_publicationurl')

        # Deleting model 'WorkAreaPage'
        db.delete_table(u'ippc_workareapage')

        # Removing M2M table for field users on 'WorkAreaPage'
        db.delete_table(db.shorten_name(u'ippc_workareapage_users'))

        # Removing M2M table for field groups on 'WorkAreaPage'
        db.delete_table(db.shorten_name(u'ippc_workareapage_groups'))

        # Deleting model 'PestStatus'
        db.delete_table(u'ippc_peststatus')

        # Deleting model 'PreferredLanguages'
        db.delete_table(u'ippc_preferredlanguages')

        # Deleting model 'EppoCode'
        db.delete_table(u'ippc_eppocode')

        # Deleting model 'ContactType'
        db.delete_table(u'ippc_contacttype')

        # Deleting model 'IppcUserProfile'
        db.delete_table(u'ippc_ippcuserprofile')

        # Removing M2M table for field contact_type on 'IppcUserProfile'
        db.delete_table(db.shorten_name(u'ippc_ippcuserprofile_contact_type'))

        # Removing M2M table for field preferredlanguage on 'IppcUserProfile'
        db.delete_table(db.shorten_name(u'ippc_ippcuserprofile_preferredlanguage'))

        # Deleting model 'PestReport'
        db.delete_table(u'ippc_pestreport')

        # Removing M2M table for field pest_status on 'PestReport'
        db.delete_table(db.shorten_name(u'ippc_pestreport_pest_status'))

        # Deleting model 'PestReportFile'
        db.delete_table(u'ippc_pestreportfile')

        # Deleting model 'PestReportUrl'
        db.delete_table(u'ippc_pestreporturl')

        # Deleting model 'DraftProtocol'
        db.delete_table(u'ippc_draftprotocol')

        # Removing M2M table for field users on 'DraftProtocol'
        db.delete_table(db.shorten_name(u'ippc_draftprotocol_users'))

        # Removing M2M table for field groups on 'DraftProtocol'
        db.delete_table(db.shorten_name(u'ippc_draftprotocol_groups'))

        # Deleting model 'DraftProtocolFile'
        db.delete_table(u'ippc_draftprotocolfile')

        # Deleting model 'DraftProtocolComments'
        db.delete_table(u'ippc_draftprotocolcomments')

        # Deleting model 'ReportingObligation'
        db.delete_table(u'ippc_reportingobligation')

        # Deleting model 'ReportingObligation_File'
        db.delete_table(u'ippc_reportingobligation_file')

        # Deleting model 'ReportingObligationUrl'
        db.delete_table(u'ippc_reportingobligationurl')

        # Deleting model 'CnPublication'
        db.delete_table(u'ippc_cnpublication')

        # Deleting model 'CnPublicationFile'
        db.delete_table(u'ippc_cnpublicationfile')

        # Deleting model 'CnPublicationUrl'
        db.delete_table(u'ippc_cnpublicationurl')

        # Deleting model 'PartnersPublication'
        db.delete_table(u'ippc_partnerspublication')

        # Deleting model 'PartnersPublicationFile'
        db.delete_table(u'ippc_partnerspublicationfile')

        # Deleting model 'PartnersPublicationUrl'
        db.delete_table(u'ippc_partnerspublicationurl')

        # Deleting model 'EventReporting'
        db.delete_table(u'ippc_eventreporting')

        # Deleting model 'EventreportingFile'
        db.delete_table(u'ippc_eventreportingfile')

        # Deleting model 'EventreportingUrl'
        db.delete_table(u'ippc_eventreportingurl')

        # Deleting model 'Website'
        db.delete_table(u'ippc_website')

        # Deleting model 'WebsiteUrl'
        db.delete_table(u'ippc_websiteurl')

        # Deleting model 'PartnersWebsite'
        db.delete_table(u'ippc_partnerswebsite')

        # Deleting model 'PartnersWebsiteUrl'
        db.delete_table(u'ippc_partnerswebsiteurl')

        # Deleting model 'PestFreeArea'
        db.delete_table(u'ippc_pestfreearea')

        # Deleting model 'PestFreeAreaFile'
        db.delete_table(u'ippc_pestfreeareafile')

        # Deleting model 'PestFreeAreaUrl'
        db.delete_table(u'ippc_pestfreeareaurl')

        # Deleting model 'ImplementationISPMVersion'
        db.delete_table(u'ippc_implementationispmversion')

        # Deleting model 'ImplementationISPM'
        db.delete_table(u'ippc_implementationispm')

        # Removing M2M table for field implementimport_version on 'ImplementationISPM'
        db.delete_table(db.shorten_name(u'ippc_implementationispm_implementimport_version'))

        # Removing M2M table for field implementexport_version on 'ImplementationISPM'
        db.delete_table(db.shorten_name(u'ippc_implementationispm_implementexport_version'))

        # Deleting model 'ImplementationISPMFile'
        db.delete_table(u'ippc_implementationispmfile')

        # Deleting model 'ImplementationISPMUrl'
        db.delete_table(u'ippc_implementationispmurl')

        # Deleting model 'CountryNews'
        db.delete_table(u'ippc_countrynews')

        # Deleting model 'CountryNewsFile'
        db.delete_table(u'ippc_countrynewsfile')

        # Deleting model 'CountryNewsUrl'
        db.delete_table(u'ippc_countrynewsurl')

        # Deleting model 'PartnersNews'
        db.delete_table(u'ippc_partnersnews')

        # Deleting model 'PartnersNewsFile'
        db.delete_table(u'ippc_partnersnewsfile')

        # Deleting model 'PartnersNewsUrl'
        db.delete_table(u'ippc_partnersnewsurl')

        # Deleting model 'Poll'
        db.delete_table(u'ippc_poll')

        # Removing M2M table for field userspoll on 'Poll'
        db.delete_table(db.shorten_name(u'ippc_poll_userspoll'))

        # Removing M2M table for field groupspoll on 'Poll'
        db.delete_table(db.shorten_name(u'ippc_poll_groupspoll'))

        # Deleting model 'Poll_Choice'
        db.delete_table(u'ippc_poll_choice')

        # Deleting model 'PollVotes'
        db.delete_table(u'ippc_pollvotes')

        # Deleting model 'EmailUtilityMessage'
        db.delete_table(u'ippc_emailutilitymessage')

        # Removing M2M table for field users on 'EmailUtilityMessage'
        db.delete_table(db.shorten_name(u'ippc_emailutilitymessage_users'))

        # Removing M2M table for field groups on 'EmailUtilityMessage'
        db.delete_table(db.shorten_name(u'ippc_emailutilitymessage_groups'))

        # Deleting model 'EmailUtilityMessageFile'
        db.delete_table(u'ippc_emailutilitymessagefile')

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
        u'ippc.cnpublication': {
            'Meta': {'object_name': 'CnPublication'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'agenda_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cnpublicatio_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cnpublication_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.cnpublicationfile': {
            'Meta': {'object_name': 'CnPublicationFile'},
            'cnpublication': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.CnPublication']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ippc.cnpublicationurl': {
            'Meta': {'object_name': 'CnPublicationUrl'},
            'cnpublication': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.CnPublication']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.commoditykeyword': {
            'Meta': {'object_name': 'CommodityKeyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.commoditykeywordsrelate': {
            'Meta': {'object_name': 'CommodityKeywordsRelate'},
            'commname': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ippc.CommodityKeyword']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'ippc.contacttype': {
            'Meta': {'object_name': 'ContactType'},
            'contacttype': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ippc.countrynews': {
            'Meta': {'object_name': 'CountryNews'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'countrynews_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'countrynews_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.countrynewsfile': {
            'Meta': {'object_name': 'CountryNewsFile'},
            'countrynews': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.CountryNews']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ippc.countrynewsurl': {
            'Meta': {'object_name': 'CountryNewsUrl'},
            'countrynews': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.CountryNews']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.countrypage': {
            'Meta': {'ordering': "['name']", 'object_name': 'CountryPage', '_ormbases': [u'pages.Page']},
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
            'region': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'ippc.draftprotocol': {
            'Meta': {'object_name': 'DraftProtocol'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'closing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filefig': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'filetext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'dpgroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'dpusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'ippc.draftprotocolcomments': {
            'Meta': {'object_name': 'DraftProtocolComments'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'draftprotocolcomments_author'", 'to': u"orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draftprotocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.DraftProtocol']"}),
            'expertise': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filefig': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'filetext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'institution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.draftprotocolfile': {
            'Meta': {'object_name': 'DraftProtocolFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'draftprotocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.DraftProtocol']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ippc.emailutilitymessage': {
            'Meta': {'object_name': 'EmailUtilityMessage'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'emailfrom': ('django.db.models.fields.CharField', [], {'default': "u'ippc@fao.org'", 'max_length': '200'}),
            'emailto': ('django.db.models.fields.CharField', [], {'default': "u'ippc@fao.org'", 'max_length': '200'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'emailgroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messagebody': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'emailusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'ippc.emailutilitymessagefile': {
            'Meta': {'object_name': 'EmailUtilityMessageFile'},
            'emailmessage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.EmailUtilityMessage']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ippc.eppocode': {
            'Meta': {'object_name': 'EppoCode'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'codedescr': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'codeparent': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'creationdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'preferred': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.eventreportingfile': {
            'Meta': {'object_name': 'EventreportingFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'eventreporting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.EventReporting']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ippc.eventreportingurl': {
            'Meta': {'object_name': 'EventreportingUrl'},
            'eventreporting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.EventReporting']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.implementationispm': {
            'Meta': {'object_name': 'ImplementationISPM'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'implementationispm_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'implementationispm_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.implementationispmfile': {
            'Meta': {'object_name': 'ImplementationISPMFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementationispm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.ImplementationISPM']"})
        },
        u'ippc.implementationispmurl': {
            'Meta': {'object_name': 'ImplementationISPMUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementationispm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.ImplementationISPM']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.implementationispmversion': {
            'Meta': {'object_name': 'ImplementationISPMVersion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'ippc.ippcuserprofile': {
            'Meta': {'object_name': 'IppcUserProfile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'address2': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'address_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contact_type+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ippc.ContactType']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_country_page'", 'null': 'True', 'to': u"orm['ippc.CountryPage']"}),
            'date_account_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email_address_alt': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'expertize': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_partner_page'", 'null': 'True', 'to': u"orm['ippc.PartnersPage']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'preferredlanguage': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'preferredlanguages+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ippc.PreferredLanguages']"}),
            'profile_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'ippc.issuekeyword': {
            'Meta': {'object_name': 'IssueKeyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.issuekeywordsrelate': {
            'Meta': {'object_name': 'IssueKeywordsRelate'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuename': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ippc.IssueKeyword']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'ippc.notificationmessagerelate': {
            'Meta': {'object_name': 'NotificationMessageRelate'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notificatiocountries'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ippc.CountryPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notifysecretariat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'partners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notificatiopartners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ippc.PartnersPage']"})
        },
        u'ippc.partnersnews': {
            'Meta': {'object_name': 'PartnersNews'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partnersnews_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'partners': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partnersnews_partner_page'", 'to': u"orm['ippc.PartnersPage']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.partnersnewsfile': {
            'Meta': {'object_name': 'PartnersNewsFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partnersnews': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PartnersNews']"})
        },
        u'ippc.partnersnewsurl': {
            'Meta': {'object_name': 'PartnersNewsUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partnersnews': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PartnersNews']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.partnerspage': {
            'Meta': {'ordering': "['name']", 'object_name': 'PartnersPage', '_ormbases': [u'pages.Page']},
            'contact_point': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rppoeditors+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'partner_slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '550'})
        },
        u'ippc.partnerspublication': {
            'Meta': {'object_name': 'PartnersPublication'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'agenda_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partnerspublication_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'partners': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partnerspublication_country_page'", 'to': u"orm['ippc.PartnersPage']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.partnerspublicationfile': {
            'Meta': {'object_name': 'PartnersPublicationFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partnerspublication': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PartnersPublication']"})
        },
        u'ippc.partnerspublicationurl': {
            'Meta': {'object_name': 'PartnersPublicationUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partnerspublication': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PartnersPublication']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.partnerswebsite': {
            'Meta': {'object_name': 'PartnersWebsite'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partnerswebsite__reporting_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'partners': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partnerswebsite_partner_page'", 'to': u"orm['ippc.PartnersPage']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'web_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'ippc.partnerswebsiteurl': {
            'Meta': {'object_name': 'PartnersWebsiteUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partnerswebsite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PartnersWebsite']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.pestfreearea': {
            'Meta': {'object_name': 'PestFreeArea'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pestfreearea_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pestfreearea_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pest_under_consideration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pfa_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.pestfreeareafile': {
            'Meta': {'object_name': 'PestFreeAreaFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pfa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PestFreeArea']"})
        },
        u'ippc.pestfreeareaurl': {
            'Meta': {'object_name': 'PestFreeAreaUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pfa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PestFreeArea']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.pestreport': {
            'Meta': {'object_name': 'PestReport'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pest_report_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pest_report_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'geographical_distribution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hosts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nature_of_danger': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pest_identity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.EppoCode']", 'null': 'True', 'blank': 'True'}),
            'pest_status': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pest_status+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ippc.PestStatus']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'report_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_status': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.pestreportfile': {
            'Meta': {'object_name': 'PestReportFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pestreport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PestReport']"})
        },
        u'ippc.pestreporturl': {
            'Meta': {'object_name': 'PestReportUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pestreport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.PestReport']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.peststatus': {
            'Meta': {'object_name': 'PestStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.poll': {
            'Meta': {'object_name': 'Poll'},
            'closing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'groupspoll': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pollgroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'polltext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userspoll': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pollusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'ippc.poll_choice': {
            'Meta': {'object_name': 'Poll_Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'ippc.pollvotes': {
            'Meta': {'object_name': 'PollVotes'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.Poll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'ippc.preferredlanguages': {
            'Meta': {'object_name': 'PreferredLanguages'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.publication': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Publication'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'agenda_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.publicationfile': {
            'Meta': {'object_name': 'PublicationFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.Publication']"})
        },
        u'ippc.publicationlibrary': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'PublicationLibrary', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publicationlibrarygroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publicationlibraryusers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'ippc.publicationurl': {
            'Meta': {'object_name': 'PublicationUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.Publication']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'ippc.reportingobligation': {
            'Meta': {'object_name': 'ReportingObligation'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reporting_obligation_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reporting_obligation_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_obligation_type': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'ippc.reportingobligation_file': {
            'Meta': {'object_name': 'ReportingObligation_File'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reportingobligation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.ReportingObligation']"})
        },
        u'ippc.reportingobligationurl': {
            'Meta': {'object_name': 'ReportingObligationUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reportingobligation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.ReportingObligation']"}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('lang',)", 'object_name': 'TransPublicationLibraryPage'},
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
        u'ippc.website': {
            'Meta': {'object_name': 'Website'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'website__reporting_author'", 'to': u"orm['auth.User']"}),
            'contact_for_more_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'website_country_page'", 'to': u"orm['ippc.CountryPage']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'web_type': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'ippc.websiteurl': {
            'Meta': {'object_name': 'WebsiteUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_for_more_information': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ippc.Website']"})
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