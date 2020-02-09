#! /usr/bin/env python3
import requests
import argparse
import os,sys

def start():
    s = requests.Session()
# credentials below are demo credentials    
    BULKCNAMID = 'b5398435ec3ecffd07ded0fafd90e45d'
    DID = '3109060901'
    url = 'https://cnam.bulkCNAM.com/?id={}&did={}'.format(BULKCNAMID, DID)
    print(url)
    r = s.get(url)
    status = r.status_code
    if (status != 200):
        print(status)
        print(url)
        r.raise_for_status()
    print(r.text)


if __name__ == '__main__':
    start()

