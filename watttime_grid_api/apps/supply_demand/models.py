from django.db import models
from apps.griddata.models import BaseObservation, BaseUnboundObservation, DataPoint
import logging


logger = logging.getLogger(__name__)


class Load(BaseObservation):
    DEFAULT_UNITS = 'MW'


class TieFlow(BaseUnboundObservation):
    # source data point
    dp_source = models.ForeignKey(DataPoint, related_name='outflow')

    # destination data point
    dp_dest = models.ForeignKey(DataPoint, related_name='inflow')

    DEFAULT_UNITS = 'MW'
