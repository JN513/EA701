from machine import Pin
import time

# Definições dos pinos
R_PIN = 13
G_PIN = 11
B_PIN = 12

# Função para verificar primos até n
def primos_ate(n):
    primos = []
    for num in range(2, n+1):
        eh_primo = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                eh_primo = False
                break
        if eh_primo:
            primos.append(num)
    return primos

# Espera inicial (5s) para abrir o terminal
time.sleep(5)

print("Hello, World!")
print("Iniciando Benchmark...")

# Marca de tempo inicial
inicio = time.ticks_us()

# Inicialização dos GPIOs
r = Pin(R_PIN, Pin.OUT)
g = Pin(G_PIN, Pin.OUT)
b = Pin(B_PIN, Pin.OUT)

r.value(0)
g.value(0)
b.value(0)

fim_init_gpios = time.ticks_us()

# Loop de contagem com LED piscando
for i in range(10):
    print("Counter:", i)
    b.value(1)
    time.sleep_ms(500)
    b.value(0)
    time.sleep_ms(500)

fim = time.ticks_us()

# Diferenças de tempo (usando ticks_diff para evitar overflow)
tempo_total = time.ticks_diff(fim, inicio)
tempo_init_gpios = time.ticks_diff(fim_init_gpios, inicio)

print("Tempo total:", tempo_total, "us")
print("Tempo inicialização GPIOs:", tempo_init_gpios, "us")

# Benchmark
N = 10000  # limite superior para calcular primos

print("Iniciando benchmark de primos até", N)

inicio = time.ticks_us()
resultado = primos_ate(N)
fim = time.ticks_us()

tempo_total = time.ticks_diff(fim, inicio)

print("Total de primos encontrados:", len(resultado))
print("Tempo decorrido:", tempo_total, "us")

# Loop infinito piscando o LED verde
while True:
    g.value(1)
    time.sleep_ms(500)
    g.value(0)
    time.sleep_ms(500)

# Tempo total: 10000689 us
# Tempo inicialização GPIOs: 452 us
# Iniciando benchmark de primos até 10000
# Total de primos encontrados: 1229
# Tempo decorrido: 1226509 us