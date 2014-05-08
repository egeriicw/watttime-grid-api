# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('supply_demand', '0002_auto__add_generation__add_unique_generation_fuel_mix'),
    )

    def forwards(self, orm):
        pass
        # # Removing unique constraint on 'Generation', fields ['fuel', 'mix']
        # db.delete_unique(u'genmix_generation', ['fuel_id', 'mix_id'])

        # # Deleting model 'Generation'
        # db.delete_table(u'genmix_generation')


    def backwards(self, orm):
        pass
        # # Adding model 'Generation'
        # db.create_table(u'genmix_generation', (
        #     ('fuel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridentities.FuelType'])),
        #     ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='genmix', to=orm['griddata.DataPoint'])),
        #     (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        #     ('gen_MW', self.gf('django.db.models.fields.FloatField')()),
        # ))
        # db.send_create_signal(u'genmix', ['Generation'])

        # # Adding unique constraint on 'Generation', fields ['fuel', 'mix']
        # db.create_unique(u'genmix_generation', ['fuel_id', 'mix_id'])


    models = {
        
    }

    complete_apps = ['genmix']