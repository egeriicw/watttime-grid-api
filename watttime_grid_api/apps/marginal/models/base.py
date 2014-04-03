from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import BaseObservation
import logging
from datetime import datetime
import pytz


logger = logging.getLogger(__name__)


class BaseStructuralModel(models.Model):
    """
    Base class for parameters of and methods for evaluating a structural model:
    the beta of a linear regression,
    the associated data sources
    """
    # the beta parameter from a linear regression
    beta1 = models.FloatField()
    std_dev1 = models.FloatField(null=True, blank=True)

    # balancing authority
    ba = models.ForeignKey(BalancingAuthority, null=True, blank=True)
    
    # timestamp data validity begins (in UTC) (can be present, past, or future)
    valid_after = models.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))

    # minimum value in range (greater-equal)
    min_value = models.FloatField()

    # maximum value in range (strictly less)
    max_value = models.FloatField()
    
    class Meta:
        get_latest_by = 'valid_after'
        abstract = True
        app_label = 'marginal'

    def __str__(self):
        return "%s (%.1f,%.1f) beta=%.2f" % (self.ba.abbrev, self.min_value, self.max_value, self.beta1)

    def clean(self):
        """
        Validate max value greater than min value
        """
        if self.max_value <= self.min_value:
            raise ValidationError("Max value must be less than min value")

    @classmethod
    def predict(self, dp, **kwargs):
        """
        Compute a prediction for a DataPoint using the best available model,
        or return None if no model is found.
        """
        # compute inputs
        inputs = self.inputs(dp, **kwargs)

        # get model
        try:
            model = self.best_model(dp, inputs)
        except ValueError as e:
            logger.warn(e)
            return None

        # compute output
        output = model.output(**kwargs)

        # return
        return output

    @classmethod
    def best_model(self, dp, inputs):
        """
        Model is determined by balancing authority and input values.
        """
        # extract input value
        try:
            input_value = inputs['bin_value']
        except KeyError:
            raise ValueError("Inputs %s missing key 'bin_value'")

        # filter for balancing authority
        qset = self.objects.filter(ba=dp.ba)
        if not qset.exists():
            raise ValueError("No model found for dp %s, nothing matches for ba %s" % (dp, dp.ba.abbrev))

        # filter for valid_after
        qset = qset.filter(valid_after__lte=dp.timestamp)
        if not qset.exists():
            raise ValueError("No model found for dp %s valid after timestamp" % (dp))

        # get best for min value (supremum by min_value)
        qset = qset.filter(min_value__lte=input_value)
        row = qset.order_by('min_value').last()
        if row is None:
            raise ValueError("No model found for dp %s with value %s, all bins too high" % (dp, input_value))

        # test for max val
        if row.max_value <= input_value:
            raise ValueError("No model found for dp %s with value %s, best guess was %s" % (dp, input_value, row))

        # should have only one value now
        return row

    @classmethod
    def inputs(self, dp, **kwargs):
        raise NotImplementedError("Must implement inputs on derived classes")

    def output(self, **kwargs):
        raise NotImplementedError("Must implement output on derived classes")


class SimpleStructuralModel(BaseStructuralModel):
    """
    Base class for models where the prediction result = beta
    """
    def output(self, **kwargs):
        """Output value is beta"""
        return self.beta1

    class Meta(BaseStructuralModel.Meta):
        unique_together = ('ba', 'min_value', 'max_value', 'valid_after')


class BaseCarbon(BaseObservation):
    DEFAULT_UNITS = 'lb/MW'

    class Meta:
        app_label = 'marginal'
        abstract = False

