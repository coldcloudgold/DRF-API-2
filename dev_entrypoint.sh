#! /bin/sh


rm -r dev_database.db REST_API_app/__pycache__/ REST_API_app/migrations/__pycache__/ REST_API_app/migrations/0001_initial.py REST_API_app/service/__pycache__/ REST_API_app/tests/__pycache__/ REST_API_project/__pycache__/


python manage.py makemigrations


python manage.py migrate


python manage.py loaddata fixtures/initial_data.json


python manage.py runserver 8080