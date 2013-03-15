# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'feedjack_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'feedjack', ['Link'])

        # Adding model 'Site'
        db.create_table(u'feedjack_site', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('welcome', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('greets', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_site', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('posts_per_page', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('order_posts_by', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('tagcloud_levels', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('show_tagcloud', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('use_internal_cache', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cache_duration', self.gf('django.db.models.fields.IntegerField')(default=86400)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'feedjack', ['Site'])

        # Adding M2M table for field links on 'Site'
        db.create_table(u'feedjack_site_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('site', models.ForeignKey(orm[u'feedjack.site'], null=False)),
            ('link', models.ForeignKey(orm[u'feedjack.link'], null=False))
        ))
        db.create_unique(u'feedjack_site_links', ['site_id', 'link_id'])

        # Adding model 'Feed'
        db.create_table(u'feedjack_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shortname', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('tagline', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('etag', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feedjack', ['Feed'])

        # Adding model 'Tag'
        db.create_table(u'feedjack_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'feedjack', ['Tag'])

        # Adding model 'Post'
        db.create_table(u'feedjack_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedjack.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('author_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('comments', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'feedjack', ['Post'])

        # Adding unique constraint on 'Post', fields ['feed', 'guid']
        db.create_unique(u'feedjack_post', ['feed_id', 'guid'])

        # Adding M2M table for field tags on 'Post'
        db.create_table(u'feedjack_post_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'feedjack.post'], null=False)),
            ('tag', models.ForeignKey(orm[u'feedjack.tag'], null=False))
        ))
        db.create_unique(u'feedjack_post_tags', ['post_id', 'tag_id'])

        # Adding model 'Subscriber'
        db.create_table(u'feedjack_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedjack.Site'])),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedjack.Feed'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedjack.Group'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('shortname', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'feedjack', ['Subscriber'])

        # Adding unique constraint on 'Subscriber', fields ['site', 'feed']
        db.create_unique(u'feedjack_subscriber', ['site_id', 'feed_id'])

        # Adding model 'Group'
        db.create_table(u'feedjack_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedjack.Group'], null=True, blank=True)),
        ))
        db.send_create_signal(u'feedjack', ['Group'])


    def backwards(self, orm):
        # Removing unique constraint on 'Subscriber', fields ['site', 'feed']
        db.delete_unique(u'feedjack_subscriber', ['site_id', 'feed_id'])

        # Removing unique constraint on 'Post', fields ['feed', 'guid']
        db.delete_unique(u'feedjack_post', ['feed_id', 'guid'])

        # Deleting model 'Link'
        db.delete_table(u'feedjack_link')

        # Deleting model 'Site'
        db.delete_table(u'feedjack_site')

        # Removing M2M table for field links on 'Site'
        db.delete_table('feedjack_site_links')

        # Deleting model 'Feed'
        db.delete_table(u'feedjack_feed')

        # Deleting model 'Tag'
        db.delete_table(u'feedjack_tag')

        # Deleting model 'Post'
        db.delete_table(u'feedjack_post')

        # Removing M2M table for field tags on 'Post'
        db.delete_table('feedjack_post_tags')

        # Deleting model 'Subscriber'
        db.delete_table(u'feedjack_subscriber')

        # Deleting model 'Group'
        db.delete_table(u'feedjack_group')


    models = {
        u'feedjack.feed': {
            'Meta': {'ordering': "('name', 'feed_url')", 'object_name': 'Feed'},
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tagline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'feedjack.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feedjack.Group']", 'null': 'True', 'blank': 'True'})
        },
        u'feedjack.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'feedjack.post': {
            'Meta': {'ordering': "('-date_modified',)", 'unique_together': "(('feed', 'guid'),)", 'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'comments': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feedjack.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['feedjack.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'feedjack.site': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Site'},
            'cache_duration': ('django.db.models.fields.IntegerField', [], {'default': '86400'}),
            'default_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'greets': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['feedjack.Link']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order_posts_by': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'posts_per_page': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'show_tagcloud': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tagcloud_levels': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'use_internal_cache': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'welcome': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'feedjack.subscriber': {
            'Meta': {'ordering': "('site', 'name', 'feed')", 'unique_together': "(('site', 'feed'),)", 'object_name': 'Subscriber'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feedjack.Feed']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feedjack.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feedjack.Site']"})
        },
        u'feedjack.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['feedjack']