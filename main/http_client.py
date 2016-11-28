import json

import tornado.httpclient
import tornado.httputil


def send_message(text):
    url = "https://line-bot-hirakida.herokuapp.com/api/textMessage"
    send_text(text, url)


def send_log(text):
    url = "https://line-bot-hirakida.herokuapp.com/api/textMessage/logging"
    send_text(text, url)


def send_text(text, url):
    data = {"text": text}
    headers = tornado.httputil.HTTPHeaders({"content-type": "application/json; charset=utf-8"})
    request = tornado.httpclient.HTTPRequest(
        url=url,
        method="POST",
        body=json.dumps(data),
        headers=headers,
        validate_cert=False)
    client = tornado.httpclient.AsyncHTTPClient()
    client.fetch(request)


def send_alert_sticker():
    send_sticker("alert")


def send_start_sticker():
    send_sticker("start")


def send_stop_sticker():
    send_sticker("stop")


def send_sticker(path):
    data = {"text": "dummy"}
    headers = tornado.httputil.HTTPHeaders({"content-type": "application/json; charset=utf-8"})
    url = "https://line-bot-hirakida.herokuapp.com/api/stickerMessage/" + path
    request = tornado.httpclient.HTTPRequest(
        url=url,
        method="POST",
        body=json.dumps(data),
        headers=headers,
        validate_cert=False)
    client = tornado.httpclient.AsyncHTTPClient()
    client.fetch(request)
