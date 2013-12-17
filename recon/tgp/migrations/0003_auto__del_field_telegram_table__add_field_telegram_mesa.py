# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Telegram.table'
        db.delete_column(u'tgp_telegram', 'table')

        # Adding field 'Telegram.mesa'
        db.add_column(u'tgp_telegram', 'mesa',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Telegram.table'
        db.add_column(u'tgp_telegram', 'table',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)

        # Deleting field 'Telegram.mesa'
        db.delete_column(u'tgp_telegram', 'mesa')


    models = {
        u'tgp.cell': {
            'Meta': {'object_name': 'Cell'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'score': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '3'})
        },
        u'tgp.table': {
            'Meta': {'object_name': 'Table'},
            'cells': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tgp.Cell']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tgp.telegram': {
            'Meta': {'object_name': 'Telegram'},
            'circuit': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mesa': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'province': ('django.db.models.fields.CharField', [], {'default': "u'C\\xf3rdoba'", 'max_length': '15'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tables': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tgp.Table']"})
        }
    }

    complete_apps = ['tgp']