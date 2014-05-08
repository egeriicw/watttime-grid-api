from __future__ import absolute_import
from celery import shared_task, group
from pyiso.tasks import get_generation
from apps.supply_demand.tasks import insert_generation
from apps.carbon.tasks import set_average_carbons
from apps.marginal.tasks import set_moers
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
    
@shared_task
def log_load(res_list, job):
    # get unique datapoint ids
    dps = set(res_list)

    # save to job
    job.datapoints = dps
    job.save()

    # return job
    return dps

def run_chain(chain, job):
    """Run a chain of tasks and log the result to job"""
    # run chain
    try:
        chain()
        job.success = True
    except Exception as e:
        # log stack trace
        msg = traceback.format_exc(e)
        logger.error('Error on job %d (%s)' % (job.id, str(job)))
        job.set_error(msg)

    # return
    return job
    
@shared_task(ignore_result=True)
def update_generation(ba_name, **kwargs):    
    # set up job
    job = ETLJob.objects.create(task='update_generation',
                                args=json.dumps([ba_name]),
                                kwargs=json.dumps(kwargs),
                                )
    
    # set up transformations
    # these tasks will run in parallel, so make sure they're independent!
    transformations = []
    if kwargs.get('set_average_carbon', True):
        # set average carbon by default
        transformations.append(set_average_carbons.s())
    moer_alg_name = kwargs.get('moer_alg_name', None)
    if moer_alg_name == '1':
        # set MOER only if alg name given
        transformations.append(set_moers.s(moer_alg_name))

    # set up ETL chain
    extract = get_generation.s(ba_name, **kwargs)
    load = cmap.s(insert_generation) | log_load.s(job)
    transform = group(transformations)
    chain = (extract | load | transform)

    # run chain
    try:
        chain()
        job.success = True
    except Exception as e:
        # log stack trace
        msg = traceback.format_exc(e)
        logger.error('Error on job %d (%s)' % (job.id, str(job)))
        job.set_error(msg)

    # save the job
    job.save()
