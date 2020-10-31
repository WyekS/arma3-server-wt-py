#!/bin/bash
# Tipo de update: 1 todo, 2 solo instancia/s, 3 solo mods
P1=$1

# Steam user/pass
P2=$2
P3=$3

echo "Starting update server Arma..."

cd /opt/update_arma
if test -f update.log; then
    rm update.log
fi
touch update.log && chown arma3hc:arma3hc update.log && /usr/bin/python3 /opt/update_arma/upwolf.py $P1 $P2 $P3
