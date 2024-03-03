#!/bin/sh

# Apply database migrations
echo "Making migrations"
python manage.py makemigrations

echo "Applying migrations"
python manage.py migrate

python manage.py runserver 0.0.0.0:5432