FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY devopsproject /app
COPY requirements.txt /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

RUN pip install -r requirements.txt

EXPOSE 8000/tcp

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]