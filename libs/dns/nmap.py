import os
from mongo import Db
import sys
from time import gmtime, strftime
import datetime
import helper
import time

CWD = os.path.dirname(os.path.realpath(__file__))

class Nmap():

    def run_scan(self, root_domain, ips):

        self.root_domain = root_domain
        self.ips = ips
        self.path = os.getcwd()

        self.ips.sort()

        #  -sn: Ping Scan - disable port scan
        for ip in self.ips:
            self.scan_looped_ip(ip)

    def scan_looped_ip(self, ip):
        
            time.sleep(0.2)
            command = 'nmap -sn ' + ip
            print (command)
            os.system(command)
            helper.hr()

