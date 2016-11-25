# -*- coding: utf-8 -*-
import wiringpi

from main.repeated_timer import RepeatedTimer
from main.utils import *

SERVO_0_GPIO = 12  # GPIO12
SERVO_1_GPIO = 13  # GPIO13

AMP_VALUE_NEUTRAL = 70  # neutral:アクセルオフ状態値

ESC_LIMITTER = 0.1      # ESC出力をESC_LIMITTER % で絞る

class ServoDriver(object):
    pin_values = {
        SERVO_0_GPIO: 0,
        SERVO_1_GPIO: AMP_VALUE_NEUTRAL  # 70:neutral, v > 70:forward, v < 70:reverse
    }

    def __init__(self, interval):
        wiringpi.wiringPiSetupGpio()
        # ハードウェアPWMで出力する
        wiringpi.pinMode(SERVO_0_GPIO, 2)
        wiringpi.pinMode(SERVO_1_GPIO, 2)
        # サーボモータに合わせたPWM波形の設定
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetRange(1024)
        wiringpi.pwmSetClock(375)
        pass
        self.rt = RepeatedTimer(interval, self.writeValue, "SERVO")

    def start(self):
        self.rt.start()

    def stop(self):
        self.rt.stop()
        self.writeValue("STOPPED")

    # target: SERVO_0_PIN or SERVO_1_PIN
    # defree: -90 〜 90
    @logger
    def setValue(self, target, value):
        if target != SERVO_0_GPIO and target != SERVO_1_GPIO:
            return

        self.pin_values[target] = value

    def writeValue(self, message):
        row_value0 = self.clip(self.pin_values[SERVO_0_GPIO])
        row_value1 = self.clip(self.pin_values[SERVO_1_GPIO])

        servo_value = 81 + 41 * row_value0 / 3.0  # degree
        esc_value = (row_value1 * 10 * ESC_LIMITTER) + AMP_VALUE_NEUTRAL

        # Steering制御
        wiringpi.pwmWrite(SERVO_0_GPIO, int(servo_value))

        # AMP制御
        wiringpi.pwmWrite(SERVO_1_GPIO, int(esc_value))

    def clip(self, value):
        if value < -1.0:
            value = -1.0
        elif value > 1.0:
            value = 1.0

        return value
