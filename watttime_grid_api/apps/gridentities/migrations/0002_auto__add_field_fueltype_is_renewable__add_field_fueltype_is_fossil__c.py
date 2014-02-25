# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FuelType.is_renewable'
        db.add_column(u'gridentities_fueltype', 'is_renewable',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FuelType.is_fossil'
        db.add_column(u'gridentities_fueltype', 'is_fossil',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'FuelType.description'
        db.alter_column(u'gridentities_fueltype', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):
        # Deleting field 'FuelType.is_renewable'
        db.delete_column(u'gridentities_fueltype', 'is_renewable')

        # Deleting field 'FuelType.is_fossil'
        db.delete_column(u'gridentities_fueltype', 'is_fossil')


        # Changing field 'FuelType.description'
        db.alter_column(u'gridentities_fueltype', 'description', self.gf('django.db.models.fields.CharField')(max_length=40))

    models = {
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fossil': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_renewable': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['gridentities']