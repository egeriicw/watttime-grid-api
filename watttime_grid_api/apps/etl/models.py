from django.db import models
from apps.griddata.models import DataPoint


class ETLJob(models.Model):
   # auto timestamps for creating and updating
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # task name
    task = models.CharField(max_length=100, default='')

    # arguments task was called with
    args = models.TextField(default='')
    kwargs = models.TextField(default='')

    # datapoints touched
    datapoints = models.ManyToManyField(DataPoint)

    # error log
    errors = models.TextField(default='')

    # finished successfully
    success = models.BooleanField(default=False)
