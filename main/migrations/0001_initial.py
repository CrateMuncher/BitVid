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
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
            ('videoes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Video'])),
        ))
        db.send_create_signal(u'main', ['Channel'])

        # Adding model 'Video'
        db.create_table(u'main_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
            ('uploader', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.User'], unique=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')()),
            ('comments', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
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
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('login_token', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'main', ['User'])

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
            ('author', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.User'], unique=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
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


    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_table(u'main_channel')

        # Deleting model 'Video'
        db.delete_table(u'main_video')

        # Removing M2M table for field likers on 'Video'
        db.delete_table(db.shorten_name(u'main_video_likers'))

        # Removing M2M table for field dislikers on 'Video'
        db.delete_table(db.shorten_name(u'main_video_dislikers'))

        # Deleting model 'User'
        db.delete_table(u'main_user')

        # Removing M2M table for field channels on 'User'
        db.delete_table(db.shorten_name(u'main_user_channels'))

        # Deleting model 'Comment'
        db.delete_table(u'main_comment')

        # Removing M2M table for field likers on 'Comment'
        db.delete_table(db.shorten_name(u'main_comment_likers'))

        # Removing M2M table for field dislikers on 'Comment'
        db.delete_table(db.shorten_name(u'main_comment_dislikers'))


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'videoes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Video']"})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.User']", 'unique': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'dislikers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'disliked_comments'", 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'liked_comments'", 'symmetrical': 'False', 'to': u"orm['main.User']"})
        },
        u'main.user': {
            'Meta': {'object_name': 'User'},
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Channel']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_token': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'main.video': {
            'Meta': {'object_name': 'Video'},
            'comments': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dislikers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'disliked_videoes'", 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'liked_videoes'", 'symmetrical': 'False', 'to': u"orm['main.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uploader': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.User']", 'unique': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']