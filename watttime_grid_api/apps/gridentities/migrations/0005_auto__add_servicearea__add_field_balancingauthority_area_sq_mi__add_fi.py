# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceArea'
        db.create_table(u'gridentities_servicearea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal(u'gridentities', ['ServiceArea'])

        # Adding field 'BalancingAuthority.area_sq_mi'
        db.add_column(u'gridentities_balancingauthority', 'area_sq_mi',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BalancingAuthority.bal_auth_id'
        db.add_column(u'gridentities_balancingauthority', 'bal_auth_id',
                      self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BalancingAuthority.rec_id'
        db.add_column(u'gridentities_balancingauthority', 'rec_id',
                      self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BalancingAuthority.service_area'
        db.add_column(u'gridentities_balancingauthority', 'service_area',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.ServiceArea'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ServiceArea'
        db.delete_table(u'gridentities_servicearea')

        # Deleting field 'BalancingAuthority.area_sq_mi'
        db.delete_column(u'gridentities_balancingauthority', 'area_sq_mi')

        # Deleting field 'BalancingAuthority.bal_auth_id'
        db.delete_column(u'gridentities_balancingauthority', 'bal_auth_id')

        # Deleting field 'BalancingAuthority.rec_id'
        db.delete_column(u'gridentities_balancingauthority', 'rec_id')

        # Deleting field 'BalancingAuthority.service_area'
        db.delete_column(u'gridentities_balancingauthority', 'service_area_id')


    models = {
        u'gridentities.balancingauthority': {
            'Meta': {'object_name': 'BalancingAuthority'},
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'area_sq_mi': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ba_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'bal_auth_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'rec_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'service_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.ServiceArea']", 'null': 'True', 'blank': 'True'})
        },
        u'gridentities.fueltype': {
            'Meta': {'object_name': 'FuelType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fossil': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_renewable': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'gridentities.powerplant': {
            'Meta': {'object_name': 'PowerPlant'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'coord': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'fuel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gridentities.FuelType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'gridentities.servicearea': {
            'Meta': {'object_name': 'ServiceArea'},
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['gridentities']