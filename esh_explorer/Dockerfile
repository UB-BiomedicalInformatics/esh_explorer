FROM python:3.9-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8888

ENTRYPOINT ["python3"]

CMD ["esh_standalone.py"]
