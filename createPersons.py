# coding: utf-8

#Person Groupを作成する
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import argparse
import time
import sys
import configparser
import os


DIR = os.path.dirname(os.path.abspath(__file__))
API_BASE = 'westus.api.cognitive.microsoft.com'
API_URI  = '/face/v1.0/persongroups/'
METHOD   = 'POST'
CREATE_GROUPS_NUM = 1
INDEX = 1

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
	for i in range(INDEX, CREATE_GROUPS_NUM+1):

		person_group_id   = "pgid%s" % args.personGroupId
		name              = "%s-%s" % (person_group_id, i)
		body              = '{"name":"%s", "userData":"user data of %s"}' % (name, name)
		print("[REQ] " + body)
		try:
		    #begin_at = time.time()
		    conn = http.client.HTTPSConnection(API_BASE)
		    conn.request(METHOD, API_URI + person_group_id + "/persons", body , HEADERS)
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
