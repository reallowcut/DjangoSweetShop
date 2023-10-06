FROM python:3.10-slim

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
ADD ./requirements.txt .
RUN pip3  install -r requirements.txt
RUN mkdir ./src
ADD ./src /src

WORKDIR src
USER user