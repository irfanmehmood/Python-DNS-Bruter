

import os

ip_address = list()
domain_name = list()

with open('appcheck-ng.com-output.txt') as lines:
        for line in lines:
           line = line.rstrip('\n').lower()
           #print (line)
           data = line.split(" - ")
           print (data[0])