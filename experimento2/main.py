from machine import Pin
import time

class LedRGB:
    def __init__(self, r=13, g=11, b=12):
        self.r = Pin(r, Pin.OUT)
        self.g = Pin(g, Pin.OUT)
        self.b = Pin(b, Pin.OUT)

    def set(self, r=0, g=0, b=0):
        self.r.value(r)
        self.g.value(g)
        self.b.value(b)

    def off(self):
        self.set(0,0,0)

led = LedRGB()
led.set(1,0,0)  # vermelho
time.sleep(1)
led.off()