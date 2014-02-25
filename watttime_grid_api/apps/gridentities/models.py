from django.db import models


class BalancingAuthority(models.Model):
    """Model for a balancing authority"""
    # long name
    name = models.CharField(max_length=40)

    # short name
    abbrev = models.SlugField(unique=True)
    
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
