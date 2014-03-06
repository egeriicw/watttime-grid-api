from django.db import models
from apps.griddata.models import DataPoint
from datetime import timedelta
import pytz


#class QCFlag(models.Model):
#    """Model for storing results of quality control checks"""
#    # error code
#    code = models.CharField(max_length=4, unique=True)
#    
#    # error description
#    description = models.CharField(max_length=200)
#    
#    def __unicode__(self):
#        return '%s: %s' % (self.code, self.description)
#        
#
#class QC(models.Model):
#    """Model for storing results of quality control checks"""
#    # timestamp for qc flag creation
#    created_at = models.DateTimeField(auto_now_add=True)
#    # timestamp for qc flag resolution    
#    resolved_at = models.DateTimeField(null=True, blank=True)
#
#    # every error must be associated with a DataPoint
#    dp_flagged = models.ForeignKey(DataPoint)
#    
#    # error code
#    flag = models.ForeignKey(QCFlag)
    
    
    
    
### notes
# test for too few generations
DataPoint.objects.annotate(num_genmix=models.Count('genmix')).filter(num_genmix__lt=2)
        
# test for timestamp later than creation (for non forecast data)
DataPoint.objects.filter(quality='PAST', timestamp__gt=models.F('created_at'))

# test for missing carbon
DataPoint.objects.filter(carbon__emissions_intensity=None)
DataPoint.objects.filter(carbon__emissions_intensity__lte=0)

# test for stale data, high freq
DataPoint.objects.filter(quality='PAST', freq='10m', ba__abbrev='CAISO',
                         timestamp__lt=models.F('created_at')-timedelta(minutes=2))                         
DataPoint.objects.filter(quality='PAST', freq='5m', ba__abbrev='MISO',
                         timestamp__lt=models.F('created_at')-timedelta(minutes=2))
DataPoint.objects.filter(quality='PAST', freq='5m', ba__abbrev='BPA',
                         timestamp__lt=models.F('created_at')-timedelta(minutes=2))
DataPoint.objects.filter(quality='PAST', freq='5m', ba__abbrev='PJM',
                         timestamp__lt=models.F('created_at')-timedelta(minutes=5))

# test for stale data, low freq
DataPoint.objects.filter(quality='PAST', ba__abbrev='ERCOT',
                         timestamp__lt=models.F('created_at')-timedelta(minutes=94))

# test for yesterday's data collected at right time
DataPoint.objects.filter(ba__abbrev='CAISO', market='RTHR').latest().timestamp.astimezone(pytz.timezone('US/Pacific')).hour == 23
DataPoint.objects.filter(ba__abbrev='CAISO', market='RTHR').latest().timestamp.astimezone(pytz.timezone('America/Chicago')).hour == 23
