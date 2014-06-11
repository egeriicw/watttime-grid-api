# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'DataPoint', fields ['ba', 'timestamp', 'is_marginal', 'freq', 'quality', 'market']
        db.delete_unique(u'griddata_datapoint', ['ba_id', 'timestamp', 'is_marginal', 'freq', 'quality', 'market'])

        # Deleting field 'DataPoint.is_marginal'
        db.delete_column(u'griddata_datapoint', 'is_marginal')

        # Deleting field 'DataPoint.quality'
        db.delete_column(u'griddata_datapoint', 'quality')

        # Adding unique constraint on 'DataPoint', fields ['timestamp', 'freq', 'ba', 'market']
        db.create_unique(u'griddata_datapoint', ['timestamp', 'freq', 'ba_id', 'market'])


    def backwards(self, orm):
        # Removing unique constraint on 'DataPoint', fields ['timestamp', 'freq', 'ba', 'market']
        db.delete_unique(u'griddata_datapoint', ['timestamp', 'freq', 'ba_id', 'market'])

        # Adding field 'DataPoint.is_marginal'
        db.add_column(u'griddata_datapoint', 'is_marginal',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'DataPoint.quality'
        db.add_column(u'griddata_datapoint', 'quality',
                      self.gf('django.db.models.fields.CharField')(default='PAST', max_length=4),
                      keep_default=False)

        # Adding unique constraint on 'DataPoint', fields ['ba', 'timestamp', 'is_marginal', 'freq', 'quality', 'market']
        db.create_unique(u'griddata_datapoint', ['ba_id', 'timestamp', 'is_marginal', 'freq', 'quality', 'market'])


    models = {
        u'griddata.datapoint': {
            'Meta': {'ordering': "['-timestamp', 'ba']", 'unique_together': "(('timestamp', 'ba', 'freq', 'market'),)", 'object_name': 'DataPoint'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'freq': ('django.db.models.fields.CharField', [], {'default': "'1hr'", 'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'default': "'RTHR'", 'max_length': '4'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        u'griddata.dataseries': {
            'Meta': {'object_name': 'DataSeries'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']"}),
            'datapoints': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['griddata.DataPoint']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'series_type': ('django.db.models.fields.CharField', [], {'default': "'PAST'", 'max_length': '4'})
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
        }
    }

    complete_apps = ['griddata']