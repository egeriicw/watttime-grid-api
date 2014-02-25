# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BalancingAuthority'
        db.create_table(u'gridentities_balancingauthority', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('abbrev', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('ba_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'gridentities', ['BalancingAuthority'])

        # Adding model 'FuelType'
        db.create_table(u'gridentities_fueltype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'gridentities', ['FuelType'])


    def backwards(self, orm):
        # Deleting model 'BalancingAuthority'
        db.delete_table(u'gridentities_balancingauthority')

        # Deleting model 'FuelType'
        db.delete_table(u'gridentities_fueltype')


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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['gridentities']