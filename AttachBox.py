# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import sys
import wx.lib.scrolledpanel as scrolled

class AttachBox(scrolled.ScrolledPanel):
    def __init__(self, parent, func, *args, **kwargs):
        super(AttachBox, self).__init__(*args, **kwargs)
        self.parent = parent
        # Set func to *
        self.func = "*"
        self.manager = None
        # Get the passed in name type
        self.name = func
        self.barSize = (610, -1)
        self.buttonSize = (30, 24)
        self.browseSize = (-1, 24)
        self.labelSize = (190, -1)
        self.buttonList = []
        self.addrList = []
        self.labelList = []
        self.browseList = []
        self.columnList = []
        self.pathList = []
        self.rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.count = 0
        self.InitUI()

    def InitUI(self):

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.layoutSizer)
        self.tableSizer = wx.BoxSizer(wx.VERTICAL)
        self.column = wx.BoxSizer(wx.HORIZONTAL)

        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))

        self.buttonList.append(wx.Button(self, label="-", size=self.buttonSize))
        self.addrList.append(wx.TextCtrl(self, size=self.barSize))
        self.browseList.append(wx.Button(self, label="Browse", size=self.browseSize))
        self.labelList.append(wx.TextCtrl(self, size=self.labelSize, style=wx.TE_READONLY))
        self.pathList.append("")

        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
        self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)

        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.addrList[-1])
        self.columnList[-1].Add(self.browseList[-1])
        self.columnList[-1].Add(self.labelList[-1])

        self.tableSizer.Add(self.columnList[-1])

        self.addButton = wx.Button(self, label="+", size=self.buttonSize)
        self.addButton.Bind(wx.EVT_BUTTON, self.add_remove)
        self.column.Add(self.addButton)
        
        self.layoutSizer.Add(self.tableSizer)
        self.layoutSizer.Add(self.column)
        self.SetupScrolling()
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)

    def add(self):
        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))
        self.buttonList.append(wx.Button(self, label="-", size=self.buttonSize))
        self.addrList.append(wx.TextCtrl(self, size=self.barSize))
        self.browseList.append(wx.Button(self, label="Browse", size=self.browseSize))
        self.labelList.append(wx.TextCtrl(self, size=self.labelSize, style=wx.TE_READONLY))
        self.pathList.append("")

        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
        self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)
        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.addrList[-1])
        self.columnList[-1].Add(self.browseList[-1])
        self.columnList[-1].Add(self.labelList[-1])

        self.tableSizer.Add(self.columnList[-1])
        self.layoutSizer.Layout()
        self.Update()

    def add_remove(self, evt):
        if evt.GetEventObject().GetLabel() == "+":
            self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))
            self.buttonList.append(wx.Button(self, label="-", size=self.buttonSize))
            self.addrList.append(wx.TextCtrl(self, size=self.barSize))
            self.browseList.append(wx.Button(self, label="Browse", size=self.browseSize))
            self.labelList.append(wx.TextCtrl(self, size=self.labelSize, style=wx.TE_READONLY))
            self.pathList.append("")

            self.buttonList[-1].Bind(wx.EVT_BUTTON, self.add_remove)
            self.browseList[-1].Bind(wx.EVT_BUTTON, self.Browse)
            self.columnList[-1].Add(self.buttonList[-1])
            self.columnList[-1].Add(self.addrList[-1])
            self.columnList[-1].Add(self.browseList[-1])
            self.columnList[-1].Add(self.labelList[-1])

            self.tableSizer.Add(self.columnList[-1])
            self.updateLabels()
            self.layoutSizer.Layout()
            self.Update()

        elif evt.GetEventObject().GetLabel() == "-":
            id = self.buttonList.index(evt.GetEventObject())
            self.buttonList[id].Destroy()
            self.addrList[id].Destroy()
            self.browseList[id].Destroy()
            self.labelList[id].Destroy()
            del self.columnList[id]
            del self.buttonList[id]
            del self.addrList[id]
            del self.browseList[id]
            del self.pathList[id]
            del self.labelList[id]
            self.updateLabels()

            self.layoutSizer.Layout()
            self.Update()
        self.parent.Layout()
    
    # Update the displayed file labels for the window
    def updateLabels(self):
        
        # Set the count back to zero
        self.count = 0

        # Get the station number
        stnNum = self.parent.parent.genInfo.stnNumCmbo.GetValue()
        if stnNum.isspace():
            stnNum = ''

        # Get the date
        dateVal = self.parent.parent.genInfo.datePicker.GetValue().Format(self.parent.fm)

        # Iterate over every entered path
        # And increment the count and set the label based on the passed in name type
        for id in range(len(self.addrList)):
            if self.name == "LoggerData" and self.addrList[id].GetValue() != "":
                self.count += 1
                self.labelList[id].ChangeValue(stnNum + "_" + dateVal + "_LG" + str(self.count))
            elif self.name == "LoggerDiagnostic" and self.addrList[id].GetValue() != "":
                self.count += 1
                self.labelList[id].ChangeValue(stnNum + "_" + dateVal + "_LD" + str(self.count))
            elif self.name == "LoggerProgram" and self.addrList[id].GetValue() != "":
                self.count += 1
                self.labelList[id].ChangeValue(stnNum + "_" + dateVal + "_LP" + str(self.count))
            elif self.name == "DischargeSummary" and self.addrList[id].GetValue() != "":
                self.count += 1
                self.labelList[id].ChangeValue(stnNum + "_" + dateVal + "_M" + str(self.count))

    def Browse(self, evt):
        id = self.browseList.index(evt.GetEventObject())
        fileOpenDialog = wx.FileDialog(self, "Select the File", self.rootPath, '',
                                       self.func,
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        filepath = fileOpenDialog.GetPath()
        fileOpenDialog.Destroy()

        # Get the extension of the file
        name, extension = os.path.splitext(filepath)

        # If the discharge summary file is not a pdf, then display a warning to the user
        if extension != '.pdf' and self.name == "DischargeSummary":
            info = wx.MessageDialog(self, 'The Discharge Measurement Summary File type must be PDF.', 'Incorect file type',
                                wx.OK | wx.ICON_ERROR)
            info.ShowModal()
            return
        else:
            self.pathList[id] = filepath
            self.addrList[id].ChangeValue(self.pathList[id])
            self.updateLabels()

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
    AttachBox(wx.Frame, "DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()