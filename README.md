watttime-grid-api
=================

What kind of electricity are you getting right now? The WattTime grid API collects real-time information on the current generation fuel mix from the major American electricity markets (MISO, PJM, CAISO, ERCOT, ISONE, SPP, and BPA) using the [pyiso](https://github.com/WattTime/pyiso) library and displays it in a convenient standardized format. The API also calculates a real-time carbon footprint of electricity use in a given place and time based on this fuel mix. See the code in action at http://api.watttime.org/!

What's included
---------------
All the Django apps are in `watttime_grid_api/apps`. These are
* `gridentities`: provides models for metadata and descriptions of geographic entities (`BalancingAuthority` and `PowerPlant`) and data types (`FuelType`); standalone
* `griddata`: provides models for time series data (`DataPoint`); depends on `gridentities`
* `supply_demand`: provides `Generation`, `Load`, and `TieFlow` models that associates generation and load observations to `DataPoint`s, and management commands and celery tasks for pulling the data; depends on `gridentities` and `griddata`
* `carbon`: provides `Carbon` and `FuelCarbonIntensity` models that associate carbon intensity observations to `DataPoint`s, and tasks for calculating the data; depends on `gridentities`, `griddata`, and `supply_demand`
* `marginal`: provides `MOER`, `MOERAlgorithm`, and `StructuralModelSet` models that associate marginal carbon intensity observations (MOER) to `DataPoint`s, and tasks for calculating the data; depends on `gridentities`, `griddata`, and `supply_demand`
* `api`: implements a Django REST Framework API to all other apps; depends on `gridentities`, `griddata`, `supply_demand`, `carbon`, and `marginal`
* `etl`: implements a extract-transform-load job flow to supply data to all other apps; depends on `gridentities`, `griddata`, `supply_demand`, `carbon`, and `marginal`


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
<code>celery -A watttime_grid_api worker -B -l info</code>
or
<code>foreman start</code> (if you have <code>newrelic-admin</code> installed locally).
