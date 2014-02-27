# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FuelCarbonIntensity.ba'
        db.alter_column(u'carbon_fuelcarbonintensity', 'ba_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'], null=True))

    def backwards(self, orm):

        # Changing field 'FuelCarbonIntensity.ba'
        db.alter_column(u'carbon_fuelcarbonintensity', 'ba_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gridentities.BalancingAuthority']))

    models = {
        u'carbon.carbon': {
            'Meta': {'object_name': 'Carbon'},
            'dp': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'carbon'", 'unique': 'True', 'to': u"orm['griddata.DataPoint']"}),
            'emissions_intensity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fuel_carbons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['carbon.FuelCarbonIntensity']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'carbon.fuelcarbonintensity': {
            'Meta': {'object_name': 'FuelCarbonIntensity'},
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']", 'null': 'True', 'blank': 'True'}),
            'fuel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.FuelType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lb_CO2_per_MW': ('django.db.models.fields.FloatField', [], {}),
            'valid_after': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 27, 0, 0)'})
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
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'ba_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        u'gridentities.fueltype': {
            'Meta': {'object_name': 'FuelType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fossil': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_renewable': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['carbon']