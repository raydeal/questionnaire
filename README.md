# questionnaire
Simple questionnaire

## Installation and running with Docker
Before starting, [install Compose](https://docs.docker.com/compose/install/).
To get the containers running, build the images and then start the services:
```shell
docker-compose up --build -d
```
Now you in your browser the servis is available as URL: localhost:8000/

To stop docker service:
```shell
docker-compose stop web
```

To start docker service again:
```shell
docker-compose start web
```

To stop service and/or to remove image:
```shell
docker-compose down
```

To run test:
```shell
docker-compose run web python manage.py test
```

## Installation and running without Docker
Requirements:
* Python 3

Run commands:
```shell
pip install -r requirements_dev.txt
mkdir db
python manage.py migrate
python manage.py loaddata --app core questions.json
```
To create super user run:
```shell
python manage.py createsuperuser --username super-mario --email super-mario@snap.company
```

Run server:
```shell
python manage.py runserver --insecure
```

Now you in your browser the servis is available as URL: localhost:8000/

To run tests:
```shell
python manage.py test tests
```