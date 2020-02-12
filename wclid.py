#! /usr/bin/env python3
#pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name
import argparse
import os
import requests
import wx

def create_parse():
    parser = argparse.ArgumentParser(
        description='Caller ID lookup tool')
    parser.add_argument('subject', help='phone number[s] to look up', nargs='*')
    return parser


def start():
    parser = create_parse()
    args = parser.parse_args()
    subject = args.subject
    for i in subject:
        print(process(i))

def process(subject):
    DID = str(subject)
    url = 'https://cnam.bulkCNAM.com/?id='+apikey+'&did='+DID
#    print(url)
    r = s.get(url)
    status = r.status_code
    if status != 200:
        print(status)
        print(url)
        r.raise_for_status()
    return r.text

class mainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(mainWindow, self).__init__(parent, title=title, style=wx.MAXIMIZE_BOX
                | wx.SYSTEM_MENU | wx.CAPTION |  wx.CLOSE_BOX | wx.MINIMIZE_BOX,
            size=(300, 200))
        self.Centre()
        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
#        importItem = fileMenu.Append(wx.ID_ANY, 'Import file for lookup')
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Exit', 'Exit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
 #       self.Bind(wx.EVT_MENU, self.Import, importItem)

        panel=wx.Panel(self)
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(8)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Lookup target')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 10))
        panel.SetSizer(vbox)

    def OnQuit(self, e):
        self.Close()

#    def Import(self, e):
#        self.SetTitle('Import monster')



#try:
#    apikey = os.environ["BULKAPI"]
#except KeyError:
#    apikey = 'NONE'
#s = requests.Session()
def main():
    app = wx.App()
    frame = mainWindow(None, title='Caller ID Lookup')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
#    start()
    main()
