import os
from mongo import Db
import sys
from time import gmtime, strftime
import datetime
import helper

hr = '-' * 55
db = Db()
CWD = os.path.dirname(os.path.realpath(__file__))

class Dnscan():

    def __init__(self, root_domain):

        self.root_domain = root_domain
        self.path = os.getcwd()

        # Build our directory paths
        self.app_slug = self.__class__.__name__
        

    def brute_force_subdomains(self, domain):

        exist = db.dnscan_scan_exist(domain)
        if (exist):
            print ("[DNSCAN] domain has been scanned [" + domain + "]")
            helper.hr()
        else:
            # Create app directory
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
            # Set output files
            self.output_file = self.app_slug_output_dir_domain + '/' + domain + '.txt'
            resolvers_file = self.path + '/libs/dns/resolvers.txt'
            sbdomains_dic_file = self.path + '/libs/dns/sub-domains-list/subdomain-dictionary.txt'
            # IPv6 (AAAA) records found, Try running dnscan with the -6 option
            # Wild card domains found 104.31.79.27, 104.31.78.27
            cmd = [
                'python3', 'vendor/dnscan/dnscan.py',
                '-d', domain,
                '-w', sbdomains_dic_file,
                '-o', self.output_file ,
                '-t', '32',
            ]
            command = ' '.join([str(elem) for elem in cmd])
            print (command)
            os.system(command)

            # Read data from dnscan output file
            with open(self.output_file, 'r') as file:
                results_output = file.read()
            # Once finished, format results into something we can work with
            extracted_lines = self.extract_from_results(self.output_file)
            # Once finished, format results into something we can work with
            domains_ips = self.results_to_domain_ip_list(extracted_lines, joined=True, ip=False)
            # Once finished, format results into something we can work with
            domains = self.results_to_domain_ip_list(extracted_lines, joined=False, ip=False)
            # Once finished, format results into something we can work with
            ips = self.results_to_domain_ip_list(extracted_lines, joined=False, ip=True)
            print("Found" + str(len(domains)))
            print(hr)
            # Creat a new scan row and gets its ID
            scan_id = db.dnscan_add_scan(domain,
                extracted_lines,
                domains, 
                ips, 
                os.path.basename(self.output_file), 
                datetime.datetime.utcnow())
            print ("[" + str(scan_id) + "]: Scan Added To Database")
            print(hr) 

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
                    ok = helper.if_subdomain_valid_clean_it(self.root_domain, data[1])
                    if ok:
                        info_list.append(ok)
                
        return info_list

    def get_domain_subdomains(self, root_domain):
        each_scan_domains = []
        results = db.dnscan_scans_by_subdomain(root_domain)
        for result in results:
            each_scan_domains.append(result['found_subdomains'])
        return each_scan_domains