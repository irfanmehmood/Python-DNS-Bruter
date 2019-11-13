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