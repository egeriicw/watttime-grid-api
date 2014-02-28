import os
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource, geometries
from django.contrib.gis import geos
from models import PowerPlant, BalancingAuthority, ServiceArea

# See https://docs.djangoproject.com/en/1.6/ref/contrib/gis/tutorial/#layermapping
# and https://docs.djangoproject.com/en/1.6/ref/contrib/gis/tutorial/#importing-spatial-data

# ./manage.py ogrinspect watttime_grid_api/apps/gridentities/fixtures/powerplants/points2.shp PowerPlant --mapping
powerplant_mapping = {
    'code' : 'NAME',
    'coord' : 'POINT',
}

balancingauthority_mapping = {
    'name' : 'BAL_AUTH',
    'area_sq_mi' : 'AREA_SQ_MI',
    'bal_auth_id' : 'BAL_AUTHID',
    'rec_id' : 'REC_ID',
}
ba_abbrev_mapping = {
    'CISO': 'CAISO',
    'ERCO': 'ERCOT',
    'NYIS': 'NYISO',
    'ISNE': 'ISONE',
    'BPAT': 'BPA',
}

pp_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      'fixtures/powerplants/points2.shp'))
ba_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      'fixtures/balancing_authorities/ctl_area_region.shp'))

def run_power_plant(verbose=True):
    lm = LayerMapping(PowerPlant, pp_shp, powerplant_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose, fid_range=(0,1324))


def run_balancing_authority():
    ds = DataSource(ba_shp)
    lyr = ds[0]
    for ba in lyr:
        # use the preferred abbrev list
        try:
            abbrev = ba_abbrev_mapping[ba.get('BA_ABBREV')]
        except KeyError:
            abbrev = ba.get('BA_ABBREV')
            
        # create service area
        if isinstance(ba.geom, geometries.MultiPolygon):
            sa = ServiceArea.objects.create(geom=ba.geom.wkt)
        else:
            # awkwardly coerce into MultiPolygon
            # see http://gis.stackexchange.com/questions/13498/can-polygons-be-generalized-to-multipolygons-in-geodjango
            mp = geos.MultiPolygon(geos.fromstr(str(ba.geom)))
            sa = ServiceArea.objects.create(geom=mp)
            
        # create or update BA
        defaults = {k: ba.get(v) for k, v in balancingauthority_mapping.iteritems()}
        defaults['service_area'] = sa
        ba_db, created = BalancingAuthority.objects.get_or_create(abbrev=abbrev,
                                                                  defaults=defaults)
        if not ba_db.ba_type:
            ba_db.ba_type = 'BA'
            ba_db.save()
            