#include "pico/stdlib.h"

#define PIN_R 12
#define PIN_G 13
#define PIN_B 11
#define BTN_A 5
#define BTN_B 6
#define BTN_C 10
#define DEBOUNCE_MS 40

int main() {
    stdio_init_all();

    // LEDs
    gpio_init(PIN_R); gpio_set_dir(PIN_R, GPIO_OUT);
    gpio_init(PIN_G); gpio_set_dir(PIN_G, GPIO_OUT);
    gpio_init(PIN_B); gpio_set_dir(PIN_B, GPIO_OUT);

    // Botões
    gpio_init(BTN_A); gpio_set_dir(BTN_A, GPIO_IN); gpio_pull_up(BTN_A);
    gpio_init(BTN_B); gpio_set_dir(BTN_B, GPIO_IN); gpio_pull_up(BTN_B);
    gpio_init(BTN_C); gpio_set_dir(BTN_C, GPIO_IN); gpio_pull_up(BTN_C);

    bool r_on = false, g_on = false, b_on = false;
    bool lastA = true, lastB = true, lastC = true;
    absolute_time_t lastA_t = 0, lastB_t = 0, lastC_t = 0;

    while (true) {
        bool vA = gpio_get(BTN_A);
        bool vB = gpio_get(BTN_B);
        bool vC = gpio_get(BTN_C);
        absolute_time_t now = get_absolute_time();

        // A → vermelho
        if (!vA && lastA) {
            if (absolute_time_diff_us(lastA_t, now) >= DEBOUNCE_MS * 1000) {
                r_on = !r_on;
                gpio_put(PIN_R, r_on);
                lastA_t = now;
            }
        }
        lastA = vA;

        // B → azul
        if (!vB && lastB) {
            if (absolute_time_diff_us(lastB_t, now) >= DEBOUNCE_MS * 1000) {
                b_on = !b_on;
                gpio_put(PIN_B, b_on);
                lastB_t = now;
            }
        }
        lastB = vB;

        // C → verde
        if (!vC && lastC) {
            if (absolute_time_diff_us(lastC_t, now) >= DEBOUNCE_MS * 1000) {
                g_on = !g_on;
                gpio_put(PIN_G, g_on);
                lastC_t = now;
            }
        }
        lastC = vC;

        sleep_ms(2); // pequena folga para CPU
    }
}