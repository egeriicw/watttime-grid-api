from django.db import models
from apps.griddata.models import DataPoint
from django.core.mail import mail_admins
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.html import format_html


#adapted from https://djangosnippets.org/snippets/2657/
def get_admin_url(obj):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    url = reverse(
      "admin:%s_%s_change" % (content_type.app_label, content_type.model), 
      args=[obj.pk])
    link = format_html('<a href="%s">%d (%s)</a>' % (url, obj.pk, str(obj)))
    return link


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

    def datapoints_admin_links(self):
        """Links to admin pages for datapoints"""
        return [get_admin_url(dp) for dp in self.datapoints.all()]
    datapoints_admin_links.allow_tags = True

    def gen_admin_links(self):
        """Links to admin pages for generations"""
        return [get_admin_url(v) for dp in self.datapoints.all() for v in dp.genmix.all()]
    gen_admin_links.allow_tags = True

    def carbon_admin_links(self):
        """Links to admin pages for carbons"""
        return [get_admin_url(dp.carbon) for dp in self.datapoints.all() if hasattr(dp, 'carbon')]
    carbon_admin_links.allow_tags = True

    def moer_admin_links(self):
        """Links to admin pages for MOERs"""
        return [get_admin_url(v) for dp in self.datapoints.all() for v in dp.moer_set.all()]
    moer_admin_links.allow_tags = True
