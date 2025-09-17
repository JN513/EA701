#include <stdio.h>
#include "pico/stdlib.h"
// For ADC input:
#include "hardware/adc.h"
#include "hardware/dma.h"



#define BUTTON_PIN 5


// Channel 0 is GPIO26
#define CAPTURE_CHANNEL 2
#define CAPTURE_DEPTH 60000

uint16_t capture_buf[CAPTURE_DEPTH];


int main() {
    stdio_init_all();

    sleep_ms(5000); // dá tempo para conectar terminal
    printf("Pressione o botão para iniciar a captura...\n");

    gpio_init(BUTTON_PIN);
    gpio_set_dir(BUTTON_PIN, false);
    gpio_pull_up(BUTTON_PIN);


    // Init GPIO for analogue use: hi-Z, no pulls, disable digital input buffer.
    adc_gpio_init(26 + CAPTURE_CHANNEL);


    adc_init();
    adc_select_input(CAPTURE_CHANNEL);
    adc_fifo_setup(
        true,    // Write each completed conversion to the sample FIFO
        true,    // Enable DMA data request (DREQ)
        1,       // DREQ (and IRQ) asserted when at least 1 sample present
        false,   // We won't see the ERR bit because of 8 bit reads; disable.
        false     // Shift each sample to 8 bits when pushing to FIFO
    );


    adc_set_clkdiv(1200);


    printf("Arming DMA\n");
    sleep_ms(1000);
    // Set up the DMA to start transferring data as soon as it appears in FIFO
    uint dma_chan = dma_claim_unused_channel(true);
    dma_channel_config cfg = dma_channel_get_default_config(dma_chan);


    // Reading from constant address, writing to incrementing byte addresses
    channel_config_set_transfer_data_size(&cfg, DMA_SIZE_16);
    channel_config_set_read_increment(&cfg, false);
    channel_config_set_write_increment(&cfg, true);


    // Pace transfers based on availability of ADC samples
    channel_config_set_dreq(&cfg, DREQ_ADC);


    dma_channel_configure(dma_chan, &cfg,
        capture_buf,    // dst
        &adc_hw->fifo,  // src
        CAPTURE_DEPTH,  // transfer count
        true            // start immediately
    );


while (gpio_get(BUTTON_PIN) == 1) {
    tight_loop_contents(); // função de espera "educada"
}


    printf("Gravando...\n");
    adc_run(true);


    // Once DMA finishes, stop any new conversions from starting, and clean up
    // the FIFO in case the ADC was still mid-conversion.
    dma_channel_wait_for_finish_blocking(dma_chan);
    printf("Gravação encerrada.\n");
    adc_run(false);
    adc_fifo_drain();


    // Print samples to stdout so you can display them in pyplot, excel, matlab
    /*for (int i = 0; i < CAPTURE_DEPTH; ++i) {
        printf("%-3d, ", capture_buf[i]);
    }*/

    
}
