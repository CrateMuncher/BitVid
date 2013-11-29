# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Video', fields ['uploader']
        db.delete_unique(u'main_video', ['uploader_id'])

        # Adding unique constraint on 'Channel', fields ['name']
        db.create_unique(u'main_channel', ['name'])


        # Changing field 'Video.uploader'
        db.alter_column(u'main_video', 'uploader_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.User']))

    def backwards(self, orm):
        # Removing unique constraint on 'Channel', fields ['name']
        db.delete_unique(u'main_channel', ['name'])


        # Changing field 'Video.uploader'
        db.alter_column(u'main_video', 'uploader_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.User'], unique=True))
        # Adding unique constraint on 'Video', fields ['uploader']
        db.create_unique(u'main_video', ['uploader_id'])


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscriptions'", 'symmetrical': 'False', 'to': u"orm['main.User']"})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dislikers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'disliked_comments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_comments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': u"orm['main.Video']"})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'main.user': {
            'Meta': {'object_name': 'User'},
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'members'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Channel']"}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'videoes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Tag']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '64'})
        },
        u'main.video': {
            'Meta': {'object_name': 'Video'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video'", 'null': 'True', 'to': u"orm['main.Channel']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dislikers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'disliked_videoes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_videoes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.User']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.videofile': {
            'Meta': {'object_name': 'VideoFile'},
            'codec': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_files'", 'null': 'True', 'to': u"orm['main.Video']"})
        }
    }

    complete_apps = ['main']