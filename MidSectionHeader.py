# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import sigfig

import matplotlib.pyplot as plt
import numpy as np

from DropdownTime import *

class MidSectionHeader(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(MidSectionHeader, self).__init__(*args, **kwargs)
        self.startTimeLbl = "Mmt. Start Time"
        self.endTimeLbl = "Mmt. End Time"
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

        self.InitUI()

    def InitUI(self):
        self.layout = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.layout)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        leftH1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftH2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftH3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftH4Sizer = wx.BoxSizer(wx.HORIZONTAL)

        startTimeTxt = wx.StaticText(self, label=self.startTimeLbl)
        # self.startTimeCtrl = wx.TextCtrl(self, size=(self.width, -1))
        self.startTimeCtrl = DropdownTime(False, parent=self, size=(self.width, -1), style=wx.BORDER_NONE)

        endTimeTxt = wx.StaticText(self, label=self.endTimeLbl)
        # self.endTimeCtrl = wx.TextCtrl(self, size=(self.width, -1))
        self.endTimeCtrl = DropdownTime(False, parent=self, size=(self.width, -1), style=wx.BORDER_NONE)

        leftH1Sizer.Add(startTimeTxt, 1, wx.EXPAND|wx.TOP, 5)
        leftH1Sizer.Add(self.startTimeCtrl, 1, wx.EXPAND|wx.BOTTOM, 5)
        leftH1Sizer.Add(endTimeTxt, 1, wx.EXPAND|wx.LEFT|wx.TOP, 5)
        leftH1Sizer.Add(self.endTimeCtrl, 1, wx.EXPAND|wx.BOTTOM, 5)


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

        # meterTableMeter2Sizer.Add(self.meter2Ckbox, 1, wx.EXPAND|wx.ALL, 5)
        # meterTableMeter2Sizer.Add(self.meter2Txt, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2MeterNoCtrl, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2SlopeCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2InterceptCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2SlopeCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2InterceptCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        meterTableMeter2Sizer.Add(self.meter2CalibDateCtrl, 1, wx.EXPAND|wx.ALL, 5)

        meterTableSizer.Add(meterTableHeaderPanel, 1, wx.EXPAND)
        meterTableSizer.Add(meterTableMeter1Panel, 1, wx.EXPAND)
        meterTableSizer.Add(meterTableMeter2Panel, 1, wx.EXPAND)



        leftSizer.Add(leftH1Sizer, 0, wx.EXPAND)
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

        measurementSummaryTxt = wx.StaticText(self, label=self.measSummLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        measurementSummaryTxt.SetFont(headerFont)
        rightH1Sizer.Add(measurementSummaryTxt, 1, wx.EXPAND)

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

    def OnPlot(self, e):
        self.plotBtn.Disable()
        try:
            self.GeneratePlot()
            self.plotBtn.Enable()
        except:
            print e
            self.plotBtn.Enable()
        e.Skip()

    def GeneratePlot(self):
        panelObjs = self.GetParent().table.panelObjs

        isIncreasing = True
        if float(panelObjs[0].distance) > float(panelObjs[1].distance):
            isIncreasing = False

        fig, ax = plt.subplots(2, facecolor="white", sharex=True, figsize=(10,10))
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
        pierTagLineList = [] # List of lists with index 0 being start pier tagmark, index 1 being end pier tagmark
        pierDepthList = [] # List of lists with index 0 being start pier depth, index 1 being end pier depth
        for i in range(len(panelObjs)):
            if panelObjs[i].distance!="":
                tagmarkList.append(panelObjs[i].distance)
                if i != len(panelObjs)-1:
                    #if isIncreasing:
                    tagmarkLineList.append(float(panelObjs[i].distance) - abs((float(panelObjs[i+1].distance) - float(panelObjs[i].distance))/2))
                    if panelObjs[i].panelType==0:
                        if "start p" in panelObjs[i].panelNum.lower() or "end p" in panelObjs[i].panelNum.lower():
                            pierTagLineList.append(float(panelObjs[i].distance) - abs((float(panelObjs[i+1].distance) - float(panelObjs[i].distance))/2))
                            pierDepthList.append(float(panelObjs[i].depth))
                    #else:
                    #tagmarkLineList.append(float(panelObjs[i].distance) - (float(panelObjs[i].distance) - float(panelObjs[i+1].distance))/2)
                # For end edge
                if i == len(panelObjs)-1:
                    #if isIncreasing:
                    #    tagmarkLineList.append(float(panelObjs[i].distance) - (float(panelObjs[i].distance) - float(panelObjs[i-1].distance))/2)
                    #else:
                    tagmarkLineList.append(float(panelObjs[i].distance) - abs((float(panelObjs[i-1].distance) - float(panelObjs[i].distance))/2))
            if panelObjs[i].flow!="":
                flowList.append(panelObjs[i].flow)
                flowTagList.append(float(panelObjs[i].distance))
            if panelObjs[i].corrMeanVelocity!="":
                veloList.append(panelObjs[i].corrMeanVelocity)
                veloTagList.append(float(panelObjs[i].distance))
            if panelObjs[i].depth!="":
                depthList.append(float(panelObjs[i].depth))
                depthTagList.append(float(panelObjs[i].distance))
            if panelObjs[i].panelType==1:
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
            if panelObjs[i].panelType==0:
                bottomIceList.append(0)
                iceTagList.append(float(panelObjs[i].distance))
                bottomSlushList.append(0)
                slushTagList.append(float(panelObjs[i].distance))
                #edgeTagmarkList.append(panelObjs[i].distance)
                #dgeDepthList.append(panelObjs[i].depth)
                # Here, I assume if there is start pier, the next panel will be end pier ALWAYS
                #if "start p" in panelObjs[i].panelNum.lower():
                #    pierTagLineList.append([float(panelObjs[i].distance),float(panelObjs[i+1].distance)])
                #    pierDepthList.append([float(panelObjs[i].depth),float(panelObjs[i+1].depth)])
        try:
            if panelObjs[0].leftOrRight!="":
                leftOrRight = panelObjs[0].leftOrRight
	        edgeTagmarkPos = float(panelObjs[0].distance)
	        edgeDepthPos = float(panelObjs[0].depth)
	except:
            pass


        # Plot Flow
        lns1, = ax[0].step(flowTagList, flowList,where='mid',linewidth=2, color="purple", label="Discharge(q/Q%)")
        # Plot Velocity
        lns2, = velo.plot(veloTagList, veloList, color="blue", label="Velocity")



        ax[1].invert_yaxis()
        if ("left" in leftOrRight.lower() and not isIncreasing) or ("right" in leftOrRight.lower() and isIncreasing):
            ax[1].invert_xaxis()

        # Depth curve
        lns3 = ax[1].fill_between(depthTagList,depthList, facecolor="#91c7f7", edgecolor="#91c7f7", label="River Body")
        # Ice
        lns4 = ax[1].fill_between(iceTagList,bottomIceList, facecolor="#e5e5e5", edgecolor="#e5e5e5", label="Ice")
        lns5 = ax[1].fill_between(slushTagList,bottomSlushList, facecolor="#c4c4c4", edgecolor="#c4c4c4", label="Slush Ice")

        # observation points for edge
        #for tagmark, depth in zip(edgeTagmarkList, edgeDepthList):
        #    ax[1].plot(tagmark, depth, "ro", marker="s", label="Obsevation Points")

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

        # Pier/Island
        pierTagLineList = pierTagLineList[1::2]

        if isIncreasing:
            y = np.interp(pierTagLineList, depthTagList, depthList)
        else:
            y = np.interp(pierTagLineList, depthTagList[::-1], depthList[::-1])

        lns = [lns1, lns2, lns3, lns4, lns5, lns6, lns7]
        labels=["Discharge(q/Q%)","Velocity","River Body","Ice","Slush Ice","Obsevation Points","Panel Boundary"]

        lns8 = None
        if len(pierTagLineList)>0 and len(y)>0:
            markerline, stemlines, baseline = ax[1].stem(pierTagLineList, y, markerfmt=" ", linefmt="#844b0a", label="Pier/Island")
            plt.setp(stemlines, 'linewidth', 3)
            lns8, = ax[1].plot(1,1,color="#844b0a", linewidth=3)
            lns.append(lns8)
            labels.append("Pier/Island [graphical display still under development]")


        #box = ax[0].get_position()
        #ax[0].set_position([box.x0, box.y0 + box.height*0.6, box.width, box.height])
        #box = ax[1].get_position()
        #ax[1].set_position([box.x0, box.y0 + box.height *0.6, box.width, box.height])
        #ax[1].legend(lns,labels,loc='upper center', bbox_to_anchor=(0.5, -0.15),fancybox=True, shadow=True, ncol=5, numpoints=1, borderaxespad=0.)
        ax[1].legend(lns,labels,loc='best', numpoints=1, borderaxespad=0.)

        lns7.set_visible(False)
        if lns8 is not None:
            lns8.set_visible(False)

        ax[0].spines['left'].set_color('purple')
        ax[0].yaxis.label.set_color('purple')
        ax[0].tick_params(axis='y', colors='purple')
        velo.spines['right'].set_color('blue')
        velo.yaxis.label.set_color('blue')
        velo.tick_params(axis='y', colors='blue')

        ax[0].set_ylabel("Discharge (q/Q%)", fontsize=14, color="purple")
        velo.set_ylabel("Velocity (m/s)", fontsize=14, color="b")
        ax[1].set_xlabel("Tagmark (m)", fontsize=14)
        ax[1].set_ylabel("Depth (m)", fontsize=14)

        #ax[0].locator_params(nbins=10)
        ax[1].locator_params(axis='both', nbins=10)
        #velo.locator_params(nbins=10)

        ax[0].grid('on')
        ax[1].grid('on')

        ax[0].autoscale_view(True,True,True)
        ax[1].autoscale_view(True,True,True)

        #ax[1].annotate(leftOrRight, xy=(edgeTagmarkPos,edgeDepthPos), xycoords='data', textcoords='offset points')
        plt.show()

    def CalculateSummary(self):
        table = self.GetParent().table

        totalWidth = 0
        totalArea = 0
        totalDischarge = 0
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
        print summary
        self.UpdateSummary(summary)


    def UpdateSummary(self, values):
        self.numOfPanelCtrl.SetValue(values[0])
        self.widthCtrl.SetValue(str(round(float(values[1]),3)))
        self.areaCtrl.SetValue(sigfig.round_sig(float(values[2]),3))
        self.avgDepthCtrl.SetValue(str(round(float(values[3]),3)))
        self.avgVelCtrl.SetValue(sigfig.round_sig(float(values[4]),3))
        #self.avgVelCtrl.SetValue(str(round(float(values[4]),3)))
        self.totalDisCtrl.SetValue(sigfig.round_sig(float(values[5]),3))
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
