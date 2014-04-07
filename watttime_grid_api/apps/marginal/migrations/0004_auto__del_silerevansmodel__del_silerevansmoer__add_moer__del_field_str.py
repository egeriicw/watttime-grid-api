# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'StructuralModelSet', fields ['ba', 'valid_after', 'model_name']
        db.delete_unique(u'marginal_structuralmodelset', ['ba_id', 'valid_after', 'model_name'])

        # Deleting model 'SilerEvansModel'
        db.delete_table(u'marginal_silerevansmodel')

        # Deleting model 'SilerEvansMOER'
        db.delete_table(u'marginal_silerevansmoer')

        # Adding model 'MOER'
        db.create_table(u'marginal_moer', (
            (u'basecarbon_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['marginal.BaseCarbon'], unique=True, primary_key=True)),
            ('structural_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marginal.StructuralModelSet'], null=True, blank=True)),
        ))
        db.send_create_signal('marginal', ['MOER'])

        # Deleting field 'StructuralModelSet.model_name'
        db.delete_column(u'marginal_structuralmodelset', 'model_name')

        # Adding field 'StructuralModelSet.algorithm'
        db.add_column(u'marginal_structuralmodelset', 'algorithm',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['marginal.MOERAlgorithm']),
                      keep_default=False)

        # Adding unique constraint on 'StructuralModelSet', fields ['algorithm', 'ba', 'valid_after']
        db.create_unique(u'marginal_structuralmodelset', ['algorithm_id', 'ba_id', 'valid_after'])


    def backwards(self, orm):
        # Removing unique constraint on 'StructuralModelSet', fields ['algorithm', 'ba', 'valid_after']
        db.delete_unique(u'marginal_structuralmodelset', ['algorithm_id', 'ba_id', 'valid_after'])

        # Adding model 'SilerEvansModel'
        db.create_table(u'marginal_silerevansmodel', (
            (u'simplestructuralmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['marginal.SimpleStructuralModel'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('marginal', ['SilerEvansModel'])

        # Adding model 'SilerEvansMOER'
        db.create_table(u'marginal_silerevansmoer', (
            (u'basecarbon_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['marginal.BaseCarbon'], unique=True, primary_key=True)),
            ('structural_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marginal.SilerEvansModel'], null=True, blank=True)),
        ))
        db.send_create_signal('marginal', ['SilerEvansMOER'])

        # Deleting model 'MOER'
        db.delete_table(u'marginal_moer')

        # Adding field 'StructuralModelSet.model_name'
        db.add_column(u'marginal_structuralmodelset', 'model_name',
                      self.gf('django.db.models.fields.CharField')(default='silerevansmodel', max_length=50),
                      keep_default=False)

        # Deleting field 'StructuralModelSet.algorithm'
        db.delete_column(u'marginal_structuralmodelset', 'algorithm_id')

        # Adding unique constraint on 'StructuralModelSet', fields ['ba', 'valid_after', 'model_name']
        db.create_unique(u'marginal_structuralmodelset', ['ba_id', 'valid_after', 'model_name'])


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
        'marginal.moer': {
            'Meta': {'object_name': 'MOER', '_ormbases': ['marginal.BaseCarbon']},
            u'basecarbon_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['marginal.BaseCarbon']", 'unique': 'True', 'primary_key': 'True'}),
            'structural_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marginal.StructuralModelSet']", 'null': 'True', 'blank': 'True'})
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
            'Meta': {'object_name': 'SimpleStructuralModel'},
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
            'valid_after': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 7, 0, 0)'})
        }
    }

    complete_apps = ['marginal']