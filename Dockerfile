FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
ENV DJANGO_LOG_LEVEL DEBUG

COPY app/requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

COPY app/ /app/

#CMD ./manage.py runserver 0.0.0.0:5000
