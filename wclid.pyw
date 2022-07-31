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

menu_def = [
    [
        "&File",
        [
            "&Preferences",
            "E&xit",
        ],
    ],
    [
        "&Help",
        ["&License", "&About"],
    ],
]

main_layout = [
    [sg.Menu(menu_def)],
    [
        sg.Text("Phone number"),
        sg.InputText(key="target", enable_events=True),
        sg.Button("Lookup"),
    ],
    [sg.Text(result, key="resultwindow")],
    [sg.Button("Close")],
]

try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"


def main():
    """main event loop"""
    global apikey

    window = sg.Window("Caller ID Lookup Utility", main_layout)
    while True:
        event, values = window.read()
        if (
            event == sg.WIN_CLOSED or event == "Close" or event == "Exit"
        ):  # if user closes window or clicks cancel
            break
        elif event == "Lookup":
            if apikey == "NONE":
                apikey = getapikey()
                window["resultwindow"].update("API key set to: " + apikey)
            if len(values["target"]) != 10:
                sg.popup("Phone number must be 10 digits")
            else:
                target = clid.cleanup(values["target"])
                result, status = clid.process(apikey, session, target)
                if status == 200:
                    window["resultwindow"].update(target + ": " + result)
                elif status == 401:
                    sg.popup(
                        "Authentication error.\nAPI Key is set to '" + apikey + "'"
                    )
                else:
                    sg.popup("Status: " + str(status)+"\n"+result)
        # validation logic deletes non-digits entered into phone number field
        elif (
            event == "target"
            and values["target"]
            and values["target"][-1] not in ("0123456789")
        ):
            window["target"].update(values["target"][:-1])
        elif event == "Preferences":
            apikey = getapikey()
            window["resultwindow"].update("API Key: " + str(apikey))
        elif event == "About":
            sg.popup(clid.abouttext, title="About")
        elif event == "License":
            sg.popup(clid.licensetext, title="MIT License")
    window.close()
    sys.exit(0)


def getapikey():
    global apikey

    event, values = sg.Window(
        "API Key",
        [
            [
                sg.Text("bulkvs.com API Key"),
                sg.Input(apikey, key="new_apikey"),
            ],
            [sg.Text("Set the environment variable BULKAPI to avoid re-entry")],
            [
                sg.Button("OK"),
                sg.Button("Cancel"),
            ],
        ],
    ).read(close=True)
    if event == "OK":
        entry = values["new_apikey"]
        if "'" in entry:
            sg.popup("API key contains a single quote character, which may cause a HTTP 500 error.")
        elif len(entry) != 32:
            sg.popup(
                "API keys are usually 32 characters long.\nYou provided "
                + str(len(entry))
                + " characters."
            )
        apikey = entry
    return apikey


if __name__ == "__main__":
    main()
