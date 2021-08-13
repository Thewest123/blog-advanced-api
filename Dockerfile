# Pull official base image
FROM python:3.7-alpine
LABEL maintainer="Jan Černý"

# Set Envinronment variables
ENV PYTHONUNBUFFERED 1

# Install Postgres client
RUN apk add --update --no-cache postgresql-client

# Install Geospatial libraries for GeoDjango
RUN apk add --update --no-cache proj geos gdal binutils

# Install temporary build dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc musl-dev libc-dev linux-headers postgresql-dev

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Remove temporary build dependencies
RUN apk del .tmp-build-deps

# Make directory for the Django App
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Make directories for the Django App static and media files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Limit the scope of the user who runs the docker image
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user