# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Search'
        db.create_table('main_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word_or_phrase', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('recent_result', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('main', ['Search'])

        # Adding model 'Registration'
        db.create_table('main_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('search_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Search'])),
        ))
        db.send_create_signal('main', ['Registration'])


    def backwards(self, orm):
        # Deleting model 'Search'
        db.delete_table('main_search')

        # Deleting model 'Registration'
        db.delete_table('main_registration')


    models = {
        'main.registration': {
            'Meta': {'object_name': 'Registration'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Search']"})
        },
        'main.search': {
            'Meta': {'object_name': 'Search'},
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recent_result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'word_or_phrase': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['main']