watttime-grid-api
=================

An API for the power grid. See the code in action at http://watttime-grid-api.herokuapp.com/api/v1!


Quickstart dev environment
-----------
After cloning and starting a virtual environment:

      ./manage.py syncdb
      ./manage.py migrate
      ./manage.py test
      ./manage.py loaddata isos gentypes fuelcarbonintensities
      ./manage.py runserver

To run tasks with celery, run <code>rabbitmq-server &</code> in one terminal window, and <code>celery -A watttime_grid_api worker -l info</code> in another.
