#include <stdio.h>
#include "pico/stdlib.h"

#define R_PIN 13
#define G_PIN 11
#define B_PIN 12


int main(){
    stdio_init_all();

    printf("Hello, World!\n");

    gpio_init(R_PIN);
    gpio_init(G_PIN);
    gpio_init(B_PIN);
    gpio_set_dir(R_PIN, GPIO_OUT);
    gpio_set_dir(G_PIN, GPIO_OUT);
    gpio_set_dir(B_PIN, GPIO_OUT);

    gpio_put(R_PIN, 0);
    gpio_put(G_PIN, 0);
    gpio_put(B_PIN, 0);

    while (true) {
        printf("Hello, World!\n");
        gpio_put(B_PIN, 1);
        sleep_ms(500);
        gpio_put(B_PIN, 0);
        sleep_ms(500);
    }
}