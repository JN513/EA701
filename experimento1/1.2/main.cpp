#include <stdio.h>
#include "pico/stdlib.h"

#define R_PIN 13
#define G_PIN 11
#define B_PIN 12

typedef struct
{
    int r;
    int g;
    int b;

    void set(int red, int green, int blue) {
        r = red;
        g = green;
        b = blue;
    }

    void init_gpios() {
        gpio_init(r);
        gpio_init(g);
        gpio_init(b);
        gpio_set_dir(r, GPIO_OUT);
        gpio_set_dir(g, GPIO_OUT);
        gpio_set_dir(b, GPIO_OUT);
    }

    void acende_todos() {
        gpio_put(r, 1);
        gpio_put(g, 1);
        gpio_put(b, 1);
    }

    void apaga_todos() {
        gpio_put(r, 0);
        gpio_put(g, 0);
        gpio_put(b, 0);
    }
} Cor_t;


int main(){
    stdio_init_all();

    printf("Hello, World!\n");

    Cor_t cor;
    cor.set(R_PIN, G_PIN, B_PIN);
    cor.init_gpios();
    cor.apaga_todos();

    sleep_ms(10000);

    cor.acende_todos();

    sleep_ms(10000);

    cor.apaga_todos();

    while (true) {
        printf("Hello, World!\n");
        gpio_put(cor.b, 1);
        sleep_ms(500);
        gpio_put(cor.b, 0);
        sleep_ms(500);
    }
}