from __future__ import absolute_import
from celery import shared_task
from pyiso.tasks import get_generation
from apps.genmix.tasks import insert_generation
import logging

# set up logger
logger = logging.getLogger(__name__)


@shared_task
def cmap(it, callback):
    """Apply a task to each element of a task result, in series"""
    # NOT this solution http://stackoverflow.com/questions/13271056/how-to-chain-a-celery-task-that-returns-a-list-into-a-group
    return [callback(x) for x in it]
    
@shared_task(ignore_result=True)
def log_update(res_list, ba_name):
    n_new_gen = sum([x[0] for x in res_list])
    n_new_dp = sum([x[1] for x in res_list])
    logger.info('%s: Created %d new generations at %d new datapoints' % (ba_name, n_new_gen, n_new_dp))
    
@shared_task(ignore_result=True)
def update_generation(ba_name, **kwargs):    
    # pre-log
    logger.info('%s: Getting data with args %s' % (ba_name, kwargs))
    
    # run chain
    chain = (get_generation.s(ba_name, **kwargs) | cmap.s(insert_generation) | log_update.s(ba_name))
    chain()
