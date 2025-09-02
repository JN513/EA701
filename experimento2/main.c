#include "pico/stdlib.h"

#define LED 13
#define BTN 5

int main() {
    stdio_init_all();
    gpio_init(LED); gpio_set_dir(LED, GPIO_OUT);
    gpio_init(BTN); gpio_set_dir(BTN, GPIO_IN); gpio_pull_down(BTN);

    bool last = false, state = false;

    // Defina aqui a carga artificial: número de iterações do laço vazio
    int N = 8000;   // experimente 2000, 8000, 32000, 128000

    while (true) {
        bool v = gpio_get(BTN);
        if (v && !last) {
            state = !state;
            gpio_put(LED, state);
            sleep_ms(20);   // debounce simples
        }
        last = v;

        // Laço vazio para simular CPU ocupada
        for (volatile int i=0; i<N; i++) {
            __asm volatile("nop"); // "no operation" - só gasta tempo
        }
    }
}