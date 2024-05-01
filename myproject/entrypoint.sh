#!/bin/sh

# Apply database migrations
echo "Making migrations"
python manage.py makemigrations

echo "Applying migrations"
python manage.py migrate
python manage.py make_users

echo "Assigning superuser status to users with user type 1"
python manage.py assign_superuser

python manage.py runserver 0.0.0.0:8000