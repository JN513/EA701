import time, os

# Gera bloco de dados para gravar
N = 32 * 1024
data = bytes([i & 0xFF for i in range(N)])

def write_once(path, payload):
    t0 = time.ticks_us()
    with open(path, "wb") as f:
        f.write(payload)
        f.flush()            # força flush no FS
        # Alguns ports têm uos.sync(); no RP2040 pode não existir.
        # close() também força commit no final do with.
    t1 = time.ticks_us()
    return time.ticks_diff(t1, t0)/1000

# "Aquecimento" (evita medir latência inicial do FS/interprete)
write_once("warmup.bin", b"\x00"*1024)

# Rodadas cruas
times = [write_once("data.bin", data) for _ in range(5)]
print("Flash FS write ({} bytes) ms:", times, "média =", sum(times)/len(times))