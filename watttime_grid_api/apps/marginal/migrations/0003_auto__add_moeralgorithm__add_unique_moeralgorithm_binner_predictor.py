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


    def backwards(self, orm):
        # Removing unique constraint on 'MOERAlgorithm', fields ['binner', 'predictor']
        db.delete_unique(u'marginal_moeralgorithm', ['binner', 'predictor'])

        # Deleting model 'MOERAlgorithm'
        db.delete_table(u'marginal_moeralgorithm')


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
        'marginal.basecarbon': {
            'Meta': {'object_name': 'BaseCarbon'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dp': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['griddata.DataPoint']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'marginal.silerevansmodel': {
            'Meta': {'object_name': 'SilerEvansModel', '_ormbases': ['marginal.SimpleStructuralModel']},
            u'simplestructuralmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['marginal.SimpleStructuralModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        'marginal.silerevansmoer': {
            'Meta': {'object_name': 'SilerEvansMOER', '_ormbases': ['marginal.BaseCarbon']},
            u'basecarbon_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['marginal.BaseCarbon']", 'unique': 'True', 'primary_key': 'True'}),
            'structural_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marginal.SilerEvansModel']", 'null': 'True', 'blank': 'True'})
        },
        'marginal.simplestructuralmodel': {
            'Meta': {'object_name': 'SimpleStructuralModel'},
            'beta1': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.FloatField', [], {}),
            'min_value': ('django.db.models.fields.FloatField', [], {}),
            'model_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marginal.StructuralModelSet']"}),
            'std_dev1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'marginal.structuralmodelset': {
            'Meta': {'unique_together': "(('ba', 'valid_after', 'model_name'),)", 'object_name': 'StructuralModelSet'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "'silerevansmodel'", 'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'valid_after': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 7, 0, 0)'})
        }
    }

    complete_apps = ['marginal']