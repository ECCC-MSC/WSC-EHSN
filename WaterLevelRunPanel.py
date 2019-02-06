# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from WaterLevelNotesPanel import *
import wx.lib.masked as masked
import wx.lib.scrolledpanel as scrolledpanel
# import wx.combo as cb
# import wx.lib.agw.flatnotebook as fnb
from wx import ComboPopup
import sys
import os
import NumberControl
from DropdownTime import *



class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""
# from ElevationTransferFrame import *

#----------------------------------------------------------------------
# This class is used to provide an interface between a ComboCtrl and the
# ListCtrl that is used as the popoup for the combo widget.

class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

class ListCtrlComboPopup(wx.ComboPopup):

    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None

    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


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


class WaterLevelRunPanel(wx.Panel):

    def __init__(self, mode, lang, dir, *args, **kwargs):
        super(WaterLevelRunPanel, self).__init__(*args, **kwargs)

        self.levelNotesLbl = "Level Notes"
        self.timeLbl = "Time"
        self.WLRefLbl = "WL Reference Point"
        self.elevationLbl = "Established Elevation (m)"
        self.DtWSLbl = "Distance to Water Surface (+/- m)"
        self.upDownLbl = "Up to/Down to Water Surface"
        self.surgeLbl = "Surge (+/- m)/ Comment"
        self.WLElevLbl = "Water Level Elevation"
        self.commentsLbl = "Comments"
        self.completedByLbl = "Completed by"
        self.datumLbl = "Datum (m)"
        self.loggerLbl = "HG"
        self.loggerLbl2 = "HG2"
        self.cwlLbl = "Corrected Water Level"
        self.hintLbl = "Transfer selected elevation and reference station to Direct Water Level table"
        self.correctCmtBtnHint = 'Please note that these comments are uploaded to the to "Activity Remarks Management" section of Leveling Activity in AQUARIUS' \
                + 'and these comments are also printed for Benchmark History Report.'
        self.transferSumLbl = "Transfer to Front Page"
        self.transferConfirmationMsg = "Corrected water level  and logger values have been transfered"
        self.transferToFrontHintLbl = "Transfer to front page"
        self.emptyDWLMessage = "You should check at least one Water Level Reference Point."
        self.overMaxDWLMessage = "Cannot have more than 2 selected WL References"
        self.duplicateWLRMessage = "Different WL Reference Points cannot be mapped to the same field on Front Page"
        self.duplicateColMessage = "WL elevations from the same WL Reference Point cannot be mapped to two fields on Front Page"
        self.nameTransferMessage = "Either empty or conflict WL Reference/Logger header names are detected. Do you want to overwrite these names?"
        self.emptyTimeMessage = "Invalid time input!"
        self.changeLvlMethodMessage = "Selecting this will automatically deselect the other leveling method, and this will cause changes to the calculated values in the Level Notes page. Are you sure you want to change the levelling method?"
        self.transferLbl = "Transfer Elevations to DWL Table"
        self.transferToFrontLbl = "Transfer to Front Page Stage Table"
        self.wls = ["", "WLR1", "WLR2"]
        self.hgs = ["", "HG", "HG2"]
        self.addRunButLbl = "Add Circuit"
        self.miniFrame = None
        self.dir = dir
        if hasattr(sys, '_MEIPASS'):
            self.myBitmap = os.path.join(sys._MEIPASS, "downarrow.png")
            self.myBitmapFront = os.path.join(sys._MEIPASS, "backarrow.png")
        else:

            self.myBitmap = self.dir + "\\" + "downarrow.png"
            self.myBitmapFront = self.dir + "\\" + "backarrow.png"

        self.picture = wx.Image(self.myBitmap, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.transToFrontpicture = wx.Image(self.myBitmapFront, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.rb1Lbl = "Conventional Levelling"
        self.rb2Lbl = "Total Station"
        # self.rb3Lbl = "Both"
        # self.levelNoteToolTipDesc = "Note: Aggregation of the Foresight and/or Backsight measurements may be needed externally before entering the values" \
        #         + " in eHSN when levelling a wire-weight gauge (e.g. when sight on the grooves of weight and WWG reading are used) or a staff gauge" \
        #         + " (e.g. when more than one rod is used for measurements) is performed."
        self.upDownVals = ["Up to", "Down to"]
        self.BMs = []

        self.buttonWidth = 80
        self.buttonHeight = 50
        self.entryNum = 0

        self.colHeaderHeight = 60
        self.colHeaderWidth = 48
        self.rowHeight = 30

        self.manager = None
        self.mode = mode
        self.lang = lang

        self.InitUI()


    def InitUI(self):
        if self.mode == "DEBUG":
            print "WaterLevelRunPanel"

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.locale = wx.Locale(self.lang)


        #Setup scroll panel
        self.WLRScroll = scrolledpanel.ScrolledPanel(self, style=wx.SIMPLE_BORDER)
        self.WLRScroll.SetupScrolling()
        # self.WLRScroll.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        #Title
        self.titlePanel = wx.Panel(self.WLRScroll, style=wx.SIMPLE_BORDER)

        levelNotesTxt = wx.StaticText(self.titlePanel, label=self.levelNotesLbl, name="-1")
        # levelNotesTxt.SetToolTip(wx.ToolTip(self.levelNoteToolTipDesc))
        levelNotesTxt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        # dummyTxt=wx.StaticText(self.titlePanel, name="-1")


        self.rb1 = wx.RadioButton(self.titlePanel, -1, self.rb1Lbl, (10, 10),style = wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.titlePanel, -1, self.rb2Lbl, (10, 10))
        # self.rb3 = wx.RadioButton(self.titlePanel, -1, self.rb3Lbl, (10, 10))
        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.OnChangeLevelType)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.OnChangeLevelType)

        titleSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(self.rb1, 0, wx.EXPAND)
        titleSizer.Add(self.rb2, 0, wx.EXPAND)

        # titleSizer.Add(self.rb3, 0, wx.EXPAND)
        titleSizer.Add(levelNotesTxt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 150)
        # titleSizer.Add(dummyTxt, 1, wx.EXPAND)

        self.titlePanel.SetSizer(titleSizer)

        #Sizer holds Title and Runs
        levelNotesSizer = wx.BoxSizer(wx.VERTICAL)

        self.splitter = wx.SplitterWindow(self.WLRScroll, style=wx.SP_3D|wx.SP_THIN_SASH|wx.SP_BORDER|wx.SP_NO_XP_THEME, size=(1, 410))

        #Panel parent to table
        # self.runTablePanel = scrolledpanel.ScrolledPanel(self.WLRScroll, style=wx.BORDER_NONE, size=(1, 120))
        self.runTablePanel = wx.Panel(self.splitter, style=wx.BORDER_NONE)


        runSizer = wx.BoxSizer(wx.VERTICAL)
        self.runTablePanel.SetSizer(runSizer)


        # self.levelNoteTab = fnb.FlatNotebook(self.runTablePanel, style=wx.NB_TOP, agwStyle=fnb.FNB_ALLOW_FOREIGN_DND|fnb.FNB_FANCY_TABS|\
        #     fnb.FNB_DCLICK_CLOSES_TABS|fnb.FNB_FF2)



        #Level Notes Table
        self.levelNotes = WaterLevelNotesPanel(self.mode, True, 20, self, self.runTablePanel, style=wx.BORDER_NONE, size=(-1,1))

        self.secondSplitPanel = wx.Panel(self.splitter)
        secondSplitSizer = wx.BoxSizer(wx.VERTICAL)
        self.secondSplitPanel.SetSizer(secondSplitSizer)

        bar = wx.Panel(self.secondSplitPanel, size=(1, 3))
        bar.SetBackgroundColour('green')


        addRunSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondSplitSizer.Add(bar, 0, wx.EXPAND)
        secondSplitSizer.Add(addRunSizer, 0, wx.EXPAND)

        self.addRunButton = wx.Button(self.secondSplitPanel, label=self.addRunButLbl, size=(-1, 50))
        self.addRunButton.Bind(wx.EVT_BUTTON, self.levelNotes.OnAddRun)

        self.transferSizer = wx.BoxSizer(wx.HORIZONTAL)
        addRunSizer.Add(self.transferSizer, 5, wx.EXPAND|wx.ALL, 5)
        addRunSizer.Add(self.addRunButton, 0, wx.RIGHT, 5)





        #Adding transfer button to transferSizer
        transferBtn = wx.BitmapButton(self.secondSplitPanel, size=(-1, 50), bitmap=self.picture)
        transferBtn.Bind(wx.EVT_BUTTON, self.OnTransferToSummary)

        tooltipTransferToSummary = wx.ToolTip(self.hintLbl)
        tooltipTransferToSummary.SetDelay(10)
        tooltipTransferToSummary.SetAutoPop(30000)
        transferBtn.SetToolTip(tooltipTransferToSummary)

        transferDesc = wx.StaticText(self.secondSplitPanel, label=self.transferLbl)


        self.transferSizer.Add(transferBtn, 0)
        self.transferSizer.Add(transferDesc, 0, wx.TOP, 25)
        # self.levelNotes2 = WaterLevelNotesPanel(self.mode, True, 20, self.levelNoteTab, style=wx.BORDER_NONE, size=(1, 34 + 20*22 + 45))
        # self.levelNotes3 = WaterLevelNotesPanel(self.mode, True, 20, self.levelNoteTab, style=wx.BORDER_NONE, size=(1, 34 + 20*22 + 45))
        # self.levelNotes4 = WaterLevelNotesPanel(self.mode, True, 20, self.levelNoteTab, style=wx.BORDER_NONE, size=(1, 34 + 20*22 + 45))
        # self.levelNotes5 = WaterLevelNotesPanel(self.mode, True, 20, self.levelNoteTab, style=wx.BORDER_NONE, size=(1, 34 + 20*22 + 45))
        # self.levelNotes6 = WaterLevelNotesPanel(self.mode, True, 20, self.levelNoteTab, style=wx.BORDER_NONE, size=(1, 34 + 20*22 + 45))
        # self.levelNoteTab.AddPage(self.levelNotes, "#1")
        # self.levelNoteTab.AddPage(self.levelNotes2, "#2")
        # self.levelNoteTab.AddPage(self.levelNotes3, "#3")
        # self.levelNoteTab.AddPage(self.levelNotes4, "#4")
        # self.levelNoteTab.AddPage(self.levelNotes5, "#5")
        # self.levelNoteTab.AddPage(self.levelNotes6, "#6")


        #Add the levelling notes
        # runSizer.Add(self.levelNoteTab, 0, wx.EXPAND)
        runSizer.Add(self.levelNotes, 1, wx.EXPAND)
        # self.runTablePanel.SetupScrolling()
        # self.runTablePanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)


 ####################################################################

        #Water Level Table
        self.waterLevelPanel = scrolledpanel.ScrolledPanel(self.secondSplitPanel, style=wx.BORDER_NONE)
        self.waterLevelPanel.SetupScrolling()
        self.waterLevelPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        secondSplitSizer.Add(self.waterLevelPanel, 1, wx.EXPAND)

        self.waterLevelSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.waterLevelSizerV = wx.BoxSizer(wx.VERTICAL)


        #Entry Adding Column
        self.entryColumnSizer = wx.BoxSizer(wx.VERTICAL)

        entryColPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        wx.StaticText(entryColPanel, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.rowHeight, self.colHeaderHeight))



        #For dynamically added entries
        self.entryColButtonPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.entryColButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.entryColButtonPanel.SetSizer(self.entryColButtonSizer)

        #Add a default button
        name = "%s" % self.entryNum
        button = wx.Button(self.entryColButtonPanel, id=10101+self.entryNum, label="+", name=name, size=(self.rowHeight, self.rowHeight))
        self.entryNum += 1
        button.Bind(wx.EVT_BUTTON, self.OnAddPress)
        self.entryColButtonSizer.Add(button, 0, wx.EXPAND)

        self.entryColumnSizer.Add(entryColPanel, 0, wx.EXPAND)
        self.entryColumnSizer.Add(self.entryColButtonPanel, 0, wx.EXPAND)

        #Select Column
        self.selectColumnSizer = wx.BoxSizer(wx.VERTICAL)

        selectHeaderPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        selectHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        selectHeaderPanel.SetSizer(selectHeaderSizer)

        selectHeaderTxt = wx.StaticText(selectHeaderPanel, size=(15, self.colHeaderHeight))
        selectHeaderSizer.Add(selectHeaderTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.selectPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.selectSizer = wx.BoxSizer(wx.VERTICAL)
        self.selectPanel.SetSizer(self.selectSizer)

        self.selectColumnSizer.Add(selectHeaderPanel, 0, wx.EXPAND)
        self.selectColumnSizer.Add(self.selectPanel, 0, wx.EXPAND)


        #Time column
        self.timeColumnSizer = wx.BoxSizer(wx.VERTICAL)

        timeLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        timeLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeLabelPanel.SetSizer(timeLabelSizer)

        timeLabelTxt = wx.StaticText(timeLabelPanel, label=self.timeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        timeLabelSizer.Add(timeLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.timeValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.timeValSizer = wx.BoxSizer(wx.VERTICAL)
        self.timeValPanel.SetSizer(self.timeValSizer)

        #Add all to the Time
        self.timeColumnSizer.Add(timeLabelPanel, 0, wx.EXPAND)
        self.timeColumnSizer.Add(self.timeValPanel, 0, wx.EXPAND)


        #WLRef column
        self.WLRefColumnSizer = wx.BoxSizer(wx.VERTICAL)

        WLRefLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        WLRefLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        WLRefLabelPanel.SetSizer(WLRefLabelSizer)

        WLRefLabelTxt = wx.StaticText(WLRefLabelPanel, label=self.WLRefLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        WLRefLabelSizer.Add(WLRefLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.WLRefValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.WLRefValSizer = wx.BoxSizer(wx.VERTICAL)
        self.WLRefValPanel.SetSizer(self.WLRefValSizer)

        #Add all to the Time
        self.WLRefColumnSizer.Add(WLRefLabelPanel, 0, wx.EXPAND)
        self.WLRefColumnSizer.Add(self.WLRefValPanel, 0, wx.EXPAND)


        #Elevation column
        self.elevationColumnSizer = wx.BoxSizer(wx.VERTICAL)

        elevationLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        elevationLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        elevationLabelPanel.SetSizer(elevationLabelSizer)

        elevationLabelTxt = wx.StaticText(elevationLabelPanel, label=self.elevationLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        elevationLabelSizer.Add(elevationLabelTxt, 0, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.elevationValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.elevationValSizer = wx.BoxSizer(wx.VERTICAL)
        self.elevationValPanel.SetSizer(self.elevationValSizer)

        #Add all to the Time
        self.elevationColumnSizer.Add(elevationLabelPanel, 0, wx.EXPAND)
        self.elevationColumnSizer.Add(self.elevationValPanel, 0, wx.EXPAND)


        #Distance to Water Surface column
        self.DtWSColumnSizer = wx.BoxSizer(wx.VERTICAL)

        DtWSLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        DtWSLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        DtWSLabelPanel.SetSizer(DtWSLabelSizer)

        DtWSLabelTxt = wx.StaticText(DtWSLabelPanel, label=self.DtWSLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        DtWSLabelSizer.Add(DtWSLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.DtWSValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.DtWSValSizer = wx.BoxSizer(wx.VERTICAL)
        self.DtWSValPanel.SetSizer(self.DtWSValSizer)

        #Add all to the Time
        self.DtWSColumnSizer.Add(DtWSLabelPanel, 0, wx.EXPAND)
        self.DtWSColumnSizer.Add(self.DtWSValPanel, 0, wx.EXPAND)


        # #UpDown to Water Surface column
        # self.upDownColumnSizer = wx.BoxSizer(wx.VERTICAL)

        # upDownLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        # upDownLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        # upDownLabelPanel.SetSizer(upDownLabelSizer)

        # upDownLabelTxt = wx.StaticText(upDownLabelPanel, label=self.upDownLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        # upDownLabelSizer.Add(upDownLabelTxt, 1, wx.EXPAND)

        # #Create new panel and sizer for dynamic entries
        # self.upDownValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        # self.upDownValSizer = wx.BoxSizer(wx.VERTICAL)
        # self.upDownValPanel.SetSizer(self.upDownValSizer)

        # #Add all to the Time
        # self.upDownColumnSizer.Add(upDownLabelPanel, 0, wx.EXPAND)
        # self.upDownColumnSizer.Add(self.upDownValPanel, 0, wx.EXPAND)


        #WLE column
        self.WLElevColumnSizer = wx.BoxSizer(wx.VERTICAL)

        wleLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        wleLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        wleLabelPanel.SetSizer(wleLabelSizer)

        wleLabelTxt = wx.StaticText(wleLabelPanel, label=self.WLElevLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        wleLabelSizer.Add(wleLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.wleValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.wleValSizer = wx.BoxSizer(wx.VERTICAL)
        self.wleValPanel.SetSizer(self.wleValSizer)

        #Add all to the Time
        self.WLElevColumnSizer.Add(wleLabelPanel, 0, wx.EXPAND)
        self.WLElevColumnSizer.Add(self.wleValPanel, 0, wx.EXPAND)





        #Datum column
        self.datumColumnSizer = wx.BoxSizer(wx.VERTICAL)

        datumLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        datumLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        datumLabelPanel.SetSizer(datumLabelSizer)

        datumLabelTxt = wx.StaticText(datumLabelPanel, label=self.datumLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        datumLabelSizer.Add(datumLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.datumValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.datumValSizer = wx.BoxSizer(wx.VERTICAL)
        self.datumValPanel.SetSizer(self.datumValSizer)

        #Add all to the Time
        self.datumColumnSizer.Add(datumLabelPanel, 0, wx.EXPAND)
        self.datumColumnSizer.Add(self.datumValPanel, 0, wx.EXPAND)










        #WLElev column
        self.CWLColumnSizer = wx.BoxSizer(wx.VERTICAL)

        cwlLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        cwlLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        cwlLabelPanel.SetSizer(cwlLabelSizer)

        cwlLabelTxt = wx.StaticText(cwlLabelPanel, label=self.cwlLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        cwlLabelSizer.Add(cwlLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.cwlValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.cwlValSizer = wx.BoxSizer(wx.VERTICAL)
        self.cwlValPanel.SetSizer(self.cwlValSizer)

        #Add all to the Time
        self.CWLColumnSizer.Add(cwlLabelPanel, 0, wx.EXPAND)
        self.CWLColumnSizer.Add(self.cwlValPanel, 0, wx.EXPAND)





        #Logger column
        self.loggerColumnSizer = wx.BoxSizer(wx.VERTICAL)

        loggerLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        loggerLabelSizer = wx.BoxSizer(wx.VERTICAL)
        loggerLabelPanel.SetSizer(loggerLabelSizer)

        loggerLabelTxt = wx.StaticText(loggerLabelPanel, label=self.loggerLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth/2, self.colHeaderHeight/2))
        self.hgText = wx.TextCtrl(loggerLabelPanel, style=wx.TE_CENTRE, size=(self.colHeaderWidth/2, self.colHeaderHeight/2))
        loggerLabelSizer.Add(loggerLabelTxt, 1, wx.EXPAND)
        loggerLabelSizer.Add(self.hgText, 1, wx.EXPAND)
        #Create new panel and sizer for dynamic entries
        self.loggerValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.loggerValSizer = wx.BoxSizer(wx.VERTICAL)
        self.loggerValPanel.SetSizer(self.loggerValSizer)

        #Add all to the Time
        self.loggerColumnSizer.Add(loggerLabelPanel, 0, wx.EXPAND)
        self.loggerColumnSizer.Add(self.loggerValPanel, 0, wx.EXPAND)



        #Logger column2
        self.loggerColumnSizer2 = wx.BoxSizer(wx.VERTICAL)

        loggerLabelPanel2 = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        loggerLabelSizer2 = wx.BoxSizer(wx.VERTICAL)
        loggerLabelPanel2.SetSizer(loggerLabelSizer2)

        loggerLabelTxt2 = wx.StaticText(loggerLabelPanel2, label=self.loggerLbl2, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth/2, self.colHeaderHeight/2))
        self.hgText2 = wx.TextCtrl(loggerLabelPanel2, style=wx.TE_CENTRE, size=(self.colHeaderWidth/2, self.colHeaderHeight/2))
        loggerLabelSizer2.Add(loggerLabelTxt2, 1, wx.EXPAND)
        loggerLabelSizer2.Add(self.hgText2, 1, wx.EXPAND)
        #Create new panel and sizer for dynamic entries
        self.loggerValPanel2 = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.loggerValSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.loggerValPanel2.SetSizer(self.loggerValSizer2)

        #Add all to the Time
        self.loggerColumnSizer2.Add(loggerLabelPanel2, 0, wx.EXPAND)
        self.loggerColumnSizer2.Add(self.loggerValPanel2, 0, wx.EXPAND)



        #Surge column
        self.surgeColumnSizer = wx.BoxSizer(wx.VERTICAL)

        surgeLabelPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        surgeLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        surgeLabelPanel.SetSizer(surgeLabelSizer)

        surgeLabelTxt = wx.StaticText(surgeLabelPanel, label=self.surgeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        surgeLabelSizer.Add(surgeLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.surgeValPanel = wx.Panel(self.waterLevelPanel, style=wx.SIMPLE_BORDER)
        self.surgeValSizer = wx.BoxSizer(wx.VERTICAL)
        self.surgeValPanel.SetSizer(self.surgeValSizer)


        #Add all to the Time
        self.surgeColumnSizer.Add(surgeLabelPanel, 0, wx.EXPAND)
        self.surgeColumnSizer.Add(self.surgeValPanel, 0, wx.EXPAND)


        #Add columns to table
        self.waterLevelSizerH.Add(self.entryColumnSizer, 0, wx.EXPAND)
        self.waterLevelSizerH.Add(self.selectColumnSizer, 0, wx.EXPAND)
        self.waterLevelSizerH.Add(self.timeColumnSizer, 0, wx.EXPAND)
        self.waterLevelSizerH.Add(self.WLRefColumnSizer, 2, wx.EXPAND)
        self.waterLevelSizerH.Add(self.elevationColumnSizer, 0, wx.EXPAND)
        self.waterLevelSizerH.Add(self.DtWSColumnSizer, 1, wx.EXPAND)
        # self.waterLevelSizerH.Add(self.upDownColumnSizer, 1, wx.EXPAND)
        self.waterLevelSizerH.Add(self.WLElevColumnSizer, 1, wx.EXPAND)
        self.waterLevelSizerH.Add(self.datumColumnSizer, 1, wx.EXPAND)
        self.waterLevelSizerH.Add(self.CWLColumnSizer, 2, wx.EXPAND)
        self.waterLevelSizerH.Add(self.loggerColumnSizer, 1, wx.EXPAND)
        self.waterLevelSizerH.Add(self.loggerColumnSizer2, 1, wx.EXPAND)
        self.waterLevelSizerH.Add(self.surgeColumnSizer, 3, wx.EXPAND)


        self.waterLevelSizerV.Add(self.waterLevelSizerH, 1, wx.EXPAND)
        self.waterLevelPanel.SetSizer(self.waterLevelSizerV)

        # #transfer button
        # transferSumBtn = wx.Button(self.waterLevelPanel, label=self.transferSumLbl, size=(150, 30))
        # transferSumBtn.Bind(wx.EVT_BUTTON, self.OnTransferToFront)

        # self.waterLevelSizerV.Add(transferSumBtn, 0)


        #Adding transfer button which transfer logger value to front page
        transferSumBtn = wx.BitmapButton(self.waterLevelPanel, size=(-1, 50), bitmap=self.transToFrontpicture)
        transferToFrontDesc = wx.StaticText(self.waterLevelPanel, size=(-1, 50), label=self.transferToFrontLbl)
        transferSumBtn.Bind(wx.EVT_BUTTON, self.OnTransferToFront)

        tooltipTransferToFront = wx.ToolTip(self.transferToFrontHintLbl)
        tooltipTransferToFront.SetDelay(10)
        tooltipTransferToFront.SetAutoPop(30000)
        transferSumBtn.SetToolTip(tooltipTransferToFront)

        transferToFrontSizerH = wx.BoxSizer(wx.HORIZONTAL)
        transferToFrontSizerH.Add(transferSumBtn, 0, wx.LEFT, 5)
        transferToFrontSizerH.Add(transferToFrontDesc, 0, wx.TOP, 25)

        self.waterLevelSizerV.Add(transferToFrontSizerH, 0, wx.LEFT, 5)








        #comments
        commentsPanel = wx.Panel(self.WLRScroll, style=wx.BORDER_NONE, size=(-1, 75))
        commentsSizer = wx.BoxSizer(wx.HORIZONTAL)
        commentsPanel.SetSizer(commentsSizer)

        commentsTxt = wx.StaticText(commentsPanel, label=self.commentsLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        correctCmtButton = wx.Button(commentsPanel, size=(15, 20), label="!")
        correctCmtButton.SetForegroundColour('red')
        correctCmtButton.Bind(wx.EVT_BUTTON, self.OnCmtBtn)

        commentsSizer.Add(commentsTxt, 0, wx.EXPAND|wx.LEFT, 5)
        commentsSizer.Add(correctCmtButton, 0, wx.RIGHT, 5)

        self.commentsCtrl = wx.TextCtrl(commentsPanel, style=wx.TE_MULTILINE|wx.TE_BESTWRAP)
        # self.commentsCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        commentsSizer.Add(self.commentsCtrl, 1, wx.EXPAND|wx.ALL, 5)

        completedByPanel = wx.Panel(self.WLRScroll, style=wx.BORDER_NONE, size=(-1, 30))
        completedBySizer = wx.BoxSizer(wx.HORIZONTAL)
        completedByPanel.SetSizer(completedBySizer)

        completedByTxt = wx.StaticText(completedByPanel, label=self.completedByLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        completedBySizer.Add(completedByTxt, 0, wx.EXPAND|wx.LEFT, 5)

        self.completedByCtrl = wx.TextCtrl(completedByPanel, style=wx.TE_MULTILINE|wx.TE_BESTWRAP)
        completedBySizer.Add(self.completedByCtrl, 1, wx.EXPAND|wx.ALL, 5)

        self.splitter.SplitHorizontally(self.runTablePanel, self.secondSplitPanel, 280)
        self.splitter.SetMinimumPaneSize(2)



        #Add to the Bigger Sizer
        # levelNotesSizer.Add(levelNotesTxt, 0, wx.EXPAND)
        levelNotesSizer.Add(self.titlePanel, 0, wx.EXPAND)
        levelNotesSizer.Add(self.splitter, 1, wx.EXPAND)
        # levelNotesSizer.Add(self.runTablePanel, 2, wx.EXPAND)
        # levelNotesSizer.Add(self.waterLevelPanel, 1, wx.EXPAND)
        levelNotesSizer.Add((-1, 10), 0, wx.EXPAND)
        levelNotesSizer.Add(commentsPanel, 0, wx.EXPAND)
        levelNotesSizer.Add(completedByPanel, 0, wx.EXPAND)
        levelNotesSizer.Add((-1, 5), 0, wx.EXPAND)


        self.WLRScroll.SetSizer(levelNotesSizer)


        self.layoutSizer.Add(self.WLRScroll, 1, wx.EXPAND)
        self.SetSizer(self.layoutSizer)


        runSizer.Layout()
        levelNotesSizer.Layout()
        self.layoutSizer.Layout()
        self.Update()
        self.Refresh()

    #convert to upper case
    def OnTextType(self, event):
        textCtr=event.GetEventObject()
        point = textCtr.GetInsertionPoint()
        textCtr.ChangeValue(unicode.upper(textCtr.GetValue()))
        textCtr.SetInsertionPoint(point)

    # On '+' button click, add a new entry into the Level Notes Summary
    def OnAddPress(self, e):
        if self.mode == "DEBUG":
            print "add"

        self.AddEntry()



    def do_nothing(self,evt):
          pass

    # Adds a row to the Level Notes Summary
    # Add a new item in each of the column sizers
    # set name based on entryNum
    # name is used for deletion and ordering
    def AddEntry(self):
        name = "%s" % self.entryNum
        otherName = "%s" % (self.entryNum - 1)
        newButton = wx.Button(self.entryColButtonPanel, id=10101 + self.entryNum, label="+", name=name, size=(self.rowHeight, self.rowHeight))

        oldButton = self.entryColButtonSizer.GetItem(self.entryNum - 1).GetWindow()
        oldButton.SetLabel('-')
        oldButton.Bind(wx.EVT_BUTTON, self.OnRemovePress)

        self.entryNum += 1
        newButton.Bind(wx.EVT_BUTTON, self.OnAddPress)
        self.entryColButtonSizer.Add(newButton, 0, wx.EXPAND)

        #select col
        selectCB = wx.CheckBox(self.selectPanel, name=otherName, size=(15,self.rowHeight))
        # selectCB.MoveAfterInTabOrder(oldButton)
        selectCB.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        # selectCB.SetValue(True)
        self.selectSizer.Add(selectCB, 0, wx.EXPAND)




        #Time col
        # tc = masked.TimeCtrl(self.timeValPanel, size=(self.colHeaderWidth-30, self.rowHeight), displaySeconds=False, name=otherName, style=wx.TE_CENTRE,  fmt24hr=True)
        # # tc.MoveAfterInTabOrder(selectCB)
        # # tc.SetValue(wx.DateTime_Now().FormatTime())
        # tc.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)

        tc = DropdownTime(False, self.timeValPanel, size=(-1, self.rowHeight), name=otherName)
        self.timeValSizer.Add(tc, 0, wx.EXPAND)

        #WLReference point col
        # wlRef = wx.TextCtrl(self.WLRefValPanel, size = (self.colHeaderWidth, self.rowHeight), name = otherName)

        wlRef = wx.ComboCtrl(self.WLRefValPanel, size = (self.colHeaderWidth, self.rowHeight), name = otherName)
        # wlRef.MoveAfterInTabOrder(tc)
        wlRef.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        wlRefCmboCmboPopup = ListCtrlComboPopup()
        wlRef.SetPopupControl(wlRefCmboCmboPopup)
        for bm in self.BMs:
            wlRefCmboCmboPopup.AddItem(bm)
        wlRef.SetPopupMinWidth(self.colHeaderWidth)
        wlRef.SetPopupMaxHeight(120)

        wlRef.Bind(wx.EVT_TEXT, self.OnTextType)
        self.WLRefValSizer.Add(wlRef, 1, wx.EXPAND|wx.BOTTOM|wx.TOP)

        #Elevation col
        elev = MyTextCtrl(self.elevationValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # elev.MoveAfterInTabOrder(wlRef)

        elev.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        elev.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        elev.Bind(wx.EVT_KILL_FOCUS, self.OnNumChangeWLE)
        self.elevationValSizer.Add(elev, 0, wx.EXPAND)

        #Dist to Water Surface col
        dist = MyTextCtrl(self.DtWSValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # dist.MoveAfterInTabOrder(elev)

        dist.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        dist.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        dist.Bind(wx.EVT_KILL_FOCUS, self.OnNumChangeWLE)
        self.DtWSValSizer.Add(dist, 0, wx.EXPAND)

        # #UpDown point col
        # updown = wx.ComboBox(self.upDownValPanel, size = (self.colHeaderWidth, self.rowHeight - 8), choices=self.upDownVals, style=wx.CB_READONLY, name = otherName)
        # updown.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        # updown.Bind(wx.EVT_TEXT, self.OnNumChangeWLE)
        # self.upDownValSizer.Add(updown, 1, wx.EXPAND|wx.BOTTOM|wx.TOP, 4)

        #Surge col
        surge = MyTextCtrl(self.surgeValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        self.surgeValSizer.Add(surge, 0, wx.EXPAND)
        # surge.MoveAfterInTabOrder(Logger2)

        #CorrectedWaterLevel col
        correctedWL = MyTextCtrl(self.cwlValPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # correctedWL.MoveAfterInTabOrder(Datum)
        correctedWL.Bind(wx.EVT_TEXT, self.NumberControl)
        correctedWL.Bind(wx.EVT_TEXT, NumberControl.Round3)
        correctedWL.SetBackgroundColour((204,204,204))
        correctedWL.SetForegroundColour((0,0,204))
        cwlCmbo = wx.ComboBox(self.cwlValPanel, choices=self.wls, style=wx.CB_READONLY, name = otherName, size=(50, self.rowHeight))
        # cwlCmbo.MoveAfterInTabOrder(correctedWL)
        cwlCmbo.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        cwlSizer = wx.BoxSizer(wx.HORIZONTAL)
        cwlSizer.Add(correctedWL, 1, wx.EXPAND)
        cwlSizer.Add(cwlCmbo, 1, wx.EXPAND)
        cwlCmbo.Hide()
        self.cwlValSizer.Add(cwlSizer, 0, wx.EXPAND)


        #Datum col
        Datum = MyTextCtrl(self.datumValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # Datum.MoveAfterInTabOrder(Wle)

        Datum.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        Datum.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        Datum.Bind(wx.EVT_KILL_FOCUS, self.OnPressCorrectedWaterLevel)
        Datum.ChangeValue("0.000")

        self.datumValSizer.Add(Datum, 0, wx.EXPAND)

        #Logger col
        Logger = MyTextCtrl(self.loggerValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # Logger.MoveAfterInTabOrder(cwlCmbo)
        Logger.Bind(wx.EVT_TEXT, self.NumberControl)
        Logger.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        Logger.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.loggerValSizer.Add(Logger, 0, wx.EXPAND)

        #Logger col2
        Logger2 = MyTextCtrl(self.loggerValPanel2, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # Logger2.MoveAfterInTabOrder(Logger)
        Logger2.Bind(wx.EVT_TEXT, self.NumberControl)
        Logger2.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        Logger2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.loggerValSizer2.Add(Logger2, 0, wx.EXPAND)


        #wle col
        Wle = MyTextCtrl(self.wleValPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # Wle.MoveAfterInTabOrder(dist)
        Wle.Bind(wx.EVT_TEXT, NumberControl.Round3)
        self.wleValSizer.Add(Wle, 0, wx.EXPAND)
        Wle.Bind(wx.EVT_TEXT, self.OnPressCorrectedWaterLevel)
        Wle.SetBackgroundColour((204,204,204))
        Wle.SetForegroundColour((0,0,204))

        # newButton.MoveAfterInTabOrder(surge)

        self.waterLevelSizerV.Layout()
        self.waterLevelPanel.Update()

        if self.manager is not None:

            selectCB.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            tc.GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            tc.GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)

            wlRef.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            elev.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            dist.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            surge.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            cwlCmbo.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            Datum.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            Logger.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            Logger2.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)





            # self.layoutSizer.Layout()
            # print self.runTablePanel.GetSizer().GetItem(0).GetWindow().GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(0).GetWindow().GetSizer().GetItem(0).GetSizer().GetItem(0).GetSizer().GetItem(1).GetWindow().GetValue()
            # self.runTablePanel.GetSizer().Layout()
        self.timeValSizer.Layout()
        self.Layout()
        self.Update()
        self.Refresh()

    #Reset water level reference bench mark
    def updateBMs(self, items, indexList):

        if len(indexList) > 0:
            updatedItems = []
            for i in range(len(items)):
                if i in indexList:
                    updatedItems.append(items[i])
            items = updatedItems
        else:
            items = []

        if self.entryNum > 0:
            for row in range(self.entryNum-1):
                wlRef = self.GetWLRef(row)
                wlRefCmboCmboPopup = ListCtrlComboPopup()
                wlRef.SetPopupControl(wlRefCmboCmboPopup)
                for bm in items:

                    wlRefCmboCmboPopup.AddItem(bm)
                wlRef.SetPopupMinWidth(self.colHeaderWidth)
                wlRef.SetPopupMaxHeight(120)
            self.BMs = items

            self.WLRefValSizer.Layout()
            self.Update()


    def OnPressCorrectedWaterLevel(self, e):
        self.NumberControl(e)
        obj = e.GetEventObject()
        # self.NumberControl(obj)
        index = int(obj.GetName())
        wle = self.GetWLElevVal(index)
        datum = self.GetDatumVal(index)
        if datum == "":
            self.SetDatumVal(index, "0.000")
            datum = 0
        if (wle != "") and (datum != ""):
            try:
                self.SetCwlVal(index, str(float(wle) - float(datum)))
            except:
                try:
                    self.SetCwlVal(index, str(float(wle)))
                except:
                    self.SetCwlVal(index, "")
        else:
            self.SetCwlVal(index, "")
        e.Skip()


    # #Event to handle constraint on float input
    # def OnNumberControl(self, evt):
    #     self.NumberControl(evt.GetEventObject())

    # #allow only the float number type inputs
    # def NumberControl(self, ctrl):
    #     try:
    #         ctrlVal = float(ctrl.GetValue())
    #         ctrl.preValue = ctrl.GetValue()
    #     except:
    #         if ctrl.GetValue() == '':
    #             ctrl.preValue = ''
    #         elif ctrl.GetValue() == '.':
    #             ctrl.preValue = '.'
    #         elif ctrl.GetValue() == '-':
    #             ctrl.preValue = '-'
    #         elif ctrl.GetValue() == '-.':
    #             ctrl.preValue = '-.'
    #         elif ctrl.GetValue() == '+':
    #             ctrl.preValue = '+'
    #         elif ctrl.GetValue() == '+.':
    #             ctrl.preValue = '+.'
    #         else:
    #             insertPoint = ctrl.GetInsertionPoint() - 1
    #             ctrl.SetValue(ctrl.preValue)
    #             ctrl.SetInsertionPoint(insertPoint)


    def OnNumChangeWLE(self, event):
        self.NumberControl(event)
        textCtr=event.GetEventObject()
        index = int(textCtr.GetName())
        # self.NumberControl(textCtr)
        elevation = self.GetElevationVal(index)
        distance = self.GetDtWSVal(index)
        wle = self.GetWLElevVal(index)
        if (distance == "") or (elevation == ""):
            # try:
            #     self.SetWLElevVal(index, str(float(elevation)))
            # except:
                self.SetWLElevVal(index, "")
        # elif (elevation != "") and (distance != ""):
        else:

                try:
                    self.SetWLElevVal(index, str(float(elevation) + float(distance)))
                except:
                    # try:
                    #     self.SetWLElevVal(index, str(float(elevation)))
                    # except:
                    self.SetWLElevVal(index, "")
        event.Skip()



    def OnTransferToSummary(self, event):
        self.manager.OnTransferToSummary()


    # When the '-' is clicked, remove that row
    def OnRemovePress(self, e):
        #Button col stuff
        button = e.GetEventObject()
        index = int(button.GetName())
        if self.mode=="DEBUG":
            print "index %s" % index
        dlg = wx.MessageDialog(self, "Do you want to remove the entry?", 'Remove',
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
        self.entryColButtonSizer.Hide(index)
        self.entryColButtonSizer.Remove(index)
        self.entryNum -= 1

        #select col stuff
        self.selectSizer.Hide(index)
        self.selectSizer.Remove(index)

        #Time col stuff
        self.timeValSizer.Hide(index)
        self.timeValSizer.Remove(index)

        #WLRef col stuff
        self.WLRefValSizer.Hide(index)
        self.WLRefValSizer.Remove(index)

        #elevation col stuff
        self.elevationValSizer.Hide(index)
        self.elevationValSizer.Remove(index)

        #DtWS col stuff
        self.DtWSValSizer.Hide(index)
        self.DtWSValSizer.Remove(index)

        # #UpDown col stuff
        # self.upDownValSizer.Hide(index)
        # self.upDownValSizer.Remove(index)

        #Surge col stuff
        self.surgeValSizer.Hide(index)
        self.surgeValSizer.Remove(index)

        #WLElev col stuff
        self.cwlValSizer.Hide(index)
        self.cwlValSizer.Remove(index)


        #Datum col stuff
        self.datumValSizer.Hide(index)
        self.datumValSizer.Remove(index)

        #Logger col stuff
        self.loggerValSizer.Hide(index)
        self.loggerValSizer.Remove(index)

        #Logger2 col stuff
        self.loggerValSizer2.Hide(index)
        self.loggerValSizer2.Remove(index)


        #Wle col stuff
        self.wleValSizer.Hide(index)
        self.wleValSizer.Remove(index)


        for index, col in enumerate(self.waterLevelSizerH.GetChildren()):
            for rowIndex, child in enumerate(col.GetSizer().GetItem(1).GetWindow().GetSizer().GetChildren()):

                    if index == 8:
                        i = int(child.GetSizer().GetItem(0).GetWindow().GetName())
                    else:
                        i = int(child.GetWindow().GetName())
                    if i > rowIndex:
                        if index == 8:
                            self.GetCwl(rowIndex).SetName("%s" % (i - 1))
                            self.GetWLCombobox(rowIndex).SetName("%s" % (i - 1))
                        else:
                            child.GetWindow().SetName("%s" % (i - 1))

        self.waterLevelSizerV.Layout()
        self.waterLevelPanel.Update()

        self.layoutSizer.Layout()

        self.Refresh()

        # self.PrintNames()

    #Creating a popup frame to display selected levels to transfer to front page
    def OnTransferToFront(self, evt):
        if not self.manager.TimeCheck():
            dlg = wx.MessageDialog(self, self.emptyTimeMessage, 'None', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()

            return



        if len(self.manager.GetSelectedList()) == 0:
            dlg = wx.MessageDialog(self, self.emptyDWLMessage, 'None', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()

            return
        if len(self.manager.GetSelectedWLRNames()) > 2:
            dlg = wx.MessageDialog(self, self.overMaxDWLMessage, 'None', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()

            return

        wlrConflictCheck, wl1List, wl2List = self.wlrConflictCheck()
        if not wlrConflictCheck:
            dlg = wx.MessageDialog(self, self.duplicateWLRMessage, 'None', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()

            return


        if not self.wlrConflictCheck2():
            dlg = wx.MessageDialog(self, self.duplicateColMessage, 'None', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()

            return
        show = False

        wl1Name = wl1List[0] if len(wl1List) == 1 else ""
        wl2Name = wl2List[0] if len(wl2List) == 1 else ""
        hgName = self.GetHG().GetValue()
        hg2Name = self.GetHG2().GetValue()

        stageMeasManager = self.manager.manager.stageMeasManager
        wl1Stage = stageMeasManager.bmLeft
        wl2Stage = stageMeasManager.bmRight
        hgStage = stageMeasManager.stageLabelCtrl1
        hg2Stage =stageMeasManager.stageLabelCtrl2

        hg = False
        hg2 = False
        wlr1 = False
        wlr2 = False

        counter = 0
        for index, ckbox in enumerate(self.selectSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                counter += 1

        if (counter == 1 and wl1Name == "") or (counter > 1 and (wl1Name == "" or wl2Name == "")):
            dlg = wx.MessageDialog(self, "Water Level Reference column name is not selected, do you want to continue without transfer wlr value?", 'None', wx.YES_NO)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                dlg.Destroy()
            else:
                dlg.Destroy()
                return
        for index, ckbox in enumerate(self.selectSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                resultHG, resultHG2, resultWLR1, resultWLR2 = self.TransferValue(int(ckbox.GetWindow().GetName()))
                show = True
                ckbox.GetWindow().SetValue(False)
                self.RefreshCombobox(index)
                #only overwrite the name if there is a new value given for the column
                if resultHG:
                    hg = resultHG
                if resultHG2:
                    hg2 = resultHG2
                if resultWLR1:
                    wlr1 = resultWLR1
                if resultWLR2:
                    wlr2 = resultWLR2
        if show:

            newWlr1Name = newWlr2Name = newHgName= newHg2Name = ""




            if (hgName != hgStage or hgStage == "")and hg:
                if hgStage != "":
                    dlg = wx.MessageDialog(self, "Overwrite HG name '" + hgStage + "' by the new name '" + hgName + "'?", 'None', wx.YES_NO)
                    res = dlg.ShowModal()
                    if res == wx.ID_YES:

                        newHgName = hgName
                    else:
                        newHgName = hgStage
                    dlg.Destroy()
                else:
                    newHgName = hgName
            if (hg2Name != hg2Stage or hg2Stage == "") and hg2:
                if hg2Stage != "":
                    dlg = wx.MessageDialog(self, "Overwrite HG2 name '" + hg2Stage + "' by the new name '" + hg2Name + "'?", 'None', wx.YES_NO)
                    res = dlg.ShowModal()
                    if res == wx.ID_YES:
                        newHg2Name = hg2Name
                    else:
                        newHg2Name = hg2Stage
                    dlg.Destroy()
                else:
                    newHg2Name = hg2Name
            if (wl1Name != wl1Stage or wl1Stage == "") and wlr1:
                if wl1Stage != "":
                    dlg = wx.MessageDialog(self, "Overwrite WLR1 name '" + wl1Stage + "' by the new name '" + wl1Name + "'?", 'None', wx.YES_NO)
                    res = dlg.ShowModal()
                    if res == wx.ID_YES:

                        newWlr1Name = wl1Name
                    else:
                        newWlr1Name = wl1Stage
                    dlg.Destroy()
                else:
                    newWlr1Name = wl1Name
            if (wl2Name != wl2Stage or wl2Stage == "") and wlr2:
                if wl2Stage != "":
                    dlg = wx.MessageDialog(self, "Overwrite WLR2 name '" + wl2Stage + "' by the new name '" + wl2Name + "'?", 'None', wx.YES_NO)
                    res = dlg.ShowModal()
                    if res == wx.ID_YES:
                        newWlr2Name = wl2Name
                    else:
                        newWlr2Name = wl2Stage
                    dlg.Destroy()
                else:
                    newWlr2Name = wl2Name


            self.TransferName(newWlr1Name, newWlr2Name, newHgName, newHg2Name)
            self.CreateToasterBox(self, self.transferConfirmationMsg, 3000, "#DFD996")



        # if self.miniFrame is None:
        #     self.miniFrame = ElevationTransferFrame(self.mode, self, style=wx.RESIZE_BORDER|wx.CAPTION|wx.STAY_ON_TOP|wx.CLOSE_BOX, size=(650, 300))

    #Transfer column name front summary to front page
    def TransferName(self, wl1, wl2, hg, hg2):

        stageMeasManager = self.manager.manager.stageMeasManager
        if wl1 != "":
            stageMeasManager.bmLeft = wl1
        if wl2 != "":
            stageMeasManager.bmRight = wl2
        if hg != "":
            stageMeasManager.stageLabelCtrl1 = hg
        if hg2 != "":
            stageMeasManager.stageLabelCtrl2 = hg2




    #Check if water level column has two different WL Reference Points
    def wlrConflictCheck(self):
        wl1List = []
        wl2List = []
        for index, ckbox in enumerate(self.selectSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                if self.GetWLCombobox(index).GetValue() == "WLR1":
                    wl1List.append(self.GetWLRefVal(index))
                elif self.GetWLCombobox(index).GetValue() == "WLR2":
                    wl2List.append(self.GetWLRefVal(index))
        return (len(set(wl1List)) == 1 or len(set(wl1List)) == 0) and (len(set(wl2List)) == 1 or len(set(wl2List)) == 0), list(set(wl1List)), list(set(wl2List))

    #Check if WL Reference Point map to different column, return true if no conflict detected
    def wlrConflictCheck2(self):
        wl1 = ""
        wl2 = ""
        wlrPoint = ""
        wlrPoint2 = ""
        for index, ckbox in enumerate(self.selectSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                if wlrPoint == "":
                    wlrPoint = self.GetWLRefVal(index)
                    wl1 = self.GetWLCombobox(index).GetValue()
                elif wlrPoint == self.GetWLRefVal(index):
                    if wl1 != self.GetWLCombobox(index).GetValue():
                        return False
                elif wlrPoint2 == "":
                    wlrPoint2 = self.GetWLRefVal(index)
                    wl2 = self.GetWLCombobox(index).GetValue()
                elif wlrPoint2 == self.GetWLRefVal(index):
                    if wl2 != self.GetWLCombobox(index).GetValue():
                        return False

        return True

    #Transfer one entry to front page by index number
    def TransferValue(self, row):
        time = self.GetTimeVal(row)
        wlValue = self.GetCwlVal(row)
        loggerValue = self.GetLoggerReadingVal(row)
        loggerValue2 = self.GetLoggerReadingVal2(row)

        wlr1 = False
        wlr2 = False
        hg = True if loggerValue != "" else False
        hg2 = True if loggerValue2 != "" else False
        if self.GetWLCombobox(row).GetValue() == "" and loggerValue == "" and loggerValue2 == "":
            return False, False, False, False
        if self.GetWLCombobox(row).GetValue() == "WLR1":
            self.manager.TransferToStageMeasurement(time, loggerValue, loggerValue2, wlValue, None)
            wlr1 = True if wlValue != "" else False
        elif self.GetWLCombobox(row).GetValue() == "WLR2":
            self.manager.TransferToStageMeasurement(time, loggerValue, loggerValue2, None, wlValue)
            wlr2 = True if wlValue != "" else False
        else:
            self.manager.TransferToStageMeasurement(time, loggerValue, loggerValue2, None, None)
        return hg, hg2, wlr1, wlr2


    #Creating a toaster box message after transfer
    def CreateToasterBox(self, parent, msg, second, color, size=(160, 50)):
        myToasterBox = tb.ToasterBox(self, tbstyle=tb.TB_COMPLEX, windowstyle=tb.TB_DEFAULT_STYLE, closingstyle=tb.TB_ONTIME, scrollType=tb.TB_SCR_TYPE_DU)
        myToasterBox.SetPopupPauseTime(3000)
        myToasterBox.SetPopupScrollSpeed(8)

        tbPanel = myToasterBox.GetToasterBoxWindow()
        myPanel = wx.Panel(tbPanel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(myPanel, label=self.transferConfirmationMsg)
        txt.SetForegroundColour("Blue")
        myPanel.SetSizer(sizer)
        sizer.Add(txt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        myToasterBox.AddPanel(myPanel)

        myToasterBox.CenterOnParent()
        myToasterBox.SetPopupBackgroundColour("#DFD996")

        myToasterBox.SetPopupSize((160, 50))

        myToasterBox.Play()


    #Event for click on the checkbox for each entry
    def OnCheckBox(self, evt):
        obj = evt.GetEventObject()
        index = int(obj.GetName())
        # print index
        self.RefreshCombobox(index)

    def RefreshCombobox(self, index):
        if self.GetCheckbox(index).IsChecked():
            self.GetWLCombobox(index).Show()
            self.AutoSelect(index)
        else:
            self.GetWLCombobox(index).Hide()
            self.GetWLCombobox(index).SetValue("")
        self.cwlValSizer.Layout()
        self.loggerValSizer.Layout()


    #Auto select the corresponding column for CWL and Logger by row number
    def AutoSelect(self, row):
        if self.GetWLRef(row).GetValue() == "" and self.manager.manager.stageMeasManager.bmLeft == "":
            self.GetWLCombobox(row).SetValue("")
        elif self.GetWLRef(row).GetValue() == self.manager.manager.stageMeasManager.bmLeft:
            self.GetWLCombobox(row).SetValue("WLR1")
        elif self.GetWLRef(row).GetValue() == self.manager.manager.stageMeasManager.bmRight:
            self.GetWLCombobox(row).SetValue("WLR2")
        else:
            self.GetWLCombobox(row).SetValue("")

        # if self.loggerLabelCtrl.GetValue() == self.manager.manager.stageMeasManager.stageLabelCtrl1:
        #     self.GetHGCombobox(row).SetValue("HG")
        # elif self.loggerLabelCtrl.GetValue() == self.manager.manager.stageMeasManager.stageLabelCtrl2:
        #     self.GetHGCombobox(row).SetValue("HG2")
        # else:
        #     self.GetHGCombobox(row).SetValue("")


    #Checkbox
    def GetCheckbox(self, row):
        maxrow = len(self.selectSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return  self.selectSizer.GetItem(row).GetWindow()



    #Time window
    def GetTime(self, row):
        maxrow = len(self.timeValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return  self.timeValSizer.GetItem(row).GetWindow()


    #Time Val Getter
    def GetTimeVal(self, row):
        return self.GetTime(row).GetValue()

    #Time Val Setter
    def SetTimeVal(self, row, val):
        self.GetTime(row).SetValue(val)

    #WLRef window
    def GetWLRef(self, row):
        maxrow = len(self.WLRefValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.WLRefValSizer.GetItem(row).GetWindow()



    #WLRef Val Getter
    def GetWLRefVal(self, row):
        return self.GetWLRef(row).GetValue()

    #WLRef Val Setter
    def SetWLRefVal(self, row, val):
        self.GetWLRef(row).SetValue(val)


    #Elevation window
    def GetElevation(self, row):
        maxrow = len(self.elevationValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.elevationValSizer.GetItem(row).GetWindow()


    #Elevation Val Getter
    def GetElevationVal(self, row):
        return self.GetElevation(row).GetValue()

    #Elevation Val Setter
    def SetElevationVal(self, row, val):
        self.GetElevation(row).SetValue(val)

    #DtWS window
    def GetDtWS(self, row):
        maxrow = len(self.DtWSValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.DtWSValSizer.GetItem(row).GetWindow()


    #DtWS Val Getter
    def GetDtWSVal(self, row):
        return self.GetDtWS(row).GetValue()

    #DtWS Val Setter
    def SetDtWSVal(self, row, val):
        self.GetDtWS(row).SetValue(val)


    #Surge window
    def GetSurge(self, row):
        maxrow = len(self.surgeValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.surgeValSizer.GetItem(row).GetWindow()

    #Surge Val Getter
    def GetSurgeVal(self, row):
        return self.GetSurge(row).GetValue()

    #Surge Val Setter
    def SetSurgeVal(self, row, val):
        self.GetSurge(row).SetValue(val)

    #WLElev window
    def GetWLElev(self, row):
        maxrow = len(self.wleValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.wleValSizer.GetItem(row).GetWindow()


    #WLElev Val Getter
    def GetWLElevVal(self, row):
        return self.GetWLElev(row).GetValue()

    #WLElev Val Setter
    def SetWLElevVal(self, row, val):
        self.GetWLElev(row).SetValue(val)

    #Datum window
    def GetDatum(self, row):
        maxrow = len(self.datumValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.datumValSizer.GetItem(row).GetWindow()


    #Datum Val Getter
    def GetDatumVal(self, row):
        return self.GetDatum(row).GetValue()

    #Datum Val Setter
    def SetDatumVal(self, row, val):
        self.GetDatum(row).SetValue(val)

    #CorrectedWaterLevel window
    def GetCwl(self, row):
        maxrow = len(self.cwlValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.cwlValSizer.GetItem(row).GetSizer().GetItem(0).GetWindow()


    #CorrectedWaterLevel Val Getter
    def GetCwlVal(self, row):
        return self.GetCwl(row).GetValue()

    #CorrectedWaterLevel Val Setter
    def SetCwlVal(self, row, val):
        self.GetCwl(row).SetValue(val)


    #WLR checkbox
    def GetWLCombobox(self, row):
        maxrow = len(self.cwlValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.cwlValSizer.GetItem(row).GetSizer().GetItem(1).GetWindow()

    #LoggerReading window
    def GetLoggerReading(self, row):
        maxrow = len(self.loggerValSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.loggerValSizer.GetItem(row).GetWindow()


    #LoggerReading Val Getter
    def GetLoggerReadingVal(self, row):
        return self.GetLoggerReading(row).GetValue()

    #LoggerReading Val Setter
    def SetLoggerReadingVal(self, row, val):
        self.GetLoggerReading(row).SetValue(val)

    #LoggerReading window2
    def GetLoggerReading2(self, row):
        maxrow = len(self.loggerValSizer2.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.loggerValSizer2.GetItem(row).GetWindow()


    #LoggerReading2 Val Getter
    def GetLoggerReadingVal2(self, row):
        return self.GetLoggerReading2(row).GetValue()

    #LoggerReading2 Val Setter
    def SetLoggerReadingVal2(self, row, val):
        self.GetLoggerReading2(row).SetValue(val)



    #Return HG name header
    def GetHG(self):
        return self.hgText

    #Return HG2 name header
    def GetHG2(self):
        return self.hgText2

    #Disable scrolling function for combobox
    def NoScrolling(self, evt):
        pass

    def PrintNames(self):
        for index, item in enumerate(self.entryColButtonSizer.GetChildren()):
            if index < len(self.entryColButtonSizer.GetChildren()) -1 :
                print self.entryColButtonSizer.GetItem(index).GetWindow().GetName(), \
                        self.selectSizer.GetItem(index).GetWindow().GetName(),\
                        self.timeValSizer.GetItem(index).GetWindow().GetName(), \
                        self.surgeValSizer.GetItem(index).GetWindow().GetName(), \
                        self.elevationValSizer.GetItem(index).GetWindow().GetName(), \
                        self.cwlValSizer.GetItem(index).GetSizer().GetItem(0).GetWindow().GetName(), \
                        self.cwlValSizer.GetItem(index).GetSizer().GetItem(1).GetWindow().GetName(), \
                        self.datumValSizer.GetItem(index).GetWindow().GetName(), \
                        self.loggerValSizer.GetItem(index).GetWindow().GetName(), \
                        self.loggerValSizer2.GetItem(index).GetWindow().GetName(), \
                        self.wleValSizer.GetItem(index).GetWindow().GetName()

            else:
                print self.entryColButtonSizer.GetItem(index).GetWindow().GetName()

        print "================"

    #Remove invalid char from cell other than a float number
    #possibilly rounding as well
    # def OnKillFocus(self, event, decimal):
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

    #allow only the float number type inputs
    def NumberControl(self, event):
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


    #Reset the time ctrl to "00:00" by pressing 'R'
    def OnResetTime(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('R'):
            ctrl = event.GetEventObject()
            ctrl.SetValue("00:00")
        event.Skip()


    #Event on changing the radio button for levelling type
    def OnChangeLevelType(self, event):
        dlg = wx.MessageDialog(self, self.changeLvlMethodMessage, "Are you sure?", wx.YES_NO|wx.YES_DEFAULT)
        res = dlg.ShowModal()
        if res == wx.ID_YES:
            if self.rb1.GetValue():
                self.levelNotes.type = 0
            else:
                self.levelNotes.type = 1
            self.levelNotes.RefreshTable()
            dlg.Destroy()
        else:
            if not self.rb1.GetValue():
                self.rb1.SetValue(True)
            else:
                self.rb2.SetValue(True)
            dlg.Destroy()

    #Hint button on Comments
    def OnCmtBtn(self, event):
        dlg = wx.MessageDialog(self, self.correctCmtBtnHint, 'Hint', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 800))
    WaterLevelRunPanel("DEBUG", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
