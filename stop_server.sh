#!/bin/bash

USER=$1

su - $USER -c "killall screen"

echo "################# Servidor Arma parado ####################"
