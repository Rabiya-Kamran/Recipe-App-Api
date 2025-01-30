#base image, efficient image, alpine reduces image size
FROM python:3.9-alpine3.13 

#whoever is maitaining this dockerimage (no delay) 
LABEL maintainer=""

#print out directly on console without buffering 
ENV PYTHONBUFFERED 1

#copying from host mahine to the container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

#Sets the working directory inside the container to /app
WORKDIR /app
#port
EXPOSE 8000

ARG DEV=false
#running theses commands make code running more efficient
RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV=  "true "]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Modifies the system's PATH environment variable to include a custom directory, /py/bin with executables or binaries .
# full path of our virtual env
ENV PATH="/py/bin:$PATH"

#no need of any root previlges for anything as user is django-user
USER django-user