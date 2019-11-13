

import os
import sys
import subprocess



# SET PATH for our libs/classes
CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD + '/')
sys.path.append(CWD + '/dns')

import helper
import dns.iscan
subprocess.call('clear', shell=True)
PATH = os.getcwd()
DNS_SCANNERS = []
hr = '-' * 55

def show_splash_screen():
        print (hr)
        print ('1. Attack Domain')
        print ('2. Merge your domains into a text file')
        print (hr)

def generate_subdomains_dictionary(input_domain):
        print (hr)
        print ("1. Merging Subdomains into [subdomain-dictionary.txt] for [" + input_domain + "] Domain")
        print (hr)
        helper.generate_subdomains()
        print(hr)

def run_dns_scanners(input_domain):
        print (hr)
        print ('2. Running Scanners for :' + input_domain)
        print (hr)
        for scanner in DNS_SCANNERS:
            recursive=True
            torred=True
            #scanner.run(recursive, 'passive')
            scanner.run(recursive, 'active')

def save_dns_scanners_to_mongo(input_domain):

        for scanner in DNS_SCANNERS:

            all_domains_files = {}
            path = CWD + '/dns/scan-output/' + scanner.app_slug

            for domain in os.listdir(path):
                path = CWD + '/dns/scan-output/' + scanner.app_slug + '/' + domain
                #print (path)
                for file in os.listdir(path):
                    file_path = path + '/' + file
                    if os.path.isfile(file_path):
                        all_domains_files[file_path] = domain
                
            # Now add all these files data to Database
            #scanner.save_to_mongo
            #print (all_domains_files)
            for key in all_domains_files:
                domain = all_domains_files[key]
                filepath = key
                scan_id = scanner.save_to_mongo(domain, filepath)
                #print ("[" + filepath + "]: Scan Added To Database")
                print ("[" + str(scan_id) + "]: Scan Added To Database")
                print(hr)


hr = '-' * 55
show_splash_screen()

#choice = input("Enter a Choice: ")
#choice = int(choice)
choice = 1
if (choice == 1):
    print (hr)
    #input_domain = str(input ("Enter domain: "))
    #input_domain = 'jainuniversity.ac.in'
    input_domain = 'vu.edu.pk'
    #input_domain = 'tagww.com'
    #input_domain = 'appcheck-ng.com'
    DNS_SCANNERS = dns.iscan.load_scanners(input_domain)
    generate_subdomains_dictionary(input_domain)
    run_dns_scanners(input_domain)
    save_dns_scanners_to_mongo(input_domain)
elif (choice == 2):
    print (hr)
    print ('Generating subdomains, merged your subdomains directory')
    print (hr)
    idnscan.generate_subdomains(root_domain, recursive=False, torred=True)
else:
    print ('bye')




