import os
from mongo import Db
import sys
from time import gmtime, strftime
import datetime
PATH = os.getcwd()
hr = '-' * 55

def generate_subdomains():
    domains_list = list()
    domains_list_duplicates = list()

    # This is the dir which holds our subdomains
    path = PATH + '/libs/dns/sub-domains-list'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file and 'subdomain-dictionary.txt' not in file and 'test' not in file:
                print ("[" + file + "] MERGED")
                with open(os.path.join(r, file)) as domian_names_file:
                    for line in domian_names_file:
                        domain = line.rstrip('\n').lower()
                        if domain in domains_list:
                            #print (domain + ":exits")
                            domains_list_duplicates.append(domain)
                        else:
                            domains_list.append(domain)

    # Sort our list fo subdomains alphabatically
    domains_list.sort()

    # Write out merged file
    with open(path + '/subdomain-dictionary.txt', 'w') as f:
        for item in domains_list:
            f.write("%s\n" % item)

    print ("[subdomain-dictionary.txt]>> GENERATED")
    print ("[" + str(len(domains_list_duplicates)) + "]>> SUBDOMAINS  Duplicates Removed")
    print ("[" + str(len(domains_list)) + "]>> SUBDOMAINS In Dictionary")


def merge_lists_remove_duplicates(lists):

    non_duplicate_list = []

    for l in lists:
        for ll in l:
            if ll not in non_duplicate_list:
                non_duplicate_list.append(ll)


    return non_duplicate_list


def merge_lists_remove_duplicates_and_find_ips(lists):

    non_duplicate_list = []

    for l in lists:
        for ll in l:
            if ll not in non_duplicate_list:
                get_ip_address_from_amass_line(ll, non_duplicate_list)


    return non_duplicate_list


def if_subdomain_valid_clean_it(ok_domain, domain_to_check):
    # Remove empty line
    domain_to_check = domain_to_check.rstrip('\n').lower()

    if domain_to_check.endswith(ok_domain):
         #! Sometimes you get this in domain names in amass scan, just removing it, dont know what it does
        domain_to_check = domain_to_check.strip('c-domain__target--')
        domain_to_check = domain_to_check.strip('www.')
        return domain_to_check
    else:
        return False

def get_ip_address_from_amass_line(line, ip_list):
    ips = line.split(",")
    for ip in ips:
        if ":" in ip:
            print ('illegal ip:' + ip)
        else:
            if ip not in ip_list:
                ip_list.append(ip)


   

