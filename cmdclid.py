#! /usr/bin/env python3
""" command line util to pull CLID data from bulkcnam.com """
# pylint: disable=invalid-name
import argparse
import os
import requests
import clid
import sys


def create_parse():
    """set up parser options"""
    parser = argparse.ArgumentParser(description="Caller ID lookup tool")
    parser.add_argument("subject", help="phone number[s] to look up", nargs="*")
    return parser


def start():
    """main function body"""
    parser = create_parse()
    args = parser.parse_args()
    subject = args.subject
    for i in subject:
        result, status = clid.process(apikey, session, clid.cleanup(i))
        if status == 401:
            print("Authentication unsuccessful, check BULKAPI?")
        elif status == 200:
            print(result)
        else:
            print("Status: ", status)
            print("Result: ", result)
    sys.exit(0)


try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"
    print("No API key found. Please create an account with bulkvs.com.")
    print("The ID found on the CNAM Instructions page at portal.bulkvs.com", end=" ")
    print("should be stored in the BULKAPI environment variable.")
    print("Lookups probably won't work without it.")

session = requests.Session()

if __name__ == "__main__":
    start()
