# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SimpleStructuralModel'
        db.create_table(u'marginal_simplestructuralmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beta1', self.gf('django.db.models.fields.FloatField')()),
            ('std_dev1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'], null=True, blank=True)),
            ('valid_after', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 6, 0, 0))),
            ('min_value', self.gf('django.db.models.fields.FloatField')()),
            ('max_value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('marginal', ['SimpleStructuralModel'])

        # Adding unique constraint on 'SimpleStructuralModel', fields ['ba', 'min_value', 'max_value', 'valid_after']
        db.create_unique(u'marginal_simplestructuralmodel', ['ba_id', 'min_value', 'max_value', 'valid_after'])

        # Adding model 'BaseCarbon'
        db.create_table(u'marginal_basecarbon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dp', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['griddata.DataPoint'], unique=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('marginal', ['BaseCarbon'])

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


    def backwards(self, orm):
        # Removing unique constraint on 'SimpleStructuralModel', fields ['ba', 'min_value', 'max_value', 'valid_after']
        db.delete_unique(u'marginal_simplestructuralmodel', ['ba_id', 'min_value', 'max_value', 'valid_after'])

        # Deleting model 'SimpleStructuralModel'
        db.delete_table(u'marginal_simplestructuralmodel')

        # Deleting model 'BaseCarbon'
        db.delete_table(u'marginal_basecarbon')

        # Deleting model 'SilerEvansModel'
        db.delete_table(u'marginal_silerevansmodel')

        # Deleting model 'SilerEvansMOER'
        db.delete_table(u'marginal_silerevansmoer')


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
            'Meta': {'unique_together': "(('ba', 'min_value', 'max_value', 'valid_after'),)", 'object_name': 'SimpleStructuralModel'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']", 'null': 'True', 'blank': 'True'}),
            'beta1': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.FloatField', [], {}),
            'min_value': ('django.db.models.fields.FloatField', [], {}),
            'std_dev1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valid_after': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 6, 0, 0)'})
        }
    }

    complete_apps = ['marginal']