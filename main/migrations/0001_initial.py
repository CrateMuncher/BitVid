# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Channel'
        db.create_table(u'main_channel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('videoes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Video'])),
        ))
        db.send_create_signal(u'main', ['Channel'])

        # Adding M2M table for field subscribers on 'Channel'
        m2m_table_name = db.shorten_name(u'main_channel_subscribers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm[u'main.channel'], null=False)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['channel_id', 'user_id'])

        # Adding model 'Video'
        db.create_table(u'main_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('uploader', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.User'], unique=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('video_files', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video', null=True, to=orm['main.VideoFile'])),
            ('comments', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video', null=True, to=orm['main.Comment'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Video'])

        # Adding M2M table for field likers on 'Video'
        m2m_table_name = db.shorten_name(u'main_video_likers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm[u'main.video'], null=False)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['video_id', 'user_id'])

        # Adding M2M table for field dislikers on 'Video'
        m2m_table_name = db.shorten_name(u'main_video_dislikers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm[u'main.video'], null=False)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['video_id', 'user_id'])

        # Adding model 'User'
        db.create_table(u'main_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            ('nickname', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('login_token', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('comments', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author', null=True, to=orm['main.Comment'])),
            ('registration_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['User'])

        # Adding M2M table for field tags on 'User'
        m2m_table_name = db.shorten_name(u'main_user_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False)),
            ('tag', models.ForeignKey(orm[u'main.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'tag_id'])

        # Adding M2M table for field channels on 'User'
        m2m_table_name = db.shorten_name(u'main_user_channels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False)),
            ('channel', models.ForeignKey(orm[u'main.channel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'channel_id'])

        # Adding model 'Comment'
        db.create_table(u'main_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'main', ['Comment'])

        # Adding M2M table for field likers on 'Comment'
        m2m_table_name = db.shorten_name(u'main_comment_likers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'main.comment'], null=False)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'user_id'])

        # Adding M2M table for field dislikers on 'Comment'
        m2m_table_name = db.shorten_name(u'main_comment_dislikers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'main.comment'], null=False)),
            ('user', models.ForeignKey(orm[u'main.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'user_id'])

        # Adding model 'VideoFile'
        db.create_table(u'main_videofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('format', self.gf('django.db.models.fields.CharField')(default='', max_length=5)),
            ('codec', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'main', ['VideoFile'])

        # Adding model 'Tag'
        db.create_table(u'main_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'main', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_table(u'main_channel')

        # Removing M2M table for field subscribers on 'Channel'
        db.delete_table(db.shorten_name(u'main_channel_subscribers'))

        # Deleting model 'Video'
        db.delete_table(u'main_video')

        # Removing M2M table for field likers on 'Video'
        db.delete_table(db.shorten_name(u'main_video_likers'))

        # Removing M2M table for field dislikers on 'Video'
        db.delete_table(db.shorten_name(u'main_video_dislikers'))

        # Deleting model 'User'
        db.delete_table(u'main_user')

        # Removing M2M table for field tags on 'User'
        db.delete_table(db.shorten_name(u'main_user_tags'))

        # Removing M2M table for field channels on 'User'
        db.delete_table(db.shorten_name(u'main_user_channels'))

        # Deleting model 'Comment'
        db.delete_table(u'main_comment')

        # Removing M2M table for field likers on 'Comment'
        db.delete_table(db.shorten_name(u'main_comment_likers'))

        # Removing M2M table for field dislikers on 'Comment'
        db.delete_table(db.shorten_name(u'main_comment_dislikers'))

        # Deleting model 'VideoFile'
        db.delete_table(u'main_videofile')

        # Deleting model 'Tag'
        db.delete_table(u'main_tag')


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscriptions'", 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            'videoes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Video']"})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dislikers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'disliked_comments'", 'null': 'True', 'to': u"orm['main.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_comments'", 'null': 'True', 'to': u"orm['main.User']"}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'main.user': {
            'Meta': {'object_name': 'User'},
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'null': 'True', 'to': u"orm['main.Channel']"}),
            'comments': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author'", 'null': 'True', 'to': u"orm['main.Comment']"}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'videoes'", 'null': 'True', 'to': u"orm['main.Tag']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '64'})
        },
        u'main.video': {
            'Meta': {'object_name': 'Video'},
            'comments': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video'", 'null': 'True', 'to': u"orm['main.Comment']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dislikers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'disliked_videoes'", 'null': 'True', 'to': u"orm['main.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_videoes'", 'null': 'True', 'to': u"orm['main.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'uploader': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.User']", 'unique': 'True'}),
            'video_files': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video'", 'null': 'True', 'to': u"orm['main.VideoFile']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.videofile': {
            'Meta': {'object_name': 'VideoFile'},
            'codec': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['main']