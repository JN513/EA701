#include <stdio.h>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();
    const int N = 10000;
    static uint8_t buf[10000];

    sleep_ms(5000);

    printf("Hello, World!\n");

    absolute_time_t t0 = get_absolute_time();
    for (int i = 0; i < N; i++) buf[i] = i & 0xFF;
    absolute_time_t t1 = get_absolute_time();

    int64_t us = absolute_time_diff_us(t0, t1);
    printf("RAM write (%d bytes): %.3f ms\n", N, us/1000.0);

    while (1) tight_loop_contents();
}
// RAM write (10000 bytes): 0.001 ms
// RAM write (10000 bytes): 0.001 ms
// RAM write (10000 bytes): 0.001 ms