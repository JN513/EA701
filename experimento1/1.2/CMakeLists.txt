cmake_minimum_required(VERSION 3.13)

include("$ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake")

project(main)

pico_sdk_init()

add_executable(main
    main.cpp
    )

# pull in common dependencies
target_link_libraries(main pico_stdlib)

pico_enable_stdio_usb(main 1)

# create map/bin/hex file etc.
pico_add_extra_outputs(main)
