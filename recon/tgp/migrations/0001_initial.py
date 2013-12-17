# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Telegram'
        db.create_table(u'tgp_telegram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('circuit', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('province', self.gf('django.db.models.fields.CharField')(default=u'C\xf3rdoba', max_length=15)),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('tables', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tgp.Table'])),
        ))
        db.send_create_signal(u'tgp', ['Telegram'])

        # Adding model 'Table'
        db.create_table(u'tgp_table', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cells', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tgp.Cell'])),
        ))
        db.send_create_signal(u'tgp', ['Table'])

        # Adding model 'Cell'
        db.create_table(u'tgp_cell', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('score', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=3)),
        ))
        db.send_create_signal(u'tgp', ['Cell'])


    def backwards(self, orm):
        # Deleting model 'Telegram'
        db.delete_table(u'tgp_telegram')

        # Deleting model 'Table'
        db.delete_table(u'tgp_table')

        # Deleting model 'Cell'
        db.delete_table(u'tgp_cell')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'province': ('django.db.models.fields.CharField', [], {'default': "u'C\\xf3rdoba'", 'max_length': '15'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tables': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tgp.Table']"})
        }
    }

    complete_apps = ['tgp']