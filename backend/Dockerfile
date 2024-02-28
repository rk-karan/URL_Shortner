FROM python:3.9.6

WORKDIR /backend

COPY ./requirements.txt .

RUN python -m pip install --proxy http://proxy-wsa.esl.cisco.com:80 --upgrade pip
RUN pip3 install --proxy http://proxy-wsa.esl.cisco.com:80 -r requirements.txt

COPY . .

CMD ["python", "-m", "gunicorn", "main:app", "--workers", "2", "--bind", "0.0.0.0:8000", "--timeout", "2400", "-k" , "uvicorn.workers.UvicornWorker"]