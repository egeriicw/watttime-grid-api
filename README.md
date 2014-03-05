watttime-grid-api
=================

An API for the power grid. See the code in action at http://watttime-grid-api.herokuapp.com/api/v1!


Quickstart dev environment
-----------
Start a postgres server (eg http://postgresapp.com/) and create a database called <code>mydbname</code>.
You'll also need libmemcached:

       brew install libmemcached

Also install the GeoDjango requirements. See the platform-specific instructions at 
https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/,
I used homebrew:

       brew install postgresql
       brew install postgis
       brew install libgeoip
       psql mydbname
       # CREATE EXTENSION postgis;

Clone this repo and install the requirements:

      cd watttime-grid-api
      mkvirtualenv watttime-grid-api
      pip install -r reqs/dev.txt

Set up the environment variables. You can put then in a <code>.env</code> file and use foreman
(get it at https://github.com/ddollar/foreman or as part of the Heroku CLI)
or put them in your bash profile or whatever.
If you're not using foreman, remove the 'foreman run' from all following commands.

      echo DATABASE_URL=postgres://localhost/mydbname > .env

Create database tables for the models (create user when prompted):

      foreman run ./manage.py syncdb
      foreman run ./manage.py migrate

Test the site:

      foreman run ./manage.py test
      foreman run ./manage.py loaddata isos gentypes fuelcarbonintensities griddata
      foreman run ./manage.py shell
      >>> from apps.gridentities import load
      >>> load.run_balancing_authority()
      foreman run ./manage.py runserver

To run tasks with celery, run <code>rabbitmq-server &</code>, then
<code>celery -A watttime_grid_api worker -l info</code>
or
<code>foreman start</code> (if you have <code>newrelic-admin</code> installed locally).
