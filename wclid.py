#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name,no-member,unused-argument,unused-variable,missing-class-docstring
import os
import requests
import wx


def processclid(subject):
    DID = str(subject)
    url = "https://cnam.bulkCNAM.com/?id=" + apikey + "&did=" + DID
    #    print(url)
    r = s.get(url)
    status = r.status_code
    if status != 200:
        print(status)
        print(url)
        r.raise_for_status()
    return r.text, status


def cleanup(input):
    charFound = False
    allowed = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    newstr = ""
    for char in input:
        if char in allowed:
            newstr += char
    return newstr


class mainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(mainWindow, self).__init__(
            parent, title=title, style=wx.DEFAULT_FRAME_STYLE, size=(300, 300)
        )
        self.Centre()
        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        #        importItem = fileMenu.Append(wx.ID_ANY, 'Import file for lookup')
        fileItem = fileMenu.Append(wx.ID_EXIT, "Exit", "Exit application")
        menubar.Append(fileMenu, "&File")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        #       self.Bind(wx.EVT_MENU, self.Import, importItem)
        self.CreateStatusBar()

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 3)

        st1 = wx.StaticText(panel, label="Lookup target")
        sizer.Add(st1, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.tc = wx.TextCtrl(panel)
        sizer.Add(self.tc, pos=(1, 0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        btn1 = wx.Button(panel, label="Go")
        sizer.Add(btn1, pos=(2, 0), flag=wx.ALL, border=5)

        self.check = wx.CheckBox(panel, label="Remote lookup")
        sizer.Add(self.check, pos=(3, 0), flag=wx.ALL, border=5)

        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(self.tc2, pos=(4, 0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        sizer.AddGrowableRow(4)
        sizer.AddGrowableCol(0)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.Process, id=btn1.GetId())
        if apikey != "NONE":
            self.check.SetValue(True)
        else:
            self.check.SetValue(False)

    def OnQuit(self, e):
        self.Close()

    def Process(self, e):
        dirty = self.tc.GetValue()
        clean = cleanup(dirty)
        statusline = ""
        #        statusline = ('{}:{}:'.format(dirty,clean))
        self.tc.SetValue(clean)
        sb = self.GetStatusBar()
        if self.check.GetValue() and apikey != "NONE":
            sb.SetStatusText("Checking...")
            answer, retval = processclid(clean)
            statusline += str(retval)
            line = clean + " = " + answer + "\n"
        else:
            statusline += "Remote check disabled."
            line = clean + "\n"
        self.tc2.AppendText(line)
        self.tc.SetValue("")
        sb.SetStatusText(statusline)


#    def Import(self, e):
#        self.SetTitle('Import monster')


try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = "NONE"
s = requests.Session()


def main():
    app = wx.App()
    frame = mainWindow(None, title="Caller ID Lookup")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    #    start()
    main()
