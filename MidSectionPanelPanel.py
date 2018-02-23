# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
from wx.grid import *
import math
import NumberControl
import sigfig
from DropdownTime import *
from MidSectionSubPanelObj import *

#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""


class MidSectionPanelPanel(wx.Panel):
    def __init__(self, panelNum, panelId, modify, index, *args, **kwargs):
        super(MidSectionPanelPanel, self).__init__(*args, **kwargs)
        self.panelId = panelId
        self.index=index
        self.panelNum = panelNum
        self.modify = modify
        self.titleLbl = "Panel #:"
        self.panelLbl = "Panel #:"
        self.currentMeterLbl = "Current Meter:"
        self.meterEquationLbl = "Meter Equation:"
        self.slopeLbl1 = "Slope #1:"
        self.interceptLbl1 = "Intercept #1:"
        self.slopeLbl2 = "Slope #2:"
        self.interceptLbl2 = "Intercept #2:"
        self.measurementTimeLbl = "Measurement Time:"
        self.panelTagMarkLbl = "Panel Tagmark (m):"
        self.panelConditionLbl = "Panel Condition:"
        self.openWaterLbl = "Open Water"
        self.IceLbl = "Ice"
        self.depthLbl = "Depth Reading (m):"
        self.amountWeightLbl = "Amount of Weight (lb):"
        self.weightOffsetLbl = "Weight to Meter Offset (m):"
        self.wldlLbl = "WL/DL Correction:"
        self.dryLineAngleLbl = "Dry Line Angle (deg.):"
        self.distSurfaceLbl = "Dist. to Water Surface (m):"
        self.dryCorrectionLbl = "Dry Line Correction:"
        self.wetCorretionLbl = "Wet Line Correction:"
        self.effectiveDepthLbl = "Effective Depth (m):"
        self.corrections = ["No", "Yes", "Yes_w_Tags"]

        self.iceAssemblyLbl = "Ice Assembly:"
        self.meterAboveLbl = "Meter Above Footing:"
        self.meterBelowLbl = "Meter Below Footing:"
        self.distanceAboveLbl = "Distance Above Weight (m):"
        self.iceThickLbl = "Ice Thickness (m):"
        self.waterSurfaceIceLbl = "WS to Bottom of Ice (m):"
        self.adjustedLbl = "Adjusted:"
        self.waterSurfaceSlushLbl = "WS to Bottom of Slush (m):"
        self.slushThicknessLbl = "Slush Thickness (m):"
        self.slushLbl = "Slush:                                                    "

        self.velocityMethodLbl = "Velocity Method:"
        self.obliqueLbl = "Angle of Flow Correction:"
        self.velocityCorrLbl = "Velocity Corr. Factor:"
        self.reverseFlowLbl = "Reverse Flow:"

        self.mandatoryFieldsMsg = "You are missing the field: "

        self.panelConditions = ["Open", "Ice"]
        self.velocityMethods = ["0.5", "0.6", "0.2/0.8", "0.2/0.6/0.8", "Surface"]
        self.iceAssemblySelections = ["No_Weight", "NACA", "Pancake", "Slush", "USGS_Tipup", "Ice_Rod"]
        self.weights = ["0", "15", "30", "50", "75", "100", "150", "300"]
        self.meterOffsets = ["0", "0.21", "0.22", "0.31", "0.32", "0.33", "0.55", "0.55"]
        self.velocityCorrFactors = ["1.0", "0.88", "0.92"]
        self.currentMeters = []

        self.rawAtPointVel = ["", "", ""]
        self.rawMeanVal = ""

        self.height = 21
        self.headerHeight = 28
        self.ctrlWidth = 60
        self.lblWidth = 150
        self.panelNumber = -1

        self.summaryLblWidth = 132
        self.summaryHeight = 20
        self.summaryCtrlWidth = 100

        self.openWidth = 150



        self.backgrounColour = (242,242,242)
        self.textColour = (54,96,146)

        self.saveBtnLbl = "Save && Exit"
        self.cancelBtnLbl = "Cancel"
        self.nextBtnLbl = "Next"

        self.newPanel = True


        self.InitUI()

    def InitUI(self):
        #Header
        sizerV = wx.BoxSizer(wx.VERTICAL)
        self.headerTxt = wx.StaticText(self, label=self.titleLbl + " " + str(self.panelNum), size=(-1, 22), style=wx.ALIGN_CENTRE_HORIZONTAL)
        headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        self.headerTxt.SetFont(headerFont)
        self.headerTxt.SetBackgroundColour('grey')

        #Depth Summary
        summarySizer = wx.BoxSizer(wx.HORIZONTAL)
        summaryLeftSizer = wx.BoxSizer(wx.VERTICAL)
        summaryRightSizer = wx.BoxSizer(wx.VERTICAL)
        summarySizer.Add(summaryLeftSizer, 1, wx.EXPAND)
        summarySizer.Add(summaryRightSizer, 1, wx.EXPAND)



        #Panel #
        panelNumberSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelNumberTxt = wx.StaticText(self, label=self.panelLbl, size=(self.summaryLblWidth, self.summaryHeight))
        self.panelNumberCtrl = wx.TextCtrl(self, size=(self.summaryCtrlWidth, self.summaryHeight))
        self.panelNumberCtrl.SetValue(str(self.panelNum))
        self.panelNumberCtrl.Disable()

        panelNumberSizer.Add(panelNumberTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        panelNumberSizer.Add(self.panelNumberCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Measurement Time
        measurementTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        measurementTimeTxt = wx.StaticText(self, label=self.measurementTimeLbl, size=(self.summaryLblWidth, self.headerHeight))
        # self.measurementTimeCtrl = wx.TextCtrl(self, size=(-1, self.height))
        self.measurementTimeCtrl = DropdownTime(False, parent=self, size=(self.summaryCtrlWidth, self.headerHeight), style=wx.BORDER_NONE)
        self.measurementTimeCtrl.UpdateTime(67)
        measurementTimeSizer.Add(measurementTimeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        measurementTimeSizer.Add(self.measurementTimeCtrl, 1, wx.EXPAND)
        # print self.measurementTimeCtrl.GetSize()

        #panel TagMark Distance (m)
        panelTagMarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelTagMarkTxt = wx.StaticText(self, label=self.panelTagMarkLbl, size=(self.summaryLblWidth, self.summaryHeight))
        self.panelTagMarkCtrl = MyTextCtrl(self, size=(self.summaryCtrlWidth, self.summaryHeight), style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
        self.panelTagMarkCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnTagmarkTabEnter)
        self.panelTagMarkCtrl.Bind(wx.EVT_NAVIGATION_KEY, self.OnTagmarkTabEnter)
        self.panelTagMarkCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.panelTagMarkCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        panelTagMarkSizer.Add(panelTagMarkTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        panelTagMarkSizer.Add(self.panelTagMarkCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Panel Condition
        panelConditionSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelConditionTxt = wx.StaticText(self, label=self.panelConditionLbl, size=(self.summaryLblWidth, self.summaryHeight))
        self.panelConditionCombox = wx.ComboBox(self, style=wx.CB_READONLY, choices=self.panelConditions, size=(self.summaryCtrlWidth, self.summaryHeight))
        panelConditionSizer.Add(panelConditionTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        panelConditionSizer.Add(self.panelConditionCombox, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        self.panelConditionCombox.SetSelection(0)

        summaryLeftSizer.Add(panelNumberSizer, 1, wx.EXPAND)
        summaryLeftSizer.Add(measurementTimeSizer, 1, wx.EXPAND)
        summaryLeftSizer.Add(panelTagMarkSizer, 1, wx.EXPAND)
        summaryLeftSizer.Add(panelConditionSizer, 1, wx.EXPAND)


        #Current Meter
        currentMeterSizer = wx.BoxSizer(wx.HORIZONTAL)
        currentMeterTxt = wx.StaticText(self, label=self.currentMeterLbl, size=(-1, self.summaryHeight))
        # self.currentMeterCtrl = wx.TextCtrl(self, size=(-1, self.summaryHeight))
        self.currentMeterCtrl = wx.ComboBox(self, size=(-1, self.summaryHeight), choices=self.currentMeters)
        self.currentMeterCtrl.Bind(wx.EVT_COMBOBOX, self.OnCurrMeterCtrl)
        currentMeterSizer.Add(currentMeterTxt, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        currentMeterSizer.Add(self.currentMeterCtrl, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        # #Meter Equation
        # meterEquationSizer = wx.BoxSizer(wx.HORIZONTAL)
        # meterEquationTxt = wx.StaticText(self, label=self.meterEquationLbl, size=(-1, self.summaryHeight))
        # meterEquationSizer.Add(meterEquationTxt, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        slopInterceptSizer = wx.BoxSizer(wx.HORIZONTAL)
        #Radio button 1
        self.slopBtn1 = wx.RadioButton(self, style=wx.RB_GROUP)
        self.slopBtn1.Bind(wx.EVT_RADIOBUTTON, self.OnSlopeRadioBtn)


        #Slope
        slopeSizer = wx.BoxSizer(wx.HORIZONTAL)
        slopeTxt = wx.StaticText(self, label=self.slopeLbl1, size=(50, self.summaryHeight))
        self.slopeCtrl = wx.TextCtrl(self, size=(50, self.summaryHeight))

        slopeSizer.Add(slopeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        slopeSizer.Add(self.slopeCtrl, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Intercept
        interceptSizer = wx.BoxSizer(wx.HORIZONTAL)
        interceptTxt = wx.StaticText(self, label=self.interceptLbl1, size=(70, self.summaryHeight))
        self.interceptCtrl = wx.TextCtrl(self, size=(50, self.summaryHeight))

        interceptSizer.Add(interceptTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        interceptSizer.Add(self.interceptCtrl, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        slopInterceptSizer.Add(self.slopBtn1, 0)
        slopInterceptSizer.Add(slopeSizer, 1)
        slopInterceptSizer.Add(interceptSizer, 1)

        #second slop and intercept pair
        slopInterceptSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        #Radio button 2
        self.slopBtn2 = wx.RadioButton(self)
        self.slopBtn2.Bind(wx.EVT_RADIOBUTTON, self.OnSlopeRadioBtn)


        #Slop
        slopeSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        slopeTxt2 = wx.StaticText(self, label=self.slopeLbl2, size=(50, self.summaryHeight))
        self.slopeCtrl2 = wx.TextCtrl(self, size=(50, self.summaryHeight))
        self.slopeCtrl2.Enable(False)

        slopeSizer2.Add(slopeTxt2, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        slopeSizer2.Add(self.slopeCtrl2, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Intercept
        interceptSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        interceptTxt2 = wx.StaticText(self, label=self.interceptLbl2, size=(70, self.summaryHeight))
        self.interceptCtrl2 = wx.TextCtrl(self, size=(50, self.summaryHeight))
        self.interceptCtrl2.Enable(False)

        interceptSizer2.Add(interceptTxt2, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        interceptSizer2.Add(self.interceptCtrl2, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        slopInterceptSizer2.Add(self.slopBtn2, 0)
        slopInterceptSizer2.Add(slopeSizer2, 1)
        slopInterceptSizer2.Add(interceptSizer2, 1)



        # meterEquationSizer.Add(slopeSizer, 1, wx.EXPAND)
        # meterEquationSizer.Add(interceptSizer, 1, wx.EXPAND)

        summaryRightSizer.Add(currentMeterSizer, 0, wx.EXPAND)
        # summaryRightSizer.Add(meterEquationSizer, 1, wx.EXPAND)
        summaryRightSizer.Add(slopInterceptSizer, 0, wx.EXPAND|wx.TOP, 5)
        summaryRightSizer.Add(slopInterceptSizer2, 0, wx.EXPAND|wx.TOP, 5)
        # summaryRightSizer.Add(interceptSizer, 1, wx.EXPAND)





        #Depth table for open water
        self.openWaterPanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(220, -1))
        openWaterSizer = wx.BoxSizer(wx.VERTICAL)
        self.openWaterPanel.SetSizer(openWaterSizer)

        openDepthReadSizer = wx.BoxSizer(wx.HORIZONTAL)
        openDepthReadTxt = wx.StaticText(self.openWaterPanel, label=self.depthLbl, size = (self.openWidth, self.height))
        self.openDepthReadCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.openDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.openDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)


        openDepthReadSizer.Add(openDepthReadTxt, 0, wx.EXPAND)
        openDepthReadSizer.Add(self.openDepthReadCtrl, 0, wx.EXPAND)

        amountWeightSizer = wx.BoxSizer(wx.HORIZONTAL)
        amountWeightTxt = wx.StaticText(self.openWaterPanel, label=self.amountWeightLbl, size = (self.openWidth, self.height))
        self.amountWeightCmbox = wx.ComboBox(self.openWaterPanel, size=(self.ctrlWidth, self.height), choices=self.weights, style=wx.CB_READONLY)

        self.amountWeightCmbox.SetValue("0")
        amountWeightSizer.Add(amountWeightTxt, 0, wx.EXPAND)
        amountWeightSizer.Add(self.amountWeightCmbox, 0, wx.EXPAND)

        weightOffsetSizer = wx.BoxSizer(wx.HORIZONTAL)
        weightOffsetTxt = wx.StaticText(self.openWaterPanel, label=self.weightOffsetLbl, size = (self.openWidth, self.height))
        # print weightOffsetTxt.GetSize()
        self.weightOffsetCtrl = wx.TextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.weightOffsetCtrl.SetValue("0")
        self.weightOffsetCtrl.SetBackgroundColour(self.backgrounColour)
        self.weightOffsetCtrl.SetForegroundColour(self.textColour)
        weightOffsetSizer.Add(weightOffsetTxt, 0, wx.EXPAND)
        weightOffsetSizer.Add(self.weightOffsetCtrl, 0, wx.EXPAND)

        wldlCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        wldlCorrectionTxt = wx.StaticText(self.openWaterPanel, label=self.wldlLbl, size = (self.openWidth, self.height))
        self.wldlCorrectionCmbox = wx.ComboBox(self.openWaterPanel, size = (self.ctrlWidth, self.height), choices=self.corrections, style=wx.CB_READONLY)

        wldlCorrectionSizer.Add(wldlCorrectionTxt, 0, wx.EXPAND)
        wldlCorrectionSizer.Add(self.wldlCorrectionCmbox, 0, wx.EXPAND)

        dryLineSizer = wx.BoxSizer(wx.HORIZONTAL)
        dryLineTxt = wx.StaticText(self.openWaterPanel, label=self.dryLineAngleLbl, size = (self.openWidth, self.height))
        self.dryLineAngleCtrl = wx.TextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.dryLineAngleCtrl.Enable(False)

        # self.dryLineAngleCtrl.SetValue("0")
        dryLineSizer.Add(dryLineTxt, 0, wx.EXPAND)
        dryLineSizer.Add(self.dryLineAngleCtrl, 0, wx.EXPAND)

        distWaterSizer = wx.BoxSizer(wx.HORIZONTAL)
        distWaterTxt = wx.StaticText(self.openWaterPanel, label=self.distSurfaceLbl, size = (self.openWidth, self.height))
        self.distWaterCtrl = wx.TextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.distWaterCtrl.Enable(False)

        distWaterSizer.Add(distWaterTxt, 0, wx.EXPAND)
        distWaterSizer.Add(self.distWaterCtrl, 0, wx.EXPAND)

        dryLineCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        dryLineCorrectionTxt = wx.StaticText(self.openWaterPanel, label=self.dryCorrectionLbl, size = (self.openWidth, self.height))
        self.dryLineCorrectionCtrl = wx.TextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.dryLineCorrectionCtrl.Enable(False)
        self.dryLineCorrectionCtrl.SetBackgroundColour(self.backgrounColour)
        self.dryLineCorrectionCtrl.SetForegroundColour(self.textColour)
        dryLineCorrectionSizer.Add(dryLineCorrectionTxt, 0, wx.EXPAND)
        dryLineCorrectionSizer.Add(self.dryLineCorrectionCtrl, 0, wx.EXPAND)

        wetLineCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        wetLineCorrectionTxt = wx.StaticText(self.openWaterPanel, label=self.wetCorretionLbl, size = (self.openWidth, self.height))
        self.wetLineCorrectionCtrl = wx.TextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.wetLineCorrectionCtrl.Enable(False)
        self.wetLineCorrectionCtrl.SetBackgroundColour(self.backgrounColour)
        self.wetLineCorrectionCtrl.SetForegroundColour(self.textColour)
        wetLineCorrectionSizer.Add(wetLineCorrectionTxt, 0, wx.EXPAND)
        wetLineCorrectionSizer.Add(self.wetLineCorrectionCtrl, 0, wx.EXPAND)

        effectiveDepthSizer = wx.BoxSizer(wx.HORIZONTAL)
        effectiveDepthLbl = wx.StaticText(self.openWaterPanel, label=self.effectiveDepthLbl, size = (self.openWidth, self.height))
        self.OpenEffectiveDepthCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.OpenEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.OpenEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.OpenEffectiveDepthCtrl.SetBackgroundColour(self.backgrounColour)
        self.OpenEffectiveDepthCtrl.SetForegroundColour(self.textColour)
        effectiveDepthSizer.Add(effectiveDepthLbl, 0, wx.EXPAND)
        effectiveDepthSizer.Add(self.OpenEffectiveDepthCtrl, 0, wx.EXPAND)

        openWaterSizer.Add(openDepthReadSizer, 0, wx.EXPAND)
        openWaterSizer.Add(amountWeightSizer, 0, wx.EXPAND)
        openWaterSizer.Add(weightOffsetSizer, 0, wx.EXPAND)
        openWaterSizer.Add(wldlCorrectionSizer, 0, wx.EXPAND)
        openWaterSizer.Add(dryLineSizer, 0, wx.EXPAND)
        openWaterSizer.Add(distWaterSizer, 0, wx.EXPAND)
        openWaterSizer.Add(dryLineCorrectionSizer, 0, wx.EXPAND)
        openWaterSizer.Add(wetLineCorrectionSizer, 0, wx.EXPAND)
        openWaterSizer.Add(effectiveDepthSizer, 0, wx.EXPAND)

        # self.openWaterPanel.Hide()

        #Depth table for Ice
        self.icePanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(340, -1))
        iceSizer = wx.BoxSizer(wx.VERTICAL)
        self.icePanel.SetSizer(iceSizer)

        iceDepthReadSizer = wx.BoxSizer(wx.HORIZONTAL)
        iceDepthReadTxt = wx.StaticText(self.icePanel, label=self.depthLbl, size = (self.lblWidth, self.height))
        self.iceDepthReadCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.iceDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.iceDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        iceDepthReadSizer.Add(iceDepthReadTxt, 0, wx.EXPAND)
        iceDepthReadSizer.Add(self.iceDepthReadCtrl, 0, wx.EXPAND)

        iceAssemblySizer = wx.BoxSizer(wx.HORIZONTAL)
        iceAssemblyTxt = wx.StaticText(self.icePanel, label=self.iceAssemblyLbl, size = (self.lblWidth, self.height))
        self.iceAssemblyCmbbox = wx.ComboBox(self.icePanel, size = (90, self.height), choices=self.iceAssemblySelections, style=wx.CB_READONLY)

        iceAssemblySizer.Add(iceAssemblyTxt, 0, wx.EXPAND)
        iceAssemblySizer.Add(self.iceAssemblyCmbbox, 0, wx.EXPAND)

        meterAboveSizer = wx.BoxSizer(wx.HORIZONTAL)
        meterAboveTxt = wx.StaticText(self.icePanel, label=self.meterAboveLbl, size = (self.lblWidth, self.height))
        self.meterAboveCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.meterAboveCtrl.SetValue("0")

        self.meterAboveCtrl.SetBackgroundColour(self.backgrounColour)
        self.meterAboveCtrl.SetForegroundColour(self.textColour)

        meterAboveSizer.Add(meterAboveTxt, 0, wx.EXPAND)
        meterAboveSizer.Add(self.meterAboveCtrl, 0, wx.EXPAND)

        meterBelowSizer = wx.BoxSizer(wx.HORIZONTAL)
        meterBelowTxt = wx.StaticText(self.icePanel, label=self.meterBelowLbl, size = (self.lblWidth, self.height))
        self.meterBelowCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.meterBelowCtrl.SetValue("0")
        self.meterBelowCtrl.SetBackgroundColour(self.backgrounColour)
        self.meterBelowCtrl.SetForegroundColour(self.textColour)
        meterBelowSizer.Add(meterBelowTxt, 0, wx.EXPAND)
        meterBelowSizer.Add(self.meterBelowCtrl, 0, wx.EXPAND)

        distanceAboveSizer = wx.BoxSizer(wx.HORIZONTAL)
        distanceAboveTxt = wx.StaticText(self.icePanel, label=self.distanceAboveLbl, size = (self.lblWidth, self.height))
        self.distanceAboveCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.distanceAboveCtrl.SetValue("0")
        self.distanceAboveCtrl.SetBackgroundColour(self.backgrounColour)
        self.distanceAboveCtrl.SetForegroundColour(self.textColour)
        distanceAboveSizer.Add(distanceAboveTxt, 0, wx.EXPAND)
        distanceAboveSizer.Add(self.distanceAboveCtrl, 0, wx.EXPAND)

        iceThickRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        iceThickSizer = wx.BoxSizer(wx.HORIZONTAL)
        iceThickTxt = wx.StaticText(self.icePanel, label=self.iceThickLbl, size=(self.lblWidth, self.height))
        iceThickAdjustedSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.iceThickCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

        iceThickAdjustedTxt = wx.StaticText(self.icePanel, label=self.adjustedLbl)
        self.iceThickAdjustedCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.iceThickAdjustedCtrl.SetBackgroundColour(self.backgrounColour)
        self.iceThickAdjustedCtrl.SetForegroundColour(self.textColour)


        iceThickAdjustedSizer.Add(iceThickAdjustedTxt, 0, wx.EXPAND)
        iceThickAdjustedSizer.Add(self.iceThickAdjustedCtrl, 0, wx.EXPAND)

        iceThickSizer.Add(iceThickTxt, 0, wx.EXPAND)
        iceThickSizer.Add(self.iceThickCtrl, 0, wx.EXPAND)

        iceThickRowSizer.Add(iceThickSizer, 1, wx.EXPAND)
        iceThickRowSizer.Add(iceThickAdjustedSizer, 1, wx.EXPAND)


        waterSufaceRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        waterSurfaceIceSizer = wx.BoxSizer(wx.HORIZONTAL)
        waterSurfaceIceTxt = wx.StaticText(self.icePanel, label=self.waterSurfaceIceLbl, size = (self.lblWidth, self.height))
        waterAdjustSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.waterSurfaceIceCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))



        waterIceAdjustTxt = wx.StaticText(self.icePanel, label=self.adjustedLbl, size = (-1, self.height))
        self.waterIceAdjustCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.waterIceAdjustCtrl.SetBackgroundColour(self.backgrounColour)
        self.waterIceAdjustCtrl.SetForegroundColour(self.textColour)


        waterAdjustSizer.Add(waterIceAdjustTxt, 0, wx.EXPAND)
        waterAdjustSizer.Add(self.waterIceAdjustCtrl, 0, wx.EXPAND)



        waterSurfaceIceSizer.Add(waterSurfaceIceTxt, 0, wx.EXPAND)
        waterSurfaceIceSizer.Add(self.waterSurfaceIceCtrl, 0, wx.EXPAND)



        waterSufaceRowSizer.Add(waterSurfaceIceSizer, 1, wx.EXPAND)
        waterSufaceRowSizer.Add(waterAdjustSizer, 1, wx.EXPAND)



        self.slushCkbox = wx.CheckBox(self.icePanel, label=self.slushLbl, style=wx.ALIGN_RIGHT)
        self.slushCkbox.Bind(wx.EVT_CHECKBOX, self.OnSlushCkbox)



        waterSurfaceSlushSizer = wx.BoxSizer(wx.HORIZONTAL)
        waterSurfaceSlushTxt = wx.StaticText(self.icePanel, label=self.waterSurfaceSlushLbl, size = (self.lblWidth, self.height))
        # print waterSurfaceSlushTxt.GetSize()
        self.waterSurfaceSlushCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.waterSurfaceSlushCtrl.Enable(False)

        waterSurfaceSlushSizer.Add(waterSurfaceSlushTxt, 0, wx.EXPAND)
        waterSurfaceSlushSizer.Add(self.waterSurfaceSlushCtrl, 0, wx.EXPAND)

        slushThicknessSizer = wx.BoxSizer(wx.HORIZONTAL)
        slushThicknessTxt = wx.StaticText(self.icePanel, label=self.slushThicknessLbl, size = (self.lblWidth, self.height))
        self.slushThicknessCtrl = wx.TextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.slushThicknessCtrl.SetBackgroundColour(self.backgrounColour)
        self.slushThicknessCtrl.SetForegroundColour(self.textColour)

        slushThicknessSizer.Add(slushThicknessTxt, 0, wx.EXPAND)
        slushThicknessSizer.Add(self.slushThicknessCtrl, 0, wx.EXPAND)

        effectiveDepthSizer = wx.BoxSizer(wx.HORIZONTAL)
        effectiveDepthLbl = wx.StaticText(self.icePanel, label=self.effectiveDepthLbl, size = (self.lblWidth, self.height))
        self.iceEffectiveDepthCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.iceEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.iceEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.iceEffectiveDepthCtrl.SetBackgroundColour(self.backgrounColour)
        self.iceEffectiveDepthCtrl.SetForegroundColour(self.textColour)
        effectiveDepthSizer.Add(effectiveDepthLbl, 0, wx.EXPAND)
        effectiveDepthSizer.Add(self.iceEffectiveDepthCtrl, 0, wx.EXPAND)

        iceSizer.Add(iceDepthReadSizer, 0, wx.EXPAND)
        iceSizer.Add(iceAssemblySizer, 0, wx.EXPAND)
        iceSizer.Add(meterAboveSizer, 0, wx.EXPAND)
        iceSizer.Add(meterBelowSizer, 0, wx.EXPAND)
        iceSizer.Add(distanceAboveSizer, 0, wx.EXPAND)
        iceSizer.Add(iceThickRowSizer, 0, wx.EXPAND)
        iceSizer.Add(waterSufaceRowSizer, 0, wx.EXPAND)
        # iceSizer.Add(waterAdjustSizer, 0, wx.EXPAND)
        iceSizer.Add(self.slushCkbox, 0)
        iceSizer.Add(waterSurfaceSlushSizer, 0, wx.EXPAND)
        iceSizer.Add(slushThicknessSizer, 0, wx.EXPAND)
        iceSizer.Add(effectiveDepthSizer, 0, wx.EXPAND)

        self.icePanel.Hide()
        #################################


        #Velocity Summary
        self.velocityPanel = wx.Panel(self)
        velocitySizer = wx.BoxSizer(wx.VERTICAL)
        self.velocityPanel.SetSizer(velocitySizer)

        velocitySummarySizer = wx.BoxSizer(wx.HORIZONTAL)

        velocityLeftSizer = wx.BoxSizer(wx.VERTICAL)

        velocityMethodSizer = wx.BoxSizer(wx.HORIZONTAL)
        velocityLbl = wx.StaticText(self.velocityPanel, label=self.velocityMethodLbl, size = (-1, self.height))
        self.velocityCombo = wx.ComboBox(self.velocityPanel, style=wx.CB_READONLY, choices=self.velocityMethods, size=(-1, self.height))

        velocityMethodSizer.Add(velocityLbl, 1, wx.EXPAND)
        velocityMethodSizer.Add(self.velocityCombo, 1, wx.EXPAND)

        velocityLeftSizer.Add((-1, -1), 1, wx.EXPAND|wx.TOP, 5)
        velocityLeftSizer.Add((-1, -1), 1, wx.EXPAND|wx.TOP, 5)
        velocityLeftSizer.Add(velocityMethodSizer, 1, wx.EXPAND|wx.TOP, 5)

        velocityRightSizer = wx.BoxSizer(wx.VERTICAL)

        obliqueSizer = wx.BoxSizer(wx.HORIZONTAL)
        obliqueLbl = wx.StaticText(self.velocityPanel, label=self.obliqueLbl, size = (self.lblWidth, self.height))
        self.obliqueCtrl = wx.TextCtrl(self.velocityPanel, size = (self.ctrlWidth, self.height))
        self.obliqueCtrl.SetValue("1")
        obliqueSizer.Add(obliqueLbl, 0, wx.EXPAND)
        obliqueSizer.Add(self.obliqueCtrl, 0, wx.EXPAND)

        velocityCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        velocityCorrectionLbl = wx.StaticText(self.velocityPanel, label=self.velocityCorrLbl, size = (self.lblWidth, self.height))
        # self.velocityCorrectionCtrl = wx.ComboBox(self.velocityPanel, size = (-1, self.height), choices=self.velocityCorrFactors, style=wx.CB_DROPDOWN)
        self.velocityCorrectionCtrl = wx.TextCtrl(self.velocityPanel, size = (self.ctrlWidth, self.height))
        self.velocityCorrectionCtrl.SetBackgroundColour(self.backgrounColour)
        self.velocityCorrectionCtrl.SetForegroundColour(self.textColour)
        velocityCorrectionSizer.Add(velocityCorrectionLbl, 0, wx.EXPAND)
        velocityCorrectionSizer.Add(self.velocityCorrectionCtrl, 0, wx.EXPAND)

        reverseSizer = wx.BoxSizer(wx.HORIZONTAL)
        # reverseLbl = wx.StaticText(self.velocityPanel, label=self.reverseFlowLbl, size = (-1, self.height))
        self.reverseCkbox = wx.CheckBox(self.velocityPanel, label=self.reverseFlowLbl)#, style=wx.ALIGN_RIGHT)

        # reverseSizer.Add(reverseLbl, 1, wx.EXPAND)
        reverseSizer.Add(self.reverseCkbox, 1, wx.EXPAND|wx.ALIGN_LEFT)

        velocityRightSizer.Add(obliqueSizer, 1, wx.EXPAND|wx.TOP, 5)
        velocityRightSizer.Add(velocityCorrectionSizer, 1, wx.EXPAND|wx.TOP, 5)
        velocityRightSizer.Add(reverseSizer, 1, wx.EXPAND|wx.TOP|wx.ALIGN_LEFT, 5)

        velocitySummarySizer.Add(velocityLeftSizer, 1, wx.EXPAND|wx.RIGHT, 30)
        velocitySummarySizer.Add(velocityRightSizer, 1, wx.EXPAND)

        velocitySizer.Add(velocitySummarySizer, 0, wx.EXPAND)


        #Velocity table
        self.velocityGrid = Grid(self.velocityPanel, size=(-1, -1))
        self.velocityGrid.CreateGrid(3, 7)

        self.velocityGrid.SetColLabelValue(0, "%Depth")
        self.velocityGrid.SetColLabelValue(1, "Depth\n of Obs (m)")
        self.velocityGrid.SetColLabelValue(2, "Revs.")
        self.velocityGrid.SetColLabelValue(3, "Time (s)")
        self.velocityGrid.SetColLabelValue(4, "At point\n vel. (m/s)")
        self.velocityGrid.SetColLabelValue(5, "Mean vel.\n(m/s)")
        self.velocityGrid.SetColLabelValue(6, "Corr. mean vel.\n (m/s)")

        self.velocityGrid.SetColSize(0, 50)
        self.velocityGrid.SetColSize(1, 70)
        self.velocityGrid.SetColSize(2, 50)
        self.velocityGrid.SetColSize(3, 50)
        self.velocityGrid.SetColSize(4, 70)
        self.velocityGrid.SetColSize(5, 70)
        self.velocityGrid.SetColSize(6, 85)


        self.velocityGrid.SetCellBackgroundColour(0, 4, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(1, 4, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(2, 4, self.backgrounColour)


        self.velocityGrid.SetCellTextColour(0, 4, self.textColour)
        self.velocityGrid.SetCellTextColour(1, 4, self.textColour)
        self.velocityGrid.SetCellTextColour(2, 4, self.textColour)


        self.velocityGrid.SetCellBackgroundColour(0, 1, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(1, 1, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(2, 1, self.backgrounColour)


        self.velocityGrid.SetCellTextColour(0, 1, self.textColour)
        self.velocityGrid.SetCellTextColour(1, 1, self.textColour)
        self.velocityGrid.SetCellTextColour(2, 1, self.textColour)

        self.velocityGrid.SetCellBackgroundColour(0, 5, self.backgrounColour)
        self.velocityGrid.SetCellTextColour(0, 5, self.textColour)

        self.velocityGrid.SetCellBackgroundColour(0, 6, self.backgrounColour)
        self.velocityGrid.SetCellTextColour(0, 6, self.textColour)


        self.velocityGrid.SetCellSize(0, 5, 3, 1)
        self.velocityGrid.SetCellSize(0, 6, 3, 1)

        self.velocityGrid.SetColFormatFloat(1, precision=3)
        self.velocityGrid.SetColFormatFloat(3, precision=1)
        # Below are now commented out because I manually put 3sigfig each time I set values for those columns
        #self.velocityGrid.SetColFormatFloat(4, precision=7)
        #self.velocityGrid.SetColFormatFloat(5, precision=7)
        # self.velocityGrid.SetColFormatFloat(6, precision=3)

        # self.velocityGrid.GetCellEditor(2, 0).SetControl(wx.Control(self))
        # print self.velocityGrid.GetCellEditor(2, 0).IsCreated()



        self.velocityGrid.SetRowLabelSize(1)
        velocitySizer.Add(self.velocityGrid, 0, wx.EXPAND|wx.TOP, 5)



        #button panel
        buttonPanel = wx.Panel(self, style=wx.BORDER_NONE)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonPanel.SetSizer(buttonSizer)

        self.saveBtn = wx.Button(buttonPanel, label=self.saveBtnLbl, size=(100, 30))
        self.nextBtn = wx.Button(buttonPanel, label=self.nextBtnLbl, size=(50, 30))
        self.cancelBtn = wx.Button(buttonPanel, label=self.cancelBtnLbl, size=(50, 30))

        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.nextBtn.Bind(wx.EVT_BUTTON, self.OnNext)

        buttonSizer.Add(self.cancelBtn, 0, wx.LEFT, 250)
        buttonSizer.Add(self.nextBtn, 0, wx.LEFT, 5)
        buttonSizer.Add(self.saveBtn, 0, wx.LEFT, 5)

        sizerV.Add(self.headerTxt, 0, wx.EXPAND)
        sizerV.Add(summarySizer, 0, wx.EXPAND)
        sizerV.Add(self.openWaterPanel, 0, wx.TOP|wx.LEFT|wx.RIGHT, 15)
        sizerV.Add(self.icePanel, 0, wx.TOP|wx.LEFT|wx.RIGHT, 15)
        sizerV.Add(self.velocityPanel, 0, wx.ALL|wx.EXPAND, 15)
        sizerV.Add(buttonPanel, 0, wx.ALL|wx.EXPAND, 15)


        self.SetSizer(sizerV)
        # self.SetSize(100, 80)


        self.obliqueCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAdjVelocity)
        self.velocityCombo.Bind(wx.EVT_COMBOBOX, self.OnUpdateMeanVel)
        self.slopeCtrl.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)
        self.slopeCtrl2.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)
        self.interceptCtrl.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)
        self.velocityCorrectionCtrl.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)

        self.panelNumberCtrl.Bind(wx.EVT_TEXT, self.OnPanelNumber)
        self.panelConditionCombox.Bind(wx.EVT_COMBOBOX, self.OnUpdateVelocityCorrection)
        self.panelConditionCombox.Bind(wx.EVT_COMBOBOX, self.OnPanelCondition)
        self.slopeCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAllPointVel)
        self.slopeCtrl2.Bind(wx.EVT_TEXT, self.OnUpdateAllPointVel)
        self.interceptCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAllPointVel)
        self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.UpdateWetLineCorrection)
        self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.amountWeightCmbox.Bind(wx.EVT_COMBOBOX, self.OnUpdateMeterOffset)
        self.weightOffsetCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.waterIceAdjustCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.iceEffectiveDepthCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.weightOffsetCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.wldlCorrectionCmbox.Bind(wx.EVT_COMBOBOX, self.OnWLDLCorrection)
        self.wldlCorrectionCmbox.Bind(wx.EVT_COMBOBOX, self.UpdateWetLineCorrection)
        self.dryLineAngleCtrl.Bind(wx.EVT_TEXT, self.UpdateDryLineCorrection)
        self.dryLineAngleCtrl.Bind(wx.EVT_TEXT, self.UpdateWetLineCorrection)
        self.dryLineCorrectionCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.wetLineCorrectionCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.distWaterCtrl.Bind(wx.EVT_TEXT, self.UpdateDryLineCorrection)
        self.iceDepthReadCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.iceAssemblyCmbbox.Bind(wx.EVT_COMBOBOX, self.OnIceAssembly)
        self.meterBelowCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAdjusted)
        self.meterBelowCtrl.Bind(wx.EVT_TEXT, self.OnUpdateIceThickAdjusted)
        self.meterAboveCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.waterSurfaceIceCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAdjusted)
        self.waterSurfaceIceCtrl.Bind(wx.EVT_TEXT, self.UpdateSlushThickness)
        self.waterSurfaceIceCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.slushCkbox.Bind(wx.EVT_CHECKBOX, self.UpdateSlushThickness)
        self.slushCkbox.Bind(wx.EVT_CHECKBOX, self.UpdateIceEffectiveDepth)
        self.waterSurfaceSlushCtrl.Bind(wx.EVT_TEXT, self.UpdateSlushThickness)
        self.slushThicknessCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.velocityCombo.Bind(wx.EVT_COMBOBOX, self.OnUpdateVelocityCorrection)
        self.velocityCombo.Bind(wx.EVT_COMBOBOX, self.OnVelMethod)
        self.reverseCkbox.Bind(wx.EVT_CHECKBOX, self.OnUpdateAllPointVel)
        self.iceThickCtrl.Bind(wx.EVT_TEXT, self.OnUpdateIceThickAdjusted)


        self.velocityGrid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnUpdateAtPointVel)
        self.velocityGrid.Bind(wx.grid.EVT_GRID_TABBING, self.OnRevTimeTab)

        self.wldlCorrectionCmbox.SetValue(self.corrections[0])
        self.iceAssemblyCmbbox.SetValue(self.iceAssemblySelections[5])

    def OnRevTimeTab(self, event):
        totalRows = self.velocityGrid.GetNumberRows()
        col = event.GetCol()
        row = event.GetRow()
        if col==2:
            self.velocityGrid.GoToCell(row,3)
        elif col==3:
            if row!=totalRows-1:
                self.velocityGrid.GoToCell(row+1,2)

    def OnTagmarkTabEnter(self, event):
        if "open" in self.panelConditionCombox.GetValue().lower():
            self.openDepthReadCtrl.SetFocus()
        if "ice" in self.panelConditionCombox.GetValue().lower():
            self.iceDepthReadCtrl.SetFocus()

    def OnUpdateIceThickAdjusted(self, event):
        self.UpdateIceThickAdjusted()
        event.Skip()

    def UpdateIceThickAdjusted(self):
        iceThickness = self.iceThickCtrl.GetValue()
        meterBelowFoot = self.meterBelowCtrl.GetValue()
        if iceThickness!="" and meterBelowFoot!="":
            adjustedIceThickness = float(iceThickness) - float(meterBelowFoot)
            self.iceThickAdjustedCtrl.SetValue(str(adjustedIceThickness))

    def OnUpdateDepthOfObs(self, event):
        for i in range(3):
            self.UpdateDepthOfObs(i)
        event.Skip()

    def UpdateDepthOfObs(self, row):
        # print "UpdateDepthOfObs"
        coef = self.velocityGrid.GetCellValue(row, 0)
        if self.velocityCombo.GetValue() == "Surface" or coef == "":
            val = ""

        elif self.panelConditionCombox.GetValue() == "Open":
            if self.openDepthReadCtrl.GetValue() == "":
                val = ""
            else:
                offset = self.weightOffsetCtrl.GetValue() if self.weightOffsetCtrl.GetValue() != "" else "0"
                val = float(coef) * (float(self.openDepthReadCtrl.GetValue()) + float(offset))
        elif self.panelConditionCombox.GetValue() == "Ice":
            effectiveDepth = self.iceEffectiveDepthCtrl.GetValue()
            #print effectiveDepth
            if effectiveDepth == "":
                    val = ""
            elif self.slushCkbox.IsChecked():
                slush = self.waterSurfaceSlushCtrl.GetValue() if self.waterSurfaceSlushCtrl.GetValue() != '' else "0"
                val = float(effectiveDepth) * float(coef) + float(slush)

            else:
                adjusted = self.waterIceAdjustCtrl.GetValue() if self.waterIceAdjustCtrl.GetValue() != '' else "0"
                val = float(effectiveDepth) * float(coef) + float(adjusted)

        else:
            val = ""
        if val == "":
            self.velocityGrid.SetCellValue(row, 1, val)
        else:
            self.velocityGrid.SetCellValue(row, 1, sigfig.round_sig(val,3))






    def OnUpdateAtPointVel(self, event):
        # print "OnUpdateAtPointVel"
        if event.GetCol() == 2 or event.GetCol() == 3:
            row = event.GetRow()
            self.UpdateAtPointVelByRow(row)

        if event.GetCol() == 0:
            self.OnUpdateDepthOfObs(event)

        self.OnUpdateMeanVel(event)
        event.Skip()



    def UpdateAtPointVelByRow(self, row):
        rev = self.velocityGrid.GetCellValue((row, 2))
        time = self.velocityGrid.GetCellValue((row, 3))
        if self.slopBtn1.GetValue():
            slop = self.slopeCtrl.GetValue()
            intercept = self.interceptCtrl.GetValue()
        else:
            slop = self.slopeCtrl2.GetValue()
            intercept = self.interceptCtrl2.GetValue()
        reverse = self.reverseCkbox.IsChecked()

        if rev != "" and time != "" and slop != '' and intercept != "":
            if rev == "0":
                val = "0"
            elif reverse:
                val = -(float(rev) / float(time) * float(slop) + float(intercept))
            else:
                val = float(rev) / float(time) * float(slop) + float(intercept)

            # apply 3sigfig
            print "row", row
            if isinstance(val, str):
                self.velocityGrid.SetCellValue((row, 4), val)
                self.rawAtPointVel[row] = val
                self.openWaterPanel.Disable()
                self.icePanel.Disable()
            else:
                self.velocityGrid.SetCellValue((row, 4), sigfig.round_sig(val,3))
                self.rawAtPointVel[row] = val
                #self.velocityGrid.SetCellValue((row, 4), str(val))
                self.openWaterPanel.Disable()
                self.icePanel.Disable()
        else:
            self.velocityGrid.SetCellValue((row, 4), "")

    def UpdateAllPointVel(self):
        for i in range(3):
            self.UpdateAtPointVelByRow(i)
        self.UpdateMeanVel()


    def OnUpdateAllPointVel(self, event):
        self.UpdateAllPointVel()
        event.Skip()


    def OnPanelCondition(self, event):
        # print "OnPanelCondition"

        self.PanelConditionUpdate()
        self.OnVelMethod(event)
        self.OnUpdateDepthOfObs(event)
        self.OnIceAssembly(event)
        self.Layout()
        event.Skip()


    def PanelConditionUpdate(self):
        if self.panelConditionCombox.GetValue() == "Ice":
            self.openWaterPanel.Hide()
            self.icePanel.Show()

            self.openDepthReadCtrl.SetValue("")
            self.amountWeightCmbox.SetValue(self.weights[0])
            self.weightOffsetCtrl.SetValue("")
            self.wldlCorrectionCmbox.SetValue(self.corrections[0])
            self.dryLineAngleCtrl.SetValue("")
            self.distWaterCtrl.SetValue("")
            self.dryLineCorrectionCtrl.SetValue("")
            self.wetLineCorrectionCtrl.SetValue("")
            self.OpenEffectiveDepthCtrl.SetValue("")

            self.velocityCombo.SetItems(self.velocityMethods)
            self.velocityCombo.SetValue("0.5")

        else:
            self.icePanel.Hide()
            self.openWaterPanel.Show()

            if self.weightOffsetCtrl.GetValue()=="":
                self.weightOffsetCtrl.SetValue("0")
            self.iceDepthReadCtrl.SetValue("")
            self.iceAssemblyCmbbox.SetValue(self.iceAssemblySelections[5])
            self.meterAboveCtrl.SetValue("")
            self.meterBelowCtrl.SetValue("")
            self.distanceAboveCtrl.SetValue("")
            self.waterSurfaceIceCtrl.SetValue("")
            self.waterIceAdjustCtrl.SetValue("")
            self.slushThicknessCtrl.SetValue("")
            self.slushCkbox.SetValue(False)
            self.waterSurfaceSlushCtrl.SetValue("")

            self.velocityCombo.SetItems(self.velocityMethods[1:])
            self.velocityCombo.SetValue("0.6")

    def OnPanelNumber(self, event):
        val = self.panelNumberCtrl.GetValue()
        self.headerTxt.SetLabel(self.titleLbl + "  " + val)
        self.Layout()
        event.Skip()

    def VelMethod(self):
        self.UpdateGrid()
        for i in range(3):
            self.UpdateDepthOfObs(i)
        self.Layout()

    def OnVelMethod(self, event):
        self.VelMethod()
        event.Skip()

    def UpdateGrid(self):
        if self.velocityCombo.GetValue() == "0.5":
            self.velocityGrid.SetCellValue((0,0), "0.5")
            self.velocityGrid.SetCellValue((1,0), "")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "3.05")
            # self.velocityGrid.SetCellValue((1,1), "")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.HideRow(1)
            self.velocityGrid.HideRow(2)

        elif self.velocityCombo.GetValue() == "0.6":
            self.velocityGrid.SetCellValue((0,0), "0.6")
            self.velocityGrid.SetCellValue((1,0), "")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "3.26")
            # self.velocityGrid.SetCellValue((1,1), "")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.HideRow(1)
            self.velocityGrid.HideRow(2)

        elif self.velocityCombo.GetValue() == "0.2/0.8":
            self.velocityGrid.SetCellValue((0,0), "0.2")
            self.velocityGrid.SetCellValue((1,0), "0.8")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "2.42")
            # self.velocityGrid.SetCellValue((1,1), "3.68")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.ShowRow(1)
            self.velocityGrid.HideRow(2)

        elif self.velocityCombo.GetValue() == "0.2/0.6/0.8":
            self.velocityGrid.SetCellValue((0,0), "0.2")
            self.velocityGrid.SetCellValue((1,0), "0.6")
            self.velocityGrid.SetCellValue((2,0), "0.8")

            # self.velocityGrid.SetCellValue((0,1), "2.42")
            # self.velocityGrid.SetCellValue((1,1), "3.26")
            # self.velocityGrid.SetCellValue((2,1), "3.68")

            self.velocityGrid.ShowRow(1)
            self.velocityGrid.ShowRow(2)

        elif self.velocityCombo.GetValue() == "Surface":
            self.velocityGrid.SetCellValue((0,0), "Surface")
            self.velocityGrid.SetCellValue((1,0), "")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "")
            # self.velocityGrid.SetCellValue((1,1), "")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.HideRow(1)
            self.velocityGrid.HideRow(2)

    def OnIceAssmeblyNoEvent(self):
        iceVal = self.iceAssemblyCmbbox.GetValue()
        if iceVal == self.iceAssemblySelections[0]:
            self.meterAboveCtrl.SetValue("0.1")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0")
        elif iceVal == self.iceAssemblySelections[1]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.25")
        elif iceVal == self.iceAssemblySelections[2]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.26")
        elif iceVal == self.iceAssemblySelections[3]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.32")
        elif iceVal == self.iceAssemblySelections[4]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.36")
        elif iceVal == self.iceAssemblySelections[5]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0")
        self.UpdateIceThickAdjusted()

    def OnIceAssembly(self, event):
        self.OnIceAssmeblyNoEvent()
        event.Skip()


    def UpdateSlushThickness(self, event):
        if self.slushCkbox.IsChecked():
            if self.waterSurfaceIceCtrl.GetValue() != "" and self.waterSurfaceSlushCtrl.GetValue() != "":
                self.slushThicknessCtrl.SetValue(str(float(self.waterSurfaceSlushCtrl.GetValue()) - float(self.waterSurfaceIceCtrl.GetValue())))
            else:
                self.slushThicknessCtrl.SetValue(self.waterSurfaceSlushCtrl.GetValue())

        event.Skip()

    def UpdateIceEffectiveDepth(self, event):
        iceDepth = self.iceDepthReadCtrl.GetValue()
        meterAbove = self.meterAboveCtrl.GetValue()
        meterBelow = self.meterBelowCtrl.GetValue()
        waterIce = self.waterSurfaceIceCtrl.GetValue()
        slushThick = self.slushThicknessCtrl.GetValue()
        if iceDepth != "" and meterAbove != "" and waterIce != "":
            if self.slushCkbox.IsChecked():
                if slushThick != "":
                    self.iceEffectiveDepthCtrl.SetValue(str(round(float(iceDepth) + float(meterAbove) - float(waterIce) + float(meterBelow) - float(slushThick),3)))
                else:
                    self.iceEffectiveDepthCtrl.SetValue(str(round(float(iceDepth) + float(meterAbove) - float(waterIce) + float(meterBelow),3)))
            else:
                self.iceEffectiveDepthCtrl.SetValue(str(round(float(iceDepth) + float(meterAbove) - float(waterIce) + float(meterBelow),3)))
        else:
            self.iceEffectiveDepthCtrl.SetValue("")

        if self.iceEffectiveDepthCtrl.GetValue() != "" and not self.modify:
            if float(self.iceEffectiveDepthCtrl.GetValue()) < 0.75 and "open" in self.panelConditionCombox.GetValue().lower():
                self.velocityCombo.SetValue("0.6")
                self.UpdateMeanVel()
                self.UpdateVelocityCorrection()
                self.VelMethod()
            if float(self.iceEffectiveDepthCtrl.GetValue()) < 0.75 and "ice" in self.panelConditionCombox.GetValue().lower():
                self.velocityCombo.SetValue("0.5")
                self.UpdateMeanVel()
                self.UpdateVelocityCorrection()
                self.VelMethod()
            elif float(self.iceEffectiveDepthCtrl.GetValue()) >= 0.75:
                self.velocityCombo.SetValue("0.2/0.8")
                self.UpdateMeanVel()
                self.UpdateVelocityCorrection()
                self.VelMethod()

        event.Skip()

    def UpdateMeterOffset(self):
        val = self.amountWeightCmbox.GetValue()
        key = self.weights.index(val)
        self.weightOffsetCtrl.SetValue(self.meterOffsets[key])
        self.UpdateOpenEffectiveDepth()

    def OnUpdateMeterOffset(self, event):
        self.UpdateMeterOffset()
        event.Skip()

    def WLDLCorrection(self):
        if self.wldlCorrectionCmbox.GetValue() == "No":
            self.dryLineAngleCtrl.Enable(False)
            self.distWaterCtrl.Enable(False)
            self.dryLineCorrectionCtrl.Enable(False)
            self.wetLineCorrectionCtrl.Enable(False)
        elif self.wldlCorrectionCmbox.GetValue() == "Yes":
            self.dryLineAngleCtrl.Enable(True)
            self.distWaterCtrl.Enable(True)
            self.dryLineCorrectionCtrl.Enable(True)
            self.wetLineCorrectionCtrl.Enable(True)
        else:
            self.dryLineAngleCtrl.Enable(True)
            self.distWaterCtrl.Enable(False)
            self.dryLineCorrectionCtrl.Enable(False)
            self.wetLineCorrectionCtrl.Enable(True)
        self.UpdateDryLineCorrectionNoEvent()

    def OnWLDLCorrection(self, event):
        self.WLDLCorrection()
        event.Skip()

    def UpdateOpenEffectiveDepth(self):
        depthRead = self.openDepthReadCtrl.GetValue()
        offset = self.weightOffsetCtrl.GetValue()
        dryLine = self.dryLineCorrectionCtrl.GetValue()
        wetLine = self.wetLineCorrectionCtrl.GetValue()


        if depthRead != "":
            offset = float(offset) if offset != "" else 0
            dryLine = float(dryLine) if dryLine != ""  and self.dryLineCorrectionCtrl.IsEnabled() else 0
            wetLine = float(wetLine) if wetLine != "" and self.wetLineCorrectionCtrl.IsEnabled() else 0
            effectiveDepth = str(round(float(depthRead) + offset - dryLine - wetLine,3))
            # print  depthRead
            # print  offset
            # print dryLine
            # print wetLine
        else:
            effectiveDepth = ""
        if effectiveDepth != "" and not self.modify:
            if offset < 0.2:
                if float(effectiveDepth) < 0.75:
                    self.velocityCombo.SetValue("0.6")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()
                elif float(effectiveDepth) >= 0.75:
                    self.velocityCombo.SetValue("0.2/0.8")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()
            else:
                cutOffDepth = offset/0.2
                print cutOffDepth
                if float(effectiveDepth) < cutOffDepth:
                    self.velocityCombo.SetValue("0.6")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()
                elif float(effectiveDepth) >= cutOffDepth:
                    self.velocityCombo.SetValue("0.2/0.8")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()


        self.OpenEffectiveDepthCtrl.SetValue(effectiveDepth)

    def OnUpdateOpenEffectiveDepth(self, event):
        self.UpdateOpenEffectiveDepth()
        event.Skip()

    def UpdateDryLineCorrectionNoEvent(self):
        dryLine = self.dryLineAngleCtrl.GetValue()
        distWater = self.distWaterCtrl.GetValue()
        if self.wldlCorrectionCmbox.GetValue() == "Yes" and dryLine != "" and distWater != "":
            dryCorrection = str(((1 / math.cos(math.radians(float(dryLine)))) - 1) * float(distWater))
        else:

            dryCorrection = ""
            # self.dryLineAngleCtrl.ChangeValue("")
            # self.distWaterCtrl.ChangeValue("")
            # self.wetLineCorrectionCtrl.ChangeValue("")
        self.dryLineCorrectionCtrl.SetValue(dryCorrection)

    def UpdateDryLineCorrection(self, event):
        self.UpdateDryLineCorrectionNoEvent()
        event.Skip()

    def UpdateWetLineCorrectionNoEvent(self):
        angle = self.dryLineAngleCtrl.GetValue()
        depthRead = self.openDepthReadCtrl.GetValue()
        if self.wldlCorrectionCmbox.GetValue() == "Yes" or self.wldlCorrectionCmbox.GetValue() == "Yes_w_Tags":
            if angle != "" and depthRead != "":
                angle = float(angle)
                depthRead = float(depthRead)
                wetLineCorrection = depthRead - (depthRead * ((0.000313*angle) + (0.000075*angle*angle) + (0.998015*(math.cos(math.radians(angle))))))
                # print 0.000313*angle
                # print 0.000075*angle*angle
                # print math.cos(math.radians(angle))
                # print 0.998015*(math.cos(math.radians(angle)))
            else:
                wetLineCorrection = ""

        else:
            wetLineCorrection = 0
            # self.dryLineAngleCtrl.ChangeValue("")
            # self.distWaterCtrl.ChangeValue("")
            # self.wetLineCorrectionCtrl.ChangeValue("")

        self.wetLineCorrectionCtrl.SetValue(str(wetLineCorrection))

    def UpdateWetLineCorrection(self, event):
        self.UpdateWetLineCorrectionNoEvent()
        event.Skip()

    def OnUpdateAdjusted(self, event):
        waterBottom = self.waterSurfaceIceCtrl.GetValue()
        meterBelow = self.meterBelowCtrl.GetValue()
        if waterBottom == "":
            self.waterIceAdjustCtrl.SetValue("")
        else:
            if meterBelow == "":
                self.waterIceAdjustCtrl.SetValue(waterBottom)
            else:
                self.waterIceAdjustCtrl.SetValue(str(float(waterBottom) - float(meterBelow)))
        event.Skip()

    def OnUpdateVelocityCorrection(self, event):
        self.UpdateVelocityCorrection()
        event.Skip()

    def UpdateVelocityCorrection(self):
        panelCondition = self.panelConditionCombox.GetValue()
        velocityMethod = self.velocityCombo.GetValue()

        if panelCondition == "Ice" and velocityMethod == self.velocityMethods[0]:
            vcf = "0.88"
            self.velocityCorrectionCtrl.Enable(True)
        elif panelCondition == "Ice" and velocityMethod == self.velocityMethods[1]:
            vcf = "0.92"
            self.velocityCorrectionCtrl.Enable(True)
        elif velocityMethod == self.velocityMethods[4]:
            vcf = "0.85"
            self.velocityCorrectionCtrl.Enable(True)
        else:
            vcf = "1.0"
            self.velocityCorrectionCtrl.Enable(False)
        self.velocityCorrectionCtrl.SetValue(vcf)

    def UpdateMeanVel(self):
        # print "OnUpdateMeanVel"
        try:
            #self.velocityMethods = ["0.5", "0.6", "0.2/0.8", "0.2/0.6/0.8", "Surface"]
            if self.velocityCombo.GetValue() == self.velocityMethods[0] \
                or self.velocityCombo.GetValue() == self.velocityMethods[1]\
                or self.velocityCombo.GetValue() == self.velocityMethods[4]:
                meanVal = self.rawAtPointVel[0] * float(self.velocityCorrectionCtrl.GetValue())
            elif self.velocityCombo.GetValue() == self.velocityMethods[2]:
                meanVal = (self.rawAtPointVel[0] + self.rawAtPointVel[1]) / 2 * float(self.velocityCorrectionCtrl.GetValue())
            else:
                meanVal = ((self.rawAtPointVel[0] + self.rawAtPointVel[1] * 2 + self.rawAtPointVel[2])) / 4 * float(self.velocityCorrectionCtrl.GetValue())
            self.rawMeanVal = meanVal
            print self.rawMeanVal
            print self.rawAtPointVel
            ## apply 3 sigfigs
            self.velocityGrid.SetCellValue(0, 5, sigfig.round_sig(meanVal,3))
            #self.velocityGrid.SetCellValue(0, 5, str(meanVal))
        except:
            self.velocityGrid.SetCellValue(0, 5, "")
        # if self.velocityCombo.GetValue() == self.velocityMethods[0] \
        #     or self.velocityCombo.GetValue() == self.velocityMethods[1]\
        #     or self.velocityCombo.GetValue() == self.velocityMethods[4]:
        #     meanVal = float(self.velocityGrid.GetCellValue(0, 4)) * float(self.velocityCorrectionCtrl.GetValue())
        # elif self.velocityCombo.GetValue() == self.velocityMethods[2]:
        #     meanVal = float(self.velocityGrid.GetCellValue(0, 4)) + float(self.velocityGrid.GetCellValue(1, 4)) / 2 * float(self.velocityCorrectionCtrl.GetValue())
        # else:
        #     meanVal = (float(self.velocityGrid.GetCellValue(0, 4)) + float(self.velocityGrid.GetCellValue(1, 4)) * 2 + float(self.velocityGrid.GetCellValue(2, 4))) / 4 * float(self.velocityCorrectionCtrl.GetValue())

        # self.velocityGrid.SetCellValue(0, 5, str(meanVal))
        self.UpdateAdjVelocity()

    def UpdateAdjVelocity(self):
        # print "OnUpdateAdjVelocity"
        try:
            #meanVal = self.velocityGrid.GetCellValue(0, 5)
            obliqueCorrection = self.obliqueCtrl.GetValue()
            if self.rawMeanVal!="" and obliqueCorrection:
                try:
                    self.velocityGrid.SetCellValue(0, 6, sigfig.round_sig(float(self.rawMeanVal) * float(obliqueCorrection),3))
                except:
                    self.velocityGrid.SetCellValue(0, 6, "")
                #self.velocityGrid.SetCellValue(0, 6, str(float(meanVal) * float(obliqueCorrection)))
            else:
                self.velocityGrid.SetCellValue(0, 6, "")
        except Exception as e:
            print e
            self.velocityGrid.SetCellValue(0, 6, "")

    def OnUpdateMeanVel(self, event):
        self.UpdateMeanVel()
        event.Skip()

    def OnUpdateAdjVelocity(self, event):
        self.UpdateAdjVelocity()
        event.Skip()

    def OnSlushCkbox(self, event):
        if self.slushCkbox.IsChecked():
            self.waterSurfaceSlushCtrl.Enable(True)
        else:
            self.waterSurfaceSlushCtrl.SetValue("")
            self.waterSurfaceSlushCtrl.Enable(False)
        event.Skip()

    def OnSave(self, event):
        print "OnSave_Panel"

        # summaryTable = self.GetParent().GetParent().GetParent().summaryTable
        self.SaveToObj()
        event.Skip()


    def OnNext(self, event):
        failed = self.SaveToObj()
        if not failed==-1:
            self.GetParent().GetParent().GetParent().Adding()

    def SaveToObj(self):
        table = self.GetParent().GetParent().GetParent()

        num = self.panelNumberCtrl.GetValue()
        dist = self.panelTagMarkCtrl.GetValue()
        velocityMethod = self.velocityCombo.GetValue()

        if dist=="":
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[Panel Tagmark (m)]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1

        #if self.OpenEffectiveDepthCtrl.GetValue()=="" and self.iceEffectiveDepthCtrl.GetValue()=="":
        #    dlg = wx.MessageDialog(None, "You need to enter in the values for [Effective Depth] to be calculated", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
        #    dlg.ShowModal()
        #    return -1

        #if self.velocityGrid.GetCellValue(0,6)=="":
        #    dlg = wx.MessageDialog(None, "You need to enter in the values for [Corr. mean vel] to be calculated", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
        #    dlg.ShowModal()
        #    return -1

        #if len(table.panelObjs) > 0 and table.panelObjs[0].panelType==0:
        #    if float(dist) < float(table.panelObjs[0].distance):
        #        dlg = wx.MessageDialog(None, "Panel tagmark value must be GREATER than Start Edge", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
        #        dlg.ShowModal()
        #        return -1

        #if len(table.panelObjs) > 1 and table.panelObjs[-1].panelType==0:
        #    if float(dist) > float(table.panelObjs[-1].distance):
        #        dlg = wx.MessageDialog(None, "Panel tagmark value must be LESS than End Edge", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
        #        dlg.ShowModal()
        #        return -1

        if len(table.panelObjs) > 0:
            for i in range(len(table.panelObjs)):
                if float(table.panelObjs[i].distance) == float(dist):
                    if self.panelId == -1:
                        dlg = wx.MessageDialog(None, "Panel tagmark value already exists", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                        dlg.ShowModal()
                        return -1
                    else:
                        if float(dist) != float(table.originalTagmark):
                            dlg = wx.MessageDialog(None, "Panel tagmark value already exists", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                            dlg.ShowModal()
                            return -1
                try:
                    if isinstance(table.panelObjs[i].panelNum, str) and isinstance(table.panelObjs[i+1].panelNum, str):
                        if "start p" in table.panelObjs[i].panelNum.lower() and "end p" in table.panelObjs[i+1].panelNum.lower():
                            if float(table.panelObjs[i].distance) < float(dist) < float(table.panelObjs[i+1].distance) or float(table.panelObjs[i].distance) > float(dist) > float(table.panelObjs[i+1].distance):
                                dlg = wx.MessageDialog(None, "Panel tagmark value is within the range of P/ISL", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return -1
                except:
                    pass




        myDepths = []
        myObs = []
        myRevs = []
        myRevTimes = []
        myPointVels = []
        if self.velocityCombo.GetValue() == self.velocityMethods[0] or \
                self.velocityCombo.GetValue() == self.velocityMethods[1] or \
                self.velocityCombo.GetValue() == self.velocityMethods[4]:

            myDepths.append(self.velocityGrid.GetCellValue(0, 0))
            myObs.append(self.velocityGrid.GetCellValue(0, 1))
            myRevs.append(self.velocityGrid.GetCellValue(0, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(0, 3))
            if self.velocityGrid.GetCellValue(0, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(0, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(0, 4)),3))

        elif self.velocityCombo.GetValue() == self.velocityMethods[2]:

            myDepths.append(self.velocityGrid.GetCellValue(0, 0))
            myObs.append(self.velocityGrid.GetCellValue(0, 1))
            myRevs.append(self.velocityGrid.GetCellValue(0, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(0, 3))
            if self.velocityGrid.GetCellValue(0, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(0, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(0, 4)),3))

            myDepths.append(self.velocityGrid.GetCellValue(1, 0))
            myObs.append(self.velocityGrid.GetCellValue(1, 1))
            myRevs.append(self.velocityGrid.GetCellValue(1, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(1, 3))
            if self.velocityGrid.GetCellValue(1, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(1, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(1, 4)),3))

        elif self.velocityCombo.GetValue() == self.velocityMethods[3]:

            myDepths.append(self.velocityGrid.GetCellValue(0, 0))
            myObs.append(self.velocityGrid.GetCellValue(0, 1))
            myRevs.append(self.velocityGrid.GetCellValue(0, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(0, 3))
            if self.velocityGrid.GetCellValue(0, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(0, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(0, 4)),3))

            myDepths.append(self.velocityGrid.GetCellValue(1, 0))
            myObs.append(self.velocityGrid.GetCellValue(1, 1))
            myRevs.append(self.velocityGrid.GetCellValue(1, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(1, 3))
            if self.velocityGrid.GetCellValue(1, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(1, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(1, 4)),3))

            myDepths.append(self.velocityGrid.GetCellValue(2, 0))
            myObs.append(self.velocityGrid.GetCellValue(2, 1))
            myRevs.append(self.velocityGrid.GetCellValue(2, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(2, 3))
            if self.velocityGrid.GetCellValue(2, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(2, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(2, 4)),3))

        if self.velocityGrid.GetCellValue(0, 5)=="":
            meanVelocity = ""
        else:
            meanVelocity = sigfig.round_sig(float(self.velocityGrid.GetCellValue(0, 5)),3)
        if self.panelConditionCombox.GetValue() == "Open":
            # depth = self.openDepthReadCtrl.GetValue()
            # effetiveDepth = self.OpenEffectiveDepthCtrl.GetValue()
            obj = PanelObj(panelNum=num, distance=dist, depth=self.openDepthReadCtrl.GetValue(), \
                depths=myDepths, depthObs=myObs, revs=myRevs, revTimes=myRevTimes, pointVels=myPointVels,\
                meanVelocity=meanVelocity, corrMeanVelocity=self.velocityGrid.GetCellValue(0, 6),\
                velocityMethod=self.velocityCombo.GetValue(), panelCondition=self.panelConditionCombox.GetValue(),\
                currentMeter=self.currentMeterCtrl.GetValue(), time=self.measurementTimeCtrl.GetValue(),\
                slop=self.slopeCtrl.GetValue(), intercept=self.interceptCtrl.GetValue(), slop2=self.slopeCtrl2.GetValue(),\
                intercept2=self.interceptCtrl2.GetValue(), slopBtn1=self.slopBtn1.GetValue(),\
                openDepthRead=self.openDepthReadCtrl.GetValue(), weight=self.amountWeightCmbox.GetValue(), \
                offset=self.weightOffsetCtrl.GetValue(), wldl=self.wldlCorrectionCmbox.GetValue(), \
                dryAngle=self.dryLineAngleCtrl.GetValue(), distWaterSurface=self.distWaterCtrl.GetValue(), \
                dryCorrection=self.dryLineCorrectionCtrl.GetValue(), wetCorrection=self.wetLineCorrectionCtrl.GetValue(), \
                openEffectiveDepth=self.OpenEffectiveDepthCtrl.GetValue(),\
                obliqueCorrection=self.obliqueCtrl.GetValue(), velocityCorrFactor=self.velocityCorrectionCtrl.GetValue(), \
                reverseFlow=self.reverseCkbox.GetValue(), panelId=self.panelId, index=self.index)


        else:
            depth = self.iceDepthReadCtrl.GetValue()
            effetiveDepth = self.iceEffectiveDepthCtrl.GetValue()
            bottomIce = self.waterSurfaceIceCtrl.GetValue()

            obj = PanelObj(panelNum=num, distance=dist, depth=depth, \
            depths=myDepths, depthObs=myObs, revs=myRevs, revTimes=myRevTimes, pointVels=myPointVels,\
            meanVelocity=meanVelocity, corrMeanVelocity=self.velocityGrid.GetCellValue(0, 6),\
            velocityMethod=self.velocityCombo.GetValue(),\
            panelCondition=self.panelConditionCombox.GetValue(),\
            currentMeter=self.currentMeterCtrl.GetValue(), time=self.measurementTimeCtrl.GetValue(),\
            slop=self.slopeCtrl.GetValue(), intercept=self.interceptCtrl.GetValue(), slop2=self.slopeCtrl2.GetValue(),\
            intercept2=self.interceptCtrl2.GetValue(), slopBtn1=self.slopBtn1.GetValue(),\
            iceDepthRead=self.iceDepthReadCtrl.GetValue(), iceAssembly=self.iceAssemblyCmbbox.GetValue(), \
            aboveFoot=self.meterAboveCtrl.GetValue(), belowFoot=self.meterBelowCtrl.GetValue(), \
            distAboveWeight=self.distanceAboveCtrl.GetValue(), wsBottomIce=self.waterSurfaceIceCtrl.GetValue(), \
            adjusted=self.waterIceAdjustCtrl.GetValue(), slush=self.slushCkbox.GetValue(), \
            wsBottomSlush=self.waterSurfaceSlushCtrl.GetValue(), thickness=self.slushThicknessCtrl.GetValue(), \
            iceEffectiveDepth=self.iceEffectiveDepthCtrl.GetValue(),\
            obliqueCorrection=self.obliqueCtrl.GetValue(), velocityCorrFactor=self.velocityCorrectionCtrl.GetValue(), \
            reverseFlow=self.reverseCkbox.GetValue(), panelId=self.panelId, index=self.index, \
            iceThickness = self.iceThickCtrl.GetValue(), iceThicknessAdjusted = self.iceThickAdjustedCtrl.GetValue())




        if obj.panelId == -1:
            print "**AddRow**"
            table.AddRow(obj, self.GetScreenPosition())
            table.nextPanelNum += 1
        else:
            print "**UpdateRow**"
            table.UpdateRow(obj, self.GetScreenPosition())
        self.GetParent().GetParent().Close()

    def OnCancel(self, event):
        self.GetParent().GetParent().Close()

        event.Skip()

    def OnSlopeRadioBtn(self, event):
        self.SlopeRadioUpdate()
        event.Skip()

    def SlopeRadioUpdate(self):
        if self.slopBtn1.GetValue():
            self.slopeCtrl.Enable(True)
            self.interceptCtrl.Enable(True)
            self.slopeCtrl2.Enable(False)
            self.interceptCtrl2.Enable(False)

        else:
            self.slopeCtrl.Enable(False)
            self.interceptCtrl.Enable(False)
            self.slopeCtrl2.Enable(True)
            self.interceptCtrl2.Enable(True)

        self.UpdateMeanVel()
        self.UpdateAllPointVel()

        #event.Skip()

    def OnCurrMeterCtrl(self, event):
        index = event.GetSelection()
        header = self.GetParent().GetParent().GetParent().GetParent().header
        if index==0:
            if header.meter1MeterNoCtrl.GetValue()!="":
                self.slopeCtrl.SetValue(header.meter1SlopeCtrl1.GetValue())
                self.interceptCtrl.SetValue(header.meter1InterceptCtrl1.GetValue())
                self.slopeCtrl2.SetValue(header.meter1SlopeCtrl2.GetValue())
                self.interceptCtrl2.SetValue(header.meter1InterceptCtrl2.GetValue())
            else:
                self.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
                self.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
                self.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
                self.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())
        if index==1:
            self.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
            self.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
            self.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
            self.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(540, 660))
    MidSectionPanelPanel(panelNum=1, parent=frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
