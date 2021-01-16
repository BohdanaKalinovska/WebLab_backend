# FROM python:3.8

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# #MAINTAINER Bohdana Kalinovska <winter06012001@gmail.com>

# WORKDIR /urs/src/django-lab4
# COPY ./requirements.txt /urs/src/requirements.txt
# #Run ["pip", "install", "--upgrade pip"]

FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
