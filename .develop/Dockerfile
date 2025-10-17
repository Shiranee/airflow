FROM python:3.10-alpine3.16
LABEL maintainer="crmadmin.liveoficial.ind.br"

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
COPY .develop/requirements.dev.txt /tmp/requirements.dev.txt

ENV DJANGO_PATH=/srv/app
WORKDIR $DJANGO_PATH/app

EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache supervisor && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

COPY ./app/ $DJANGO_PATH

COPY .develop/entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN chown -R django-user:django-user $DJANGO_PATH

USER django-user

ENTRYPOINT ["sh", "/entrypoint.sh"]
