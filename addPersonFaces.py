# coding: utf-8

#PersonにFaceを追加する
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import argparse
import time
import sys
import configparser
import os
import json
import csv

DIR = os.path.dirname(os.path.abspath(__file__))
API_BASE = 'westus.api.cognitive.microsoft.com'
API_URI  = '/face/v1.0/persongroups/'
METHOD   = 'POST'

ini_file = DIR + "/config.ini"
config = configparser.SafeConfigParser()

if os.path.exists(ini_file):
    config.read(ini_file, encoding='utf8')
else:
    sys.stderr.write(ini_file + " が見つかりません")
    sys.exit(2)

HEADERS = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': config.get('account', 'subscription-key'),
}

parser = argparse.ArgumentParser(
    description='personGroupId')
parser.add_argument('personGroupId', help='personGroupId')
args = parser.parse_args()

target_json_file = DIR + "/data/addPersonFaces.json";
def main():
    with open(target_json_file) as data_file:
        target_data = json.load(data_file)
        person_group_id   = "pgid%s" % args.personGroupId

        for key in target_data.keys():
            person_id  = str(key)
            print(person_id)
            for image_url in target_data[person_id]["images"]:
                body = '{"url":"%s"}' % image_url
                print("[REQ] personId: %s, body: %s" %(person_id, body))
                try:
                    #begin_at = time.time()
                    conn = http.client.HTTPSConnection(API_BASE)
                    conn.request(METHOD, API_URI + person_group_id + "/persons/" + person_id + "/persistedFaces", body , HEADERS)
                    response = conn.getresponse()
                    data = response.read()
                    print("[RES] " + str(data))
                    conn.close()
                    
                    #end_at = time.time()-begin_at
                    #print(end_at)
                    time.sleep(3)
                except Exception as e:
                    print("[Errno {0}] {1}".format(e.errno, e.strerror))    

if __name__ == "__main__" :
    main()