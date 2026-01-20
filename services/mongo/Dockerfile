FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

RUN pip install fastapi[standard]

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
EXPOSE 80

CMD ["fastapi", "run", "/code/app/main.py", "--host", "0.0.0.0", "--port", "80"]