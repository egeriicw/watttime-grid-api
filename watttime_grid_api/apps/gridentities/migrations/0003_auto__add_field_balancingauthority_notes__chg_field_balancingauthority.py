# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BalancingAuthority.notes'
        db.add_column(u'gridentities_balancingauthority', 'notes',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


        # Changing field 'BalancingAuthority.abbrev'
        db.alter_column(u'gridentities_balancingauthority', 'abbrev', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10))
        # Removing index on 'BalancingAuthority', fields ['abbrev']
     #   db.delete_index(u'gridentities_balancingauthority', ['abbrev'])


        # Changing field 'BalancingAuthority.name'
        db.alter_column(u'gridentities_balancingauthority', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):
        # Adding index on 'BalancingAuthority', fields ['abbrev']
      #  db.create_index(u'gridentities_balancingauthority', ['abbrev'])

        # Deleting field 'BalancingAuthority.notes'
        db.delete_column(u'gridentities_balancingauthority', 'notes')


        # Changing field 'BalancingAuthority.abbrev'
        db.alter_column(u'gridentities_balancingauthority', 'abbrev', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))

        # Changing field 'BalancingAuthority.name'
        db.alter_column(u'gridentities_balancingauthority', 'name', self.gf('django.db.models.fields.CharField')(max_length=40))

    models = {
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

    complete_apps = ['gridentities']