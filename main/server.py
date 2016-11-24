# Fail-safe: Wifiが切れたりした時にAMP出力を停止して、Steeringを中立に戻すようなことをやっときたい
# commandを受け取って、ステアリングとアンプの制御をする。
# サーボコントローラを別クラスで作って、そこにコマンド情報を引き渡す
#  サーボ制御にかかる時間＞message受信時間 だと思うので、受信コマンドを馬鹿正直に全部こなそうとすると破綻(変な動き)する
#    サーボコントロールが完了するまでに受信したコマンドは破棄する？ でもAMPの制御はそうはいかないかもしれない
#
# 安全側に倒すなら、コマンドはHealth checkも兼ねて、常時送信してもらうようにする。
#   コマンドが一定時間途切れたら自動停止(Steering中立＋アクセルオフ)
#   &リスタート的なコマンドを受信してから再開する(ステートを持つことになってしまう・・・？)
# 赤外線からの信号を別途読み取らせて、危ない時は割り込んで動作させる。
#
# ws:/localhost:9090/ws
#
import json

import tornado.ioloop
import tornado.template
import tornado.web
import tornado.websocket

import main.RepeatedTimer
from main.IrDriver import *
from main.utils import *


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    @logger
    def open(self):
        self.write_message("The server says: 'Hello'. Connection was accepted.")
        self.clients.append(self)

    @logger
    def on_message(self, message):
        data = json.loads(message)
        if isinstance(data, list):
            for d in data:
                self.write_message("Received: " + d['command'] + "=" + str(d['value']))

    @logger
    def on_close(self):
        self.clients.remove(self)
        rt.stop()

    @classmethod
    def write_to_clients(cls, message):
        for client in cls.clients:
            client.write_message(message)


def ir_notify(value):
    WSHandler.write_to_clients("ir_notify" + value)


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

# interval push message sample
rt = main.RepeatedTimer.RepeatedTimer(1, WSHandler.write_to_clients, "inoue")
ir = IrDriver(ir_notify, 10)

if __name__ == "__main__":
    application.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
