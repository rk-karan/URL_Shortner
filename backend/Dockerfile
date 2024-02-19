FROM python:3.9.6

WORKDIR /src

COPY ./src/requirements.txt .

RUN pip3 install -r requirements.txt
# RUN pip3 install -r requirements.txt

COPY ./src/. .

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "--timeout", "2400", "uvicorn.workers.UvicornWorker", "application:app"]
# CMD [ "python3", "application.py"]