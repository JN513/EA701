from machine import Pin
import utime, time

led = Pin(13, Pin.OUT)
btn = Pin(5, Pin.IN, Pin.PULL_UP)

last_ms = 0
state = 0

# Callback executado automaticamente quando o botão é pressionado
def on_press(pin):
    global last_ms, state
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_ms) < 150:  # debounce ~20 ms
        return
    last_ms = now
    state ^= 1
    led.value(state)

# Registra a função como interrupção na borda de subida
btn.irq(trigger=Pin.IRQ_FALLING
, handler=on_press)

N = 256000
last = 0

while True:
    # Laço vazio para simular CPU ocupada
    for _ in range(N):
        pass