FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get install -y libsm6 libxext6 libxrender-dev

ENV PYTHONUNBUFFERED 1
RUN mkdir /strokerecognition
WORKDIR /strokerecognition

COPY . /strokerecognition
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
