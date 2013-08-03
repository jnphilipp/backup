#!/bin/bash

sudo apt-get install python-configparser

sudo cp backup /usr/bin/backup
sudo chmod +x /usr/bin/backup

MESSAGE="backup install completed."
echo $MESSAGE