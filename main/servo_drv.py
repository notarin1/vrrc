# -*- coding: utf-8 -*-
import wiringpi

from main.utils import *

SERVO_0_PIN = 32  # GPIO12
SERVO_1_PIN = 33  # GPIO13


class ServoDriver(object):
    def __init__(self):
        wiringpi.wiringPiSetupGpio()
        # ハードウェアPWMで出力する
        wiringpi.pinMode(SERVO_0_PIN, 2)
        wiringpi.pinMode(SERVO_1_PIN, 2)
        # サーボモータに合わせたPWM波形の設定
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetRange(1024)
        wiringpi.pwmSetClock(375)
        pass

    # target: SERVO_0_PIN or SERVO_1_PIN
    # defree: -90 〜 90
    @logger
    def setValue(self, target, degree):
        if target != SERVO_0_PIN and target != SERVO_1_PIN:
            return

        if degree < -90 or degree > 90:
            return

        # 角度から送り出すPWMのパルス幅を算出する
        move_deg = int(81 + 41 / 90 * degree)
        # サーボモータにPWMを送り、サーボモータを動かす
        wiringpi.pwmWrite(target, move_deg)
