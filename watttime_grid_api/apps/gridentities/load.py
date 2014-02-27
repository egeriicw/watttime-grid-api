import os
from django.contrib.gis.utils import LayerMapping
from models import PowerPlant

# See https://docs.djangoproject.com/en/1.6/ref/contrib/gis/tutorial/#layermapping
# ./manage.py ogrinspect watttime_grid_api/apps/gridentities/fixtures/powerplants/points2.shp PowerPlant --mapping
powerplant_mapping = {
    'code' : 'NAME',
    'coord' : 'POINT',
}

pp_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      'fixtures/powerplants/points2.shp'))

def run(verbose=True):
    lm = LayerMapping(PowerPlant, pp_shp, powerplant_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose, fid_range=(0,1324))
