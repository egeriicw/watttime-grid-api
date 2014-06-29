# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CurrentDataSet'
        db.create_table(u'griddata_currentdataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'])),
            ('current', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['griddata.DataPoint'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'griddata', ['CurrentDataSet'])

        # Adding M2M table for field past on 'CurrentDataSet'
        m2m_table_name = db.shorten_name(u'griddata_currentdataset_past')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('currentdataset', models.ForeignKey(orm[u'griddata.currentdataset'], null=False)),
            ('datapoint', models.ForeignKey(orm[u'griddata.datapoint'], null=False))
        ))
        db.create_unique(m2m_table_name, ['currentdataset_id', 'datapoint_id'])

        # Adding M2M table for field forecast on 'CurrentDataSet'
        m2m_table_name = db.shorten_name(u'griddata_currentdataset_forecast')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('currentdataset', models.ForeignKey(orm[u'griddata.currentdataset'], null=False)),
            ('datapoint', models.ForeignKey(orm[u'griddata.datapoint'], null=False))
        ))
        db.create_unique(m2m_table_name, ['currentdataset_id', 'datapoint_id'])


    def backwards(self, orm):
        # Deleting model 'CurrentDataSet'
        db.delete_table(u'griddata_currentdataset')

        # Removing M2M table for field past on 'CurrentDataSet'
        db.delete_table(db.shorten_name(u'griddata_currentdataset_past'))

        # Removing M2M table for field forecast on 'CurrentDataSet'
        db.delete_table(db.shorten_name(u'griddata_currentdataset_forecast'))


    models = {
        u'griddata.currentdataset': {
            'Meta': {'object_name': 'CurrentDataSet'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']"}),
            'current': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['griddata.DataPoint']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'forecast': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forecast_set'", 'symmetrical': 'False', 'to': u"orm['griddata.DataPoint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'past': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'past_set'", 'symmetrical': 'False', 'to': u"orm['griddata.DataPoint']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
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