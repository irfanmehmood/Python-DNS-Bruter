#!/bin/bash 

name='mongoDb'

#Create our docker mongo instance, if not running already
[[ $(sudo docker ps -f "name=$name" --format '{{.Names}}') == $name ]] ||
sudo docker run -d -p 27017:27017 --name $name mongo:latest

# Install Pip and libs
sudo apt-get install python-pip
sudo python3 -m pip install pymongo

# Install DNS Amass
sudo apt-get install amass

# Tor ghost
# sudo apt-get install tor -y -qq
# sudo pip install stem
# git clone git@github.com:irfanmehmood/torghost.git vendor/torghost
# chmod +x vendor/torghost/torghost

# Tor ghost always switch IP
sudo vendor/torghost/torghost start
sudo vendor/torghost/torghost switch

dnsenum --dnsserver 128.52.130.209 --noreverse --enum  vu.edu.pk -f /home/iffy/irfan/Documents/Python/Python-DNS-Bruter/libs/dns/sub-domains-list/subdomain-dictionary.txt


#python3 libs/main.py

#amass viz -d3

#amass viz -d3
