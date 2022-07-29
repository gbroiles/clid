#! /usr/bin/env python3
""" command line util to pull CLID data from bulkcnam.com """
# pylint: disable=invalid-name
import argparse
import os
import requests
import clid
import sys

noAPImsg = """The BULKAPI environment variable is missing. 
You must create an account at https://bulkvs.com prior to using this utility.
Please copy the ID value from the CNAM Instructions/CNAM Methods page at 
https://portal.bulkvs.com into the BULKAPI environment variable before using this program.
The author of the program has no relationship to the operators of bulkvs.com and is not
compensated for your use of their service.

"""


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
            print("Authentication unsuccessful, check BULKAPI environment variable?")
        elif status == 200:
            print(result,end='')
        else:
            print("Status: ", status)
            print("Result: ", result)
#    sys.exit(0)


try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"
    print(noAPImsg)


session = requests.Session()

if __name__ == "__main__":
    start()
