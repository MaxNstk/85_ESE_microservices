FROM python:3.12
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN chown root -R /code

RUN pip install --upgrade pip

COPY ./requirements.txt ./
COPY ./app ./
COPY ./manage.py ./

RUN pip install -r requirements.txt
#RUN python manage.py migrate

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]