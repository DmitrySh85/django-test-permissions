FROM python:3.10

SHELL ["/bin/bash", "-c"]

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev\
    libpq-dev gettext cron openssh-client locales vim

RUN useradd -rms /bin/bash dev && chmod 777 /opt /run

WORKDIR /permissions

RUN chown -R dev:dev /permissions && chmod 755 /permissions

COPY --chown=dev:dev . .

RUN pip install -r requirements.txt

USER dev

CMD ["sh", "-c", "python3 manage.py runserver"]