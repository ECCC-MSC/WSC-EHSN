# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
from time import strptime
import wx.lib.agw.toasterbox as tb

class ElevationTransferFrame(wx.MiniFrame):
    def __init__(self, mode, *args, **kwargs):
        super(ElevationTransferFrame, self).__init__(*args, **kwargs)
        self.mode = mode
        # self.manager = manager
        self.titleLbl = "Automatic Transfer of Stage Values to Front Page"
        self.titleDesc = """Please review if the water level readings from References and the stage readings from loggers are mapped correctly before transferring to the Stage Mmt table at the Front Page! """
        self.timeLbl = "Time"
        self.wlLbl = "Direct WL Mmts"
        self.loggerLbl = "Logger Readings"
        self.wlr1Lbl = "WLR1"
        self.wlr2Lbl = "WLR2"
        self.hg1Lbl = "HG"
        self.hg2Lbl = "HG2"
        self.transferBtnLbl = "Transfer"
        self.cancelBtnLbl = "Cancel"
        self.cwlLbl = "Corr. WL (m)"
        self.lValueLbl = "Logger Val (m)"
        self.headerHeight = 25
        self.columnLength = 10
        self.overwriteMessage = "Do you want to overwirte the logger and WL Reference?"
        self.wlrManager = self.GetParent().manager
        self.stageManager = self.wlrManager.manager.stageMeasManager
        self.Init()
        self.Show()





    def Init(self):
        self.panel = wx.Panel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        #title 
        titlePanel = wx.Panel(self.panel)
        titleSizer = wx.BoxSizer(wx.VERTICAL)
        titlePanel.SetSizer(titleSizer)
        titleTxt = wx.StaticText(titlePanel, label=self.titleLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, 50))
        # titleDescTxt = wx.StaticText(titlePanel, label=self.titleDesc, style=wx.ALIGN_CENTRE_HORIZONTAL)
        titleTxt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        titleSizer.Add(titleTxt, 1, wx.EXPAND)
        # titleSizer.Add(titleDescTxt, 1, wx.EXPAND)


        #header 
        headerPanel = wx.Panel(self.panel, style=wx.SIMPLE_BORDER)
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerPanel.SetSizer(headerSizer)
        timeTxt = wx.StaticText(headerPanel, label=self.timeLbl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        timeTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        headerSizer.Add(timeTxt, 1, wx.EXPAND|wx.BOTTOM, 5)

        #Logger Value Header
        loggerValueHeaderTxt = wx.StaticText(headerPanel, label=self.lValueLbl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        loggerValueHeaderTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        headerSizer.Add(loggerValueHeaderTxt, 1, wx.EXPAND|wx.BOTTOM, 5)


        #CWL Header
        cwlTxt = wx.StaticText(headerPanel, label=self.cwlLbl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        cwlTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        headerSizer.Add(cwlTxt, 1, wx.EXPAND|wx.BOTTOM, 5)


        #Logger Name Header
        loggerHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        loggerTxt = wx.StaticText(headerPanel, label=self.hg1Lbl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        loggerTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        loggerTxt2 = wx.StaticText(headerPanel, label=self.hg2Lbl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        loggerTxt2.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        loggerHeaderSizer.Add(loggerTxt, 1, wx.EXPAND)
        loggerHeaderSizer.Add(loggerTxt2, 1, wx.EXPAND)

        loggerNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.logger1Ctrl = wx.TextCtrl(headerPanel, value=self.wlrManager.loggerLabelCtrl, size=(self.columnLength, 20))
        self.logger2Ctrl = wx.TextCtrl(headerPanel, size=(self.columnLength, 20))
        if self.stageManager.stageLabelCtrl2 == self.wlrManager.loggerLabelCtrl:
            self.logger1Ctrl.SetValue("")
            self.logger2Ctrl.SetValue(self.wlrManager.loggerLabelCtrl)


        bms = self.wlrManager.GetBMs()

        # logger1Cbbox= wx.ComboBox(headerPanel, choices=bms, value=self.stageManager.stageLabelCtrl1, style=wx.CB_DROPDOWN, size=(self.columnLength, 20))
        # logger2Cbbox= wx.ComboBox(headerPanel, choices=bms, value=self.stageManager.stageLabelCtrl2, style=wx.CB_DROPDOWN, size=(self.columnLength, 20))
        loggerNameSizer.Add(self.logger1Ctrl, 1, wx.EXPAND)
        loggerNameSizer.Add(self.logger2Ctrl, 1, wx.EXPAND)

        loggerSizer = wx.BoxSizer(wx.VERTICAL)
        loggerSizer.Add(loggerHeaderSizer, 1, wx.EXPAND)
        loggerSizer.Add(loggerNameSizer, 1, wx.EXPAND)
        headerSizer.Add(loggerSizer, 2, wx.EXPAND|wx.BOTTOM, 5)


        #WL Name Header
        wlTxt = wx.StaticText(headerPanel, label=self.wlLbl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        wlTxt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        wlNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        # wl1Ctrl = wx.TextCtrl(headerPanel, size=(self.columnLength, 20))
        # wl2Ctrl = wx.TextCtrl(headerPanel, size=(self.columnLength, 20))
        self.wl1Cbbox= wx.ComboBox(headerPanel, choices=bms, style=wx.CB_DROPDOWN, size=(self.columnLength, 20))
        self.wl2Cbbox= wx.ComboBox(headerPanel, choices=bms, style=wx.CB_DROPDOWN, size=(self.columnLength, 20))
        
        wlNames = self.wlrManager.GetSelectedWLRNames()
        if len(wlNames) == 1:
            if wlNames[0] == self.stageManager.bmRight:
                self.wl2Cbbox.SetValue(wlNames[0])
            else:
                self.wl1Cbbox.SetValue(wlNames[0])
        elif len(wlNames) == 2:
            if wlNames[0] == self.stageManager.bmRight or wlNames[1] == self.stageManager.bmLeft:
                self.wl2Cbbox.SetValue(wlNames[0])
                self.wl1Cbbox.SetValue(wlNames[1])
            else:
                self.wl2Cbbox.SetValue(wlNames[1])
                self.wl1Cbbox.SetValue(wlNames[0])


        wlNameSizer.Add(self.wl1Cbbox, 1, wx.EXPAND)
        wlNameSizer.Add(self.wl2Cbbox, 1, wx.EXPAND)

        wlSizer = wx.BoxSizer(wx.VERTICAL)
        wlSizer.Add(wlTxt, 1, wx.EXPAND)
        wlSizer.Add(wlNameSizer, 1, wx.EXPAND)
        headerSizer.Add(wlSizer, 2, wx.EXPAND|wx.BOTTOM, 5)

        #list panel contains all the selected stations


        


        self.listPanel = wx.Panel(self.panel, style=wx.NO_BORDER)
        self.listSizer = wx.BoxSizer(wx.VERTICAL)
        self.listPanel.SetSizer(self.listSizer) 

        


        selectedList = self.wlrManager.GetSelectedList()
        loggerLabelCtrl = self.wlrManager.loggerLabelCtrl


        for i in selectedList:

            self.AddRow(str(i), self.wlrManager.GetWLRefVal(i), loggerLabelCtrl, \
                self.wlrManager.GetTimeVal(i), self.wlrManager.GetCwlVal(i), self.wlrManager.GetLoggerReadingVal(i))


        #button
        buttonPanel = wx.Panel(self.panel)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonPanel.SetSizer(buttonSizer)
        transferBtn = wx.Button(buttonPanel, label=self.transferBtnLbl)
        transferBtn.Bind(wx.EVT_BUTTON, self.OnTransfer)
        cancelBtn = wx.Button(buttonPanel, label=self.cancelBtnLbl)
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        buttonSizer.Add(transferBtn, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 50)
        buttonSizer.Add(cancelBtn, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 50)

        self.sizer.Add(titlePanel, 1, wx.EXPAND)
        self.sizer.Add(headerPanel,1, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        self.sizer.Add(self.listPanel, 2, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        self.sizer.Add(buttonPanel, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)

        self.Bind(wx.EVT_CLOSE, self.OnCancel)

    def AddRow(self, name, wlName, loggerName, time, cwl, lv):
        
        hg2 = self.stageManager.stageLabelCtrl2
        wlr2 = self.stageManager.bmRight

        newPanel = wx.Panel(self.listPanel, style=wx.NO_BORDER, name=name)
        newSizer = wx.BoxSizer(wx.HORIZONTAL)
        newPanel.SetSizer(newSizer)

        subPanel1 = wx.Panel(newPanel, style=wx.SIMPLE_BORDER)
        subSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        subPanel1.SetSizer(subSizer1)
        subPanel2 = wx.Panel(newPanel, style=wx.SIMPLE_BORDER)
        subSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        subPanel2.SetSizer(subSizer2)
        subPanel3 = wx.Panel(newPanel, style=wx.SIMPLE_BORDER)
        subSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        subPanel3.SetSizer(subSizer3)
        subPanel4 = wx.Panel(newPanel, style=wx.SIMPLE_BORDER)
        subSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        subPanel4.SetSizer(subSizer4)
        subPanel5 = wx.Panel(newPanel, style=wx.SIMPLE_BORDER)
        subSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        subPanel5.SetSizer(subSizer5)

        timeTxt = wx.StaticText(subPanel1, label=time, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        correctedWLTxt = wx.StaticText(subPanel4, label=cwl, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        loggerValueTxt = wx.StaticText(subPanel5, label=lv, style=wx.ALIGN_LEFT, size=(self.columnLength * 2, self.headerHeight))
        wlrCkbox1 = wx.CheckBox(subPanel2, size=(self.columnLength, 20), name="1")
        wlrCkbox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        wlrCkbox2 = wx.CheckBox(subPanel2, size=(self.columnLength, 20), name="2")
        wlrCkbox2.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        loggerCkbox1 = wx.CheckBox(subPanel3, size=(self.columnLength, 20), name="1")
        loggerCkbox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        loggerCkbox2 = wx.CheckBox(subPanel3, size=(self.columnLength, 20), name="2")
        loggerCkbox2.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        # wx.CheckListBox(self, size=(-1, 45), choices=[self.adcpByMovingBoatLbl, self.midsectionLbl], style=wx.LB_SINGLE)


        if loggerName == hg2 and loggerName != '':
            loggerCkbox2.SetValue(True)
        else:
            loggerCkbox1.SetValue(True)

        if wlName == wlr2 and wlName != '':
            wlrCkbox2.SetValue(True)
        else:
            wlrCkbox1.SetValue(True)


        subSizer1.Add(timeTxt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        subSizer4.Add(correctedWLTxt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        subSizer5.Add(loggerValueTxt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        subSizer2.Add(wlrCkbox1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        subSizer2.Add(wlrCkbox2, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        subSizer3.Add(loggerCkbox1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        subSizer3.Add(loggerCkbox2, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        newSizer.Add(subPanel1, 1, wx.EXPAND)
        newSizer.Add(subPanel5, 1, wx.EXPAND)
        newSizer.Add(subPanel4, 1, wx.EXPAND)
        newSizer.Add(subPanel3, 2, wx.EXPAND)
        newSizer.Add(subPanel2, 2, wx.EXPAND)

        self.listSizer.Add(newPanel, 0, wx.EXPAND)

    def GetIndex(self):
        result = []
        for child in self.listSizer.GetChildren():
            result.append(int(child.GetWindow().GetName()))
        return result


    def OnTransfer(self, evt):
        if self.stageManager.stageLabelCtrl1 != self.logger1Ctrl.GetValue() or self.stageManager.stageLabelCtrl2 != self.logger2Ctrl.GetValue() or \
        self.stageManager.bmLeft != self.wl1Cbbox.GetValue() or self.stageManager.bmRight != self.wl2Cbbox.GetValue():
            dlg = wx.MessageDialog(self, self.overwriteMessage, 'None', wx.YES_NO|wx.CANCEL)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                self.OverwriteNamesOnFrontPage()
            elif res == wx.ID_CANCEL:
                dlg.Destroy()
                return
        self.Transfer()

    def OverwriteNamesOnFrontPage(self):
        self.stageManager.stageLabelCtrl1 = self.logger1Ctrl.GetValue()
        self.stageManager.stageLabelCtrl2 = self.logger2Ctrl.GetValue()
        self.stageManager.bmLeft = self.wl1Cbbox.GetValue()
        self.stageManager.bmRight = self.wl2Cbbox.GetValue()

    def Transfer(self):
        indexList = self.GetIndex()
        for index in indexList:

            time = self.wlrManager.GetTimeVal(index)
            wlValue = self.wlrManager.GetCwlVal(index)
            loggerValue = self.wlrManager.GetLoggerReadingVal(index)

            # timeCtrl = strptime(time, "%H:%M")


            rowPanel = self.GetRowByName(index)
            wlCkbox1 = rowPanel.GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(0).GetWindow().GetValue()
            wlCkbox2 = rowPanel.GetSizer().GetItem(2).GetWindow().GetSizer().GetItem(1).GetWindow().GetValue()
            loggerCkbox1 = rowPanel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(0).GetWindow().GetValue()
            loggerCkbox2 = rowPanel.GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(1).GetWindow().GetValue()

            if wlCkbox1:
                if loggerCkbox1:
                    self.wlrManager.TransferToStageMeasurement(time, loggerValue, None, wlValue, None)

                elif loggerCkbox2:
                    self.wlrManager.TransferToStageMeasurement(time, None, loggerValue, wlValue, None)

                else:
                    self.wlrManager.TransferToStageMeasurement(time, None, None, wlValue, None)

            elif wlCkbox2:
                if loggerCkbox1:
                    self.wlrManager.TransferToStageMeasurement(time, loggerValue, None, None, wlValue)

                elif loggerCkbox2:
                    self.wlrManager.TransferToStageMeasurement(time, None, loggerValue, None, wlValue)

                else:
                    self.wlrManager.TransferToStageMeasurement(time, None, None, None, wlValue)

            else:
                if loggerCkbox1:
                    self.wlrManager.TransferToStageMeasurement(time, loggerValue, None, None, None)
                elif loggerCkbox2:
                    self.wlrManager.TransferToStageMeasurement(time, None, loggerValue, None, None)
                else:
                    break
        self.GetParent().miniFrame = None
        if len(indexList) > 0:
            self.GetParent().CreateToasterBox()

        self.Destroy()

    def GetRowByName(self, name):
        for child in self.listSizer.GetChildren():
            if child.GetWindow().GetName() == str(name):
                return child.GetWindow()

    def OnCancel(self, event):
        self.GetParent().miniFrame = None
        self.Destroy()


    def OnCheckBox(self, event):
        cb = event.GetEventObject()
        parent = cb.GetParent()
        if cb.IsChecked():
            if cb.GetName() == "1":
                parent.GetSizer().GetItem(1).GetWindow().SetValue(False)
            else:
                parent.GetSizer().GetItem(0).GetWindow().SetValue(False)





        # wx.CallAfter(self.SetFocus)


