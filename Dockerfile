# pull official base image
FROM python:3.9

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create workdir
# RUN mkdir /src
WORKDIR /src

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /src
# RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN pip install -r requirements.txt


ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
CMD python3 _bot.py


# ENV BINANCE_API_KEY ${BINANCE_API_KEY}
# ENV BINANCE_SECRET_KEY ${BINANCE_SECRET_KEY}
# CMD python3 _binance/binance_webhook.py

# copy project
COPY . /src