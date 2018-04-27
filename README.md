# flask_rep

# create database "flask_test"

# create env variables for APP and DATABASE
```
$ export FLASK_APP=app.py
$ export DATABASE_URL="postgresql://serg:1789@localhost:5432/flask_server"
```

# apply initial migrations
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

#run flask
```
flask run
```