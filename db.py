import os
import config
from pymongo import MongoClient

class Db:

    # node which is connecting, setup for multiple
    DbConnect = False

    def __init__(self):
        # node unique ip, which is connecting
        self.nodeIP = config.node['IP']
        # This should be the centeral db server
        client = MongoClient('127.0.0.1:27017')
        self.DbConnect = client.Recon

    def page_add(self, job_id, job_url, status_code, page_html, page_path, page_full_path):
        return self.DbConnect.subdomains.insert({
            "job_id" : job_id,
            'job_url' : job_url,
            "status_code" : status_code,
            "page_html" : page_html,
            "page_path": page_path,
            "page_full_path" : page_full_path,
            "attack_complete": 0,
            "scan_complete": 0,
            "exploits_found": 0,
            "exploit_payloads_found" : '',
            "exploit_payload_response" : '',
            "exploit_payload_response_mini" : '',
            "node_ip": self.nodeIP
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
