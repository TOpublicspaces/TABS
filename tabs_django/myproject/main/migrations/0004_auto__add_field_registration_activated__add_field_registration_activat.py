# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Registration.activated'
        db.add_column('main_registration', 'activated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Registration.activation_key'
        db.add_column('main_registration', 'activation_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Registration.activated'
        db.delete_column('main_registration', 'activated')

        # Deleting field 'Registration.activation_key'
        db.delete_column('main_registration', 'activation_key')


    models = {
        'main.registration': {
            'Meta': {'object_name': 'Registration'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'search_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Search']"})
        },
        'main.search': {
            'Meta': {'object_name': 'Search'},
            'committee': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'from_date': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_status': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'recent_result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'to_date': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'word_or_phrase': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['main']