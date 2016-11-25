import json
import tornado.httputil
import tornado.httpclient


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
