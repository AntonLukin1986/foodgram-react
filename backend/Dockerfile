FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]

CMD ["python3", "manage.py", "runserver", "0:8000"]

ENV DB_HOST database
ENV DB_PORT 5432

LABEL author='shahter1986@yandex.ru' version=1 broken_keyboards=7
