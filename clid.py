#! /usr/bin/env python3
import requests
import argparse
import os,sys

def start(DID):
    url = 'https://cnam.bulkCNAM.com/?id='+apikey+'&did='+DID
#    print(url)
    r = s.get(url)
    status = r.status_code
#    print(status)
    if (status != 200):
        print(status)
        print(url)
        r.raise_for_status()
    print(r.text)

BULKAPI=''
try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = 'NONE'

s = requests.Session()
DID = '9517884141'

if __name__ == '__main__':
    start(DID)
