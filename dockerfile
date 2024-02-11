FROM python:3.11

WORKDIR /messenger

COPY requirements.txt .
COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "run.py"]