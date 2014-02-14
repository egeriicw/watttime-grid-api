from django.db import models

class BalancingAuthority(models.Model):
    """Model for a balancing authority"""
    # long name
    name = models.CharField(max_length=40)

    # short name
    abbrev = models.CharField(max_length=8)
    
    # type of grid entity
    ISO = 'ISO'
    BA = 'BA'
    BA_TYPE_CHOICES = (
        (ISO, 'Independent System Operator (also use for RTOs or similar)'),
        (BA, 'non-ISO balancing authority'),
    )
    ba_type = models.CharField(max_length=8, choices=BA_TYPE_CHOICES)
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.abbrev)
        
