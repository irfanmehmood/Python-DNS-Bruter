import os
from pymongo import MongoClient

class Db:

    # node which is connecting, setup for multiple
    DbConnect = False

    def __init__(self):
        # node unique ip, which is connecting
        # This should be the centeral db server
        client = MongoClient('127.0.0.1:27017')
        self.DbConnect = client.DnsBuster
        #self.scans_clear_all_data()

    def amass_add_scan(self, start_domain, scan_results, found_subdomains, found_ips, scan_outputfile, scan_datetime):

        return self.DbConnect.Amass.insert({
            "start_domain" : start_domain,
            "scan_results" : scan_results,
            "found_subdomains" : found_subdomains,
            "found_ips" : found_ips, 
            "scan_outputfile" : scan_outputfile,
            "scan_datetime" : scan_datetime
        })

    def amass_scan_exist(self, start_domain):
        find = {
            "start_domain" : start_domain
        }
        result = self.DbConnect.Amass.find_one(find)
        return False if result == None else True

    def amass_scans_by_subdomain(self, start_domain):
        find = {
            "start_domain" : start_domain,
        }
        return list(self.DbConnect.Amass.find(find))

    def dnscan_add_scan(self, 
        start_domain, 
        scan_results, 
        found_subdomains, 
        found_ips, 
        scan_outputfile, 
        scan_datetime):
        
        return self.DbConnect.Dnscan.insert({
            "start_domain" : start_domain,
            "scan_results" : scan_results,
            "found_subdomains" : found_subdomains,
            "found_ips" : found_ips, 
            "scan_outputfile" : scan_outputfile,
            "scan_datetime" : scan_datetime
        })

    def dnscan_scan_exist(self, start_domain):
        find = {
            "start_domain" : start_domain
        }
        result = self.DbConnect.Dnscan.find_one(find)
        return False if result == None else True

    def dnscan_scans_by_subdomain(self, start_domain):
        find = {
            "start_domain" : start_domain,
        }
        return list(self.DbConnect.Dnscan.find(find))

    def scans_clear_all_data(self):
        self.DbConnect.Amass.remove({})
        self.DbConnect.Dnscan.remove({})


# show dbs
# show databaseName
# use crawlerDb;
# use file_to_scan
