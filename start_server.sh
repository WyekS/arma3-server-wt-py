#!/bin/bash

USER=$1
ALIAS=$2

su - $USER -c "/usr/bin/screen -d -m /opt/wolf_functions/init.sh $ALIAS"
