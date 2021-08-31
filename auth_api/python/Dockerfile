FROM python:3-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

EXPOSE 8000
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

COPY . /app

CMD [ "python",  "api.py", "--host=0.0.0.0:8000"]