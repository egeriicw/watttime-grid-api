# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Generation'
        db.create_table(u'genmix_generation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fuel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.FuelType'])),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='genmix', to=orm['griddata.DataPoint'])),
            ('gen_MW', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'genmix', ['Generation'])

        # Adding unique constraint on 'Generation', fields ['fuel', 'mix']
        db.create_unique(u'genmix_generation', ['fuel_id', 'mix_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Generation', fields ['fuel', 'mix']
        db.delete_unique(u'genmix_generation', ['fuel_id', 'mix_id'])

        # Deleting model 'Generation'
        db.delete_table(u'genmix_generation')


    models = {
        u'genmix.generation': {
            'Meta': {'unique_together': "(('fuel', 'mix'),)", 'object_name': 'Generation'},
            'fuel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.FuelType']"}),
            'gen_MW': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'genmix'", 'to': u"orm['griddata.DataPoint']"})
        },
        u'griddata.datapoint': {
            'Meta': {'unique_together': "(('timestamp', 'quality', 'freq', 'market', 'is_marginal', 'ba'),)", 'object_name': 'DataPoint'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'freq': ('django.db.models.fields.CharField', [], {'default': "'1hr'", 'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_marginal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'market': ('django.db.models.fields.CharField', [], {'default': "'RTHR'", 'max_length': '4'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "'PAST'", 'max_length': '4'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        u'gridentities.balancingauthority': {
            'Meta': {'object_name': 'BalancingAuthority'},
            'abbrev': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'ba_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'gridentities.fueltype': {
            'Meta': {'object_name': 'FuelType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['genmix']