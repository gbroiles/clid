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
    ["&Help", "&About..."],
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


def main():
    """main event loop"""
    try:
        apikey = os.environ["BULKAPI"]
    except KeyError:
        apikey = "NONE"

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
                values = sg.Window(
                    "API Key",
                    [
                        [
                            sg.T("bulkvs.com API Key"),
                            sg.In(key="apikey"),
                        ],
                        [
                            sg.B("OK"),
                            sg.B("Cancel"),
                        ],
                    ],
                ).read(close=True)
                apikey = values["apikey"]
            else:
                target = clid.cleanup(values["target"])
                result, status = clid.process(apikey, session, target)
                window["resultwindow"].update(result)
        # validation logic deletes non-digits entered into phone number field
        elif (
            event == "target"
            and values["target"]
            and values["target"][-1] not in ("0123456789")
        ):
            window["target"].update(values["target"][:-1])
    window.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
