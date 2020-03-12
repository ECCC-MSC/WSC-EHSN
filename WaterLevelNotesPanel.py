# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
# import wx.combo as cb
# from wx import ComboPopup

import wx.lib.scrolledpanel as scrolledpanel
import wx.lib.agw.balloontip as BT
import wx.lib.agw.toasterbox as tb
import re
import NumberControl
from time import clock
from DropdownTime import *

class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""






class WaterLevelNotesPanel(wx.Panel):
    def __init__(self, mode, showTitle, entryNum, manager, *args, **kwargs):
        super(WaterLevelNotesPanel, self).__init__(*args, **kwargs)
        self.manager = manager

        self.stationLbl = "Station"
        self.timeLbl = "Time"
        self.BSLbl = "Backsight"
        self.HTInstLbl = "Height of Instrument"
        self.FSLbl = "Foresight"
        self.elevLbl = "Elevation [Surveyed]"
        self.physDescLbl = "Physical Description"
        self.establishedElevLbl = "Established Elev.\n(m)[AQUARIUS]"
        self.commentsLbl = "Comments"

        self.removeRunButLbl = "Remove Circuit"
        self.hintLbl = "Aggregation of the Foresight and/or Backsight measurements \nmay be needed externally before entering the values\n" \
                + " in eHSN when levelling a wire-weight gauge (e.g. when \nsight on the grooves of weight and WWG reading are used) \nor a staff gauge" \
                + " (e.g. when more than one rod is used for \nmeasurements) is performed."

        self.closureLbl = "Closure"
        self.closureUnitLbl = "m"
        self.numRun = 0
        self.results = []
        self.BMs = []

        self.headerRow = 34
        self.headerCol = 40
        self.entryRow = 22

        #switch from Convention Levelling to Total Station (0 or 1)
        self.type = 0

        self.entries = entryNum
        self.entryNum = []
        self.rowNum = 6

        self.mode=mode
        self.showTitle = showTitle

        self.InitUI()

    #convert to upper case
    def OnTextType(self, event):
        textCtr=event.GetEventObject()
        textCtr.ChangeValue(unicode.upper(textCtr.GetValue()))
        textCtr.SetInsertionPointEnd()
    def InitUI(self):
        if self.mode=="DEBUG":
            print "LevelNotes"

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.layoutSizer)


        levelNotesHeader = wx.BoxSizer(wx.HORIZONTAL)



        #button column
        entryColButtonPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        entryColButtonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonHeaderTxt = wx.StaticText(entryColButtonPanel, size=(30, self.headerRow))
        entryColButtonPanel.SetSizer(entryColButtonSizer)
        entryColButtonSizer.Add(buttonHeaderTxt, 0, wx.EXPAND)

        levelNotesHeader.Add(entryColButtonPanel, 0, wx.EXPAND)


        # #select column
        # selectPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        # selectSizer = wx.BoxSizer(wx.VERTICAL)
        # selectHeaderTxt = wx.StaticText(selectPanel, size=(15, self.headerRow))

        # selectPanel.SetSizer(selectSizer)
        # selectSizer.Add(selectHeaderTxt, 1, wx.EXPAND)


        # levelNotesHeader.Add(selectPanel, 0, wx.EXPAND)


        #station column
        stationTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        stationTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        stationTxt = wx.StaticText(stationTxtPanel, label=self.stationLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, \
                                    size=(self.headerCol + 6, self.headerRow))
        stationTxtPanelSizer.Add(stationTxt, 1, wx.EXPAND)
        stationTxtPanel.SetSizer(stationTxtPanelSizer)

        levelNotesHeader.Add(stationTxtPanel, 1, wx.EXPAND)


        #Time column
        timeTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        timeTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeTxt = wx.StaticText(timeTxtPanel, label=self.timeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, \
                                size=(self.headerCol+6, self.headerRow))
        timeTxtPanelSizer.Add(timeTxt, 1, wx.EXPAND)
        timeTxtPanel.SetSizer(timeTxtPanelSizer)

        levelNotesHeader.Add(timeTxtPanel, 1, wx.EXPAND)



        #BS column
        BSTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        BSTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        BSTxt = wx.StaticText(BSTxtPanel, label=self.BSLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol, self.headerRow))


        tooltipBS = wx.ToolTip(self.hintLbl)
        tooltipBS.SetDelay(10)
        tooltipBS.SetAutoPop(30000)
        BSTxt.SetToolTip(tooltipBS)

        # tooltipBS = wx.adv.RichToolTip("Note:", self.hintLbl)
        # tooltipBS.SetTimeout(999999)
        # tooltipBS.SetBackgroundColour("#D9DC75")
        # tooltipBS.SetTipKind(wx.adv.TipKind_Auto)
        # tooltipBS.ShowFor(BSTxt)


        # tipballoon = BT.BalloonTip(topicon=None, toptitle="Note: ", message=self.hintLbl, shape=BT.BT_ROUNDED, tipstyle=BT.BT_LEAVE)
        # # Set the BalloonTip target
        # tipballoon.SetTarget(BSTxt)
        # # Set the BalloonTip background colour
        # tipballoon.SetBalloonColour("#D9DC75")
        # # Set the font for the balloon title
        # tipballoon.SetTitleFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        # # Set the colour for the balloon title
        # tipballoon.SetTitleColour(wx.BLACK)
        # # Leave the message font as default
        # tipballoon.SetMessageFont()
        # # Set the message (tip) foreground colour
        # tipballoon.SetMessageColour(wx.BLACK)
        # # Set the start delay for the BalloonTip
        # tipballoon.SetStartDelay(1)
        # # # Set the time after which the BalloonTip is destroyed
        # # tipballoon.SetEndDelay(1000)



        BSTxtPanelSizer.Add(BSTxt, 1, wx.EXPAND)
        BSTxtPanel.SetSizer(BSTxtPanelSizer)

        levelNotesHeader.Add(BSTxtPanel, 1, wx.EXPAND)


        #HTInst Col
        HTInstTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        HTInstTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        HTInstTxt = wx.StaticText(HTInstTxtPanel, label=self.HTInstLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol + 6, self.headerRow))

        HTInstTxtPanelSizer.Add(HTInstTxt, 1, wx.EXPAND)
        HTInstTxtPanel.SetSizer(HTInstTxtPanelSizer)

        levelNotesHeader.Add(HTInstTxtPanel, 1, wx.EXPAND)


        #FS col
        FSTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        FSTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        FSTxt = wx.StaticText(FSTxtPanel, label=self.FSLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol - 2, self.headerRow))

        # tipballoonFS = BT.BalloonTip(topicon=None, toptitle="Note: ", message=self.hintLbl, shape=BT.BT_ROUNDED, tipstyle=BT.BT_LEAVE)
        # # Set the BalloonTip target
        # tipballoonFS.SetTarget(FSTxt)
        # # Set the BalloonTip background colour
        # tipballoonFS.SetBalloonColour("#D9DC75")
        # # Set the font for the balloon title
        # tipballoonFS.SetTitleFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        # # Set the colour for the balloon title
        # tipballoonFS.SetTitleColour(wx.BLACK)
        # # Leave the message font as default
        # tipballoonFS.SetMessageFont()
        # # Set the message (tip) foreground colour
        # tipballoonFS.SetMessageColour(wx.BLACK)
        # # Set the start delay for the BalloonTip
        # tipballoonFS.SetStartDelay(1)
        # # # Set the time after which the BalloonTip is destroyed
        # # tipballoon.SetEndDelay(1000)


        tooltipFS = wx.ToolTip(self.hintLbl)

        tooltipFS.SetDelay(10)
        tooltipFS.SetAutoPop(30000)
        FSTxt.SetToolTip(tooltipFS)

        FSTxtPanelSizer.Add(FSTxt, 1, wx.EXPAND)
        FSTxtPanel.SetSizer(FSTxtPanelSizer)

        levelNotesHeader.Add(FSTxtPanel, 1, wx.EXPAND)


        #Elevation Col
        elevTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        elevTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        elevTxt = wx.StaticText(elevTxtPanel, label=self.elevLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol, self.headerRow))
        elevTxtPanelSizer.Add(elevTxt, 1, wx.EXPAND)
        elevTxtPanel.SetSizer(elevTxtPanelSizer)

        levelNotesHeader.Add(elevTxtPanel, 1, wx.EXPAND)






        # #Physical Description
        # physDescPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        # physDescPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        # physDescTxt = wx.StaticText(physDescPanel, label=self.physDescLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol + 6, self.headerRow))
        # physDescPanelSizer.Add(physDescTxt, 1, wx.EXPAND)
        # physDescPanel.SetSizer(physDescPanelSizer)

        # levelNotesHeader.Add(physDescPanel, 2, wx.EXPAND)


        #Comments col
        commentsTxtPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        commentsTxtPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        commentsTxt = wx.StaticText(commentsTxtPanel, label=self.commentsLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol * 2, self.headerRow))
        commentsTxtPanelSizer.Add(commentsTxt, 1, wx.EXPAND)
        commentsTxtPanel.SetSizer(commentsTxtPanelSizer)

        levelNotesHeader.Add(commentsTxtPanel, 2, wx.EXPAND)



        #Established Elev
        establishPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.headerRow))
        establishPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        physDescTxt = wx.StaticText(establishPanel, label=self.establishedElevLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.headerCol, self.headerRow))
        establishPanelSizer.Add(physDescTxt, 1, wx.EXPAND)
        establishPanel.SetSizer(establishPanelSizer)

        levelNotesHeader.Add(establishPanel, 1, wx.EXPAND)
        levelNotesHeader.Add((18,-1), 0)


        self.layoutSizer.Add(levelNotesHeader, 0, wx.EXPAND)


        self.runPanel = scrolledpanel.ScrolledPanel(self, style=wx.SIMPLE_BORDER, size=(-1, 100))
        self.runPanel.SetupScrolling()
        self.runPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        # self.runPanel.SetupScrolling(scroll_x=True, scroll_y=True, scrollToTop=False)


        runPanelSizer = wx.BoxSizer(wx.VERTICAL)


        self.runSizer = wx.BoxSizer(wx.VERTICAL)
        self.runPanel.SetSizer(runPanelSizer)

        self.layoutSizer.Add(self.runPanel, 1, wx.EXPAND)



        # addRunSizer = wx.BoxSizer(wx.HORIZONTAL)

        # self.addRunButton = wx.Button(self, label=self.addRunButLbl, size=(-1, 50))
        # self.addRunButton.Bind(wx.EVT_BUTTON, self.OnAddRun)



        runPanelSizer.Add(self.runSizer, 0, wx.EXPAND)
        # # runPanelSizer.Add(addRunSizer, 0, wx.EXPAND)


        # self.layoutSizer.Add(addRunSizer, 0, wx.EXPAND)


        # if self.manager is None:
        #     addRunSizer.Add((-1,-1), 5, wx.EXPAND)
        # else:
        #     self.transferSizer = wx.BoxSizer(wx.HORIZONTAL)
        #     addRunSizer.Add(self.transferSizer, 5, wx.EXPAND|wx.ALL, 5)
        # addRunSizer.Add(self.addRunButton, 0, wx.RIGHT, 5)



        # self.AddRun()



    def OnAddRun(self, event):
        # starttime = clock()
        self.AddRun()
        self.Layout()
        # endtime = clock()
        # print "total time usage = ",endtime-starttime, " second."




    def AddRun(self):
        # starttime = clock()
        self.entryNum.append(-1)

        subRunPanel = wx.Panel(self.runPanel, style=wx.SIMPLE_BORDER, name=str(self.numRun))
        subRunSizer = wx.BoxSizer(wx.VERTICAL)
        subRunPanel.SetSizer(subRunSizer)
        #Station sizer
        levelNotesSizerV = wx.BoxSizer(wx.VERTICAL)



        button = wx.Button(subRunPanel, name = str(0), label="+", size=(30, self.entryRow))
        button.Bind(wx.EVT_BUTTON, self.OnAddEntry)

        self.entryNum[self.numRun] += 1


        rowSizer = wx.BoxSizer(wx.HORIZONTAL)
        rowSizer.Add(button, 0, wx.EXPAND)
        levelNotesSizerV.Add(rowSizer, 0, wx.EXPAND)

         # Closure
        closurePanel = wx.Panel(subRunPanel, style=wx.SIMPLE_BORDER)
        closurePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        closurePanel.SetSizer(closurePanelSizer)


        self.closureBtn = wx.Button(closurePanel, label=self.closureLbl)
        self.closureBtn.Bind(wx.EVT_BUTTON, self.OnClosure)
        closureSubPanel = wx.Panel(closurePanel, style=wx.SUNKEN_BORDER, size=(90, -1))

        self.closureCtrl = wx.TextCtrl(closureSubPanel, style=wx.TE_PROCESS_ENTER)
        self.closureCtrl.Bind(wx.EVT_TEXT, self.OnClosureCtrl)
        closureSizer = wx.BoxSizer(wx.VERTICAL)
        closureSizer.Add(self.closureCtrl, 1, wx.EXPAND)
        closureSubPanel.SetSizer(closureSizer)

        closureUnitTxt = wx.StaticText(closurePanel, label=self.closureUnitLbl)



        removeRunButton = wx.Button(closurePanel, label=self.removeRunButLbl, name = str(self.numRun), size=(120, -1))
        removeRunButton.SetForegroundColour('Red')
        removeRunButton.Bind(wx.EVT_BUTTON, self.OnRemoveRun)

        uploadCkbox = wx.CheckBox(closurePanel, label="Upload", name=str(self.numRun), size=(-1,-1))
        uploadCkbox.SetValue(False)

        # if self.numRun == 0:
        #     removeRunButton.Hide()

        # closurePanelSizer.Add((20, -1), 0, wx.EXPAND)

        closurePanelSizer.Add(self.closureBtn, 0, wx.EXPAND|wx.ALL, 5)
        closurePanelSizer.Add(closureSubPanel, 0, wx.EXPAND|wx.ALL, 5)
        closurePanelSizer.Add(closureUnitTxt, 0, wx.EXPAND|wx.TOP|wx.LEFT, 10)
        closurePanelSizer.Add((-1, -1), 1, wx.EXPAND)
        closurePanelSizer.Add(uploadCkbox, 0, wx.EXPAND)
        closurePanelSizer.Add(removeRunButton, 0, wx.EXPAND|wx.ALL|wx.ALIGN_RIGHT, 5)

        subRunSizer.Add(levelNotesSizerV, 0, wx.EXPAND)
        subRunSizer.Add(closurePanel, 0, wx.EXPAND)

        self.runSizer.Add(subRunPanel, 0, wx.EXPAND)
        self.numRun += 1


        # endtime = clock()
        # print "1 time usage = ",endtime-starttime, " second."
        # starttime = endtime


        for i in range(self.rowNum):

            self.AddEntry(self.numRun - 1)



        # endtime = clock()
        # print "2 time usage = ",endtime-starttime, " second."
        # starttime = endtime







        if self.manager is not None:
            self.manager.runTablePanel.FitInside()
            self.manager.runTablePanel.Layout()



        # endtime = clock()
        # print "3 time usage = ",endtime-starttime, " second."


    # When the 'Remove' is clicked, remove the current run
    def OnRemoveRun(self, e):

        #Button col stuff
        button = e.GetEventObject()
        index = int(button.GetName())
        # if index != 0:

        if self.mode=="DEBUG":
            print "index %s" % index

        if len(self.runSizer.GetChildren()) > index:

            runIndex = 0
            for index, run in enumerate(self.runSizer.GetChildren()):

                if button == self.GetRemoveRunButton(index):

                    dlg = wx.MessageDialog(self, "Do you want to remove the run?", 'Remove',
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

                    self.RemoveRun(runIndex)
                    break

                runIndex += 1
            self.Layout()





    # Delete the table at the index of the clicked 'Remove' button
    # Reorder the list of all runs
    def RemoveRun(self, runIndex):

        if self.mode=="DEBUG":
            print "remove %s" % runIndex

        self.runSizer.Hide(runIndex)
        self.runSizer.Remove(runIndex)

        # self.runPanel.GetChildren()[runIndex].Destroy()


        del self.entryNum[runIndex]
        self.numRun -= 1

        for child in range(0, len(self.runSizer.GetChildren())):
            i = int(self.runSizer.GetItem(child).GetWindow().GetName())
            if i > runIndex:
                self.GetSubRunPanel(child).SetName("%s" % (i - 1))
                self.GetUploadCheckBox(child).SetName("%s" % (i - 1))
                self.GetRemoveRunButton(child).SetName("%s" % (i - 1))

        self.Layout()

        if self.manager is not None:
            self.runPanel.SetSize(-1, 300)
            self.manager.levelNotes.SetSize(-1, 330)
            self.manager.splitter.SetSashPosition(330)
            self.manager.runTablePanel.FitInside()
            self.manager.runTablePanel.Layout()
            self.manager.Layout()


    def AddEntry(self, index):
        # print index
        # starttime = clock()
        
        panel = self.GetSubRunPanel(index)
        sizer = self.GetLevelNotesSizerV(index)


        rowSizer = sizer.GetItem(self.entryNum[index]).GetSizer()
        #Button col
        name = "%s" % (self.entryNum[index] + 1)
        oldname = "%s" % self.entryNum[index]

        button = wx.Button(panel, label="+", name=name, size=(30, self.entryRow))


        button.Bind(wx.EVT_BUTTON, self.OnAddEntry)


        newRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        newRowSizer.Add(button, 0, wx.EXPAND)
        sizer.Add(newRowSizer, 1, wx.EXPAND)

        oldButton = rowSizer.GetItem(0).GetWindow()
        oldButton.SetLabel('-')
        oldButton.Bind(wx.EVT_BUTTON, self.OnRemoveEntry)



        # endtime = clock()
        # print "1 time usage = ",endtime-starttime, " second."
        # starttime = endtime



        # checkbox = wx.CheckBox(panel, name=oldname)


        stationsCmbo = wx.ComboBox(panel, choices=self.BMs, style=wx.CB_DROPDOWN, name=oldname, size=(self.headerCol, self.entryRow))
        stationsCmbo.Bind(wx.EVT_TEXT, self.OnStationEnableRow)
        stationsCmbo.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)

        stationsCmbo.MoveAfterInTabOrder(oldButton)

        timeCtrl = DropdownTime(False, parent=panel, size=(self.headerCol, self.entryRow))
        timeCtrl.MoveAfterInTabOrder(stationsCmbo)


        if self.manager is not None:
            if self.manager.manager is not None:
                if self.manager.manager.manager is not None:
                    stationsCmbo.Bind(wx.EVT_TEXT, self.manager.manager.manager.gui.OnLevelNoteStationSelect)
        BSCtrl = MyTextCtrl(panel, style=wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
        BSCtrl.MoveAfterInTabOrder(timeCtrl)
        BSCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        BSCtrl.Bind(wx.EVT_TEXT, self.OnBacksightUpdateHI)
        BSCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        BSCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)


        HTInstCtrl = MyTextCtrl(panel, style=wx.TE_READONLY|wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
        HTInstCtrl.MoveAfterInTabOrder(BSCtrl)
        HTInstCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        HTInstCtrl.Bind(wx.EVT_TEXT, self.OnHIUpdateEle)
        HTInstCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        HTInstCtrl.Bind(wx.EVT_TEXT, NumberControl.Round3)
        HTInstCtrl.SetBackgroundColour((204,204,204))
        HTInstCtrl.SetForegroundColour((0,0,204))


        # endtime = clock()
        # print "2 time usage = ",endtime-starttime, " second."
        # starttime = endtime



        if oldname == '0':
            FSCtrl = MyTextCtrl(panel, style=wx.TE_READONLY|wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
        else:
            FSCtrl = MyTextCtrl(panel, style=wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
        FSCtrl.MoveAfterInTabOrder(HTInstCtrl)
        FSCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        FSCtrl.Bind(wx.EVT_TEXT, self.OnForesightUpdateEle)
        FSCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        FSCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)


        eleSizer = wx.BoxSizer(wx.HORIZONTAL)
        eleChkbx = wx.CheckBox(panel, name=oldname)
        eleChkbx.Bind(wx.EVT_CHECKBOX, self.OnElevationCkbox)
        eleChkbx.MoveAfterInTabOrder(FSCtrl)
        eleChkbx.Hide()



        # endtime = clock()
        # print "3 time usage = ",endtime-starttime, " second."
        # starttime = endtime




        if oldname == '0':
            elevCtrl = MyTextCtrl(panel, style=wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
            elevCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        else:
            elevCtrl = MyTextCtrl(panel, style=wx.TE_READONLY|wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
            elevCtrl.Bind(wx.EVT_TEXT, NumberControl.Round3)
            elevCtrl.SetBackgroundColour((204,204,204))
            elevCtrl.SetForegroundColour((0,0,204))
        elevCtrl.Bind(wx.EVT_TEXT, self.OnElevation)
        elevCtrl.MoveAfterInTabOrder(FSCtrl)
        elevCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        elevCtrl.Bind(wx.EVT_TEXT, self.OnElevationUpdateHI)



        # endtime = clock()
        # print "4 time usage = ",endtime-starttime, " second."
        # starttime = endtime

        # elevCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)



        eleSizer.Add(elevCtrl, 1, wx.EXPAND)
        eleSizer.Add(eleChkbx, 0, wx.EXPAND|wx.ALL, 3)

        commentsCtrl = wx.TextCtrl(panel, name=oldname, size=(self.headerCol * 2, self.entryRow))
        commentsCtrl.MoveAfterInTabOrder(elevCtrl)

        establishedSizer = wx.BoxSizer(wx.HORIZONTAL)

        estElevChkbx = wx.CheckBox(panel, name=oldname)
        estElevChkbx.Bind(wx.EVT_CHECKBOX, self.OnEstablishCkbox)
        estElevChkbx.MoveAfterInTabOrder(commentsCtrl)
        estElevChkbx.Hide()

        establishCtrl = wx.TextCtrl(panel, style=wx.TE_CENTRE, name=oldname, size=(self.headerCol, self.entryRow))
        establishCtrl.Bind(wx.EVT_TEXT, self.OnEstablish)
        establishCtrl.MoveAfterInTabOrder(estElevChkbx)
        descButton = wx.Button(panel, name=oldname, size=(20, self.entryRow), label="?")
        descButton.MoveAfterInTabOrder(establishCtrl)

        if self.manager is not None:
            descButton.Bind(wx.EVT_BUTTON, self.manager.manager.manager.gui.OnLevelNoteEstablishedBtn)

        establishedSizer.Add(estElevChkbx, 0, wx.EXPAND)
        establishedSizer.Add(establishCtrl, 1, wx.EXPAND)
        establishedSizer.Add(descButton, 0)


        button.MoveAfterInTabOrder(descButton)

        # rowSizer.Add(checkbox, 0, wx.EXPAND)
        rowSizer.Add(stationsCmbo, 1, wx.EXPAND)
        rowSizer.Add(timeCtrl, 1, wx.EXPAND)
        rowSizer.Add(BSCtrl, 1, wx.EXPAND)
        rowSizer.Add(HTInstCtrl, 1, wx.EXPAND)
        rowSizer.Add(FSCtrl, 1, wx.EXPAND)
        # rowSizer.Add(elevCtrl, 1, wx.EXPAND)
        rowSizer.Add(eleSizer, 1, wx.EXPAND)

        rowSizer.Add(commentsCtrl, 2, wx.EXPAND)
        rowSizer.Add(establishedSizer, 1, wx.EXPAND)

        self.entryNum[index] += 1


        self.EnableEntry(index, self.entryNum[index] - 1, False)
        self.Layout()



        # endtime = clock()
        # print "5 time usage = ",endtime-starttime, " second."
        # starttime = endtime



        if self.manager is not None:
            # starttime = clock()
            if self.manager.manager is not None:
                if self.manager.manager.manager is not None:


                    # endtime = clock()
                    # print "1 time usage = ",endtime-starttime, " second."
                    # starttime = endtime


                    self.updateBMs(self.manager.manager.manager.gui.bm, self.manager.manager.manager.gui.bmIndex)
                    

                    # endtime = clock()
                    # print "2 time usage = ",endtime-starttime, " second."
                    # starttime = endtime


                    #binding event for auto save
                    # stationsCmbo.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.manager.gui.OnAutoSave)
                    # endtime = clock()
                    # print "3 time usage = ",endtime-starttime, " second."
                    # starttime = endtime


                    BSCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.manager.gui.OnAutoSave)
                    timeCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.manager.gui.OnAutoSave)
                    FSCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.manager.gui.OnAutoSave)
                    elevCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.manager.gui.OnAutoSave)
                    commentsCtrl.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.manager.gui.OnAutoSave)

                    # endtime = clock()
                    # print "4 time usage = ",endtime-starttime, " second."
                    # starttime = endtime


            self.manager.runTablePanel.FitInside()
            self.manager.runTablePanel.Layout()

            # endtime = clock()
            # print "5 time usage = ",endtime-starttime, " second."
            # starttime = endtime
            # print "___________________________"


        # endtime = clock()
        # print "6 time usage = ",endtime-starttime, " second."




    def OnStationEnableRow(self, event):

        station = event.GetEventObject()
        parent = station.GetParent()
        rowIndex = int(station.GetName())
        runIndex = int(parent.GetName())

        if station.GetValue() == '':
            self.EnableEntry(runIndex, rowIndex, False)
        else:
            self.EnableEntry(runIndex, rowIndex, True)
        index = self.GetRunIndex(parent)
        self.FindMatchBM(index)

        insertPoint = station.GetInsertionPoint()
        # station.ChangeValue(unicode.upper(station.GetValue()))
        station.SetInsertionPoint(insertPoint)



        event.Skip()

    #Find index for givin run panel
    def GetRunIndex(self, run):
    	for index, item in enumerate(self.runSizer.GetChildren()):
    		if item.GetWindow() == run:
    			return index

    #Find the first match bench mark for the givin run
    def FindMatchBM(self, index):

        if len(self.GetLevelNotesSizerV(index).GetChildren()) > 1:
            bm1 = self.GetStation(index, 0)
            if bm1.GetValue() != '':
                color = True
                match = False
                for i, row in reversed(list(enumerate(self.GetLevelNotesSizerV(index).GetChildren()))):

                    if i > 0 and i < len(self.GetLevelNotesSizerV(index).GetChildren()) - 1:
                        bm = self.GetStation(index, i)
                        if color:
                            if bm1.GetValue() == bm.GetValue():
                                bm1.SetBackgroundColour("Yellow")
                                bm.SetBackgroundColour("Yellow")
                                bm1.Refresh()
                                bm.Refresh()
                                color = False
                                match = True
                            else:
                                bm.SetBackgroundColour("White")
                                bm.Refresh()
                        else:
                            bm.SetBackgroundColour("White")
                            bm.Refresh()
                if match:
                    return
            for i, row in enumerate(self.GetLevelNotesSizerV(index).GetChildren()):
                if i < len(self.GetLevelNotesSizerV(index).GetChildren()) - 1:
                    bm = self.GetStation(index, i)
                    bm.SetBackgroundColour("White")
                    bm.Refresh()


    #Enable or disable the row by givin row and index
    def EnableEntry(self, run, row, enable):

        self.GetBacksight(run, row).Enable(enable)
        self.GetHI(run, row).Enable(enable)
        self.GetForesight(run, row).Enable(enable)
        self.GetElevation(run, row).Enable(enable)
        self.GetEstablishCheckbox(run, row).Enable(enable)
        self.GetElevationCheckbox(run, row).Enable(enable)
        self.GetEstablishedElevation(run, row).Enable(enable)
        self.GetEstablishedElevationBtn(run, row).Enable(enable)
        self.GetComments(run, row).Enable(enable)
        if not enable:
            self.GetEstablishCheckbox(run, row).SetValue(False)
            self.GetElevationCheckbox(run, row).Enable(False)



    #Set name for all the items for given row
    def SetRowItemNames(self, run, row, name):

        self.GetButton(run, row).SetName(name)

        if row < self.entryNum[run] - 1:
            self.GetStation(run, row).SetName(name)
            self.GetBacksight(run, row).SetName(name)
            self.GetHI(run, row).SetName(name)
            self.GetForesight(run, row).SetName(name)
            self.GetElevation(run, row).SetName(name)
            self.GetEstablishCheckbox(run, row).SetName(name)
            self.GetElevationCheckbox(run, row).SetName(name)
            self.GetEstablishedElevation(run, row).SetName(name)
            self.GetEstablishedElevationBtn(run, row).SetName(name)
            self.GetComments(run, row).SetName(name)






    #Add new row to each run
    def OnAddEntry(self, event):

        # index = 0
        objButton = event.GetEventObject()

        for index, child in enumerate(self.runSizer.GetChildren()):

            if objButton == self.GetButton(index, self.entryNum[index]):

                self.AddEntry(index)

                break

 	#On change of Elevation calculate the value of Height of Instrument
    def OnElevationUpdateHI(self, event):
        # self.NumberControl(event)
        index = int(event.GetEventObject().GetName())
        panel = event.GetEventObject().GetParent()
        runIndex = int(panel.GetName())
        hi = self.GetHI(runIndex, index)
        backsight = self.GetBacksight(runIndex, index)
        elevation = self.GetElevation(runIndex, index)
        eleChkbx = self.GetElevationCheckbox(runIndex, index)
        if elevation.GetValue() != '':
            eleChkbx.Show()
        else:
            eleChkbx.Hide()
            eleChkbx.SetValue(False)
        self.runPanel.Layout()
        # self.NumberControl(elevation)
        foresight = self.GetForesight(runIndex, index)

        try:
            elevationVal = float(elevation.GetValue())

            if index == 0:
                foresight.SetBackgroundColour("#f3f3f3")
                foresight.Refresh()

            try:
                backsightVal = float(backsight.GetValue())
                if self.type == 0:
                    hi.SetValue(str(elevationVal + backsightVal))
                else:
                    hi.SetValue(str(elevationVal - backsightVal))

                backsight.SetBackgroundColour("WHITE")
                backsight.Refresh()
                event.Skip()

            except:
                hi.ChangeValue("")
                if index > 0:
                    backsight.SetBackgroundColour("#f3f3f3")
                    backsight.Refresh()


                event.Skip()

        except:
            try:
                backsightVal = float(backsight.GetValue())
                hi.SetValue(str(backsightVal))
            except:
                hi.SetValue('')
            event.Skip()
            return



 	#On change of backsight calculate the value of Height of Instrument
    def OnBacksightUpdateHI(self, event):
        # self.NumberControl(event)
        index = int(event.GetEventObject().GetName())
        panel = event.GetEventObject().GetParent()
        runIndex = int(panel.GetName())
        hi = self.GetHI(runIndex, index)
        backsight = self.GetBacksight(runIndex, index)
        # self.NumberControl(backsight)
        elevation = self.GetElevation(runIndex, index)
        try:
            backsightVal = float(backsight.GetValue())
            try:
                elevationVal = float(elevation.GetValue())
                if self.type == 0:
                    hi.SetValue(str(elevationVal + backsightVal))
                else:
                    hi.SetValue(str(elevationVal - backsightVal))
            except:

                hi.SetValue(str(backsightVal))
            backsight.SetBackgroundColour("WHITE")
            backsight.Refresh()

        except:
            hi.SetValue("")
            if index > 0:
                backsight.SetBackgroundColour("#f3f3f3")
                backsight.Refresh()
        event.Skip()



 	#On change of Foresight calculate the value of Elevation
    def OnForesightUpdateEle(self, event):
        # self.NumberControl(event)
        index = int(event.GetEventObject().GetName())
        panel = event.GetEventObject().GetParent()
        runIndex = int(panel.GetName())

        # runIndex = self.GetRunIndex(panel)
        foresight = event.GetEventObject()
        self.ForesightUpdateEle(index, runIndex, foresight)
        event.Skip()

    def ForesightUpdateEle(self, index, runIndex, foresight):

        elevation = self.GetElevation(runIndex, index)
        # self.NumberControl(foresight)
        if index < len(self.GetLevelNotesSizerV(runIndex).GetChildren()) - 1:

            for i in reversed(range(index)):

                hi = self.GetHI(runIndex, i)
                try:

                    hiVal = float(hi.GetValue())
                    break
                except:
                    if i == 0:
                        return


            foresightVal = foresight.GetValue()


            try:
                foresightVal = float(foresightVal)
                if self.type == 0:
                    elevation.SetValue(str(hiVal - foresightVal))
                else:
                    elevation.SetValue(str(hiVal + foresightVal))

                # if
                # if self.results[runIndex][0]:

                #   self.results[runIndex][1] = elevation.GetValue()
                #   print self.results
            except:
                elevation.SetValue("")

                return
        else:
            return

    #On change of height of Instrument calculate the value of Elevation
    def OnHIUpdateEle(self, event):
        # self.NumberControl(event)
        index = int(event.GetEventObject().GetName())
        panel = event.GetEventObject().GetParent()
        runIndex = int(panel.GetName())
        hi = self.GetHI(runIndex, index).GetValue()
        if hi == '':
            hi = 0
        try:
            hi = float(hi)
            if index < len(self.GetLevelNotesSizerV(runIndex).GetChildren()) - 2:
                for i in range(index + 1, len(self.GetLevelNotesSizerV(runIndex).GetChildren()) - 1):
                    foresightVal = self.GetForesight(runIndex, i).GetValue()
                    if foresightVal == '':
                        event.Skip()
                        return
                    try:
                        foresightVal = float(foresightVal)
                        elevation = self.GetElevation(runIndex, i)
                        if self.type == 0:
                            elevation.SetValue(str(hi - foresightVal))
                        else:
                            elevation.SetValue(str(hi + foresightVal))
                        try:
                            float(self.GetHI(runIndex, i).GetValue())
                            event.Skip()
                            return
                        except:
                            continue
                    except:
                        continue
        except:
            event.Skip()
            return
        event.Skip()


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


    # #update Closure if the benchmark matched
    # def CalClosure(self, event):
    #     index = int(event.GetEventObject().GetName())
    #     panel = event.GetEventObject().GetParent()
    #     startBenchmark = panel.GetSizer().GetItem(0).GetSizer().GetItem(0).GetSizer().GetItem(1).GetWindow().GetValue()
    #     if startBenchmark == "":
    #         panel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(0).GetWindow().SetValue('')
    #         event.Skip()
    #         return
    #     startElevation = panel.GetSizer().GetItem(0).GetSizer().GetItem(0).GetSizer().GetItem(5).GetWindow().GetValue()
    #     try:
    #         startElevation = float(startElevation)
    #         for i, bm in enumerate(panel.GetSizer().GetItem(0).GetSizer().GetChildren()):
    #             if i > 0:
    #                 pairBM = bm.GetSizer().GetItem(1).GetWindow().GetValue()
    #                 if pairBM == startBenchmark:
    #                     pairEle = bm.GetSizer().GetItem(5).GetWindow().GetValue()
    #                     try:
    #                     	pairEle = float(pairEle)
    #                     	panel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(0).GetWindow().SetValue(str(pairEle - startElevation))
    #                     except:
    #                         panel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(0).GetWindow().SetValue('')
    #                         pass
    #                     self.OnElevationUpdateHI(event)
    #                     break
    #                 else:
    #                     panel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(0).GetWindow().SetValue('')

    #     except:
    #         panel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(0).GetWindow().SetValue('')
    #         event.Skip()
    #         return


    #Recalculate the closure when pressing the closure button for the run
    def OnClosure(self, event):

        panel = event.GetEventObject().GetParent().GetParent()
        runIndex = int(panel.GetName())
        # print "runIndex", runIndex
        startBenchmark = self.GetStation(runIndex, 0).GetValue()
        startElevation = self.GetElevation(runIndex, 0).GetValue()
        if startBenchmark == "":
            warning = wx.MessageDialog(None,"The first station is empty",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                event.Skip()
                return
        if startElevation == "":
            warning = wx.MessageDialog(None,"The first elevation is empty",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                event.Skip()
                return
        try:
        # if True:
            startElevation = float(startElevation)
            for i, bm in enumerate(reversed(self.GetLevelNotesSizerV(runIndex).GetChildren())):
                if i > 0 and i < len(self.GetLevelNotesSizerV(runIndex).GetChildren()) - 1:

                    pairBM = self.GetStation(runIndex, i).GetValue()

                    if pairBM == startBenchmark:
                        pairEle = self.GetElevation(runIndex, i).GetValue()

                        try:
                            pairEle = float(pairEle)
                            closureValue = round(pairEle - startElevation, 3)
                            self.GetClosureText(runIndex).SetValue(str(closureValue))
                            if abs(closureValue) > 0.003:
                                self.GetClosureText(runIndex).SetBackgroundColour("red")
                            
                            self.GetUploadCheckBox(runIndex).SetValue(True)
                            event.Skip()
                            return
                        except:
                            warning = wx.MessageDialog(None,"The elevation values provided for the 'BMs' is not a valid number.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
                            cont = warning.ShowModal()
                            if cont == wx.ID_OK:
                                event.Skip()
                                return

            event.Skip()


            warning = wx.MessageDialog(None,"The beginning and ending BM/Reference names are not identical.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                return

        except Exception,e:
            print str(e)
            warning = wx.MessageDialog(None,"The elevation values provided for thr 'REF' is not a valid number.",
                                            "Error", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                evnet.Skip()
                return

    def OnClosureCtrl(self, event):
        panel = event.GetEventObject().GetParent().GetParent().GetParent()
        runIndex = int(panel.GetName())
        closureCtrl = self.GetClosureText(runIndex)
        if closureCtrl.GetValue()!="":
            if abs(float(closureCtrl.GetValue())) > 0.003:
                closureCtrl.SetBackgroundColour("red")
            else:
                closureCtrl.SetBackgroundColour("white")
        closureCtrl.Refresh()
        
        event.Skip()


    # When the '-' is clicked, remove that row
    def OnRemoveEntry(self, e):
        #Button col stuff
        button = e.GetEventObject()
        index = int(button.GetName())
        if self.mode=="DEBUG":
            print "remove button index %s" % index

        runIndex = 0
        for run in self.runSizer.GetChildren():
            if len(self.GetLevelNotesSizerV(runIndex).GetChildren()) > index:
                if button == self.GetButton(runIndex, index):
                    if self.GetStation(runIndex, index).GetValue() != "":

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

                    self.RemoveEntry(runIndex, index)
                    break
            runIndex += 1

        if self.manager is not None:
            self.manager.runTablePanel.FitInside()
            self.manager.runTablePanel.Layout()




    # Delete each column's item at the index of the clicked '-' button
    # Reorder the list of entries
    def RemoveEntry(self, runIndex, entryIndex):

        if self.mode=="DEBUG":
            print "remove run index %s" % runIndex
            print "remove entry index %s" % entryIndex
        self.GetLevelNotesSizerV(runIndex).Hide(entryIndex)

        self.GetLevelNotesSizerV(runIndex).Remove(entryIndex)

        for i, row in enumerate(self.GetLevelNotesSizerV(runIndex).GetChildren()):
            if i >= entryIndex:
                self.SetRowItemNames(runIndex, i, "%s" % i)


        for i, row in enumerate(self.GetLevelNotesSizerV(runIndex).GetChildren()):
            if i >= entryIndex:
                if i == 0 and len(self.GetLevelNotesSizerV(runIndex).GetChildren()) > 1:
                    self.GetForesight(runIndex, 0).SetEditable(False)
                    self.GetElevation(runIndex, 0).SetEditable(True)
                    #change the way rounding if the row become the first row in the circuit
                    self.GetElevation(runIndex, 0).Unbind(wx.EVT_TEXT, handler=NumberControl.Round3)
                    # self.GetElevation(runIndex, 0).Unbind(wx.EVT_KILL_FOCUS)
                    self.GetElevation(runIndex, 0).Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
                    self.GetElevation(runIndex, 0).Bind(wx.EVT_TEXT, self.OnElevationUpdateHI)
                    self.GetElevation(runIndex, 0).Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

                    self.GetForesight(runIndex, 0).SetValue("")

                    self.GetStation(runIndex, 0).SetValue(self.GetStation(runIndex, 0).GetValue())


                    self.GetBacksight(runIndex, 0).SetBackgroundColour("White")
                    self.GetBacksight(runIndex, 0).Refresh()

        self.entryNum[runIndex] -= 1

        if entryIndex != 0:
            panel = self.GetSubRunPanel(runIndex)
            for rowIndex in range(entryIndex, len(self.GetLevelNotesSizerV(runIndex).GetChildren()) - 1):
                nextForesight = self.GetForesight(runIndex, rowIndex)
                self.ForesightUpdateEle(rowIndex, runIndex, nextForesight)
        self.FindMatchBM(runIndex)
        self.Layout()




    #Reset water level reference bench mark
    def updateBMs(self, items, indexList):

        preList = ["RP1", "RP2", "TP1", "TP2"]
        if len(indexList) > 0:
            updatedItems = []
            for i in range(len(items)):
                if i in indexList:
                    updatedItems.append(items[i])
            items = updatedItems
        else:
            items = []
        for item in preList:
            items.append(item)
        # print items
        for runIndex, subRunPanel in enumerate(self.runSizer.GetChildren()):
            levelNotesSizerV = self.GetLevelNotesSizerV(runIndex)
            for row in range(len(levelNotesSizerV.GetChildren()) - 1):
                rowSizer = self.GetRowSizer(runIndex, row)
                stationsCmbo = self.GetStation(runIndex, row)


                if stationsCmbo.GetValue() == '':
                    stationsCmbo.SetItems(items)
                    # stationsCmbo.Append("***ttt", wx.Font(19, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
                else:
                    ele = self.GetElevation(runIndex, row)
                    eleValue = ele.GetValue()


                    desc = self.GetEstablishedElevation(runIndex, row)
                    descVal = desc.GetValue()
                    comment = self.GetComments(runIndex, row)
                    commentVal = comment.GetValue()


                    bm = stationsCmbo.GetValue()
                    stationsCmbo.SetItems(items)
                    stationsCmbo.SetValue(bm)
                    desc.SetValue(descVal)
                    comment.SetValue(commentVal)

                    if row == 0:
                        ele.SetValue(eleValue)

        	levelNotesSizerV.Layout()
        	self.Update()

    #Select all the ckeck box without duplicate station name or uncheck all the selections if it is unchecked
    def OnSelectAll(self, event):
        if event.GetEventObject().IsChecked():
            selected = []
            for circuitIndex, circuit in enumerate(self.runSizer.GetChildren()):
                for rowIndex, row in enumerate(self.GetLevelNotesSizerV(circuitIndex).GetChildren()):
                    if rowIndex > len(self.GetLevelNotesSizerV(circuitIndex).GetChildren()) - 2:
                        break

                    station = self.GetStation(circuitIndex, rowIndex)
                    ckbox = self.GetEstablishCheckbox(circuitIndex, rowIndex)
                    stName = station.GetValue()
                    if stName not in selected and stName != '':
                        ckbox.SetValue(True)
                        selected.append(stName)
                    else:
                        ckbox.SetValue(False)
        else:
            for circuitIndex, circuit in enumerate(self.runSizer.GetChildren()):
                for rowIndex, row in enumerate(self.GetLevelNotesSizerV(circuitIndex).GetChildren()):
                    if rowIndex > len(self.GetLevelNotesSizerV(circuitIndex).GetChildren()) - 2:
                        break
                    ckbox = self.GetEstablishCheckbox(circuitIndex, rowIndex)
                    ckbox.SetValue(False)


    def GetSubRunPanel(self, index):

        return self.runSizer.GetItem(index).GetWindow()



    def GetClosurePanel(self, index):
        return self.runSizer.GetItem(index).GetWindow().GetSizer().GetItem(1).GetWindow()

    def GetClosureButton(self, index):
        return self.GetClosurePanel(index).GetSizer().GetItem(0).GetWindow()

    def GetClosureText(self, index):
        return self.GetClosurePanel(index).GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(0).GetWindow()


    def GetUploadCheckBox(self, index):
        return self.GetClosurePanel(index).GetSizer().GetItem(4).GetWindow()

    def GetRemoveRunButton(self, index):
        return self.GetClosurePanel(index).GetSizer().GetItem(5).GetWindow()

    def IsUploaded(self):
        for circuitIndex, circuit in enumerate(self.runSizer.GetChildren()):
            if self.GetUploadCheckBox(circuitIndex).IsChecked():
                return True
        return False

    def OnUploadCheckbox(self, event):
        # print self.IsUploaded()
        print self.IsEmpty()


    #If any upload checkbox selected including any value in the circuit, will return False. Otherwise, return True
    def IsEmpty(self):
        if not self.IsUploaded():
            return True
        for circuitIndex, circuit in enumerate(self.runSizer.GetChildren()):
            if self.GetUploadCheckBox(circuitIndex).IsChecked():
                for rowIndex, row in enumerate(self.GetLevelNotesSizerV(circuitIndex).GetChildren()):
                    if rowIndex > len(self.GetLevelNotesSizerV(circuitIndex).GetChildren()) - 2:
                        break
                    if self.GetStation(circuitIndex, rowIndex).GetValue() != "":
                        return False
        return True







    def GetRunEntryNumber(self, run):
        return self.entryNum[run]

    def GetNumberOfRuns(self):
        return self.numRun



    def GetTransferSizer(self):
        return self.transferSizer

    def GetLevelNotesSizerV(self, run):
        return self.runSizer.GetItem(run).GetWindow().GetSizer().GetItem(0).GetSizer()

    def GetRowSizer(self, run, row):
        return self.GetLevelNotesSizerV(run).GetItem(row).GetSizer()



    #unselect all selected checkboxes
    def UncheckAll(self):
        for runIndex, run in enumerate(self.runSizer.GetChildren()):
            for index, row in enumerate(self.GetLevelNotesSizerV(runIndex).GetChildren()):
                if index < len(self.GetLevelNotesSizerV(runIndex).GetChildren()) - 1:
                    self.GetEstablishCheckbox(runIndex, index).SetValue(False)
        self.runSizer.Layout()



    # #Gets table val for given run/row/col
    # def GetTableValue(self, run, row, col):
    #     if run >= 0 and run < len(self.runSizer.GetChildren()):
    #         if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
    #             if col > 0 and col < 8:
    #                 if self.numRun > run:
    #                     if self.entryNum[run] > row:
    #                         levelNotesSizerV = self.GetLevelNotesSizerV(run)
    #                         if col != 5:
    #                             return levelNotesSizerV.GetItem(row).GetSizer().GetItem(col).GetWindow().GetValue()
    #                         else:
    #                             return levelNotesSizerV.GetItem(row).GetSizer().GetItem(col).GetSizer().GetItem(0).GetWindow().GetValue()


    # #Sets table val for given run/row/col by value
    # def SetTableValue(self, run, row, col, value):
    #     if col > 0 and col < 8:
    #         if self.numRun > run:
    #             if self.entryNum[run] > row:
    #                 circulationSizer = self.runSizer.GetItem(run).GetWindow().GetSizer()
    #                 line = circulationSizer.GetItem(0)
    #                 if col != 5:
    #                     line.GetSizer().GetItem(row).GetSizer().GetItem(col).GetWindow().SetValue(value)
    #                 else:
    #                     line.GetSizer().GetItem(row).GetSizer().GetItem(col).GetSizer().GetItem(0).GetWindow().SetValue(value)

    # #Sets table val for given run/row/col by value
    # def ChangeTableValue(self, run, row, col, value):
    #     if col > 0 and col < 8:
    #         if self.numRun > run:
    #             if self.entryNum[run] > row:
    #                 circulationSizer = self.runSizer.GetItem(run).GetWindow().GetSizer()
    #                 line = circulationSizer.GetItem(0)
    #                 if col != 5:
    #                     line.GetSizer().GetItem(row).GetSizer().GetItem(col).GetWindow().ChangeValue(value)
    #                 else:
    #                     line.GetSizer().GetItem(row).GetSizer().GetItem(col).GetSizer().GetItem(0).GetWindow().ChangeValue(value)



    #Return the button for specific circuit and row number:
    def GetButton(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) >= row:
                        return self.GetRowSizer(run, row).GetItem(0).GetWindow()



    #Return the station for specific circuit and row number:
    def GetStation(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(1).GetWindow()


    #Return the backsight for specific circuit and row number:
    def GetBacksight(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(3).GetWindow()



    #Return the HI for specific circuit and row number:
    def GetHI(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(4).GetWindow()




    #Return the foresight for specific circuit and row number:
    def GetForesight(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(5).GetWindow()




    #Return the elevation for specific circuit and row number:
    def GetElevation(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(6).GetSizer().GetItem(0).GetWindow()

    #Return the elevation for specific circuit and row number:
    def GetElevationCheckbox(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(6).GetSizer().GetItem(1).GetWindow()



    #Return the checkbox for specific circuit and row number:
    def GetEstablishCheckbox(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(8).GetSizer().GetItem(0).GetWindow()


    #Return the Established Elevation for specific circuit and row number:
    def GetEstablishedElevation(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(8).GetSizer().GetItem(1).GetWindow()


    #Return the Established Elevation button for specific circuit and row number:
    def GetEstablishedElevationBtn(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(8).GetSizer().GetItem(2).GetWindow()


    #Return the comments for specific circuit and row number:
    def GetComments(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(7).GetWindow()

    #Return the Time for specific circuit and row number:
    def GetTime(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(2).GetWindow()

    #Return the hour for specific circuit and row number:
    def GetHour(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(2).GetWindow().GetHour()

    #Return the minute for specific circuit and row number:
    def GetMinute(self, run, row):
        if run >= 0 and run < len(self.runSizer.GetChildren()):
            if row < len(self.GetLevelNotesSizerV(run).GetChildren()) - 1 and row >= 0:
                if self.GetNumberOfRuns() > run:
                    if self.GetRunEntryNumber(run) > row:
                        return self.GetRowSizer(run, row).GetItem(2).GetWindow().GetMinute()

    #Disable scrolling function for combobox
    def NoScrolling(self, evt):
        pass

    #return the levelling type
    def GetType(self):
        return self.type
    #set the levelling type (convention or total station)
    def SetType(self, value):
        self.type = value

    #Creating a toaster box message after transfer
    def CreateToasterBox(self, parent, msg, second, color, size=(160, 50)):
        myToasterBox = tb.ToasterBox(parent, tbstyle=tb.TB_COMPLEX, windowstyle=tb.TB_CAPTION, scrollType=tb.TB_SCR_TYPE_FADE)
        myToasterBox.SetPopupPauseTime(99999999)
        myToasterBox.SetPopupScrollSpeed(8)

        tbPanel = myToasterBox.GetToasterBoxWindow()
        myPanel = wx.Panel(tbPanel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(myPanel, label=msg)
        txt.SetForegroundColour("Blue")
        myPanel.SetSizer(sizer)
        sizer.Add(txt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        myToasterBox.AddPanel(myPanel)

        myToasterBox.CenterOnParent()
        myToasterBox.SetPopupBackgroundColour(color)

        myToasterBox.SetPopupSize(size)

        myToasterBox.Play()

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

    # #allow only the float number type inputs
    # def NumberControl(self, event):
    #     ctrl = event.GetEventObject()
    #     value = ctrl.GetValue().strip()

    #     try:
    #         float(value)
    #         ctrl.preValue = value
    #         insertPoint = ctrl.GetInsertionPoint()
    #         ctrl.ChangeValue(value)
    #         ctrl.SetInsertionPoint(insertPoint)

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

    #Recalculate values for all circuit
    def RefreshTable(self):
        for i in range(self.numRun):
            bs = self.GetBacksight(i, 0)
            bs.SetValue(bs.GetValue())

    #Update checkbox if Established Elevation is not Empty
    def OnEstablish(self, event):
        elevation = event.GetEventObject()
        runIndex = int(elevation.GetParent().GetName())
        eleChkbx = self.GetEstablishCheckbox(runIndex, int(elevation.GetName()))
        if elevation.GetValue() != '':
            eleChkbx.Show()
        else:
            eleChkbx.Hide()
            eleChkbx.SetValue(False)
        self.Layout()

    #Update checkbox if Elevation is not Empty
    def OnElevation(self, event):
        elevation = event.GetEventObject()
        runIndex = int(elevation.GetParent().GetName())
        eleChkbx = self.GetElevationCheckbox(runIndex, int(elevation.GetName()))
        if elevation.GetValue() != '':
            eleChkbx.Show()
        else:
            eleChkbx.Hide()
            eleChkbx.SetValue(False)
        self.Layout()
        event.Skip()
    #On check elevation check box do uncheck establish check box
    def OnElevationCkbox(self, event):
        row = int(event.GetEventObject().GetName())
        run = int(event.GetEventObject().GetParent().GetName())

        if self.GetElevationCheckbox(run, row).IsChecked():
            self.GetEstablishCheckbox(run, row).SetValue(False)

    #On check establish check box do uncheck elevation check box
    def OnEstablishCkbox(self, event):
        row = int(event.GetEventObject().GetName())
        run = int(event.GetEventObject().GetParent().GetName())

        if self.GetEstablishCheckbox(run, row).IsChecked():
            self.GetElevationCheckbox(run, row).SetValue(False)



def main():
    app = wx.App()






    frame = wx.Frame(None, size=(800, 400))

    waterLevelPanel = scrolledpanel.ScrolledPanel(frame, style=wx.BORDER_NONE, size=(1, 120))
    sizer = wx.BoxSizer(wx.VERTICAL)



    wlnp = WaterLevelNotesPanel("DEBUG", False, 8, None, waterLevelPanel)
    sizer.Add(wlnp, 1, wx.EXPAND)
    waterLevelPanel.SetSizer(sizer)

    waterLevelPanel.SetupScrolling()
    waterLevelPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)


    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
