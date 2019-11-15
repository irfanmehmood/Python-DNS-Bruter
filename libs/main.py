

import os
import sys
import subprocess



# SET PATH for our libs/classes
CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD + '/')
sys.path.append(CWD + '/dns')

import dns.helper
from dns.amass import Amass
from dns.dnscan import Dnscan
subprocess.call('clear', shell=True)
PATH = os.getcwd()
DNS_SCANNERS = []
hr = '-' * 55

def show_splash_screen():
        print (hr)
        print ('Merge your domains into a text file')
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
    #input_domain = 'appcheck-ng.com'


    # Generate subdomains dictionary
    dns.helper.generate_subdomains()

    # Save Scan Info to Database
    Amass = Amass(input_domain)
    Amass.run_scan(True, 'active')

    # All sub domains found for this by all Amass scans for this domain 
    ALL_AMASS_FOUND_SUBDOMAINS = Amass.get_all_found_subdomains_lists_for_domain(input_domain)

    # All sub domains found for this by all Amass scans for this domain 
    ALL_AMASS_FOUND_IPS = Amass.get_all_found_ip_lists_for_domain(input_domain)

    #* Remove all Duplicates
    ALL_AMASS_FOUND_IPS = dns.helper.merge_lists_remove_duplicates_and_find_ips(ALL_AMASS_FOUND_IPS)

    print (ALL_AMASS_FOUND_IPS)

    sys.exit()

    #* Remove all Duplicates
    ALL_AMASS_FOUND_SUBDOMAINS = dns.helper.merge_lists_remove_duplicates(ALL_AMASS_FOUND_SUBDOMAINS)

    #! NOW GET DNSCAN TO BRUTE FORCE root_domain
    Dnscan = Dnscan(input_domain)
    Dnscan.brute_force_subdomains(input_domain)

    #! NOW MERGE AMASS + DNSCAN subdomains, so we get a final list of subdomains to Brute
    # All sub domains found for this by all Amass scans for this domain 
    ALL_DNSCAN_INITIAL_SUBDOMAINS = Dnscan.get_domain_subdomains(input_domain)

     #* Remove all Duplicates from DNMASSS initial subdomains
    ALL_DNSCAN_INITIAL_SUBDOMAINS = dns.helper.merge_lists_remove_duplicates(ALL_DNSCAN_INITIAL_SUBDOMAINS)

    #* Remove all Duplicates from DNMASSS + AMASS merge
    FINAL_MERGED_SUBDOMAINS_LIST = dns.helper.merge_lists_remove_duplicates([
        ALL_AMASS_FOUND_SUBDOMAINS, ALL_DNSCAN_INITIAL_SUBDOMAINS]
    )

    #* Remove all Duplicates
    print ("[Amass] Found Sub Domains: " + str(len(ALL_AMASS_FOUND_SUBDOMAINS)))
    print ("[Dnmass] Brute Sub Domains For Root Domain : " + str(len(ALL_DNSCAN_INITIAL_SUBDOMAINS)))
    print ("Final Domains : " + str(len(FINAL_MERGED_SUBDOMAINS_LIST)))

    for d in FINAL_MERGED_SUBDOMAINS_LIST:
        Dnscan.brute_force_subdomains(d)

elif (choice == 2):
    print (hr)
    print ('Generating subdomains, merged your subdomains directory')
    print (hr)
    idnscan.generate_subdomains(root_domain, recursive=False, torred=True)
else:
    print ('bye')




