# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import sys
import wx.lib.scrolledpanel as scrolled

class AttachPhotoBox(scrolled.ScrolledPanel):
    def __init__(self, parent, func, *args, **kwargs):
        super(AttachPhotoBox, self).__init__(*args, **kwargs)
        self.parent = parent
        self.func = func
        self.manager = None
        self.barSize = (655, -1)
        self.buttonSize = (30, -1)
        self.buttonList = []
        self.addrList = []
        self.browseList = []
        self.columnList = []
        self.typeList = []
        self.type = ["SIT", "STR", "COL", "CBL", "EQP", "CDT", "HSN"]
        self.rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.InitUI()

    def InitUI(self):

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.layoutSizer)

        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))

        self.buttonList.append(wx.Button(self, label="+", size=self.buttonSize))
        self.typeList.append(wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.TE_READONLY, choices=self.type))
        self.typeList[-1].SetValue("SIT")
        self.addrList.append(wx.TextCtrl(self, size=self.barSize))
        self.browseList.append(wx.Button(self, label="Browse"))

        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
        self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)

        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.typeList[-1])
        self.columnList[-1].Add(self.addrList[-1])
        self.columnList[-1].Add(self.browseList[-1])
        self.layoutSizer.Add(self.columnList[-1])

        self.SetupScrolling()
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

    def check(self):
        for x in self.buttonList:
            if x != self.buttonList[-1]:
                x.SetLabel("-")
            else:
                x.SetLabel("+")

    def add(self):
        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))
        self.buttonList.append(wx.Button(self, label="+", size=self.buttonSize))
        self.typeList.append(wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.TE_READONLY, choices=self.type))
        self.typeList[-1].SetValue("SIT")
        self.addrList.append(wx.TextCtrl(self, size=self.barSize))
        self.browseList.append(wx.Button(self, label="Browse"))

        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
        self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)
        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.typeList[-1])
        self.columnList[-1].Add(self.addrList[-1])
        self.columnList[-1].Add(self.browseList[-1])

        self.layoutSizer.Add(self.columnList[-1])
        self.check()
        self.layoutSizer.Layout()
        self.Update()

    def add_remove(self, evt):
        if evt.GetEventObject().GetLabel() == "+":
            self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))
            self.buttonList.append(wx.Button(self, label="+", size=self.buttonSize))
            self.typeList.append(wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.TE_READONLY, choices=self.type))
            self.typeList[-1].SetValue("SIT")
            self.addrList.append(wx.TextCtrl(self, size=self.barSize))
            self.browseList.append(wx.Button(self, label="Browse"))

            self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
            self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)
            self.columnList[-1].Add(self.buttonList[-1])
            self.columnList[-1].Add(self.typeList[-1])
            self.columnList[-1].Add(self.addrList[-1])
            self.columnList[-1].Add(self.browseList[-1])

            self.layoutSizer.Add(self.columnList[-1])
            self.check()
            self.layoutSizer.Layout()
            self.Update()

        elif evt.GetEventObject().GetLabel() == "-":
            id = self.buttonList.index(evt.GetEventObject())
            self.buttonList[id].Destroy()
            self.typeList[id].Destroy()
            self.addrList[id].Destroy()
            self.browseList[id].Destroy()
            del self.columnList[id]
            del self.buttonList[id]
            del self.typeList[id]
            del self.addrList[id]
            del self.browseList[id]

            self.check()
            self.layoutSizer.Layout()
            self.Update()
        self.parent.Layout()

    def Browse(self, evt):
        id = self.browseList.index(evt.GetEventObject())
        if self.typeList[id].GetValue() == "Folder":
            DirOpenDialog = wx.DirDialog(self, "Select the Folder", self.rootPath,
                                         style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            if DirOpenDialog.ShowModal() == wx.ID_CANCEL:
                DirOpenDialog.Destroy()
                return

            self.addrList[id].ChangeValue(DirOpenDialog.GetPath())

            DirOpenDialog.Destroy()

        else:
            fileOpenDialog = wx.FileDialog(self, "Select the File", self.rootPath, '',
                                           self.func,
                                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
            if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
                fileOpenDialog.Destroy()
                return

            self.addrList[id].ChangeValue(fileOpenDialog.GetPath())

            fileOpenDialog.Destroy()

    def returnSIT(self):
        SITList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "SIT" and self.addrList[x].GetValue() != "":
                SITList.append(self.addrList[x].GetValue())
        return SITList

    def returnSTR(self):
        STRList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "STR" and self.addrList[x].GetValue() != "":
                STRList.append(self.addrList[x].GetValue())
        return STRList

    def returnCOL(self):
        COLList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "COL" and self.addrList[x].GetValue() != "":
                COLList.append(self.addrList[x].GetValue())
        return COLList

    def returnCBL(self):
        CBLList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "CBL" and self.addrList[x].GetValue() != "":
                CBLList.append(self.addrList[x].GetValue())
        return CBLList

    def returnEQP(self):
        EQPList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "EQP" and self.addrList[x].GetValue() != "":
                EQPList.append(self.addrList[x].GetValue())
        return EQPList

    def returnCDT(self):
        CDTList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "CDT" and self.addrList[x].GetValue() != "":
                CDTList.append(self.addrList[x].GetValue())
        return CDTList

    def returnHSN(self):
        HSNList = []
        for x in range(len(self.addrList)):
            if self.typeList[x].GetValue() == "HSN" and self.addrList[x].GetValue() != "":
                HSNList.append(self.addrList[x].GetValue())
        return HSNList

    def returnPath(self):
        pathList = []
        for x in range(len(self.addrList)):
            if self.addrList[x].GetValue() != "":
                pathList.append(self.addrList[x].GetValue())
        return pathList


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(850, 600))
    AttachPhotoBox(wx.Frame, "DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()