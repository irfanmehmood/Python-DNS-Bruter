#!/bin/bash 

#Create our mongo instance, if not running already
name='mongoDb'

[[ $(docker ps -f "name=$name" --format '{{.Names}}') == $name ]] ||
docker run -d -p 27017:27017 --name $name mongo:latest


python3 main.py
