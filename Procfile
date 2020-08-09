release : python manage.py makemigrations && python manage.py migrate
web: UPDATE_DB=true gunicorn -b 0.0.0.0:$PORT pharmadados.wsgi
