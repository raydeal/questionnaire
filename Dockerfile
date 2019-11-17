FROM python:3.7

ENV DJANGO_SU_NAME=super-mario
ENV DJANGO_SU_EMAIL=super-mario@snap.company
ENV DJANGO_SU_PASSWORD=Mario2admin

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements_dev.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements_dev.txt

ADD . /usr/src/app

RUN mkdir static
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python manage.py loaddata --app core questions.json
RUN python -c "import os; \
   os.environ['DJANGO_SETTINGS_MODULE'] = 'questionnaire.settings'; \
   import django; django.setup(); \
   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
   get_user_model().objects.create_superuser( \
   username='$DJANGO_SU_NAME', \
   email='$DJANGO_SU_EMAIL', \
   password='$DJANGO_SU_PASSWORD')"
