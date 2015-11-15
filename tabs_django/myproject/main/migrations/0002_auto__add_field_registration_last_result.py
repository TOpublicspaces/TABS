# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Registration.last_result'
        db.add_column('main_registration', 'last_result',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Registration.last_result'
        db.delete_column('main_registration', 'last_result')


    models = {
        'main.registration': {
            'Meta': {'object_name': 'Registration'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
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