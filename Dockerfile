FROM python:3.6

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
COPY ./app /app

WORKDIR /app
RUN python -m pip install -r requirements.txt

ENV CONFIG_FILE /app/config/default_config.json
VOLUME /config

EXPOSE 8080

CMD ["python","/app/bot.py"]