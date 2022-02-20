FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get upgrade -y && apt-get install postgresql postgresql-contrib -y
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . /app