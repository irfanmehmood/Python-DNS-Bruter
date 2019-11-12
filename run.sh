#!/bin/bash 

#Create our mongo instance, if not running already
name='mongoDb'

[[ $(sudo docker ps -f "name=$name" --format '{{.Names}}') == $name ]] ||
sudo docker run -d -p 27017:27017 --name $name mongo:latest

sudo apt-get install python-pip

sudo python3 -m pip install pymongo

python3 main.py

#amass viz -d3

#amass viz -d3
