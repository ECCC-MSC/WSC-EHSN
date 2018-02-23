import wx
import wx.lib.masked as masked
import wx.lib.newevent as newevent
import math
import datetime
import re
from decimal import *
import NumberControl
from DropdownTime import *

#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""


#Overwrite the ComboBox Class in order to control the float input
class MyComboBox(wx.ComboBox):
    def __init__(self, *args, **kwargs):
        super(MyComboBox, self).__init__(*args, **kwargs)
        self.preValue = ""

LRToggleEvent, EVT_LR_TOGGLE_EVENT = newevent.NewEvent()

class StartBankPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(StartBankPanel, self).__init__(*args, **kwargs)
        
        self.lButtonLbl = "L"
        self.rButtonLbl = "R"
        
        
        self.InitUI()


    def InitUI(self):
        layoutSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.lButton = wx.ToggleButton(self, label=self.lButtonLbl, style=wx.BORDER_NONE, name="LEFT", size=(10, 20))
        self.rButton = wx.ToggleButton(self, label=self.rButtonLbl, style=wx.BORDER_NONE, name="RIGHT", size=(10, 20))

        self.lButton.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleButton)
        self.rButton.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleButton)

        layoutSizer.Add(self.lButton, 1, wx.EXPAND)
        layoutSizer.Add(self.rButton, 1, wx.EXPAND)
        

        self.SetSizer(layoutSizer)
        

    def ToggleButton(self, e):
        obj = e.GetEventObject()
        
        button = self.lButton
        otherButton = self.rButton
        if obj.GetName() == "RIGHT":
            button = self.rButton
            otherButton = self.lButton
        
        if button.GetValue():
            if otherButton.GetValue():
                button.SetValue(True)
                otherButton.SetValue(False)
            

    def GetValue(self):
        if self.lButton.GetValue():
            return "L"
        elif self.rButton.GetValue():
            return "R"
        else:
            return None
        
    def SetValue(self, val):
        if val == "L":
            lButEvent = LRToggleEvent()
            lButEvent.SetEventObject(self.lButton)
            self.lButton.SetValue(True)
            self.ToggleButton(lButEvent)
        elif val == "R":
            rButEvent = LRToggleEvent()
            rButEvent.SetEventObject(self.rButton)
            self.rButton.SetValue(True)
            self.ToggleButton(rButEvent)
        else:
            self.rButton.SetValue(False)
            self.lButton.SetValue(False)
            

class MovingBoatMeasurementsPanel(wx.Panel):
    def __init__(self, mode, lang, *args, **kwargs):
        super(MovingBoatMeasurementsPanel, self).__init__(*args, **kwargs)

        self.bedMatLbl = "Bed Material:"
        self.mbTestDoneLbl = "MB Test Done"
        self.mbTestList = ['', 'Loop', 'Stationary']
        self.detectedLbl = "% Detected"
        self.trackRefSelLbl = "Track Ref Selected*:"
        self.trackRefList = ['', "BT", "GGA", "VTG", "Other"]
        self.leftBankLbl = "Left Bank*:"
        self.bankList = ['', "Sloping (0.3535)", "Vertical (0.91)", "Other"]
        self.otherList = [""]
        self.rightBankLbl = "Right Bank*:"
        self.edgeDistMmntLbl = "Edge Dist Mmnt Method:"
        self.lockLbl = 'Lock'
        # self.coeffLbl = 'Coeff:'
        self.edgeDistMmntMethod = ['Rangefinder', 'Tagline', 'Level Rod', 'Projection', 'Buoy', 'Cablemarks', 'Other']
        self.bedMaterialList = ['Mud', 'Silt', 'Sand', 'Gravel', 'Cobble', 'Boulders', 'Riprap', 'Smooth Rock', 'Fractured Rock', 'Vegetation']
        self.transectLbl = "Transect\nID"
        self.startBankLbl = "Start\nBank*"
        self.startTimeLbl = "Start\nTime*"
        self.startDistLbl = "Start\nDistance (m)*"
        self.endDistLbl = "End\nDistance (m)*"
        self.rawDischLbl = u"Raw Discharge\n(m\N{SUPERSCRIPT THREE}/s)"
        self.finalDisLbl = u"Final Discharge\n(m\N{SUPERSCRIPT THREE}/s)"
        self.remarksLbl = "Remarks"
        self.commentsLbl = "Comments"
        self.mmntStartTimeLbl = "Mmnt Start Time:"
        self.mmntEndTimeLbl = "Mmnt End Time*:"
        self.mmntMeanTimeLbl = "Mmnt Mean Time:"
        self.rawDischMeanLbl = u"Raw Discharge\nMean (m\N{SUPERSCRIPT THREE}/s):"
        self.mbCorrAppLbl = u"MB Correction\nApplied (m\N{SUPERSCRIPT THREE}/s):"
        self.finalDischLbl = u"Final Discharge\nMean (m\N{SUPERSCRIPT THREE}/s):"
        self.corrMeanGHLbl = "Corrected Mean\nGauge Height (m):"
        self.baseCurveGHLbl = "Base Curve\nGauge Height (m):"
        self.baseCurveDischLbl = u"Base Curve\nDischarge (m\N{SUPERSCRIPT THREE}/s):"
        self.standDevMeanDischLbl = "Standard Dev/Mean\n Discharge (%):"
        self.calcShiftBaseCurveLbl = "Calculate Shift from\nBase Curve (m):"
        self.dischDiffBaseCurveLbl = "Discharge Difference\nBase Curve (%):"

        self.velocityMethodLbl = "Velocity Extrapolation Method:"
        self.topLbl = "Top:"
        self.bottomLbl = "Bottom:"
        self.exponentLbl = "Exponent:"
        self.differenceInQLbl = "% Difference in Q from power,\n power, 0.1667.\n(value calculated by extrap):"
        self.compositeTracksLbl = "Composite Tracks: (SonTek Only)"
        self.depthRefLbl = "Depth Ref:"

        self.tops = ["", "Power", "Constant", "3-Point"]
        self.bottoms = ["", "Power", "No Slip"]
        self.compositeTracks = ["", "Off", "On"]
        self.depthRef = ["", "Bottom Track", "Vertical Beam", "Composite (BT)", "Composite (VB)", "Depth Sounder"]
        self.diffToolTip = "% difference in discharge from power, power, 0.1667."


        self.headerHeight = 36
        self.rowHeight = 24
        self.entryNum = 0
 

        self.manager = None
        self.mode = mode
        self.lang = lang

        self.InitUI()
    def do_nothing(self,evt):
          pass
    def InitUI(self):
        if self.mode=="DEBUG":
            print "In MovingBoatMeasurementsPanel"

        self.locale = wx.Locale(self.lang)

        #Separate sheet into 5 rows
        layoutSizer = wx.BoxSizer(wx.VERTICAL)
        
        horizontalSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        #Bed Material
        bedMatPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        bedMatSizer = wx.BoxSizer(wx.HORIZONTAL)
        bedMatTxt = wx.StaticText(bedMatPanel, label=self.bedMatLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        # self.bedMatCtrl = wx.TextCtrl(bedMatPanel, style=wx.TE_PROCESS_ENTER, size=(10, 24))
        self.bedMatCmbo = wx.ComboBox(bedMatPanel, choices=self.bedMaterialList, style=wx.CB_DROPDOWN|wx.ALIGN_CENTRE_HORIZONTAL, size=(80, -1))
        self.bedMatCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        bedMatSizer.Add((5, -1), 0)
        bedMatSizer.Add(bedMatTxt, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        bedMatSizer.Add(self.bedMatCmbo, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        bedMatSizer.Add((5, -1), 0)
        bedMatPanel.SetSizer(bedMatSizer)


        #MB Test
        mbPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mbSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.mbCB = wx.CheckBox(mbPanel, label=self.mbTestDoneLbl, style=wx.ALIGN_RIGHT)
        self.mbCmbo = wx.ComboBox(mbPanel, choices=self.mbTestList, style=wx.CB_READONLY, size=(60, -1))
        self.mbCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        detectedTxt = wx.StaticText(mbPanel, label=self.detectedLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.detectedCtrl = MyTextCtrl(mbPanel, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.detectedCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.detectedCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        
        mbSizer.Add(self.mbCB, 0, wx.EXPAND|wx.ALL, 3)
        mbSizer.Add(self.mbCmbo, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        mbSizer.Add(detectedTxt, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        mbSizer.Add(self.detectedCtrl, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        mbSizer.Add((5, -1), 0)
        mbPanel.SetSizer(mbSizer)

        #Track Ref Selected
        trackRefPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        trackRefSizer = wx.BoxSizer(wx.HORIZONTAL)

        trackRefTxt = wx.StaticText(trackRefPanel, label=self.trackRefSelLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.trackRefCmbo = wx.ComboBox(trackRefPanel, choices=self.trackRefList, style=wx.CB_READONLY, size=(45, -1))
        self.trackRefCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)

        trackRefSizer.Add((5, -1), 0)
        trackRefSizer.Add(trackRefTxt, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        trackRefSizer.Add(self.trackRefCmbo, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        trackRefSizer.Add((5, -1), 0)
        trackRefPanel.SetSizer(trackRefSizer)

        #Composite Tracks
        compositeTrackPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        compositeTrackSizer = wx.BoxSizer(wx.HORIZONTAL)
        compositeTrackPanel.SetSizer(compositeTrackSizer)


        compositeTrackTxt = wx.StaticText(compositeTrackPanel, label=self.compositeTracksLbl, size=(100, 30))
        self.compositeTrackCmbo = wx.ComboBox(compositeTrackPanel, choices=self.compositeTracks, style=wx.CB_READONLY, size=(45, -1))
        self.compositeTrackCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        compositeTrackSizer.Add((5, -1), 0)
        compositeTrackSizer.Add(compositeTrackTxt, 0, wx.EXPAND)
        compositeTrackSizer.Add(self.compositeTrackCmbo, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        compositeTrackSizer.Add((5, -1), 0)



        #Lock
        # lockPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(60, -1))
        # lockSizer = wx.BoxSizer(wx.HORIZONTAL)

        # self.lockCB = wx.CheckBox(lockPanel, label=self.lockLbl)
        # # self.lockCB.Bind(wx.EVT_CHECKBOX, self.OnLock)
        # lockSizer.Add(self.lockCB, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.BOTTOM|wx.LEFT, 5)
        # lockPanel.SetSizer(lockSizer)

        #Add all elements to the first horizontal sizer
        horizontalSizer1.Add(bedMatPanel, 5, wx.EXPAND)
        horizontalSizer1.Add(mbPanel, 6, wx.EXPAND)
        horizontalSizer1.Add(trackRefPanel, 5, wx.EXPAND)
        horizontalSizer1.Add(compositeTrackPanel, 5, wx.EXPAND)
        # horizontalSizer1.Add(lockPanel, 0, wx.EXPAND)





        #Second row (horizontal sizer 2)
        horizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        #left bank
        leftBankPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        leftBankSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftBankTxt = wx.StaticText(leftBankPanel, label=self.leftBankLbl)
        self.leftBankCmbo = wx.ComboBox(leftBankPanel, choices=self.bankList, style=wx.CB_READONLY, size=(65, -1))
        self.leftBankCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.leftBankCmbo.Bind(wx.EVT_COMBOBOX, self.OnLeftBank)
        # self.leftBankOtherCtrl = wx.TextCtrl(leftBankPanel, size=(35, -1))
        self.leftBankOtherCtrl = wx.ComboBox(leftBankPanel, choices=self.otherList, style=wx.CB_DROPDOWN, size=(35, -1))
        # leftCoeffLbl = wx.StaticText(leftBankPanel, label=self.coeffLbl, size=(32, -1))


        leftBankSizer.Add(leftBankTxt, 3, wx.ALL, 5)
        leftBankSizer.Add(self.leftBankCmbo, 4, wx.EXPAND|wx.ALL, 5)
        # leftBankSizer.Add(leftCoeffLbl, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 6)
        leftBankSizer.Add(self.leftBankOtherCtrl, 2, wx.EXPAND|wx.ALL, 6)
        self.leftBankOtherCtrl.Hide()
        leftBankPanel.SetSizer(leftBankSizer)

        #Right bank
        rightBankPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        rightBankSizer = wx.BoxSizer(wx.HORIZONTAL)

        rightBankTxt = wx.StaticText(rightBankPanel, label=self.rightBankLbl)
        self.rightBankCmbo = wx.ComboBox(rightBankPanel, choices=self.bankList, style=wx.CB_READONLY, size=(65, -1))
        self.rightBankCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.rightBankCmbo.Bind(wx.EVT_COMBOBOX, self.OnRightBank)
        # self.rightBankOtherCtrl = wx.TextCtrl(rightBankPanel, size=(35, -1))
        self.rightBankOtherCtrl = wx.ComboBox(rightBankPanel, choices=self.otherList, style=wx.CB_DROPDOWN, size=(35, -1))
        self.rightBankOtherCtrl.Hide()
        # rifhtCoeffLbl = wx.StaticText(rightBankPanel, label=self.coeffLbl, size=(32, -1))

        rightBankSizer.Add(rightBankTxt, 3, wx.ALL, 5)
        rightBankSizer.Add(self.rightBankCmbo, 4, wx.EXPAND|wx.ALL, 5)
        # rightBankSizer.Add(rifhtCoeffLbl, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 6)
        rightBankSizer.Add(self.rightBankOtherCtrl, 2, wx.EXPAND|wx.ALL, 6)
        rightBankPanel.SetSizer(rightBankSizer)

        #Edge dist mmnt method
        edgeDistPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        edgeDistSizer = wx.BoxSizer(wx.HORIZONTAL)

        edgeDistMmntTxt = wx.StaticText(edgeDistPanel, label=self.edgeDistMmntLbl)
        self.edgeDistMmntCmbo = wx.ComboBox(edgeDistPanel, choices=self.edgeDistMmntMethod, style=wx.CB_DROPDOWN)
        self.edgeDistMmntCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)

        edgeDistSizer.Add(edgeDistMmntTxt, 0, wx.ALL, 5)
        edgeDistSizer.Add(self.edgeDistMmntCmbo, 1, wx.EXPAND|wx.ALL, 5)
        edgeDistPanel.SetSizer(edgeDistSizer)

        #Depth Ref
        depthRefPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        depthRefSizer = wx.BoxSizer(wx.HORIZONTAL)
        depthRefPanel.SetSizer(depthRefSizer)

        depthRefTxt = wx.StaticText(depthRefPanel, label=self.depthRefLbl)
        self.depthRefCmbo = wx.ComboBox(depthRefPanel, choices=self.depthRef, style=wx.CB_READONLY)
        self.depthRefCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)

        depthRefSizer.Add(depthRefTxt, 0, wx.ALL, 5)
        depthRefSizer.Add(self.depthRefCmbo, 1, wx.EXPAND|wx.ALL, 5)


        horizontalSizer2.Add(leftBankPanel, 1, wx.EXPAND)
        horizontalSizer2.Add(rightBankPanel, 1, wx.EXPAND)
        horizontalSizer2.Add(edgeDistPanel, 1, wx.EXPAND)
        horizontalSizer2.Add(depthRefPanel, 1, wx.EXPAND)





        #Seventh row (added for "velocity extrapolation method" and "difference in Q")
        horizontalSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        #velocity extrapolation method
        velocityPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        velocitySizerV = wx.BoxSizer(wx.VERTICAL)
        velocityPanel.SetSizer(velocitySizerV)

        velocitySizerH1 = wx.BoxSizer(wx.HORIZONTAL)
        velocitySizerH2 = wx.BoxSizer(wx.HORIZONTAL)

        velocityTxt = wx.StaticText(velocityPanel, label=self.velocityMethodLbl)
        velocityTopTxt = wx.StaticText(velocityPanel, label=self.topLbl)
        velocityBottomTxt = wx.StaticText(velocityPanel, label=self.bottomLbl)
        velocityExponentTxt = wx.StaticText(velocityPanel, label=self.exponentLbl)

        self.velocityTopCombo = wx.ComboBox(velocityPanel, choices=self.tops, style=wx.CB_READONLY)
        self.velocityTopCombo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.velocityBottomCombo = wx.ComboBox(velocityPanel, choices=self.bottoms, style=wx.CB_READONLY)
        self.velocityBottomCombo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.velocityExponentCtrl = MyTextCtrl(velocityPanel)
        self.velocityExponentCtrl.Bind(wx.EVT_TEXT, self.NumberControl)
        self.velocityExponentCtrl.Bind(wx.EVT_KILL_FOCUS, lambda event: self.OnKillFocus(event, 4))


        velocitySizerH1.Add(velocityTxt, 1, wx.TOP|wx.LEFT, 5)

        velocitySizerH2.Add(velocityTopTxt, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        velocitySizerH2.Add(self.velocityTopCombo, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        velocitySizerH2.Add(velocityBottomTxt, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        velocitySizerH2.Add(self.velocityBottomCombo, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        velocitySizerH2.Add(velocityExponentTxt, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        velocitySizerH2.Add(self.velocityExponentCtrl, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

        velocitySizerV.Add(velocitySizerH1, 1, wx.EXPAND)
        velocitySizerV.Add(velocitySizerH2, 1, wx.EXPAND)

        #Difference in Q
        differenceQPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        differenceQSizer = wx.BoxSizer(wx.HORIZONTAL)
        differenceQPanel.SetSizer(differenceQSizer)

        differenceTxt = wx.StaticText(differenceQPanel, label=self.differenceInQLbl)
        self.differenceCtrl = MyTextCtrl(differenceQPanel)
        self.differenceCtrl.Bind(wx.EVT_TEXT, self.NumberControl)
        self.differenceCtrl.Bind(wx.EVT_KILL_FOCUS, lambda event: self.OnKillFocus(event, 2))


        differenceCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        differenceCtrlSizer.Add(self.differenceCtrl, 1, wx.EXPAND|wx.TOP, 20)
        # tooltipBS = wx.ToolTip(self.diffToolTip)
        # tooltipBS.SetDelay(10)
        # tooltipBS.SetAutoPop(30000)
        # differenceTxt.SetToolTip(tooltipBS)

        differenceQSizer.Add(differenceTxt, 0, wx.LEFT|wx.TOP|wx.RIGHT, 5)
        differenceQSizer.Add(differenceCtrlSizer, 1, wx.EXPAND|wx.ALL, 5)



        horizontalSizer7.Add(velocityPanel, 1, wx.EXPAND)
        horizontalSizer7.Add(differenceQPanel, 1, wx.EXPAND)




        #Third row (horizontal sizer 3)
        horizontalSizer3 = wx.BoxSizer(wx.HORIZONTAL)




        #col headers
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)


        #For dynamically added entries
        entryColButtonPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        entryColButtonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonHeaderTxt = wx.StaticText(entryColButtonPanel, size=(30, self.headerHeight))
        entryColButtonPanel.SetSizer(entryColButtonSizer)
        entryColButtonSizer.Add(buttonHeaderTxt, 0, wx.EXPAND)


        #Check Box
        selectPanel = wx.Panel(self, style=wx.RAISED_BORDER)
        selectSizer = wx.BoxSizer(wx.HORIZONTAL)

        selectTxt = wx.StaticText(selectPanel, size=(10, self.headerHeight))
        selectSizer.Add(selectTxt, 0, wx.EXPAND)
        selectPanel.SetSizer(selectSizer)

        #Transect
        transectPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        transectSizer = wx.BoxSizer(wx.HORIZONTAL)

        transectTxt = wx.StaticText(transectPanel, label=self.transectLbl, size=(95, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        transectSizer.Add(transectTxt, 1, wx.EXPAND)
        transectPanel.SetSizer(transectSizer)

        #Start Bank
        startBankPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        startBankSizer = wx.BoxSizer(wx.HORIZONTAL)

        startBankTxt = wx.StaticText(startBankPanel, label=self.startBankLbl, size=(50, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        startBankSizer.Add(startBankTxt, 1, wx.EXPAND)
        startBankPanel.SetSizer(startBankSizer)

        #Start Time
        startTimePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        startTimeSizer = wx.BoxSizer(wx.HORIZONTAL)

        startTimeTxt = wx.StaticText(startTimePanel, label=self.startTimeLbl, size=(65, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        startTimeSizer.Add(startTimeTxt, 1, wx.EXPAND)
        startTimePanel.SetSizer(startTimeSizer)

        #Start Distance
        startDistPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        startDistSizer = wx.BoxSizer(wx.HORIZONTAL)

        startDistTxt = wx.StaticText(startDistPanel, label=self.startDistLbl, size=(76, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        startDistSizer.Add(startDistTxt, 1, wx.EXPAND)
        startDistPanel.SetSizer(startDistSizer)

        #End Distance
        endDistPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        endDistSizer = wx.BoxSizer(wx.HORIZONTAL)

        endDistTxt = wx.StaticText(endDistPanel, label=self.endDistLbl, size=(76, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        endDistSizer.Add(endDistTxt, 1, wx.EXPAND)
        endDistPanel.SetSizer(endDistSizer)

        #Raw Discharge
        rawDischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        rawDischSizer = wx.BoxSizer(wx.HORIZONTAL)

        rawDischTxt = wx.StaticText(rawDischPanel, label=self.rawDischLbl, size=(80, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        rawDischSizer.Add(rawDischTxt, 1, wx.EXPAND)
        rawDischPanel.SetSizer(rawDischSizer)

        # #Final Discharge
        # finalDischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        # finalDischSizer = wx.BoxSizer(wx.HORIZONTAL)

        # finalDischTxt = wx.StaticText(finalDischPanel, label=self.finalDisLbl, size=(80, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        # finalDischSizer.Add(finalDischTxt, 1, wx.EXPAND)
        # finalDischPanel.SetSizer(finalDischSizer)


        #Remarks
        remarksPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        remarksSizer = wx.BoxSizer(wx.HORIZONTAL)

        remarksTxt = wx.StaticText(remarksPanel, label=self.remarksLbl, size=(60, self.headerHeight), style=wx.ALIGN_CENTRE_HORIZONTAL)
        remarksSizer.Add(remarksTxt, 1, wx.EXPAND)
        remarksPanel.SetSizer(remarksSizer)
        
        headerSizer.Add(entryColButtonPanel, 0)
        headerSizer.Add(selectPanel, 0, wx.EXPAND)
        headerSizer.Add(transectPanel, 2, wx.EXPAND)
        headerSizer.Add(startBankPanel, 2, wx.EXPAND)
        headerSizer.Add(startTimePanel, 2, wx.EXPAND)
        headerSizer.Add(startDistPanel, 2, wx.EXPAND)
        headerSizer.Add(endDistPanel, 2, wx.EXPAND)
        headerSizer.Add(rawDischPanel, 2, wx.EXPAND)
        # headerSizer.Add(finalDischPanel, 2, wx.EXPAND)
        headerSizer.Add(remarksPanel, 7, wx.EXPAND)


        self.tableSizerV = wx.BoxSizer(wx.VERTICAL)
        self.tableSizerV.Add(headerSizer, 0, wx.EXPAND)






        

        button = wx.Button(self, name = str(self.entryNum), label="+", size=(30, self.rowHeight))
        button.SetForegroundColour('Red')
        button.Bind(wx.EVT_BUTTON, self.OnAddPress)
        self.entryNum += 1
        rowSizer = wx.BoxSizer(wx.HORIZONTAL)
        rowSizer.Add(button, 0, wx.EXPAND)
        self.tableSizerV.Add(rowSizer, 0, wx.EXPAND)


        # 6 Entries
        # for i in range(9):

        #     self.AddEntry()

            # button = wx.Button(self, name = str(self.entryNum), label="-", size=(30, self.rowHeight))
            # selectCheckbox = wx.CheckBox(self, size=(15, self.rowHeight), name = str(self.entryNum), style=wx.ALIGN_RIGHT)
            # transectCtrl = wx.TextCtrl(self, size=(97, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
            # startBankCtrl = StartBankPanel(self, style=wx.SIMPLE_BORDER, size=(52, self.rowHeight), name = str(self.entryNum))
            # startTimeCtrl = masked.TimeCtrl(self, displaySeconds=True, size=(67, self.rowHeight))
            # startDistanceCtrl = wx.TextCtrl(self, size=(78, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
            # endDistanceCtrl = wx.TextCtrl(self, size=(78, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
            # rawDischCtrl = wx.TextCtrl(self, size=(82, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
            # finalDisCtrl = wx.TextCtrl(self, size=(82, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
            # remarksCtrl = wx.TextCtrl(self, size=(62, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))

            # transectCtrl.SetForegroundColour('Red')
            # startDistanceCtrl.SetForegroundColour('Red')
            # endDistanceCtrl.SetForegroundColour('Red')
            # rawDischCtrl.SetForegroundColour('Red')
            # finalDisCtrl.SetForegroundColour('Red')
            # remarksCtrl.SetForegroundColour('Red')



            # transectCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
            # startDistanceCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
            # endDistanceCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
            # rawDischCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
            # finalDisCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
            # remarksCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)


            # selectCheckbox.Bind(wx.EVT_CHECKBOX, self.OnCheckbox)

            # rowSizer = wx.BoxSizer(wx.HORIZONTAL)
            # rowSizer.Add(button, 0, wx.EXPAND)
            # rowSizer.Add(selectCheckbox, 0, wx.EXPAND)
            # rowSizer.Add(transectCtrl, 0, wx.EXPAND)
            # rowSizer.Add(startBankCtrl, 2, wx.EXPAND)
            # rowSizer.Add(startTimeCtrl, 2, wx.EXPAND)
            # rowSizer.Add(startDistanceCtrl, 2, wx.EXPAND)
            # rowSizer.Add(endDistanceCtrl, 2, wx.EXPAND)
            # rowSizer.Add(rawDischCtrl, 2, wx.EXPAND)
            # rowSizer.Add(finalDisCtrl, 2, wx.EXPAND)
            # rowSizer.Add(remarksCtrl, 7, wx.EXPAND)
            # rowSizer.Layout()

            # self.tableSizerV.Add(rowSizer, 0)
            # self.entryNum += 1
        

        horizontalSizer3.Add(self.tableSizerV, 1, wx.EXPAND)

        



        #Bottom grid (H Sizer 4)
        horizontalSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        #Mmnt Start Time Label
        mmntStartTimePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mmntStartTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        mmntStartTimeTxt = wx.StaticText(mmntStartTimePanel, label=self.mmntStartTimeLbl, style=wx.ALIGN_RIGHT, size=(100, -1))
        mmntStartTimeSizer.Add(mmntStartTimeTxt, 1, wx.EXPAND)
        mmntStartTimePanel.SetSizer(mmntStartTimeSizer)

        #Mmnt Start Time Val
        # self.mmntStartTimeCtrl = masked.TimeCtrl(self, displaySeconds=True, size=(40, -1), fmt24hr = True)
        # self.mmntStartTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        # self.mmntStartTimeCtrl.Bind(wx.EVT_TEXT, self.OnEndTime)
        self.mmntStartTimeCtrl = DropdownTime(True, self, size=(-1, -1))
        self.mmntStartTimeCtrl.GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.OnEndTime)
        self.mmntStartTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.OnEndTime)
        self.mmntStartTimeCtrl.GetSecondCtrl().Bind(wx.EVT_COMBOBOX, self.OnEndTime)
        self.mmntStartTimeCtrl.GetHourCtrl().Bind(wx.EVT_KEY_DOWN, self.OnEndTime)
        self.mmntStartTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_KEY_DOWN, self.OnEndTime)
        self.mmntStartTimeCtrl.GetSecondCtrl().Bind(wx.EVT_KEY_DOWN, self.OnEndTime)

        #Mmnt Raw Discharge Mean
        rawDischMeanPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        rawDischMeanSizer = wx.BoxSizer(wx.HORIZONTAL)
        rawDischMeanTxt = wx.StaticText(rawDischMeanPanel, label=self.rawDischMeanLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        # rawDischMeanBtn = wx.Button(rawDischMeanPanel, label=self.rawDischMeanLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        rawDischMeanTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, u'Consolas'))
        # rawDischMeanBtn.Bind(wx.EVT_BUTTON, self.OnBTDischargeMean)
        rawDischMeanSizer.Add(rawDischMeanTxt, 1, wx.EXPAND)
        rawDischMeanPanel.SetSizer(rawDischMeanSizer)

        #Mmnt Raw Discharge Mean Val
        self.rawDischMeanCtrl = MyTextCtrl(self, size=(40, -1))
        self.rawDischMeanCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.rawDischMeanCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        #Corrected Mean Gauge Height
        corrMeanGHPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        corrMeanGHSizer = wx.BoxSizer(wx.HORIZONTAL)
        corrMeanGHTxt = wx.StaticText(corrMeanGHPanel, label=self.corrMeanGHLbl, style=wx.ALIGN_LEFT, size=(100, -1))

        corrMeanGHSizer.Add(corrMeanGHTxt, 1, wx.EXPAND)
        corrMeanGHPanel.SetSizer(corrMeanGHSizer)

        #Corrected Mean Gauge Height Val
        self.corrMeanGHCtrl = MyTextCtrl(self, size=(40, -1))
        self.corrMeanGHCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.corrMeanGHCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        #Standard Dev
        standDevMeanDischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        standDevMeanDischSizer = wx.BoxSizer(wx.HORIZONTAL)
        # standDevMeanDischTxt = wx.StaticText(standDevMeanDischPanel, label=self.standDevMeanDischLbl, style=wx.ALIGN_LEFT, size=(110, -1))
        standDevMeanDischBtn = wx.Button(standDevMeanDischPanel, label=self.standDevMeanDischLbl, style=wx.ALIGN_LEFT, size=(110, -1))
        standDevMeanDischBtn.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, u'Consolas'))
        # standDevMeanDischBtn.Bind(wx.EVT_BUTTON, self.OnStandardDev)
        standDevMeanDischSizer.Add(standDevMeanDischBtn, 1, wx.EXPAND)
        standDevMeanDischPanel.SetSizer(standDevMeanDischSizer)

        #Standard Dev Val
        self.standDevMeanDischCtrl = MyTextCtrl(self, size=(40, -1))
        self.standDevMeanDischCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.standDevMeanDischCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

        #Row 1
        horizontalSizer4.Add(mmntStartTimePanel, 1, wx.EXPAND)
        horizontalSizer4.Add(self.mmntStartTimeCtrl, 1, wx.EXPAND)
        horizontalSizer4.Add(rawDischMeanPanel, 1, wx.EXPAND)
        horizontalSizer4.Add(self.rawDischMeanCtrl, 1, wx.EXPAND)
        horizontalSizer4.Add(corrMeanGHPanel, 1, wx.EXPAND)
        horizontalSizer4.Add(self.corrMeanGHCtrl, 1, wx.EXPAND)
        horizontalSizer4.Add(standDevMeanDischPanel, 1, wx.EXPAND)
        horizontalSizer4.Add(self.standDevMeanDischCtrl, 1, wx.EXPAND)
        

        #H Sizer 5
        horizontalSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        
        #MmntEndTime
        mmntEndTimePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mmntEndTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        mmntEndTimeTxt = wx.StaticText(mmntEndTimePanel, label=self.mmntEndTimeLbl, style=wx.ALIGN_RIGHT, size=(100, -1))
        mmntEndTimeSizer.Add(mmntEndTimeTxt, 1, wx.EXPAND)
        mmntEndTimePanel.SetSizer(mmntEndTimeSizer)

        #Mmnt End Time val
        # self.mmntEndTimeCtrl = masked.TimeCtrl(self, displaySeconds=True, size=(40, -1), fmt24hr = True)
        # self.mmntEndTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        # self.mmntEndTimeCtrl.Bind(wx.EVT_TEXT, self.OnEndTime)
        self.mmntEndTimeCtrl = DropdownTime(True, self, size=(-1, -1))
        self.mmntEndTimeCtrl.GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.OnEndTime)
        self.mmntEndTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.OnEndTime)
        self.mmntEndTimeCtrl.GetSecondCtrl().Bind(wx.EVT_COMBOBOX, self.OnEndTime)
        self.mmntEndTimeCtrl.GetHourCtrl().Bind(wx.EVT_KEY_DOWN, self.OnEndTime)
        self.mmntEndTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_KEY_DOWN, self.OnEndTime)
        self.mmntEndTimeCtrl.GetSecondCtrl().Bind(wx.EVT_KEY_DOWN, self.OnEndTime)

        #MB Correction
        mbCorrAppPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mbCorrAppSizer = wx.BoxSizer(wx.HORIZONTAL)
        mbCorrAppTxt = wx.StaticText(mbCorrAppPanel, label=self.mbCorrAppLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        # mbCorrAppBtn = wx.Button(mbCorrAppPanel, label=self.mbCorrAppLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        mbCorrAppTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, u'Consolas'))
        # mbCorrAppBtn.Bind(wx.EVT_BUTTON, self.OnMBCorrApp)

        mbCorrAppSizer.Add(mbCorrAppTxt, 1, wx.EXPAND)
        mbCorrAppPanel.SetSizer(mbCorrAppSizer)

        #MB Correction Val
        self.mbCorrAppCtrl = MyTextCtrl(self, size=(40, -1))
        self.mbCorrAppCtrl.Bind(wx.EVT_TEXT, self.OnFinalDischargeMean)
        self.mbCorrAppCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.mbCorrAppCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        #Base Curve Gauge Height
        baseCurveGHPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        baseCurveGHSizer = wx.BoxSizer(wx.HORIZONTAL)
        baseCurveGHTxt = wx.StaticText(baseCurveGHPanel, label=self.baseCurveGHLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        baseCurveGHSizer.Add(baseCurveGHTxt, 1, wx.EXPAND)
        baseCurveGHPanel.SetSizer(baseCurveGHSizer)

        #Base Curve Gauge Height Val
        self.baseCurveGHCtrl = MyTextCtrl(self, size=(40, -1))
        self.baseCurveGHCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.baseCurveGHCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        #Calc shift from base curve
        calcShiftBaseCurvePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        calcShiftBaseCurveSizer = wx.BoxSizer(wx.HORIZONTAL)
        calcShiftBaseCurveTxt = wx.StaticText(calcShiftBaseCurvePanel, label=self.calcShiftBaseCurveLbl, style=wx.ALIGN_LEFT, size=(110, -1))
        calcShiftBaseCurveSizer.Add(calcShiftBaseCurveTxt, 1, wx.EXPAND)
        calcShiftBaseCurvePanel.SetSizer(calcShiftBaseCurveSizer)

        #Calc shift from base curve Val
        self.calcShiftBaseCurveCtrl = MyTextCtrl(self, size=(40, -1))
        self.calcShiftBaseCurveCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.calcShiftBaseCurveCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

        #Row 2
        horizontalSizer5.Add(mmntEndTimePanel, 1, wx.EXPAND)
        horizontalSizer5.Add(self.mmntEndTimeCtrl, 1, wx.EXPAND)
        horizontalSizer5.Add(mbCorrAppPanel, 1, wx.EXPAND)
        horizontalSizer5.Add(self.mbCorrAppCtrl, 1, wx.EXPAND)
        horizontalSizer5.Add(baseCurveGHPanel, 1, wx.EXPAND)
        horizontalSizer5.Add(self.baseCurveGHCtrl, 1, wx.EXPAND)
        horizontalSizer5.Add(calcShiftBaseCurvePanel, 1, wx.EXPAND)
        horizontalSizer5.Add(self.calcShiftBaseCurveCtrl, 1, wx.EXPAND)
        

        #H Sizer 6
        horizontalSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        #Mmnt Mean Time
        mmntMeanTimePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mmntMeanTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        mmntMeanTimeTxt = wx.StaticText(mmntMeanTimePanel, label=self.mmntMeanTimeLbl, style=wx.ALIGN_RIGHT, size=(100, -1))
        mmntMeanTimeSizer.Add(mmntMeanTimeTxt, 1, wx.EXPAND)
        mmntMeanTimePanel.SetSizer(mmntMeanTimeSizer)

        #Mmnt Meant Time Val
        # self.mmntMeanTimeCtrl = masked.TimeCtrl(self, displaySeconds=True, size=(40, -1), fmt24hr = True)
        # self.mmntMeanTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        self.mmntMeanTimeCtrl = DropdownTime(True, self, size=(-1, -1))

        #Final Discharge 
        finalDischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        finalDischSizer = wx.BoxSizer(wx.HORIZONTAL)
        finalDischTxt = wx.StaticText(finalDischPanel, label=self.finalDischLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        # finalDischBtn = wx.Button(finalDischPanel, label=self.finalDischLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        finalDischTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, u'Consolas'))
        # finalDischBtn.Bind(wx.EVT_BUTTON, self.OnFinalDischargeMean)
        finalDischSizer.Add(finalDischTxt, 1, wx.EXPAND)
        finalDischPanel.SetSizer(finalDischSizer)

        #Final Discharge Ctrl
        self.finalDischCtrl = MyTextCtrl(self, size=(40, -1))
        self.finalDischCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.finalDischCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        #Base Curve Discharge
        baseCurveDischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        baseCurveDischSizer = wx.BoxSizer(wx.HORIZONTAL)
        baseCurveDischTxt = wx.StaticText(baseCurveDischPanel, label=self.baseCurveDischLbl, style=wx.ALIGN_LEFT, size=(100, -1))
        baseCurveDischSizer.Add(baseCurveDischTxt, 1, wx.EXPAND)
        baseCurveDischPanel.SetSizer(baseCurveDischSizer)

        #Base Curve Discharge Val
        self.baseCurveDischCtrl = MyTextCtrl(self, size=(40, -1))
        self.baseCurveDischCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.baseCurveDischCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        #dischargeDiff
        dischDiffBaseCurvePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        dischDiffBaseCurveSizer = wx.BoxSizer(wx.HORIZONTAL)
        dischDiffBaseCurveTxt = wx.StaticText(dischDiffBaseCurvePanel, label=self.dischDiffBaseCurveLbl, style=wx.ALIGN_LEFT, size=(110, -1))
        dischDiffBaseCurveSizer.Add(dischDiffBaseCurveTxt, 1, wx.EXPAND)
        dischDiffBaseCurvePanel.SetSizer(dischDiffBaseCurveSizer)

        #Discharge Diff Val
        self.dischDiffBaseCurveCtrl = MyTextCtrl(self, size=(40, -1))
        self.dischDiffBaseCurveCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.dischDiffBaseCurveCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

        #Row 3
        horizontalSizer6.Add(mmntMeanTimePanel, 1, wx.EXPAND)
        horizontalSizer6.Add(self.mmntMeanTimeCtrl, 1, wx.EXPAND)
        horizontalSizer6.Add(finalDischPanel, 1, wx.EXPAND)
        horizontalSizer6.Add(self.finalDischCtrl, 1, wx.EXPAND)
        horizontalSizer6.Add(baseCurveDischPanel, 1, wx.EXPAND)
        horizontalSizer6.Add(self.baseCurveDischCtrl, 1, wx.EXPAND)
        horizontalSizer6.Add(dischDiffBaseCurvePanel, 1, wx.EXPAND)
        horizontalSizer6.Add(self.dischDiffBaseCurveCtrl, 1, wx.EXPAND)
        


        
        #Row 4
        #comments
        commentsPanel = wx.Panel(self, style=wx.BORDER_NONE, size=(-1, 175))
        commentsSizer = wx.BoxSizer(wx.HORIZONTAL)
        commentsPanel.SetSizer(commentsSizer)

        commentsTxt = wx.StaticText(commentsPanel, label=self.commentsLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        commentsSizer.Add(commentsTxt, 0, wx.EXPAND|wx.ALL, 5)

        self.commentsCtrl = wx.TextCtrl(commentsPanel, style=wx.TE_MULTILINE|wx.TE_BESTWRAP)
        # self.commentsCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        commentsSizer.Add(self.commentsCtrl, 1, wx.EXPAND|wx.ALL, 5)



        layoutSizer.Add(horizontalSizer1, 0, wx.EXPAND)
        layoutSizer.Add(horizontalSizer2, 0, wx.EXPAND)
        layoutSizer.Add(horizontalSizer7, 0, wx.EXPAND)
        layoutSizer.Add(horizontalSizer3, 0, wx.EXPAND)
        layoutSizer.Add(horizontalSizer4, 0, wx.EXPAND)
        layoutSizer.Add(horizontalSizer5, 0, wx.EXPAND)
        layoutSizer.Add(horizontalSizer6, 0, wx.EXPAND)
        layoutSizer.Add(commentsPanel, 0, wx.EXPAND)

        self.SetSizer(layoutSizer)

    def OnAddPress(self, evt):
        self.AddEntry()


    #Add new row to moving boat transect
    def AddEntry(self):

        #Button col
        name = "%s" % self.entryNum

        button = wx.Button(self, label="+", name=name, size=(30, self.rowHeight))

        oldButton = self.tableSizerV.GetItem(self.entryNum).GetSizer().GetItem(0).GetWindow()
        oldButton.SetLabel('-')
        oldButton.Bind(wx.EVT_BUTTON, self.OnRemovePress)



        
        selectCheckbox = wx.CheckBox(self, size=(15, self.rowHeight), name = str(self.entryNum), style=wx.ALIGN_RIGHT)
        transectCtrl = wx.TextCtrl(self, size=(95, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
        startBankCtrl = StartBankPanel(self, style=wx.SIMPLE_BORDER, size=(50, self.rowHeight), name = str(self.entryNum))
        startTimeCtrl = masked.TimeCtrl(self, displaySeconds=True, size=(65, self.rowHeight), fmt24hr=True)
        startDistanceCtrl = MyTextCtrl(self, size=(76, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
        startDistanceCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        startDistanceCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        endDistanceCtrl = MyTextCtrl(self, size=(76, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
        endDistanceCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        endDistanceCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        rawDischCtrl = MyTextCtrl(self, size=(80, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
        rawDischCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        rawDischCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # finalDisCtrl = wx.TextCtrl(self, size=(82, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))
        remarksCtrl = wx.TextCtrl(self, size=(60, self.rowHeight), style=wx.TE_PROCESS_ENTER, name = str(self.entryNum))

        startTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)

        button.SetForegroundColour('Red')
        transectCtrl.SetForegroundColour('Red')
        startDistanceCtrl.SetForegroundColour('Red')
        endDistanceCtrl.SetForegroundColour('Red')
        rawDischCtrl.SetForegroundColour('Red')
        # finalDisCtrl.SetForegroundColour('Red')
        remarksCtrl.SetForegroundColour('Red')


        button.Bind(wx.EVT_BUTTON, self.OnAddPress)
        transectCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        startDistanceCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        endDistanceCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        rawDischCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        # finalDisCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        remarksCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)


        selectCheckbox.Bind(wx.EVT_CHECKBOX, self.OnCheckbox)

        rowSizerNew = wx.BoxSizer(wx.HORIZONTAL)    
        rowSizerNew.Add(button, 0, wx.EXPAND)

        rowSizerOld = self.tableSizerV.GetItem(self.entryNum).GetSizer()


        rowSizerOld.Add(selectCheckbox, 0, wx.EXPAND)
        rowSizerOld.Add(transectCtrl, 2, wx.EXPAND)
        rowSizerOld.Add(startBankCtrl, 2, wx.EXPAND)
        rowSizerOld.Add(startTimeCtrl, 2, wx.EXPAND)
        rowSizerOld.Add(startDistanceCtrl, 2, wx.EXPAND)
        rowSizerOld.Add(endDistanceCtrl, 2, wx.EXPAND)
        rowSizerOld.Add(rawDischCtrl, 2, wx.EXPAND)
        # rowSizerOld.Add(finalDisCtrl, 2, wx.EXPAND)
        rowSizerOld.Add(remarksCtrl, 7, wx.EXPAND)


        self.tableSizerV.Add(rowSizerNew, 0, wx.EXPAND)
        self.entryNum += 1
        self.Layout()


        if self.manager is not None:
            if self.manager.manager is not None:
                selectCheckbox.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
                transectCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
                startTimeCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
                startDistanceCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
                endDistanceCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
                rawDischCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
                remarksCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)







    # When the '-' is clicked, remove that row
    def OnRemovePress(self, e):
        #Button col stuff
        button = e.GetEventObject()
        index = int(button.GetName()) + 1
        if self.mode=="DEBUG":
            print "index %s" % index
        
        if not self.IsEmptyRow(index - 1):
            dlg = wx.MessageDialog(self, "Are you sure you want to delete the row with data entered?", 'Remove',
                                  wx.YES_NO | wx.ICON_QUESTION)

            res = dlg.ShowModal()
            if res == wx.ID_YES:
                dlg.Destroy()
                
            elif res == wx.ID_NO:
                dlg.Destroy()
                return

            else:
                dlg.Destroy()
                return

        self.RemoveEntry(index)
        

    # Delete each column's item at the index of the clicked '-' button
    # Reorder the list of entries
    def RemoveEntry(self, index):
        if self.mode=="DEBUG":
            print "remove %s" % index

        self.tableSizerV.Hide(index)
        self.tableSizerV.Remove(index)
        self.entryNum -= 1      

        for child in range(1, len(self.tableSizerV.GetChildren())):
            i = int(self.tableSizerV.GetItem(child).GetSizer().GetItem(0).GetWindow().GetName())
            if i > index - 1:
                self.tableSizerV.GetItem(child).GetSizer().GetItem(0).GetWindow().SetName("%s" % (i - 1))
        self.Layout()



    def OnTextEnter(self, evt):
    	item = evt.GetEventObject()
        item.SetBackgroundColour('White')
        self.UpdateSammury(evt)

    def UpdateMmntStartTime(self):
        time = None
        for i in range(1, len(self.tableSizerV.GetChildren()) - 1):
            if self.tableSizerV.GetItem(i).GetSizer().GetItem(1).GetWindow().IsChecked():
                time = self.tableSizerV.GetItem(i).GetSizer().GetItem(4).GetWindow().GetValue() if time is None else time
        if time is not None:
            self.mmntStartTimeCtrl.SetValue(time)
  
    def OnCheckbox(self, event):
        box = event.GetEventObject()
        index = -1
        self.UpdateMmntStartTime()
        self.UpdateMeanTime()
        for row in self.tableSizerV.GetChildren():
 

            if box == row.GetSizer().GetChildren()[1].GetWindow():

                for i in range(10):
                    if box.IsChecked():
                        self.manager.SetFontColor(index, i, 'Black')
                    else:
                        self.manager.SetFontColor(index, i, 'Red')
                self.UpdateSammury(event)
                
                return
            else:
                index += 1
            

    def OnBTDischargeMean(self, event):
        counter = 0
        mean = 0

        for i in range(1, len(self.tableSizerV.GetChildren()) - 1):
            row = self.tableSizerV.GetChildren()[i]
            if row.GetSizer().GetChildren()[1].GetWindow().GetValue():
                if row.GetSizer().GetChildren()[7].GetWindow().GetValue() != '':
                    mean += float(row.GetSizer().GetChildren()[7].GetWindow().GetValue())
                    counter += 1
        if counter > 0:
            mean = '' if mean == 0 else mean/counter
        else:
            mean = ''
        if mean != '':
            self.rawDischMeanCtrl.SetValue(str(format(mean, '.3f')))
        else:
            self.rawDischMeanCtrl.SetValue('')

    def OnFinalDischargeMean(self, event):
    	if self.rawDischMeanCtrl.GetValue() != '' and self.mbCorrAppCtrl.GetValue() != '':
    		self.finalDischCtrl.SetValue(str(float(self.rawDischMeanCtrl.GetValue()) + float(self.mbCorrAppCtrl.GetValue())))
    	elif self.rawDischMeanCtrl.GetValue() != '' and self.mbCorrAppCtrl.GetValue() == '':
    		self.finalDischCtrl.SetValue(self.rawDischMeanCtrl.GetValue())
        event.Skip()


    # def OnFinalDischargeMean(self, event):
    #     counter = 0
    #     mean = 0
    #     for i in range(1, len(self.tableSizerV.GetChildren()) - 2):
    #         row = self.tableSizerV.GetChildren()[i]
    #         if row.GetSizer().GetChildren()[1].GetWindow().GetValue():
    #             if row.GetSizer().GetChildren()[8].GetWindow().GetValue() != '':
    #                 mean += float(row.GetSizer().GetChildren()[8].GetWindow().GetValue()) if \
    #                             row.GetSizer().GetChildren()[8].GetWindow().GetValue() != '' else 0
    #                 counter += 1
    #     if counter > 0:
    #         mean = '' if mean == 0 else mean/counter
    #     else:
    #         mean = ''
    #     if mean != '':
    #         self.finalDischCtrl.SetValue(str(format(mean, '.3f')))
    #     else:
    #         self.finalDischCtrl.SetValue('')


    # def OnMBCorrApp(self, event):
    # 	if (self.trackRefCmbo.GetValue() == 'BT') and self.finalDischCtrl.GetValue() != '' and self.rawDischMeanCtrl.GetValue() != '':
    # 		corr = (float(self.finalDischCtrl.GetValue()) - float(self.rawDischMeanCtrl.GetValue()) )/ float(self.finalDischCtrl.GetValue()) * 100
    # 		self.mbCorrAppCtrl.SetValue(str(format(corr, '.3f')))
    # 	else:
    # 		self.mbCorrAppCtrl.SetValue('')

    # def OnStandardDev(self, evt):
    #     discharges = []
    #     for i in range(1, len(self.tableSizerV.GetChildren()) - 2):
    #         row = self.tableSizerV.GetChildren()[i]
    #         if row.GetSizer().GetChildren()[1].GetWindow().GetValue():
    #             if row.GetSizer().GetChildren()[8].GetWindow().GetValue() != '':
    #                 discharges.append(float(row.GetSizer().GetChildren()[8].GetWindow().GetValue())) if \
    #                             row.GetSizer().GetChildren()[8].GetWindow().GetValue() != '' else 0

    #     if len(discharges) > 0 and self.finalDischCtrl.GetValue() != '':
    #         self.standDevMeanDischCtrl.SetValue(format(float(self.standardDeviation(discharges) / float(self.finalDischCtrl.GetValue()) * 100), '.3f'))
    #     else:
    #         self.standDevMeanDischCtrl.SetValue('')

    def UpdateSammury(self, event):
    	self.OnBTDischargeMean(event)
    	
    	# self.OnMBCorrApp(event)
    	self.OnFinalDischargeMean(event)
    	# self.OnStandardDev(event)



    #return the standard deviation of a list of numbers
    def standardDeviation(self, nums):
        mean = 0
        total = 0
        if len(nums) == 1:
            return 0
        for i in range(len(nums)):
            mean += float(nums[i])
        mean = mean / len(nums)

        for i in range(len(nums)):
            total += (float(nums[i]) - mean) ** 2
        return math.sqrt(total / (len(nums) - 1))


    #On end time update mean time
    def OnEndTime(self, event):
        try:
            event.GetEventObject().GetParent().UpdateTime(event.GetKeyCode())
        except:
            pass
        self.UpdateMeanTime()
        event.Skip()


    def UpdateMeanTime(self):
        
        mean = DropdownTime.CalculateMean(self.mmntStartTimeCtrl, self.mmntEndTimeCtrl)
        self.mmntMeanTimeCtrl.SetValue(mean)





    #allow only the float number type inputs
    def NumberControl(self, event):
        ctrl = event.GetEventObject()
        try:
            ctrlVal = float(ctrl.GetValue())
            ctrl.preValue = ctrl.GetValue()
        except:
            if ctrl.GetValue() == '':
                ctrl.preValue = ''
            elif ctrl.GetValue() == '.':
                ctrl.preValue = '.'
            elif ctrl.GetValue() == '-':
                ctrl.preValue = '-'
            elif ctrl.GetValue() == '-.':
                ctrl.preValue = '-.'
            elif ctrl.GetValue() == '+':
                ctrl.preValue = '+'
            elif ctrl.GetValue() == '+.':
                ctrl.preValue = '+.'
            else:
                insertPoint = ctrl.GetInsertionPoint() - 1
                ctrl.SetValue(ctrl.preValue)
                ctrl.SetInsertionPoint(insertPoint)



    def OnKillFocus(self, event, decimal):
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
            # ctrl.ChangeValue(str(round(float(value), decimal)))
        elif re.match(reg2, value):
            value = value[:-1]
            # ctrl.ChangeValue(value)
        elif re.match(reg5, value):
            pass
        # else:
            # ctrl.ChangeValue(str(round(float(value), decimal)))
        if ctrl.GetValue() != "":
            decimalPlaces = Decimal(10) ** -decimal
            value = Decimal(value).quantize(decimalPlaces)
            ctrl.ChangeValue(str(value))
        event.Skip()

    #Reset the time ctrl to "00:00:00" by pressing 'R'
    def OnResetTime(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('R'):
            ctrl = event.GetEventObject()
            ctrl.SetValue("00:00:00")
        event.Skip()


    def IsEmptyRow(self, index):
        if self.manager.GetTableValue(index, 2) == "" and self.manager.GetTableValue(index, 5) == ""\
        and self.manager.GetTableValue(index, 6) == "" and self.manager.GetTableValue(index, 7) == ""\
        and self.manager.GetTableValue(index, 8) == "":
            return True
        else:
            return False

    #Display bank other textctrl if other selected, otherwise hide textctrl
    def OnLeftBank(self, event):
        if event.GetEventObject().GetValue() == "Other":
            self.leftBankOtherCtrl.Show()
        else:
            self.leftBankOtherCtrl.Hide()
            self.leftBankOtherCtrl.SetValue("")
        self.Layout()
        event.Skip()



    def OnRightBank(self, event):
        if event.GetEventObject().GetValue() == "Other":
            self.rightBankOtherCtrl.Show()
        else:
            self.rightBankOtherCtrl.Hide()
            self.rightBankOtherCtrl.SetValue("")

        self.Layout()
        event.Skip()
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(780, 700))
    MovingBoatMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
