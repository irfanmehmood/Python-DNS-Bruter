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

    def scan_add_result(self, root_domain, scanner_slug, scanner_command, scanner_results, scanner_results_filename, scan_datetime):
        return self.DbConnect.scans.insert({
            "root_domain" : root_domain,
            'scanner_slug' : scanner_slug,
            "scanner_command" : scanner_command,
            "scanner_results" : scanner_results,
            "scanner_results_filename" : scanner_results_filename,
            "scan_datetime" : scan_datetime
        })

    def jobs_clear_all_data(self):
        self.DbConnect.job.remove({})
        self.DbConnect.page.remove({})
        self.DbConnect.page_collected_links.remove({})
        self.DbConnect.page_payloads.remove({})


# show dbs
# show databaseName
# use crawlerDb;
# use file_to_scan
