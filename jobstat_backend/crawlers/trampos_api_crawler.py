# -*- coding: utf-8 -*-
import urllib2
import json
import os
import io

from common import check_or_create_save_folder

JOB_PLATFORM = "trampos"
API_URL = 'http://trampos.co/api/v2/opportunities/%s'
SAVE_PATH = '../crawled_data/%s' % JOB_PLATFORM

# Quits after encountering X offers that aren't available or already saved
ACCESS_LIMIT = 200


def get_api_data(url):
    response = urllib2.urlopen(url)
    return json.load(response)


def save_data(data_json, job_id, access_limit):
    file_name = "%s-%s.json" % (JOB_PLATFORM, job_id)
    save_path = SAVE_PATH + '/%s' % file_name

    if not os.path.isfile(save_path):
        with io.open(save_path, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(data_json, sort_keys=True, indent=4, ensure_ascii=False)))
            print'Created file: %s' % file_name
    else:
        print'File already exists: %s' % file_name
        access_limit -= 1

    return access_limit


def crawl_api(api_url, job_id, access_limit):
    data = get_api_data(api_url % job_id)
    if 'status' in data:
        print("%s: %s" % (job_id, data['status']))
        return access_limit - 1
    else:
        return save_data(data, job_id, access_limit)


def get_latest_job_id():
    data = get_api_data(API_URL % '')
    highest_id = 0

    for opportunity in data['opportunities']:
        if opportunity['id'] > highest_id:
            highest_id = opportunity['id']

    print "Start Crawling from jobId: %s" % highest_id
    return highest_id


def main():
    check_or_create_save_folder(SAVE_PATH)
    job_id = get_latest_job_id()
    print("[+] The bot is starting!")
    access_limit = ACCESS_LIMIT

    while job_id > 0 and access_limit > 0:
        access_limit = crawl_api(API_URL, job_id, access_limit)
        job_id -= 1

        if access_limit <= 0:
            print "\nNo new jobs found. Exiting..."

if __name__ == '__main__':
    main()
