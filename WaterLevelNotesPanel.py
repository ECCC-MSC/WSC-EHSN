# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from ElectronicFieldNotesGUI import *
from WaterLevelTablePanel import *


class WaterLevelNotesPanel(wx.Panel):
    def __init__(self, mode, lang, manager, *args, **kwargs):
        super(WaterLevelNotesPanel, self).__init__(*args, **kwargs)
        self.mode = mode
        self.lang = lang
        self.manager = manager

        self.headerRow = 34
        self.headerCol = 40

        self.circuitList = []
        self.closureList = []
        self.uploadList = []

        self.current = 0

        self.InitUI()

    def InitUI(self):
        self.runSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.runSizer)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.titleSizer = wx.BoxSizer(wx.HORIZONTAL)

        blank = WaterTag("", (32, self.headerRow), self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        station = WaterTag("Station", (self.headerCol + 6, self.headerRow), self, style=wx.SIMPLE_BORDER,
                           size=(-1, self.headerRow))
        time = WaterTag("Time", (self.headerCol + 6, self.headerRow), self, style=wx.SIMPLE_BORDER,
                        size=(-1, self.headerRow))
        backsight = WaterTag("Backsight", (self.headerCol, self.headerRow), self, style=wx.SIMPLE_BORDER,
                             size=(-1, self.headerRow))
        heightOfInstrument = WaterTag("Height of Instrument", (self.headerCol + 6, self.headerRow), self,
                                      style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        foresight = WaterTag("Foresight", (self.headerCol - 2, self.headerRow), self, style=wx.SIMPLE_BORDER,
                             size=(-1, self.headerRow))
        elevated = WaterTag("Elevated [Surveyed]", (self.headerCol, self.headerRow), self, style=wx.SIMPLE_BORDER,
                            size=(-1, self.headerRow))
        comments = WaterTag("Comments", (self.headerCol * 2, self.headerRow), self, style=wx.SIMPLE_BORDER,
                            size=(-1, self.headerRow))
        established = WaterTag("Established Elev.\n(m)[AQUARIUS]", (self.headerCol, self.headerRow), self,
                               style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        self.titleSizer.Add(blank)
        self.titleSizer.Add(station, 1, wx.EXPAND)
        self.titleSizer.Add(time, 1, wx.EXPAND)
        self.titleSizer.Add(backsight, 1, wx.EXPAND)
        self.titleSizer.Add(heightOfInstrument, 1, wx.EXPAND)
        self.titleSizer.Add(foresight, 1, wx.EXPAND)
        self.titleSizer.Add(elevated, 1, wx.EXPAND)
        self.titleSizer.Add(comments, 2, wx.EXPAND)
        self.titleSizer.Add(established, 1, wx.EXPAND)
        self.titleSizer.Add((42, -1), 0)
        self.panel = WaterLevelTablePanel(self, "DEBUG", self, self, style=wx.SIMPLE_BORDER, size=(-1, 175))

        self.runSizer.Add(self.titleSizer, 0, wx.EXPAND)
        self.runSizer.Add(self.panel, 0, wx.EXPAND)
        # sizer.Add(wlnp, wx.EXPAND)
        # self.runSizer.Add(sizer, 1, wx.EXPAND)
        self.circuitList.append(self.panel.returnCircuit())
        self.closureList.append(self.panel.returnClosure())
        self.uploadList.append(self.panel.returnUpload())

        # Closure Panel
        closurePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        closurePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        closurePanel.SetSizer(closurePanelSizer)


        self.closureBtn = wx.Button(closurePanel, label="Closure")
        self.closureBtn.Bind(wx.EVT_BUTTON, self.OnClosure)
        closureSubPanel = wx.Panel(closurePanel, style=wx.SUNKEN_BORDER, size=(90, -1))

        self.closureCtrl = wx.TextCtrl(closureSubPanel, style=wx.TE_PROCESS_ENTER)
        self.closureCtrl.Bind(wx.EVT_TEXT, self.OnClosureCtrl)
        closureSizer = wx.BoxSizer(wx.VERTICAL)
        closureSizer.Add(self.closureCtrl, 1, wx.EXPAND)
        closureSubPanel.SetSizer(closureSizer)

        closureUnitTxt = wx.StaticText(closurePanel, label="m")



        removeRunButton = wx.Button(closurePanel, label="Remove Circuit", size=(120, -1))
        removeRunButton.SetForegroundColour('Red')
        removeRunButton.Bind(wx.EVT_BUTTON, self.remove)

        self.uploadCkbox = wx.CheckBox(closurePanel, label="Upload", size=(-1, -1))
        self.uploadCkbox.Bind(wx.EVT_CHECKBOX, self.uploadUpdate)
        self.uploadCkbox.SetValue(False)

        closurePanelSizer.Add(self.closureBtn, 0, wx.EXPAND|wx.ALL, 5)
        closurePanelSizer.Add(closureSubPanel, 0, wx.EXPAND|wx.ALL, 5)
        closurePanelSizer.Add(closureUnitTxt, 0, wx.EXPAND|wx.TOP|wx.LEFT, 10)
        closurePanelSizer.Add((-1, -1), 1, wx.EXPAND)
        closurePanelSizer.Add(self.uploadCkbox, 0, wx.EXPAND)
        closurePanelSizer.Add(removeRunButton, 0, wx.EXPAND|wx.ALL|wx.ALIGN_RIGHT, 5)
        self.runSizer.Add(closurePanel, 0, wx.EXPAND)

        pageBar = wx.Panel(self, style=wx.SIMPLE_BORDER)
        pageBarSizer = wx.BoxSizer(wx.HORIZONTAL)
        pageBar.SetSizer(pageBarSizer)

        self.pageText = wx.StaticText(pageBar, label="Page 1/1")
        self.prevButton = wx.Button(pageBar, label="< Prev", size=(50, -1))
        self.prevButton.Bind(wx.EVT_BUTTON, self.prevPage)

        self.nextButton = wx.Button(pageBar, label="Next >", size=(50, -1))
        self.nextButton.Bind(wx.EVT_BUTTON, self.nextPage)

        jump = wx.StaticText(pageBar, label="Jump to")
        self.pageBox = wx.ComboBox(pageBar, style=wx.CB_DROPDOWN | wx.SIMPLE_BORDER, choices=["1"])
        self.pageBox.Bind(wx.EVT_COMBOBOX, self.jumpPage)
        self.pageBox.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)

        pageBarSizer.Add((550, -1))
        pageBarSizer.Add(self.prevButton)
        pageBarSizer.Add((20, -1))
        pageBarSizer.Add(self.pageText, 0, wx.EXPAND | wx.TOP | wx.LEFT, 5)
        pageBarSizer.Add((20, -1))
        pageBarSizer.Add(self.nextButton)
        pageBarSizer.Add((30, -1))
        pageBarSizer.Add(jump, 0, wx.EXPAND | wx.TOP | wx.LEFT, 5)
        pageBarSizer.Add((10, -1))
        pageBarSizer.Add(self.pageBox)

        self.runSizer.Add(pageBar, 0, wx.EXPAND)

    def newPage(self):
        self.pageText.SetLabel("Page " + str(self.current + 1) + "/" + str(len(self.circuitList)))

    def add(self, evt):
        self.circuitList[self.current] = self.panel.returnCircuit()
        self.panel.newCircuit()
        self.circuitList.append(self.panel.returnCircuit())
        self.closureList.append(self.panel.returnClosure())
        self.uploadList.append(self.panel.returnUpload())
        self.current = len(self.circuitList) - 1
        self.newPage()
        self.pageBox.Append(str(len(self.circuitList)))
        self.closureCtrl.SetValue(self.closureList[self.current])
        self.uploadCkbox.SetValue(self.uploadList[self.current])

    def remove(self, evt):
        if len(self.circuitList) <= 1:
            pass
        else:
            del self.circuitList[self.current]
            del self.closureList[self.current]
            del self.uploadList[self.current]
            if self.current != 0:
                self.current = self.current - 1
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def prevPage(self, evt):
        if self.current > 0:
            self.current = self.current - 1
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def nextPage(self, evt):
        if self.current < len(self.circuitList) - 1:
            self.current = self.current + 1
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def jumpPage(self, evt):
        destination = int(evt.GetEventObject().GetValue()) - 1
        if destination != self.current:
            self.current = destination
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def jumpToPage(self, page):
        self.current = page
        self.newPage()
        data = self.circuitList[self.current]
        self.panel.load(data)
        self.closureCtrl.SetValue(self.closureList[self.current])
        self.uploadCkbox.SetValue(self.uploadList[self.current])

    def NoScrolling(self, evt):
        pass

    #Recalculate the closure when pressing the closure button for the run
    def OnClosure(self, event):
        startBenchmark = self.panel.stationList[0].GetValue()
        startElevation = self.panel.elevatedList[0].GetValue()
        if startBenchmark == "":
            warning = wx.MessageDialog(None,"The first station is empty",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                event.Skip()
                return
        if startElevation == "":
            warning = wx.MessageDialog(None,"The first elevation is empty",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                event.Skip()
                return
        try:
        # if True:
            startElevation = float(startElevation)
            for i in range(len(self.panel.stationList) - 1, -1, -1):
                if i > 0:
                    pairBM = self.panel.stationList[i].GetValue()

                    if pairBM == startBenchmark:
                        pairEle = self.panel.elevatedList[i].GetValue()
                        try:
                            pairEle = float(pairEle)
                            closureValue = round(pairEle - startElevation, 3)
                            self.closureCtrl.SetValue(str(closureValue))
                            if abs(closureValue) > 0.003:
                                self.closureCtrl.SetBackgroundColour("red")

                            self.uploadCkbox.SetValue(True)
                            self.panel.uploadVal = True
                            event.Skip()
                            return
                        except:
                            warning = wx.MessageDialog(None,"The elevation values provided for the 'BMs' is not a valid number.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
                            cont = warning.ShowModal()
                            if cont == wx.ID_OK:
                                event.Skip()
                                return

            event.Skip()


            warning = wx.MessageDialog(None,"The beginning and ending BM/Reference names are not identical.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                return

        except Exception,e:
            print str(e)
            warning = wx.MessageDialog(None,"The elevation values provided for thr 'REF' is not a valid number.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                evnet.Skip()
                return

    def OnClosureCtrl(self, event):
        self.panel.closureVal = self.closureCtrl.GetValue()
        self.closureList[self.current] = self.panel.closureVal
        if self.closureCtrl.GetValue() != "":
            if abs(float(self.closureCtrl.GetValue())) > 0.003:
                self.closureCtrl.SetBackgroundColour("red")
            else:
                self.closureCtrl.SetBackgroundColour("white")
        else:
            self.closureCtrl.SetBackgroundColour("white")
        self.closureCtrl.Refresh()

        event.Skip()

    def uploadUpdate(self, event):
        self.panel.uploadVal = self.uploadCkbox.GetValue()
        self.uploadList[self.current] = self.panel.uploadVal

    def AddEntry(self, index):
        self.circuitList[index].append(["", "", "", "", "", "", "", False, "", False, ""])

    # Reset water level reference bench mark
    def updateBMs(self, items, indexList):
        preList = ["RP1", "RP2", "RP3", "RP4", "RP5", "TP1", "TP2", "TP3", "TP4", "TP5"]
        if len(indexList) > 0:
            updatedItems = []
            for i in range(len(items)):
                if i in indexList:
                    updatedItems.append(items[i])
            items = updatedItems
        else:
            items = []
        for item in preList:
            items.append(item)

        self.panel.stationType = items

        stationData = []
        for row in self.circuitList[self.current]:
            stationData.append(row[0])

        for id in range(len(self.panel.stationList)):
            self.panel.stationList[id].SetItems(self.panel.stationType)
            self.panel.stationList[id].SetValue(stationData[id])
        # print items
        # for runIndex, subRunPanel in enumerate(self.runSizer.GetChildren()):
        #    levelNotesSizerV = self.GetLevelNotesSizerV(runIndex)
        #    for row in range(len(levelNotesSizerV.GetChildren()) - 1):
        #        rowSizer = self.GetRowSizer(runIndex, row)
        #        stationsCmbo = self.GetStation(runIndex, row)

        #        if stationsCmbo.GetValue() == '':
        #            stationsCmbo.SetItems(items)
        # stationsCmbo.Append("***ttt", wx.Font(19, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        #        else:
        #            ele = self.GetElevation(runIndex, row)
        #            eleValue = ele.GetValue()

        #            desc = self.GetEstablishedElevation(runIndex, row)
        #            descVal = desc.GetValue()
        #            comment = self.GetComments(runIndex, row)
        #            commentVal = comment.GetValue()

        #            bm = stationsCmbo.GetValue()
        #            stationsCmbo.SetItems(items)
        #            stationsCmbo.SetValue(bm)
        #            desc.SetValue(descVal)
        #            comment.SetValue(commentVal)

        #            if row == 0:
        #                ele.SetValue(eleValue)

        #        levelNotesSizerV.Layout()
        #        self.Update()


def main():
    app = wx.App()
    frame = wx.Frame(None, size=(1000, 650))
    WaterLevelNotesPanel("debug", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
