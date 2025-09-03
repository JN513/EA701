from machine import Pin
import utime

DEBOUNCE_MS = 20

# === Classes ===
class LedRGB:
    def __init__(self, r_pin, g_pin, b_pin):
        self.r = Pin(r_pin, Pin.OUT)
        self.g = Pin(g_pin, Pin.OUT)
        self.b = Pin(b_pin, Pin.OUT)
        self.r_on = 0
        self.g_on = 0
        self.b_on = 0
        self.apply()

    def toggle_r(self):
        self.r_on ^= 1
        self.apply()

    def toggle_g(self):
        self.g_on ^= 1
        self.apply()

    def toggle_b(self):
        self.b_on ^= 1
        self.apply()

    def apply(self):
        self.r.value(self.r_on)
        self.g.value(self.g_on)
        self.b.value(self.b_on)


class Button:
    def __init__(self, pin, callback):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.last_time = utime.ticks_ms()
        # Configura IRQ na borda de subida (botão pressionado)
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=self._irq_handler)
        self.callback = callback

    def _irq_handler(self, pin):
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.last_time) >= DEBOUNCE_MS:
            self.callback()
            self.last_time = now


# === Inicialização ===
led = LedRGB(r_pin=12, g_pin=13, b_pin=11)

# Associa cada botão à função de alternar a cor correspondente
btnA = Button(5, led.toggle_r)  # vermelho
btnB = Button(6, led.toggle_b)  # azul
btnC = Button(10, led.toggle_g) # verde

# Loop principal vazio, LEDs controlados por interrupção
while True:
    utime.sleep_ms(100)
