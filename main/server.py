# -*- coding: utf-8 -*-
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
import sys
import time

import tornado.websocket

sys.path.append('/home/pi/vrrc')

from main.ir_driver import *
from main.servo_drv import *
from main.repeated_timer import *
from main.redray import *
from main.http_client import send_message


# test用のhandler
class SendMessageHandler(tornado.web.RequestHandler):
    def get(self, *args):
        data = self.get_argument("data")
        if data is not None:
            send_message(data)


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    @logger
    def open(self):
        self.write_message("The server says: 'Hello'. Connection was accepted.")
        self.clients.append(self)
        send_message("open")
        if len(self.clients) == 1:
            health_check.start()
            servo.start()
            ir.start()

    @logger
    def on_message(self, message):
        data = json.loads(message)
        if isinstance(data, list):
            for d in data:
                self.write_message(d['command'] + ":" + str(d['value']))
                command_dict.get(d['command'])(d['value'])
                #send_message(str(d['command']) + ":" + str(d['value']))

    @logger
    def on_close(self):
        self.clients.remove(self)
        send_message("on_close")
        if len(self.clients) == 0:
            health_check.stop()
            ir.stop()
            servo.stop()

    @classmethod
    def write_to_clients(cls, message):
        for client in cls.clients:
            client.write_message(message)


def ir_notify(value):
    WSHandler.write_to_clients("ir_notify" + value)


@logger
def steering(value):
    servo.setValue(SERVO_0_GPIO, value)


@logger
def acceleration(value):
    print('------------ acceleration:')
    print(redray.fireBrake)
    if redray.fireBrake:
        if value > 0:
            servo.setValue(SERVO_1_GPIO, 0)
        else:
            servo.setValue(SERVO_1_GPIO, value)
    else:
        servo.setValue(SERVO_1_GPIO, value)


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/msg', SendMessageHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

command_dict = {
    'steering': steering,
    'acceleration': acceleration
}

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.add_event_detect(24, GPIO.RISING, callback=deploy, bouncetime=400)

# interval push message sample
health_check = RepeatedTimer(1, WSHandler.write_to_clients, "active")
RepeatedTimer(0.1, queue_routine, WSHandler.write_to_clients)
ir = IrDriver(ir_notify, 10)
servo = ServoDriver(0.05)
redray = Redray()

if __name__ == "__main__":
    threads = []
    try:
        threads.append(redray)
        redray.start()
        application.listen(9090)
        tornado.ioloop.IOLoop.instance().start()
        while redray.is_alive():
            redray.join(1)
    except KeyboardInterrupt:
        for thread in threads:
            thread.running = False
        while threading.active_count() > 1:
            print("waiting shutdown. thread count={}".format(threading.active_count()))
            time.sleep(1)
