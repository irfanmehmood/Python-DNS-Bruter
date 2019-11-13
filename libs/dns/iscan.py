import os
from mongo import Db
import sys
from time import gmtime, strftime
import datetime
hr = '-' * 55
db = Db()

def load_scanners(root_domain):
    return [Amass(root_domain)]


from abc import ABC, abstractmethod

class DnsScannerInterface(ABC):

    def __init__(self, root_domain):

        self.root_domain = root_domain
        self.path = os.getcwd()

        # Build our directory paths
        self.app_slug = self.__class__.__name__
        self.app_slug_output_dir = self.path + '/libs/dns/scan-output/' + self.app_slug
        self.app_slug_output_dir_domain = self.app_slug_output_dir + '/' + self.root_domain

        # Create out output directories
        try:
            if os.path.isdir(self.app_slug_output_dir_domain) == False:
                os.makedirs(self.app_slug_output_dir_domain)
        except OSError:
            print ("Creation of the directory [%s] failed" % self.app_slug_output_dir_domain)
            print (OSError)
            sys.exit()
        else:
            print ("Successfully created the directory [%s] " % self.app_slug_output_dir_domain)
            print (hr)

        # Set output file
        time_text = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        self.output_file = self.app_slug_output_dir_domain + '/' + time_text + '.txt'

    @abstractmethod
    def run(self, recursive=False, torred=True):
        pass

    @abstractmethod
    def save_to_mongo(self):
        pass



class Amass(DnsScannerInterface):

    def enum_command_by_mode(self, recursive, mode):

        # Build our command line vars
        time_text = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        self.output_file = self.app_slug_output_dir_domain + '/' + time_text + '.txt'

        #! -ip & -passive do not work together
        #* amass enum --passive -d <DOMAIN>
        #* amass enum --active -d <DOMAIN> -p 80,443,8080
        #--include-unresolvable	Output DNS names that did not resolve
        #-list	Print the names of all available data sources
        #-noalts	Disable generation of altered names
        #-src	Print data sources for the discovered names
        #-w	Path to a different wordlist file	amass enum -brute -w wordlist.txt -d example.com


        if (mode == 'passive'):
            amass_cmd = [
                'amass', 
                'enum',
                '' if recursive else '-norecursive', 
                '-d', self.root_domain,
                '-passive',
                '-o', self.output_file
            ]
        elif (mode == 'active'):
            amass_cmd = [
                'amass', 
                'enum',
                '' if recursive else '-norecursive', 
                '-d', self.root_domain,
                '-ip',
                '-o', self.output_file
            ]
        
        resolvers_file = self.path + '/libs/dns/resolvers.txt'
        #print (subdomains_dictionary_file)
        #amass_cmd.append('-src')
        amass_cmd.append('-include-unresolvable')
        #amass_cmd.append('-brute -min-for-recursive 3 -w ' + subdomains_dictionary_file) 
        amass_cmd.append('-max-dns-queries 100')
        #amass_cmd.append('-public-dns') 
        amass_cmd.append('-rf ' + resolvers_file)
        
        
        
        return amass_cmd

    def run(self, recursive=False, mode='passive'):

        command_list = self.enum_command_by_mode(recursive, mode)

        command = ' '.join([str(elem) for elem in command_list])
        print (command)
        os.system(command)

        return

    def save_to_mongo(self, domain, scanner_log_file):
        
        extracted_lines = []
        # Now from found subdomains create new scan record
        with open(scanner_log_file) as file:
            for line in file:
                extracted_lines.append(line.rstrip('\n').lower())

        # Once finished, format results into something we can work with
        domains = self.results_to_domain_ip_list(extracted_lines, ip=False)
        
        print (domains)
        # Once finished, format results into something we can work with
        ips = self.results_to_domain_ip_list(extracted_lines,  ip=True)

    
        # Creat a new scan row and gets its ID
        return db.scan_add_result(domain, 
            self.app_slug, 
            extracted_lines,
            domains, 
            ips, 
            os.path.basename(scanner_log_file), 
            datetime.datetime.utcnow())





    def results_to_domain_ip_list(self, extracted_lines,ip=True):
        info_list = []

        for line in extracted_lines:
            
            if ip:
                    data = line.split(" ")
                    #In passive scan amass does not return IP address
                    if (len(data) > 0 and len(data) > 1):
                        info_list.append(data[1])
            else:
                    data = line.split(" ")
                    #In passive scan amass does not return IP address
                    if (len(data) > 0):
                        info_list.append(data[0])
                    else:
                        info_list.append(data)
                    
                
                
        return info_list