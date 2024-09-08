FROM python:3.12
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN chown root -R /code

RUN pip install --upgrade pip

RUN mkdir -p uploads

COPY ./requirements.txt ./requirements.txt
COPY ./app ./app

RUN pip install -r requirements.txt
ENTRYPOINT [ "uvicorn", "app.main:app" ] 