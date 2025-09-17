import time

N = 10_000
buf = bytearray(N)

t0 = time.ticks_us()
for i in range(N):
    buf[i] = i & 0xFF   # escrita em RAM (heap)
t1 = time.ticks_us()

dt_ms = time.ticks_diff(t1, t0) / 1000
print("RAM write ({} bytes): {:.3f} ms".format(N, dt_ms))

# RAM write (10000 bytes): 153.715 ms
# RAM write (10000 bytes): 153.715 ms
# RAM write (10000 bytes): 153.720 ms
# 153.716