from __future__ import absolute_import
from celery import shared_task
from pyiso.tasks import get_generation
from apps.genmix.tasks import insert_generation
from apps.etl.models import ETLJob
import logging
import json
import traceback


# set up logger
logger = logging.getLogger(__name__)


@shared_task
def cmap(it, callback):
    """Apply a task to each element of a task result, in series"""
    # NOT this solution http://stackoverflow.com/questions/13271056/how-to-chain-a-celery-task-that-returns-a-list-into-a-group
    return [callback(x) for x in it]
    
@shared_task(ignore_result=True)
def log_update(res_list, job):
    # get unique datapoint ids
    dps = set(res_list)

    # save to job
    job.datapoints = dps
    job.success = True
    job.save()
    
@shared_task(ignore_result=True)
def update_generation(ba_name, **kwargs):    
    # set up job
    job = ETLJob.objects.create(task='update_generation',
                                args=json.dumps([ba_name]),
                                kwargs=json.dumps(kwargs),
                                )
    
    # set up chain
    # get and set generation
    chain = (get_generation.s(ba_name, **kwargs) | cmap.s(insert_generation) | log_update.s(job))

    # run chain
    try:
        chain()
    except Exception as e:
        # log stack trace
        msg = traceback.format_exc(e)
        logger.error('Error on job %d (%s)' % (job.id, str(job)))
        job.set_error(msg)

    # save the job
    job.save()
