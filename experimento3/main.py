from machine import Pin
import utime

# === PINAGEM (ajuste conforme sua placa) ===
PIN_R = 12
PIN_G = 13
PIN_B = 11
BTN_A = 5
BTN_B = 6
BTN_C = 10

# === LEDs ===
R = Pin(PIN_R, Pin.OUT)
G = Pin(PIN_G, Pin.OUT)
B = Pin(PIN_B, Pin.OUT)

# === Botões (pull-down) ===
btnA = Pin(BTN_A, Pin.IN, Pin.PULL_UP)
btnB = Pin(BTN_B, Pin.IN, Pin.PULL_UP)
btnC = Pin(BTN_C, Pin.IN, Pin.PULL_UP)

# Estados atuais das cores (0=off, 1=on)
r_on = g_on = b_on = 0

# Para detecção de borda + debounce
lastA = lastB = lastC = 10
last_ms_A = last_ms_B = last_ms_C = 0
DEBOUNCE_MS = 20

def apply_leds():
    R.value(1 if r_on else 0)
    G.value(1 if g_on else 0)
    B.value(1 if b_on else 0)

while True:
    now = utime.ticks_ms()

    # --- Botão A → vermelho ---
    vA = btnA.value()
    if vA and not lastA:
        if utime.ticks_diff(now, last_ms_A) >= DEBOUNCE_MS:
            r_on ^= 1
            apply_leds()
            last_ms_A = now
    lastA = vA

    # --- Botão B → azul ---
    vB = btnB.value()
    if vB and not lastB:
        if utime.ticks_diff(now, last_ms_B) >= DEBOUNCE_MS:
            b_on ^= 1
            apply_leds()
            last_ms_B = now
    lastB = vB

    # --- Botão C → verde ---
    vC = btnC.value()
    if vC and not lastC:
        if utime.ticks_diff(now, last_ms_C) >= DEBOUNCE_MS:
            g_on ^= 1
            apply_leds()
            last_ms_C = now
    lastC = vC

    utime.sleep_ms(2)  # alivia CPU e ajuda o debounce