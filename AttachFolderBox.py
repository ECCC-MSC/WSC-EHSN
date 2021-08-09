# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import sys
import wx.lib.scrolledpanel as scrolled

class AttachFolderBox(wx.Panel):
    def __init__(self, parent, func, *args, **kwargs):
        super(AttachFolderBox, self).__init__(*args, **kwargs)
        self.parent = parent
        self.func = func
        self.manager = None
        self.barSize = (710, -1)
        self.buttonSize = (30, 24)
        self.browseSize = (-1, 24)
        self.buttonList = []
        self.addrList = []
        self.browseList = []
        self.columnList = []
        self.pathList = []
        self.rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.InitUI()

    def InitUI(self):

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.layoutSizer)
        self.tableSizer = wx.BoxSizer(wx.VERTICAL)
        self.column = wx.BoxSizer(wx.HORIZONTAL)
        
        self.pathPanel = scrolled.ScrolledPanel(self, style = wx.NO_BORDER)
        self.pathSizer = wx.BoxSizer(wx.VERTICAL)
        self.pathPanel.SetSizer(self.pathSizer)
        
        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))

        self.buttonList.append(wx.Button(self.pathPanel, label="-", size=self.buttonSize))
        self.addrList.append(wx.TextCtrl(self.pathPanel, size=self.barSize))
        self.browseList.append(wx.Button(self.pathPanel, label="Browse", size=self.browseSize))
        self.pathList.append("")

        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
        self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)

        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.addrList[-1])
        self.columnList[-1].Add(self.browseList[-1])

        self.tableSizer.Add(self.columnList[-1])
        
        self.addButton = wx.Button(self.pathPanel, label="+", size=self.buttonSize)
        self.addButton.Bind(wx.EVT_BUTTON, self.add_remove)
        self.column.Add(self.addButton)

        self.pathSizer.Add(self.tableSizer)
        self.pathSizer.Add(self.column)
        
        self.layoutSizer.Add(self.pathPanel, 1, wx.EXPAND)
        
        self.spit = wx.Panel(self, style = wx.SIMPLE_BORDER, size = (-1, 1))
        self.layoutSizer.Add(self.spit, 0, wx.EXPAND)
        self.layoutSizer.Add((-1, 4))
        
        self.includePanel = wx.Panel(self, size = (-1, 20))
        self.inlcudeRow = wx.BoxSizer(wx.HORIZONTAL)
        self.includePanel.SetSizer(self.inlcudeRow)
        contentLabel = wx.StaticText(self.includePanel, label = "Content of Logger Folder:")
        
        self.dataCheck = wx.CheckBox(self.includePanel)
        self.dataCheck.Bind(wx.EVT_CHECKBOX, self.notEmpty)
        dataLabel = wx.StaticText(self.includePanel, label = "Data Files")
       
        self.diagnosticCheck = wx.CheckBox(self.includePanel)
        self.diagnosticCheck.Bind(wx.EVT_CHECKBOX, self.notEmpty)
        diagnosticLabel = wx.StaticText(self.includePanel, label="Diagnostic Files")
        
        self.programCheck = wx.CheckBox(self.includePanel)
        self.programCheck.Bind(wx.EVT_CHECKBOX, self.notEmpty)
        programLabel = wx.StaticText(self.includePanel, label="Program Files")
        
        self.inlcudeRow.Add((5, -1))
        self.inlcudeRow.Add(contentLabel)
        self.inlcudeRow.Add((60,-1))
        self.inlcudeRow.Add(self.dataCheck)
        self.inlcudeRow.Add(dataLabel)
        self.inlcudeRow.Add((80, -1))
        self.inlcudeRow.Add(self.diagnosticCheck)
        self.inlcudeRow.Add(diagnosticLabel)
        self.inlcudeRow.Add((80, -1))
        self.inlcudeRow.Add(self.programCheck)
        self.inlcudeRow.Add(programLabel)
        
        self.layoutSizer.Add(self.includePanel, 0, wx.EXPAND)
        self.pathPanel.SetupScrolling()
        self.pathPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)

    def notEmpty(self, evt):
        if len(self.returnPath()) == 0:
            evt.GetEventObject().SetValue(False)
        evt.Skip()

    def add(self):
        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))
        self.buttonList.append(wx.Button(self.pathPanel, label="-", size=self.buttonSize))
        self.addrList.append(wx.TextCtrl(self.pathPanel, size=self.barSize))
        self.browseList.append(wx.Button(self.pathPanel, label="Browse", size=self.browseSize))
        self.pathList.append("")

        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
        self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)
        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.addrList[-1])
        self.columnList[-1].Add(self.browseList[-1])

        self.tableSizer.Add(self.columnList[-1])
        self.layoutSizer.Layout()

        self.Update()

    def add_remove(self, evt):
        if evt.GetEventObject().GetLabel() == "+":
            self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))
            self.buttonList.append(wx.Button(self.pathPanel, label="-", size=self.buttonSize))
            self.addrList.append(wx.TextCtrl(self.pathPanel, size=self.barSize))
            self.browseList.append(wx.Button(self.pathPanel, label="Browse", size=self.browseSize))
            self.pathList.append("")

            self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
            self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)
            self.columnList[-1].Add(self.buttonList[-1])
            self.columnList[-1].Add(self.addrList[-1])
            self.columnList[-1].Add(self.browseList[-1])

            self.tableSizer.Add(self.columnList[-1])
            self.layoutSizer.Layout()

            self.Update()

        elif evt.GetEventObject().GetLabel() == "-":
            id = self.buttonList.index(evt.GetEventObject())
            self.buttonList[id].Destroy()
            self.addrList[id].Destroy()
            self.browseList[id].Destroy()
            del self.columnList[id]
            del self.buttonList[id]
            del self.addrList[id]
            del self.browseList[id]
            del self.pathList[id]

            if len(self.returnPath()) == 0:
                self.dataCheck.SetValue(False)
                self.diagnosticCheck.SetValue(False)
                self.programCheck.SetValue(False)

            self.layoutSizer.Layout()
            self.Update()
        self.parent.Layout()

    def Browse(self, evt):
        id = self.browseList.index(evt.GetEventObject())
        folderOpenDialog = wx.DirDialog(self, "Select the File", self.rootPath, 
                                        style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if folderOpenDialog.ShowModal() == wx.ID_CANCEL:
            folderOpenDialog.Destroy()
            return

        self.pathList[id] = folderOpenDialog.GetPath()
        self.addrList[id].ChangeValue(self.pathList[id])

        folderOpenDialog.Destroy()

    # return none empty path
    def returnPath(self):
        pathList = []
        for x in range(len(self.addrList)):
            if self.addrList[x].GetValue() != "":
                pathList.append(self.addrList[x].GetValue())
        return pathList


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(850, 600))
    AttachFolderBox(wx.Frame, "DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()