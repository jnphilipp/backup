#!/bin/bash

sudo apt-get install python-configparser

sudo cp psync /usr/bin/psync
sudo chmod +x /usr/bin/psync

MESSAGE="psync install completed."
echo $MESSAGE