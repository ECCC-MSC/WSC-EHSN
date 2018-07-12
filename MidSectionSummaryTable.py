# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import sigfig
from wx.grid import *
from MidSectionSubPanel import *
from MidSectionSubPanelObj import *

import win32gui




class MidSectionSummaryTable(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(MidSectionSummaryTable, self).__init__(*args, **kwargs)
        self.channelLbl = "Channel Condition"
        self.panelNumLbl = "Panel #"
        self.distanceLbl = "Tagmark (m)"
        self.widthLbl = "Width\n(m)"
        self.depthLbl = "Depth\n(m)"
        self.wsBottomIceLbl = "W.S.\nto\nBottom Ice\n(m)"
        self.depthUnderIceLbl = "Effective\nDepth\n(m)"
        self.observationDepthLbl = "Observation\nDepth\n(m)"
        self.revolutionsLbl = "Revolutions"
        self.timeLbl = "Time\n(s)"
        self.velocityPointLbl = "Velocity\nat Point\n(m/s)"
        self.areaLbl = U"Area\n(m\N{SUPERSCRIPT TWO})"
        self.dischargeLbl = u"Discharge\n(m\N{SUPERSCRIPT THREE}/s)"
        self.flowLbl = "% Flow"
        self.meanVelLbl = "Mean\nVelocity\n(m/s)"
        self.dlg = None
        self.nextPanelNum = 1
        self.edgeSize = (440, 310)
        self.panelSize = (570, 660)

        self.numberOfPanels = 0

        # self.summaryTable.GetNumberRows() = 0
        self.panelObjs = []
        self.lastPanelObj = None
        self.lastObj = None
        self.pos = None
        self.numberOfPanelObjs = 0

        self.modifiedPanelArrayIndex = -1
        self.modifiedPanelTableIndex = -1
        self.cellHeight = 21
        self.increasingPolority = None
        self.nextPid = 100
        self.subpanel = None


        self.InitUI()



    def InitUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(layout)

        self.summaryTable = Grid(self)
        self.summaryTable.CreateGrid(1, 14)

        self.summaryTable.SetColLabelValue(0, self.panelNumLbl)
        self.summaryTable.SetColLabelValue(1, self.distanceLbl)
        self.summaryTable.SetColLabelValue(2, self.widthLbl)
        self.summaryTable.SetColLabelValue(3, self.depthLbl)
        self.summaryTable.SetColLabelValue(4, self.wsBottomIceLbl)
        self.summaryTable.SetColLabelValue(5, self.depthUnderIceLbl)
        self.summaryTable.SetColLabelValue(6, self.observationDepthLbl)
        self.summaryTable.SetColLabelValue(7, self.revolutionsLbl)
        self.summaryTable.SetColLabelValue(8, self.timeLbl)
        self.summaryTable.SetColLabelValue(9, self.velocityPointLbl)
        self.summaryTable.SetColLabelValue(10, self.meanVelLbl)
        self.summaryTable.SetColLabelValue(11, self.areaLbl)
        self.summaryTable.SetColLabelValue(12, self.dischargeLbl)
        self.summaryTable.SetColLabelValue(13, self.flowLbl)

        self.summaryTable.SetColLabelSize(60)

        self.summaryTable.SetRowLabelSize(40)
        self.summaryTable.HideRowLabels()

        #self.summaryTable.SetColFormatFloat(1, precision=3)
        self.summaryTable.SetColFormatFloat(1, precision=2)
        self.summaryTable.SetColFormatFloat(2, precision=3)
        self.summaryTable.SetColFormatFloat(3, precision=2)
        self.summaryTable.SetColFormatFloat(4, precision=2)
        self.summaryTable.SetColFormatFloat(5, precision=2)
        self.summaryTable.SetColFormatFloat(6, precision=2)
        self.summaryTable.SetColFormatFloat(7, precision=0)
        self.summaryTable.SetColFormatFloat(8, precision=1)
        self.summaryTable.SetColFormatFloat(9, precision=3)
        self.summaryTable.SetColFormatFloat(10, precision=3)
        self.summaryTable.SetColFormatFloat(11, precision=3)
        # I manually round it to 3 sigfig and put it. <- this statement is not valid anymore
        self.summaryTable.SetColFormatFloat(12, precision=3)
        self.summaryTable.SetColFormatFloat(13, precision=1)

        self.summaryTable.Bind(EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
        self.summaryTable.EnableEditing(False)

        self.summaryTable.AutoSize()
        self.summaryTable.SetColSize(0, 60)



        self.addBtn = wx.Button(self, label="+", size=(-1, -1))
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAdd)
        layout.Add(self.summaryTable, 0, wx.EXPAND|wx.ALL, 20)
        layout.Add(self.addBtn, 0, wx.ALL, 20)

        self.GetParent().GetParent().GetParent().GetParent().Bind(wx.EVT_SIZE, self.OnSize)
        self.subPanel = None


    def OnSize(self, event):

        size = event.GetSize()
        width = size.GetWidth()
        height = size.GetHeight()

        for col in range(14):
            self.summaryTable.SetColSize(col, width/(14 + 2))

        event.Skip()


    def OnRightClick(self, event):
        # x = event.GetPosition().x + self.GetPosition().x + self.GetParent().GetParent().GetParent().GetParent().GetPosition().x
        # y = event.GetPosition().y + self.GetPosition().y + self.GetParent().GetParent().GetParent().GetParent().GetPosition().y

        if len(self.panelObjs) > 0:
            # for i in self.panelObjs:
            #     i.ToString()
            index = event.GetRow()

            objIndex = ""
            if len(self.panelObjs) > 0:
                for i in reversed(range(index + 1)):
    
                    if self.summaryTable.GetCellValue(i, 0) != "":
                        for j, obj in enumerate(self.panelObjs):

                            if str(obj.panelNum) == self.summaryTable.GetCellValue(i, 0) and float(obj.distance) == float(self.summaryTable.GetCellValue(i, 1)):
                                self.modifiedPanelArrayIndex = j
                                self.modifiedPanelTableIndex = i
                                break
                        break




            self.summaryTable.ClearSelection()
            modifiedPanelObj = self.panelObjs[self.modifiedPanelArrayIndex]

            if isinstance(modifiedPanelObj, EdgeObj):
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex)
            elif isinstance(modifiedPanelObj, PanelObj) and len(modifiedPanelObj.depths) == 1:
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex)
            elif isinstance(modifiedPanelObj, PanelObj) and len(modifiedPanelObj.depths) == 2:
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex, addToSelected=True)
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex+1, addToSelected=True)
            elif isinstance(modifiedPanelObj, PanelObj) and len(modifiedPanelObj.depths) == 3:
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex, addToSelected=True)
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex+1, addToSelected=True)
                self.summaryTable.SelectRow(self.modifiedPanelTableIndex+2, addToSelected=True)
            #self.summaryTable.DeselectRow(self.modifiedPanelTableIndex)
            self.dlg = wx.Dialog(self, title="Editing Menu", size=(150, 170), pos=win32gui.GetCursorPos())
            dlgSizer = wx.BoxSizer(wx.VERTICAL)
            self.dlg.SetSizer(dlgSizer)
            addBtn = wx.Button(self.dlg, label="Add")
            insertBtn = wx.Button(self.dlg, label="Insert")
            deleteBtn = wx.Button(self.dlg, label="Remove")
            deleteBtn.SetBackgroundColour("Grey")
            modifyBtn = wx.Button(self.dlg, label="Edit")

            if len(self.panelObjs) > 0 and self.panelObjs[-1].panelNum == "End Edge":
                addBtn.Enable(False)
            if len(self.panelObjs) > 1 and self.modifiedPanelArrayIndex == 0:
                deleteBtn.Enable(False)

            addBtn.Bind(wx.EVT_BUTTON, self.OnAdd)
            deleteBtn.Bind(wx.EVT_BUTTON, self.OnRemove)
            insertBtn.Bind(wx.EVT_BUTTON, self.OnInsert)
            modifyBtn.Bind(wx.EVT_BUTTON, self.OnEdit)


            dlgSizer.Add(addBtn, 1, wx.EXPAND)
            dlgSizer.Add(modifyBtn, 1, wx.EXPAND)
            dlgSizer.Add(insertBtn, 1, wx.EXPAND)
            dlgSizer.Add(deleteBtn, 1, wx.EXPAND)


            self.dlg.ShowModal()


    def OnRemove(self, event):

        if self.dlg != None:
            self.dlg.Destroy()
            self.dlg = None


        if len(self.panelObjs) > 0:

            dlg = wx.MessageDialog(self, "Do you want to delete the selected Panel/Edge?", 'None', wx.YES_NO)
            res = dlg.ShowModal()
            if res == wx.ID_NO:
                dlg.Destroy()
                return
            else:
                dlg.Destroy()

        if "P" in str(self.panelObjs[self.modifiedPanelArrayIndex].panelNum):
            if self.panelObjs[self.modifiedPanelArrayIndex].startOrEnd:
                self.Remove(self.modifiedPanelArrayIndex, self.modifiedPanelTableIndex)
                self.Remove(self.modifiedPanelArrayIndex, self.modifiedPanelTableIndex)
            else:
                self.Remove(self.modifiedPanelArrayIndex, self.modifiedPanelTableIndex)
                self.Remove(self.modifiedPanelArrayIndex-1, self.modifiedPanelTableIndex-1)

        else:
            self.Remove(self.modifiedPanelArrayIndex, self.modifiedPanelTableIndex)






    def Remove(self, arrayIndex, tableIndex):

        removedObj = self.panelObjs.pop(arrayIndex)
        if isinstance(removedObj, PanelObj):
            for obj in self.panelObjs:
                if isinstance(obj, PanelObj) and obj.panelNum > removedObj.panelNum:
                    obj.panelNum = str(int(obj.panelNum) - 1)

            length = len(removedObj.depths)
            self.nextPanelNum -= 1

        else:
            length = 1

        self.summaryTable.DeleteRows(tableIndex, length)

        self.UpdateObjInfoByRow(arrayIndex - 1)
        self.TransferFromObjToTable()
        self.RefreshFlow()
        self.CalculatePolority()

        #self.CalculateSummary()

        newHeight = self.summaryTable.GetSize().GetHeight() - length * self.cellHeight
        self.summaryTable.SetSize((-1, newHeight))

        #Enable the Adding Button if "End Edge" removed
        if len(self.panelObjs) > 0 and self.panelObjs[-1].panelNum != "End Edge":
            self.addBtn.Enable(True)

        if self.summaryTable.GetNumberRows() == 0:
            self.summaryTable.AppendRows()


        self.Layout()


    def GetTableIndex(self, obj):
        for i in range(self.summaryTable.GetNumberRows()):

            if str(self.summaryTable.GetCellValue(i, 1)) == str(obj.distance):
                return i

        return -1


    def OnAdd(self, event):

        if self.dlg != None:
            self.dlg.Destroy()
            self.dlg = None
        #TBD ===================================================================================NEED MORE CONDITIONS HERE!===
        self.Adding()
        # event.Skip()

    def OnInsert(self, event):
        if self.dlg != None:
            self.dlg.Destroy()
            self.dlg = None

        self.Adding(insert=True)

    def Adding(self, insert=False, endPier=False):
        panelType = 1
        panelSize = self.panelSize
        if len(self.panelObjs) == 0:
            panelType = 0
            panelSize = self.edgeSize



        frame = wx.Dialog(self, size=panelSize, style=wx.RESIZE_BORDER|wx.CAPTION)
        header = self.GetParent().header


        if len(self.panelObjs) > 0:
            self.lastObj = self.panelObjs[-1]

        if self.lastObj is not None:
            if isinstance(self.lastObj, EdgeObj) or isinstance(self.lastObj, EdgeObj):
                if isinstance(self.lastObj.startOrEnd, str):
                    if self.lastObj.startOrEnd=="True":
                        self.lastObj.startOrEnd = True
                    else:
                        self.lastObj.startOrEnd = False
                if (isinstance(self.lastObj, EdgeObj) and self.lastObj.startOrEnd and self.lastObj.edgeType == "Pier") or endPier:
                    panelType = 2
                    panelSize = self.edgeSize


            if isinstance(self.lastObj, PanelObj):
                self.lastPanelObj = self.lastObj
        else:
            self.lastPanelObj = None

        nextTagMark = self.GetNextTagMark()

        if insert:
            modify=1
            nextTagMark = ""

        else:
            modify=0

        if endPier:
            nextTagMark = ""
            panelType = 2
            panelSize = self.edgeSize

        else:    
            self.GenerateNextPid()

        

        self.subPanel = MidSectionSubPanel(panelNum=self.nextPanelNum, parent=frame, size=panelSize, panelType=panelType, \
            pos=self.pos, nextTagMark=nextTagMark, modify=modify, pid=self.nextPid)





        if insert and not endPier:
            self.subPanel.panel.headerTxt.SetLabel("Inserting a new panel")
            if len(self.panelObjs) > 0 and self.panelObjs[-1].panelNum == "End Edge":
                self.subPanel.windowTypeBtn1.Disable()
        # else:
        #     subPanel.panel.saveNextBtn.Show()
        #     subPanel.edge.saveNextBtn.Show()
        #     subPanel.pier.saveNextBtn.Show()
        if endPier:
            self.subPanel.pier.endEdgeRdBtn.SetValue(True)
            self.subPanel.pier.startEdgeRdBtn.Disable()
        





        if len(self.panelObjs) == 0 and panelType == 0:
            # subPanel.edge.panelNumberCtrl.SetValue(subPanel.edge.types[0])
            self.subPanel.edge.endEdgeRdBtn.Disable()
            self.subPanel.windowTypeBtn1.Disable()
            self.subPanel.windowTypeBtn2.Disable()
            self.subPanel.windowTypeBtn3.Disable()
        else:
            self.subPanel.edge.riverBankCtrl.Disable()

            if self.panelObjs[0].leftOrRight == self.subPanel.edge.leftRight[2]:
                self.subPanel.edge.riverBankCtrl.SetValue(self.subPanel.edge.leftRight[1])
            else:
                self.subPanel.edge.riverBankCtrl.SetValue(self.subPanel.edge.leftRight[2])



        self.subPanel.UpdateSubPanel()
        #### Edge #####
        if isinstance(self.lastObj, EdgeObj):
            if self.lastObj.startOrEnd and "start p" in self.lastObj.panelNum.lower():
                self.subPanel.edge.endEdgeRdBtn.SetValue(True)
                self.subPanel.windowTypeBtn2.Disable()
                self.subPanel.edge.startEdgeRdBtn.Disable()
                # subPanel.edge.panelNumberCtrl.Disable()
        

        # Check if start edge exists in panels, if so, check if user selected [Edge @ Bank],
        # if so, automatically select End Radio button
        for obj in self.panelObjs:
            if isinstance(obj, EdgeObj) and obj.startOrEnd:    #"edge" in obj.edgeType.lower():
                self.subPanel.edge.endEdgeRdBtn.SetValue(True)
                break


        #### Panel ###
        if header.meter1MeterNoCtrl.GetValue() != "":
            self.subPanel.panel.slopeCtrl.SetValue(header.meter1SlopeCtrl1.GetValue())
            self.subPanel.panel.slopeCtrl2.SetValue(header.meter1SlopeCtrl2.GetValue())
            self.subPanel.panel.interceptCtrl.SetValue(header.meter1InterceptCtrl1.GetValue())
            self.subPanel.panel.interceptCtrl2.SetValue(header.meter1InterceptCtrl2.GetValue())
        elif header.meter2MeterNoCtrl.GetValue() != "":
            self.subPanel.panel.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
            self.subPanel.panel.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
            self.subPanel.panel.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
            self.subPanel.panel.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())
        else:
            self.subPanel.panel.slopeCtrl.SetValue("")
            self.subPanel.panel.slopeCtrl2.SetValue("")
            self.subPanel.panel.interceptCtrl.SetValue("")
            self.subPanel.panel.interceptCtrl2.SetValue("")

        if header.meter1MeterNoCtrl.GetValue() != "" and header.meter1MeterNoCtrl.GetValue() is not None:
            if header.meter2MeterNoCtrl.GetValue() != "" and header.meter2MeterNoCtrl.GetValue() is not None:
                self.subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue(), header.meter2MeterNoCtrl.GetValue()])
            else:
                self.subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue()])
            if self.lastPanelObj is not None:
                self.subPanel.panel.currentMeterCtrl.SetValue(self.lastPanelObj.currentMeter)
                self.subPanel.panel.slopeCtrl.SetValue(self.lastPanelObj.slop)
                self.subPanel.panel.interceptCtrl.SetValue(self.lastPanelObj.intercept)
                self.subPanel.panel.slopeCtrl2.SetValue(self.lastPanelObj.slop2)
                self.subPanel.panel.interceptCtrl2.SetValue(self.lastPanelObj.intercept2)
            else:
                self.subPanel.panel.currentMeterCtrl.SetValue(header.meter1MeterNoCtrl.GetValue())
        else:
            if header.meter2MeterNoCtrl.GetValue() != "":
                self.subPanel.panel.currentMeterCtrl.SetItems([header.meter2MeterNoCtrl.GetValue()])
                self.subPanel.panel.currentMeterCtrl.SetValue(header.meter2MeterNoCtrl.GetValue())
            else:
                self.subPanel.panel.currentMeterCtrl.SetItems([])

        if header.measureSectionCtrl.GetValue().lower() == "open":
            self.subPanel.panel.panelConditionCombox.SetItems(["Open"])
            self.subPanel.panel.panelConditionCombox.SetValue("Open")
        elif header.measureSectionCtrl.GetValue().lower() == "ice":
            self.subPanel.panel.panelConditionCombox.SetItems(["Ice"])
            self.subPanel.panel.panelConditionCombox.SetValue("Ice")
        else:
            if self.lastPanelObj is not None:
                self.subPanel.panel.panelConditionCombox.SetItems(["Open", "Ice"])
                self.subPanel.panel.panelConditionCombox.SetValue(self.lastPanelObj.panelCondition)
                # subPanel.panel.OnPanelCondition(event)
            else:
                self.subPanel.panel.panelConditionCombox.SetItems(["Open", "Ice"])
                self.subPanel.panel.panelConditionCombox.SetSelection(0)

        if self.lastPanelObj is not None:
            # remember last slope radio button
            if self.lastPanelObj.slopBtn1:
                self.subPanel.panel.slopBtn1.SetValue(True)
            else:
                self.subPanel.panel.slopBtn2.SetValue(True)
            # remember 'amount of weight', 'WL/DL Correction' if panelCondition=open

            if self.subPanel.panel.panelConditionCombox.GetValue() == "Open":
                self.subPanel.panel.amountWeightCmbox.SetValue(self.lastPanelObj.weight)
                self.subPanel.panel.wldlCorrectionCmbox.SetValue(self.lastPanelObj.wldl)
                self.subPanel.panel.weightOffsetCtrl.SetValue(self.lastPanelObj.offset)
            # remember 'Ice Assembly' if panelCondition=ice
            if self.subPanel.panel.panelConditionCombox.GetValue() == "Ice":
                self.subPanel.panel.iceAssemblyCmbbox.SetValue(self.lastPanelObj.iceAssembly)
                self.subPanel.panel.meterAboveCtrl.SetValue(self.lastPanelObj.aboveFoot)
                self.subPanel.panel.meterBelowCtrl.SetValue(self.lastPanelObj.belowFoot)
                self.subPanel.panel.distanceAboveCtrl.SetValue(self.lastPanelObj.distAboveWeight)
                self.subPanel.panel.iceThickCtrl.SetValue(str(self.lastPanelObj.iceThickness))
                self.subPanel.panel.iceThickAdjustedCtrl.SetValue(str(self.lastPanelObj.iceThicknessAdjusted))



        self.subPanel.panel.PanelConditionUpdate()
        # self.subPanel.panel.SlopeRadioUpdate()
        #subPanel.panel.OnIceAssmeblyNoEvent()
        self.subPanel.panel.WLDLCorrection()
        self.subPanel.panel.UpdateWetLineCorrectionNoEvent()
        #subPanel.panel.UpdateMeterOffset()
        self.subPanel.panel.UpdateVelocityCorrection()
        self.subPanel.panel.UpdateGrid()

        self.subPanel.panel.BindingEvents()

        # self.modifiedPanelArrayIndex
        # self.modifiedPanelTableIndex

        frame.ShowModal()
        # frame.Show(True)



    def GenerateNextPid(self):
        self.nextPid += 1
        return self.nextPid


    def OnEdit(self, event):

        self.Modify()

    def Modify(self):
        if self.dlg != None:
            self.dlg.Destroy()
            self.dlg = None
        if len(self.panelObjs) == 0:
            return

        if self.modifiedPanelArrayIndex > len(self.panelObjs) - 1:
            self.modifiedPanelArrayIndex = len(self.panelObjs) - 1
            dlg = wx.MessageDialog(None, "This is the last panel", "", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
        #TBD ===================================================================================NEED MORE CONDITIONS HERE!===
        # for i in self.panelObjs:
        #     i.ToString()
        if isinstance(self.panelObjs[self.modifiedPanelArrayIndex], EdgeObj):
            if self.panelObjs[self.modifiedPanelArrayIndex].edgeType == "Edge" or "Edge" in str(self.panelObjs[self.modifiedPanelArrayIndex].panelNum):
                panelType = 0
            else:
                panelType = 2
        else:
            panelType = 1

        if panelType == 0 or panelType == 2:
            panelSize = self.edgeSize
        elif panelType == 1:
            panelSize = self.panelSize

        frame = wx.Dialog(self, size=panelSize, style=wx.RESIZE_BORDER|wx.CAPTION)
        header = self.GetParent().header
        modifiedObj = self.panelObjs[self.modifiedPanelArrayIndex]

        # modifiedObj.ToString()
        pid = modifiedObj.pid

        self.subPanel = MidSectionSubPanel(panelNum=modifiedObj.panelNum, parent=frame, \
            size=panelSize, panelType=panelType, modify=2, pos=self.pos, pid=pid)



        # subPanel.edge.nextBtn.Show()
        # subPanel.edge.preBtn.Show()
        # subPanel.panel.nextBtn.Show()
        # subPanel.panel.preBtn.Show()

        # if panelType == 2 and subPanel.pier.startEdgeRdBtn.GetValue() and (self.modifiedPanelArrayIndex == len(self.panelObjs) - 1\
        #  or self.panelObjs[self.modifiedPanelArrayIndex+1].panelNum != "End Pier"):
        #     subpanel.pier.saveBtn.Hide()


        self.subPanel.windowTypeBtn1.Disable()
        self.subPanel.windowTypeBtn2.Disable()
        self.subPanel.windowTypeBtn3.Disable()

        self.subPanel.UpdateSubPanel()
        if header.meter1MeterNoCtrl.GetValue() != "":
            self.subPanel.panel.slopeCtrl.SetValue(header.meter1SlopeCtrl1.GetValue())
            self.subPanel.panel.slopeCtrl2.SetValue(header.meter1SlopeCtrl2.GetValue())
            self.subPanel.panel.interceptCtrl.SetValue(header.meter1InterceptCtrl1.GetValue())
            self.subPanel.panel.interceptCtrl2.SetValue(header.meter1InterceptCtrl2.GetValue())
        elif header.meter2MeterNoCtrl.GetValue() != "":
            self.subPanel.panel.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
            self.subPanel.panel.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
            self.subPanel.panel.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
            self.subPanel.panel.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())
        else:
            self.subPanel.panel.slopeCtrl.SetValue("")
            self.subPanel.panel.slopeCtrl2.SetValue("")
            self.subPanel.panel.interceptCtrl.SetValue("")
            self.subPanel.panel.interceptCtrl2.SetValue("")

        if header.meter1MeterNoCtrl.GetValue() != "" and header.meter1MeterNoCtrl.GetValue() is not None:
            if header.meter2MeterNoCtrl.GetValue() != "" and header.meter2MeterNoCtrl.GetValue() is not None:
                self.subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue(), header.meter2MeterNoCtrl.GetValue()])
            else:
                self.subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue()])
        else:
            if header.meter2MeterNoCtrl.GetValue() != "" and header.meter2MeterNoCtrl.GetValue() is not None:
                self.subPanel.panel.currentMeterCtrl.SetItems([header.meter2MeterNoCtrl.GetValue()])
            else:
                self.subPanel.panel.currentMeterCtrl.SetItems([])

        if header.measureSectionCtrl.GetValue() == "Open":
            self.subPanel.panel.panelConditionCombox.SetItems(["Open"])
        elif header.measureSectionCtrl.GetValue() == "Ice":
            self.subPanel.panel.panelConditionCombox.SetItems(["Ice"])
        else:
            self.subPanel.panel.panelConditionCombox.SetItems(["Open", "Ice"])
            if isinstance(modifiedObj, PanelObj):
                self.subPanel.panel.panelConditionCombox.SetValue(modifiedObj.panelCondition)
                if "Ice" in self.subPanel.panel.panelConditionCombox.GetValue():
                    self.subPanel.panel.icePanel.Show()
                    self.subPanel.panel.openWaterPanel.Hide()
                else:
                    self.subPanel.panel.openWaterPanel.Show()
                    self.subPanel.panel.icePanel.Hide()

                self.subPanel.panel.Layout()
            # else:
            #     subPanel.panel.panelConditionCombox.SetValue("Open")

        if panelType == 0 or panelType == 2:
            if panelType == 0:
                edgePanel = self.subPanel.edge
            else:
                edgePanel = self.subPanel.pier
            edgePanel.measurementTimeCtrl.SetValue(modifiedObj.time)
            # edgePanel.panelNumberCtrl.SetValue(modifiedObj.edgeType)
            if isinstance(modifiedObj.startOrEnd, str):
                if modifiedObj.startOrEnd == "True":
                    modifiedObj.startOrEnd = True
                else:
                    modifiedObj.startOrEnd = False
            if modifiedObj.startOrEnd:
                edgePanel.startEdgeRdBtn.SetValue(True)
            else:
                edgePanel.endEdgeRdBtn.SetValue(True)
            if panelType == 0:
                edgePanel.riverBankCtrl.SetValue(modifiedObj.leftOrRight)

                if edgePanel.types[1] == modifiedObj.edgeType or (edgePanel.types[0] == modifiedObj.edgeType and not modifiedObj.startOrEnd):
                    edgePanel.riverBankCtrl.Disable()
            edgePanel.edgeTagmarkCtrl.SetValue(modifiedObj.distance)
            
            edgePanel.depthCtrl.SetValue(modifiedObj.depth)
            edgePanel.estimatedVelCtrl.SetValue(modifiedObj.corrMeanVelocity)
            if modifiedObj.depthAdjacent:
                edgePanel.depthAdjacentCkbox.SetValue(True)
                edgePanel.depthCtrl.Disable()
            if modifiedObj.velocityAdjacent:
                edgePanel.velAdjacentCkbox.SetValue(True)
                edgePanel.estimatedVelCtrl.Disable()

            if int(self.modifiedPanelArrayIndex) == len(self.panelObjs) - 1:
                edgePanel.nextBtn.Enable(False)
            if int(self.modifiedPanelArrayIndex) == 0:
                edgePanel.preBtn.Enable(False)

        else:
            panelPanel = self.subPanel.panel
            panelPanel.panelConditionCombox.SetValue(modifiedObj.panelCondition)
            self.subPanel.panel.PanelConditionUpdate()
            panelPanel.velocityCombo.SetValue(modifiedObj.velocityMethod)
            panelPanel.UpdateVelocityCorrection()
            panelPanel.UpdateGrid()

            if modifiedObj.currentMeter is not None:
                panelPanel.currentMeterCtrl.SetValue(modifiedObj.currentMeter)
            panelPanel.measurementTimeCtrl.SetValue(modifiedObj.time)
            panelPanel.panelTagMarkCtrl.SetValue(modifiedObj.distance)
            panelPanel.slopeCtrl.SetValue(modifiedObj.slop)
            panelPanel.interceptCtrl.SetValue(modifiedObj.intercept)
            panelPanel.slopeCtrl2.SetValue(modifiedObj.slop2)
            panelPanel.interceptCtrl2.SetValue(modifiedObj.intercept2)
            if not modifiedObj.slopBtn1:
                panelPanel.slopBtn2.SetValue(True)
                slope = modifiedObj.slop2
                intercept = modifiedObj.intercept2
            else:
                slope = modifiedObj.slop
                intercept = modifiedObj.intercept
            #open
            panelPanel.openDepthReadCtrl.SetValue(modifiedObj.openDepthRead)
            panelPanel.amountWeightCmbox.SetValue(modifiedObj.weight)
            panelPanel.weightOffsetCtrl.SetValue(modifiedObj.offset)
            panelPanel.wldlCorrectionCmbox.SetValue(modifiedObj.wldl)
            panelPanel.dryLineAngleCtrl.SetValue(modifiedObj.dryAngle)
            panelPanel.distWaterCtrl.SetValue(modifiedObj.distWaterSurface)
            panelPanel.dryLineCorrectionCtrl.SetValue(modifiedObj.dryCorrection)
            panelPanel.wetLineCorrectionCtrl.SetValue(modifiedObj.wetCorrection)
            panelPanel.OpenEffectiveDepthCtrl.SetValue(modifiedObj.openEffectiveDepth)
            #ice
            panelPanel.iceDepthReadCtrl.SetValue(modifiedObj.iceDepthRead)
            panelPanel.iceAssemblyCmbbox.SetValue(modifiedObj.iceAssembly)
            panelPanel.meterAboveCtrl.SetValue(modifiedObj.aboveFoot)
            panelPanel.meterBelowCtrl.SetValue(modifiedObj.belowFoot)
            panelPanel.distanceAboveCtrl.SetValue(modifiedObj.distAboveWeight)
            panelPanel.iceThickCtrl.SetValue(modifiedObj.iceThickness)
            panelPanel.iceThickAdjustedCtrl.SetValue(modifiedObj.iceThicknessAdjusted)
            panelPanel.waterSurfaceIceCtrl.SetValue(modifiedObj.wsBottomIce)
            panelPanel.waterIceAdjustCtrl.SetValue(modifiedObj.adjusted)
            if modifiedObj.slush:
                panelPanel.slushCkbox.SetValue(True)
            panelPanel.waterSurfaceSlushCtrl.SetValue(modifiedObj.wsBottomSlush)
            panelPanel.slushThicknessCtrl.SetValue(modifiedObj.thickness)
            panelPanel.iceEffectiveDepthCtrl.SetValue(modifiedObj.iceEffectiveDepth)

            # if modifiedObj.depthPanelLock:
            #     panelPanel.depthPanelLockCkbox.SetValue(True)


            panelPanel.obliqueCtrl.SetValue(modifiedObj.obliqueCorrection)
            panelPanel.velocityCorrectionCtrl.SetValue(modifiedObj.velocityCorrFactor)
            if modifiedObj.reverseFlow:
                panelPanel.reverseCkbox.SetValue(True)
            panelPanel.velocityGrid.SetCellValue(0, 5, modifiedObj.meanVelocity)
            panelPanel.velocityGrid.SetCellValue(0, 6, modifiedObj.corrMeanVelocity)

            pointVelsIsNone = True
            for i in range(len(modifiedObj.depths)):
                panelPanel.velocityGrid.SetCellValue(i, 0, modifiedObj.depths[i])
                panelPanel.velocityGrid.SetCellValue(i, 1, modifiedObj.depthObs[i])
                panelPanel.velocityGrid.SetCellValue(i, 2, modifiedObj.revs[i])
                panelPanel.velocityGrid.SetCellValue(i, 3, modifiedObj.revTimes[i])
                panelPanel.velocityGrid.SetCellValue(i, 4, str(modifiedObj.pointVels[i]))
                panelPanel.rawAtPointVel[i] = panelPanel.CalculateVel(modifiedObj.revs[i], modifiedObj.revTimes[i], slope, intercept, modifiedObj.reverseFlow)
                pointVelsIsNone = False

            # if modifiedObj.meanVelocity!="":
            #     panelPanel.openWaterPanel.Disable()
            #     panelPanel.icePanel.Disable()
            # panelPanel.SlopeRadioUpdate()


            if int(self.modifiedPanelArrayIndex) == len(self.panelObjs) - 1:
                panelPanel.nextBtn.Enable(False)
            if int(self.modifiedPanelArrayIndex) == 0:
                panelPanel.preBtn.Enable(False)

            panelPanel.BindingEvents()
        self.originalTagmark = float(modifiedObj.distance)
        frame.ShowModal()
        # subPanel.Layout()


    #Add object to object array and update the table
    def AddRow(self, obj, pos=None):
        self.pos = pos

        self.panelObjs.append(obj)
        # Check if it's decreasing/increasing order then sort accordingly
        if len(self.panelObjs)>2:
            if float(self.panelObjs[0].distance) > float(self.panelObjs[1].distance):
                self.panelObjs.sort(key=lambda f: float(f.distance), reverse=True)

            else:
                self.panelObjs.sort(key=lambda f: float(f.distance))
   

        # Update Panel Number
        c = 1
        for i in range(len(self.panelObjs)):
            if isinstance(self.panelObjs[i], PanelObj):
                self.panelObjs[i].panelNum = c
                c+=1
            if self.panelObjs[i]==obj:
                addedIndexInArray = i


        if len(self.panelObjs)<=2:
            self.UpdateObjInfoByRow(len(self.panelObjs) -1)
        elif addedIndexInArray>0 and addedIndexInArray<len(self.panelObjs)-1:
            self.UpdateObjInfoByRow(addedIndexInArray-1)
            self.UpdateObjInfoByRow(addedIndexInArray)
            self.UpdateObjInfoByRow(addedIndexInArray+1)
        elif addedIndexInArray==0:
            self.UpdateObjInfoByRow(addedIndexInArray)
            self.UpdateObjInfoByRow(addedIndexInArray+1)
        elif addedIndexInArray==len(self.panelObjs)-1:
            self.UpdateObjInfoByRow(addedIndexInArray-1)
            self.UpdateObjInfoByRow(addedIndexInArray)
        self.TransferFromObjToTable()

        for row in range(self.summaryTable.GetNumberRows()):
            if self.summaryTable.GetCellValue(row, 1) == str(obj.distance):
                addedIndexInTable = row

        # Same as Adjacent for Edge
        try:
            if len(self.panelObjs) > 1:
                if isinstance(self.panelObjs[addedIndexInArray-1], EdgeObj):
                    if ("start edge" in self.panelObjs[addedIndexInArray-1].panelNum.lower() or "end p" in self.panelObjs[addedIndexInArray-1].panelNum.lower()) and self.panelObjs[addedIndexInArray-1].depthAdjacent:
                        self.summaryTable.SetCellValue(addedIndexInArray-1, 3, self.summaryTable.GetCellValue(addedIndexInArray, 3))
                        self.summaryTable.SetCellValue(addedIndexInArray-1, 5, self.summaryTable.GetCellValue(addedIndexInArray, 5))
                        self.panelObjs[addedIndexInArray-1].depth = self.panelObjs[addedIndexInArray].depth
                        self.UpdateObjInfoByRow(addedIndexInArray-1)
                        self.TransferFromObjToTable()
                    if ("start edge" in self.panelObjs[addedIndexInArray-1].panelNum.lower() or "end p" in self.panelObjs[addedIndexInArray-1].panelNum.lower()) and self.panelObjs[addedIndexInArray-1].velocityAdjacent:
                        self.summaryTable.SetCellValue(addedIndexInArray-1, 10, self.summaryTable.GetCellValue(addedIndexInArray, 10))
                        self.panelObjs[addedIndexInArray-1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                        self.UpdateObjInfoByRow(addedIndexInArray-1)
                        self.TransferFromObjToTable()

                if not len(self.panelObjs) == addedIndexInArray+1:
                    if isinstance(self.panelObjs[addedIndexInArray+1], EdgeObj):
                        if ("end edge" in self.panelObjs[addedIndexInArray+1].panelNum.lower() or "start p" in self.panelObjs[addedIndexInArray+1].panelNum.lower()) and self.panelObjs[addedIndexInArray+1].depthAdjacent:
                            if isinstance(self.panelObjs[addedIndexInArray], PanelObj):
                                if len(self.panelObjs[addedIndexInArray].depths) == 1:
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 2:
                                    self.summaryTable.SetCellValue(addedIndexInTable+2, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+2, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 3:
                                    self.summaryTable.SetCellValue(addedIndexInTable+3, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+3, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                            if isinstance(self.panelObjs[addedIndexInArray], EdgeObj):
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                        if ("end edge" in self.panelObjs[addedIndexInArray+1].panelNum.lower() or "start p" in self.panelObjs[addedIndexInArray+1].panelNum.lower()) and self.panelObjs[addedIndexInArray+1].velocityAdjacent:
                            if isinstance(self.panelObjs[addedIndexInArray], PanelObj):
                                if len(self.panelObjs[addedIndexInArray].depths) == 1:
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 2:
                                    self.summaryTable.SetCellValue(addedIndexInTable+2, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 3:
                                    self.summaryTable.SetCellValue(addedIndexInTable+3, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                            if isinstance(self.panelObjs[addedIndexInArray], EdgeObj):
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                if isinstance(self.panelObjs[addedIndexInArray], EdgeObj):
                    if ("end edge" in self.panelObjs[addedIndexInArray].panelNum.lower() or "start p" in self.panelObjs[addedIndexInArray].panelNum.lower()) and self.panelObjs[addedIndexInArray].depthAdjacent:
                        if isinstance(self.panelObjs[addedIndexInArray-1], PanelObj):
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 1:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-1, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-1, 5))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 2:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-2, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-2, 5))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 3:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-3, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-3, 5))
                        if isinstance(self.panelObjs[addedIndexInArray-1], EdgeObj):
                            self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-1, 3))
                            self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-1, 5))
                        self.panelObjs[addedIndexInArray].depth = self.panelObjs[addedIndexInArray-1].depth
                        self.UpdateObjInfoByRow(addedIndexInArray)
                        self.TransferFromObjToTable()

                    if ("end edge" in self.panelObjs[addedIndexInArray].panelNum.lower() or "start p" in self.panelObjs[addedIndexInArray].panelNum.lower()) and self.panelObjs[addedIndexInArray].velocityAdjacent:
                        if isinstance(self.panelObjs[addedIndexInArray-1], PanelObj):
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 1:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-1, 10))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 2:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-2, 10))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 3:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-3, 10))
                        if isinstance(self.panelObjs[addedIndexInArray-1], EdgeObj):
                            self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-1, 10))
                        self.panelObjs[addedIndexInArray].corrMeanVelocity = self.panelObjs[addedIndexInArray-1].corrMeanVelocity
                        self.UpdateObjInfoByRow(addedIndexInArray)
                        self.TransferFromObjToTable()
                    if ("start edge" in self.panelObjs[addedIndexInArray].panelNum.lower() or "end p" in self.panelObjs[addedIndexInArray].panelNum.lower()) and self.panelObjs[addedIndexInArray].depthAdjacent:
                        if isinstance(self.panelObjs[addedIndexInArray+1], PanelObj):
                            if len(self.panelObjs[addedIndexInArray+1].depths) == 1:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable+1, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable+1, 5))
                            if len(self.panelObjs[addedIndexInArray+1].depths) == 2:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable+2, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable+2, 5))
                            if len(self.panelObjs[addedIndexInArray+1].depths) == 3:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable+3, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable+3, 5))
                        if isinstance(self.panelObjs[addedIndexInArray+1], EdgeObj):
                            self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable+1, 3))
                            self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable+1, 5))
                        self.panelObjs[addedIndexInArray].depth = self.panelObjs[addedIndexInArray+1].depth
                        self.UpdateObjInfoByRow(addedIndexInArray)
                        self.TransferFromObjToTable()
                    if ("start edge" in self.panelObjs[addedIndexInArray].panelNum.lower() or "end p" in self.panelObjs[addedIndexInArray].panelNum.lower()) and self.panelObjs[addedIndexInArray].velocityAdjacent:
                        if isinstance(self.panelObjs[addedIndexInArray+1], PanelObj):
                            if len(self.panelObjs[addedIndexInArray+1].depths) == 1:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable+1, 10))
                            if len(self.panelObjs[addedIndexInArray+1].depths) == 2:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable+2, 10))
                            if len(self.panelObjs[addedIndexInArray+1].depths) == 3:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable+3, 10))
                        if isinstance(self.panelObjs[addedIndexInArray+1], EdgeObj):
                            self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable+1, 10))
                        self.panelObjs[addedIndexInArray].corrMeanVelocity = self.panelObjs[addedIndexInArray+1].corrMeanVelocity
                        self.UpdateObjInfoByRow(addedIndexInArray)
                        self.TransferFromObjToTable()
        except Exception as e:
            print e

        self.RefreshFlow()
        self.lastObj = obj
        for i in self.panelObjs:
            #i.ToString()
            # Calculate Summary if end edge is detected
            if "End Edge" == i.panelNum:
                self.addBtn.Enable(False)
                self.GetParent().header.CalculateSummary()
                break


        self.CalculatePolority()

        # if obj.panelNum == "Start Pier":
        #     adding(endPier=True)


    #Recalculate the width, mean velocity, area, discharge, flow if anything changed in the given panel
    def UpdateObjInfoByRow(self, index):

        if index > -1:

            currentObj = self.panelObjs[index]

            if isinstance(currentObj, EdgeObj):
                start = currentObj.startOrEnd
                edgeType = currentObj.edgeType
                panelNum = currentObj.panelNum


                if panelNum == "Start Edge" or panelNum == "End P / ISL":


                    if index < len(self.panelObjs) - 1:

                        if currentObj.distance != "" and self.panelObjs[index+1].distance != "":
                            currentObj.width = abs(float(currentObj.distance) - float(self.panelObjs[index+1].distance)) / 2
                        else:
                            currentObj.width = ""
                        nextObj = self.panelObjs[index+1]
                        if isinstance(nextObj, PanelObj) and index < len(self.panelObjs) - 2:
                            nextNextObj = self.panelObjs[index+2]
                            if currentObj.distance != "" and nextNextObj.distance != "":
                                nextObj.width = abs(float(currentObj.distance) - float(nextNextObj.distance)) / 2
                            else:
                                nextObj.width = ""
                    else:
                        currentObj.width = ""



                elif panelNum == "End Edge" or panelNum == "Start P / ISL":
                    if index > 0:
                        if currentObj.distance != "" and self.panelObjs[index-1].distance != "":
                            currentObj.width = abs(float(currentObj.distance) - float(self.panelObjs[index-1].distance)) / 2
                        else:
                            currentObj.width = ""
                        preObj = self.panelObjs[index-1]
                        if isinstance(preObj, PanelObj) and index > 1:
                            prePreObj = self.panelObjs[index-2]
                            if currentObj.distance != "" and prePreObj.distance != "":
                                preObj.width = abs(float(currentObj.distance) - float(prePreObj.distance)) / 2
                            else:
                                preObj.width = ""
                    else:
                        currentObj.width = ""


            else:
                #check if the row has next and previous rows, update current row
                if index < len(self.panelObjs) - 1 and index > 0:

                        nextObj = self.panelObjs[index+1]
                        preObj = self.panelObjs[index-1]
                        if nextObj.distance != "" and preObj.distance != "":
                            currentObj.width = abs(float(nextObj.distance) - float(preObj.distance)) / 2
                        else:
                            currentObj.width = ""
                else:
                    currentObj.width = ""
                #check next, update next
                if index < len(self.panelObjs) - 1:
                    nextObj = self.panelObjs[index+1]
                    #if next is an edge
                    if isinstance(nextObj, EdgeObj):
                        if currentObj.distance != "" and nextObj.distance != "":
                            nextObj.width = abs(float(currentObj.distance) - float(nextObj.distance)) / 2
                        else:
                            nextObj.width = ""
                    #if next is a panel
                    else:
                        if index < len(self.panelObjs) - 2:
                            nextNextObj = self.panelObjs[index+2]
                            if currentObj.distance != "" and nextNextObj.distance != "":
                                nextObj.width = abs(float(currentObj.distance) - float(nextNextObj.distance)) / 2
                            else:
                                nextObj.width = ""

                #check previous, update previous
                if index > 0:

                    preObj = self.panelObjs[index-1]
                    #if previous is an edge
                    if isinstance(preObj, EdgeObj):
                        if currentObj.distance != "" and preObj.distance != "":

                            preObj.width = abs(float(currentObj.distance) - float(preObj.distance)) / 2
                        else:
                            preObj.width = ""
                    #if previous is a panel
                    else:
                        if index > 1:
                            prePreObj = self.panelObjs[index-2]
                            if currentObj.distance != "" and prePreObj.distance != "":
                                preObj.width = abs(float(currentObj.distance) - float(prePreObj.distance)) / 2
                            else:
                                preObj.width = ""


            #Recalculate the area and discharge
            self.UpdateObjAreaAndDischarge(index)
            if index > 0:
                self.UpdateObjAreaAndDischarge(index - 1)
            if index < len(self.panelObjs) - 1:
                self.UpdateObjAreaAndDischarge(index + 1)

            #for i in self.panelObjs:
            #    i.ToString()



    def UpdateObjAreaAndDischarge(self, index):

        obj = self.panelObjs[index]
        if isinstance(obj, PanelObj):
            if obj.panelCondition == "Ice":
                if obj.width != "" and obj.iceEffectiveDepth != "":
                    rawArea = float(obj.width) * float(obj.iceEffectiveDepth)
                    #obj.area = sigfig.round_sig(float(obj.width) * float(obj.iceEffectiveDepth),3)
                    obj.area = str(float(obj.width) * float(obj.iceEffectiveDepth))
                    if obj.corrMeanVelocity != "":
                        #obj.discharge = sigfig.round_sig(rawArea * float(obj.corrMeanVelocity),3)
                        obj.discharge = str(rawArea * float(obj.corrMeanVelocity))
                    else:
                        obj.discharge = ""
                else:
                    obj.area = ""
                    obj.discharge = ""

            elif obj.panelCondition == "Open":
                if obj.width != "" and obj.openEffectiveDepth != "":
                    rawArea = float(obj.width) * float(obj.openEffectiveDepth)
                    #obj.area = sigfig.round_sig(float(obj.width) * float(obj.openEffectiveDepth),3)
                    obj.area = str(float(obj.width) * float(obj.openEffectiveDepth))

                    if obj.corrMeanVelocity != "" and float(obj.corrMeanVelocity) != 0.0:

                        obj.discharge = str(rawArea * float(obj.corrMeanVelocity))


                    # elif obj.corrMeanVelocity != "" and float(obj.corrMeanVelocity) != 0.0:
                    #     obj.discharge = str(rawArea * float(obj.corrMeanVelocity))
                    else:
                        obj.discharge = ""
                else:
                    obj.area = ""
                    obj.discharge = ""
        else:
            if obj.width != "" and obj.depth != "":
                rawArea = float(obj.width) * float(obj.depth)
                #obj.area = sigfig.round_sig(float(obj.width) * float(obj.depth),3)
                obj.area = str(float(obj.width) * float(obj.depth))
                if obj.corrMeanVelocity != "":
                    obj.discharge = rawArea * float(obj.corrMeanVelocity)
                else:
                    obj.discharge = ""
            else:
                obj.area = ""
                obj.discharge = ""




    def TransferFromObjToTable(self):
        counter = 0
        coloured = False
        colour1 = (220,230,240)
        colour2 = (255,245,235)
        self.summaryTable.ClearGrid()

        rows = self.summaryTable.GetNumberRows()
        rowsNeeded = self.CountNumberOfRows()



        for i in range(rowsNeeded - rows):
            self.summaryTable.AppendRows()

        for i in range(rows - rowsNeeded):
            self.summaryTable.DeleteRows()

        for obj in self.panelObjs:
            oldCounter = counter
            if isinstance(obj, EdgeObj):
                # obj.ToString()
                start = obj.startOrEnd
                edgeType = obj.panelNum
                # When opening xml, start will be string. So identify that.
                if isinstance(start, str):
                    if start=="True":
                        start=True
                    elif start=="False":
                        start=False

                if start:
                    if "Edge" in edgeType:

                        panelType = "Start Edge"
    
                        if coloured:
                            for col in range(14):
                                self.summaryTable.SetCellBackgroundColour(oldCounter, col, colour1)
                        else:
                            for col in range(14):
                                self.summaryTable.SetCellBackgroundColour(oldCounter, col, "white")
                        coloured = not coloured
                    else:
                        panelType = "Start P / ISL"
                        for col in range(14):
                            self.summaryTable.SetCellBackgroundColour(counter, col, colour2)
                        coloured = False

                else:
                    if "Edge" in edgeType:
                        panelType = "End Edge"
         
                        if coloured:
                            for col in range(14):
                                self.summaryTable.SetCellBackgroundColour(oldCounter, col, colour1)
                        else:
                            for col in range(14):
                                self.summaryTable.SetCellBackgroundColour(oldCounter, col, "white")
                        coloured = not coloured
                    else:
                        panelType = "End P / ISL"
                        for col in range(14):
                            self.summaryTable.SetCellBackgroundColour(counter, col, colour2)
                        coloured = False



                self.summaryTable.SetCellValue(counter, 0, panelType)
                self.summaryTable.SetCellValue(counter, 1, obj.distance)
                self.summaryTable.SetCellValue(counter, 3, obj.depth)
                self.summaryTable.SetCellValue(counter, 5, obj.depth)
                self.summaryTable.SetCellValue(counter, 10, obj.corrMeanVelocity)




            elif isinstance(obj, PanelObj):

                self.summaryTable.SetCellValue(counter, 0, str(obj.panelNum))
                self.summaryTable.SetCellValue(counter, 1, obj.distance)
                self.Layout()

                if obj.panelCondition == "Open":
                    self.summaryTable.SetCellValue(counter, 3, str(obj.openDepthRead))
                    self.summaryTable.SetCellValue(counter, 5, obj.openEffectiveDepth)
                else:
                    self.summaryTable.SetCellValue(counter, 3, obj.iceDepthRead)
                    self.summaryTable.SetCellValue(counter, 5, obj.iceEffectiveDepth)
                    if obj.wsBottomSlush != "":

                        self.summaryTable.SetCellValue(counter, 4, obj.wsBottomSlush)
                    else:
                        self.summaryTable.SetCellValue(counter, 4, obj.wsBottomIce)

                self.summaryTable.SetCellValue(counter, 10, obj.corrMeanVelocity)



                for i in range(len(obj.depths)):


                    self.summaryTable.SetCellValue(counter, 6, obj.depthObs[i])
                    self.summaryTable.SetCellValue(counter, 7, obj.revs[i])
                    self.summaryTable.SetCellValue(counter, 8, obj.revTimes[i])
                    self.summaryTable.SetCellValue(counter, 9, str(obj.pointVels[i]))

                    if i == len(obj.depths) - 1:
                        break

                    counter += 1
                    if coloured:
                        for col in range(14):
                            self.summaryTable.SetCellBackgroundColour(counter, col, colour1)
                    else:
                        for col in range(14):
                            self.summaryTable.SetCellBackgroundColour(counter, col, "white")

                if coloured:
                    for col in range(14):
                        self.summaryTable.SetCellBackgroundColour(oldCounter, col, colour1)
                else:
                    for col in range(14):
                        self.summaryTable.SetCellBackgroundColour(oldCounter, col, "white")
                coloured = not coloured



            self.summaryTable.SetCellValue(oldCounter, 12, str(obj.discharge))
            self.summaryTable.SetCellValue(oldCounter, 11, obj.area)


            self.summaryTable.SetCellValue(oldCounter, 2, str(obj.width))





            counter += 1


    def CountNumberOfRows(self):
        counter = 0
        for i in self.panelObjs:
            if isinstance(i, EdgeObj):
                counter += 1
            else:
                for j in range(len(i.depths)):
                    counter += 1
        return counter



    #Add object to object array and update the table
    def UpdateRow(self, obj, pos=None):

        self.pos = pos


        self.panelObjs[self.modifiedPanelArrayIndex] = obj

        # Check if it's decreasing/increasing order then sort accordingly
        if len(self.panelObjs)>2:
            if float(self.panelObjs[0].distance) > float(self.panelObjs[1].distance):
                self.panelObjs.sort(key=lambda f: float(f.distance), reverse=True)
            else:
                self.panelObjs.sort(key=lambda f: float(f.distance))

        # Update Panel Number
        c = 1
        for i in range(len(self.panelObjs)):
            if isinstance(self.panelObjs[i], PanelObj):
                self.panelObjs[i].panelNum = c
                c+=1
        #    if self.panelObjs[i] == obj:
        #        rearrangedIndex = i

        # Calculate width, area, discharge for ALL panels (this could be better)
        for i in range(len(self.panelObjs)):
            self.UpdateObjInfoByRow(i)


        self.TransferFromObjToTable()
        for i in range(len(self.panelObjs)):
            if obj==self.panelObjs[i]:
                addedIndexInArray = i
        for row in range(self.summaryTable.GetNumberRows()):
            if self.summaryTable.GetCellValue(row, 1) == str(obj.distance):
                addedIndexInTable = row

        # Same as Adjacent for Edge
        try:
            if len(self.panelObjs) > 1:
                if isinstance(self.panelObjs[addedIndexInArray-1], EdgeObj):
                    if ("start edge" in self.panelObjs[addedIndexInArray-1].panelNum.lower() or "end p" in self.panelObjs[addedIndexInArray-1].panelNum.lower()) and self.panelObjs[addedIndexInArray-1].depthAdjacent:
                        self.summaryTable.SetCellValue(addedIndexInArray-1, 3, self.summaryTable.GetCellValue(addedIndexInArray, 3))
                        self.summaryTable.SetCellValue(addedIndexInArray-1, 5, self.summaryTable.GetCellValue(addedIndexInArray, 5))
                        self.panelObjs[addedIndexInArray-1].depth = self.panelObjs[addedIndexInArray].depth
                        self.UpdateObjInfoByRow(addedIndexInArray-1)
                        self.TransferFromObjToTable()
                    if ("start edge" in self.panelObjs[addedIndexInArray-1].panelNum.lower() or "end p" in self.panelObjs[addedIndexInArray-1].panelNum.lower()) and self.panelObjs[addedIndexInArray-1].velocityAdjacent:
                        self.summaryTable.SetCellValue(addedIndexInArray-1, 10, self.summaryTable.GetCellValue(addedIndexInArray, 10))
                        self.panelObjs[addedIndexInArray-1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                        self.UpdateObjInfoByRow(addedIndexInArray-1)
                        self.TransferFromObjToTable()

                if not len(self.panelObjs) == addedIndexInArray+1:
                    if isinstance(self.panelObjs[addedIndexInArray+1], EdgeObj):
                        if ("end edge" in self.panelObjs[addedIndexInArray+1].panelNum.lower() or "start p" in self.panelObjs[addedIndexInArray+1].panelNum.lower()) and self.panelObjs[addedIndexInArray+1].depthAdjacent:
                            if isinstance(self.panelObjs[addedIndexInArray], PanelObj):
                                if len(self.panelObjs[addedIndexInArray].depths) == 1:
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 2:
                                    self.summaryTable.SetCellValue(addedIndexInTable+2, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+2, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 3:
                                    self.summaryTable.SetCellValue(addedIndexInTable+3, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+3, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                            if isinstance(self.panelObjs[addedIndexInArray], EdgeObj):
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 3, self.summaryTable.GetCellValue(addedIndexInTable, 3))
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 5, self.summaryTable.GetCellValue(addedIndexInTable, 5))
                                    self.panelObjs[addedIndexInArray+1].depth = self.panelObjs[addedIndexInArray].depth
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                        if ("end edge" in self.panelObjs[addedIndexInArray+1].panelNum.lower() or "start p" in self.panelObjs[addedIndexInArray+1].panelNum.lower()) and self.panelObjs[addedIndexInArray+1].velocityAdjacent:
                            if isinstance(self.panelObjs[addedIndexInArray], PanelObj):
                                if len(self.panelObjs[addedIndexInArray].depths) == 1:
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 2:
                                    self.summaryTable.SetCellValue(addedIndexInTable+2, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                                if len(self.panelObjs[addedIndexInArray].depths) == 3:
                                    self.summaryTable.SetCellValue(addedIndexInTable+3, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                            if isinstance(self.panelObjs[addedIndexInArray], EdgeObj):
                                    self.summaryTable.SetCellValue(addedIndexInTable+1, 10, self.summaryTable.GetCellValue(addedIndexInTable, 10))
                                    self.panelObjs[addedIndexInArray+1].corrMeanVelocity = self.panelObjs[addedIndexInArray].corrMeanVelocity
                                    self.UpdateObjInfoByRow(addedIndexInArray+1)
                                    self.TransferFromObjToTable()
                if isinstance(obj, EdgeObj):
                    if ("end edge" in str(obj.panelNum).lower() or "start p" in str(obj.panelNum).lower()) and obj.depthAdjacent:
                        if isinstance(self.panelObjs[addedIndexInArray-1], PanelObj):
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 1:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-1, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-1, 5))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 2:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-2, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-2, 5))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 3:
                                self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-3, 3))
                                self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-3, 5))
                        if isinstance(self.panelObjs[addedIndexInArray-1], EdgeObj):
                            self.summaryTable.SetCellValue(addedIndexInTable, 3, self.summaryTable.GetCellValue(addedIndexInTable-1, 3))
                            self.summaryTable.SetCellValue(addedIndexInTable, 5, self.summaryTable.GetCellValue(addedIndexInTable-1, 5))
                        self.panelObjs[addedIndexInArray].depth = self.panelObjs[addedIndexInArray-1].depth
                        self.UpdateObjInfoByRow(addedIndexInArray)
                        self.TransferFromObjToTable()

                    if ("end edge" in str(obj.panelNum).lower() or "start p" in str(obj.panelNum).lower()) and obj.velocityAdjacent:
                        if isinstance(self.panelObjs[addedIndexInArray-1], PanelObj):
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 1:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-1, 10))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 2:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-2, 10))
                            if len(self.panelObjs[addedIndexInArray-1].depths) == 3:
                                self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-3, 10))
                        if isinstance(self.panelObjs[addedIndexInArray-1], EdgeObj):
                            self.summaryTable.SetCellValue(addedIndexInTable, 10, self.summaryTable.GetCellValue(addedIndexInTable-1, 10))
                        self.panelObjs[addedIndexInArray].corrMeanVelocity = self.panelObjs[addedIndexInArray-1].corrMeanVelocity
                        self.UpdateObjInfoByRow(addedIndexInArray)
                        self.TransferFromObjToTable()
        except Exception as e:
            print e

        for i in self.panelObjs:
            if "end edge"==i.panelNum:
                self.GetParent().header.CalculateSummary()
                break

        self.RefreshFlow()
        #self.CalculateSummary()


    def RefreshFlow(self):
        total = 0
        indexDischarge = {}



        for i in range(len(self.panelObjs)):
            discharge = self.panelObjs[i].discharge
            if discharge != "":
                total += float(discharge)
                indexDischarge[i] = float(discharge)


        if total != 0:
            for key in indexDischarge.keys():
                flow = indexDischarge.get(key) / total * 100
                self.panelObjs[key].flow = round(flow, 1)
                for row in range(self.summaryTable.GetNumberRows()):
                    if self.summaryTable.GetCellValue(row, 0) == str(self.panelObjs[key].panelNum):
                        self.summaryTable.SetCellValue(row, 13, str(flow))
                        if flow>10:
                            self.summaryTable.SetCellTextColour(row, 13, "red")
                        else:
                            self.summaryTable.SetCellTextColour(row, 13, "black")


    #shift the rows from the index number given inclusively move by numbers of lines
    #row: the index of row start to move inclusively
    #lines: positive number to the bottom, negative number to the above
    def Shift(self, row, lines):


        oldTableSize = self.summaryTable.GetNumberRows()
        #shifting down(expand table)
        if lines > 0:
            for i in range(lines):
                self.summaryTable.AppendRows()

            newHeight = self.summaryTable.GetSize().GetHeight() + lines * self.cellHeight
            self.summaryTable.SetSize((-1, newHeight))
            self.Layout()



            #clear the table
            for i in range(self.summaryTable.GetNumberRows()):
                for j in range(14):
                    self.summaryTable.SetCellValue(i, j, "")

        elif lines < 0:
            lines = abs(lines)

            self.summaryTable.DeleteRows(self.summaryTable.GetNumberRows()-lines, lines)






    def OrderedTimes(self):
        times = []
        for i in self.panelObjs:
            times.append(i.time)
        return sorted(times)

    def GetNextTagMark(self):
        if len(self.panelObjs) < 2:
            return ''
        else:
            secondLast = float(self.panelObjs[-2].distance)
            last = float(self.panelObjs[-1].distance)
            distance = last * 2 - secondLast 
            return str(distance)


    def CalculatePolority(self):

        if len(self.panelObjs) > 2 or (len(self.panelObjs) > 1 and self.panelObjs[-1].panelNum == "End Edge"):

            self.increasingPolority = float(self.panelObjs[1].distance) > float(self.panelObjs[0].distance)
        else:
            self.increasingPolority = None


    def IsValidTagMark(self, tagmark, arrayIndex, pid=None, modify=0, startEdge=False, endEdge=False, startPier=False, endPier=False):

        if len(self.panelObjs) == 0:
            return 0
        
        #check boundary between edges
        if self.increasingPolority is not None and len(self.panelObjs) > 1 and self.panelObjs[-1].panelNum == "End Edge":
            if self.increasingPolority:
                if float(tagmark) < float(self.panelObjs[0].distance) or float(tagmark) > float(self.panelObjs[-1].distance):
                    dlg = wx.MessageDialog(None, "Panel tagmark is out of the boundary", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                    dlg.ShowModal()
                    return 7
            else:
                if float(tagmark) > float(self.panelObjs[0].distance) or float(tagmark) < float(self.panelObjs[-1].distance):
                    dlg = wx.MessageDialog(None, "Panel tagmark is out of the boundary", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                    dlg.ShowModal()
                    return 7


        for index, obj in enumerate(self.panelObjs):
            #Between Pier check
            if not startPier and not endPier:

                if "Start P" in str(obj.panelNum):
                    if self.increasingPolority:
                        if float(tagmark) > float(obj.distance) and float(tagmark) < float(self.panelObjs[index+1].distance):
                            dlg = wx.MessageDialog(None, "Panel tagmark cannot between piers", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                            dlg.ShowModal()
                            return 1
                    else:
                        if float(tagmark) < float(obj.distance) and float(tagmark) > float(self.panelObjs[index+1].distance):
                            dlg = wx.MessageDialog(None, "Panel tagmark cannot between piers", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                            dlg.ShowModal()
                            return 1


            #Duplicate Check

            if (modify != 2 and float(tagmark) == float(obj.distance)) or \
            (modify == 2 and float(tagmark) == float(obj.distance) and arrayIndex != index and not endPier):
                # print "====----------------------"
                # print "modify", modify
                # print "arrayIndex", arrayIndex
                # print "index", index
                # print "endPier", endPier 
                dlg = wx.MessageDialog(None, "Panel tagmark cannot be duplicated", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                return 2
        #Polority Check for adding
        if modify == 0:           
            if self.increasingPolority is not None and ((self.increasingPolority and float(self.panelObjs[-1].distance) > float(tagmark))\
                 or (self.increasingPolority == False and float(self.panelObjs[-1].distance) < float(tagmark))):
                    dlg = wx.MessageDialog(None, "Panel tagmark doesn't follow the polority", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                    dlg.ShowModal()
                    return 3

        #polority check for editing
        else:
            if self.increasingPolority == True is not None and not startEdge:
                if (self.increasingPolority == True and float(tagmark) < float(self.panelObjs[0].distance)) or\
                        (self.increasingPolority == False and float(tagmark) > float(self.panelObjs[0].distance)):
                    dlg = wx.MessageDialog(None, "Panel tagmark is out of the boundary of Start Edge", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                    dlg.ShowModal()
                    return 8


        

        #check only for end Edge
        if endEdge:   
            #Check number of edges
            counter = 0
            for obj in self.panelObjs:
                if isinstance(obj, EdgeObj) and obj.edgeType == "Edge":
                    counter += 1

                #check end edge boundary
                if isinstance(obj, PanelObj):
                    if (self.increasingPolority == True and float(tagmark) < float(obj.distance)) \
                        or (self.increasingPolority == False and float(tagmark) > float(obj.distance)):
                        dlg = wx.MessageDialog(None, "Invalid tagmark for end edge", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                        dlg.ShowModal()
                        return 5
            if counter > 1 and modify == 0:
                dlg = wx.MessageDialog(None, "Number of edges exceeded", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                return 4

        #check startEdge boundary
        if startEdge and modify != 0 and self.increasingPolority is not None:
            for obj in self.panelObjs:
                if isinstance(obj, PanelObj):
                    if (self.increasingPolority and float(tagmark) > float(obj.distance)) \
                        or (self.increasingPolority == False and float(tagmark) < float(obj.distance)):
                        dlg = wx.MessageDialog(None, "The start edge is out of the boundary", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                        dlg.ShowModal()
                        return 6

        #Check only for end Pier
        if endPier:

            if pid is not None:
                for index, obj in enumerate(self.panelObjs):
                    if pid == obj.pid:
                        if (self.increasingPolority and float(tagmark) < float(obj.distance)) or\
                         (self.increasingPolority == False and float(tagmark) > float(obj.distance)):
                            dlg = wx.MessageDialog(None, "The end pier is out of the boundary 6", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                            dlg.ShowModal()
                            return 18

                        if modify == 0 or modify == 1:
                            if (index < len(self.panelObjs) - 1) and ((self.increasingPolority and float(tagmark) > float(self.panelObjs[index+1].distance)) or\
                                (self.increasingPolority == False and float(tagmark) < float(self.panelObjs[index+1].distance))):


                                dlg = wx.MessageDialog(None, "The end pier is out of the boundary 7", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return 19
                        else:
                            if (index < len(self.panelObjs) - 2) and ((self.increasingPolority and float(tagmark) > float(self.panelObjs[index+2].distance)) or\
                                (self.increasingPolority == False and float(tagmark) < float(self.panelObjs[index+2].distance))):

                                dlg = wx.MessageDialog(None, "The end pier is out of the boundary 8", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return 20
                        break

        

        #check only for start Pier
        if startPier:
            #modify
            if modify == 2 and arrayIndex != -1:
                if arrayIndex < len(self.panelObjs) - 1:
                    if "End P" in str(self.panelObjs[arrayIndex + 1].panelNum):
                        #less than end pier
                        if self.increasingPolority == True:
                            if float(tagmark) > float(self.panelObjs[arrayIndex + 1].distance):
                                dlg = wx.MessageDialog(None, "The start pier is out of the boundary 1", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return 9 
                        #greater than end pier
                        elif self.increasingPolority == False:
                            if float(tagmark) < float(self.panelObjs[arrayIndex + 1].distance):
                                dlg = wx.MessageDialog(None, "The start pier is out of the boundary 2", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return 10
                
                        #greater than previous panel
                        if self.increasingPolority == True:
                            if float(self.panelObjs[arrayIndex - 1].distance) > float(tagmark):
                                dlg = wx.MessageDialog(None, "The start pier is out of the boundary 3", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return 11

                        #less than previous panel
                        elif self.increasingPolority == False:
                            if float(self.panelObjs[self.modifiedPanelArrayIndex - 1].distance) < float(tagmark):
                                dlg = wx.MessageDialog(None, "The start pier is out of the boundary 4", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return 12


        return 0




def main():
    app = wx.App()

    frame = wx.Frame(None, size=(1200, 200))
    MidsectionSummaryTable(frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
