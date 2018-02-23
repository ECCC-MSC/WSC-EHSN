import wx
import wx.lib.masked as masked
# import wx.combo as cb
from wx import ComboPopup
import DropdownTime


"""
A simple test case for wx.ComboCtrl using a wx.ListCtrl for the popup
"""

import wx
import NumberControl


#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

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
    
class MeasurementResultsPanel(wx.Panel):
    def __init__(self, mode, lang, *args, **kwargs):
        super(MeasurementResultsPanel, self).__init__(*args, **kwargs)

        self.timeLevelsTxtLbl = "Logger"
        self.sensorRefTxtLbl = "Sensor Reference"
        self.observedValTxtLbl = "Observed Value"
        self.sensorValTxtLbl = "Sensor Value"
        self.timeHeaderTxtLbl = "Time"

        self.observedTimeLbl = "Observed Time"
        self.loggerTimeLbl = "Logger Time"

        self.loggerTimeTxtLbl = "Logger"
        self.loggers = ["HG", "HG2"]
        self.remarkTxtLbl = "Remarks"
        self.remarkChoice = ["Reset"]

        
        self.sensorRef = ['Atmos Pres',
                          'Battery Voltage Under Load',
                          'Internal Temp',
                          'Lake Area',
                          'Lake Stage',
                          'Open Water Extent',
                          'Precip',
                          'R Ice Cover',
                          'R Ice Cover Extent',
                          'Reflective Power',
                          'Salinity',
                          'Sediment Load',
                          'Sediment Transport Rate',
                          'Signal Strength',
                          'Snow Cover',
                          'Snow Depth',
                          'Solar Panel Voltage',
                          'Sound Vel In Water',
                          'Water Velocity']

        self.lang = lang
        self.mode = mode
        self.manager = None


        self.InitUI()

    def InitUI(self):
        if self.mode=="DEBUG":
            print "In MeasurementResultsPanel"
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.SetSizer(mainSizer)

        layoutSizer = wx.GridSizer(rows=4, cols=5, hgap=0, vgap=0)
        self.locale =  wx.Locale(self.lang)
        
        #Time stuff
        timeSizer = wx.BoxSizer(wx.HORIZONTAL)
        timePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        timePanel.SetSizer(timeSizer)

        timeTxt = wx.StaticText(timePanel, label=self.timeLevelsTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        timeSizer.Add(timeTxt, 1, wx.EXPAND)
        # self.timeCtrl = masked.TimeCtrl(self, displaySeconds=False, size=(200, 30), style=wx.TE_CENTRE, fmt24hr = True)
        # self.timeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        # self.timeCtrl.SetValue(wx.DateTime_Now().FormatTime())

        #Time Header
        timeHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeHeaderPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        timeHeaderPanel.SetSizer(timeHeaderSizer)

        timeHeaderText = wx.StaticText(timeHeaderPanel, label=self.timeHeaderTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        timeHeaderSizer.Add(timeHeaderText, 1, wx.EXPAND)


        #Sensor Ref
        sensorRefSizer = wx.BoxSizer(wx.HORIZONTAL)
        sensorRefPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        sensorRefPanel.SetSizer(sensorRefSizer)

        sensorRefTxt = wx.StaticText(sensorRefPanel, label=self.sensorRefTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        sensorRefSizer.Add(sensorRefTxt, 1, wx.EXPAND)

        #Empty Panel
        blankPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)


        #Observed Val
        observedValSizer = wx.BoxSizer(wx.HORIZONTAL)
        observedValPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        observedValPanel.SetSizer(observedValSizer)

        observedValTxt = wx.StaticText(observedValPanel, label=self.observedValTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        observedValSizer.Add(observedValTxt, 1, wx.EXPAND)

        
        #Sensor Val
        sensorValSizer = wx.BoxSizer(wx.HORIZONTAL)
        sensorValPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        sensorValPanel.SetSizer(sensorValSizer)

        sensorValTxt = wx.StaticText(sensorValPanel, label=self.sensorValTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        sensorValSizer.Add(sensorValTxt, 1, wx.EXPAND)


        #Time Ctrl1
        self.timeCtrlPanel1 = DropdownTime.DropdownTime(False, self, style=wx.SIMPLE_BORDER)

        #Time Ctrl2
        self.timeCtrlPanel2 = DropdownTime.DropdownTime(False, self, style=wx.SIMPLE_BORDER)

        #Time Ctrl3
        self.timeCtrlPanel3 = DropdownTime.DropdownTime(False, self, style=wx.SIMPLE_BORDER)

        #Time Ctrl4
        self.timeCtrlPanel4 = DropdownTime.DropdownTime(False, self, style=wx.SIMPLE_BORDER)

        #Time Ctrl5
        self.timeCtrlPanel5 = DropdownTime.DropdownTime(False, self, style=wx.SIMPLE_BORDER)




        #SensorRef/Observed Vals
        self.sensorRefEntry1 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        self.popup1 = ListCtrlComboPopup(self, self.sensorRefEntry1)
        self.popup1.AppendItems(self.sensorRef)
        self.sensorRefEntry1.SetPopupControl(self.popup1)
        self.sensorRefEntry1.SetPopupMinWidth(150)
        # self.sensorRefEntry1 = wx.ComboCtrl(self, style=wx.CB_SORT|wx.TE_LEFT, size=(20, 30))
        # self.sensorRefEntry1Popup = ComboCtrlPopup()
        # self.sensorRefEntry1.SetPopupControl(ComboPopupself.sensorRefEntry1Popup)
        # self.sensorRefEntry1Popup.AddItems(self.sensorRef)
        # self.sensorRefEntry1.SetPopupMinWidth(150)
        
        self.observedVal1 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.observedVal1.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.sensorVal1 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.sensorVal1.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        #col2
        self.sensorRefEntry2 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        self.popup2 = ListCtrlComboPopup(self, self.sensorRefEntry2)
        self.popup2.AppendItems(self.sensorRef)
        self.sensorRefEntry2.SetPopupControl(self.popup2)
        self.sensorRefEntry2.SetPopupMinWidth(150)
        # self.sensorRefEntry2 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # self.sensorRefEntry2Popup = ComboCtrlPopup()
        # self.sensorRefEntry2.SetPopupControl(self.sensorRefEntry2Popup)
        # self.sensorRefEntry2Popup.AddItems(self.sensorRef)
        # self.sensorRefEntry2.SetPopupMinWidth(150)
        
        self.observedVal2 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.observedVal2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.sensorVal2 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.sensorVal2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        #col3
        self.sensorRefEntry3 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        self.popup3 = ListCtrlComboPopup(self, self.sensorRefEntry3)
        self.popup3.AppendItems(self.sensorRef)
        self.sensorRefEntry3.SetPopupControl(self.popup3)
        self.sensorRefEntry3.SetPopupMinWidth(150)
        # self.sensorRefEntry3 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # self.sensorRefEntry3Popup = ComboCtrlPopup()
        # self.sensorRefEntry3.SetPopupControl(self.sensorRefEntry3Popup)
        # self.sensorRefEntry3Popup.AddItems(self.sensorRef)
        # self.sensorRefEntry3.SetPopupMinWidth(150)
        
        self.observedVal3 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.observedVal3.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.sensorVal3 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.sensorVal3.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        
        #Col4
        self.sensorRefEntry4 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        self.popup4 = ListCtrlComboPopup(self, self.sensorRefEntry4)
        self.popup4.AppendItems(self.sensorRef)
        self.sensorRefEntry4.SetPopupControl(self.popup4)
        self.sensorRefEntry4.SetPopupMinWidth(150)
        # self.sensorRefEntry4 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # self.sensorRefEntry4Popup = ComboCtrlPopup()
        # self.sensorRefEntry4.SetPopupControl(self.sensorRefEntry4Popup)
        # self.sensorRefEntry4Popup.AddItems(self.sensorRef)
        # self.sensorRefEntry4.SetPopupMinWidth(150)
        
        self.observedVal4 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.observedVal4.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.sensorVal4 = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        self.sensorVal4.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        # #col5
        # self.sensorRefEntry5 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # self.popup5 = ListCtrlComboPopup(self, self.sensorRefEntry5)
        # self.popup5.AppendItems(self.sensorRef)
        # self.sensorRefEntry5.SetPopupControl(self.popup5)
        # self.sensorRefEntry5.SetPopupMinWidth(150)
        # # self.sensorRefEntry5 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # # self.sensorRefEntry5Popup = ComboCtrlPopup()
        # # self.sensorRefEntry5.SetPopupControl(self.sensorRefEntry5Popup)
        # # self.sensorRefEntry5Popup.AddItems(self.sensorRef)
        # # self.sensorRefEntry5.SetPopupMinWidth(150)
        
        # self.observedVal5 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        # self.sensorVal5 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))

        # #col6
        # self.sensorRefEntry6 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # self.popup6 = ListCtrlComboPopup(self, self.sensorRefEntry6)
        # self.popup6.AppendItems(self.sensorRef)
        # self.sensorRefEntry6.SetPopupControl(self.popup6)
        # self.sensorRefEntry6.SetPopupMinWidth(150)
        # # self.sensorRefEntry6 = wx.ComboCtrl(self, style=wx.CB_SORT, size=(20, 30))
        # # self.sensorRefEntry6Popup = ComboCtrlPopup()
        # # self.sensorRefEntry6.SetPopupControl(self.sensorRefEntry6Popup)
        # # self.sensorRefEntry6Popup.AddItems(self.sensorRef)
        # # self.sensorRefEntry6.SetPopupMinWidth(150)
        
        # self.observedVal6 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        # self.sensorVal6 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(20, 30))
        
        
        #Row 1
        # layoutSizer.Add(timePanel, 0, wx.EXPAND)
        layoutSizer.Add(sensorRefPanel, 0, wx.EXPAND)
        
        layoutSizer.Add(self.sensorRefEntry1, 0, wx.EXPAND)
        layoutSizer.Add(self.sensorRefEntry2, 0, wx.EXPAND)
        
        layoutSizer.Add(self.sensorRefEntry3, 0, wx.EXPAND)
        layoutSizer.Add(self.sensorRefEntry4, 0, wx.EXPAND)
        
        # layoutSizer.Add(self.sensorRefEntry5, 0, wx.EXPAND)
        # layoutSizer.Add(self.sensorRefEntry6, 0, wx.EXPAND)


        #Row 2
        

        layoutSizer.Add(timeHeaderPanel, 0, wx.EXPAND)
        layoutSizer.Add(self.timeCtrlPanel1, 0, wx.EXPAND)
        layoutSizer.Add(self.timeCtrlPanel2, 0, wx.EXPAND)

        layoutSizer.Add(self.timeCtrlPanel3, 0, wx.EXPAND)
        layoutSizer.Add(self.timeCtrlPanel4, 0, wx.EXPAND)

        # layoutSizer.Add(self.timeCtrlPanel5, 0, wx.EXPAND)
        # layoutSizer.Add(timeCtrlPanel6, 0, wx.EXPAND)
        
        #Row 3
        # layoutSizer.Add(self.timeCtrl, 0, wx.EXPAND)
        layoutSizer.Add(observedValPanel, 0, wx.EXPAND)

        layoutSizer.Add(self.observedVal1, 0, wx.EXPAND)
        layoutSizer.Add(self.observedVal2, 0, wx.EXPAND)

        layoutSizer.Add(self.observedVal3, 0, wx.EXPAND)
        layoutSizer.Add(self.observedVal4, 0, wx.EXPAND)

        # layoutSizer.Add(self.observedVal5, 0, wx.EXPAND)
        # layoutSizer.Add(self.observedVal6, 0, wx.EXPAND)

        #Row 4
        # layoutSizer.Add(blankPanel, 0, wx.EXPAND)
        layoutSizer.Add(sensorValPanel, 0, wx.EXPAND)

        layoutSizer.Add(self.sensorVal1, 0, wx.EXPAND)
        layoutSizer.Add(self.sensorVal2, 0, wx.EXPAND)

        layoutSizer.Add(self.sensorVal3, 0, wx.EXPAND)
        layoutSizer.Add(self.sensorVal4, 0, wx.EXPAND)

        # layoutSizer.Add(self.sensorVal5, 0, wx.EXPAND)
        # layoutSizer.Add(self.sensorVal6, 0, wx.EXPAND)


        loggerTimeTablePanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        loggerTimeTableSizer = wx.GridSizer(rows=4, cols=3, hgap=0, vgap=0)
        loggerTimeTablePanel.SetSizer(loggerTimeTableSizer)


        #Logger Time
        loggerTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        loggerTimePanel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        loggerTimePanel.SetSizer(loggerTimeSizer)

        loggerTimeText = wx.StaticText(loggerTimePanel, label=self.loggerTimeTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        loggerTimeSizer.Add(loggerTimeText, 1, wx.EXPAND)

        #Col1
        col1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        col1Panel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        col1Panel.SetSizer(col1Sizer)

        self.col1Combo = wx.ComboBox(col1Panel, style=wx.CB_DROPDOWN, choices=self.loggers)
        col1Sizer.Add(self.col1Combo, 1, wx.EXPAND)


        #Col2
        col2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        col2Panel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        col2Panel.SetSizer(col2Sizer)

        self.col2Combo = wx.ComboBox(col2Panel, style=wx.CB_DROPDOWN, choices=self.loggers)
        col2Sizer.Add(self.col2Combo, 1, wx.EXPAND)

        #Time label
        remarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        remarkPanel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        remarkPanel.SetSizer(remarkSizer)

        remarkeText = wx.StaticText(remarkPanel, label=self.remarkTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        remarkSizer.Add(remarkeText, 1, wx.EXPAND)


        #Reset Column 1
        reset1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        reset1Panel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        reset1Panel.SetSizer(reset1Sizer)

        self.reset1Combo = wx.ComboBox(reset1Panel, style=wx.CB_DROPDOWN, choices=self.remarkChoice)
        reset1Sizer.Add(self.reset1Combo, 1, wx.EXPAND)

        #Reset Column 2
        reset2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        reset2Panel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        reset2Panel.SetSizer(reset2Sizer)

        self.reset2Combo = wx.ComboBox(reset2Panel, style=wx.CB_DROPDOWN, choices=self.remarkChoice)
        reset2Sizer.Add(self.reset2Combo, 1, wx.EXPAND)

        #Oberserved label
        observedSizer = wx.BoxSizer(wx.HORIZONTAL)
        observedPanel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        observedPanel.SetSizer(observedSizer)

        observedeText = wx.StaticText(observedPanel, label=self.observedTimeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        observedSizer.Add(observedeText, 1, wx.EXPAND)

        #Time Ctrl7
        self.timeCtrlPanel7 = DropdownTime.DropdownTime(False, loggerTimeTablePanel, style=wx.SIMPLE_BORDER)


        #Time Ctrl8
        self.timeCtrlPanel8 = DropdownTime.DropdownTime(False, loggerTimeTablePanel, style=wx.SIMPLE_BORDER)


        #Sensor label
        sensorSizer = wx.BoxSizer(wx.HORIZONTAL)
        sensorPanel = wx.Panel(loggerTimeTablePanel, style=wx.SIMPLE_BORDER)
        sensorPanel.SetSizer(sensorSizer)

        sensoreText = wx.StaticText(sensorPanel, label=self.loggerTimeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(50, 30))
        sensorSizer.Add(sensoreText, 1, wx.EXPAND)

        #Time Ctrl9
        self.timeCtrlPanel9 = DropdownTime.DropdownTime(False, loggerTimeTablePanel, style=wx.SIMPLE_BORDER)


        #Time Ctrl10
        self.timeCtrlPanel10 = DropdownTime.DropdownTime(False, loggerTimeTablePanel, style=wx.SIMPLE_BORDER)



        #Row 1
        loggerTimeTableSizer.Add(loggerTimePanel, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(col1Panel, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(col2Panel, 0, wx.EXPAND)

        #Row 2
        loggerTimeTableSizer.Add(remarkPanel, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(reset1Panel, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(reset2Panel, 0, wx.EXPAND)

        #Row 3
        loggerTimeTableSizer.Add(observedPanel, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(self.timeCtrlPanel7, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(self.timeCtrlPanel8, 0, wx.EXPAND)


        #Row 4
        loggerTimeTableSizer.Add(sensorPanel, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(self.timeCtrlPanel9, 0, wx.EXPAND)
        loggerTimeTableSizer.Add(self.timeCtrlPanel10, 0, wx.EXPAND)



        mainSizer.Add(layoutSizer, 2, wx.EXPAND)
        mainSizer.Add(loggerTimeTablePanel, 1, wx.EXPAND)






    # #Time stuff
    # def GetTimeCtrl(self):
    #     return self.timeCtrl.GetValue()

    # def SetTimeCtrl(self, timeCtrl):
    #     date = wx.DateTime()
    #     date.ParseTime(timeCtrl)
    #     self.timeCtrl.SetValue(date)

    #Time vals

    #Hours
    def GetHour1(self):
        return self.timeCtrlPanel1.GetHourVal()
    def SetHour1(self, val):
        self.timeCtrlPanel1.SetHourVal(val)

    def GetHour2(self):
        return self.timeCtrlPanel2.GetHourVal()
    def SetHour2(self, val):
        self.timeCtrlPanel2.SetHourVal(val)

    def GetHour3(self):
        return self.timeCtrlPanel3.GetHourVal()
    def SetHour3(self, val):
        self.timeCtrlPanel3.SetHourVal(val)

    def GetHour4(self):
        return self.timeCtrlPanel4.GetHourVal()
    def SetHour4(self, val):
        self.timeCtrlPanel4.SetHourVal(val)

    def GetHour5(self):
        return self.timeCtrlPanel5.GetHourVal()
    def SetHour5(self, val):
        self.timeCtrlPanel5.SetHourVal(val)


    def GetHour7(self):
        return self.timeCtrlPanel7.GetHourVal()
    def SetHour7(self, val):
        self.timeCtrlPanel7.SetHourVal(val)
    def GetHour8(self):
        return self.timeCtrlPanel8.GetHourVal()
    def SetHour8(self, val):
        self.timeCtrlPanel8.SetHourVal(val)
    def GetHour9(self):
        return self.timeCtrlPanel9.GetHourVal()
    def SetHour9(self, val):
        self.timeCtrlPanel9.SetHourVal(val)
    def GetHour10(self):
        return self.timeCtrlPanel10.GetHourVal()
    def SetHour10(self, val):
        self.timeCtrlPanel10.SetHourVal(val)


    #Minutes
    def GetMinute1(self):
        return self.timeCtrlPanel1.GetMinuteVal()
    def SetMinute1(self, val):
        self.timeCtrlPanel1.SetMinuteVal(val)

    def GetMinute2(self):
        return self.timeCtrlPanel2.GetMinuteVal()
    def SetMinute2(self, val):
        self.timeCtrlPanel2.SetMinuteVal(val)

    def GetMinute3(self):
        return self.timeCtrlPanel3.GetMinuteVal()
    def SetMinute3(self, val):
        self.timeCtrlPanel3.SetMinuteVal(val)

    def GetMinute4(self):
        return self.timeCtrlPanel4.GetMinuteVal()
    def SetMinute4(self, val):
        self.timeCtrlPanel4.SetMinuteVal(val)

    def GetMinute5(self):
        return self.timeCtrlPanel5.GetMinuteVal()
    def SetMinute5(self, val):
        self.timeCtrlPanel5.SetMinuteVal(val)


    def GetMinute7(self):
        return self.timeCtrlPanel7.GetMinuteVal()
    def SetMinute7(self, val):
        self.timeCtrlPanel7.SetMinuteVal(val)
    def GetMinute8(self):
        return self.timeCtrlPanel8.GetMinuteVal()
    def SetMinute8(self, val):
        self.timeCtrlPanel8.SetMinuteVal(val)
    def GetMinute9(self):
        return self.timeCtrlPanel9.GetMinuteVal()
    def SetMinute9(self, val):
        self.timeCtrlPanel9.SetMinuteVal(val)
    def GetMinute10(self):
        return self.timeCtrlPanel10.GetMinuteVal()
    def SetMinute10(self, val):
        self.timeCtrlPanel10.SetMinuteVal(val)


    #Sensor Vals
    def GetSensorRefEntry1(self):
        return self.sensorRefEntry1.GetValue()

    def SetSensorRefEntry1(self, sensorRefEntry1):
        self.sensorRefEntry1.SetValue(sensorRefEntry1)
        
    def GetSensorRefEntry2(self):
        return self.sensorRefEntry2.GetValue()

    def SetSensorRefEntry2(self, sensorRefEntry2):
        self.sensorRefEntry2.SetValue(sensorRefEntry2)
        
    def GetSensorRefEntry3(self):
        return self.sensorRefEntry3.GetValue()

    def SetSensorRefEntry3(self, sensorRefEntry3):
        self.sensorRefEntry3.SetValue(sensorRefEntry3)
        
    def GetSensorRefEntry4(self):
        return self.sensorRefEntry4.GetValue()

    def SetSensorRefEntry4(self, sensorRefEntry4):
        self.sensorRefEntry4.SetValue(sensorRefEntry4)
        
    # def GetSensorRefEntry5(self):
    #     return self.sensorRefEntry5.GetValue()

    # def SetSensorRefEntry5(self, sensorRefEntry5):
    #     self.sensorRefEntry5.SetValue(sensorRefEntry5)
        
    # def GetSensorRefEntry6(self):
    #     return self.sensorRefEntry6.GetValue()

    # def SetSensorRefEntry6(self, sensorRefEntry6):
    #     self.sensorRefEntry6.SetValue(sensorRefEntry6)


    #Observed Val
    def GetObservedVal1(self):
        return self.observedVal1.GetValue()

    def SetObservedVal1(self, observedVal1):
        self.observedVal1.SetValue(observedVal1)
        
    def GetObservedVal2(self):
        return self.observedVal2.GetValue()

    def SetObservedVal2(self, observedVal2):
        self.observedVal2.SetValue(observedVal2)
        
    def GetObservedVal3(self):
        return self.observedVal3.GetValue()

    def SetObservedVal3(self, observedVal3):
        self.observedVal3.SetValue(observedVal3)
        
    def GetObservedVal4(self):
        return self.observedVal4.GetValue()

    def SetObservedVal4(self, observedVal4):
        self.observedVal4.SetValue(observedVal4)
        
    def GetObservedVal5(self):
        return self.observedVal5.GetValue()

    def SetObservedVal5(self, observedVal5):
        self.observedVal5.SetValue(observedVal5)
        
    def GetObservedVal6(self):
        return self.observedVal6.GetValue()

    def SetObservedVal6(self, observedVal6):
        self.observedVal6.SetValue(observedVal6)


    #Sensor Val
    def GetSensorVal1(self):
        return self.sensorVal1.GetValue()
    def SetSensorVal1(self, sensorVal1):
        self.sensorVal1.SetValue(sensorVal1)
        
    def GetSensorVal2(self):
        return self.sensorVal2.GetValue()
    def SetSensorVal2(self, sensorVal2):
        self.sensorVal2.SetValue(sensorVal2)
        
    def GetSensorVal3(self):
        return self.sensorVal3.GetValue()
    def SetSensorVal3(self, sensorVal3):
        self.sensorVal3.SetValue(sensorVal3)
        
    def GetSensorVal4(self):
        return self.sensorVal4.GetValue()
    def SetSensorVal4(self, sensorVal4):
        self.sensorVal4.SetValue(sensorVal4)
        
    def GetSensorVal5(self):
        return self.sensorVal5.GetValue()
    def SetSensorVal5(self, sensorVal5):
        self.sensorVal5.SetValue(sensorVal5)
        
    def GetSensorVal6(self):
        return self.sensorVal6.GetValue()
    def SetSensorVal6(self, sensorVal6):
        self.sensorVal6.SetValue(sensorVal6)





    #Reset the time ctrl to "00:00" by pressing 'R'
    def OnResetTime(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('R'):
            ctrl = event.GetEventObject()
            ctrl.SetValue("00:00")
        event.Skip()








def main():
    app = wx.App()

    frame = wx.Frame(None, size=(500, 200))
    MeasurementResultsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame)

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
