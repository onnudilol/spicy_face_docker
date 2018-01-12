FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD ./source /code/

RUN pip install pipenv
RUN pipenv install --system
