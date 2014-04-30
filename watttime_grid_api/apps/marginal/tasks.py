from __future__ import absolute_import
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from apps.griddata.models import DataPoint
from apps.marginal.models import StructuralModelSet
import logging

# set up logger
logger = logging.getLogger(__name__)

@shared_task
def set_moers(dp_pks, alg_name):
	"""Set MOER for each data point id in iterable, using named algorithm"""
	# set up storage
	result = []
	for dp_pk in dp_pks:
		# get dp
		dp = DataPoint.objects.get(pk=dp_pk)

		# get model set
		sset = StructuralModelSet.objects.all().best(dp, alg_name)

		# get or create MOER
		try:
			moer = sset.moer_set.get(dp=dp)
			result.append(False)
		except ObjectDoesNotExist:
			moer = sset.moer_set.create(dp=dp)
			result.append(True)

		# set value
		moer.set()

	# return
	return result
