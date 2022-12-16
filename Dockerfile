FROM python:3.10-slim-buster

RUN apt update --no-install-recommends -y

RUN mkdir /app
COPY . /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python3", "main.py"]