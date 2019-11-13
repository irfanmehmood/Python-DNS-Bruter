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

    @abstractmethod
    def run(self, recursive=False, torred=True):
        pass

    @abstractmethod
    def save_to_mongo(self):
        pass



class Amass(DnsScannerInterface):

    def run(self, recursive=False, torred=True):

        # Build our command line vars
        recursive_subdomain_scan_flag = ' -norecursive' if recursive else ''
        domain_flag = ' -d ' + self.root_domain
        domain_list = ''
        nocheck = ' -n' if torred else ''
        threads = ' -t 4'
        show_ip_flag = ' -ip'

        # Dictionay file location
        subdomains_dictionary_file = ' -w subdomain-dictionary.txt'

        # Create our output file
        time_text = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        self.output_file = self.app_slug_output_dir_domain + '/' + time_text + '.txt'
        subdomains_found_output_file = ' -o ' + self.output_file

        

        #build our command line string from vars
        args = (show_ip_flag + domain_flag + recursive_subdomain_scan_flag + subdomains_found_output_file)
        
        print ("STARTING amass")
        print ("[# '-d', '--domain']" + domain_flag)
        print ("[# '-l', '--list']" + domain_list)
        print ("[# '-w', '--wordlist']" + subdomains_dictionary_file)
        print ("[# -o', '--output']" + subdomains_found_output_file)
        print ("[# '-t', '--threads']" + threads)
        print ("[# '-r', '--recursive']" + recursive_subdomain_scan_flag)
        print (hr)

        #run our command
        command = 'amass enum -ip ' + args
        os.system(command)

        return

    def save_to_mongo(self, domain, scanner_log_file):
        # Read data from amass output file
        with open(scanner_log_file, 'r') as file:
            results_output = file.read()
        #print (results_output)
        # Once finished, format results into something we can work with
        extracted_lines = self.extract_from_results(scanner_log_file)

        # Once finished, format results into something we can work with
        domains_ips = self.results_to_domain_ip_list(extracted_lines, joined=True, ip=False)

        # Once finished, format results into something we can work with
        domains = self.results_to_domain_ip_list(extracted_lines, joined=False, ip=False)

        # Once finished, format results into something we can work with
        ips = self.results_to_domain_ip_list(extracted_lines, joined=False, ip=True)

        # Creat a new scan row and gets its ID
        return db.scan_add_result(domain, 
            self.app_slug, 
            results_output, 
            domains_ips.sort(),
            domains.sort(), 
            ips.sort(), 
            scanner_log_file, 
            datetime.datetime.utcnow())


    def extract_from_results(self, filepath):
        data_line = []
        start_after_this_line = '[*] Scanning '
        collect_line = False
        # Now from found subdomains create new scan record
        with open(filepath) as file:
            for line in file:
                if collect_line:
                    data_line.append(line.rstrip('\n').lower())
                # We need to check it only once to set it as True
                if start_after_this_line in line:
                    collect_line = True
                
        #print (data_line)
        return data_line


    def results_to_domain_ip_list(self, extracted_lines, joined=True, ip=True):
        info_list = []

        for line in extracted_lines:
            data = line.split(" - ")
            if joined:
                info_list.append(data[1]+":"+data[0])
            else:  
                if ip:
                    info_list.append(data[0])
                else:
                    info_list.append(data[1])
                
        return info_list