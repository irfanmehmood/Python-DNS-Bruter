

import os
import sys
import subprocess
import idnscan
import iamass
subprocess.call('clear', shell=True)
PATH = os.getcwd()


def show_splash_screen():
        print (hr)
        print ('1. Attack Domain')
        print ('2. Merge your domains into a text file')
        print (hr)



hr = '-' * 55
show_splash_screen()

#choice = input("Enter a Choice: ")
#choice = int(choice)
choice = 1

if (choice == 1):
    print (hr)
    #input_domain = str(input ("Enter domain: "))
    #input_domain = 'jainuniversity.ac.in'
    #input_domain = 'vu.edu.pk'
    input_domain = 'tagww.com'
    print (hr)
    print ("1. Merging Subdomains into [subdomain-dictionary.txt] for [" + input_domain + "] Domain")
    print (hr)
    idnscan.generate_subdomains()
    print (hr)
    print ('2. Running GITHUB:DNSCAN :' + input_domain)
    print (hr)
    #idnscan.run_dnscan(input_domain)
    print (hr)
    print ('3. Running GITHUB:AMASS :' + input_domain)
    print (hr)
    iamass.run_amass(input_domain)
elif (choice == 2):
    print (hr)
    print ('Generating subdomains, merged your subdomains directory')
    print (hr)
    idnscan.generate_subdomains()
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




