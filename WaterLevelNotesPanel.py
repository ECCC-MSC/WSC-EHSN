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
        self.headerCol = 100

        self.circuitList = []
        self.closureList = []
        self.uploadList = []
        
        self.levelingMessage = "NOTE: Time entered only for the first Station will propagate to the others within the Circuit upon upload to AQUARIUS."

        # Current index into lists
        self.current = 0

        # Conventional leveling (0) or total station (1)
        # Defaults to conventional leveling
        self.type = 0

        self.InitUI()

    def InitUI(self):
        self.runSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.runSizer)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.titleSizer = wx.BoxSizer(wx.HORIZONTAL)

        blank = WaterTag("", "", (32, self.headerRow), self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        station = WaterTag("Station", "", (self.headerCol + 30, self.headerRow), self, style=wx.SIMPLE_BORDER,
                           size=(-1, self.headerRow))
        time = WaterTag("   Time", self.levelingMessage, (self.headerCol + 18, self.headerRow), self, style=wx.SIMPLE_BORDER,
                        size=(-1, self.headerRow))
        backsight = WaterTag("Backsight", "", (self.headerCol + 30, self.headerRow), self, style=wx.SIMPLE_BORDER,
                             size=(-1, self.headerRow))
        heightOfInstrument = WaterTag("Height of Instrument", "", (self.headerCol + 31, self.headerRow), self,
                                      style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        foresight = WaterTag("Foresight", "", (self.headerCol + 31, self.headerRow), self, style=wx.SIMPLE_BORDER,
                             size=(-1, self.headerRow))
        elevated = WaterTag("Elevation [Surveyed]", "", (self.headerCol + 31, self.headerRow), self, style=wx.SIMPLE_BORDER,
                            size=(-1, self.headerRow))
        comments = WaterTag("Comments", "", ((self.headerCol * 2) + 64, self.headerRow), self, style=wx.SIMPLE_BORDER,
                            size=(-1, self.headerRow))
        established = WaterTag("Established Elev.\n(m)[AQUARIUS]", "", (self.headerCol, self.headerRow), self,
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
        closurePanelSizer.Add(removeRunButton, 0, wx.EXPAND|wx.ALL|wx.RIGHT, 5)
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
        self.panel.newCircuit(self.type)
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
            # Confirm that this circuit will be deleted
            dlg = wx.MessageDialog(self, "Are you sure you want to delete this circuit?", 'Remove', wx.YES_NO | wx.ICON_QUESTION)
            res = dlg.ShowModal()

            if res == wx.ID_YES:
                dlg.Destroy()
            elif res == wx.ID_NO:
                dlg.Destroy()
                return
            else:
                dlg.Destroy()
                return

            del self.circuitList[self.current]
            del self.closureList[self.current]
            del self.uploadList[self.current]
            if self.current != 0:
                self.current = self.current - 1
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data, self.type)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def prevPage(self, evt):
        if self.current > 0:
            self.current = self.current - 1
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data, self.type)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def nextPage(self, evt):
        if self.current < len(self.circuitList) - 1:
            self.current = self.current + 1
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data, self.type)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def jumpPage(self, evt):
        destination = int(evt.GetEventObject().GetValue()) - 1
        if destination != self.current:
            self.current = destination
            self.newPage()
            data = self.circuitList[self.current]
            self.panel.load(data, self.type)
            self.closureCtrl.SetValue(self.closureList[self.current])
            self.uploadCkbox.SetValue(self.uploadList[self.current])

    def jumpToPage(self, page):
        self.current = page
        self.newPage()
        data = self.circuitList[self.current]
        self.panel.load(data, self.type)
        self.closureCtrl.SetValue(self.closureList[self.current])
        self.uploadCkbox.SetValue(self.uploadList[self.current])

    def NoScrolling(self, evt):
        pass

    # Recalculate the closure when pressing the closure button for the run
    def OnClosure(self, event):

        # Get the starting benchmark and starting elevation
        startBenchmark = self.panel.stationList[0].GetValue()
        startElevation = self.panel.elevatedList[0].GetValue()

        # If either of these are empty, then display an error message to the user
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
            startElevation = float(startElevation)
            # Iterate over every benchmark value in reverse
            for i in range(len(self.panel.stationList) - 1, -1, -1):
                if i > 0:
                    pairBM = self.panel.stationList[i].GetValue()

                    # If the benchmark value here is equal to the starting benchmark
                    # Then the closure can be calculated using the corresponding elevation
                    if pairBM == startBenchmark:
                        pairEle = self.panel.elevatedList[i].GetValue()
                        try:
                            # Calculate the closure
                            pairEle = float(pairEle)
                            closureValue = round(startElevation - pairEle, 3)

                            # Set the closure and set the colour
                            self.closureCtrl.SetValue(str(closureValue))
                            if abs(closureValue) > 0.003:
                                self.closureCtrl.SetBackgroundColour("red")

                            # Set the upload checkbox as this is automatically checked
                            # when the closure is calculated
                            self.uploadCkbox.SetValue(True)
                            self.panel.uploadVal = self.uploadCkbox.GetValue()
                            self.uploadList[self.current] = self.panel.uploadVal
                            
                            # Clear all other upload checkboxes
                            # as only one circuit should be uploaded at a time
                            #for i in range(len(self.uploadList)):
                            #    if i != self.current and self.uploadList[i] == True:
                            #        self.uploadList[i] = False
                            
                            event.Skip()
                            return
                        except:
                            # Display an error message for the user
                            warning = wx.MessageDialog(None,"The elevation values provided for the 'BMs' is not a valid number.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
                            cont = warning.ShowModal()
                            if cont == wx.ID_OK:
                                event.Skip()
                                return

            event.Skip()

            # Display an error message for the user
            warning = wx.MessageDialog(None,"The beginning and ending BM/Reference names are not identical.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                return

        except Exception as e:
            print(str(e))
            # Display an error message for the user
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
        # Clear all other upload checkboxes
        # as only one circuit should be uploaded at a time
        #for i in range(len(self.uploadList)):
        #    if i != self.current and self.uploadList[i] == True:
        #        self.uploadList[i] = False

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
    
    def IsUploaded(self):
        for circuitIndex in range(len(self.circuitList)):
            if self.uploadList[circuitIndex]:
                return True
        return False
    
    # If any upload checkbox selected including any value in the circuit, will return False. Otherwise, return True
    def IsEmpty(self):
        if not self.IsUploaded():
            return True
        for circuitIndex in range(len(self.circuitList)):
            if self.uploadList[circuitIndex]:
                for rowIndex in range(len(self.circuitList[circuitIndex])):
                    if self.circuitList[circuitIndex][rowIndex][0] != "":
                        return False
        return True
    
    # Update height of instrument and elevation for all circuits when type is changed
    def UpdateCircuitHOIandElevation(self):

        # Iterate over every circuit
        for circuitIndex in range(len(self.circuitList)):

            # Don't update height of instrument or elevation if the circuit is currently displayed
            # This is updated separately
            if circuitIndex != self.current:

                # Get the circuit
                given_circuit = self.circuitList[circuitIndex]

                # Iterate over every row in the given circuit
                for rowIndex in range(len(given_circuit)):
                    
                    # Get the row
                    row = self.circuitList[circuitIndex][rowIndex]

                    # ---------------------------
                    # Update height of instrument
                    # ---------------------------
                    try:
                        # Get the float value for backsight
                        backsightVal = float(row[3])
                        try:
                            # Get the float value for elevation
                            elevationVal = float(row[6])

                            # Calculate the height of instrument based on these
                            if self.type == 0:
                                # Conventional Leveling
                                row[4] = str(elevationVal + backsightVal)
                            else:
                                # Total Station
                                row[4] = str(elevationVal - backsightVal)

                        except:
                            # If the elevation value cannot be obtained
                            # then set the height of instrument to the backsight
                            row[4] = str(backsightVal)

                    except:
                        # If both values cannot be obtained
                        # then set the height of instrument to an empty string
                        row[4] = ''
                    

                    # ----------------
                    # Update elevation
                    # ----------------

                    # Get the height of instrument value
                    hoiVal = row[4]

                    if hoiVal == '':
                        # If height of instrument is an empty string
                        # Then iterate in reverse to find the last height of instrument value that is not empty
                        for i in reversed(list(range(rowIndex))):
                            try:
                                # If this value can be converted to a float
                                # then a suitable height of instrument has been found
                                hoiVal = float(self.circuitList[circuitIndex][i][4])
                                break
                            except:
                                # If no suitable values can be found
                                # then height of instrument will remain an empty string
                                if i == 0:
                                    break
                    try:
                        # Get the float value for height of instrument
                        # This will fail if hoiVal is an empty string
                        hoiVal = float(hoiVal)

                        # If the index of the row is less than the second last index in the circuit
                        if rowIndex < len(self.circuitList[circuitIndex]) - 2:

                            # Iterate from the next index for the row up to the last index in the circuit
                            for i in range(rowIndex + 1, len(self.circuitList[circuitIndex]) - 1):

                                # Get the forsight value at this given row
                                foresightVal = self.circuitList[circuitIndex][i][5]

                                # If the foresight is an empty string
                                # then break out of the loop
                                if foresightVal == '':
                                    break

                                try:
                                    # Get the float value for foresight
                                    foresightVal = float(foresightVal)

                                    # Calculate the elevation based on these
                                    if self.type == 0:
                                        # Conventional Leveling
                                        self.circuitList[circuitIndex][i][6] = str(hoiVal - foresightVal)
                                    else:
                                        # Total Station
                                        self.circuitList[circuitIndex][i][6] = str(hoiVal + foresightVal)
                                    
                                    # Try converting the height of instrument at this index to a float
                                    # If this succeeds, then break out of the loop
                                    try:
                                        float(self.circuitList[circuitIndex][i][4])
                                        break
                                    except:
                                        continue
                                except:
                                    continue
                    except:
                        continue


    # Update the previously calculated closure value for the level notes table 
    # when conventional leveling is changed to total station and vice versa
    def ClosureUpdate(self):

        # If there is a closure value already calculated, then it must be recalculated
        if self.closureList[self.current] != '':

            # Get the starting benchmark and starting elevation
            startBenchmark = self.panel.stationList[0].GetValue()
            startElevation = self.panel.elevatedList[0].GetValue()

            # If either of these are empty, then return
            if startBenchmark == "":
                return
            if startElevation == "":
                return
            
            try:
                startElevation = float(startElevation)
                # Iterate over every benchmark value in reverse
                for i in range(len(self.panel.stationList) - 1, -1, -1):
                    if i > 0:
                        pairBM = self.panel.stationList[i].GetValue()

                        # If the benchmark value here is equal to the starting benchmark
                        # Then the closure can be calculated using the corresponding elevation
                        if pairBM == startBenchmark:
                            pairEle = self.panel.elevatedList[i].GetValue()
                            try:
                                # Calculate the closure
                                pairEle = float(pairEle)
                                closureValue = round(startElevation - pairEle, 3)

                                # Set the closure and set the colour
                                self.closureCtrl.SetValue(str(closureValue))
                                if abs(closureValue) > 0.003:
                                    self.closureCtrl.SetBackgroundColour("red")

                                return
                            except:
                                return
                return
            except:
                return


    # Update all previously calculated closure values for all circuits
    # when conventional leveling is changed to total station and vice versa
    def CircuitClosureUpdate(self):
        
        # Iterate over every circuit
        for circuitIndex in range(len(self.circuitList)):
            
            # Don't update the closure value if the circuit is currently displayed
            # This is updated separately
            if circuitIndex != self.current:

                # If there is a previous value for closure for this circuit, it must be updated
                if self.closureList[circuitIndex] != '':

                    # Get the circuit list
                    given_circuit = self.circuitList[circuitIndex]

                    # Get the starting benchmark and starting elevation from the list
                    startBenchmark = given_circuit[0][0]
                    startElevation = given_circuit[0][6]

                    # If either of these are empty, then continue to the next circuit
                    if startBenchmark == "":
                        continue
                    if startElevation == "":
                        continue
                    
                    try:
                        startElevation = float(startElevation)
                        # Iterate over every row in the circuit in reverse
                        for i in range(len(given_circuit) - 1, -1, -1):
                            if i > 0:
                                # Get the benchmark for this row
                                pairBM = given_circuit[i][0]

                                # If the benchmark value here is equal to the starting benchmark
                                # Then the closure can be calculated using the corresponding elevation
                                if pairBM == startBenchmark:
                                    # Get the elevation for this row
                                    pairEle = given_circuit[i][6]
                                    try:
                                        # Calculate the closure
                                        pairEle = float(pairEle)
                                        closureValue = round(startElevation - pairEle, 3)

                                        # Set the new closure value in the closure list
                                        self.closureList[circuitIndex] = str(closureValue)
                                        
                                        continue
                                    except:
                                        continue
                        continue
                    except:
                        continue

def main():
    app = wx.App()
    frame = wx.Frame(None, size=(1000, 650))
    WaterLevelNotesPanel("debug", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
