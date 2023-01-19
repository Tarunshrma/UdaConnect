FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN \
    apk add --no-cache bash && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt
CMD ["python", "app.py"]