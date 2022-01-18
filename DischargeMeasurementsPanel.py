# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import wx.lib.masked as masked
import NumberControl
from DropdownTime import *


from wx import ComboPopup

from pdb import set_trace
#----------------------------------------------------------------------
# This class is used to provide an interface between a ComboCtrl and the
# ListCtrl that is used as the popoup for the combo widget.

class ListCtrlComboPopup(wx.ComboPopup):

    def __init__(self, parent, combo):
        wx.ComboPopup.__init__(self)
        self.lc = None
        self.Create(parent)
        self.combo = combo
        
    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def AppendItems(self, items):
        for item in items:
            self.AddItem(item)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()
        self.combo.SetInsertionPoint(0)


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)


#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

class DischargeMeasurementsPanel(wx.Panel):
    def __init__(self, mode, lang, *args, **kwargs):
        super(DischargeMeasurementsPanel, self).__init__(*args, **kwargs)

        self.startTimeLbl = "Start Time"
        self.endTimeLbl = "End Time"
        self.airTempLbl = "Air Temp. \n(\N{DEGREE SIGN}C)"
        self.waterTempLbl = "Water Temp. \n(\N{DEGREE SIGN}C)"
        self.widthLbl = "Width\n(m)"
        self.areaLbl = "Area\n(m\N{SUPERSCRIPT TWO})"
        self.meanVelLbl = "Mean Velocity (m/s)"
        self.mghLbl = "M.G.H. (m)"
        self.dischLbl = "Discharge (m\N{SUPERSCRIPT THREE}/s)"
        self.uncertaintyLbl = "Uncertainty (%)"
        self.mmtLbl = "Mmt Mean Time"
        self.shiftLbl = "Calc. Shift Base Curve (m)"
        self.diffLbl = "Difference Base Curve (%)"
        self.curveLbl = "Curve #"
        self.mghChoices = ["", "  (HG)", "  (HG2)", "  (WLR1)", "  (WLR2)"]
        # self.dischChoices = ["","E","B"]
        self.curveList = [""]

        self.controlConditionRemLbl = "Control Condition Remarks"
        self.dischRemarkLbl = "Discharge Activity Remarks"
#         self.correctMGHBtnHint = "Attention! \n\nYou must enter your SRC in the stage summary table below if:\n\n\
#         1.  SRC is not 0.000\n\
#         2.  You are uploading logger information\n\n\
# This field is not directly uploaded to AQUARIUS. To ensure the correct gauge correction is uploaded, Weighted M.G.H, SRC \
# and Gauge Correction must be entered in the EHSN stage summary table below."
        self.correctMGHBtnHint = "This field is not directly uploaded to AQUARIUS. To ensure the correct gauge correction is uploaded, the Weighted M.G.H, SRC \
 and Gauge Correction must be entered in the EHSN stage summary table below."

        self.uncertaintyInfoMsg = """
All uncertainty values reported here are 2-sigma value
- FlowTracker (2 x Uncertainty Value reported in *.dis File)
- FlowTracker2 (2 x Uncertainty Value reported in *.ft File)
- SxS Pro (1 x Uncertainty Value reported in *.xml File)
- RSSL(2 x Uncertainty Value reported in *.dis File)
- QRev (1 x Uncertainty Value reported in *.xml File)
- eHSN Mid-section (IVE Value)
"""

        self.timeFormat = "%H:%M"
        if lang == wx.LANGUAGE_ENGLISH:
            self.timeFormat = "%I:%M"
        
        self.mmtDfltValLbl = wx.DateTime.Now().Format(self.timeFormat)
        self.mode = mode
        self.manager = None



        self.controlLbl = "Control Condition"
        self.contCondLbl = "Condition"
        self.contCondList = ["", "Unspecified", "No Flow", "Clear", "Altered", "Debris",
                             "Vegetation", "Fill", "Scour", "Ice"]
        # self.picturedLbl = "Site and/or control pictures were taken."


        #height for panels
        self.height = 40
        f = self.GetFont()
        dc = wx.WindowDC(self)
        dc.SetFont(f)
        self.width, self.height = dc.GetTextExtent("Ag")
        self.height *= 2.2

        self.ctrlHeight = self.height - 6

        self.BGColour = (210, 210, 210)


        self.wrapLength = 80
        self.lang = lang

        self.InitUI()

        # self.endTimeCtrl.SetToCurrent()
        # self.airTempCtrl.SetValue("11111")

    def InitUI(self):
        if self.mode=="DEBUG":
            print("In DischargeMeasurementsPanel")
        self.layoutSizer = wx.GridBagSizer(0, 0)
        self.locale = wx.Locale(self.lang)

        #Start Time Info
        startTimePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        startTimePanel.SetBackgroundColour(self.BGColour)
        startTimeSizer = wx.BoxSizer(wx.VERTICAL)
        startTimeSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        startTimeTxt = wx.StaticText(startTimePanel, 1, label=self.startTimeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        startTimeTxt.Wrap(self.wrapLength)
        # self.startTimeCtrl = masked.TimeCtrl(startTimePanel, 2, size=(-1, self.ctrlHeight), displaySeconds=False, fmt24hr = True)
        # # self.startTimeCtrl.SetValue(wx.DateTime_Now().FormatTime())
        # self.startTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)

        self.startTimeCtrl = DropdownTime(False, parent=startTimePanel, id=2, size=(-1, self.ctrlHeight))
        startTimeSizer.Add(startTimeTxt, 1, wx.EXPAND)
        startTimeSizer.Add(self.startTimeCtrl, 1, wx.EXPAND)
        startTimeSizerH.Add(startTimeSizer, 1, wx.EXPAND, 0)
        
        startTimePanel.SetSizer(startTimeSizerH)

        #End Time Info
        endTimePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        endTimePanel.SetBackgroundColour(self.BGColour)
        endTimeSizer = wx.BoxSizer(wx.VERTICAL)
        endTimeSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        endTimeTxt = wx.StaticText(endTimePanel, 3, label=self.endTimeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        endTimeTxt.Wrap(self.wrapLength)
        # self.endTimeCtrl = masked.TimeCtrl(endTimePanel, 4, size=(-1, self.ctrlHeight), displaySeconds=False, fmt24hr = True)
        # # self.endTimeCtrl.SetValue(wx.DateTime_Now().FormatTime())
        # self.endTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        self.endTimeCtrl = DropdownTime(False, parent=endTimePanel, id=4, size=(-1, self.ctrlHeight))
        endTimeSizer.Add(endTimeTxt, 1, wx.EXPAND)
        endTimeSizer.Add(self.endTimeCtrl, 1, wx.EXPAND)
        endTimeSizerH.Add(endTimeSizer, 1, wx.EXPAND)

        endTimePanel.SetSizer(endTimeSizerH)

        #Air Temperature Info
        airTempPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        airTempPanel.SetBackgroundColour(self.BGColour)
        airTempSizer = wx.BoxSizer(wx.VERTICAL)
        airTempSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        airTempTxt = wx.StaticText(airTempPanel, 5, label=self.airTempLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        airTempTxt.Wrap(self.wrapLength)
        self.airTempCtrl = MyTextCtrl(airTempPanel, 6, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.airTempCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.airTempCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round1)
        airTempSizer.Add(airTempTxt, 1, wx.EXPAND)
        airTempSizer.Add(self.airTempCtrl, 1, wx.EXPAND)
        airTempSizerH.Add(airTempSizer, 1, wx.EXPAND)

        airTempPanel.SetSizer(airTempSizerH)

        #Water Temperature Info
        waterTempPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        waterTempPanel.SetBackgroundColour(self.BGColour)
        waterTempSizer = wx.BoxSizer(wx.VERTICAL)
        waterTempSizerH = wx.BoxSizer(wx.HORIZONTAL)
         
        waterTempTxt = wx.StaticText(waterTempPanel, 7, label=self.waterTempLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        waterTempTxt.Wrap(self.wrapLength)
        self.waterTempCtrl = MyTextCtrl(waterTempPanel, 8, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.waterTempCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.waterTempCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round1)
        waterTempSizer.Add(waterTempTxt, 1, wx.EXPAND)
        waterTempSizer.Add(self.waterTempCtrl, 1, wx.EXPAND)
        waterTempSizerH.Add(waterTempSizer, 1, wx.EXPAND)

        waterTempPanel.SetSizer(waterTempSizerH)

        #Width Info
        widthPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        widthPanel.SetBackgroundColour(self.BGColour)
        widthSizer = wx.BoxSizer(wx.VERTICAL)
        widthSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        widthTxt = wx.StaticText(widthPanel, 9, label=self.widthLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        widthTxt.Wrap(self.wrapLength)
        self.widthCtrl = MyTextCtrl(widthPanel, 10, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.widthCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.widthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        widthSizer.Add(widthTxt, 1, wx.EXPAND)
        widthSizer.Add(self.widthCtrl, 1, wx.EXPAND)
        widthSizerH.Add(widthSizer, 1, wx.EXPAND)

        widthPanel.SetSizer(widthSizerH)

        #Area Info
        areaPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        areaPanel.SetBackgroundColour(self.BGColour)
        areaSizer = wx.BoxSizer(wx.VERTICAL)
        areaSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        areaTxt = wx.StaticText(areaPanel, 11, label=self.areaLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        areaTxt.Wrap(self.wrapLength)
        self.areaCtrl = MyTextCtrl(areaPanel, 12, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.areaCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.areaCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        areaSizer.Add(areaTxt, 1, wx.EXPAND)
        areaSizer.Add(self.areaCtrl, 1, wx.EXPAND)
        areaSizerH.Add(areaSizer, 1, wx.EXPAND)

        areaPanel.SetSizer(areaSizerH)

        #Mean Velocity Info
        meanVelPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        meanVelPanel.SetBackgroundColour(self.BGColour)
        meanVelSizer = wx.BoxSizer(wx.VERTICAL)
        meanVelSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        meanVelTxt = wx.StaticText(meanVelPanel, 13, label=self.meanVelLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        meanVelTxt.Wrap(self.wrapLength)
        self.meanVelCtrl = MyTextCtrl(meanVelPanel, 14, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(85, self.ctrlHeight))
        self.meanVelCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.meanVelCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnMeanVel)
        meanVelSizer.Add(meanVelTxt, 1, wx.EXPAND)
        meanVelSizer.Add(self.meanVelCtrl, 1, wx.EXPAND)
        meanVelSizerH.Add(meanVelSizer, 1, wx.EXPAND)

        meanVelPanel.SetSizer(meanVelSizerH)

        #Mean Gauge Height Info
        mghPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mghPanel.SetBackgroundColour(self.BGColour)
        mghSizer = wx.BoxSizer(wx.VERTICAL)
        mghSizerH = wx.BoxSizer(wx.HORIZONTAL)
            
        cmghSizer = wx.BoxSizer(wx.HORIZONTAL)


        mghTxt = wx.StaticText(mghPanel, 15, label=self.mghLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height/2))
        self.correctMGHButton = wx.Button(mghPanel, size=(15, self.height/2), label="!")
        self.correctMGHButton.SetForegroundColour('red')
        self.correctMGHButton.Bind(wx.EVT_BUTTON, self.OnCMGHBtn)

        self.mghCmbo = wx.ComboBox(mghPanel, choices=self.mghChoices, style=wx.CB_READONLY, size=(-1, self.height/2))
        # set_trace()
        self.mghCmbo.Bind(wx.EVT_COMBOBOX, self.UpdateMGHCtrl)


        cmghSizer.Add(mghTxt, 1, wx.EXPAND)
        cmghSizer.Add(self.correctMGHButton, 0, wx.EXPAND)

        mghTxt.Wrap(self.wrapLength)
        
        self.mghCtrl = MyTextCtrl(mghPanel, 16, style=wx.TE_READONLY|wx.TE_CENTRE, size=(-1, self.ctrlHeight))



        mghSizer.Add(cmghSizer, 3, wx.EXPAND)
        mghSizer.Add(self.mghCmbo, 4, wx.EXPAND)
        mghSizer.Add(self.mghCtrl, 5, wx.EXPAND)
        mghSizerH.Add(mghSizer, 1, wx.EXPAND)

        mghPanel.SetSizer(mghSizerH)

        #Discharge Info
        dischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        dischPanel.SetBackgroundColour(self.BGColour)
        dischSizer = wx.BoxSizer(wx.VERTICAL)
        dischSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        dischSizerH = wx.BoxSizer(wx.HORIZONTAL)

        dischTxt = wx.StaticText(dischPanel, 17, label=self.dischLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        dischTxt.Wrap(self.wrapLength)
        self.dischCtrl = MyTextCtrl(dischPanel, 18, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.dischCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.dischCtrl.Bind(wx.EVT_TEXT, self.OnChangeUpdateMovingBoat)
        self.dischCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnDischarge)
        self.dischCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnUpdateHGQValues)
        # self.dischCombo = wx.ComboBox(dischPanel, choices=self.dischChoices, style=wx.CB_READONLY, size=(32, self.ctrlHeight))

        dischSizer.Add(dischTxt, 1, wx.EXPAND)
        dischSizer1.Add(self.dischCtrl, 1, wx.EXPAND)
        # dischSizer1.Add(self.dischCombo, 0, wx.EXPAND)
        dischSizer.Add(dischSizer1, 1, wx.EXPAND)
        dischSizerH.Add(dischSizer, 1, wx.EXPAND)

        dischPanel.SetSizer(dischSizerH)


        #Uncertainty Info
        uncertaintyPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        uncertaintyPanel.SetBackgroundColour(self.BGColour)
        uncertaintySizer = wx.BoxSizer(wx.VERTICAL)
        uncertaintySizer1 = wx.BoxSizer(wx.HORIZONTAL)
        uncertaintySizerH = wx.BoxSizer(wx.HORIZONTAL)

        uncertaintyLabelSizerH = wx.BoxSizer(wx.HORIZONTAL)

        self.uncertaintyInfoBtn = wx.Button(uncertaintyPanel, size=(15, self.height/2), label="!")
        self.uncertaintyInfoBtn.SetForegroundColour('red')
        self.uncertaintyInfoBtn.Bind(wx.EVT_BUTTON, self.OnUncertaintyInfoBtn)

        uncertaintyTxt = wx.StaticText(uncertaintyPanel, 17, label=self.uncertaintyLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        uncertaintyTxt.Wrap(self.wrapLength)
        self.uncertaintyCtrl = MyTextCtrl(uncertaintyPanel, 18, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.uncertaintyCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        # self.uncertaintyCtrl.Bind(wx.EVT_TEXT, self.OnChangeUpdateMovingBoat)
        self.uncertaintyCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnDischarge)
        self.uncertaintyCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnUpdateHGQValues)

        uncertaintyLabelSizerH.Add(uncertaintyTxt, 1, wx.EXPAND)
        uncertaintyLabelSizerH.Add(self.uncertaintyInfoBtn, 0, wx.EXPAND)

        uncertaintySizer.Add(uncertaintyLabelSizerH, 1, wx.EXPAND)
        uncertaintySizer1.Add(self.uncertaintyCtrl, 1, wx.EXPAND)
        uncertaintySizer.Add(uncertaintySizer1, 1, wx.EXPAND)

        uncertaintySizerH.Add(uncertaintySizer, 1, wx.EXPAND)

        uncertaintyPanel.SetSizer(uncertaintySizerH)



        #Mmt Mean Time Info
        mmtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        mmtPanel.SetBackgroundColour(self.BGColour)
        mmtLblSubPanel = wx.Panel(mmtPanel)
        mmtValSubPanel = wx.Panel(mmtPanel, style=wx.BORDER_SUNKEN)
        
        mmtSizerH = wx.BoxSizer(wx.HORIZONTAL)
        mmtLblSubSizerH = wx.BoxSizer(wx.HORIZONTAL)
        mmtValSubSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        mmtTxt = wx.StaticText(mmtLblSubPanel, 19, label=self.mmtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        mmtTxt.Wrap(self.wrapLength)
        self.mmtValTxt = wx.StaticText(mmtValSubPanel, 20, label='', style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.ctrlHeight))

        mmtLblSubSizerH.Add(mmtTxt, 1, wx.EXPAND)
        mmtLblSubPanel.SetSizer(mmtLblSubSizerH)
        mmtValSubSizerH.Add(self.mmtValTxt, 1, wx.EXPAND)
        mmtValSubPanel.SetSizer(mmtValSubSizerH)
        
        mmtSizerH.Add(mmtLblSubPanel, 1, wx.EXPAND)
        mmtSizerH.Add(mmtValSubPanel, 1, wx.EXPAND)

        mmtPanel.SetSizer(mmtSizerH)

        #Calc Shift Base Curve Info
        shiftPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        shiftPanel.SetBackgroundColour(self.BGColour)
        shiftSizerH = wx.BoxSizer(wx.HORIZONTAL)

        shiftTxt = wx.StaticText(shiftPanel, 21, label=self.shiftLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        shiftTxt.Wrap(self.wrapLength)
        self.shiftCtrl = MyTextCtrl(shiftPanel, 22, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.shiftCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.shiftCtrl.Bind(wx.EVT_TEXT, self.OnChangeUpdateMovingBoat)
        self.shiftCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        shiftSizerH.Add(shiftTxt, 1, wx.EXPAND)
        shiftSizerH.Add(self.shiftCtrl, 1, wx.EXPAND)

        shiftPanel.SetSizer(shiftSizerH)

        #Difference Base Curve Info
        diffPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        diffPanel.SetBackgroundColour(self.BGColour)
        diffSizerH = wx.BoxSizer(wx.HORIZONTAL)

        diffTxt = wx.StaticText(diffPanel, 23, label=self.diffLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        diffTxt.Wrap(self.wrapLength)
        self.diffCtrl = MyTextCtrl(diffPanel, 24, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(70, self.ctrlHeight))
        self.diffCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.diffCtrl.Bind(wx.EVT_TEXT, self.OnChangeUpdateMovingBoat)

        diffSizerH.Add(diffTxt, 1, wx.EXPAND)
        diffSizerH.Add(self.diffCtrl, 1, wx.EXPAND)

        diffPanel.SetSizer(diffSizerH)

        #Curve Info
        curvePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        curvePanel.SetBackgroundColour(self.BGColour)
        curveSizerG = wx.GridBagSizer(0, 0)

        curveTxt = wx.StaticText(curvePanel, 25, label=self.curveLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, self.height))
        curveTxt.Wrap(self.wrapLength)
        
        self.curveCtrl = wx.ComboBox(curvePanel, 26, choices=self.curveList, style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(120, self.ctrlHeight))
        self.curveCtrl.Bind(wx.EVT_TEXT, self.FloatNumberControl)
        self.curveCtrl.Bind(wx.EVT_TEXT, self.OnRCText)
        self.curveCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnRCKillFocus)
        self.curveCtrl.Bind(wx.EVT_COMBOBOX, self.OnRCCombo)
        curveSizerG.Add(curveTxt, pos=(0, 0), span=(1, 1), flag=wx.EXPAND)
        curveSizerG.Add(self.curveCtrl, pos=(0, 1), span=(1, 2), flag=wx.EXPAND)

        for i in range(2):
            curveSizerG.AddGrowableCol(i)
        for i in range(1):
            curveSizerG.AddGrowableRow(i)

        curvePanel.SetSizer(curveSizerG)





        #Control and Remarks
        controlConditionSizer = wx.BoxSizer(wx.HORIZONTAL)

        controlConditionPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.height))
        controlConditionPanel.SetSizer(controlConditionSizer)

        controlTxt = wx.StaticText(controlConditionPanel, label=self.controlLbl, size=(80, self.height), style=wx.ALIGN_CENTRE_HORIZONTAL)
        controlTxt.SetForegroundColour("blue")
        controlTxt.SetBackgroundColour(self.BGColour)
        # controlTxt.SetBackgroundColour("gold")
        self.controlConditionCmbo = wx.ComboBox(controlConditionPanel, choices=self.contCondList, style=wx.CB_READONLY, size=(80, self.height))
        self.controlConditionCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        # self.picturedCkbox = wx.CheckBox(controlConditionPanel, label=self.picturedLbl)

        controlConditionSizer.Add(controlTxt, 1, wx.EXPAND)
        controlConditionSizer.Add(self.controlConditionCmbo, 1, wx.EXPAND)




        # #control condition remarks
        controlConditionRemarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        controlConditionRemarkPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.height * 1.2))
        controlConditionRemarkPanel.SetSizer(controlConditionRemarkSizer)


        controlConditionTxt = wx.StaticText(controlConditionRemarkPanel, label=self.controlConditionRemLbl, size=(200, self.height), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.controlConditionRemarksCtrl = wx.TextCtrl(controlConditionRemarkPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, self.height * 1.2))
        controlConditionRemarkSizer.Add(controlConditionTxt, 0, wx.EXPAND)
        controlConditionRemarkSizer.Add(self.controlConditionRemarksCtrl, 1, wx.EXPAND)


        dischargeRemarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        dischargeRemarkPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.height * 1.2))
        dischargeRemarkPanel.SetSizer(dischargeRemarkSizer)

        self.dischTxt = wx.StaticText(dischargeRemarkPanel, label=self.dischRemarkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(200, self.height))
        self.dischRemarksCtrl = wx.TextCtrl(dischargeRemarkPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, self.height * 1.2))
        dischargeRemarkSizer.Add(self.dischTxt, 0)
        dischargeRemarkSizer.Add(self.dischRemarksCtrl, 1, wx.EXPAND)



        self.layoutSizer.Add(startTimePanel, pos=(0, 0), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(endTimePanel, pos=(0, 1), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(airTempPanel, pos=(0, 2), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(waterTempPanel, pos=(0, 3), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(widthPanel, pos=(0, 4), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(areaPanel, pos=(0, 5), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(meanVelPanel, pos=(0, 6), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(mghPanel, pos=(0, 7), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(dischPanel, pos=(0, 8), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(uncertaintyPanel, pos=(0, 9), span=(2, 1), flag=wx.EXPAND)
        self.layoutSizer.Add(mmtPanel, pos=(2, 0), span=(1, 2), flag=wx.EXPAND)
        self.layoutSizer.Add(shiftPanel, pos=(2, 2), span=(1, 2), flag=wx.EXPAND)
        self.layoutSizer.Add(diffPanel, pos=(2, 4), span=(1, 2), flag=wx.EXPAND)
        self.layoutSizer.Add(curvePanel, pos=(2, 6), span=(1, 4), flag=wx.EXPAND)


        self.layoutSizer.Add(controlConditionPanel, pos=(3, 0), span=(1, 2), flag=wx.EXPAND)
        self.layoutSizer.Add(controlConditionRemarkPanel, pos=(3, 2), span=(1, 8), flag=wx.EXPAND)
        self.layoutSizer.Add(dischargeRemarkPanel, pos=(4, 0), span=(1, 10), flag=wx.EXPAND)
        

        self.startTimeCtrl.GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeChange)
        self.startTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeChange)
        self.startTimeCtrl.GetHourCtrl().Bind(wx.EVT_KEY_UP, self.OnTimeChange)
        self.startTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_KEY_UP, self.OnTimeChange)
        self.startTimeCtrl.cBtn.Bind(wx.EVT_BUTTON, self.OnCBtn)
        # self.startTimeCtrl.GetHourCtrl().Bind(wx.EVT_TEXT, self.OnTimeChange)
        # self.startTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_TEXT, self.OnTimeChange)
        self.endTimeCtrl.GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeChange)
        self.endTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeChange)
        self.endTimeCtrl.GetHourCtrl().Bind(wx.EVT_KEY_UP, self.OnTimeChange)
        self.endTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_KEY_UP, self.OnTimeChange)
        self.endTimeCtrl.cBtn.Bind(wx.EVT_BUTTON, self.OnCBtn)
        # self.endTimeCtrl.GetHourCtrl().Bind(wx.EVT_TEXT, self.OnTimeChange)
        # self.endTimeCtrl.GetMinuteCtrl().Bind(wx.EVT_TEXT, self.OnTimeChange)

        for i in range(9):
            self.layoutSizer.AddGrowableCol(i)

        for i in range(3):
            self.layoutSizer.AddGrowableRow(i)

        self.SetSizerAndFit(self.layoutSizer)
        


    #Activate or Deactivate the row by row number
    #And call OnTimeUpdateMGH event
    def OnCBtn(self, event):
        timeObj = event.GetEventObject().GetParent()
        timeObj.SetToCurrent()
        self.OnTimeChange(event)
        event.Skip()


    # used to calculate mean time
    def OnTimeChange(self, event):

        try:
            # keycode = event.GetEventObject().GetValue()[-1]
            keycode = event.GetKeyCode()
            event.GetEventObject().GetParent().NumberControl(event)
            if keycode == ord('R') or keycode == ord('C'):
                event.GetEventObject().GetParent().UpdateTime(keycode)      
        except:
            pass
        self.UpdateMeanTime()

    #update mean time
    def UpdateMeanTime(self):
        startHour = self.startTimeCtrl.GetHourVal()
        startMinute = self.startTimeCtrl.GetMinuteVal()

        endHour = self.endTimeCtrl.GetHourVal()
        endMinute = self.endTimeCtrl.GetMinuteVal()

        if startHour == "" or startMinute == "" or endHour == "" or endMinute == "":
            self.SetMmtValTxt("")
            self.layoutSizer.Layout()

        else:
            startHour = int(startHour)
            startMinute = int(startMinute)
            endHour = int(endHour)
            endMinute = int(endMinute)

            if startHour > endHour or (startHour == endHour and startMinute > endMinute):
                endHour += 24

            totalMinute = (startHour + endHour) * 60 + startMinute + endMinute
            meanMinute = totalMinute / 2

            meanHour = meanMinute / 60 % 24
            if meanHour < 10:
                meanHour = "0" + str(meanHour)

            meanMinute = meanMinute % 60
            if meanMinute < 10:
                meanMinute = "0" + str(meanMinute)

            self.SetMmtValTxt(str(meanHour) + ":" + str(meanMinute))
            self.layoutSizer.Layout()

        # event.Skip()
        


        

    # Any update will affect data on moving boat
    def OnChangeUpdateMovingBoat(self, event):
        if self.manager is not None:
            if self.manager.manager.instrDepManager.GetMethodCBListBox().GetCurrentSelection()==2:
                self.manager.manager.movingBoatMeasurementsManager.recalculate()
        event.Skip()
        

    #Checking if all the field to upload to AQ are empty
    def IsEmpty(self):
        if self.GetWidthCtrl() == '' \
                and self.GetAreaCtrl() == '' \
                and self.GetMeanVelCtrl() == ''\
                and self.GetDischCtrl() == '':
                # and self.GetMghCtrl() == '':
            return True
        else:

            return False




    #Start Time Ctrl
    def GetStartTimeCtrl(self):
        return self.startTimeCtrl.GetValue()


    # def SetStartTimeCtrl(self, startTimeCtrl):
    #     time = wx.DateTime()
    #     time.ParseTime(startTimeCtrl)
    #     self.startTimeCtrl.SetValue(time)

    def SetStartTimeCtrl(self, time):
        self.startTimeCtrl.SetValue(time)




    #End Time Ctrl
    def GetEndTimeCtrl(self):
        return self.endTimeCtrl.GetValue()


    def SetEndTimeCtrl(self, time):
        # time = wx.DateTime()
        # time.ParseTime(endTimeCtrl)
        self.endTimeCtrl.SetValue(time)




    #Air Temp Ctrl
    def GetAirTempCtrl(self):
        return self.airTempCtrl.GetValue()

    def SetAirTempCtrl(self, airTempCtrl):
        self.airTempCtrl.SetValue(airTempCtrl)


    #Water Temp Ctrl

    def GetWaterTempCtrl(self):
        return self.waterTempCtrl.GetValue()


    def SetWaterTempCtrl(self, waterTempCtrl):
        self.waterTempCtrl.SetValue(waterTempCtrl)


    #Width Info ctrl
    def GetWidthCtrl(self):
        return self.widthCtrl.GetValue()

    def SetWidthCtrl(self, widthCtrl):
        self.widthCtrl.SetValue(widthCtrl)


    #Area Info Ctrl
    def GetAreaCtrl(self):
        return self.areaCtrl.GetValue()


    def SetAreaCtrl(self, areaCtrl):
        self.areaCtrl.SetValue(areaCtrl)


    #Mean Velocity Info
    def GetMeanVelCtrl(self):
        return self.meanVelCtrl.GetValue()

    def SetMeanVelCtrl(self, meanVelCtrl):
        self.meanVelCtrl.SetValue(meanVelCtrl)



    #MGH Ctrl
    def GetMghCtrl(self):
        return self.mghCtrl.GetValue()


    def SetMghCtrl(self, mghCtrl):
        self.mghCtrl.SetValue(mghCtrl)

    #MGH Combo
    def GetMghCmbo(self):
        return self.mghCmbo.GetValue()


    def SetMghCmbo(self, mghCmbo):
        self.mghCmbo.SetValue(mghCmbo)




    #Discharge Ctrl
    def GetDischCtrl(self):
        return self.dischCtrl.GetValue()


    def SetDischCtrl(self, dischCtrl):
        self.dischCtrl.SetValue(dischCtrl)

    #Discharge Combo
    # def GetDischCombo(self):
        # return self.dischCombo.GetValue()

    # def SetDischCombo(self,dischCombo):
        # self.dischCombo.SetValue(dischCombo)


    #Uncertainty Ctrl
    def GetUncertaintyCtrl(self):
        return self.uncertaintyCtrl.GetValue()

    def SetUncertaintyCtrl(self, val):
        self.uncertaintyCtrl.SetValue(val)



    #Mmt Mean Time Ctrl
    def GetMmtValTxt(self):
        return self.mmtValTxt.GetLabel()

    def SetMmtValTxt(self, mmtValTxt):
        self.mmtValTxt.SetLabel(mmtValTxt)
        self.layoutSizer.Layout()



    #Calculate Shift Base Curve Ctrl
    def GetShiftCtrl(self):
        return self.shiftCtrl.GetValue()

    def SetShiftCtrl(self, shiftCtrl):
        self.shiftCtrl.SetValue(shiftCtrl)



    #Diff Base Curve Info Ctrl
    def GetDiffCtrl(self):
        return self.diffCtrl.GetValue()


    def SetDiffCtrl(self, diffCtrl):
        self.diffCtrl.SetValue(diffCtrl)



    #Curve Info Ctrl
    def GetCurveCtrl(self):
        return self.curveCtrl.GetValue()


    def SetCurveCtrl(self, curveCtrl):
        self.curveCtrl.ChangeValue(curveCtrl)


    def SetCurveCombo(self, rcList):
        curveList = list(rcList)
        curveList.append("")

        curveVal = self.GetCurveCtrl()
        self.curveCtrl.SetItems(curveList)
        self.SetCurveCtrl(curveVal)


    def SetCurveIndex(self, index):
        self.curveCtrl.SetSelection(index)

    def OnUpdateHGQValues(self, event):
        if self.manager is not None:
            self.manager.OnUpdateHGQValues()

        event.Skip()

    def OnUpdateCurveValues(self, event):
        if self.manager is not None:
            self.manager.OnUpdateCurveValues()

    def OnRCText(self, event):
        if self.manager is not None:
            self.manager.OnRCText()

        event.Skip()

    def OnRCKillFocus(self, event):
        if self.manager is not None:
            self.manager.OnRCKillFocus()

        event.Skip()

    def OnRCCombo(self, event):
        if self.manager is not None:
            self.manager.OnRCCombo()

        event.Skip()

    #allow only the float number type inputs
    def FloatNumberControl(self, event):
        ctrl = event.GetEventObject()
        value = ctrl.GetValue().strip()

        try:
            float(value)
            ctrl.preValue = value
            insertPoint = ctrl.GetInsertionPoint()
            ctrl.ChangeValue(value)
            ctrl.SetInsertionPoint(insertPoint)
            
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

        ctrl.SetBackgroundColour("white")
        ctrl.Refresh()
        event.Skip()

    #Reset the time ctrl to "00:00" by pressing 'R'
    def OnResetTime(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('R'):
            ctrl = event.GetEventObject()
            ctrl.SetValue("00:00")
        event.Skip()

    #hint button on corrected MGH
    def OnCMGHBtn(self, event):
        dlg = wx.MessageDialog(self, self.correctMGHBtnHint, 'Hint', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return

    #hint button on uncertainty infomation
    def OnUncertaintyInfoBtn(self, event):
        dlg = wx.MessageDialog(self, self.uncertaintyInfoMsg, 'Uncertainty Value Description', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return


    # 3 sig if v < 0.1 m/s else 3 dec
    def OnMeanVel(self, event):
        if event.GetEventObject().GetValue() == "":
            event.Skip()
            return
        if float(event.GetEventObject().GetValue()) < 0.1:
            NumberControl.Round3(event)
        else:
            NumberControl.Sig3(event)
        event.Skip()

    # 3 sig if v < 0.1 m/s else 4 dec
    def OnDischarge(self, event):
        if event.GetEventObject().GetValue() == "":
            event.Skip()
            return
        if float(event.GetEventObject().GetValue()) < 0.1:
            NumberControl.Round4(event)
        else:
            NumberControl.Sig3(event)
            
        event.Skip()


    def IncompleteTimeCheck(self):
        startHour = self.startTimeCtrl.GetHourVal()
        startMinute = self.startTimeCtrl.GetMinuteVal()
        endHour = self.endTimeCtrl.GetHourVal()
        endMinute = self.endTimeCtrl.GetMinuteVal()

        if startHour != '' or startMinute != '' or endHour != '' or endMinute != '':
            if startHour == '' or startMinute == '' or endHour == '' or endMinute == '':
                return True
        return False


    def UpdateMGHCtrl(self, event):
        val = self.mghCmbo.GetValue()
        if val != "":
            val = val.split("  ")[0]
        
        self.mghCtrl.SetValue(val)

        if self.manager is not None:
            self.manager.OnUpdateHGQValues()

    def do_nothing(self,evt):
          pass



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 140))
    DischargeMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()

