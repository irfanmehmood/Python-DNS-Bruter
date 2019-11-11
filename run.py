

import os
import sys
import subprocess
import subdomains
subprocess.call('clear', shell=True)
PATH = os.getcwd()


def show_splash_screen():
        print (hr)
        print ('1. Attack Domain')
        print ('2. Merge your domains into a text file')
        print (hr)

def run_dnscan(domain, recursive=False, torred=True):
        #sys.exit()
        recursive_flag = ' -r' if recursive else ''
        domain_flag = ' -d ' + domain
        domain_list = ''
        nocheck = ' -n' if torred else ''
        threads = ' -t 4'

        subdomains_dictionary_file = ' -w ' + PATH + '/sub-domains-list/subdomain-dictionary.txt'
        subdomains_found_output_file = ' -o ' + PATH + '/scan_output/ ' + domain + '-output.txt'
        args = (recursive_flag 
            + threads
            + domain_flag 
            + domain_list
            + subdomains_dictionary_file
            + nocheck)
        
        print ("STARTING DNSCAN")
        print ("[# '-d', '--domain']" + domain_flag)
        print ("[# '-l', '--list']" + domain_list)
        print ("[# '-w', '--wordlist']" + subdomains_dictionary_file)
        print ("[# '-t', '--threads']" + threads)
        print ("[# '-r', '--recursive']" + recursive_flag)
        print ("[# '-n', '--nocheck']" + nocheck)
        print (hr)

        os.system('python3 vendors/dnscan/dnscan.py' + args)

hr = '-' * 55
show_splash_screen()

choice = input("Enter a Choice: ")
choice = int(choice)

if (choice == 1):
    print (hr)
    #input_domain = str(input ("Enter domain: "))
    input_domain = 'appcheck-ng.com'
    print (hr)
    print ("1. Merging Subdomains into [subdomain-dictionary.txt] for [" + input_domain + "] Domain")
    print (hr)
    subdomains.generate_subdomains()
    print (hr)
    print ('2. Running GITHUB:DNSCAN :' + input_domain)
    print (hr)
    run_dnscan(input_domain)
elif (choice == 2):
    print (hr)
    print ('Generating subdomains, merged your subdomains directory')
    print (hr)
    subdomains.generate_subdomains()
else:
    print ('bye')


# -6', '--ipv6', help='Scan for AAAA records', action="store_true", dest='ipv6', required=False, default=False)
# -z', '--zonetransfer', action="store_true", default=False, help='Only perform zone transfers', dest='zonetransfer', required=False)
# -R', '--resolver', help="Use the specified resolver instead of the system default", dest='resolver', required=False)
# -T', '--tld', action="store_true", default=False, help="Scan for TLDs", dest='tld', required=False)
# -o', '--output', help="Write output to a file", dest='output_filename', required=False)
# -i', '--output-ips',   help="Write discovered IP addresses to a file", dest='output_ips', required=False)
# -D', '--domain-first', action="store_true", default=False, help='Output domain first, rather than IP address', dest='domain_first', required=False)
# -v', '--verbose', action="store_true", default=False, help='Verbose mode', dest='verbose', required=False)
# -n', '--nocheck', action="store_true", default=False, help='Don\'t check nameservers before scanning', dest='nocheck', required=False)




