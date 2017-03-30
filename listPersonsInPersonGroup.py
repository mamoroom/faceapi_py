# coding: utf-8

#Person Groupを作成する
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
METHOD   = 'GET'

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

if not (int(args.personGroupId) > 0 and int(args.personGroupId) < 1001):
    sys.stderr.write("invalid attributes| %s\n" % args.personGroupId)
    sys.exit(2)

def test():
	print("test")

def main():

	person_group_id   = "pgid%s" % args.personGroupId
	try:
	    #begin_at = time.time()
	    conn = http.client.HTTPSConnection(API_BASE)
	    conn.request(METHOD, API_URI + person_group_id + "/persons", {}, HEADERS)
	    response = conn.getresponse()
	    data = response.read()
	    conn.close()
	    j_list = json.loads(data.decode('utf-8'))
	    #for d in j_list:
	    #	print(d["personId"])
	    keys = j_list[0].keys()
	    with open(DIR + '/data/' + person_group_id + '.csv', 'w') as f:
	    	dict_writer = csv.DictWriter(f, keys)
    		dict_writer.writeheader()
    		dict_writer.writerows(j_list)

	    #with open(DIR + '/data/' + person_group_id + '.csv', 'w') as f:
		#    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
		#    writer.writerow(j_list)     # list（1次元配列）の場合
		    #writer.writerows(array2d) # 2次元配列も書き込める
	    
	    #end_at = time.time()-begin_at
	    #print(end_at)
    
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))	

if __name__ == "__main__" :
	main()
