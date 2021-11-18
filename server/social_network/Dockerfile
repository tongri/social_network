FROM python:3.8.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN /usr/local/bin/python -m pip install --upgrade pip

ADD ../requirements.txt ./requirements.txt

RUN pip install psycopg2
RUN pip install psycopg2-binary

RUN pip install -r requirements.txt
