FROM python:3.8-slim-buster
LABEL maintainer=ahaljh@gmail.com

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential
RUN pip3 install -U pip

COPY ./requirements.txt /code/
RUN pip3 install --no-cache-dir -r /code/requirements.txt

COPY ./*.py /code/

WORKDIR /code/
ENTRYPOINT [ "/bin/bash", "python", "weatherbot.py" ]