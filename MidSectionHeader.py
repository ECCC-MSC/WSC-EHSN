# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import sigfig

import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os

from DropdownTime import *
import NumberControl
from MidSectionSubPanelObj import *
from MidSectionTransferFrame import *

class MidSectionHeader(wx.Panel):

    def __init__(self, mode, *args, **kwargs):
        super(MidSectionHeader, self).__init__(*args, **kwargs)
        self.mode = mode
        self.startTimeLbl = "Start Time"
        self.endTimeLbl = "End Time"
        self.measSectionLbl = "Measurement Section"
        self.deployMethodLbl = "Deployment Method"
        self.meterInfoLbl = "Meter Information"
        self.meterEquationLbl = "Meter Equation"
        self.meterNumlbl = "Meter No."
        self.slopeLbl1 = "Slope1"
        self.interceptLbl1 = "Intercept1"
        self.slopeLbl2 = "Slope2"
        self.interceptLbl2 = "Intercept2"
        self.calibDateLbl = "Calibration Date"
        self.meter1Lbl = "Meter1"
        self.meter2Lbl = "Meter2"
        self.measSummLbl = "Measurement Summary"
        self.numPanelLbl = "Num. Panels"
        self.widthLbl = "Width (m)"
        self.areaLbl = u"Area (m\N{SUPERSCRIPT TWO})"
        self.avgDepthLbl = "Avg Depth (m)"
        self.avgVelLbl = "Avg Velocity (m/s)"
        self.totalDisLbl = u"Total Discharge (m\N{SUPERSCRIPT THREE}/s) "
        self.uncertLbl = "Uncertainty (ISO)(%)"
        self.plotLbl = "Plot"
        self.updateSummaryLbl = "Update Summary"
        self.startBankLbl = "Start Bank"
        self.width = 50


        self.meterNoList = [""]
        self.slope1List = [""]
        self.intercept1List = [""]
        self.slope2List = [""]
        self.intercept2List = [""]
        self.calibDateList = [""]
        self.allDeployMethods = ["", "Bridge", "Boat", "Cableway", "Wading", "Ice", "Ice_Bridge", "Ice_Cableway", "Ice_Wading"]
        self.measureSections = ["Open", "Ice", "Combined"]
        self.deployMethodsOpen = ["Wading", "Boat", "Cableway", "Bridge"]
        self.deployMethodsIce = ["Ice"]
        self.deployMethodsCombined = ["Ice_Wading", "Ice_Cableway", "Ice_Bridge"]
        self.startBanks = ["Left", "Right"]
        self.dir = self.GetParent().GetParent().GetParent().GetParent().dir
        self.transferBtnLbl = "Transfer to Front Page"
        self.transferFrameSize = (420, 300)

        if hasattr(sys, '_MEIPASS'):
            self.myBitmapFront = os.path.join(sys._MEIPASS, "backarrow.png")
        else:
            self.myBitmapFront = self.dir + "\\" + "backarrow.png"

        self.transToFrontpicture = wx.Image(self.myBitmapFront, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.InitUI()

    def InitUI(self):
        self.layout = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.layout)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        # leftH1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftH2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftH3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftH4Sizer = wx.BoxSizer(wx.HORIZONTAL)

        # startTimeTxt = wx.StaticText(self, label=self.startTimeLbl)
        # self.startTimeCtrl = DropdownTime(False, parent=self, size=(self.width, -1), style=wx.BORDER_NONE)

        # endTimeTxt = wx.StaticText(self, label=self.endTimeLbl)
        # self.endTimeCtrl = DropdownTime(False, parent=self, size=(self.width, -1), style=wx.BORDER_NONE)

        # leftH1Sizer.Add(startTimeTxt, 1, wx.EXPAND|wx.TOP, 5)
        # leftH1Sizer.Add(self.startTimeCtrl, 1, wx.EXPAND|wx.BOTTOM, 5)
        # leftH1Sizer.Add(endTimeTxt, 1, wx.EXPAND|wx.LEFT|wx.TOP, 5)
        # leftH1Sizer.Add(self.endTimeCtrl, 1, wx.EXPAND|wx.BOTTOM, 5)


        measureSectionTxt = wx.StaticText(self, label=self.measSectionLbl)
        # self.measureSectionCtrl = wx.TextCtrl(self, size=(self.width, -1))
        self.measureSectionCtrl = wx.ComboBox(self, size=(self.width, -1), choices=self.measureSections, style=wx.CB_READONLY)
        self.measureSectionCtrl.Bind(wx.EVT_COMBOBOX, self.OnMeasurementSection)
        deployMethodTxt = wx.StaticText(self, label=self.deployMethodLbl)
        # self.deployMethodCtrl = wx.TextCtrl(self, size=(self.width, -1))
        self.deployMethodCtrl = wx.ComboBox(self, size=(self.width, -1), choices=self.allDeployMethods, style=wx.CB_READONLY)

        leftH2Sizer.Add(measureSectionTxt, 1, wx.EXPAND)
        leftH2Sizer.Add(self.measureSectionCtrl, 1, wx.EXPAND)
        leftH2Sizer.Add(deployMethodTxt, 1, wx.EXPAND|wx.LEFT, 5)
        leftH2Sizer.Add(self.deployMethodCtrl, 1, wx.EXPAND)

        meterInforTxt = wx.StaticText(self, label=self.meterInfoLbl)
        leftH3Sizer.Add(meterInforTxt, 1, wx.EXPAND)

        meterTablePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        meterTableSizer = wx.BoxSizer(wx.VERTICAL)
        meterTablePanel.SetSizer(meterTableSizer)



        meterTableHeaderPanel = wx.Panel(meterTablePanel, style=wx.SIMPLE_BORDER)
        meterTableHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        meterTableHeaderPanel.SetSizer(meterTableHeaderSizer)

        # meterHeader1Txt = wx.StaticText(meterTableHeaderPanel, label=" ")
        meterHeader2Txt = wx.StaticText(meterTableHeaderPanel, label=self.meterNumlbl)
        meterHeader3Txt = wx.StaticText(meterTableHeaderPanel, label=self.slopeLbl1)
        meterHeader4Txt = wx.StaticText(meterTableHeaderPanel, label=self.interceptLbl1)
        meterHeader5Txt = wx.StaticText(meterTableHeaderPanel, label=self.slopeLbl2)
        meterHeader6Txt = wx.StaticText(meterTableHeaderPanel, label=self.interceptLbl2)
        meterHeader7Txt = wx.StaticText(meterTableHeaderPanel, label=self.calibDateLbl)

        # meterTableHeaderSizer.Add(meterHeader1Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableHeaderSizer.Add(meterHeader2Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableHeaderSizer.Add(meterHeader3Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableHeaderSizer.Add(meterHeader4Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableHeaderSizer.Add(meterHeader5Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableHeaderSizer.Add(meterHeader6Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableHeaderSizer.Add(meterHeader7Txt, 1, wx.EXPAND|wx.ALL, 5)

        leftH4Sizer.Add(meterTablePanel, 1, wx.EXPAND)


        meterTableMeter1Panel = wx.Panel(meterTablePanel, style=wx.SIMPLE_BORDER)
        meterTableMeter1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        meterTableMeter1Panel.SetSizer(meterTableMeter1Sizer)

        # self.meter1Ckbox = wx.CheckBox(meterTableMeter1Panel, label=self.meterCkbLbl1)
        # self.meter1MeterNoCtrl = wx.TextCtrl(meterTableMeter1Panel, size=(self.width, -1))
        # self.meter1Txt = wx.StaticText(meterTableMeter1Panel, label=self.meter1Lbl)
        self.meter1MeterNoCtrl = wx.ComboBox(meterTableMeter1Panel, size=(self.width, -1))
        self.meter1MeterNoCtrl.Bind(wx.EVT_COMBOBOX, self.UpdateMeter1Info)
        self.meter1SlopeCtrl1 = wx.TextCtrl(meterTableMeter1Panel, size=(self.width, -1))
        self.meter1InterceptCtrl1 = wx.TextCtrl(meterTableMeter1Panel, size=(self.width, -1))
        self.meter1SlopeCtrl2 = wx.TextCtrl(meterTableMeter1Panel, size=(self.width, -1))
        self.meter1InterceptCtrl2 = wx.TextCtrl(meterTableMeter1Panel, size=(self.width, -1))
        self.meter1CalibDateCtrl = wx.TextCtrl(meterTableMeter1Panel, size=(self.width, -1))

        self.meter1SlopeCtrl1.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.meter1InterceptCtrl1.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.meter1SlopeCtrl2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.meter1InterceptCtrl2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)

        # meterTableMeter1Sizer.Add(self.meter1Ckbox, 1, wx.EXPAND|wx.ALL, 5)
        # meterTableMeter1Sizer.Add(self.meter1Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter1Sizer.Add(self.meter1MeterNoCtrl, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter1Sizer.Add(self.meter1SlopeCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter1Sizer.Add(self.meter1InterceptCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter1Sizer.Add(self.meter1SlopeCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter1Sizer.Add(self.meter1InterceptCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter1Sizer.Add(self.meter1CalibDateCtrl, 1, wx.EXPAND|wx.ALL, 5)




        meterTableMeter2Panel = wx.Panel(meterTablePanel, style=wx.SIMPLE_BORDER)
        meterTableMeter2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        meterTableMeter2Panel.SetSizer(meterTableMeter2Sizer)

        # self.meter2Ckbox = wx.CheckBox(meterTableMeter2Panel, label=self.meterCkbLbl2)
        # self.meter2MeterNoCtrl = wx.TextCtrl(meterTableMeter2Panel, size=(self.width, -1))
        # self.meter2Txt = wx.StaticText(meterTableMeter2Panel, label=self.meter2Lbl)
        self.meter2MeterNoCtrl = wx.ComboBox(meterTableMeter2Panel, size=(self.width, -1))
        self.meter2MeterNoCtrl.Bind(wx.EVT_COMBOBOX, self.UpdateMeter2Info)
        self.meter2SlopeCtrl1 = wx.TextCtrl(meterTableMeter2Panel, size=(self.width, -1))
        self.meter2InterceptCtrl1 = wx.TextCtrl(meterTableMeter2Panel, size=(self.width, -1))
        self.meter2SlopeCtrl2 = wx.TextCtrl(meterTableMeter2Panel, size=(self.width, -1))
        self.meter2InterceptCtrl2 = wx.TextCtrl(meterTableMeter2Panel, size=(self.width, -1))
        self.meter2CalibDateCtrl = wx.TextCtrl(meterTableMeter2Panel, size=(self.width, -1))

        self.meter2SlopeCtrl1.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.meter2InterceptCtrl1.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.meter2SlopeCtrl2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.meter2InterceptCtrl2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)

        # meterTableMeter2Sizer.Add(self.meter2Ckbox, 1, wx.EXPAND|wx.ALL, 5)
        # meterTableMeter2Sizer.Add(self.meter2Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2MeterNoCtrl, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2SlopeCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2InterceptCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2SlopeCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2InterceptCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2CalibDateCtrl, 1, wx.EXPAND|wx.ALL, 5)


        bankSizer = wx.BoxSizer(wx.HORIZONTAL)


        meterTableSizer.Add(meterTableHeaderPanel, 1, wx.EXPAND)
        meterTableSizer.Add(meterTableMeter1Panel, 1, wx.EXPAND)
        meterTableSizer.Add(meterTableMeter2Panel, 1, wx.EXPAND)



        # leftSizer.Add(leftH1Sizer, 0, wx.EXPAND)
        leftSizer.Add(leftH2Sizer, 0, wx.EXPAND)
        leftSizer.Add(leftH3Sizer, 0, wx.EXPAND)
        leftSizer.Add(leftH4Sizer, 0, wx.EXPAND)




        #right hand size for Meeasurement Summary

        rightH1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH6Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH7Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH8Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH9Sizer = wx.BoxSizer(wx.HORIZONTAL)

        rightH10Sizer = wx.BoxSizer(wx.HORIZONTAL)
        rightH11Sizer = wx.BoxSizer(wx.HORIZONTAL)

        measurementSummaryTxt = wx.StaticText(self, label=self.measSummLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        measurementSummaryTxt.SetFont(headerFont)



        
        # self.transferBtn = wx.Button(self, label=self.transferBtnLbl, size=(20, 10))
        
        # transferBtnSizer = wx.BoxSizer(wx.VERTICAL)
        self.transferBtn = wx.BitmapButton(self, size=(-1, 50), bitmap=self.transToFrontpicture)
        self.transferBtn.Bind(wx.EVT_BUTTON, self.OnTransBtn)

        transferTxt = wx.StaticText(self, label="\n\nTransfer to Front Page", style=wx.ST_ELLIPSIZE_END)
        # transferBtnSizer.Add(self.transferBtn, 0, wx.EXPAND)


        rightH1Sizer.Add(measurementSummaryTxt, 1, wx.EXPAND)
        rightH1Sizer.Add(self.transferBtn, 0, wx.EXPAND)
        rightH1Sizer.Add(transferTxt, 0, wx.BOTTOM)

        startTimeTxt = wx.StaticText(self, label=self.startTimeLbl, size=(70, -1))
        self.startTimeCtrl = DropdownTime(False, parent=self, size=(150, -1), style=wx.BORDER_NONE)
        self.startTimeCtrl.Enable(False)

        endTimeTxt = wx.StaticText(self, label=self.endTimeLbl, size=(70, -1))
        self.endTimeCtrl = DropdownTime(False, parent=self, size=(150, -1), style=wx.BORDER_NONE)
        self.endTimeCtrl.Enable(False)

        rightH10Sizer.Add(startTimeTxt, 0, wx.EXPAND)
        rightH10Sizer.Add((-1,-1), 1, wx.EXPAND)
        rightH10Sizer.Add(self.startTimeCtrl, 0, wx.ALIGN_RIGHT)

        rightH11Sizer.Add(endTimeTxt, 0, wx.EXPAND)
        rightH11Sizer.Add((-1,-1), 1, wx.EXPAND)
        rightH11Sizer.Add(self.endTimeCtrl, 0, wx.ALIGN_RIGHT)

        numOfPanelTxt = wx.StaticText(self, label=self.numPanelLbl)
        self.numOfPanelCtrl = wx.TextCtrl(self)

        rightH2Sizer.Add(numOfPanelTxt, 1, wx.EXPAND)
        rightH2Sizer.Add(self.numOfPanelCtrl, 1, wx.EXPAND)

        widthTxt = wx.StaticText(self, label=self.widthLbl)
        self.widthCtrl = wx.TextCtrl(self)

        rightH3Sizer.Add(widthTxt, 1, wx.EXPAND)
        rightH3Sizer.Add(self.widthCtrl, 1, wx.EXPAND)

        areaTxt = wx.StaticText(self, label=self.areaLbl)
        self.areaCtrl = wx.TextCtrl(self)

        rightH4Sizer.Add(areaTxt, 1, wx.EXPAND)
        rightH4Sizer.Add(self.areaCtrl, 1, wx.EXPAND)


        avgDepthTxt = wx.StaticText(self, label=self.avgDepthLbl)
        self.avgDepthCtrl = wx.TextCtrl(self)

        rightH5Sizer.Add(avgDepthTxt, 1, wx.EXPAND)
        rightH5Sizer.Add(self.avgDepthCtrl, 1, wx.EXPAND)


        avgVelTxt = wx.StaticText(self, label=self.avgVelLbl)
        self.avgVelCtrl = wx.TextCtrl(self)

        rightH6Sizer.Add(avgVelTxt, 1, wx.EXPAND)
        rightH6Sizer.Add(self.avgVelCtrl, 1, wx.EXPAND)

        totalDisTxt = wx.StaticText(self, label=self.totalDisLbl)
        self.totalDisCtrl = wx.TextCtrl(self)

        rightH7Sizer.Add(totalDisTxt, 1, wx.EXPAND)
        rightH7Sizer.Add(self.totalDisCtrl, 1, wx.EXPAND)

        uncertainityTxt = wx.StaticText(self, label=self.uncertLbl)
        self.uncertaintyCtrl = wx.TextCtrl(self)
        self.uncertaintyCtrl.Enable(False)

        rightH8Sizer.Add(uncertainityTxt, 1, wx.EXPAND)
        rightH8Sizer.Add(self.uncertaintyCtrl, 1, wx.EXPAND)

        self.updateSummaryBtn = wx.Button(self, label=self.updateSummaryLbl)
        self.updateSummaryBtn.Bind(wx.EVT_BUTTON, self.OnUpdateSummary)
        self.plotBtn = wx.Button(self, label=self.plotLbl,size=(15,-1))
        self.plotBtn.Bind(wx.EVT_BUTTON, self.OnPlot)
        #self.plotBtn.Disable()
        rightH9Sizer.Add(self.updateSummaryBtn, 1, wx.EXPAND)
        rightH9Sizer.Add(self.plotBtn, 1, wx.EXPAND)

        

        rightSizer.Add(rightH1Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH10Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH11Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH2Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH3Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH4Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH5Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH6Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH7Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH8Sizer, 0, wx.EXPAND)
        rightSizer.Add(rightH9Sizer, 0, wx.EXPAND)

        self.layout.Add(leftSizer, 1, wx.EXPAND|wx.ALL, 10)
        self.layout.Add(rightSizer, 1, wx.EXPAND|wx.ALL, 10)
        # self.layout.Add(transferBtnSizer, 0, wx.ALL, 10)

    def OnTransBtn(self, evt):
        position = self.GetParent().GetParent().GetParent().GetParent().GetPosition()
        x = position.x + 200
        y = position.y + 50
        frame = MidSectionTransferFrame(mode=self.mode, parent=self, title="Transfer to The Front Page", size=self.transferFrameSize, pos=(x, y))
        frame.Show()

        evt.Skip()

    def OnMeasurementSection(self, event):
        measureSection = self.measureSectionCtrl.GetValue()
        if measureSection == self.measureSections[0]:
            self.deployMethodCtrl.SetItems(self.deployMethodsOpen)
        elif measureSection == self.measureSections[1]:
            self.deployMethodCtrl.SetItems(self.deployMethodsIce)
            self.deployMethodCtrl.SetValue(self.deployMethodsIce[0])
        elif measureSection == self.measureSections[2]:
            self.deployMethodCtrl.SetItems(self.deployMethodsCombined)
        else:
            self.deployMethodCtrl.SetItems([])

        event.Skip()

    def OnUpdateSummary(self, evt):
        self.CalculateSummary()

    def OnPlot(self, event):
        self.plotBtn.Disable()
        # self.GeneratePlot()
        try:
            self.GeneratePlot()
            self.plotBtn.Enable()
        except Exception as e:
            print str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.plotBtn.Enable()
        event.Skip()

    def GeneratePlot(self):

        panelObjs = self.GetParent().table.panelObjs

        isIncreasing = True
        if float(panelObjs[0].distance) > float(panelObjs[1].distance):
            isIncreasing = False


        width, height = wx.GetDisplaySize()

        fig, ax = plt.subplots(2, facecolor="white", sharex=True, figsize=(width/80*0.8,height/80*0.8))
        velo = ax[0].twinx()

        

        for tk in ax[0].get_xticklabels():
            tk.set_visible(True)

        tagmarkList = []
        panelTagmarkList = [] # List of tagmarks just for panels
        edgeTagmarkList = [] # List of tagmarks just for edge
        edgeDepthList = [] # List of depth just for edge
        tagmarkLineList = [] # List of calculated x values for the lines
        flowList = []
        flowTagList = []
        veloList = []
        veloTagList = []
        depthList = []
        depthTagList = []
        depthObsList = []
        bottomIceList = []
        iceTagList = []
        bottomSlushList = []
        slushTagList = []

        for i, obj in enumerate(panelObjs):
            if isinstance(obj, EdgeObj):
                if "Start P" in obj.panelNum or "End E" in obj.panelNum:
                    tagmarkLineList.append((float(obj.distance) + float(panelObjs[i-1].distance))/2)
                tagmarkLineList.append(float(obj.distance))
                
            else:
                tagmarkLineList.append((float(obj.distance) + float(panelObjs[i-1].distance))/2)


            if panelObjs[i].flow!="":
                flowList.append(panelObjs[i].flow)
                flowTagList.append(float(panelObjs[i].distance))
            if panelObjs[i].corrMeanVelocity!="":
                veloList.append(panelObjs[i].corrMeanVelocity)
                veloTagList.append(float(panelObjs[i].distance))
            if isinstance(panelObjs[i], PanelObj):
                if panelObjs[i].panelCondition == "Open" and panelObjs[i].openDepthRead != "":
                    depthList.append(float(panelObjs[i].openDepthRead))
                elif panelObjs[i].panelCondition == "Ice" and panelObjs[i].iceDepthRead != "":
                    depthList.append(float(panelObjs[i].iceDepthRead))
                else:
                    depthList.append(0)
                depthTagList.append(float(panelObjs[i].distance))
            else:
                if panelObjs[i].edgeType == "Edge":
                    if panelObjs[i].depth != "":
                        depthList.append(float(panelObjs[i].depth))
                    else:
                        depthList.append(0)
                    
                else:
                    depthList.append(0)

                if panelObjs[i].distance != "":
                    depthTagList.append(float(panelObjs[i].distance))
                else:
                    depthTagList.append(0)



            if isinstance(panelObjs[i], PanelObj):
                if panelObjs[i].wsBottomIce!="":
                    bottomIceList.append(float(panelObjs[i].wsBottomIce))
                    iceTagList.append(float(panelObjs[i].distance))
                if panelObjs[i].wsBottomIce=="":
                    bottomIceList.append(0)
                    iceTagList.append(float(panelObjs[i].distance))
                if panelObjs[i].wsBottomSlush!="":
                    bottomSlushList.append(float(panelObjs[i].wsBottomSlush))
                    slushTagList.append(float(panelObjs[i].distance))
                if panelObjs[i].wsBottomSlush=="":
                    bottomSlushList.append(0)
                    slushTagList.append(float(panelObjs[i].distance))
                if len(panelObjs[i].depthObs) > 0:
                    if "" not in panelObjs[i].depthObs:
                        depthObsList.append(panelObjs[i].depthObs)
                        panelTagmarkList.append(panelObjs[i].distance)

            if isinstance(panelObjs[i], EdgeObj):
                bottomIceList.append(0)
                iceTagList.append(float(panelObjs[i].distance))
                bottomSlushList.append(0)
                slushTagList.append(float(panelObjs[i].distance))



        try:
            if panelObjs[0].leftOrRight!="":
                leftOrRight = panelObjs[0].leftOrRight
            edgeTagmarkPos = float(panelObjs[0].distance)
            edgeDepthPos = float(panelObjs[0].depth)
        except:
            pass



        #adding extra point on each side if ice coverd
        counter = 0
        for index, obj in enumerate(panelObjs):

            if isinstance(obj, EdgeObj) and ("Start E" in obj.panelNum or "End P" in obj.panelNum) and panelObjs[index+1].wsBottomIce!="":
                y=float(panelObjs[index+1].wsBottomIce)
                if panelObjs[index+1].panelCondition == "Open" and panelObjs[index+1].openDepthRead != "":
                    depth2 = float(panelObjs[index+1].openDepthRead)
                elif panelObjs[index+1].panelCondition == "Ice" and panelObjs[index+1].iceDepthRead != "":
                    depth2 = float(panelObjs[index+1].iceDepthRead)
                else:
                    depth2 = 0
                depth1 = float(obj.depth)
                tagMark2 = float(panelObjs[index+1].distance)
                tagMark1 = float(obj.distance)
                slop = (depth2-depth1) / (tagMark2-tagMark1)

     

                x = tagMark1 + (y - depth1) / slop


                bottomIceList.insert(index+1+counter, y)
                iceTagList.insert(index+1+counter, x)
                counter += 1

            elif isinstance(obj, EdgeObj) and ("End E" in obj.panelNum or "Start P" in obj.panelNum) and panelObjs[index-1].wsBottomIce!="":
                y=float(panelObjs[index-1].wsBottomIce)

                if panelObjs[index-1].panelCondition == "Open" and panelObjs[index-1].openDepthRead != "":
                    depth2 = float(panelObjs[index-1].openDepthRead)
                elif panelObjs[index-1].panelCondition == "Ice" and panelObjs[index-1].iceDepthRead != "":
                    depth2 = float(panelObjs[index-1].iceDepthRead)
                else:
                    depth2 = 0
                depth1 = float(obj.depth)
                tagMark2 = float(panelObjs[index-1].distance)
                tagMark1 = float(obj.distance)
                slop = (depth2-depth1) / (tagMark2-tagMark1)



                x = tagMark1 + (y - depth1) / slop


                bottomIceList.insert(index+counter, y)
                iceTagList.insert(index+counter, x)
                counter += 1



        # Plot Flow
        lns1, = ax[0].step(flowTagList, flowList,where='mid',linewidth=2, color="purple", label="Discharge(q/Q%)")
        # Plot Velocity
        lns2, = velo.plot(veloTagList, veloList, color="blue", label="Velocity")

        maxTagFlow = float(max(flowTagList))
        minTagFlow = float(min(flowTagList))
        maxTagVel = float(max(veloTagList))
        minTagVel = float(min(veloTagList))
        maxTagFV = maxTagFlow if maxTagFlow > maxTagVel else maxTagVel
        minTagFV = minTagFlow if minTagFlow < minTagVel else minTagVel

        minX = float(min(tagmarkLineList))
        maxX = float(max(tagmarkLineList))
        difference = maxX - minX

        newMinX = int(minX - math.ceil(difference / 20 * 0.5))
        newMaxX = int(maxX + math.ceil(difference / 20 * 0.5))


        

        ax[1].invert_yaxis()
        if ("right" in leftOrRight.lower() and not isIncreasing) or ("left" in leftOrRight.lower() and isIncreasing):
            ax[0].set_xlim(newMinX, newMaxX)

        else:
            ax[0].set_xlim(newMaxX, newMinX)


        # Depth curve

        lns3 = ax[1].fill_between(np.array(depthTagList),np.array(depthList), facecolor="#91c7f7", edgecolor="#91c7f7", label="River Body")
        # Ice
        lns4 = ax[1].fill_between(iceTagList,bottomIceList, facecolor="#5b5858", edgecolor="#5b5858", label="Ice")
        lns5 = ax[1].fill_between(slushTagList,bottomSlushList, facecolor="#e5e5e5", edgecolor="#e5e5e5", label="Slush Ice")


        # observation points for panel
        for tagmark, depthObs in zip(panelTagmarkList, depthObsList):
            for point in depthObs:
                lns6, = ax[1].plot(tagmark, point, "ro", marker="s", label="Obsevation Points")
        # Lines
        if isIncreasing:
            
            y = np.interp(tagmarkLineList, depthTagList, depthList)

        else:
            y = np.interp(tagmarkLineList, depthTagList[::-1], depthList[::-1])


        ax[1].stem(tagmarkLineList, y, markerfmt=" ", label="Panel Boundary", linefmt="#00143d")
        lns7, = ax[1].plot(1,1,color="#00143d") #This is a proxy; just for the legend

       

        lns = [lns1, lns2, lns3, lns4, lns5, lns6, lns7]
        labels=["Discharge(q/Q%)","Velocity","River Body","Ice","Slush Ice","Obsevation Points","Panel Boundary"]


        ax[1].legend(lns,labels,prop={'size':9}, loc='lower left', numpoints=1, borderaxespad=0.)

        lns7.set_visible(False)


        ax[0].spines['left'].set_color('purple')
        ax[0].yaxis.label.set_color('purple')
        ax[0].tick_params(axis='y', colors='purple')
        velo.spines['right'].set_color('blue')
        velo.yaxis.label.set_color('blue')
        velo.tick_params(axis='y', colors='blue')


        maxFlow = float(max(flowList))
        minFlow = float(min(flowList))
        maxVel = float(max(veloList))
        minVel = float(min(veloList))
        maxFV = maxFlow if maxFlow > maxVel else maxVel
        minFV = minFlow if minFlow < minVel else minVel
        ax[0].set_ylim(minFV, maxFV * 1.1)

        


        maxY = float(max(y))
        ax[1].set_ylim(maxY * 1.1, 0)

        ax[0].set_ylabel("Discharge (q/Q%)", fontsize=14, color="purple")
        velo.set_ylabel("Velocity (m/s)", fontsize=14, color="b")
        ax[1].set_xlabel("Tagmark (m)", fontsize=14)
        ax[1].set_ylabel("Depth (m)", fontsize=14)

        ax[1].locator_params(axis='both', nbins=10)
        ax[1].yaxis.set_ticks_position('both')
        ax[1].tick_params(labeltop=False, labelright=True)



        if maxX - minX < 20:
            plt.xticks(np.arange(newMinX,newMaxX, step=1))
        else:
            plt.xticks(np.arange(newMinX,newMaxX, step=(int((difference) / 20))))



        ax[0].grid('on')
        ax[1].grid('on')

        ax[0].autoscale_view(True,True,True)
        ax[1].autoscale_view(True,True,True)


        pltManager = plt.get_current_fig_manager()
        pltManager.window.wm_geometry("+50+0")

        plt.show()

        self.plotBtn.Enable(True)

    def CalculateSlop(self, x1, y1, x2, y2):
        return (y2 - y1) / (x2 / x1)

    def CalculateSummary(self):
        table = self.GetParent().table

        totalWidth = 0
        totalArea = 0
        totalDischarge = 0
        width = ""
        area = ""
        discharge = ""
        for obj in table.panelObjs:
            if obj.width!="":
                width = obj.width
            if obj.area!="":
                area = obj.area
            if obj.discharge!="":
                discharge = obj.discharge


            if width != "":
                totalWidth += float(width)
            if area != "":
                totalArea += float(area)
            if discharge != "":
                totalDischarge += float(discharge)

        summary = []

        summary.append(str(table.nextPanelNum - 1))
        summary.append(str(totalWidth))
        summary.append(str(totalArea))
        if totalWidth != 0:
            summary.append(str(totalArea / totalWidth))
        else:
            summary.append("")
        if totalArea != 0:
            summary.append(str(totalDischarge / totalArea))
        else:
            summary.append("")
        summary.append(str(totalDischarge))
        times = table.OrderedTimes()
        if len(times) > 0:
            summary.append(str(times[0]))
            summary.append(str(times[-1]))
        else:
            summary.append("")
            summary.append("")


        self.UpdateSummary(summary)

        



    def UpdateSummary(self, values):
        try:
            self.numOfPanelCtrl.SetValue(values[0])
        except:
            pass
        try:
            self.widthCtrl.SetValue(str(round(float(values[1]),3)))
        except:
            pass
        try:
            self.areaCtrl.SetValue(sigfig.round_sig(float(values[2]),3))
        except:
            pass
        try:
            self.avgDepthCtrl.SetValue(str(round(float(values[3]),3)))
        except:
            pass
        try:
            self.avgVelCtrl.SetValue(sigfig.round_sig(float(values[4]),3))
        except:
            pass
        try:
            self.totalDisCtrl.SetValue(sigfig.round_sig(float(values[5]),3))
        except:
            pass

        self.startTimeCtrl.SetValue(values[6])
        self.endTimeCtrl.SetValue(values[7])
        #self.totalDisCtrl.SetValue(str(round(float(values[5]),3)))



    def UpdateMeterNo(self):
        self.meter1MeterNoCtrl.SetItems(self.meterNoList)
        self.meter2MeterNoCtrl.SetItems(self.meterNoList)

    def UpdateMeter1Info(self, evt):
        index = evt.GetSelection()
        self.meter1SlopeCtrl1.SetValue(self.slope1List[index])
        self.meter1InterceptCtrl1.SetValue(self.intercept1List[index])
        self.meter1SlopeCtrl2.SetValue(self.slope2List[index])
        self.meter1InterceptCtrl2.SetValue(self.intercept2List[index])
        self.meter1CalibDateCtrl.SetValue(self.calibDateList[index])

    def UpdateMeter2Info(self,evt):
        index = evt.GetSelection()
        self.meter2SlopeCtrl1.SetValue(self.slope1List[index])
        self.meter2InterceptCtrl1.SetValue(self.intercept1List[index])
        self.meter2SlopeCtrl2.SetValue(self.slope2List[index])
        self.meter2InterceptCtrl2.SetValue(self.intercept2List[index])
        self.meter2CalibDateCtrl.SetValue(self.calibDateList[index])

def main():
    app = wx.App()

    frame = wx.Frame(None, size=(940, 250))
    MidSectionHeader(frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
