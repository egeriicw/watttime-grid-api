from django.db import models
from django.db.models import Sum

##################
# biner utils
##################

def total_gen(dp):
    """total generation"""
    return dp.genmix.all().aggregate(bin_value=Sum('gen_MW'))


##################
# predictor utils
##################

def beta1(model):
    """prediction is simply beta"""
    return model.beta1


class MOERAlgorithm(models.Model):
    """
    Model for algorithms that predict marginal carbon emissions
    """
    # Replicating Siler-Evans et al, Environ Sci Technol 2012.
    # http://pubs.acs.org/doi/abs/10.1021/es300145v
    SILEREVANS = 0
    SILEREVANS_GEN = 1

    NAME_CHOICES = (
        (SILEREVANS, 'Siler-Evans'),
        (SILEREVANS_GEN, 'Siler-Evans binned by gen'),
    )

    # algorithm name
    name = models.CharField(max_length=50, unique=True,
                            choices=NAME_CHOICES)

    # algorithm description
    description = models.TextField(default='')

    # binning method
    TOTAL_LOAD = 0
    TOTAL_GEN = 1
    BINNER_CHOICES = (
        (TOTAL_LOAD, 'total load'),
        (TOTAL_GEN, 'total generation'),
    )
    binner = models.CharField(max_length=50, unique=True,
                              choices=BINNER_CHOICES)

    # predictor method
    BETA = 0
    PREDICTOR_CHOICES = (
        (BETA, 'simple'),
    )
    predictor = models.CharField(max_length=50, unique=True,
                                 choices=PREDICTOR_CHOICES)

    class Meta:
        unique_together = ('binner', 'predictor')

    def __str__(self):
        """Descriptive name"""
        return dict(self.NAME_CHOICES)[self.name]

    def bin_value(self, **kwargs):
        """Get the binning parameter"""
        if self.binner == self.TOTAL_GEN:
            # check args
            try:
                dp = kwargs['dp']
            except KeyError:
                raise ValueError('%s bin_value requires a dp kwarg' % self.binner)

            # return
            # TODO: should be load not gen
            return total_gen(dp)

        else:
            raise NotImplementedError("bin_value not implemented for %s" % self.binner)

    def prediction_result(self, **kwargs):
        """Marginal carbon emissions value"""
        if self.predictor == self.BETA:
            # check args
            try:
                model = kwargs['model']
            except KeyError:
                raise ValueError('%s prediction_result requires a model kwarg' % self.predictor)

            # return
            return beta1(model)

        else:
            raise NotImplementedError("prediction_result not implemented for %s" % self.predictor)

    def predict(self, dp=None, model=None):
        """Predict marginal carbon emissions for inputs"""
        if model is None:
            # get best model set
            modelset = self.structuralmodelset_set.best(dp)

            # get best model based on bin value
            bin_val = self.bin_value(dp=dp)
            model = modelset.best(bin_val)

        # return prediction
        return self.prediction_result(model=model)
