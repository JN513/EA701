#include "pico/stdlib.h"
#include <stdbool.h>

#define DEBOUNCE_MS 40

typedef struct {
    uint pin;
    bool state;
} Led;

// LEDs
Led led_r = {12, false};
Led led_g = {13, false};
Led led_b = {11, false};

// Função para alternar LED
void toggle_led(Led* led) {
    led->state = !led->state;
    gpio_put(led->pin, led->state);
}

// Interrupção de botão
void button_irq_handler(uint gpio, uint32_t events) {
    static absolute_time_t lastA_t = 0;
    static absolute_time_t lastB_t = 0;
    static absolute_time_t lastC_t = 0;

    absolute_time_t now = get_absolute_time();

    switch (gpio) {
        case 5: // BTN_A -> vermelho
            if (absolute_time_diff_us(lastA_t, now) >= DEBOUNCE_MS * 1000) {
                toggle_led(&led_r);
                lastA_t = now;
            }
            break;
        case 6: // BTN_B -> azul
            if (absolute_time_diff_us(lastB_t, now) >= DEBOUNCE_MS * 1000) {
                toggle_led(&led_b);
                lastB_t = now;
            }
            break;
        case 10: // BTN_C -> verde
            if (absolute_time_diff_us(lastC_t, now) >= DEBOUNCE_MS * 1000) {
                toggle_led(&led_g);
                lastC_t = now;
            }
            break;
        default:
            break;
    }
}

int main() {
    stdio_init_all();

    // Inicializa LEDs
    gpio_init(led_r.pin); gpio_set_dir(led_r.pin, GPIO_OUT);
    gpio_init(led_g.pin); gpio_set_dir(led_g.pin, GPIO_OUT);
    gpio_init(led_b.pin); gpio_set_dir(led_b.pin, GPIO_OUT);

    // Inicializa botões com pull-up e interrupção
    uint button_pins[] = {5, 6, 10};
    for (int i = 0; i < 3; i++) {
        gpio_init(button_pins[i]);
        gpio_set_dir(button_pins[i], GPIO_IN);
        gpio_pull_up(button_pins[i]);
        gpio_set_irq_enabled_with_callback(button_pins[i], GPIO_IRQ_EDGE_FALL, true, &button_irq_handler);
    }

    while (1) {
        tight_loop_contents(); // loop principal vazio, LEDs controlados por interrupção
    }
}
