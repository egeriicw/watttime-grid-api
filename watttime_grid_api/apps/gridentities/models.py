from django.db import models

class GridEntity(models.Model):
    """Model for a player on the grid"""
    ISO = 'ISO'
    BA = 'BA'
    GEN = 'GEN'
    ENTITY_TYPE_CHOICES = (
        (ISO, 'Independent System Operator (also use for RTOs or similar)'),
        (BA, 'non-ISO balancing authority'),
        (GEN, 'generator')
    )
    entity_type = models.CharField(max_length=8, choices=ENTITY_TYPE_CHOICES)
    
    name = models.CharField(max_length=40)
    