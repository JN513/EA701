# BitDogLab v7 — PWM (GPIO0) + PROBE por PIO (streaming, baixa memória) + OLED I2C1 (2/3)
# Joystick: VRx=GPIO27 (freq), VRy=GPIO26 (duty)
# Botões: A=GPIO5 -> mostra GERADOR; B=GPIO6 -> mostra PROBE; C=GPIO10 -> HOLD (toggle)
# Conexão física: GPIO0 -> GPIO1 (jumper)

from machine import Pin, PWM, ADC, I2C
import time
import rp2
from array import array

# ===================== Parâmetros =====================
FREQ_MIN      = 50           # Hz
FREQ_MAX      = 20000        # Hz
LPF_ALPHA     = 0.2          # filtro do joystick (0..1)
UPDATE_MS     = 250          # taxa de atualização display/medição (ms)

SAMPLE_RATE   = 1_000_000    # amostragem do sinal (Hz)
WINDOW_MS     = 3            # janela de captura (~3 ms)
EMA_ALPHA     = 0.25         # suavização do PROBE (0..1)

DEBOUNCE_MS   = 180          # debounce para o botão C (HOLD)

# ===================== PWM (GPIO0) ====================
pwm = PWM(Pin(0))
pwm.freq(1000)
pwm.duty_u16(32768)

# ===================== Joystick =======================
adc_x = ADC(27)   # VRx -> frequência
adc_y = ADC(26)   # VRy -> duty
adc_pwm = ADC(28)

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def u01(v):
    return clamp(v/65535.0, 0.0, 1.0)

def map_lin(z, a, b):
    return a + (b - a) * z

xf = u01(adc_x.read_u16())
yf = u01(adc_y.read_u16())
ypwm = u01(adc_pwm.read_u16())

# ===================== Botões (modo/HOLD) =============
btnA = Pin(5, Pin.IN, Pin.PULL_UP)   # GERADOR
btnB = Pin(6, Pin.IN, Pin.PULL_UP)   # PROBE
btnC = Pin(10, Pin.IN, Pin.PULL_UP)  # HOLD toggle (ativo em LOW)

show_probe = False
lastA = btnA.value()
lastB = btnB.value()

hold = False           # estado HOLD (True = congelado)
lastC = btnC.value()
lastC_ts = time.ticks_ms()

# ===================== OLED I2C1 (GPIO2=SDA, GPIO3=SCL)
use_oled = False
oled = None
width, height = 128, 64

def try_init_oled():
    global use_oled, oled, width, height
    try:
        i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)  # BitDogLab v7
        try:
            import ssd1306
            oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
            width, height = 128, 64
            use_oled = True
            return
        except:
            pass
        try:
            import sh1107
            oled = sh1107.SH1107_I2C(128, 128, i2c, addr=0x3C)
            width, height = 128, 128
            use_oled = True
            return
        except:
            pass
    except:
        pass

try_init_oled()

def oled_show(mode_txt, freq_hz, duty_pct, note_txt=""):
    if not use_oled:
        return
    try:
        oled.fill(0)
        oled.text("PWM GPIO0 + PIO", 0, 0)
        # selo HOLD no canto direito se ativo
        if hold:
            tag = "[HOLD]"
            x_tag = width - (len(tag) * 8)  # aprox monoespaçado 8 px
            oled.text(tag, x_tag, 0)
        oled.text("Mode: " + mode_txt, 0, 16)
        oled.text("Freq: {:>6} Hz".format(int(freq_hz)), 0, 32)
        oled.text("Duty: {:>5.1f}%".format(duty_pct), 0, 44)
        if note_txt:
            y = 56 if height == 64 else 80
            oled.text(note_txt, 0, y)
        # barra duty
        bar_y = 56 if height == 64 else (height - 14)
        bar_w = int((width - 4) * clamp(duty_pct, 0, 100) / 100.0)
        oled.rect(2, bar_y, width - 4, 10, 1)
        oled.fill_rect(2, bar_y, max(0, bar_w), 10, 1)
        oled.show()
    except:
        pass

# ===================== PIO sampler (streaming) ========
# IN + JMP = 2 ciclos → freq do SM em 2*SAMPLE_RATE p/ obter SAMPLE_RATE efetivo
@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_LEFT, autopush=True, push_thresh=32)
def logic_sampler():
    label("loop")
    in_(pins, 1)
    jmp("loop")

# StateMachine para ler GPIO1 (probe)
sm = rp2.StateMachine(0, logic_sampler, freq=SAMPLE_RATE * 2, in_base=Pin(1))

def popcount32_kern(v):
    """Popcount compatível com MicroPython (algoritmo de Kernighan)."""
    v &= 0xFFFFFFFF
    c = 0
    while v:
        v &= v - 1
        c += 1
    return c

def pio_capture_stats(n_samples, sample_rate_hz=SAMPLE_RATE):
    """
    Captura n_samples do GPIO1 e calcula estatísticas SEM listas grandes:
      - duty: contagem de '1' apenas nos bits válidos / n_samples
      - freq: média dos períodos entre bordas de SUBIDA (em amostras)
    Retorna (freq_hz, duty_pct, ok)
    """
    words = (n_samples + 31) // 32
    buf = array('I', [0] * words)

    # reinicia SM e limpa FIFO
    sm.active(0)
    sm.restart()
    while sm.rx_fifo() > 0:
        _ = sm.get()
    sm.active(1)

    # lê 'words' palavras (bloqueante)
    for i in range(words):
        buf[i] = sm.get()

    sm.active(0)

    total_bits = n_samples
    ones_count = 0
    transitions = 0
    rise_period_sum = 0
    rise_count = 0

    prev_bit = None
    last_rise_index = None
    bit_index = 0
    remain = total_bits

    # processa MSB->LSB (SHIFT_LEFT)
    for w in buf:
        take = 32 if remain >= 32 else remain
        if take <= 0:
            break

        # máscara para manter apenas os 'take' bits mais significativos
        if take < 32:
            mask = ((1 << take) - 1) << (32 - take)
            w_masked = w & mask
        else:
            w_masked = w & 0xFFFFFFFF

        # popcount apenas dos bits válidos
        ones_count += popcount32_kern(w_masked)

        # varrer só os bits válidos
        for i in range(take):
            cur_bit = (w_masked >> (31 - i)) & 1
            if prev_bit is not None:
                if cur_bit != prev_bit:
                    transitions += 1
                    # borda de subida
                    if prev_bit == 0 and cur_bit == 1:
                        if last_rise_index is not None:
                            period = bit_index - last_rise_index
                            if period > 0:
                                rise_period_sum += period
                                rise_count += 1
                        last_rise_index = bit_index
            prev_bit = cur_bit
            bit_index += 1

        remain -= take

    duty_pct = (ones_count * 100.0) / total_bits if total_bits > 0 else 0.0

    # Freq preferencial: períodos entre subidas
    if rise_count > 0 and rise_period_sum > 0:
        avg_period_samps = rise_period_sum / rise_count
        freq_hz = sample_rate_hz / avg_period_samps
        return (freq_hz, duty_pct, True)

    # Fallback: por transições (menos preciso)
    cycles = transitions / 2.0
    if cycles > 0:
        freq_hz = cycles * (sample_rate_hz / total_bits)
        return (freq_hz, duty_pct, True)

    return (0.0, duty_pct, False)

# ===================== Laço principal =================
print("PWM(GPIO0) + PROBE PIO(GPIO1). A=GERADOR, B=PROBE, C=HOLD. CTRL+C ok.")

ema_freq = None
ema_duty = None
last_update = time.ticks_ms()
last_ui = time.ticks_ms()

# número de amostras por janela
N_SAMPLES = int(SAMPLE_RATE * (WINDOW_MS / 1000.0))
if N_SAMPLES < 256:
    N_SAMPLES = 256  # mínimo

# Valores atuais aplicados ao PWM (ficam congelados no HOLD)
freq_set = 1000
duty_set = 50.0

while True:
    # ---- Leitura do botão C (HOLD toggle) com debounce ----
    now = time.ticks_ms()
    c = btnC.value()
    if lastC == 1 and c == 0 and time.ticks_diff(now, lastC_ts) > DEBOUNCE_MS:
        hold = not hold           # alterna HOLD
        lastC_ts = now
    lastC = c

    # ---- PWM controlado pelo joystick (a menos que HOLD) ----
    if not hold:
        xr = u01(adc_x.read_u16()); yr = u01(adc_y.read_u16())
        xf = (1 - LPF_ALPHA)*xf + LPF_ALPHA*xr
        yf = (1 - LPF_ALPHA)*yf + LPF_ALPHA*yr

        freq_set = int(map_lin(xf, FREQ_MIN, FREQ_MAX))
        freq_set = clamp(freq_set, FREQ_MIN, FREQ_MAX)
        freq_set = 10000
        duty_set = (1.0 - yf) * 100.0

    # aplica (mesmo em HOLD os valores ficam constantes)
    pwm.freq(freq_set)
    pwm.duty_u16(int(65535 * (duty_set/100.0)))

    # ---- alternância de tela pelos botões A/B ----
    if time.ticks_diff(now, last_ui) >= 20:
        a = btnA.value(); b = btnB.value()
        if lastA == 1 and a == 0:
            show_probe = False  # GERADOR
        if lastB == 1 and b == 0:
            show_probe = True   # PROBE
        lastA, lastB = a, b
        last_ui = now

    ypwm = u01(adc_pwm.read_u16())
    # ---- captura/análise PIO e display ----
    if time.ticks_diff(now, last_update) >= UPDATE_MS:
        if show_probe:
            f, d, ok = pio_capture_stats(N_SAMPLES, SAMPLE_RATE)
            if ema_freq is None:
                ema_freq = f
            else:
                ema_freq = (1-EMA_ALPHA)*ema_freq + EMA_ALPHA*f
            if ema_duty is None:
                ema_duty = d
            else:
                ema_duty = (1-EMA_ALPHA)*ema_duty + EMA_ALPHA*d
            note = "" if ok else "Poucos ciclos"
            oled_show("PROBE PIO (GPIO1)", ema_freq, ema_duty, note)
        else:
            #oled_show("GERADOR (GPIO0)", freq_set, duty_set, "")
            # fix to interval 0 - 1 for voltage
            y_v = 3.3 * ypwm
            #oled_show("Tensao ", y_v, "")
            oled.fill(0)
            oled.text("Tensao (V)", 0, 0)
            oled.text("{:.2f}".format(y_v), 0, 10)
            #oled.text("Bruto: ", 0, 20)
            #oled.text("{}".format(ypwm), 0, 30)
            oled.text("Duty: ", 0, 20)
            oled.text("{}".format(duty_set), 0, 30)
            oled.text("Freq: ", 0, 40)
            oled.text("{}".format(freq_set), 0, 50)
            oled.show()
        last_update = now

    time.sleep_ms(2)