from django.test import TestCase
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.marginal.models import StructuralModelSet, MOERAlgorithm
from apps.marginal import tasks
from datetime import datetime
import pytz


class TestSetTask(TestCase):
    fixtures = ['isos', 'gentypes']

    def setUp(self):
        # data point
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=100)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=200)

        # structural model
        self.alg = MOERAlgorithm.objects.create(binner=MOERAlgorithm.TOTAL_GEN,
                                                predictor=MOERAlgorithm.BETA,
                                                name=MOERAlgorithm.SILEREVANS_GEN)
        self.sset = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.alg)
        self.sset.models().create(beta1=1, min_value=1, max_value=400)

    def test_set_one(self):
    	# input is a list of dp ids
    	inputs = [self.dp.pk]
    	result = tasks.set_moers(inputs, self.alg.name)

    	# output is a list of booleans for MOER created
    	self.assertEqual(len(result), len(inputs))

    	# MOER should be created
    	self.assertEqual(result, [True])

    def test_set_dup(self):
    	# input is a list of dp ids
    	inputs = [self.dp.pk for i in range(2)]
    	result = tasks.set_moers(inputs, self.alg.name)

    	# output is a list of booleans for MOER created
    	self.assertEqual(len(result), len(inputs))

    	# MOER should only be created first time
    	self.assertEqual(result, [True, False])
