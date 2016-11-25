# -*- coding: utf-8 -*-
import sys
import threading
from time import sleep

import RPi.GPIO as GPIO
import spidev

sys.path.append('/home/pi/vrrc')
from main.event_queue import *

class Redray(threading.Thread):
    def __init__(self):
        super(Redray, self).__init__()
        self.running = True

    # MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
    def readadc_spidev(self, adcnum, spi):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        commandout = adcnum
        commandout |= 0x08  # シングルエンドビット
        commandout = commandout<<4
        ret = spi.xfer2([1, commandout, 0, 0])
        adcout = ((ret[1]&0x03)<<10) | (ret[2]<<2) | ret[3]&0x03
        return adcout

    def convert_voltage(self, analog):
        return analog * 5.0 / 4095

    def distance(self, voltage):
        return (18.679 / voltage) - 4.774 if voltage != 0 else 0

    def switchBrake(self, dist):
        if 1 < dist && dist < 5:
            global fireBrake = True
        else:
            global fireBrake = False
        print(fireBrake)


    def run(self):
        GPIO.setmode(GPIO.BCM)
        spi = spidev.SpiDev()
        spi.open(0, 0) # bus0, CE0

        try:
            while self.running:
                inputVal0 = self.readadc_spidev(0, spi)
                volt = self.convert_voltage(inputVal0)
                dist = (self.distance(volt))
                print(" distance: {} ".format(dist))
                switchBrake(dist)
                enqueue_event(" distance: {} ".format(dist))
                sleep(0.02)
        finally:
            spi.close()
