watttime-grid-api
=================

An API for the power grid. See the code in action at http://watttime-grid-api.herokuapp.com/api/v1!


Quickstart dev environment
-----------
Clone this, then install the requirements:

      mkvirtualenv watttime-grid-api
      pip install -r reqs/dev.txt

Set up the environment variables. You can use foreman
(get it at https://github.com/ddollar/foreman or as part of the Heroku CLI)
or put them in your bash profile or whatever.
If you're not using foreman, remove the 'foreman run' from all following commands.

      echo DATABASE_URL=postgres://localhost/mydbname > .env

Set up the database by starting a postgres server (eg http://postgresapp.com/), then:

      foreman run ./manage.py syncdb
      foreman run ./manage.py migrate

Test the site:

      foreman run ./manage.py test
      foreman run ./manage.py loaddata isos gentypes fuelcarbonintensities griddata
      foreman run ./manage.py runserver

To run tasks with celery, run <code>rabbitmq-server &</code>, then
<code>celery -A watttime_grid_api worker -l info</code>
or
<code>foreman start</code> (if you have <code>newrelic-admin</code> installed locally).
