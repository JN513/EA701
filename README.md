# EA701

Repositorio da disciplina **EA701 - Introdução a Sistemas Embarcados**
FEEC / Unicamp

## Pico Tool - Comandos

### Mostrar informações do Pi Pico

```bash
picotool info -a
```

### Carregar arquivo UF2 no Pi Pico

```bash
picotool load <project_name>.uf2
```

Com a opção `-f`, o Pico é colocado automaticamente em modo **BOOTSEL** antes do carregamento, e após o `load` ele retorna para o modo de aplicação:

```bash
picotool load <project_name>.uf2 -f
```

# Roda o código Micropython no Pi Pico

```bash
sudo mpremote a0 run templates/micropython/main.py
```

## Dependências:

- pico-sdk
- picotool
- micropython
- micropython-mpremote