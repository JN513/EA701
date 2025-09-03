#include <stdio.h>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();

    // Definindo os pinos RGB
    const uint PIN_R = 13;
    const uint PIN_G = 11;
    const uint PIN_B = 12;

    // Inicializando os pinos como saída
    gpio_init(PIN_R);
    gpio_set_dir(PIN_R, GPIO_OUT);

    gpio_init(PIN_G);
    gpio_set_dir(PIN_G, GPIO_OUT);

    gpio_init(PIN_B);
    gpio_set_dir(PIN_B, GPIO_OUT);

    // Sequência de cores (R, G, B)
    bool colors[][3] = {
        {1, 0, 0},  // vermelho
        {0, 1, 0},  // verde
        {0, 0, 1},  // azul
        {0, 0, 0}   // desligado
    };

    int n = sizeof(colors) / sizeof(colors[0]);

    while (1) {
        for (int i = 0; i < n; i++) {
            gpio_put(PIN_R, colors[i][0]);
            gpio_put(PIN_G, colors[i][1]);
            gpio_put(PIN_B, colors[i][2]);
            sleep_ms(500);
        }
    }
}
