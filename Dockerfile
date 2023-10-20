FROM python:3.11

WORKDIR /project

COPY ./requirements.txt ./requirements.dev.txt /project/

RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt -r /project/requirements.dev.txt

COPY ./app /project/app
COPY ./tests /project/tests

CMD ["uvicorn", "app.main:web", "--host", "0.0.0.0", "--port", "8080"]
