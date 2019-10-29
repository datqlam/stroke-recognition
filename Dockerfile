FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /strokerecognition
WORKDIR /strokerecognition

COPY . /strokerecognition
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
