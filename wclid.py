#! /usr/bin/env python3
""" GUI utility to retrieve Caller ID info given a phone number """
# pylint: invalid-name,no-member
import os
import requests
import wx
import clid


class mainWindow(wx.Frame):
    """ Main window """
    def __init__(self, parent, title):
        """ set up defaults """
        super(mainWindow, self).__init__(
            parent, title=title, style=wx.DEFAULT_FRAME_STYLE, size=(300, 300)
        )
        self.Centre()
        self.InitUI()

    def InitUI(self):
        """ initialize UI elements """
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        #        importItem = fileMenu.Append(wx.ID_ANY, 'Import file for lookup')
        fileItem = fileMenu.Append(wx.ID_EXIT, "Exit", "Exit application")
        menubar.Append(fileMenu, "&File")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.onQuit, fileItem)
        #       self.Bind(wx.EVT_MENU, self.Import, importItem)
        self.CreateStatusBar()

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 3)

        st1 = wx.StaticText(panel, label="Lookup target")
        sizer.Add(st1, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.tc = wx.TextCtrl(panel)
        sizer.Add(self.tc, pos=(1, 0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        btn1 = wx.Button(panel, label="Go")
        btn1.SetDefault()
        sizer.Add(btn1, pos=(2, 0), flag=wx.ALL, border=5)

        self.check = wx.CheckBox(panel, label="Remote lookup")
        sizer.Add(self.check, pos=(3, 0), flag=wx.ALL, border=5)

        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(self.tc2, pos=(4, 0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        sizer.AddGrowableRow(4)
        sizer.AddGrowableCol(0)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.process, id=btn1.GetId())
        if apikey != "NONE":
            self.check.SetValue(True)
        else:
            self.check.SetValue(False)

    def onQuit(self, e):
        """ user has requested close """
        self.Close()

    def process(self, e):
        """ process user input, return value """
        dirty = self.tc.GetValue()
        clean = clid.cleanup(dirty)
        statusline = ""
        #        statusline = ('{}:{}:'.format(dirty,clean))
        self.tc.SetValue(clean)
        sb = self.GetStatusBar()
        if self.check.GetValue() and apikey != "NONE" and len(clean) == 10:
            sb.SetStatusText("Checking...")
            answer, status = clid.process(apikey, session, clean)
            statusline += str(status)
            line = clean + " = " + answer + "\n"
        else:
            statusline += "Remote check disabled/invalid."
            line = dirty + "/" + clean + " Not checked.\n"
        self.tc2.AppendText(line)
        self.tc.SetValue("")
        sb.SetStatusText(statusline)


#    def Import(self, e):
#        self.SetTitle('Import monster')


try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"
session = requests.Session()


def main():
    """ main event loop """
    app = wx.App()
    frame = mainWindow(None, title="Caller ID Lookup")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    #    start()
    main()
