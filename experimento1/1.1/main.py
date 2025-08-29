# exemplo_pico.py
# Código em MicroPython para Raspberry Pi Pico
# Faz o LED onboard piscar a cada 0.5s

from machine import Pin, Timer

# LED onboard do Pico fica no pino 25
led = Pin(12, Pin.OUT)

# Função que alterna o estado do LED
def toggle_led(timer):
    led.toggle()

# Timer chama a função a cada 500ms
timer = Timer()
timer.init(freq=2, mode=Timer.PERIODIC, callback=toggle_led)

# Mantém o programa rodando
while True:
    pass
