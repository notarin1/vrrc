# -*- coding: utf-8 -*-
import wiringpi
import main.RepeatedTimer as RepeatedTimer

from main.utils import *

SERVO_0_PIN = 32  # GPIO12
SERVO_1_PIN = 33  # GPIO13


class ServoDriver(object):
    pin_values = {
        SERVO_0_PIN: 0,
        SERVO_1_PIN: 0
    }

    def __init__(self, interval):
        wiringpi.wiringPiSetupGpio()
        # ハードウェアPWMで出力する
        wiringpi.pinMode(SERVO_0_PIN, 2)
        wiringpi.pinMode(SERVO_1_PIN, 2)
        # サーボモータに合わせたPWM波形の設定
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetRange(1024)
        wiringpi.pwmSetClock(375)
        pass
        self.rt = RepeatedTimer.RepeatedTimer(interval, self.writeValue, "SERVO")

    def start(self):
        self.rt.start()

    def stop(self):
        self.rt.stop()

    # target: SERVO_0_PIN or SERVO_1_PIN
    # defree: -90 〜 90
    @logger
    def setValue(self, target, value):
        if target != SERVO_0_PIN and target != SERVO_1_PIN:
            return

        self.pin_values[target] = value

    def writeValue(self, message):
        servo0_value = self.pin_values[SERVO_0_PIN]
        servo1_value = self.pin_values[SERVO_1_PIN]

        # Steering制御
        move_deg = int(81 + 41 / 90 * servo0_value)
        wiringpi.pwmWrite(SERVO_0_PIN, move_deg)

        # AMP制御
        wiringpi.pwmWrite(SERVO_1_PIN, servo1_value)
