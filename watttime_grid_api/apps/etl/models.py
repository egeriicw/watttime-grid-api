from django.db import models
from apps.griddata.models import DataPoint
from django.core.mail import mail_admins


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

    class Meta:
        get_latest_by = 'updated_at'

    def __str__(self):
        return ' '.join([self.task, self.args, self.kwargs, str(self.created_at)])

    def set_error(self, msg):
        """Register error message and send email"""
        # set error
        self.errors = msg
        self.save()

        # send email
        mail_admins('Error on job %d (%s)' % (self.id, str(self)), msg)
