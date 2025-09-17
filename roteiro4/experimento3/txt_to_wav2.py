import numpy as np
import wave
import struct


# Configurações
input_file = "arquivo_audio.txt"   # arquivo com valores do ADC separados por vírgula
output_file = "saida.wav"  # arquivo wav gerado
sample_rate = 40000        # Hz


# 1. Ler o arquivo txt
with open(input_file, "r") as f:
    data_str = f.read().strip()


# 2. Converter para lista de inteiros
adc_values = np.array([int(x) for x in data_str.split(",") if x.strip() != ""])


# 3. Normalizar 12 bits (0-4095) para 16 bits signed (-32768 a 32767)
# Centralizar em zero: (valor - 2048) → vai de -2048 a +2047
centered = adc_values - 2048
# Expandir para 16 bits
scaled = np.int16(centered * (32767 / 2048))


# 4. Criar arquivo WAV
with wave.open(output_file, "w") as wav_file:
    n_channels = 1          # mono
    sampwidth = 2           # 2 bytes (16 bits)
    n_frames = len(scaled)


    wav_file.setparams((n_channels, sampwidth, sample_rate, n_frames, "NONE", "not compressed"))


    # Escrever os dados
    for s in scaled:
        wav_file.writeframes(struct.pack('<h', s))  # little-endian signed 16 bits


print(f"Arquivo '{output_file}' gerado com sucesso!")