#include "pico/stdlib.h"
#include "hardware/flash.h"
#include "hardware/sync.h"
#include <string.h>
#include <stdint.h>

#define LED 13
#define FLASH_TARGET_OFFSET (256 * 1024) // ajuste: área fora do firmware/FS
#define PAGE_SIZE FLASH_PAGE_SIZE        // 256 bytes
#define SECTOR_SIZE FLASH_SECTOR_SIZE    // 4096 bytes

// Estrutura simples com "assinatura" e estado
typedef struct {
    uint32_t magic;    // 0xA5A5A5A5
    uint32_t version;  // 1
    uint8_t  led_state;// 0/1
    uint8_t  rsv[PAGE_SIZE - 9]; // padding até 256 B
} __attribute__((packed)) cfg_page_t;

static const uint8_t *flash_ptr = (const uint8_t*)(XIP_BASE + FLASH_TARGET_OFFSET);

int main(void) {
    stdio_init_all();
    gpio_init(LED); gpio_set_dir(LED, GPIO_OUT);

    // Lê página atual
    const cfg_page_t *current = (const cfg_page_t*)flash_ptr;
    uint8_t state = (current->magic == 0xA5A5A5A5 && current->version == 1) ? current->led_state : 0;
    gpio_put(LED, state);

    // Alterna estado e prepara página
    state = !state;
    cfg_page_t page = {0};
    page.magic = 0xA5A5A5A5;
    page.version = 1;
    page.led_state = state;

    // Apaga setor e programa 1 página (256 B)
    uint32_t ints = save_and_disable_interrupts();
    flash_range_erase(FLASH_TARGET_OFFSET, SECTOR_SIZE);
    flash_range_program(FLASH_TARGET_OFFSET, (const uint8_t*)&page, PAGE_SIZE);
    restore_interrupts(ints);

    // Aplica novo estado
    gpio_put(LED, state);
    while (1) tight_loop_contents();
}