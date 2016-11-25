# -*- coding: utf-8 -*-
import wiringpi

from main.repeated_timer import RepeatedTimer
from main.utils import *

SERVO_0_GPIO = 12       # GPIO12
SERVO_1_GPIO = 13       # GPIO13

AMP_VALUE_NEUTRAL = 70  # neutral:アクセルオフ状態値

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
        servo_value = self.pin_values[SERVO_0_GPIO]
        esc_value = self.pin_values[SERVO_1_GPIO] * 10 + AMP_VALUE_NEUTRAL

        # Steering制御
        move_deg = int(81 + 41 * servo_value)
        wiringpi.pwmWrite(SERVO_0_GPIO, move_deg)

        # AMP制御
        wiringpi.pwmWrite(SERVO_1_GPIO, int(esc_value))
