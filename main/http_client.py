import json

import tornado.httpclient
import tornado.httputil


def send_message(text):
    data = {"text": text}
    headers = tornado.httputil.HTTPHeaders({"content-type": "application/json; charset=utf-8"})
    request = tornado.httpclient.HTTPRequest(
        url="https://line-bot-hirakida.herokuapp.com/api/textMessage",
        method="POST",
        body=json.dumps(data),
        headers=headers,
        validate_cert=False)
    client = tornado.httpclient.AsyncHTTPClient()
    client.fetch(request)


def send_alert_sticker():
    send("alert")


def send_start_sticker():
    send("start")


def send_stop_sticker():
    send("stop")


def send(path):
    url = "https://line-bot-hirakida.herokuapp.com/api/stickerMessage/" + path
    headers = tornado.httputil.HTTPHeaders({"content-type": "application/json; charset=utf-8"})
    request = tornado.httpclient.HTTPRequest(
        url=url,
        method="POST",
        headers=headers,
        validate_cert=False)
    client = tornado.httpclient.AsyncHTTPClient()
    client.fetch(request)
