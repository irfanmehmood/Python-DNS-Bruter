import os
from mongo import Db
import sys
from time import gmtime, strftime
import datetime
import helper

hr = '-' * 55
db = Db()
CWD = os.path.dirname(os.path.realpath(__file__))

class Amass():

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
        self.output_file = self.app_slug_output_dir_domain + '/' + root_domain + '.txt'

    def enum_command_by_mode(self, recursive, mode):

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
        
        
        return amass_cmd

    def run_scan(self, recursive=False, mode='passive'):
        exist = db.amass_scan_exist(self.root_domain)
        if (exist):
            print ("[AMASS] domain has been scanned [" + self.root_domain + "]")
            print(hr) 
        else:
            command_list = self.enum_command_by_mode(recursive, mode)
            command = ' '.join([str(elem) for elem in command_list])
            print (command)
            os.system(command)
            self.save_to_mongo(self.root_domain, self.output_file)
        return

    def save_to_mongo(self, domain, scanner_log_file):
        
        extracted_lines = []
        # Now from found subdomains create new scan record
        with open(scanner_log_file) as file:
            for line in file:
                temp_line = line.rstrip('\n').lower()
                extracted_lines.append(temp_line)
                

        # Once finished, format results into something we can work with
        domains = self.results_to_domain_ip_list(extracted_lines, ip=False)
        domains.sort()
        
        #print (domains)
        # Once finished, format results into something we can work with
        ips = self.results_to_domain_ip_list(extracted_lines,  ip=True)
        ips.sort()

    
        # Creat a new scan row and gets its ID
        return db.amass_add_scan(domain, 
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
                        ok = helper.if_subdomain_valid_clean_it(self.root_domain, data[0])
                        if ok:
                            print (data[0])
                            info_list.append(ok)
                            print (ok)

                    else:
                        ok = helper.if_subdomain_valid_clean_it(self.root_domain, data)
                        if ok:
                            info_list.append(ok)
        return info_list



    def get_all_found_subdomains_lists_for_domain(self, root_domain):
        each_scan_domains = []
        results = db.amass_scans_by_subdomain(root_domain)
        for result in results:
            each_scan_domains.append(result['found_subdomains'])
        return each_scan_domains

    def get_all_found_ip_lists_for_domain(self, root_domain):
        each_scan_ips = []
        results = db.amass_scans_by_subdomain(root_domain)
        for result in results:
            each_scan_ips.append(result['found_ips'])
        return each_scan_ips
