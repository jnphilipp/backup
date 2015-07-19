#!/bin/bash

sudo apt-get install python3-gi rsync tar

sudo cp psync /usr/bin/psync
sudo cp psync.xsd /usr/share/psync/psync.xsd
sudo chmod +x /usr/bin/psync

MESSAGE="psync install completed."
echo $MESSAGE
