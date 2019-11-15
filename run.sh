#!/bin/bash 

# Clear Screen
clear

#? include our color script
source "$PWD/bscripts/color.cfg"

#? include install script
source "$PWD/bscripts/install.cfg"

#? include the docker script
source "$PWD/bscripts/mongo.cfg"

#Tor ghost always switch IP
#sudo vendor/torghost/torghost stop
#sudo vendor/torghost/torghost switch

#dnsenum --dnsserver 128.52.130.209 --noreverse --enum  vu.edu.pk -f /home/iffy/irfan/Documents/Python/Python-DNS-Bruter/libs/dns/sub-domains-list/subdomain-dictionary.txt

# run our program
python3 libs/main.py