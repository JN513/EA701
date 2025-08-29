#include <stdio.h>
#include <time.h>
#include "pico/stdlib.h"
#include <math.h>
#include <stdbool.h>

#define R_PIN 13
#define G_PIN 11
#define B_PIN 12

bool eh_primo(int num) {
    if (num < 2) return false;
    for (int i = 2; i <= (int)sqrt(num); i++) {
        if (num % i == 0) return false;
    }
    return true;
}


int main(){
    stdio_init_all();

    sleep_ms(5000);

    printf("Hello, World!\n");
    printf("Iniciando Benchmark...\n");

    // Marca de tempo inicial
    uint64_t inicio = time_us_64();

    gpio_init(R_PIN);
    gpio_init(G_PIN);
    gpio_init(B_PIN);
    gpio_set_dir(R_PIN, GPIO_OUT);
    gpio_set_dir(G_PIN, GPIO_OUT);
    gpio_set_dir(B_PIN, GPIO_OUT);

    gpio_put(R_PIN, 0);
    gpio_put(G_PIN, 0);
    gpio_put(B_PIN, 0);

    uint64_t fim_init_gpios = time_us_64();

    for(int i = 0; i < 10; i++) {
        printf("Counter: %d\n", i);
        gpio_put(B_PIN, 1);
        sleep_ms(500);
        gpio_put(B_PIN, 0);
        sleep_ms(500);
    }

    uint64_t fim = time_us_64();
    uint64_t tempo_total = fim - inicio;
    uint64_t tempo_init_gpios = fim_init_gpios - inicio;

    printf("Tempo total: %llu us\n", tempo_total);
    printf("Tempo inicialização GPIOs: %llu us\n", tempo_init_gpios);

    int N = 10000; // limite superior
    int count = 0;

    printf("Iniciando benchmark de primos até %d...\n", N);

    inicio = time_us_64();

    for (int i = 2; i <= N; i++) {
        if (eh_primo(i)) {
            count++;
        }
    }

    fim = time_us_64();
    tempo_total = fim - inicio;

    printf("Total de primos encontrados: %d\n", count);
    printf("Tempo decorrido: %llu us\n", tempo_total);

    while (true) {
        gpio_put(G_PIN, 1);
        sleep_ms(500);
        gpio_put(G_PIN, 0);
        sleep_ms(500);
    }

    return 0;
}

/*
Tempo total: 10010890 us
Tempo inicialização GPIOs: 13 us
Iniciando benchmark de primos até 10000...
Total de primos encontrados: 1229
Tempo decorrido: 246757 us
*/