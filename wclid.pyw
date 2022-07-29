#! /usr/bin/env python3
""" GUI utility to retrieve Caller ID info given a phone number """
# pylint: invalid-name,no-member
import os
import sys
import requests
import PySimpleGUI as sg
import clid


session = requests.Session()

result = "No lookup yet"

layout = [
    [sg.Text("Phone number"), sg.InputText(), sg.Button("Lookup")],
    [sg.Text(result, key="resultwindow")],
    [sg.Button("Close")],
]


def main():
    """main event loop"""
    try:
        apikey = os.environ["BULKAPI"]
    except KeyError:
        apikey = "NONE"

    window = sg.Window("Caller ID Lookup Utility", layout)
    while True:
        event, values = window.read()
        if (
            event == sg.WIN_CLOSED or event == "Close"
        ):  # if user closes window or clicks cancel
            break
        elif event == "Lookup":
            target = clid.cleanup(values[0])
            result, status = clid.process(apikey, session, target)
            window["resultwindow"].update(result)
    window.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
