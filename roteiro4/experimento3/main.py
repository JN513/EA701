from machine import ADC
import utime
import array

MIC_PIN = 28
FS = 20000         # 20 kHz (teórico)
DURATION = 1       # segundos de gravação (ajuste conforme RAM disponível)
FILENAME = "audio.txt"


adc = ADC(MIC_PIN)


num_samples = FS * DURATION


# Usa array para economizar RAM (uint16 = 2 bytes por amostra)
samples = array.array("H", [0] * num_samples)


print("Gravando na RAM...")
start = utime.ticks_ms()


for i in range(num_samples):
    samples[i] = adc.read_u16()
    utime.sleep_us(50)   # controla taxa (remova para ver máxima possível)


end = utime.ticks_ms()
elapsed_ms = utime.ticks_diff(end, start)
elapsed_s = elapsed_ms / 1000


print(f"{num_samples} amostras gravadas na RAM")
print(f"Tempo decorrido: {elapsed_s:.3f} s")
print(f"Taxa de amostragem efetiva: {num_samples / elapsed_s:.1f} Hz")


# --- Salva em TXT no final ---
print(f"Salvando {num_samples} amostras em {FILENAME}...")
with open(FILENAME, "w") as f:
    for v in samples:
        f.write(str(v) + "\n")


print("Salvo com sucesso!")