FROM python:3.6.9-alpine

RUN mkdir /code/
WORKDIR /code/

ADD requirements.txt /requirements.txt
RUN python -m pip install -r /requirements.txt

ADD . /code/

ENV CLIENT_TOKEN=${CLIENT_TOKEN}
ENV USER_ID=${USER_ID}
ENV GUILD_ID=${GUILD_ID}

CMD ["python", "bot.py"]
