FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5005

CMD ["python", "app.py"]