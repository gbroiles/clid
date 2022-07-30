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
            if len(values["target"]) != 10:
                sg.popup("Phone number must be 10 digits")
            elif apikey == "NONE":
                apikey = getapikey()
                window["resultwindow"].update("API key set to: "+apikey)
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
                    window["resultwindow"].update("Status: " + str(status))
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
            about()
        elif event == "License":
            license()
    window.close()
    sys.exit(0)


def getapikey():
    global apikey

    event, values = sg.Window(
        "API Key",
        [
            [
                sg.Text("bulkvs.com API Key"),
                sg.Input(apikey, key="apikey"),
            ],
            [sg.Text("Set the environment variable BULKAPI to avoid re-entry")],
            [
                sg.Button("OK"),
                sg.Button("Cancel"),
            ],
        ],
    ).read(close=True)
    #    return(str(values)+" "+str(event))
    if event == "OK":
        entry = values["apikey"]
        if len(entry) == 32:
            return entry
        else:
            sg.popup(
                "API keys are usually 32 characters long.\nYou provided "
                + str(len(entry))
                + " characters.\nYou may need to try again."
            )
            return entry
    if event == "Cancel":
        return apikey


def license():
    sg.popup(clid.licensetext, title="MIT License")


def about():
    sg.popup(clid.abouttext, title="About")


if __name__ == "__main__":
    main()
