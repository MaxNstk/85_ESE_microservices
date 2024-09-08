FROM python:3.12
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN chown root -R /code

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
COPY ./app ./app
COPY ./.env ./.env
COPY ./manage.py ./manage.py

RUN pip install -r requirements.txt