# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MOERAlgorithm'
        db.create_table(u'marginal_moeralgorithm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('binner', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('predictor', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('marginal', ['MOERAlgorithm'])

        # Adding unique constraint on 'MOERAlgorithm', fields ['binner', 'predictor']
        db.create_unique(u'marginal_moeralgorithm', ['binner', 'predictor'])

        # Adding model 'StructuralModelSet'
        db.create_table(u'marginal_structuralmodelset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'], null=True, blank=True)),
            ('valid_after', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 30, 0, 0))),
            ('algorithm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marginal.MOERAlgorithm'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('marginal', ['StructuralModelSet'])

        # Adding unique constraint on 'StructuralModelSet', fields ['ba', 'valid_after', 'algorithm']
        db.create_unique(u'marginal_structuralmodelset', ['ba_id', 'valid_after', 'algorithm_id'])

        # Adding model 'SimpleStructuralModel'
        db.create_table(u'marginal_simplestructuralmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beta1', self.gf('django.db.models.fields.FloatField')()),
            ('std_dev1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('min_value', self.gf('django.db.models.fields.FloatField')()),
            ('max_value', self.gf('django.db.models.fields.FloatField')()),
            ('model_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marginal.StructuralModelSet'])),
        ))
        db.send_create_signal('marginal', ['SimpleStructuralModel'])

        # Adding unique constraint on 'SimpleStructuralModel', fields ['min_value', 'model_set']
        db.create_unique(u'marginal_simplestructuralmodel', ['min_value', 'model_set_id'])

        # Adding model 'MOER'
        db.create_table(u'marginal_moer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['griddata.DataPoint'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('structural_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marginal.StructuralModelSet'], null=True, blank=True)),
        ))
        db.send_create_signal('marginal', ['MOER'])


    def backwards(self, orm):
        # Removing unique constraint on 'SimpleStructuralModel', fields ['min_value', 'model_set']
        db.delete_unique(u'marginal_simplestructuralmodel', ['min_value', 'model_set_id'])

        # Removing unique constraint on 'StructuralModelSet', fields ['ba', 'valid_after', 'algorithm']
        db.delete_unique(u'marginal_structuralmodelset', ['ba_id', 'valid_after', 'algorithm_id'])

        # Removing unique constraint on 'MOERAlgorithm', fields ['binner', 'predictor']
        db.delete_unique(u'marginal_moeralgorithm', ['binner', 'predictor'])

        # Deleting model 'MOERAlgorithm'
        db.delete_table(u'marginal_moeralgorithm')

        # Deleting model 'StructuralModelSet'
        db.delete_table(u'marginal_structuralmodelset')

        # Deleting model 'SimpleStructuralModel'
        db.delete_table(u'marginal_simplestructuralmodel')

        # Deleting model 'MOER'
        db.delete_table(u'marginal_moer')


    models = {
        u'griddata.datapoint': {
            'Meta': {'ordering': "['-timestamp', 'ba', 'quality']", 'unique_together': "(('timestamp', 'ba', 'quality', 'freq', 'market', 'is_marginal'),)", 'object_name': 'DataPoint'},
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
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'area_sq_mi': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ba_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'bal_auth_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'rec_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'marginal.moer': {
            'Meta': {'object_name': 'MOER'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['griddata.DataPoint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structural_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marginal.StructuralModelSet']", 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'marginal.moeralgorithm': {
            'Meta': {'unique_together': "(('binner', 'predictor'),)", 'object_name': 'MOERAlgorithm'},
            'binner': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'predictor': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'marginal.simplestructuralmodel': {
            'Meta': {'unique_together': "(('min_value', 'model_set'),)", 'object_name': 'SimpleStructuralModel'},
            'beta1': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.FloatField', [], {}),
            'min_value': ('django.db.models.fields.FloatField', [], {}),
            'model_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marginal.StructuralModelSet']"}),
            'std_dev1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'marginal.structuralmodelset': {
            'Meta': {'unique_together': "(('ba', 'valid_after', 'algorithm'),)", 'object_name': 'StructuralModelSet'},
            'algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marginal.MOERAlgorithm']"}),
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'valid_after': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 30, 0, 0)'})
        }
    }

    complete_apps = ['marginal']