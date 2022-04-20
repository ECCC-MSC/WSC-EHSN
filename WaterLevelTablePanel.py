# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import sys
import wx.lib.scrolledpanel as scrolled
from WaterTag import *
from DropdownTime import *
import NumberControl
import re
import wx.lib.scrolledpanel as scrolledpanel


class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

class WaterLevelTablePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, func, manager, *args, **kwargs):
        super(WaterLevelTablePanel, self).__init__(*args, **kwargs)
        self.parent = parent
        self.func = func
        self.manager = manager
        self.buttonSize = (32, 25)
        self.entryRow = 22
        self.buttonList = []
        self.columnList = []
        self.stationList = []
        self.timeList = []
        self.bsList = []
        self.hoiList = []
        self.fsList = []
        self.eleSizerList = []
        self.eleCheckList =[]
        self.elevatedList = []
        self.commentsList = []
        self.establishSizer = []
        self.establishCheckList = []
        self.establishList = []
        self.descList =[]
        self.stationType = ["RP1", "RP2", "RP3", "RP4", "RP5", "TP1", "TP2", "TP3", "TP4", "TP5"]
        self.rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.refresh = False
        self.match = False
        # Conventional leveling (0) or total station (1)
        # Set to the value stored in parent
        self.type = self.parent.type
        self.circuit = []
        self.closureVal = ""
        self.uploadVal = False
        self.InitUI()

    def InitUI(self):
        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.layoutSizer)
        self.tableSizer = wx.BoxSizer(wx.VERTICAL)
        self.layoutSizer.Add(self.tableSizer, 0, wx.EXPAND)
        self.column = wx.BoxSizer(wx.HORIZONTAL)

        self.addButton = wx.Button(self, label="+", size=self.buttonSize)
        self.addButton.Bind(wx.EVT_BUTTON, self.add)
        self.column.Add(self.addButton)
        self.layoutSizer.Add(self.column)

        self.SetupScrolling()
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        for x in range(6):
            self.add(1)
        self.refresh = True

    def addEntry(self):
        self.columnList.append(wx.BoxSizer(wx.HORIZONTAL))

        self.buttonList.append(wx.Button(self, label="-", size=self.buttonSize))
        self.stationList.append(wx.ComboBox(self, size=(133, self.entryRow),
                                            style=wx.CB_DROPDOWN, choices=self.stationType))
        self.stationList[-1].Bind(wx.EVT_TEXT, self.stationUpdate)
        self.stationList[-1].Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        if self.manager is not None:
            if self.manager.manager is not None:
                if self.manager.manager.manager is not None:
                    if self.manager.manager.manager.manager is not None:
                        self.stationList[-1].Bind(wx.EVT_TEXT, self.manager.manager.manager.manager.gui.OnLevelNoteStationSelect)

        self.timeList.append(DropdownTime(False, parent=self, size=(-1, 18)))
        self.timeList[-1].hourCmbox.Bind(wx.EVT_TEXT, self.hourUpdate)
        self.timeList[-1].minuteCmbox.Bind(wx.EVT_TEXT, self.minuteUpdate)
        self.timeList[-1].cBtn.Bind(wx.EVT_BUTTON, self.timeUpdate)

        self.bsList.append(MyTextCtrl(self, style= wx.TE_CENTRE))
        self.bsList[-1].Enable(False)
        self.bsList[-1].Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.bsList[-1].Bind(wx.EVT_TEXT, self.bsUpdate)
        self.bsList[-1].Bind(wx.EVT_TEXT, self.OnBacksightUpdateHI)
        self.bsList[-1].Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.bsList[-1].Bind(wx.EVT_KILL_FOCUS, self.bsRound3)

        self.hoiList.append(MyTextCtrl(self, style= wx.TE_READONLY|wx.TE_CENTRE))
        self.hoiList[-1].Enable(False)
        self.hoiList[-1].Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.hoiList[-1].Bind(wx.EVT_TEXT, self.hoiUpdate)
        self.hoiList[-1].Bind(wx.EVT_TEXT, self.OnHIUpdateEle)
        self.hoiList[-1].Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.hoiList[-1].Bind(wx.EVT_TEXT, NumberControl.Round3)

        self.hoiList[-1].SetBackgroundColour((204,204,204))
        self.hoiList[-1].SetForegroundColour((0,0,204))

        if len(self.fsList) == 0:
            self.fsList.append(MyTextCtrl(self, style= wx.TE_READONLY|wx.TE_CENTRE))
        else:
            self.fsList.append(MyTextCtrl(self, style= wx.TE_CENTRE))
        self.fsList[-1].Enable(False)
        self.fsList[-1].Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.fsList[-1].Bind(wx.EVT_TEXT, self.fsUpdate)
        self.fsList[-1].Bind(wx.EVT_TEXT, self.ForesightUpdateEle)
        self.fsList[-1].Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.fsList[-1].Bind(wx.EVT_KILL_FOCUS, self.fsRound3)

        self.eleSizerList.append(wx.BoxSizer(wx.HORIZONTAL))

        self.eleCheckList.append(wx.CheckBox(self))
        self.eleCheckList[-1].Bind(wx.EVT_CHECKBOX, self.OnElevationCkbox)
        self.eleCheckList[-1].Hide()

        if len(self.elevatedList) == 0:
            self.elevatedList.append(MyTextCtrl(self, style= wx.TE_CENTRE))
            self.elevatedList[-1].Bind(wx.EVT_KILL_FOCUS, self.eleRound3)
        else:
            self.elevatedList.append(MyTextCtrl(self, style= wx.TE_READONLY|wx.TE_CENTRE))
            self.elevatedList[-1].Bind(wx.EVT_TEXT, self.eleRound3)
            self.elevatedList[-1].SetBackgroundColour((204,204,204))
            self.elevatedList[-1].SetForegroundColour((0,0,204))
        self.elevatedList[-1].Enable(False)
        self.elevatedList[-1].Bind(wx.EVT_TEXT, self.elevatedUpdate)
        self.elevatedList[-1].Bind(wx.EVT_TEXT, self.OnElevation)
        self.elevatedList[-1].Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        self.eleSizerList[-1].Add(self.eleCheckList[-1], 0, wx.EXPAND|wx.ALL, 3)
        self.eleSizerList[-1].Add(self.elevatedList[-1], 1, wx.EXPAND)

        self.commentsList.append(MyTextCtrl(self))
        self.commentsList[-1].Enable(False)
        self.commentsList[-1].Bind(wx.EVT_TEXT, self.commentsUpdate)

        self.establishSizer.append(wx.BoxSizer(wx.HORIZONTAL))

        self.establishCheckList.append(wx.CheckBox(self))
        self.establishCheckList[-1].Bind(wx.EVT_CHECKBOX, self.OnEstablishCkbox)
        self.establishCheckList[-1].Hide()
        
        self.establishList.append(MyTextCtrl(self, style= wx.TE_CENTRE))
        self.establishList[-1].Enable(False)
        self.establishList[-1].Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.establishList[-1].Bind(wx.EVT_TEXT, self.establishUpdate)
        self.establishList[-1].Bind(wx.EVT_TEXT, self.OnEstablish)
        self.establishList[-1].Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.establishList[-1].Bind(wx.EVT_KILL_FOCUS, self.estRound3)
        
        self.establishSizer[-1].Add(self.establishCheckList[-1], 0, wx.EXPAND|wx.ALL, 3)
        self.establishSizer[-1].Add(self.establishList[-1], 1, wx.EXPAND)
        
        self.descList.append(wx.Button(self, size=(24, 25), label="?"))
        self.descList[-1].Enable(False)

        if self.manager is not None:
            if self.manager.manager is not None:
                if self.manager.manager.manager is not None:
                    if self.manager.manager.manager.manager is not None:
                        self.descList[-1].Bind(wx.EVT_BUTTON, self.manager.manager.manager.manager.gui.OnLevelNoteEstablishedBtn)
        
        self.buttonList[-1].Bind(wx.EVT_BUTTON, self.remove)

        self.columnList[-1].Add(self.buttonList[-1])
        self.columnList[-1].Add(self.stationList[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.timeList[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.bsList[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.hoiList[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.fsList[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.eleSizerList[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.commentsList[-1], 2, wx.EXPAND)
        self.columnList[-1].Add(self.establishSizer[-1], 1, wx.EXPAND)
        self.columnList[-1].Add(self.descList[-1])

        self.tableSizer.Add(self.columnList[-1], 0, wx.EXPAND)
        self.layoutSizer.Layout()
        self.Update()
        if self.refresh:
            self.parent.Layout()

    def add(self, evt):
        self.addEntry()

        self.circuit.append([self.stationList[-1].GetValue(), self.timeList[-1].GetHourVal(), self.timeList[-1].GetMinuteVal(),
                             self.bsList[-1].GetValue(), self.hoiList[-1].GetValue(), self.fsList[-1].GetValue(),
                             self.elevatedList[-1].GetValue(), self.eleCheckList[-1].GetValue(), self.commentsList[-1].GetValue(),
                             self.establishCheckList[-1].GetValue(), self.establishList[-1].GetValue()])

    def remove(self, evt):
        id = self.buttonList.index(evt.GetEventObject())
        self.buttonList[id].Destroy()
        self.stationList[id].Destroy()
        self.timeList[id].Destroy()
        self.bsList[id].Destroy()
        self.hoiList[id].Destroy()
        self.fsList[id].Destroy()
        self.eleCheckList[id].Destroy()
        self.elevatedList[id].Destroy()
        self.commentsList[id].Destroy()
        self.establishList[id].Destroy()
        self.establishCheckList[id].Destroy()
        self.descList[id].Destroy()
        del self.columnList[id]
        del self.buttonList[id]
        del self.stationList[id]
        del self.timeList[id]
        del self.bsList[id]
        del self.hoiList[id]
        del self.fsList[id]
        del self.eleSizerList[id]
        del self.eleCheckList[id]
        del self.elevatedList[id]
        del self.commentsList[id]
        del self.establishList[id]
        del self.establishSizer[id]
        del self.establishCheckList[id]
        del self.descList[id]
        del self.circuit[id]

        if len(self.stationList) > 0:
            self.fsList[0].SetEditable(False)
            self.elevatedList[0].SetEditable(True)
            self.fsList[0].SetValue("")
            self.circuit[0][5] = ""

        self.layoutSizer.Layout()
        self.Update()

        self.parent.Layout()

    def returnCircuit(self):
        return self.circuit

    def returnClosure(self):
        return self.closureVal

    def returnUpload(self):
        return self.uploadVal

    #Disable scrolling function for combobox
    def NoScrolling(self, evt):
        pass

    def stationUpdate(self, evt):
        id = self.stationList.index(evt.GetEventObject())
        if len(evt.GetEventObject().GetValue()) > 0:
            self.rowUnlock(id)
        self.circuit[id][0] = evt.GetEventObject().GetValue()
        self.FindMatch()
        evt.Skip()


    def hourUpdate(self, evt):
        hours = evt.GetEventObject().parent.GenerateHours()
        if evt.GetEventObject().GetValue() not in hours:
            evt.GetEventObject().SetValue('')
        id = self.timeList.index(evt.GetEventObject().parent)
        self.circuit[id][1] = evt.GetEventObject().GetValue()
        evt.Skip()

    def minuteUpdate(self, evt):
        minutes = evt.GetEventObject().parent.GenerateMinutes()
        if evt.GetEventObject().GetValue() not in minutes:
            evt.GetEventObject().SetValue('')
        id = self.timeList.index(evt.GetEventObject().parent)
        self.circuit[id][2] = evt.GetEventObject().GetValue()
        evt.Skip()

    def timeUpdate(self, evt):
        id = self.timeList.index(evt.GetEventObject().parent)
        self.timeList[id].SetToCurrent()
        self.circuit[id][1] = evt.GetEventObject().parent.hourCmbox.GetValue()
        self.circuit[id][2] = evt.GetEventObject().parent.minuteCmbox.GetValue()
        evt.Skip()

    def bsUpdate(self, evt):
        id = self.bsList.index(evt.GetEventObject())
        self.circuit[id][3] = evt.GetEventObject().GetValue()
        evt.Skip()

    def hoiUpdate(self, evt):
        id = self.hoiList.index(evt.GetEventObject())
        self.circuit[id][4] = evt.GetEventObject().GetValue()
        evt.Skip()

    def fsUpdate(self, evt):
        id = self.fsList.index(evt.GetEventObject())
        self.circuit[id][5] = evt.GetEventObject().GetValue()
        evt.Skip()

    def elevatedUpdate(self, evt):
        id = self.elevatedList.index(evt.GetEventObject())
        self.circuit[id][6] = evt.GetEventObject().GetValue()
        evt.Skip()

    def commentsUpdate(self, evt):
        id = self.commentsList.index(evt.GetEventObject())
        self.circuit[id][8] = evt.GetEventObject().GetValue()
        evt.Skip()

    def establishUpdate(self, evt):
        id = self.establishList.index(evt.GetEventObject())
        self.circuit[id][10] = evt.GetEventObject().GetValue()
        evt.Skip()

    def removeAll(self):
        for id in range(len(self.stationList)):
            self.buttonList[0].Destroy()
            self.stationList[0].Destroy()
            self.timeList[0].Destroy()
            self.bsList[0].Destroy()
            self.hoiList[0].Destroy()
            self.fsList[0].Destroy()
            self.eleCheckList[0].Destroy()
            self.elevatedList[0].Destroy()
            self.commentsList[0].Destroy()
            self.establishList[0].Destroy()
            self.establishCheckList[0].Destroy()
            self.descList[0].Destroy()
            del self.columnList[0]
            del self.buttonList[0]
            del self.stationList[0]
            del self.timeList[0]
            del self.bsList[0]
            del self.hoiList[0]
            del self.fsList[0]
            del self.eleCheckList[0]
            del self.eleSizerList[0]
            del self.elevatedList[0]
            del self.commentsList[0]
            del self.establishList[0]
            del self.establishSizer[0]
            del self.establishCheckList[0]
            del self.descList[0]

        self.layoutSizer.Layout()
        self.Update()

        self.parent.Layout()

    def newCircuit(self, type):
        self.removeAll()
        self.circuit = []
        # When adding set the type
        self.type = type
        self.closureVal = ""
        self.uploadVal = False
        for x in range(6):
            self.add(None)

    def load(self, circuit, type):
        # When loading set the type
        self.type = type
        self.removeAll()
        self.circuit = circuit
        for row in circuit:
            self.addEntry()
            self.stationList[-1].Unbind(wx.EVT_TEXT)
            self.stationList[-1].Bind(wx.EVT_TEXT, self.stationUpdate)
            self.stationList[-1].SetValue(row[0])
            self.stationList[-1].Bind(wx.EVT_TEXT, self.manager.manager.manager.manager.gui.OnLevelNoteStationSelect)
            if row[0] != "":
                self.bsList[-1].Enable(True)
                self.hoiList[-1].Enable(True)
                self.fsList[-1].Enable(True)
                self.elevatedList[-1].Enable(True)
                self.commentsList[-1].Enable(True)
                self.establishList[-1].Enable(True)
                self.descList[-1].Enable(True)
                self.timeList[-1].ChangeHourVal(row[1])
                self.timeList[-1].ChangeMinuteVal(row[2])
                self.bsList[-1].SetValue(row[3])
                self.hoiList[-1].SetValue(row[4])
                self.fsList[-1].SetValue(row[5])
                self.elevatedList[-1].SetValue(row[6])
                self.eleCheckList[-1].SetValue(row[7])
                self.commentsList[-1].SetValue(row[8])
                self.establishCheckList[-1].SetValue(row[9])
                self.establishList[-1].SetValue(row[10])

        self.FindMatch()

    def rowUnlock(self, id):
        self.bsList[id].Enable(True)
        self.hoiList[id].Enable(True)
        self.fsList[id].Enable(True)
        self.elevatedList[id].Enable(True)
        self.commentsList[id].Enable(True)
        self.establishList[id].Enable(True)
        self.descList[id].Enable(True)

        self.FindMatch()

    def getStationNum(self):
        count = 0
        for station in self.stationList:
            if station.GetValue() != "":
                count += 1
        return count

    def FindMatch(self):
        value = self.stationList[0].GetValue()
        matchedId = -1
        if self.getStationNum() > 1:
            for id in range(len(self.stationList)):
                if self.stationList[id].GetValue() == value:
                    matchedId = id

            for station in self.stationList:
                station.SetBackgroundColour("White")
                station.Refresh()
            if matchedId > 0:
                self.stationList[matchedId].SetBackgroundColour("Yellow")
                self.stationList[matchedId].Refresh()
                self.stationList[0].SetBackgroundColour("Yellow")
                self.stationList[0].Refresh()

    def OnKillFocus(self, event):
        ctrl = event.GetEventObject()
        value = ctrl.GetValue()

        #start with a dot following numbers
        reg1 = re.compile("^[+|-]?\.\d+$")

        #numbers end up with a dot
        reg2 = re.compile("^[+|-]?\d+\.$")
        reg3 = re.compile("^\.\d+$")
        reg4 = re.compile("\d")
        reg5 = re.compile("^[+|-]?\d+$")
        if not re.search(reg4, value):
            ctrl.ChangeValue("")
        elif re.match(reg1, value):
            if re.match(reg3, value):
                value = "0" + value
            else:
                value = value[0] + "0" + value[1:]
            ctrl.ChangeValue(value)
        elif re.match(reg2, value):
            value = value[:-1]
            ctrl.ChangeValue(value)
        elif re.match(reg5, value):
            pass
        else:
            ctrl.ChangeValue(value)
        event.Skip()

    def OnElevation(self, evt):
        id = self.elevatedList.index(evt.GetEventObject())
        if self.elevatedList[id].GetValue() != '':
            self.eleCheckList[id].Show()
        else:
            self.eleCheckList[id].Hide()
            self.eleCheckList[id].SetValue(False)

        self.Layout()

        try:
            elevationVal = float(self.elevatedList[id].GetValue())

            if id == 0:
                self.fsList[id].SetBackgroundColour("#f3f3f3")
                self.fsList[id].Refresh()

            try:
                backsightVal = float(self.bsList[id].GetValue())
                if self.type == 0:
                    # Conventional Leveling
                    self.hoiList[id].SetValue(str(elevationVal + backsightVal))
                else:
                    # Total Station
                    self.hoiList[id].SetValue(str(elevationVal - backsightVal))

                self.bsList[id].SetBackgroundColour("WHITE")
                self.bsList[id].Refresh()
                evt.Skip()

            except:
                self.hoiList[id].ChangeValue("")
                if id > 0:
                    self.bsList[id].SetBackgroundColour("#f3f3f3")
                    self.bsList[id].Refresh()

                evt.Skip()

        except:
            try:
                backsightVal = float(self.bsList[id].GetValue())
                self.hoiList[id].SetValue(str(backsightVal))
            except:
                self.hoiList[id].SetValue('')
            evt.Skip()
            return
    
    #Update checkbox if Established Elevation is not Empty
    def OnEstablish(self, event):
        id = self.establishList.index(event.GetEventObject())
        if self.establishList[id].GetValue() != '':
            self.establishCheckList[id].Show()
        else:
            self.establishCheckList[id].Hide()
            self.establishCheckList[id].SetValue(False)
        
        self.Layout()
        event.Skip()

    def OnBacksightUpdateHI(self, evt):
        id = self.bsList.index(evt.GetEventObject())
        try:
            backsightVal = float(self.bsList[id].GetValue())
            try:
                elevationVal = float(self.elevatedList[id].GetValue())
                if self.type == 0:
                    # Conventional Leveling
                    self.hoiList[id].SetValue(str(elevationVal + backsightVal))
                else:
                    # Total Station
                    self.hoiList[id].SetValue(str(elevationVal - backsightVal))
            except:

                self.hoiList[id].SetValue(str(backsightVal))
            self.bsList[id].SetBackgroundColour("WHITE")
            self.bsList[id].Refresh()

        except:
            self.hoiList[id].SetValue("")
            if id > 0:
                self.bsList[id].SetBackgroundColour("#f3f3f3")
                self.bsList[id].Refresh()
        evt.Skip()

    def OnHIUpdateEle(self, evt):
        id = self.hoiList.index(evt.GetEventObject())
        hi = self.hoiList[id].GetValue()
        if hi == '':
            for i in reversed(list(range(id))):
                try:
                    hi = float(self.hoiList[i].GetValue())
                    break
                except:
                    if i == 0:
                        evt.Skip()
                        return
        try:
            hi = float(hi)
            if id < len(self.stationList) - 2:
                for i in range(id + 1, len(self.stationList) - 1):
                    foresightVal = self.fsList[i].GetValue()
                    if foresightVal == '':
                        evt.Skip()
                        return
                    try:
                        foresightVal = float(foresightVal)
                        if self.type == 0:
                            # Conventional Leveling
                            self.elevatedList[i].SetValue(str(hi - foresightVal))
                        else:
                            # Total Station
                            self.elevatedList[i].SetValue(str(hi + foresightVal))
                        try:
                            float(self.hoiList[i].GetValue())
                            evt.Skip()
                            return
                        except:
                            continue
                    except:
                        continue
        except:
            evt.Skip()
            return
        evt.Skip()

    def ForesightUpdateEle(self, evt):
        id = self.fsList.index(evt.GetEventObject())
        if id <= len(self.stationList) - 1 and id != 0:
            for i in reversed(list(range(id))):
                try:
                    hiVal = float(self.hoiList[i].GetValue())
                    break
                except:
                    if i == 0:
                        evt.Skip()
                        return
            foresightVal = self.fsList[id].GetValue()

            try:
                foresightVal = float(foresightVal)
                if self.type == 0:
                    # Conventional Leveling
                    self.elevatedList[id].SetValue(str(hiVal - foresightVal))
                else:
                    # Total Station
                    self.elevatedList[id].SetValue(str(hiVal + foresightVal))

                # if
                # if self.results[runIndex][0]:

                #   self.results[runIndex][1] = elevation.GetValue()
                #   print self.results
            except:
                self.elevatedList[id].SetValue("")

                evt.Skip()
                return
        else:
            evt.Skip()
            return

    def bsRound3(self, event):
        NumberControl.Round3(event)
        self.bsUpdate(event)

    def fsRound3(self, event):
        NumberControl.Round3(event)
        self.fsUpdate(event)

    def eleRound3(self, event):
        NumberControl.Round3(event)
        self.elevatedUpdate(event)
    
    def estRound3(self, event):
        NumberControl.Round3(event)
        self.establishUpdate(event)

    #On check elevation check box do uncheck establish check box
    def OnElevationCkbox(self, event):
        id = self.eleCheckList.index(event.GetEventObject())
        self.circuit[id][7] = self.eleCheckList[id].GetValue()
        if self.eleCheckList[id].IsChecked():
            self.establishCheckList[id].SetValue(False)
            self.circuit[id][9] = self.establishCheckList[id].GetValue()
        event.Skip()

    #On check establish check box do uncheck elevation check box
    def OnEstablishCkbox(self, event):
        id = self.establishCheckList.index(event.GetEventObject())
        self.circuit[id][9] = self.establishCheckList[id].GetValue()
        if self.establishCheckList[id].IsChecked():
            self.eleCheckList[id].SetValue(False)
            self.circuit[id][7] = self.eleCheckList[id].GetValue()
        event.Skip()

    # Uncheck a given establish check box
    def clearEstablishCkbox(self, id):
        if self.establishCheckList[id].IsChecked():
            self.establishCheckList[id].SetValue(False)
            self.circuit[id][9] = self.establishCheckList[id].GetValue()
    
    # Uncheck a given elevation check box
    def clearElevationCkbox(self, id):
        if self.eleCheckList[id].IsChecked():
            self.eleCheckList[id].SetValue(False)
            self.circuit[id][7] = self.eleCheckList[id].GetValue()
    
    # Update height of instrument and elevation when type is changed
    def updateHOIandElevation(self):

        # Set the type to be the type of the parent as this has already been set by OnChangeLevelType
        self.type = self.parent.type

        # Iterate over every value in the backsight list
        for i in range(len(self.bsList)):

            # Get the given backsight value and set it to itself
            # This will trigger the the code to update height of instrument and elevation
            # Change in backsight -> OnBacksightUpdateHI() -> OnHIUpdateEle()
            backsightVal = self.bsList[i].GetValue()
            self.bsList[i].SetValue(backsightVal)


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(850, 600))
    WaterLevelPanelTest(wx.Frame, "DEBUG", frame)

    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()