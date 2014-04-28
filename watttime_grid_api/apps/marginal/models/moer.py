from django.db import models
from django.db.models.signals import post_save
from apps.griddata.models import DataPoint, BaseObservation
from .structural_models import StructuralModelSet
import logging


logger = logging.getLogger(__name__)


class BaseCarbon(BaseObservation):
    DEFAULT_UNITS = 'lb/MW'

    class Meta:
        app_label = 'marginal'
        abstract = False


class MOER(BaseCarbon):
    structural_model = models.ForeignKey(StructuralModelSet, null=True, blank=True)

    class Meta:
        app_label = 'marginal'

    def compute(self):
        """Compute value based on DataPoint and model"""
        inputs = self.structural_model.algorithm.bin_value(dp=self.dp)
        model = self.structural_model.best(inputs)
        return self.structural_model.algorithm.predict(dp=self.dp, model=model)

    def set(self):
        """Compute and save value"""
        self.value = self.compute()
        self.save()


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
        c, created = MOER.objects.get_or_create(dp=dp)
        c.value = sender.predict(dp)
        c.save()
#post_save.connect(reset_moer_on_model, SilerEvansModel)
