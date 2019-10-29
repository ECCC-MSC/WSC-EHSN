# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import sys
import math
from RatingCurveViewerToolManager import *
import FileDialog
from wx.lib.agw import ultimatelistctrl as ULC

import numpy as np
import matplotlib.pyplot as plt
import wx.lib.mixins.listctrl as listmix

class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, size=(-1, 185), style=wx.LC_REPORT|wx.LC_SORT_DESCENDING|wx.LC_HRULES|wx.LC_VRULES)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class RatingCurveViewerToolFrame(wx.Frame):

    ## Constructor: (mode, path, stnNum, disMeasManager, lang)
    ##      mode: displays certain print statements when set to "DEBUG"
    ##      path: file path to default folder location of rating files
    ##      stnNum: station number of the given station
    ##      disMeasManager: handle on DischargeMeasurementManager, used to send and pull data
    ##      lang: for displaying the dates in the Period of Applicability table
    def __init__(self, mode, path, stnNum, disMeasManager, lang, manager, *args, **kwargs):
        super(RatingCurveViewerToolFrame, self).__init__(*args, **kwargs)

        self.titleLbl = "Rating Curve Viewer Tool"
        self.inputDataLbl = "Input Data"
        self.ratingInfoLbl = "Rating Information"
        self.curveNumLbl = "Curve Number"
        self.periodOfAppLbl = "Periods of Applicability"
        self.histFieldDataLbl = "Historical Field Data"
        self.browseButtonLbl = "Browse"
        self.fileOpenTitle = "Import Rating Information"

        self.obsStageDischLbl = "Observed Stage and Discharge"
        self.obsStageLbl = "Observed Stage (m)"
        self.obsDischLbl = u"Observed Discharge (m\N{SUPERSCRIPT THREE}/s)"
        self.refreshButtonLbl = "Refresh"

        self.calcShiftDischDiffLbl = "Calculated Shift and Discharge Difference"
        self.shiftLbl = "Shift (m)"
        self.rdischLbl = u"Rated Discharge (m\N{SUPERSCRIPT THREE}/s)"
        self.dischDiffLbl = "Discharge Difference (%)"
        self.calculateButtonLbl = "Calculate"
        self.plotButtonLbl = "Plot"
        self.exitButtonLbl = "Exit"
        self.toolTip = '2010-09-24 10:17:00 [UTC-05:00] | 0.195 | 0.859 | -7.15 | -0.0058\n'
        self.toolTips = self.toolTip * 4
        self.fig = None
        self.iconName = "icon_transparent.ico"
        self.plotControl = True
        self.titleFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        self.labelWidth = 125

        self.mode = mode
        self.lang = lang
        self.path = path
        self.stnNum = stnNum
        self.SetTitle(self.titleLbl)

        self.InitUI()

        self.manager = manager # RatingCurveViewerToolManager(self.mode, self.path, stnNum, disMeasManager, self.lang, self)
        self.manager.gui = self
        self.EnableXML(False)


    def InitUI(self):
        if self.mode == "DEBUG":
            print "Setup Rating Curve Viewer Tool Panel"

        # self.locale = wx.Locale(self.lang)

        self.basePanel = wx.Panel(self)
        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)


        icon_path = self.iconName
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, icon_path)

        #PNG Icon
        if os.path.exists(icon_path):
            png = wx.Image(icon_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.icon = wx.Icon(png)
            self.SetIcon(self.icon)

        #Input Data
        inputDataLabel = wx.StaticText(self.basePanel, label=self.inputDataLbl)
        inputDataLabel.SetFont(self.titleFont)

        #Rating Info Line
        ratingInfoSizer = wx.BoxSizer(wx.HORIZONTAL)
        ratingInfoLabel = wx.StaticText(self.basePanel, label=self.ratingInfoLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        self.ratingInfoText = wx.StaticText(self.basePanel, size=(100, -1), style=wx.SUNKEN_BORDER)

        self.ratingInfoButton = wx.Button(self.basePanel, label=self.browseButtonLbl)
        self.ratingInfoButton.Bind(wx.EVT_BUTTON, self.OnRatingInfo)

        ratingInfoSizer.Add(ratingInfoLabel, 0, wx.TOP, 5)
        ratingInfoSizer.Add((5, 0))
        ratingInfoSizer.Add(self.ratingInfoText, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 3)
        ratingInfoSizer.Add(self.ratingInfoButton, 0, wx.LEFT, 5)

        #Rating Curve Line
        ratingCurveSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ratingCurveLabel = wx.StaticText(self.basePanel, label=self.curveNumLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        self.ratingCurveCombo = wx.ComboBox(self.basePanel, choices=[], value="", style=wx.CB_READONLY)

        self.ratingCurveCombo.Bind(wx.EVT_COMBOBOX, self.OnRCUpdate)

        ratingCurveSizer.Add(self.ratingCurveLabel, 0, wx.TOP, 5)
        ratingCurveSizer.Add((5, 0))
        ratingCurveSizer.Add(self.ratingCurveCombo, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 3)

        #Periods of Applicability
        periodOfAppSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.periodOfAppLabel = wx.StaticText(self.basePanel, label=self.periodOfAppLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        self.periodOfAppList = wx.ListCtrl(self.basePanel, style=wx.LC_REPORT, size=(290, -1))
        self.periodOfAppList.InsertColumn(0, 'Curve #')
        self.periodOfAppList.InsertColumn(1, 'From')
        self.periodOfAppList.InsertColumn(2, 'To')
        self.periodOfAppList.SetColumnWidth(0, 70)
        self.periodOfAppList.SetColumnWidth(1, 115)
        self.periodOfAppList.SetColumnWidth(2, 115)

        self.periodOfAppList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectAppItem)

        periodOfAppSizer.Add(self.periodOfAppLabel, 0, wx.TOP, 6)
        periodOfAppSizer.Add(self.periodOfAppList, 1, wx.LEFT|wx.EXPAND, 5)


        #Historical Data Line
        histFieldDataSizer = wx.BoxSizer(wx.HORIZONTAL)
        histFieldDataLabel = wx.StaticText(self.basePanel, label=self.histFieldDataLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        histFieldDataLabel.SetToolTip(wx.ToolTip('For example:\n' + self.toolTips))
        histFieldDataLabel.SetForegroundColour((0,0,255))
        histFieldDataLabel.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False))
        self.histFieldDataText = wx.StaticText(self.basePanel, style=wx.SUNKEN_BORDER|wx.ST_NO_AUTORESIZE)

        self.histFieldDataButton = wx.Button(self.basePanel, label=self.browseButtonLbl)
        self.histFieldDataButton.Bind(wx.EVT_BUTTON, self.OnHistoricalData)

        histFieldDataSizer.Add(histFieldDataLabel, 0, wx.TOP, 5)
        histFieldDataSizer.Add((5, 0))
        histFieldDataSizer.Add(self.histFieldDataText, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 3)
        histFieldDataSizer.Add(self.histFieldDataButton, 0, wx.LEFT, 5)


        #Observed Stage and Discharge
        obsStageDischSizer = wx.BoxSizer(wx.HORIZONTAL)
        obsStageDischLabel = wx.StaticText(self.basePanel, label=self.obsStageDischLbl)
        obsStageDischLabel.SetFont(self.titleFont)

        obsStageDischSizer.Add(obsStageDischLabel, 0, wx.EXPAND|wx.TOP, 6)

        #Observed Stage
        obsStageSizer = wx.BoxSizer(wx.HORIZONTAL)
        obsStageLabel = wx.StaticText(self.basePanel, label=self.obsStageLbl)
        # self.obsStageText = wx.StaticText(self.basePanel, size=(100, -1), style=wx.BORDER_SUNKEN|wx.ALIGN_RIGHT)
        self.obsStageText = wx.TextCtrl(self.basePanel)

        obsStageSizer.Add((5, 0))
        obsStageSizer.Add(obsStageLabel, 0, wx.EXPAND|wx.TOP, 5)
        obsStageSizer.Add(self.obsStageText, 0, wx.EXPAND|wx.LEFT, 10)

        #Observed Discharge
        obsDischSizer = wx.BoxSizer(wx.HORIZONTAL)
        obsDischLabel = wx.StaticText(self.basePanel, label=self.obsDischLbl)
        # self.obsDischText = wx.StaticText(self.basePanel, size=(100, -1), style=wx.BORDER_SUNKEN|wx.ALIGN_RIGHT)
        self.obsDischText = wx.TextCtrl(self.basePanel)

        obsDischSizer.Add((5, 0))
        obsDischSizer.Add(obsDischLabel, 0, wx.EXPAND|wx.TOP, 5)
        obsDischSizer.Add(self.obsDischText, 0, wx.EXPAND|wx.LEFT, 10)


        #Calculated Shift and Discharge Difference
        calcShiftDischDiffLabel = wx.StaticText(self.basePanel, label=self.calcShiftDischDiffLbl)
        calcShiftDischDiffLabel.SetFont(self.titleFont)

        #Shift
        shiftSizer = wx.BoxSizer(wx.HORIZONTAL)
        shiftLabel = wx.StaticText(self.basePanel, label=self.shiftLbl)
        self.shiftText = wx.StaticText(self.basePanel, size=(100, -1), style=wx.BORDER_SUNKEN|wx.ALIGN_RIGHT)

        shiftSizer.Add((5, 0))
        shiftSizer.Add(shiftLabel, 0, wx.EXPAND|wx.TOP, 5)
        shiftSizer.Add(self.shiftText, 0, wx.EXPAND|wx.LEFT, 10)

        # Rated Discharge
        rdischSizer = wx.BoxSizer(wx.HORIZONTAL)
        rdischLabel = wx.StaticText(self.basePanel, label=self.rdischLbl)
        self.rdischText = wx.StaticText(self.basePanel, size=(100, -1), style=wx.BORDER_SUNKEN|wx.ALIGN_RIGHT)

        rdischSizer.Add((5, 0))
        rdischSizer.Add(rdischLabel, 0, wx.EXPAND|wx.TOP, 5)
        rdischSizer.Add(self.rdischText, 0, wx.EXPAND|wx.LEFT, 10)

        #Discharge Difference
        dischDiffSizer = wx.BoxSizer(wx.HORIZONTAL)
        dischDiffLabel = wx.StaticText(self.basePanel, label=self.dischDiffLbl)
        self.dischDiffText = wx.StaticText(self.basePanel, size=(100, -1), style=wx.SUNKEN_BORDER|wx.ALIGN_RIGHT)

        dischDiffSizer.Add((5, 0))
        dischDiffSizer.Add(dischDiffLabel, 0, wx.EXPAND|wx.TOP, 5)
        dischDiffSizer.Add(self.dischDiffText, 0, wx.EXPAND|wx.LEFT, 10)


        #Buttons line
        buttonsSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.calculateButton = wx.Button(self.basePanel, label=self.calculateButtonLbl)
        self.calculateButton.Bind(wx.EVT_BUTTON, self.OnCalculate)
        self.plotButton = wx.Button(self.basePanel, label=self.plotButtonLbl)
        self.plotButton.Bind(wx.EVT_BUTTON, self.OnPlot)
        self.exitButton = wx.Button(self.basePanel, label=self.exitButtonLbl)
        self.exitButton.Bind(wx.EVT_BUTTON, self.OnExit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        buttonsSizer1.Add((1, 0), 1, wx.EXPAND)
        buttonsSizer1.Add(self.calculateButton, 0, wx.EXPAND|wx.RIGHT, 4)
        buttonsSizer1.Add(self.plotButton, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 4)

        buttonsSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer2.Add((1, 0), 1, wx.EXPAND)
        buttonsSizer2.Add(self.exitButton, 0, wx.EXPAND|wx.LEFT, 4)


        # Historical Data Table
        self.histDataList = AutoWidthListCtrl(self.basePanel)

        # self.histDataList.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)
        self.histDataList.InsertColumn(0, 'Date/Time')
        self.histDataList.InsertColumn(1, 'Stage (m)')
        self.histDataList.InsertColumn(2, u'Discharge (m\N{SUPERSCRIPT THREE}/s)')
        self.histDataList.InsertColumn(3, 'Width (m)')
        self.histDataList.InsertColumn(4, u'Area (m\N{SUPERSCRIPT TWO})')
        self.histDataList.InsertColumn(5, u'Velocity (m\N{SUPERSCRIPT TWO})/s')
        self.histDataList.InsertColumn(6, 'R Error (%)')
        self.histDataList.InsertColumn(7, 'Shift (m)')
        self.histDataList.InsertColumn(8, 'Remarks')
        self.histDataList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectHistDataItem)




        #Add everything to the layout sizers
        THSizer = wx.BoxSizer(wx.HORIZONTAL)
        VLSizer = wx.BoxSizer(wx.VERTICAL)
        VRSizer = wx.BoxSizer(wx.VERTICAL)

        THSizer.Add(VLSizer, 1, wx.EXPAND)
        THSizer.Add(VRSizer, 0, wx.EXPAND)

        # Top Left Sizer
        VLSizer.Add(inputDataLabel, 0, wx.EXPAND|wx.LEFT|wx.UP, 3)
        VLSizer.Add(ratingInfoSizer, 0, wx.EXPAND|wx.ALL, 3)
        VLSizer.Add(ratingCurveSizer, 0, wx.EXPAND|wx.ALL, 3)
        VLSizer.Add(periodOfAppSizer, 0, wx.EXPAND|wx.ALL, 3)
        VLSizer.Add(histFieldDataSizer, 0, wx.EXPAND|wx.ALL, 3)

        # Top Right Sizer
        VRSizer.Add((0, 20))
        VRSizer.Add(obsStageDischSizer, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add(obsStageSizer, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add(obsDischSizer, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add((0, 20))
        VRSizer.Add(calcShiftDischDiffLabel, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add(shiftSizer, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add(rdischSizer, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add(dischDiffSizer, 0, wx.EXPAND|wx.ALL, 3)
        VRSizer.Add((0, 20))
        VRSizer.Add(buttonsSizer1, 0, wx.EXPAND|wx.ALL, 3)

        # Base Layout Sizer
        self.layoutSizer.Add(THSizer, 1, wx.EXPAND)
        self.layoutSizer.Add((0, 5))
        self.layoutSizer.Add(self.histDataList, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add((0, 10))
        self.layoutSizer.Add(buttonsSizer2, 0, wx.EXPAND|wx.ALL, 3)

        self.basePanel.SetSizer(self.layoutSizer)

        self.CreateStatusBar(style=wx.STB_SIZEGRIP|wx.STB_SHOW_TIPS|wx.STB_ELLIPSIZE_END|wx.FULL_REPAINT_ON_RESIZE)

        self.Layout()



    def OnColClick(self, event):
        print "column clicked"
        self.histDataList.SortItems()
        event.Skip()


    def OnRatingInfo(self, evt):
        #filetypeString = 'Rating Curve Information Files (*.xml;*.txt)|*.xml;*.txt'
        filetypeString = 'Rating Curve Information Files (*.xml;*.txt, *.json)|*.xml;*.txt;*.json'
        fileOpenDialog = wx.FileDialog(self, self.fileOpenTitle, self.path, '',
                            filetypeString, style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        self.OnOpenRatingFile(fileOpenDialog.GetPath())

        self.SetCalcShift("")
        self.SetDischDiff("")

        evt.Skip()

    def OnRCUpdate(self, e):
        print "RC choice updated"

        self.RCUpdate()

        e.Skip()


    def RCUpdate(self):
        self.manager.OnRCUpdate(self.GetSelectedCurveIndex())


    def OnSelectAppItem(self, evt):
        item = -1
        while True:
            item = self.periodOfAppList.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

            if item == -1:
                break

            self.periodOfAppList.SetItemState(item, 0, wx.LIST_STATE_SELECTED)

        evt.Skip()


    def OnSelectHistDataItem(self, evt):
        item = -1
        while True:
            item = self.histDataList.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

            if item == -1:
                break

            self.histDataList.SetItemState(item, 0, wx.LIST_STATE_SELECTED)

        evt.Skip()


    def OnHistoricalData(self, evt):
        filetypeString = 'Historical Field Data (*.csv)|*.csv'

        fileOpenDialog = wx.FileDialog(self, self.fileOpenTitle, self.path, '',
                            filetypeString, style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        self.OpenHistDataFile(fileOpenDialog.GetPath())
        self.histDataList.SetColumnWidth(0, -1)
        self.histDataList.SetColumnWidth(1, -2)
        self.histDataList.SetColumnWidth(2, -2)
        self.histDataList.SetColumnWidth(3, -2)
        self.histDataList.SetColumnWidth(4, -2)
        self.histDataList.SetColumnWidth(5, -2)
        self.histDataList.SetColumnWidth(6, -2)
        self.histDataList.SetColumnWidth(7, -2)
        self.histDataList.SetColumnWidth(8, -1)

        evt.Skip()


    def OnOpenRatingFile(self, filepath):
        if self.manager is not None:
            self.manager.OpenRatingFile(filepath)

            self.layoutSizer.Layout()
            self.Update()
            self.Refresh()


    def OpenHistDataFile(self, filepath):
        if self.manager is not None:
            self.manager.OpenHistDataFile(filepath)

            self.layoutSizer.Layout()
            self.Update()
            self.Refresh()

    #Get the stage and discharge from the front page of the EHSN (call manager)
    def GetStageDischarge(self):
        if self.manager is None:
            return
        self.manager.FetchStageDischarge()


    #Calculate the shift and discharge difference (call manager)
    def OnCalculate(self, evt):
        if self.mode == "DEBUG":
            print "CALCULATE BUTTON CLICKED"

        if self.manager is None:
            return

        self.manager.CalculateShiftDisch(self.GetObsStage(), self.GetObsDisch(), self.GetSelectedCurveIndex())


    #Plot the Rating Curve
    def OnPlot(self, evt):

        if self.mode == "DEBUG":
            print "PLOT BUTTON CLICKED"
        if self.manager is None:
            return
        if self.GetObsStage() != "" and self.GetObsDisch() != "":

            self.manager.CalculateShiftDisch(self.GetObsStage(), self.GetObsDisch(), self.GetSelectedCurveIndex())
        else:
            self.manager.obsDisch = None
            self.manager.obsStage = None


        #for testing when remove the try block above
        self.manager.PlotData()
        # self.isPlot = True
        # if self.isPlot:
        #     self.plotButton.Enable(False)
        evt.Skip()


    def OnExit(self, evt):
        if self.mode == "DEBUG":
            print "EXIT BUTTON CLICKED"
        self.Destroy()

        evt.Skip()


    def EmptyCalculatedFields(self):
        self.SetCalcShift("")
        self.SetRatedDisch("")
        self.SetDischDiff("")

    #Enable or Disable curve based on en
    def EnableXML(self, en):
        self.ratingCurveLabel.Enable(en)
        self.ratingCurveCombo.Enable(en)
        self.periodOfAppLabel.Enable(en)
        self.periodOfAppList.Enable(en)

    # Enables/Disables plot button
    def EnablePlot(self, en):
        self.plotButton.Enable(en)

        self.plotControl = en

    def GeneratePlot(self):
        print "generatePlot"
        self.fig, ax = plt.subplots(1, 1)
        plt.grid(True)
        self.fig.set_facecolor('white')


        lns = None

        # Plotting the curve
        if self.manager.extension == "xml":
            selectedCurveIndex = self.GetSelectedCurveIndex()
            RCType = self.manager.data[selectedCurveIndex][0].get('type')
            if RCType == "Logarithmic":

                ratingpoints = self.manager.data[selectedCurveIndex][2]
                for i, rpoint in enumerate(ratingpoints):
                    equation = rpoint.find('equation')

                    # We use sample points to draw the curve
                    # For each segment of the curve, allocate its
                    # percentage of the total curve in points for drawing
                    if equation is not None:
                        offset = float(rpoint.find('offset').text)
                        beta = float(equation.find('beta').text)
                        c = float(equation.find('c').text)

                        q2 = float(rpoint.find('qr').text)
                        q1 = float(ratingpoints[i-1].find('qr').text)
                        hg2 = float(rpoint.find('hg').text)
                        hg1 = float(ratingpoints[i-1].find('hg').text)

                        if not math.isinf(beta) or not math.isinf(c):
                            # Plotting curve based on percentage of total
                            if self.manager.qrta is not None:
                                num = int(max(1, 800*(q2-q1)/(self.manager.qrta[-1] - self.manager.qrta[0])))
                            else:
                                num = int(max(1, 800*(q2-q1)))
                            x = np.linspace(q1, q2, num)
                            y = (x/c)**(1/beta) + offset

                        else:
                            x = [q1, q2]
                            y = [hg1, hg2]

                        lns = plt.plot(x, y, color="r", label="Rating Curve")
            else:

                if self.manager.qrta is not None:
                    lns = plt.plot(self.manager.qrta, self.manager.hgta, color='r', label="Rating Curve")        # Plotting straight lines between the points
        #else:
        #    if self.manager.extension is not None and \
        #        self.manager.qrta is not None and self.manager.hgta is not None:
        #        lns = plt.plot(self.manager.qrta, self.manager.hgta, color='r', label="Rating Curve")        # Plotting straight lines between the points


        # read from json file to plot rating curve
        elif self.manager.extension == "json":
            selectedCurveIndex = self.GetSelectedCurveIndex()

            #discharge
            qrta = []
            #stage
            hgta = []

            for pot in self.manager.data['RatingCurves'][selectedCurveIndex]['BaseRatingTable']:
                qrta.append(float(pot['OutputValue']))
                hgta.append(float(pot['InputValue']))

            self.manager.qrpa = qrta
            self.manager.hgpa = hgta

            self.manager.qrta = self.manager.qrpa
            self.manager.hgta = self.manager.hgpa

            if self.manager.data['RatingCurves'][selectedCurveIndex]['Type'] == 'LogarithicTable':
                #the list of the offset
                offsetList = []

                #the list of the break point
                breakPointList = []

                #the list of the curve points
                curvePointList = []

                for offset_val in self.manager.data['RatingCurves'][selectedCurveIndex]['Offsets']:
                    offsetList.append(offset_val['Offset'])
                    try:
                        breakPointList.append(offset_val['InputValue'])
                    except:
                        pass
                # print offsetList
                # print breakPointList

                for num in range(len(qrta)):
                    curvePoint = []
                    curvePoint.append(hgta[num])
                    curvePoint.append(qrta[num])
                    for nn in range(len(breakPointList)):
                        if curvePoint[0]<=breakPointList[nn]:
                            curvePoint.append(offsetList[nn])
                            break
                    if len(curvePoint)<3:
                        curvePoint.append(offsetList[-1])
                    curvePointList.append(curvePoint)
                # print curvePointList

                #the whole distance of the discharge
                maxDis = curvePointList[-1][1]-curvePointList[0][1]

                #calculate the equation
                for equNum in range(len(curvePointList)-1):
                    sta1 = curvePointList[equNum][0]
                    disch1 = curvePointList[equNum][1]
                    offset1 = curvePointList[equNum][2]

                    sta2 = curvePointList[equNum+1][0]
                    disch2 = curvePointList[equNum+1][1]
                    offset2 = curvePointList[equNum+1][2]

                    pointNum = int(max(1,800*(disch2-disch1)/maxDis))

                    #print "all : "
                    #print sta1,disch1,offset1,sta2,disch2,offset2
                    beta = math.log10(disch2/disch1)/math.log10((sta2-offset2)/(sta1-offset2))

                    c = disch1/math.pow(sta1-offset2, beta)
                    #print "c: "
                    #print c
                    x = np.linspace(disch1, disch2, num)
                    y = (x/c)**(1/beta) + offset2

                    print "x: "
                    print x
                    print "y: "
                    print y

                    lns = plt.plot(x, y, color="r", label="Rating Curve")
                    print "lns: "
                    print lns
            else:
                lns = plt.plot(qrta, hgta, color='r', label="Rating Curve")
        else:
            if self.manager.extension is not None and \
                self.manager.qrta is not None and self.manager.hgta is not None:
                lns = plt.plot(self.manager.qrta, self.manager.hgta, color='r', label="Rating Curve")        # Plotting straight lines between the points


        # Hist values
        if self.manager.dischargeHist is not None and self.manager.stageHist is not None:
            for x in self.manager.validHistPoints:
                label = x[0]
                y = x[2]
                z = x[1]
                plt.annotate(label.strftime("%Y-%m-%d"), xy=(y, z), size=10)

            ln2 = plt.plot(self.manager.dischargeHist, self.manager.stageHist, "yo", markersize=9, zorder=3, alpha=0.75, label="Hist. mmts.")               # Plotting Hisorical Field MMt
            if lns is not None:
                lns = lns + ln2
            else:
                lns = ln2

        # min/max values
        if len(self.manager.minList)>0:
            qList=[]
            hList=[]
            for row in self.manager.minList:
                label = row[0].split(" ")[0] ##Date
                q = row[2]
                h = row[1]
                qList.append(q)
                hList.append(h)
                plt.annotate(str(label), xy=(q,h), size=10)

            ln3 = plt.plot(qList, hList, "co", markersize=9, zorder=3, alpha=0.75, label="Hist. Min")
            if lns is not None:
                lns = lns + ln3
            else:
                lns = ln3

        if len(self.manager.maxList)>0:
            qList=[]
            hList=[]
            for row in self.manager.maxList:
                label = row[0].split(" ")[0] ##Date
                q = row[2]
                h = row[1]
                qList.append(q)
                hList.append(h)
                plt.annotate(str(label), xy=(q,h), size=10)

            ln4 = plt.plot(qList, hList, "bo", markersize=9, zorder=3, alpha=0.75, label="Hist. Max")
            if lns is not None:
                lns = lns + ln4
            else:
                lns = ln4

        # Plotting observed point
        if self.manager.Qdiff is not None and (self.manager.obsDisch is not None and self.manager.obsStage is not None):
            if abs(self.manager.Qdiff) >= 5:
                plt.plot(self.manager.obsDisch, self.manager.obsStage, "ro", markersize=10, zorder=4)  # Plotting Qobs , Hobs
            elif abs(self.manager.Qdiff) < 5:
                plt.plot(self.manager.obsDisch, self.manager.obsStage, "go", markersize=10, zorder=4)  # Plotting Qobs , Hobs

        if self.manager.qrta is not None and self.manager.hgta is not None:
            ln5 = plt.plot(self.manager.qrta, self.manager.hgta, "c^", markersize=5, zorder=2, label="Rating Points")  # Plotting rating points
            if lns is not None:
                lns = lns + ln5
            else:
                lns = ln5

        labels = [l.get_label() for l in lns]
        plt.legend(lns, labels, loc=2, numpoints=1, framealpha=0.5)

        lowx = None
        highx = None
        lowy = None
        highy = None
        if self.manager.obsDisch is not None and self.manager.obsStage is not None and \
           self.manager.Qr is not None and self.manager.Hr is not None:
            plt.plot([self.manager.obsDisch,self.manager.obsDisch], [self.manager.obsStage, self.manager.Hr], 'b') # Plotting the Shift Line
            plt.plot([self.manager.obsDisch,self.manager.Qr], [self.manager.obsStage, self.manager.obsStage], 'b')

            # Zoom
            lowx = min(self.manager.Qr, self.manager.obsDisch) - abs(self.manager.Qr - self.manager.obsDisch)/4
            highx = max(self.manager.Qr, self.manager.obsDisch) + abs(self.manager.Qr - self.manager.obsDisch)/1.5
            lowy = min(self.manager.Hr, self.manager.obsStage) - abs(self.manager.Hr - self.manager.obsStage)/1.5
            highy = max(self.manager.Hr, self.manager.obsStage) + abs(self.manager.Hr - self.manager.obsStage)/4

            # Plot line from observed point to Y-axis
            plt.plot([0, self.manager.Qr], [self.manager.obsStage, self.manager.obsStage], linestyle='--', linewidth=2,color='g')

        # Title
        plotTitle = ""
        if self.manager.stnNum is not None:
            plotTitle = "Station: " + self.manager.stnNum
        if self.manager.curveNum is not None:
            plotTitle += "\nRating Curve #" + self.manager.curveNum
        plt.title(plotTitle)

        # Axis labels
        plt.xlabel(u"Discharge [m\N{SUPERSCRIPT THREE}/s]", fontsize=14,color="k")
        plt.ylabel("Stage [m]", fontsize=14, color="k")

        # Shift and R Error calculations
        if self.manager.Shift is not None and self.manager.Qdiff is not None:
            plt.annotate("Shift (m):"+str(self.manager.Shift) + "\nR Error (%)=" + str(self.manager.Qdiff),
                         xy=(1, 0), xycoords='axes fraction',
                         bbox=dict(facecolor='white', edgecolor='black', alpha=0.5),
                         xytext=(-5, 5), textcoords='offset points',
                         ha='right', va='bottom', zorder=5)

        # Annotate warning if |Qdiff| >= 5%
        if self.manager.Qdiff is not None:
            if abs(self.manager.Qdiff) >= 5:
                plt.annotate(self.manager.comment, xy=(.98, 0.13), xycoords='axes fraction', ha='right', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round', alpha=0.9))
            elif abs(self.manager.Qdiff) < 5:
                plt.annotate(self.manager.comment2, xy=(.98, 0.13), xycoords='axes fraction', ha='right', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round', alpha=0.9))

        if self.manager.obsDisch is not None and self.manager.obsStage is not None:
            self.fig.canvas.toolbar.push_current()  # save the 'un zoomed' view to stack
            ax.set_xlim([lowx, highx])
            ax.set_ylim([lowy, highy])
            self.fig.canvas.toolbar.push_current()  # save 'zoomed' view to stack

        # number Scaling from zoom
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

        plt.show()


    def AddRowToAppRange(self, curveNum, fromDate, toDate):
        if self.mode == "DEBUG":
            print "Adding row to table"

        rowCount = self.periodOfAppList.GetItemCount()
        self.periodOfAppList.InsertItem(rowCount, curveNum)
        self.periodOfAppList.SetItem(rowCount, 1, fromDate)
        self.periodOfAppList.SetItem(rowCount, 2, toDate)

    def AddRowToHistData(self, date, stage, disch, width, area, waterVelo, error, shift, remarks):
        if self.mode == "DEBUG":
            print "Adding row to table"

        rowCount = self.histDataList.GetItemCount()
        self.histDataList.InsertItem(rowCount, date)
        self.histDataList.SetItem(rowCount, 1, stage)
        self.histDataList.SetItem(rowCount, 2, disch)
        self.histDataList.SetItem(rowCount, 3, width)
        self.histDataList.SetItem(rowCount, 4, area)
        self.histDataList.SetItem(rowCount, 5, waterVelo)
        self.histDataList.SetItem(rowCount, 6, error)
        self.histDataList.SetItem(rowCount, 7, shift)
        self.histDataList.SetItem(rowCount, 8, remarks)


    def ClearAllAppRows(self):
        if self.mode == "DEBUG":
            print "Clearing all rows"
        self.periodOfAppList.DeleteAllItems()

    def ClearAllHistRows(self):
        if self.mode == "DEBUG":
            print "Clearing all rows"
        self.histDataList.DeleteAllItems()

    def SetRatingInfo(self, riText):
        self.ratingInfoText.SetLabel(riText)
        self.ratingInfoText.GetParent().Layout()
        

    def SetObsStage(self, stage):
        self.obsStageText.SetLabel(stage)

    def SetObsDisch(self, disch):
        self.obsDischText.SetLabel(disch)

    # def GetObsStage(self):
    #     return self.obsStageText.GetLabel()

    # def GetObsDisch(self):
    #     return self.obsDischText.GetLabel()

    def GetObsStage(self):
        return self.obsStageText.GetValue()

    def GetObsDisch(self):
        return self.obsDischText.GetValue()


    def SetCurveCombo(self, curvelist, index=0):
        self.ratingCurveCombo.SetItems(curvelist)
        if len(curvelist) > 0:
            self.ratingCurveCombo.SetSelection(index)

        # self.RCUpdate()

    def GetSelectedCurveIndex(self):
        return self.ratingCurveCombo.GetCurrentSelection()

    def SetCalcShift(self, calcShift):
        self.shiftText.SetLabel(calcShift)

    def SetRatedDisch(self, ratedDisch):
        self.rdischText.SetLabel(ratedDisch)

    def SetDischDiff(self, dischDiff):
        self.dischDiffText.SetLabel(dischDiff)

    def GetCalcShift(self, calcShift):
        return self.shiftText.GetValue()

    def GetRatedDisch(self, ratedDisch):
        return self.rdischText.GetValue()

    def GetDischDiff(self, dischDiff):
        return self.dischDiffText.GetValue()

    # def FocusOnPlot(self):
    #     if not self.plotControl:
    #         self.fig = plt.gcf()
    #         self.fig.canvas.manager.window.raise_()

    def SetStatus(self, message):
        self.SetStatusText(message)

def main():
    app = wx.App()

    frame = RatingCurveViewerToolFrame("DEBUG", os.getcwd() + "\\RC docs", None, None, wx.LANGUAGE_ENGLISH, None, size=(770, 578))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
