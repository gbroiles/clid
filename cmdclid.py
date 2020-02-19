#! /usr/bin/env python3
""" command line util to pull CLID data from bulkcnam.com """
# pylint: disable=invalid-name
import argparse
import os
import requests
import clid


def create_parse():
    """ set up parser options """
    parser = argparse.ArgumentParser(description="Caller ID lookup tool")
    parser.add_argument("subject", help="phone number[s] to look up", nargs="*")
    return parser


def start():
    """ main function body """
    parser = create_parse()
    args = parser.parse_args()
    subject = args.subject
    for i in subject:
        result, status = clid.process(apikey, session, clid.cleanup(i))
        print(result)


try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"

session = requests.Session()

if __name__ == "__main__":
    start()
