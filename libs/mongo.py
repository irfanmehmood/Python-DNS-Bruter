import os
from pymongo import MongoClient

class Db:

    # node which is connecting, setup for multiple
    DbConnect = False

    def __init__(self):
        # node unique ip, which is connecting
        # This should be the centeral db server
        client = MongoClient('127.0.0.1:27017')
        self.DbConnect = client.Recon
        #self.scans_clear_all_data()

    def scan_add_result(self, root_domain, scanner_slug, scanner_results, found_domains, found_ips, scanner_results_filename, scan_datetime):
        return self.DbConnect.scans.insert({
            "root_domain" : root_domain,
            'scanner_slug' : scanner_slug,
            "scanner_results" : scanner_results,
            "found_domains" : found_domains,
            "found_ips" : found_ips, 
            "scanner_results_filename" : scanner_results_filename,
            "scan_datetime" : scan_datetime
        })

    def scan_get_by_domain_and_application(self, root_domain, scanner_slug):
        find = {
            "root_domain" : root_domain,
            "scanner_slug" : scanner_slug
        }
        return list(self.DbConnect.scans.find(find))

    def scan_exist_for_domain(self, root_domain, scanner_slug):
        find = {
            "root_domain" : root_domain,
            "scanner_slug" : scanner_slug
        }
        result = self.DbConnect.scans.find_one(find)
        return False if result == None else True

    def scans_clear_all_data(self):
        self.DbConnect.scans.remove({})


# show dbs
# show databaseName
# use crawlerDb;
# use file_to_scan
