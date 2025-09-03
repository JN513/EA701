from machine import Pin
import time

# Definindo os pinos RGB
PIN_R = Pin(13, Pin.OUT)
PIN_G = Pin(11, Pin.OUT)
PIN_B = Pin(12, Pin.OUT)

# Função para ligar o LED
def led_set(r=0, g=0, b=0):
    PIN_R.value(r)
    PIN_G.value(g)
    PIN_B.value(b)

# Função para desligar o LED
def led_off():
    led_set(0, 0, 0)

# Exemplo de uso
led_set(1, 0, 0)  # vermelho
time.sleep(1)
led_off()
