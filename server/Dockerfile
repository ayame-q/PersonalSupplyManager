FROM python:3-alpine
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE=1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED=1
# tz_dataのインストール時の操作をスキップするために設定
ENV DEBIAN_FRONTEND=noninteractive

RUN apk --update-cache --no-cache add python3-dev postgresql-client \
    gcc libc-dev linux-headers postgresql-dev openssl-dev libffi-dev

COPY ./requirements.txt /usr/src/app/
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt

COPY . /usr/src/app
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "entrypoint.sh" ]
# DEBUG=falseの場合の実行コマンド
CMD daphne -b 0.0.0.0 -p 8000 config.asgi:application
