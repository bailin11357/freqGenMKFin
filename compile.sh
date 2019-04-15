#!/bin/sh

sudo gcc -Wall -O4 -o freq_pi_oh1 freq_pi_oh1.c -std=gnu99 -lm


sudo cp freq_pi_oh1 /usr/local/bin/
