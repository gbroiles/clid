#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name
import argparse
import os
import requests


def create_parse():
    parser = argparse.ArgumentParser(description="Caller ID lookup tool")
    parser.add_argument("subject", help="phone number[s] to look up", nargs="*")
    return parser


def cleanup(input):
    allowed = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    newstr = ""
    for char in input:
        if char in allowed:
            newstr += char
    return newstr


def start():
    parser = create_parse()
    args = parser.parse_args()
    subject = args.subject
    for i in subject:
        print(process(cleanup(i)))


def process(subject):
    DID = str(subject)
    url = "https://cnam.bulkCNAM.com/?id=" + apikey + "&did=" + DID
    #    print(url)
    r = s.get(url)
    status = r.status_code
    if status != 200:
        print(status)
        print(url)
        r.raise_for_status()
    return r.text


try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"

s = requests.Session()

if __name__ == "__main__":
    start()
