#include "pico/stdlib.h"
#include "hardware/flash.h"
#include "hardware/sync.h"
#include <stdio.h>
#include <string.h>

#define FLASH_TARGET_OFFSET (256 * 1024)  // ajuste conforme sua imagem
#define SECTOR_SIZE FLASH_SECTOR_SIZE     // tip. 4096
#define PAGE_SIZE FLASH_PAGE_SIZE         // tip. 256

uint8_t WRBUF[PAGE_SIZE];

int main() {
    stdio_init_all();
    sleep_ms(500); // dá tempo para conectar terminal

    // Preenche buffer
    for (int i=0;i<PAGE_SIZE;i++) WRBUF[i] = i & 0xFF;
    // --- mede ERASE de 1 setor ---
    absolute_time_t t0 = get_absolute_time();
    uint32_t ints = save_and_disable_interrupts();
    flash_range_erase(FLASH_TARGET_OFFSET, SECTOR_SIZE);
    restore_interrupts(ints);
    absolute_time_t t1 = get_absolute_time();

    double erase_ms = absolute_time_diff_us(t0, t1)/1000.0;
    printf("Flash ERASE (setor %d bytes): %.3f ms\n", SECTOR_SIZE, erase_ms);

    // --- mede PROGRAM de 1 página ---
    t0 = get_absolute_time();
    ints = save_and_disable_interrupts();
    flash_range_program(FLASH_TARGET_OFFSET, WRBUF, PAGE_SIZE);
    restore_interrupts(ints);
    t1 = get_absolute_time();

    double prog_ms = absolute_time_diff_us(t0, t1)/1000.0;
    printf("Flash PROGRAM (pagina %d bytes): %.3f ms\n", PAGE_SIZE, prog_ms);

    // --- mede PROGRAM de bloco maior (ex. 32 KB) ---
    const int TOTAL = 32 * 1024;
    static uint8_t bigbuf[32*1024];
    for (int i=0;i<TOTAL;i++) bigbuf[i] = i & 0xFF;

    // precisa apagar setor(es) correspondente(s) antes se for regravar
    ints = save_and_disable_interrupts();
    flash_range_erase(FLASH_TARGET_OFFSET, SECTOR_SIZE * 8); // 8*4KB = 32KB
    restore_interrupts(ints);

    t0 = get_absolute_time();
    ints = save_and_disable_interrupts();
    for (int off=0; off<TOTAL; off+=PAGE_SIZE)
        flash_range_program(FLASH_TARGET_OFFSET + off, bigbuf + off, PAGE_SIZE);
    restore_interrupts(ints);
    t1 = get_absolute_time();

    double big_prog_ms = absolute_time_diff_us(t0, t1)/1000.0;
    printf("Flash PROGRAM (32KB): %.3f ms\n", big_prog_ms);
    
    while (1) tight_loop_contents();
}