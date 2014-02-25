# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FuelCarbonIntensity'
        db.create_table(u'carbon_fuelcarbonintensity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fuel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.FuelType'])),
            ('ba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.BalancingAuthority'])),
            ('lb_CO2_per_MW', self.gf('django.db.models.fields.FloatField')()),
            ('valid_after', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 25, 0, 0))),
        ))
        db.send_create_signal(u'carbon', ['FuelCarbonIntensity'])

        # Adding model 'Carbon'
        db.create_table(u'carbon_carbon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dp', self.gf('django.db.models.fields.related.OneToOneField')(related_name='carbon', unique=True, to=orm['griddata.DataPoint'])),
            ('emissions_intensity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'carbon', ['Carbon'])

        # Adding M2M table for field fuel_carbons on 'Carbon'
        m2m_table_name = db.shorten_name(u'carbon_carbon_fuel_carbons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('carbon', models.ForeignKey(orm[u'carbon.carbon'], null=False)),
            ('fuelcarbonintensity', models.ForeignKey(orm[u'carbon.fuelcarbonintensity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['carbon_id', 'fuelcarbonintensity_id'])


    def backwards(self, orm):
        # Deleting model 'FuelCarbonIntensity'
        db.delete_table(u'carbon_fuelcarbonintensity')

        # Deleting model 'Carbon'
        db.delete_table(u'carbon_carbon')

        # Removing M2M table for field fuel_carbons on 'Carbon'
        db.delete_table(db.shorten_name(u'carbon_carbon_fuel_carbons'))


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
            'ba': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.BalancingAuthority']"}),
            'fuel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.FuelType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lb_CO2_per_MW': ('django.db.models.fields.FloatField', [], {}),
            'valid_after': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 25, 0, 0)'})
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

    complete_apps = ['carbon']