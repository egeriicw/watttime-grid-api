from django.db import models
from django.contrib.gis.db import models as geomodels


class BalancingAuthority(models.Model):
    """Model for a balancing authority"""
    # long name
    name = models.CharField(max_length=200)

    # short name
    abbrev = models.CharField(max_length=10, unique=True)
    
    # type of grid entity
    ISO = 'ISO'
    BA = 'BA'
    BA_TYPE_CHOICES = (
        (ISO, 'Independent System Operator (also use for RTOs or similar)'),
        (BA, 'non-ISO balancing authority'),
    )
    ba_type = models.CharField(max_length=4, choices=BA_TYPE_CHOICES)
    
    # link
    link = models.URLField(blank=True, null=True)
    
    # notes
    notes = models.TextField(default='')
        
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.abbrev)


class FuelType(models.Model):
    """Model for a generation source or fuel type"""
    # name
    name = models.SlugField(unique=True)

    # description
    description = models.CharField(max_length=200)
    
    # flags
    is_renewable = models.NullBooleanField(blank=True, null=True)
    is_fossil = models.NullBooleanField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name


class PowerPlant(geomodels.Model):
    """Model for a power plant or other point generation source"""
    # unique id code
    code = geomodels.CharField(max_length=4, unique=True)
    
    # lat-long
    coord = geomodels.PointField()
    
    # fuel type
    fuel = geomodels.ForeignKey(FuelType, null=True, blank=True)

    # geo manager
    objects = geomodels.GeoManager()
    
    def __unicode__(self):
        return '%s (%s)' % (self.code, self.coord)        
