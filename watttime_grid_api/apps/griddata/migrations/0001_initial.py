# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataPoint'
        db.create_table(u'griddata_datapoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('quality', self.gf('django.db.models.fields.CharField')(default='PAST', max_length=4)),
            ('freq', self.gf('django.db.models.fields.CharField')(default='1hr', max_length=4)),
            ('market', self.gf('django.db.models.fields.CharField')(default='RTHR', max_length=4)),
            ('is_marginal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'])),
        ))
        db.send_create_signal(u'griddata', ['DataPoint'])

        # Adding unique constraint on 'DataPoint', fields ['timestamp', 'quality', 'freq', 'market', 'is_marginal', 'ba']
        db.create_unique(u'griddata_datapoint', ['timestamp', 'quality', 'freq', 'market', 'is_marginal', 'ba_id'])

        # Adding model 'DataSeries'
        db.create_table(u'griddata_dataseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'])),
            ('series_type', self.gf('django.db.models.fields.CharField')(default='PAST', max_length=4)),
        ))
        db.send_create_signal(u'griddata', ['DataSeries'])

        # Adding M2M table for field datapoints on 'DataSeries'
        m2m_table_name = db.shorten_name(u'griddata_dataseries_datapoints')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dataseries', models.ForeignKey(orm[u'griddata.dataseries'], null=False)),
            ('datapoint', models.ForeignKey(orm[u'griddata.datapoint'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dataseries_id', 'datapoint_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'DataPoint', fields ['timestamp', 'quality', 'freq', 'market', 'is_marginal', 'ba']
        db.delete_unique(u'griddata_datapoint', ['timestamp', 'quality', 'freq', 'market', 'is_marginal', 'ba_id'])

        # Deleting model 'DataPoint'
        db.delete_table(u'griddata_datapoint')

        # Deleting model 'DataSeries'
        db.delete_table(u'griddata_dataseries')

        # Removing M2M table for field datapoints on 'DataSeries'
        db.delete_table(db.shorten_name(u'griddata_dataseries_datapoints'))


    models = {
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
        u'griddata.dataseries': {
            'Meta': {'object_name': 'DataSeries'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']"}),
            'datapoints': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['griddata.DataPoint']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'series_type': ('django.db.models.fields.CharField', [], {'default': "'PAST'", 'max_length': '4'})
        },
        u'gridentities.balancingauthority': {
            'Meta': {'object_name': 'BalancingAuthority'},
            'abbrev': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'ba_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['griddata']