# Regular Container
FROM python:3.7
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP app
ENV PORT 3000
ENV DEBUG True

EXPOSE 3000 3000
