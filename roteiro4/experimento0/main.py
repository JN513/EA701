from machine import Pin
import time, os

LED = Pin(13, Pin.OUT)

def load_state():
    try:
        with open("config.txt", "r") as f:
            return int(f.read().strip()) & 1
    except:
        return 0

def save_state_safe(state):
    # escreve temporário e renomeia
    with open("config.tmp", "w") as f:
        f.write(str(state))
        f.flush()
    # renomeia (substitui antigo de forma mais segura)
    try:
        os.remove("config.txt")
    except:
        pass
    os.rename("config.tmp", "config.txt")

state = load_state()
LED.value(state)

# alterna e salva (faça isso só quando necessário)
state ^= 1
LED.value(state)
save_state_safe(state)