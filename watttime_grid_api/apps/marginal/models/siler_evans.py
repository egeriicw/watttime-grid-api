from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from apps.griddata.models import DataPoint
from apps.genmix.models import Generation
from .base import SimpleStructuralModel, BaseCarbon
import logging


logger = logging.getLogger(__name__)


class SilerEvansModel(SimpleStructuralModel):
    """
    Replicating Siler-Evans et al, Environ Sci Technol 2012.
    http://pubs.acs.org/doi/abs/10.1021/es300145v
    TODO: should be load not gen
    """
    @classmethod
    def inputs(self, dp, **kwargs):
        """Input value is total generation"""
        return dp.genmix.all().aggregate(bin_value=Sum('gen_MW'))


class SilerEvansMOER(BaseCarbon):
    DEFAULT_UNITS = 'lb/MW'

    structural_model = models.ForeignKey(SilerEvansModel, null=True, blank=True)

    class Meta:
        app_label = 'marginal'


# every time a Generation model is saved, update its related MOER value
def reset_moer_on_gen(sender, instance, **kwargs):
    # add carbon to data point
    dp = instance.mix
    c, created = SilerEvansMOER.objects.get_or_create(dp=dp)
    # set value for carbon
    c.value = SilerEvansModel.predict(dp)
    # save
    c.save()
post_save.connect(reset_moer_on_gen, Generation)


# every time a structural model is saved, update its related MOER value
def reset_moer_on_model(sender, instance, **kwargs):
    # get affected data points
    dps = DataPoint.objects.filter(timestamp__gt=instance.valid_after)
    
    # filter by balancing authority, if any
    if instance.ba:
        dps = dps.filter(ba=instance.ba)
        
    # filter by later valid model
    try:
        next_instance = instance.get_next_by_valid_after()
        dps = dps.filter(timestamp__lte=next_instance.valid_after)
    except sender.DoesNotExist:
        pass

    # reset carbon on each point
    for dp in dps:
        c, created = SilerEvansMOER.objects.get_or_create(dp=dp)
        c.value = sender.predict(dp)
        c.save()
post_save.connect(reset_moer_on_model, SilerEvansModel)
