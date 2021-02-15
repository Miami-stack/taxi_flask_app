FROM python:3.8

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

EXPOSE 5050

COPY . /app

CMD ["python", "app/main.py"]
