import numpy as np
from scipy.io.wavfile import write


# carregar seu arquivo TXT
with open("audio.txt", "r") as f:
    data = np.array([int(line.strip()) for line in f if line.strip()], dtype=np.uint16)


# converter para int16
audio_data = (data.astype(np.int32) - 32768).astype(np.int16)


# salvar
write("nome_do_arquivo.wav", 20000, audio_data)