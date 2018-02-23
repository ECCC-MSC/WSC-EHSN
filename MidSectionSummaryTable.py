# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import sigfig
from wx.grid import *
from MidSectionSubPanel import *
from MidSectionSubPanelObj import *



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
        self.panelType = 1
        self.numberOfPanels = 0

        # self.summaryTable.GetNumberRows() = 0
        self.panelObjs = []
        self.lastPanelObj = None
        self.lastObj = None
        self.pos = None
        self.numberOfPanelObjs = 0

        self.modifiedPanelId = -1
        self.modifiedPanelIndex = -1
        self.cellHeight = 21


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
        # self.summaryTable.HideRowLabels()

        #self.summaryTable.SetColFormatFloat(1, precision=3)
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
        # print self.summaryTable.GetSize()
        # print self.summaryTable.GetSize().GetHeight()


        self.addBtn = wx.Button(self, label="+", size=(-1, -1))
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddBtn)
        layout.Add(self.summaryTable, 0, wx.EXPAND|wx.ALL, 20)
        layout.Add(self.addBtn, 0, wx.ALL, 20)

    def OnRightClick(self, event):
        # print event.GetRow()
        # print event.GetPosition()
        # if event.GetCol() == 0:
        print "###############################"
        for i in self.panelObjs:
            i.ToString()
        index = event.GetRow()
        print "##INDEX##"
        print index
        objIndex = ""
        if len(self.panelObjs) > 0:
            for i in reversed(range(index + 1)):
                print "i: " + str(i)
                if self.summaryTable.GetCellValue(i, 0) != "":
                    for j, obj in enumerate(self.panelObjs):
                        print "obj.panelNum: "+str(obj.panelNum)
                        print  "self.summaryTable.GetCellValue(i, 0): "+str(self.summaryTable.GetCellValue(i, 0))
                        if str(obj.panelNum) == self.summaryTable.GetCellValue(i, 0) and float(obj.distance) == float(self.summaryTable.GetCellValue(i, 1)):
                            self.modifiedPanelId = j
                            self.modifiedPanelIndex = i
                            break
                    break
        if self.modifiedPanelId != "":
            print "object index in the array is: ", self.modifiedPanelId
            print "object index in the table is: ", self.modifiedPanelIndex
        print self.panelObjs
        print self.panelObjs[self.modifiedPanelId]
        print self.panelObjs[self.modifiedPanelId].panelNum



            #     print "Click on panel#: ", self.panelObjs[event.GetRow()].panelId
            #     print "Click on type#: ", self.panelObjs[event.GetRow()].panelType
            #     self.modifiedPanelId = self.panelObjs[event.GetRow()].panelId
            #     self.panelType = self.panelObjs[event.GetRow()].panelType
        #self.originalColour = self.summaryTable.GetCellBackgroundColour(self.modifiedPanelIndex,0)
        #for i in range(self.summaryTable.GetNumberCols()):
        #    print "change color"
        #    self.summaryTable.SetCellBackgroundColour(self.modifiedPanelIndex,i,'yellow')
        # Highlight when right clicked
        self.summaryTable.ClearSelection()
        if self.panelObjs[self.modifiedPanelId].panelType == 0:
            self.summaryTable.SelectRow(self.modifiedPanelIndex)
        elif len(self.panelObjs[self.modifiedPanelId].depths) == 1:
            self.summaryTable.SelectRow(self.modifiedPanelIndex)
        elif len(self.panelObjs[self.modifiedPanelId].depths) == 2:
            self.summaryTable.SelectRow(self.modifiedPanelIndex, addToSelected=True)
            self.summaryTable.SelectRow(self.modifiedPanelIndex+1, addToSelected=True)
        elif len(self.panelObjs[self.modifiedPanelId].depths) == 3:
            self.summaryTable.SelectRow(self.modifiedPanelIndex, addToSelected=True)
            self.summaryTable.SelectRow(self.modifiedPanelIndex+1, addToSelected=True)
            self.summaryTable.SelectRow(self.modifiedPanelIndex+2, addToSelected=True)
        #self.summaryTable.DeselectRow(self.modifiedPanelIndex)
        self.dlg = wx.Dialog(self, title="Editing Menu", size=(150, 170), pos=(500, 400))
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        self.dlg.SetSizer(dlgSizer)
        addBtn = wx.Button(self.dlg, label="Add/Insert")
        deleteBtn = wx.Button(self.dlg, label="Delete")
        # deleteBtn.SetBackgroundColour("red")
        # insertBtn = wx.Button(self.dlg, label="Insert")
        modifyBtn = wx.Button(self.dlg, label="Modify")

        addBtn.Bind(wx.EVT_BUTTON, self.OnAdd)
        deleteBtn.Bind(wx.EVT_BUTTON, self.OnDelete)
        # insertBtn.Bind(wx.EVT_BUTTON, self.OnInsert)
        modifyBtn.Bind(wx.EVT_BUTTON, self.OnModify)


        dlgSizer.Add(addBtn, 1, wx.EXPAND)
        dlgSizer.Add(modifyBtn, 1, wx.EXPAND)
        # dlgSizer.Add(insertBtn, 1, wx.EXPAND)
        dlgSizer.Add(deleteBtn, 1, wx.EXPAND)


        self.dlg.ShowModal()


    def OnDelete(self, event):
        print "On Delete"
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




            removedObj = self.panelObjs.pop(self.modifiedPanelId)
            if isinstance(removedObj, PanelObj):
                for obj in self.panelObjs:
                    if isinstance(obj, PanelObj) and obj.panelNum > removedObj.panelNum:
                        obj.panelNum = str(int(obj.panelNum) - 1)

                length = len(removedObj.depths)
                self.nextPanelNum -= 1

            else:
                length = 1


            self.summaryTable.DeleteRows(self.modifiedPanelIndex, length)
            if self.summaryTable.GetNumberRows() == 0:
                self.summaryTable.AppendRows()

            print "modifiedPanelId", self.modifiedPanelId
            print "length of panelobjs", len(self.panelObjs)
            self.UpdateObjInfoByRow(self.modifiedPanelId - 1)
            self.TransferFromObjToTable()
            self.RefreshFlow()
            #self.CalculateSummary()

            newHeight = self.summaryTable.GetSize().GetHeight() - length * self.cellHeight
            self.summaryTable.SetSize((-1, newHeight))
            self.Layout()



    def OnAdd(self, event):
        print "OnAdd"
        if self.dlg != None:
            self.dlg.Destroy()
            self.dlg = None
        #TBD ===================================================================================NEED MORE CONDITIONS HERE!===
        self.Adding()
        # event.Skip()


    def Adding(self):
        self.panelType = 1
        enableEdgeStart = True
        enablePierStart = True
        enableEdgeEnd = True
        enablePierEnd = True
        if len(self.panelObjs) == 0:
            self.panelType = 0
            enableEdgeEnd = False
        if self.panelType == 0:
            panelSize = (440, 280)
        elif self.panelType == 1:
            panelSize = (540, 660)
            enableEdgeStart = False

        frame = wx.Dialog(self, size=panelSize)
        header = self.GetParent().header

        print "#########LENGTH OF PANEL OBJS: " + str(len(self.panelObjs))

        if self.lastObj is not None:
            if isinstance(self.lastObj, EdgeObj):
                if isinstance(self.lastObj.startOrEnd, str):
                    if self.lastObj.startOrEnd=="True":
                        self.lastObj.startOrEnd = True
                    else:
                        self.lastObj.startOrEnd = False
                if self.lastObj.startOrEnd and "Pier/Island" in self.lastObj.edgeType:
                    self.panelType = 0
                    panelSize = (440, 280)
                    enablePierStart = False
            if isinstance(self.lastObj, PanelObj):
                self.lastPanelObj = self.lastObj
        else:
            self.lastPanelObj = None

        subPanel = MidSectionSubPanel(panelNum=self.nextPanelNum, parent=frame, size=panelSize, panelType=self.panelType, pos=self.pos)
        if len(self.panelObjs) == 0 and self.panelType ==0:
            subPanel.edge.panelNumberCtrl.SetValue(subPanel.edge.types[0])
            subPanel.edge.endEdgeRdBtn.Disable()
            subPanel.windowTypeBtn2.Disable()
        else:
            subPanel.edge.riverBankCtrl.Disable()
        if not enablePierStart:
            subPanel.edge.panelNumberCtrl.SetValue(subPanel.edge.types[1])

            # panelId=len(self.panelObjs))
        print "nextpanelnum", self.nextPanelNum
        subPanel.UpdateSubPanel()
        #### Edge #####
        if isinstance(self.lastObj, EdgeObj):
            if self.lastObj.startOrEnd and "start p" in self.lastObj.panelNum.lower():
                subPanel.edge.endEdgeRdBtn.SetValue(True)
                subPanel.windowTypeBtn2.Disable()
                subPanel.edge.startEdgeRdBtn.Disable()
                subPanel.edge.panelNumberCtrl.Disable()
        # Check if start edge exists in panels, if so, check if user selected [Edge @ Bank],
        # if so, automatically select End Radio button
        for obj in self.panelObjs:
            if isinstance(obj, EdgeObj):
                if obj.startOrEnd and "edge" in obj.edgeType.lower():
                    def SetEndRdTrue(e):
                        if "edge" in subPanel.edge.panelNumberCtrl.GetValue().lower():
                            subPanel.edge.endEdgeRdBtn.SetValue(True)
                    subPanel.edge.panelNumberCtrl.Bind(wx.EVT_COMBOBOX, SetEndRdTrue)
                    break


        #### Panel ###
        if header.meter1MeterNoCtrl.GetValue() != "":
            subPanel.panel.slopeCtrl.SetValue(header.meter1SlopeCtrl1.GetValue())
            subPanel.panel.slopeCtrl2.SetValue(header.meter1SlopeCtrl2.GetValue())
            subPanel.panel.interceptCtrl.SetValue(header.meter1InterceptCtrl1.GetValue())
            subPanel.panel.interceptCtrl2.SetValue(header.meter1InterceptCtrl2.GetValue())
        elif header.meter2MeterNoCtrl.GetValue() != "":
            subPanel.panel.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
            subPanel.panel.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
            subPanel.panel.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
            subPanel.panel.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())
        else:
            subPanel.panel.slopeCtrl.SetValue("")
            subPanel.panel.slopeCtrl2.SetValue("")
            subPanel.panel.interceptCtrl.SetValue("")
            subPanel.panel.interceptCtrl2.SetValue("")

        if header.meter1MeterNoCtrl.GetValue() != "" and header.meter1MeterNoCtrl.GetValue() is not None:
            if header.meter2MeterNoCtrl.GetValue() != "" and header.meter2MeterNoCtrl.GetValue() is not None:
                subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue(), header.meter2MeterNoCtrl.GetValue()])
            else:
                subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue()])
            if self.lastPanelObj is not None:
                subPanel.panel.currentMeterCtrl.SetValue(self.lastPanelObj.currentMeter)
                subPanel.panel.slopeCtrl.SetValue(self.lastPanelObj.slop)
                subPanel.panel.interceptCtrl.SetValue(self.lastPanelObj.intercept)
                subPanel.panel.slopeCtrl2.SetValue(self.lastPanelObj.slop2)
                subPanel.panel.interceptCtrl2.SetValue(self.lastPanelObj.intercept2)
            else:
                subPanel.panel.currentMeterCtrl.SetValue(header.meter1MeterNoCtrl.GetValue())
        else:
            if header.meter2MeterNoCtrl.GetValue() != "":
                subPanel.panel.currentMeterCtrl.SetItems([header.meter2MeterNoCtrl.GetValue()])
                subPanel.panel.currentMeterCtrl.SetValue(header.meter2MeterNoCtrl.GetValue())
            else:
                subPanel.panel.currentMeterCtrl.SetItems([])

        if header.measureSectionCtrl.GetValue().lower() == "open":
            subPanel.panel.panelConditionCombox.SetItems(["Open"])
            subPanel.panel.panelConditionCombox.SetValue("Open")
        elif header.measureSectionCtrl.GetValue().lower() == "ice":
            subPanel.panel.panelConditionCombox.SetItems(["Ice"])
            subPanel.panel.panelConditionCombox.SetValue("Ice")
        else:
            if self.lastPanelObj is not None:
                subPanel.panel.panelConditionCombox.SetItems(["Open", "Ice"])
                subPanel.panel.panelConditionCombox.SetValue(self.lastPanelObj.panelCondition)
                # subPanel.panel.OnPanelCondition(event)
            else:
                subPanel.panel.panelConditionCombox.SetItems(["Open", "Ice"])
                subPanel.panel.panelConditionCombox.SetSelection(0)

        if self.lastPanelObj is not None:
            # remember last slope radio button
            if self.lastPanelObj.slopBtn1:
                subPanel.panel.slopBtn1.SetValue(True)
            else:
                subPanel.panel.slopBtn2.SetValue(True)
            # remember 'amount of weight', 'WL/DL Correction' if panelCondition=open

            if subPanel.panel.panelConditionCombox.GetValue() == "Open":
                subPanel.panel.amountWeightCmbox.SetValue(self.lastPanelObj.weight)
                subPanel.panel.wldlCorrectionCmbox.SetValue(self.lastPanelObj.wldl)
                subPanel.panel.weightOffsetCtrl.SetValue(self.lastPanelObj.offset)
            # remember 'Ice Assembly' if panelCondition=ice
            if subPanel.panel.panelConditionCombox.GetValue() == "Ice":
                subPanel.panel.iceAssemblyCmbbox.SetValue(self.lastPanelObj.iceAssembly)
                subPanel.panel.meterAboveCtrl.SetValue(self.lastPanelObj.aboveFoot)
                subPanel.panel.meterBelowCtrl.SetValue(self.lastPanelObj.belowFoot)
                subPanel.panel.distanceAboveCtrl.SetValue(self.lastPanelObj.distAboveWeight)
                subPanel.panel.iceThickCtrl.SetValue(str(self.lastObj.iceThickness))
                subPanel.panel.iceThickAdjustedCtrl.SetValue(str(self.lastObj.iceThicknessAdjusted))



        subPanel.panel.PanelConditionUpdate()
        subPanel.panel.SlopeRadioUpdate()
        #subPanel.panel.OnIceAssmeblyNoEvent()
        subPanel.panel.WLDLCorrection()
        subPanel.panel.UpdateWetLineCorrectionNoEvent()
        #subPanel.panel.UpdateMeterOffset()
        subPanel.panel.UpdateVelocityCorrection()
        subPanel.panel.UpdateGrid()

        frame.ShowModal()


    def OnModify(self, event):
        print "OnModify"
        if self.dlg != None:
            self.dlg.Destroy()
            self.dlg = None
        if len(self.panelObjs) == 0:
            return
        #TBD ===================================================================================NEED MORE CONDITIONS HERE!===
        self.panelType = self.panelObjs[self.modifiedPanelId].panelType

        if self.panelType == 0:
            panelSize = (440, 280)
        elif self.panelType == 1:
            panelSize = (540, 660)

        frame = wx.Dialog(self, size=panelSize)
        header = self.GetParent().header
        modifiedObj = self.panelObjs[self.modifiedPanelId]

        subPanel = MidSectionSubPanel(panelNum=modifiedObj.panelNum, parent=frame, \
            size=panelSize, panelType=self.panelType, panelId=modifiedObj.panelId, modify=True, pos=self.pos)

        subPanel.edge.nextBtn.Disable()
        subPanel.panel.nextBtn.Disable()
        if self.panelType==1:
            subPanel.windowTypeBtn1.Disable()
        if self.panelType==0:
            subPanel.windowTypeBtn2.Disable()

        subPanel.UpdateSubPanel()
        if header.meter1MeterNoCtrl.GetValue() != "":
            subPanel.panel.slopeCtrl.SetValue(header.meter1SlopeCtrl1.GetValue())
            subPanel.panel.slopeCtrl2.SetValue(header.meter1SlopeCtrl2.GetValue())
            subPanel.panel.interceptCtrl.SetValue(header.meter1InterceptCtrl1.GetValue())
            subPanel.panel.interceptCtrl2.SetValue(header.meter1InterceptCtrl2.GetValue())
        elif header.meter2MeterNoCtrl.GetValue() != "":
            subPanel.panel.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
            subPanel.panel.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
            subPanel.panel.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
            subPanel.panel.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())
        else:
            subPanel.panel.slopeCtrl.SetValue("")
            subPanel.panel.slopeCtrl2.SetValue("")
            subPanel.panel.interceptCtrl.SetValue("")
            subPanel.panel.interceptCtrl2.SetValue("")

        if header.meter1MeterNoCtrl.GetValue() != "" and header.meter1MeterNoCtrl.GetValue() is not None:
            if header.meter2MeterNoCtrl.GetValue() != "" and header.meter2MeterNoCtrl.GetValue() is not None:
                subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue(), header.meter2MeterNoCtrl.GetValue()])
            else:
                subPanel.panel.currentMeterCtrl.SetItems([header.meter1MeterNoCtrl.GetValue()])
        else:
            if header.meter2MeterNoCtrl.GetValue() != "" and header.meter2MeterNoCtrl.GetValue() is not None:
                subPanel.panel.currentMeterCtrl.SetItems([header.meter2MeterNoCtrl.GetValue()])
            else:
                subPanel.panel.currentMeterCtrl.SetItems([])

        if header.measureSectionCtrl.GetValue() == "Open":
            subPanel.panel.panelConditionCombox.SetItems(["Open"])
        elif header.measureSectionCtrl.GetValue() == "Ice":
            subPanel.panel.panelConditionCombox.SetItems(["Ice"])
        else:
            subPanel.panel.panelConditionCombox.SetItems(["Open", "Ice"])
            if isinstance(modifiedObj, PanelObj):
            	subPanel.panel.panelConditionCombox.SetValue(modifiedObj.panelCondition)
            else:
            	subPanel.panel.panelConditionCombox.SetValue("Open")

        if self.panelType == 0:
            edgePanel = subPanel.edge
            edgePanel.measurementTimeCtrl.SetValue(modifiedObj.time)
            edgePanel.panelNumberCtrl.SetValue(modifiedObj.edgeType)
            if isinstance(modifiedObj.startOrEnd, str):
                if modifiedObj.startOrEnd == "True":
                    modifiedObj.startOrEnd = True
                else:
                    modifiedObj.startOrEnd = False
            if modifiedObj.startOrEnd:
                edgePanel.startEdgeRdBtn.SetValue(True)
            else:
                edgePanel.endEdgeRdBtn.SetValue(True)
            edgePanel.riverBankCtrl.SetValue(modifiedObj.leftOrRight)
            edgePanel.edgeTagmarkCtrl.SetValue(modifiedObj.distance)
            if edgePanel.types[1] == modifiedObj.edgeType or (edgePanel.types[0] == modifiedObj.edgeType and not modifiedObj.startOrEnd):
                edgePanel.riverBankCtrl.Disable()
            edgePanel.depthCtrl.SetValue(modifiedObj.depth)
            edgePanel.estimatedVelCtrl.SetValue(modifiedObj.corrMeanVelocity)
            if modifiedObj.depthAdjacent:
                edgePanel.depthAdjacentCkbox.SetValue(True)
                edgePanel.depthCtrl.Disable()
            if modifiedObj.velocityAdjacent:
                edgePanel.velAdjacentCkbox.SetValue(True)
                edgePanel.estimatedVelCtrl.Disable()

        else:
            panelPanel = subPanel.panel
            panelPanel.panelConditionCombox.SetValue(modifiedObj.panelCondition)
            subPanel.panel.PanelConditionUpdate()
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
                pointVelsIsNone = False

            if modifiedObj.meanVelocity!="":
                panelPanel.openWaterPanel.Disable()
                panelPanel.icePanel.Disable()
            panelPanel.SlopeRadioUpdate()
        self.originalTagmark = float(modifiedObj.distance)
        frame.ShowModal()



    #Add object to object array and update the table
    def AddRow(self, obj, pos=None):
        self.pos = pos

        obj.panelId = len(self.panelObjs)
        self.panelObjs.append(obj)
        # Check if it's decreasing/increasing order then sort accordingly
        if len(self.panelObjs)>2:
            if float(self.panelObjs[0].distance) > float(self.panelObjs[1].distance):
                self.panelObjs.sort(key=lambda f: float(f.distance), reverse=True)
                print "sort reverse"
            else:
                self.panelObjs.sort(key=lambda f: float(f.distance))
                print "sort"

        # Update Panel Number
        c = 1
        for i in range(len(self.panelObjs)):
            if self.panelObjs[i].panelType==1:
                self.panelObjs[i].panelNum = c
                c+=1
            if self.panelObjs[i]==obj:
                addedIndexInArray = i

        if len(self.panelObjs) < 2:
            offset = 1
        else:
            offset = 0

        newLines = 1
        if isinstance(obj, PanelObj) and obj.depths != "":
            if len(obj.depths) > 1:
                newLines = len(obj.depths)

        newLines = newLines - offset

        # obj.panelId = self.summaryTable.GetNumberRows() - 1
        print "==============="
        print self.panelObjs[len(self.panelObjs) - 1].panelId

        for i in range(newLines):
            print "append a row"
            self.summaryTable.AppendRows()
            newHeight = self.summaryTable.GetSize().GetHeight() + self.cellHeight
            self.summaryTable.SetSize((-1, newHeight))

        #print "len(self.panelObjs) - 1", len(self.panelObjs) - 1
        #self.UpdateObjInfoByRow(len(self.panelObjs) - 1)
        print "addedIndexInArray:", addedIndexInArray
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
                self.GetParent().header.CalculateSummary()
                break


    #Recalculate the width, mean velocity, area, discharge, flow if anything changed in the given panel
    def UpdateObjInfoByRow(self, index):
        if index > -1:
            print "UpdateObjInfoByRow  index:", index
            currentObj = self.panelObjs[index]

            if isinstance(currentObj, EdgeObj):
                start = currentObj.startOrEnd
                edgeType = currentObj.edgeType
                panelNum = currentObj.panelNum


                if panelNum == "Start Edge" or panelNum == "End P / ISL":
                    print "index", index
                    print "len(panelObjs)", len(self.panelObjs)

                    if index < len(self.panelObjs) - 1:
                        print "distance", self.panelObjs[index].distance, self.panelObjs[index+1].distance
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
                    print "====================================previous checking"
                    preObj = self.panelObjs[index-1]
                    #if previous is an edge
                    if isinstance(preObj, EdgeObj):
                        if currentObj.distance != "" and preObj.distance != "":
                            print "has previous is an edge, ", currentObj.distance, preObj.distance
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

            print "current object's width is ", str(currentObj.width)
            #Recalculate the area and discharge
            self.UpdateObjAreaAndDischarge(index)
            if index > 0:
                self.UpdateObjAreaAndDischarge(index - 1)
            if index < len(self.panelObjs) - 1:
                self.UpdateObjAreaAndDischarge(index + 1)

            #for i in self.panelObjs:
            #    i.ToString()
            print "The length of panelObjs is:", len(self.panelObjs)


    def UpdateObjAreaAndDischarge(self, index):
        print "UpdateObjAreaAndDischarge", index
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
                    if obj.corrMeanVelocity != "":
                        #obj.discharge = sigfig.round_sig(rawArea * float(obj.corrMeanVelocity),3)
                        obj.discharge = str(rawArea * float(obj.corrMeanVelocity))
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


        print "obj area", obj.area
        print "obj discharge", obj.discharge


    def TransferFromObjToTable(self):
        counter = 0
        coloured = False
        colour1 = (220,230,240)
        colour2 = (255,245,235)
        self.summaryTable.ClearGrid()
        for obj in self.panelObjs:
            oldCounter = counter
            if isinstance(obj, EdgeObj):
                obj.ToString()
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
                        print panelType
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
                        print panelType
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

                print "line 869", panelType
                self.summaryTable.SetCellValue(counter, 0, panelType)
                self.summaryTable.SetCellValue(counter, 1, obj.distance)
                self.summaryTable.SetCellValue(counter, 3, obj.depth)
                self.summaryTable.SetCellValue(counter, 5, obj.depth)
                self.summaryTable.SetCellValue(counter, 10, obj.corrMeanVelocity)




            elif isinstance(obj, PanelObj):
                #print "Counter:", str(counter)
                print "line 882", obj.panelNum
                self.summaryTable.SetCellValue(counter, 0, str(obj.panelNum))
                self.summaryTable.SetCellValue(counter, 1, obj.distance)
                self.Layout()

                if obj.panelCondition == "Open":
                    self.summaryTable.SetCellValue(counter, 3, obj.openDepthRead)
                    self.summaryTable.SetCellValue(counter, 5, obj.openEffectiveDepth)
                else:
                    self.summaryTable.SetCellValue(counter, 3, obj.iceDepthRead)
                    self.summaryTable.SetCellValue(counter, 5, obj.iceEffectiveDepth)
                    if obj.wsBottomSlush != "":
                        # print self.summaryTable.GetNumberRows()
                        # print "counter", counter
                        self.summaryTable.SetCellValue(counter, 4, obj.wsBottomSlush)
                    else:
                        self.summaryTable.SetCellValue(counter, 4, obj.wsBottomIce)

                self.summaryTable.SetCellValue(counter, 10, obj.corrMeanVelocity)

                print "obj depths", obj.depths
                for i in range(len(obj.depths)):
                    # if i > 0:
                    #     self.summaryTable.AppendRows()
                    #     print "add row in transfer"

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

            # Format 3 sigfig for area and discharge
            if isinstance(obj.discharge, str) and obj.discharge=="":
                self.summaryTable.SetCellValue(oldCounter, 12, obj.discharge)
            elif isinstance(obj.discharge, str) and obj.discharge!="":
                #self.summaryTable.SetCellValue(oldCounter, 12, sigfig.round_sig(float(obj.discharge),3))
                self.summaryTable.SetCellValue(oldCounter, 12, obj.discharge)
            if isinstance(obj.discharge, float):
                #self.summaryTable.SetCellValue(oldCounter, 12, sigfig.round_sig(obj.discharge,3))
                self.summaryTable.SetCellValue(oldCounter, 12, str(obj.discharge))
            if isinstance(obj.area, str) and obj.discharge=="":
                self.summaryTable.SetCellValue(oldCounter, 11, obj.area)
            elif isinstance(obj.area, str) and obj.discharge!="":
                self.summaryTable.SetCellValue(oldCounter, 11, sigfig.round_sig(float(obj.area),3))
            if isinstance(obj.area, float):
                self.summaryTable.SetCellValue(oldCounter, 11, sigfig.round_sig(obj.area,3))

            #self.summaryTable.SetCellValue(oldCounter, 12, str(obj.discharge))
            self.summaryTable.SetCellValue(oldCounter, 2, str(obj.width))



            # print "obj.width and panelNum", obj.width, obj.panelNum

            counter += 1




    #Add object to object array and update the table
    def UpdateRow(self, obj, pos=None):
        print "update row"
        self.pos = pos

        for i in self.panelObjs:
            i.ToString()
        print "*********************"
        print "obj.panelId", obj.panelId
        if isinstance(obj, PanelObj):
            oldDepthLength = len(self.panelObjs[self.modifiedPanelId].depths)
            newDepthLength = len(obj.depths)

            if obj.panelId < len(self.panelObjs):
                self.Shift(obj.panelId+1, newDepthLength - oldDepthLength)
        self.panelObjs[self.modifiedPanelId] = obj

        # Check if it's decreasing/increasing order then sort accordingly
        if len(self.panelObjs)>2:
            if float(self.panelObjs[0].distance) > float(self.panelObjs[1].distance):
                self.panelObjs.sort(key=lambda f: float(f.distance), reverse=True)
            else:
                self.panelObjs.sort(key=lambda f: float(f.distance))

        # Update Panel Number
        c = 1
        for i in range(len(self.panelObjs)):
            if self.panelObjs[i].panelType==1:
                self.panelObjs[i].panelNum = c
                c+=1
        #    if self.panelObjs[i] == obj:
        #        rearrangedIndex = i

        # Calculate width, area, discharge for ALL panels (this could be better)
        for i in range(len(self.panelObjs)):
            self.UpdateObjInfoByRow(i)

        print "UpdateObjInfoByRow", self.modifiedPanelId
        #self.UpdateObjInfoByRow(self.modifiedPanelId)

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
                    if ("end edge" in obj.panelNum.lower() or "start p" in obj.panelNum.lower()) and obj.depthAdjacent:
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

                    if ("end edge" in obj.panelNum.lower() or "start p" in obj.panelNum.lower()) and obj.velocityAdjacent:
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

        # for i in range(self.summaryTable.GetNumberRows()):
        #     discharge = self.summaryTable.GetCellValue(i, 12)
        #     if discharge != "":
        #         total += float(discharge)
        #         indexDischarge[i] = float(discharge)


        for i in range(len(self.panelObjs)):
            discharge = self.panelObjs[i].discharge
            if discharge != "":
                total += float(discharge)
                indexDischarge[i] = float(discharge)

        print "total Discharge, ", total
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

            print "********************"
            print indexDischarge

        # i = 0
        # for obj in self.panelObjs:
        #     if obj.discharge != "":
        #         print "****************"
        #         print indexDischarge.values()[i]
        #         obj.flow = str(indexDischarge.values()[i])
        #         i += 1




    #shift the rows from the index number given inclusively move by numbers of lines
    #row: the index of row start to move inclusively
    #lines: positive number to the bottom, negative number to the above
    def Shift(self, row, lines):
        print "shift", row, lines
        print self.summaryTable.GetNumberRows()
        print "lines", lines

        oldTableSize = self.summaryTable.GetNumberRows()
        #shifting down(expand table)
        if lines > 0:
            for i in range(lines):
                self.summaryTable.AppendRows()
                print "appending a row during shifting...i=", i
            newHeight = self.summaryTable.GetSize().GetHeight() + lines * self.cellHeight
            self.summaryTable.SetSize((-1, newHeight))
            self.Layout()
            # if row < oldTableSize:
            #     for line in reversed(range(oldTableSize)[row:]):
            #         print "copy reversed index number", line
            #         for i in range(14):
            #             self.summaryTable.SetCellValue(line+lines, i, self.summaryTable.GetCellValue(line, i))


            #clear the table
            for i in range(self.summaryTable.GetNumberRows()):
                for j in range(14):
                    self.summaryTable.SetCellValue(i, j, "")

        elif lines < 0:
            lines = abs(lines)

            self.summaryTable.DeleteRows(self.summaryTable.GetNumberRows()-lines, lines)






        print "=============================================="
        print "Panel ID list:"
        for i in self.panelObjs:
            if i is not None:
                print i.panelId
            else:
                print "--"

        print "=============================================="
        print "Panel panelNum list:"
        for i in self.panelObjs:
            if i is not None:
                print i.panelNum
            else:
                print "--"

        print "=============================================="
        print "Panel index list:"
        for i in self.panelObjs:
            if i is not None:
                print i.index
            else:
                print "--"

    def OnAddBtn(self, event):
        # self.Shift(0, 2)
        self.Adding()
        event.Skip()


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(1200, 200))
    MidsectionSummaryTable(frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
