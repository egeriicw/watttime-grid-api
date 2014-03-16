web: python manage.py collectstatic --noinput; newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application
scheduler: newrelic-admin run-program celery worker -B -A watttime_grid_api -l info -E --maxtasksperchild=1000 --concurrency=2
worker: newrelic-admin run-program celery worker -A watttime_grid_api -l info -E --maxtasksperchild=1000 --concurrency=4
