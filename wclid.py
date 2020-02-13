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
            size=(300, 500))
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
        self.CreateStatusBar()

        panel=wx.Panel(self)
        sizer = wx.GridBagSizer(5, 3)

        st1 = wx.StaticText(panel, label='Lookup target')
        sizer.Add(st1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        self.tc = wx.TextCtrl(panel)
        sizer.Add(self.tc, pos=(1, 0), 
            flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)

        btn1 = wx.Button(panel, label='Go')
        sizer.Add(btn1, pos=(2,0), flag=wx.ALL, border=5)

        self.check = wx.CheckBox(panel, label="Remote lookup")
        sizer.Add(self.check, pos=(3,0), flag=wx.ALL, border=5)

        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.tc2, pos=(4,0), 
                flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)

        sizer.AddGrowableRow(4)
        sizer.AddGrowableCol(0)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON,  self.Process, id=btn1.GetId())

    def OnQuit(self, e):
        self.Close()

    def Process(self, e):
        target = self.tc.GetValue()
        if self.check.GetValue():
            line = target + ' = ' + process(target) + '\n'
        else:
            line = target + '\n'
        self.tc2.AppendText(line)

#    def Import(self, e):
#        self.SetTitle('Import monster')



try:
    apikey = os.environ["BULKAPI"]
except KeyError:
    apikey = 'NONE'
s = requests.Session()
def main():
    app = wx.App()
    frame = mainWindow(None, title='Caller ID Lookup')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
#    start()
    main()
