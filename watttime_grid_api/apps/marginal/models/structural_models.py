from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from apps.gridentities.models import BalancingAuthority
from apps.marginal.managers import ProvenanceManager
from .algorithms import MOERAlgorithm
import logging
from datetime import datetime
import pytz


logger = logging.getLogger(__name__)


class StructuralModelSet(models.Model):
    """
    Shared attributes of a set of associated structural models,
    methods for evaluating a model,
    and validators
    """
    # balancing authority
    ba = models.ForeignKey(BalancingAuthority, null=True, blank=True)
    
    # timestamp data validity begins (in UTC) (can be present, past, or future)
    valid_after = models.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))

    # algorithm
    algorithm = models.ForeignKey(MOERAlgorithm)

    # auto timestamps for creating and updating
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # custom manager
    objects = ProvenanceManager()

    class Meta:
        get_latest_by = 'valid_after'
        app_label = 'marginal'
        unique_together = ('ba', 'valid_after', 'algorithm')

    def __str__(self):
        return '%s, %s, after %s' % (self.ba.abbrev, self.algorithm, self.valid_after)

    # @classmethod
    # def predict(self, dp, **kwargs):
    #     """
    #     Compute a prediction for a DataPoint using the best available model,
    #     or return None if no model is found.
    #     """
    #     # compute inputs
    #     inputs = self.inputs(dp, **kwargs)

    #     # get model
    #     try:
    #         model = self.best_model(dp, inputs)
    #     except ValueError as e:
    #         logger.warn(e)
    #         return None

    #     # compute output
    #     output = model.output(**kwargs)

    #     # return
    #     return output


    def models(self):
        """
        Returns a queryset of the structural models in this set.
        """
        # get related model qset
        qset = self.simplestructuralmodel_set
        return qset

    def best(self, inputs):
        """
        Model within set is determined by inputs.
        """
       # extract input value
        try:
            input_value = inputs['bin_value']
        except KeyError:
            raise ValueError("Inputs %s missing key 'bin_value'")

        # get related qset of models
        qset = self.models()

        # if no models, error
        if not qset.exists():
            raise ValueError("No models associated with set %s" % self)

        # get supremum of min value
        qset = qset.filter(min_value__lte=input_value)
        supremum = qset.aggregate(val=Max('min_value'))['val']

        # best match is most recently updated with highest min_value
        try:
            row = qset.get(min_value=supremum)
        except ObjectDoesNotExist:
            raise ValueError("No model found for set %s with value %s, all bins too high" % (self, input_value))

        # test for max val
        if row.max_value <= input_value:
            raise ValueError("No model found for set %s with value %s, best guess was %s" % (self, input_value, row))

        # should have only one value now
        return row


class BaseStructuralModel(models.Model):
    """
    Base class for parameters of and methods for evaluating a structural model:
    the beta of a linear regression,
    the associated data sources
    """
    # the beta parameter from a linear regression
    beta1 = models.FloatField()
    std_dev1 = models.FloatField(null=True, blank=True)

    # minimum value in range (greater-equal)
    min_value = models.FloatField()

    # maximum value in range (strictly less)
    max_value = models.FloatField()

    # model set
    model_set = models.ForeignKey(StructuralModelSet)
    
    class Meta:
        get_latest_by = 'model_set__valid_after'
        abstract = True
        app_label = 'marginal'
        unique_together = ('min_value', 'model_set')

    def __str__(self):
        return "%s (%.1f,%.1f) beta=%.2f" % (self.model_set, self.min_value, self.max_value, self.beta1)

    def clean(self):
        """
        Validate max value greater than min value
        """
        if self.max_value <= self.min_value:
            raise ValidationError("Max value must be less than min value")


class SimpleStructuralModel(BaseStructuralModel):
    """
    Base class for models with only beta1
    """
    pass