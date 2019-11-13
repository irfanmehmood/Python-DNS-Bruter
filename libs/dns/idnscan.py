import os
from mongo import Db
import sys
from time import gmtime, strftime
import datetime
PATH = os.getcwd()
hr = '-' * 55
db = Db()

def generate_subdomains():
    domains_list = list()
    domains_list_duplicates = list()

    # This is the dir which holds our subdomains
    path = 'sub-domains-list'

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

    #print domains_list

def run_dnscan(domain, recursive=False, torred=True):
    #build our command line vars
    recursive_flag = ' -r' if recursive else ''
    domain_flag = ' -d ' + domain
    domain_list = ''
    nocheck = ' -n' if torred else ''
    threads = ' -t 4'
    app_slug = 'dnscan'
    app_slug_output_dir = PATH + '/scan-output/' + app_slug
    app_slug_output_dir_domain = app_slug_output_dir + '/' + domain
    print (os.path.isdir(app_slug_output_dir_domain))
    # Create out output directories
    try:
        if (os.path.isdir(app_slug_output_dir) == False):
            os.mkdir(app_slug_output_dir)
        if os.path.isdir(app_slug_output_dir_domain) == False:
            os.mkdir(app_slug_output_dir_domain)
    except OSError:
        print ("Creation of the directory %s failed" % PATH)
        sys.exit()
    else:
        print ("Successfully created the directory %s " % PATH)
    
    time_text = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    subdomains_dictionary_file = ' -w ' + PATH + '/sub-domains-list/subdomain-dictionary.txt'
    output_file = app_slug_output_dir_domain + '/' + time_text + '.txt'
    subdomains_found_output_file = ' -o ' + output_file

    #build our command line string from vars
    args = (recursive_flag 
        + threads
        + domain_flag 
        + domain_list
        + subdomains_dictionary_file
        + subdomains_found_output_file
        + nocheck)
    
    print ("STARTING DNSCAN")
    print ("[# '-d', '--domain']" + domain_flag)
    print ("[# '-l', '--list']" + domain_list)
    print ("[# '-w', '--wordlist']" + subdomains_dictionary_file)
    print ("[# -o', '--output']" + subdomains_found_output_file)
    print ("[# '-t', '--threads']" + threads)
    print ("[# '-r', '--recursive']" + recursive_flag)
    print ("[# '-n', '--nocheck']" + nocheck)
    print (hr)

    #run our command
    command = 'python3 vendors/dnscan/dnscan.py' + args
    os.system(command)

    # Read data from dnscan output file
    with open(output_file, 'r') as file:
        results_output = file.read()

    # Once finished, format results into something we can work with
    extracted_lines = extract_from_results(output_file)

    # Once finished, format results into something we can work with
    domains_ips = results_to_domain_ip_list(extracted_lines, joined=True, ip=False)

    # Once finished, format results into something we can work with
    domains = results_to_domain_ip_list(extracted_lines, joined=False, ip=False)

    # Once finished, format results into something we can work with
    ips = results_to_domain_ip_list(extracted_lines, joined=False, ip=True)

    # Creat a new scan row and gets its ID
    scan_id = db.scan_add_result(domain, 
        'dnscan', 
        command , 
        results_output, 
        domains_ips.sort(),
        domains.sort(), 
        ips.sort(), 
        output_file, 
        datetime.datetime.utcnow())
    print ("[" + str(scan_id) + "]: Scan Added To Database")


def extract_from_results(filepath):
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


def results_to_domain_ip_list(extracted_lines, joined=True, ip=True):
    
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