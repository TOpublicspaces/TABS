# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Search.committee'
        db.add_column('main_search', 'committee',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Search.from_date'
        db.add_column('main_search', 'from_date',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Search.to_date'
        db.add_column('main_search', 'to_date',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Search.item_status'
        db.add_column('main_search', 'item_status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Search.committee'
        db.delete_column('main_search', 'committee')

        # Deleting field 'Search.from_date'
        db.delete_column('main_search', 'from_date')

        # Deleting field 'Search.to_date'
        db.delete_column('main_search', 'to_date')

        # Deleting field 'Search.item_status'
        db.delete_column('main_search', 'item_status')


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