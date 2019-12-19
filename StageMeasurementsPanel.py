# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import wx.lib.masked as masked
import wx.lib.scrolledpanel as scrolledpanel
from time import strptime
# import wx.combo as cb
from wx import ComboPopup
import datetime
# import wx.core as cb
# import wx.ComboPopup as cb
import NumberControl
from DropdownTime import *



#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

##This class is taken from wxPython demo
##https://github.com/wxWidgets/wxPython/blob/master/demo/ComboCtrl.py
class ComboCtrlPopup(wx.ListCtrl, ComboPopup):
    def __init__(self):
        self.PostCreate(wx.PreListCtrl())

        ComboPopup.__init__(self)


    def AddItem(self, txt):
        self.InsertStringItem(self.GetItemCount(), txt)

    def AddItems(self, lis):
        for txt in lis:
            self.AddItem(txt)

    def OnMotion(self, evt):
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:
            self.Select(item)
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
        wx.ListCtrl.Create(self, parent,
                           style=wx.LC_LIST|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_Left_DOWN, self.OnLeftDown)
        return True


    # Return the widget that is to be used for the popup
    def GetControl(self):
        #self.log.write("ListCtrlComboPopup.GetControl")
        return self

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        ComboPopup.OnPopup(self)
        self.SetFocus()




class StageMeasurementsPanel(wx.Panel):
    def __init__(self, mode, lang, *args, **kwargs):
        super(StageMeasurementsPanel, self).__init__(*args, **kwargs)

        self.timeTxtLbl = "Time"
        self.stageTxtLbl = "HG"
        self.stageTxtLbl2 = "HG2"
        self.levelTxtLbl = "Water Level Reference"
        self.sensorResetTxtLbl = "Sensor Reset Correction"
        self.sensorResetAppTxtLbl = "Action Taken"
        self.weightedMghTxtLbl = "Weighted M.G.H."
        self.srcTxtLbl = "S.R.C."
        self.gcTxtLbl = "Gauge Correction"
        self.correctedMghTxtLbl = "Corrected M.G.H. (m)"
        self.mghAggregationLbl = "M.G.H. Aggr."
        self.mghAggregationChoices = ["", "HG", "HG2", "WLR1", "WLR2"]
        self.mghMethodLbl = "       MGH Aggr.\n        Method:"
        self.mghMethods = ["", "Average", "Time-weighted"]
        self.references = [""]
        self.srcChoices = ['', 'Reset (RS)', 'No Reset (NR)', 'Flushed (FL)', 'Found (FD)', 'Purged  (PU)', 'Recovered (RC)', 'Maintenance (MT)', 'G.C. Applied (GCA)', 'CTRL Cleared (CC)', 'DWL', 'Changed Tank (CT)']
        self.BMs = []
        self.mghCalBtnLbl = "Calculate M.G.H."
        self.factors = ""
        self.incompleteDischargeTimeMsg = """The discharge mmt time is not complete. As a result, the MGH calculation has not
                     taken the discharge mmt time into account."""
        self.incompleteDischargeTimeTitle = "Warning"
        self.stageLbl = "Stage Activity\nSummary Remarks"
        self.checkDischargeTime = True

        self.frame = self.GetParent()
        self.size = self.frame.GetSize()
        self.colHeaderHeight = 48 * 1.3
        self.colHeaderWidth = 38
        self.rowHeight = 28
        self.wrapLength = self.colHeaderWidth * 2
        self.entryNum = 0
        self.hgButton = True


        self.weightMGHBtnHint = "*Always enter Weighted M.G.H even if its the same as Corrected M.G.H.*\nYou should always\
enter Weighted M.G.H even if it is the same as Corrected M.G.H since Corrected M.G.H. is automatically calculated \
in Aquarius.\n\n 1. The value of the Weighted M.G.H. + S.R.C. is put in the 'Observed Value' column of the Discharge \
Activity table in Aquarius\n2. The Gauge Correction is put in the 'Correction' column in Aquarius\n3. Aquarius adds \
these numbers together to get the Corrected M.G.H.\n\nSince Corrected M.G.H. is auto-calculated in Aquarius and will \
be available in Aquarius, it is NOT uploaded from the Corrected M.G.H. field here."
        # self.correctMGHBtnHint = "Corrected MGH is not directly uploaded to Aquarius, ensure values are entered as Weighted MGH + S.R.C. and Gauge Correction."


        self.mode=mode
        self.manager = None

        self.lang = lang
        self.InitUI()

    #convert to upper case
    def OnTextType(self, event):

        textCtr=event.GetEventObject()
        insertPoint = textCtr.GetInsertionPoint()
        # textCtr.ChangeValue(unicode.upper(textCtr.GetValue()))
        textCtr.SetInsertionPoint(insertPoint)
        # while True:
        # 	raise Exception('I know Python!')

        event.Skip()









    def InitUI(self):
        if self.mode=="DEBUG":
            print "In StageMeasurementsPanel"

        self.layoutSizerV = wx.BoxSizer(wx.VERTICAL)
        self.locale = wx.Locale(self.lang)

        #Measurements Panel
        self.measurementsScrollPanel = scrolledpanel.ScrolledPanel(self, size=(-1, 200), style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.measurementsScrollPanel.SetupScrolling()
        self.measurementsScrollPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        self.measurementsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.measurementsSizerV = wx.BoxSizer(wx.VERTICAL)


        #Entry Adding Column
        self.entryColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.entryColumnPanel = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)

        entryColPanel = wx.Panel(self.entryColumnPanel, style=wx.SIMPLE_BORDER)
        wx.StaticText(entryColPanel, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.rowHeight, self.colHeaderHeight))

        #For dynamically added entries
        self.entryColButtonPanel = wx.Panel(self.entryColumnPanel, style=wx.SIMPLE_BORDER)
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
        self.entryColumnPanel.SetSizer(self.entryColumnSizer)


        #Time column
        self.timeColumnSizer = wx.BoxSizer(wx.VERTICAL)

        timeLabelPanel = wx.Panel(self.measurementsScrollPanel, style=wx.SIMPLE_BORDER)
        timeLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeLabelPanel.SetSizer(timeLabelSizer)

        timeLabelTxt = wx.StaticText(timeLabelPanel, label=self.timeTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
##        timeLabelTxt.Wrap(self.wrapLength)
        timeLabelSizer.Add(timeLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.timeValPanel = wx.Panel(self.measurementsScrollPanel, style=wx.SIMPLE_BORDER)
        self.timeValSizer = wx.BoxSizer(wx.VERTICAL)
        self.timeValPanel.SetSizer(self.timeValSizer)

        #Add all to the Time
        self.timeColumnSizer.Add(timeLabelPanel, 0, wx.EXPAND)
        self.timeColumnSizer.Add(self.timeValPanel, 0, wx.EXPAND)









        #Stage column 1
        self.stageColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.stageColumnSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.stageColumnPanel = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)

        stageLabelPanel = wx.Panel(self.stageColumnPanel, style=wx.SIMPLE_BORDER)
        stageLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        stageLabelSizerV = wx.BoxSizer(wx.VERTICAL)
        stageLabelPanel.SetSizer(stageLabelSizer)

        stageLabelTxt = wx.StaticText(stageLabelPanel, label=self.stageTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight / 2))
        stageLabelTxt.Wrap(self.wrapLength)

        # self.hgCkbox = wx.CheckBox(stageLabelPanel)
        # self.hgCkbox.Bind(wx.EVT_CHECKBOX, self.OnHGCalculateMGH)


        # self.stageLabelBtn = wx.Button(stageLabelPanel, label=self.stageTxtLbl, style=wx.BU_TOP, size=(self.colHeaderWidth, self.colHeaderHeight / 2))
        # self.stageLabelBtn.Bind(wx.EVT_BUTTON, self.OnHGButton)
        # self.stageLabelBtn.SetBackgroundColour('yellow')
        self.stageLabelCtrl1 = wx.TextCtrl(stageLabelPanel, style=wx.TE_PROCESS_ENTER, size=(self.colHeaderWidth, self.colHeaderHeight / 2))
        self.stageLabelCtrl1.Bind(wx.EVT_TEXT, self.OnTextType)
        self.stageLabelCtrl1.Bind(wx.EVT_KEY_DOWN, self.OnTab)

        stageLabelSizerV.Add(stageLabelTxt, 0, wx.EXPAND)
        stageLabelSizerV.Add(self.stageLabelCtrl1, 0, wx.EXPAND)
        # stageLabelSizerV.Add(self.hgCkbox, 0, wx.EXPAND|wx.LEFT, 20)
        stageLabelSizer.Add(stageLabelSizerV, 1, wx.EXPAND)

        #Create new panel and sizer for dynamically items
        self.stagePanel = wx.Panel(self.stageColumnPanel, style=wx.SIMPLE_BORDER, name="hg")
        self.stageSizer = wx.BoxSizer(wx.VERTICAL)
        self.stagePanel.SetSizer(self.stageSizer)

        self.stageColumnSizer.Add(stageLabelPanel, 0, wx.EXPAND)
        self.stageColumnSizer.Add(self.stagePanel, 0, wx.EXPAND)
        self.stageColumnSizerH.Add(self.stageColumnSizer, 1, wx.EXPAND)

        self.stageColumnPanel.SetSizer(self.stageColumnSizerH)


        #Stage Column 2
        self.stageColumnSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.stageColumnSizerH2 = wx.BoxSizer(wx.HORIZONTAL)
        self.stageColumnPanel2 = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)

        stageLabelPanel2 = wx.Panel(self.stageColumnPanel2, style=wx.SIMPLE_BORDER)
        stageLabelSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        stageLabelSizer2V = wx.BoxSizer(wx.VERTICAL)
        stageLabelPanel2.SetSizer(stageLabelSizer2)

        stageLabelTxt2 = wx.StaticText(stageLabelPanel2, label=self.stageTxtLbl2, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight / 2))
        stageLabelTxt2.Wrap(self.wrapLength)
        # self.hg2Ckbox = wx.CheckBox(stageLabelPanel2)
        # self.hg2Ckbox.Bind(wx.EVT_CHECKBOX, self.OnHG2CalculateMGH)
        # self.stageLabelBtn2 = wx.Button(stageLabelPanel2, label=self.stageTxtLbl2, style=wx.BU_TOP, size=(self.colHeaderWidth, self.colHeaderHeight / 2))
        # self.stageLabelBtn2.Bind(wx.EVT_BUTTON, self.OnHGButton)
        self.stageLabelCtrl2 = wx.TextCtrl(stageLabelPanel2, style=wx.TE_PROCESS_ENTER, size=(self.colHeaderWidth, self.colHeaderHeight / 2))
        self.stageLabelCtrl2.Bind(wx.EVT_TEXT, self.OnTextType)

        self.stageLabelCtrl2.Bind(wx.EVT_KEY_DOWN, self.OnTab)

        # for i in self.stageLabelCtrl1.GetParent().GetParent().GetChildren():
        #     for p in i.GetChildren():
        #         print type(p)
        # self.stageLabelCtrl1.MoveAfterInTabOrder(self.stageLabelCtrl2)



        stageLabelSizer2V.Add(stageLabelTxt2, 0, wx.EXPAND)
        stageLabelSizer2V.Add(self.stageLabelCtrl2, 0, wx.EXPAND)
        # stageLabelSizer2V.Add(self.hg2Ckbox, 0, wx.EXPAND|wx.LEFT, 20)
        stageLabelSizer2.Add(stageLabelSizer2V, 1, wx.EXPAND)

        #Create new panel and sizer for dynamically items
        self.stagePanel2 = wx.Panel(self.stageColumnPanel2, style=wx.SIMPLE_BORDER, name="hg2")
        self.stageSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.stagePanel2.SetSizer(self.stageSizer2)

        self.stageColumnSizer2.Add(stageLabelPanel2, 0, wx.EXPAND)
        self.stageColumnSizer2.Add(self.stagePanel2, 0, wx.EXPAND)
        self.stageColumnSizerH2.Add(self.stageColumnSizer2, 1, wx.EXPAND)

        self.stageColumnPanel2.SetSizer(self.stageColumnSizerH2)


        #W.L Reference column
        self.wlColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.wlColumnSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.wlColumnPanel = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)

        wlLabelPanel = wx.Panel(self.wlColumnPanel, style=wx.SIMPLE_BORDER)
        wlLabelSizer = wx.BoxSizer(wx.VERTICAL)

        self.wlSublabelPanelL = wx.Panel(wlLabelPanel, style=wx.BORDER_NONE)
        self.wlSublabelPanelLSizer = wx.BoxSizer(wx.VERTICAL)
        self.wlSublabelPanelL.SetSizer(self.wlSublabelPanelLSizer)
        # self.wlr1Ckbox = wx.CheckBox(self.wlSublabelPanelL)
        # self.wlr1Ckbox.Bind(wx.EVT_CHECKBOX, self.OnWlr1CalculateMGH)

        self.wlSublabelPanelR = wx.Panel(wlLabelPanel, style=wx.BORDER_NONE, size=(-1, self.colHeaderHeight/2))
        self.wlSublabelPanelRSizer = wx.BoxSizer(wx.VERTICAL)
        self.wlSublabelPanelR.SetSizer(self.wlSublabelPanelRSizer)
        # self.wlr2Ckbox = wx.CheckBox(self.wlSublabelPanelR)
        # self.wlr2Ckbox.Bind(wx.EVT_CHECKBOX, self.OnWlr2CalculateMGH)



        self.bmLeft = wx.ComboBox(self.wlSublabelPanelL, choices=self.BMs, style=wx.CB_DROPDOWN, size=(self.colHeaderWidth + 10, self.colHeaderHeight/2))
        # self.bmLeft = wx.TextCtrl(self.wlSublabelPanelL, size=(self.colHeaderWidth + 10, self.colHeaderHeight/2))
        self.bmLeft.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        




        self.bmLeft.Bind(wx.EVT_TEXT, self.OnTextType)
        self.bmLeft.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        self.wlSublabelPanelLSizer.Add(self.bmLeft, 1, wx.EXPAND)
        # self.wlSublabelPanelLSizer.Add(self.wlr1Ckbox, 0, wx.EXPAND|wx.LEFT, 20)


        self.bmRight = wx.ComboBox(self.wlSublabelPanelR, choices=self.BMs, style=wx.CB_DROPDOWN, size=(self.colHeaderWidth + 10, self.colHeaderHeight/2))
        self.bmRight.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)


        




        self.bmRight.Bind(wx.EVT_TEXT, self.OnTextType)
        self.bmRight.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        
        self.wlSublabelPanelRSizer.Add(self.bmRight, 1, wx.EXPAND)
        # self.wlSublabelPanelRSizer.Add(self.wlr2Ckbox, 0, wx.EXPAND|wx.LEFT, 20)

        self.wlSublabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wlSublabelSizer.Add(self.wlSublabelPanelL, 1, wx.EXPAND)
        self.wlSublabelSizer.Add(self.wlSublabelPanelR, 1, wx.EXPAND)

        wlLabelTxt = wx.StaticText(wlLabelPanel, label=self.levelTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 22, self.colHeaderHeight/2))
        wlLabelTxt.Wrap(self.wrapLength * 2)

        wlLabelSizer.Add(wlLabelTxt, 1, wx.EXPAND)
        wlLabelSizer.Add(self.wlSublabelSizer, 1, wx.EXPAND)
        wlLabelPanel.SetSizer(wlLabelSizer)


        #Create panel for dynamic entries
        self.wlSizerH = wx.BoxSizer(wx.HORIZONTAL)

        self.wlSubPanelL = wx.Panel(self.wlColumnPanel, style=wx.SIMPLE_BORDER, name="wlr1")
        self.wlSubPanelR = wx.Panel(self.wlColumnPanel, style=wx.SIMPLE_BORDER, name="wlr2")
        self.wlSubSizerL = wx.BoxSizer(wx.VERTICAL)
        self.wlSubSizerR = wx.BoxSizer(wx.VERTICAL)

        self.wlSubPanelL.SetSizer(self.wlSubSizerL)
        self.wlSubPanelR.SetSizer(self.wlSubSizerR)

        self.wlSizerH.Add(self.wlSubPanelL, 1, wx.EXPAND)
        self.wlSizerH.Add(self.wlSubPanelR, 1, wx.EXPAND)

        self.wlColumnSizer.Add(wlLabelPanel, 0, wx.EXPAND)
        self.wlColumnSizer.Add(self.wlSizerH, 0, wx.EXPAND)
        self.wlColumnSizerH.Add(self.wlColumnSizer, 1, wx.EXPAND)

        self.wlColumnPanel.SetSizer(self.wlColumnSizerH)


        #SRC column
        self.srcColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.srcColumnSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.srcColumnPanel = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)

        srcLabelPanel = wx.Panel(self.srcColumnPanel, style=wx.SIMPLE_BORDER)
        srcLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        srcLabelPanel.SetSizer(srcLabelSizer)

        srcTxt = wx.StaticText(srcLabelPanel, label=self.sensorResetTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth * 1.4, self.colHeaderHeight))
        srcTxt.Wrap(self.wrapLength)
        srcLabelSizer.Add(srcTxt, 1, wx.EXPAND)

        #Create Panel for dynamic entries
        self.srcPanel = wx.Panel(self.srcColumnPanel, style=wx.SIMPLE_BORDER)
        self.srcSizer = wx.BoxSizer(wx.VERTICAL)
        self.srcPanel.SetSizer(self.srcSizer)

        self.srcColumnSizer.Add(srcLabelPanel, 0, wx.EXPAND)
        self.srcColumnSizer.Add(self.srcPanel, 0, wx.EXPAND)
        self.srcColumnSizerH.Add(self.srcColumnSizer, 1, wx.EXPAND)

        self.srcColumnPanel.SetSizer(self.srcColumnSizerH)


        #SRC Applied Column
        self.srcAppColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.srcAppColumnSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.srcAppColumnPanel = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)

        srcAppLabelPanel = wx.Panel(self.srcAppColumnPanel, style=wx.SIMPLE_BORDER)
        srcAppLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        srcAppLabelPanel.SetSizer(srcAppLabelSizer)

        srcAppTxt = wx.StaticText(srcAppLabelPanel, label=self.sensorResetAppTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight))
        srcAppTxt.Wrap(self.wrapLength / 1.4)
        srcAppLabelSizer.Add(srcAppTxt, 1, wx.EXPAND)


        #Create Panel for dynamic entries
        self.srcAppPanel = wx.Panel(self.srcAppColumnPanel, style=wx.SIMPLE_BORDER)
        self.srcAppSizer = wx.BoxSizer(wx.VERTICAL)
        self.srcAppPanel.SetSizer(self.srcAppSizer)

        self.srcAppColumnSizer.Add(srcAppLabelPanel, 0, wx.EXPAND)
        self.srcAppColumnSizer.Add(self.srcAppPanel, 0, wx.EXPAND)
        self.srcAppColumnSizerH.Add(self.srcAppColumnSizer, 1, wx.EXPAND)

        self.srcAppColumnPanel.SetSizer(self.srcAppColumnSizerH)



        #MGH Aggregation Column
        self.mghAggColumnPanel = wx.Panel(self.measurementsScrollPanel, style=wx.BORDER_NONE)
        mghAggColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.mghAggColumnPanel.SetSizer(mghAggColumnSizer)

        #Create header panel
        mghAggHeaderSizer = wx.BoxSizer(wx.VERTICAL)
        mghAggHeaderPanel = wx.Panel(self.mghAggColumnPanel, style=wx.SIMPLE_BORDER, size=(-1, self.colHeaderHeight))
        mghAggHeaderPanel.SetSizer(mghAggHeaderSizer)

        mghAggTxt = wx.StaticText(mghAggHeaderPanel, label=self.mghAggregationLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth, self.colHeaderHeight/2))
        mghAggTxt.Wrap(self.wrapLength*2)
        # self.mghAggCombobox = wx.ComboBox(mghAggHeaderPanel, choices=sorted(self.mghAggregationChoices), value=self.mghAggregationChoices[0], style=wx.CB_READONLY, size=(self.colHeaderWidth, self.colHeaderHeight/2))
        # self.mghAggCombobox.Bind(wx.EVT_COMBOBOX, self.OnAggComboChangeMGHColor)
        mghAggHeaderSizer.Add(mghAggTxt, 1, wx.EXPAND)
        # mghAggHeaderSizer.Add(self.mghAggCombobox, 0, wx.EXPAND|wx.TOP, 5)

        #Create new panel and sizer for dynamic entries
        self.mghAggValPanel = wx.Panel(self.mghAggColumnPanel, style=wx.SIMPLE_BORDER)
        self.mghAggValSizer = wx.BoxSizer(wx.VERTICAL)
        self.mghAggValPanel.SetSizer(self.mghAggValSizer)

        mghAggColumnSizer.Add(mghAggHeaderPanel, 0, wx.EXPAND)
        mghAggColumnSizer.Add(self.mghAggValPanel, 0, wx.EXPAND)







        #Add all panels to measurementsSizer
        self.measurementsSizer.Add(self.entryColumnPanel, 0, wx.EXPAND)
        self.measurementsSizer.Add(self.timeColumnSizer, 0, wx.EXPAND)
        self.measurementsSizer.Add(self.stageColumnPanel, 5, wx.EXPAND)
        self.measurementsSizer.Add(self.stageColumnPanel2, 5, wx.EXPAND)
        self.measurementsSizer.Add(self.wlColumnPanel, 10, wx.EXPAND)
        self.measurementsSizer.Add(self.srcColumnPanel, 5, wx.EXPAND)
        self.measurementsSizer.Add(self.srcAppColumnPanel, 7, wx.EXPAND)
        self.measurementsSizer.Add(self.mghAggColumnPanel, 4, wx.EXPAND)

        self.measurementsSizerV.Add(self.measurementsSizer, 1, wx.EXPAND)
        self.measurementsScrollPanel.SetSizer(self.measurementsSizerV)


        #Pre-Summary Stuff
        preSummaryPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        preSummarySizer = wx.GridBagSizer(0, 0)
        preSummaryPanel.SetSizer(preSummarySizer)

        self.PreSummRowHeight = self.rowHeight + 3
        self.PreSummColWidth = self.colHeaderWidth
        self.SummColWidth = self.colHeaderWidth * 1.9

        weightMGHPanel = wx.Panel(preSummaryPanel, style=wx.SIMPLE_BORDER)
        weightMGHSizer = wx.BoxSizer(wx.HORIZONTAL)
        weightMGHTxt = wx.StaticText(weightMGHPanel, label=self.weightedMghTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.SummColWidth + 30, self.PreSummRowHeight + 5))
        self.weightMGHButton = wx.Button(weightMGHPanel, size=(15, self.PreSummRowHeight), label="!")
        self.weightMGHButton.Bind(wx.EVT_BUTTON, self.OnWMGHBtn)
        weightMGHSizer.Add(weightMGHTxt, 0, wx.EXPAND)
        weightMGHSizer.Add(self.weightMGHButton, 0, wx.EXPAND)
        weightMGHPanel.SetSizer(weightMGHSizer)

        srcSummPanel = wx.Panel(preSummaryPanel, style=wx.SIMPLE_BORDER)
        srcSummSizer = wx.BoxSizer(wx.HORIZONTAL)
        srcSummPanelTxt = wx.StaticText(srcSummPanel, label=self.srcTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.SummColWidth, self.PreSummRowHeight))
        srcSummSizer.Add(srcSummPanelTxt, 1, wx.EXPAND)
        srcSummPanel.SetSizer(srcSummSizer)

        gcSummPanel = wx.Panel(preSummaryPanel, style=wx.SIMPLE_BORDER)
        gcSummSizer = wx.BoxSizer(wx.HORIZONTAL)
        gcSummPanelTxt = wx.StaticText(gcSummPanel, label=self.gcTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.SummColWidth, self.PreSummRowHeight))
        gcSummSizer.Add(gcSummPanelTxt, 1, wx.EXPAND)
        gcSummPanel.SetSizer(gcSummSizer)

        corrMghPanel = wx.Panel(preSummaryPanel, style=wx.SIMPLE_BORDER)
        corrMghSizer = wx.BoxSizer(wx.HORIZONTAL)
        corrMghPanelTxt = wx.StaticText(corrMghPanel, label=self.correctedMghTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.SummColWidth, self.PreSummRowHeight))
        # self.correctMGHButton = wx.Button(corrMghPanel, size=(15, self.PreSummRowHeight), label="!")
        # self.correctMGHButton.Bind(wx.EVT_BUTTON, self.OnCMGHBtn)
        corrMghSizer.Add(corrMghPanelTxt, 1, wx.EXPAND)
        # corrMghSizer.Add(self.correctMGHButton, 0, wx.EXPAND)
        corrMghPanel.SetSizer(corrMghSizer)

        #On row by row basis
        #Weighted MGH x
        self.MGHHG = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.MGHHG2 = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))

        self.MGHWLRefL = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.MGHWLRefR = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))




        self.MGHHG.SetBackgroundColour((204,204,204))
        self.MGHHG.SetForegroundColour((0,0,204))
        self.MGHHG2.SetBackgroundColour((204,204,204))
        self.MGHHG2.SetForegroundColour((0,0,204))
        self.MGHWLRefL.SetBackgroundColour((204,204,204))
        self.MGHWLRefL.SetForegroundColour((0,0,204))
        self.MGHWLRefR.SetBackgroundColour((204,204,204))
        self.MGHWLRefR.SetForegroundColour((0,0,204))


        mghMethodTxt = wx.StaticText(preSummaryPanel, label=self.mghMethodLbl, size=(self.PreSummColWidth * 2, self.PreSummRowHeight + 7))
        self.mghMethod = wx.ComboBox(preSummaryPanel, choices=self.mghMethods, style=wx.CB_READONLY, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.mghMethod.Bind(wx.EVT_COMBOBOX, self.CalculateAllMGH)

        self.hgCkbox = wx.CheckBox(preSummaryPanel)
        self.hg2Ckbox = wx.CheckBox(preSummaryPanel)
        self.wlr1Ckbox = wx.CheckBox(preSummaryPanel)
        self.wlr2Ckbox = wx.CheckBox(preSummaryPanel)

        self.hgCkbox.Bind(wx.EVT_CHECKBOX, self.OnHGCalculateMGH)
        self.hg2Ckbox.Bind(wx.EVT_CHECKBOX, self.OnHG2CalculateMGH)
        self.wlr1Ckbox.Bind(wx.EVT_CHECKBOX, self.OnWlr1CalculateMGH)
        self.wlr2Ckbox.Bind(wx.EVT_CHECKBOX, self.OnWlr2CalculateMGH)
        # mghCalBtn = wx.Button(preSummaryPanel, label=self.mghCalBtnLbl, size=(self.PreSummColWidth, self.PreSummRowHeight))
        # mghCalBtn.Bind(wx.EVT_BUTTON, self.CalculateMGH)

        # self.MGHHG.Bind(wx.EVT_TEXT, self.OnTypeChangeColorBack)
        # self.MGHHG2.Bind(wx.EVT_TEXT, self.OnTypeChangeColorBack)
        # self.MGHWLRefL.Bind(wx.EVT_TEXT, self.OnTypeChangeColorBack)
        # self.MGHWLRefR.Bind(wx.EVT_TEXT, self.OnTypeChangeColorBack)


        # self.MGHHG.Bind(wx.EVT_TEXT, self.OnHGCol)
        # self.MGHHG2.Bind(wx.EVT_TEXT, self.OnHG2Col)
        # self.MGHWLRefL.Bind(wx.EVT_TEXT, self.OnWL1Col)
        # self.MGHWLRefR.Bind(wx.EVT_TEXT, self.OnWL2Col)


        #SRC x
        self.SRCHG = MyTextCtrl(preSummaryPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.SRCHG2 = MyTextCtrl(preSummaryPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))



        #GC x
        self.GCHG = MyTextCtrl(preSummaryPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.GCHG2 = MyTextCtrl(preSummaryPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.GCWLRefL = MyTextCtrl(preSummaryPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))
        self.GCWLRefR = MyTextCtrl(preSummaryPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight))


        #Corrected Mean gauge Height x
        self.CMGHHG = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight), name="HG1")
        # self.CMGHHG = wx.StaticText(preSummaryPanel, size=(self.PreSummColWidth, self.PreSummRowHeight))

        self.CMGHHG2 = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight), name="HG2")
        self.CMGHWLRefL = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight), name="WLR1")
        self.CMGHWLRefR = MyTextCtrl(preSummaryPanel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(self.PreSummColWidth, self.PreSummRowHeight), name="WLR2")

        self.CMGHHG.SetBackgroundColour((204,204,204))
        self.CMGHHG.SetForegroundColour((0,0,204))
        self.CMGHHG2.SetBackgroundColour((204,204,204))
        self.CMGHHG2.SetForegroundColour((0,0,204))
        self.CMGHWLRefL.SetBackgroundColour((204,204,204))
        self.CMGHWLRefL.SetForegroundColour((0,0,204))
        self.CMGHWLRefR.SetBackgroundColour((204,204,204))
        self.CMGHWLRefR.SetForegroundColour((0,0,204))


        # self.MGHHG.Enable(False)
        # self.MGHHG2.Enable(False)
        # self.MGHWLRefL.Enable(False)
        # self.MGHWLRefR.Enable(False)
        # self.CMGHHG.Enable(False)
        # self.CMGHHG2.Enable(False)
        # self.CMGHWLRefL.Enable(False)
        # self.CMGHWLRefR.Enable(False)


        stageRemarkPanel = wx.Panel(preSummaryPanel, style=wx.SIMPLE_BORDER, size=(-1, -1))
        stageRemarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        stageRemarkPanel.SetSizer(stageRemarkSizer)
        stageTxt = wx.StaticText(stageRemarkPanel, label=self.stageLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(120, -1))
        self.stageRemarksCtrl = wx.TextCtrl(stageRemarkPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, self.PreSummRowHeight * 1.7))
        stageRemarkSizer.Add(stageTxt, 0)
        stageRemarkSizer.Add(self.stageRemarksCtrl, 1, wx.EXPAND)




        #Bind rounding
        # self.MGHHG.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # self.MGHHG2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # self.MGHWLRefL.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # self.MGHWLRefR.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        self.SRCHG.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.SRCHG2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        self.GCHG.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.GCHG2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.GCWLRefL.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.GCWLRefR.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        # self.CMGHHG.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # self.CMGHHG2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # self.CMGHWLRefL.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        # self.CMGHWLRefR.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)



        #Bind corrected MGH calculation
        self.MGHHG.Bind(wx.EVT_KILL_FOCUS, self.OnHGCol)
        self.MGHHG2.Bind(wx.EVT_KILL_FOCUS, self.OnHG2Col)
        self.MGHWLRefL.Bind(wx.EVT_KILL_FOCUS, self.OnWL1Col)
        self.MGHWLRefR.Bind(wx.EVT_KILL_FOCUS, self.OnWL2Col)

        self.SRCHG.Bind(wx.EVT_KILL_FOCUS, self.OnHGCol)
        self.SRCHG2.Bind(wx.EVT_KILL_FOCUS, self.OnHG2Col)

        self.GCHG.Bind(wx.EVT_KILL_FOCUS, self.OnHGCol)
        self.GCHG2.Bind(wx.EVT_KILL_FOCUS, self.OnHG2Col)
        self.GCWLRefL.Bind(wx.EVT_KILL_FOCUS, self.OnWL1Col)
        self.GCWLRefR.Bind(wx.EVT_KILL_FOCUS, self.OnWL2Col)

        #Bind float control
        self.MGHHG.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.MGHHG2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.MGHWLRefL.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.MGHWLRefR.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        self.SRCHG.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.SRCHG2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        self.GCHG.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.GCHG2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.GCWLRefL.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.GCWLRefR.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)

        self.CMGHHG.Bind(wx.EVT_TEXT, self.OnTextUpdateDischargeMGH)
        self.CMGHHG2.Bind(wx.EVT_TEXT, self.OnTextUpdateDischargeMGH)
        self.CMGHWLRefL.Bind(wx.EVT_TEXT, self.OnTextUpdateDischargeMGH)
        self.CMGHWLRefR.Bind(wx.EVT_TEXT, self.OnTextUpdateDischargeMGH)


        self.CMGHHG.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.CMGHHG2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.CMGHWLRefL.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.CMGHWLRefR.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)



        #Summary x
        #Spacers
##        preSummarySizer.Add((self.PreSummRowHeight, self.PreSummRowHeight), pos=(0, 0), span=(1, 1))
        #The SRC col is a little longer
        # preSummarySizer.Add(self.colHeaderWidth * 1.4 + 8, self.PreSummRowHeight, pos=(0, 5), span=(1, 1))
        # preSummarySizer.Add(self.colHeaderWidth, self.PreSummRowHeight, pos=(0, 6), span=(1, 1))

        preSummarySizer.Add(self.hgCkbox, pos=(0, 1), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.hg2Ckbox, pos=(0, 2), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.wlr1Ckbox, pos=(0, 3), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.wlr2Ckbox, pos=(0, 4), span=(1, 1), flag=wx.EXPAND)

        preSummarySizer.Add(weightMGHPanel, pos=(1, 0), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.MGHHG, pos=(1, 1), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.MGHHG2, pos=(1, 2), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.MGHWLRefL, pos=(1, 3), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.MGHWLRefR, pos=(1, 4), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(mghMethodTxt, pos=(1, 5), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.mghMethod, pos=(1, 6), span=(1, 3), flag=wx.EXPAND)

        preSummarySizer.Add(srcSummPanel, pos=(2, 0), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.SRCHG, pos=(2, 1), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.SRCHG2, pos=(2, 2), span=(1, 1), flag=wx.EXPAND)
        # preSummarySizer.Add(mghCalBtn, pos=(1, 7), span=(1, 2), flag=wx.EXPAND)

        preSummarySizer.Add(gcSummPanel, pos=(3, 0), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.GCHG, pos=(3, 1), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.GCHG2, pos=(3, 2), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.GCWLRefL, pos=(3, 3), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.GCWLRefR, pos=(3, 4), span=(1, 1), flag=wx.EXPAND)

        preSummarySizer.Add(corrMghPanel, pos=(4, 0), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.CMGHHG, pos=(4, 1), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.CMGHHG2, pos=(4, 2), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.CMGHWLRefL, pos=(4, 3), span=(1, 1), flag=wx.EXPAND)
        preSummarySizer.Add(self.CMGHWLRefR, pos=(4, 4), span=(1, 1), flag=wx.EXPAND)


        preSummarySizer.Add(stageRemarkPanel, pos=(5, 0), span=(1, 9), flag=wx.EXPAND)




        for i in range(1, 9):
            preSummarySizer.AddGrowableCol(i)

        for i in range(4):
            preSummarySizer.AddGrowableRow(i)


        self.layoutSizerV.Add(self.measurementsScrollPanel, 1, wx.EXPAND)
        self.layoutSizerV.Add(preSummaryPanel, 0, wx.EXPAND)

        self.SetSizer(self.layoutSizerV)

        self.layoutSizerV.Layout()
        self.Update()
        self.Refresh()


    # On '+' button click, add a new entry into the Stage Measurements
    def OnTab(self, evt):
        if evt.GetKeyCode() == wx.WXK_TAB:
            if evt.GetEventObject() == self.stageLabelCtrl1:
                self.stageLabelCtrl2.SetFocus()
            if evt.GetEventObject() == self.stageLabelCtrl2:
                self.bmLeft.SetFocus()
            if evt.GetEventObject() == self.bmLeft:
                self.bmRight.SetFocus()
            if evt.GetEventObject() == self.bmRight:
                print self.entryNum
            if evt.GetId()/100 == 2:
                for s in self.stageColumnPanel.GetChildren():
                    for t in s.GetChildren():
                        if t.GetId() == evt.GetId()%100+300:
                            t.SetFocus()
            if evt.GetId()/100 == 3:
                for s in self.stageColumnPanel2.GetChildren():
                    for t in s.GetChildren():
                        if t.GetId() == evt.GetId()%100+400:
                            t.SetFocus()
            if evt.GetId()/100 == 4:
                for s in self.wlColumnPanel.GetChildren():
                    for t in s.GetChildren():
                        if t.GetId() == evt.GetId()%100+500:
                            t.SetFocus()

            if evt.GetId()/100 == 5:
                for s in self.wlColumnPanel.GetChildren():
                    for t in s.GetChildren():
                        if t.GetId() == evt.GetId()%100+600:
                            t.SetFocus()

            if evt.GetId()/100 == 6:
                if evt.GetId()%100 < self.entryNum:
                    for s in self.stageColumnPanel.GetChildren():
                        for t in s.GetChildren():
                            if t.GetId() == evt.GetId()%100+300+1:
                                t.SetFocus()
                else:
                    self.entryColumnPanel.SetFocus()

        evt.Skip()


    def OnAddPress(self, e):
        if self.mode=="DEBUG":
            print "add"

        self.AddEntry()

    def do_nothing(self,evt):
          pass
    # Adds a row to the Stage Measurements
    # Add a new item in each of the column sizers
    # set name based on entryNum
    # name is used for deletion and ordering
    def AddEntry(self, time=None, logger1=None, logger2=None, wl1=None, wl2=None):


        #Button col
        name = "%s" % self.entryNum
        otherName = "%s" % (self.entryNum - 1)
        button = wx.Button(self.entryColButtonPanel, id=10101+self.entryNum, label="+", name=name, size=(self.rowHeight, self.rowHeight))

        oldButton = self.entryColButtonSizer.GetItem(self.entryNum-1).GetWindow()
        oldButton.SetLabel('-')
        oldButton.Unbind(wx.EVT_BUTTON)
        oldButton.Bind(wx.EVT_BUTTON, self.OnRemovePress)
        # oldButton.Bind(wx.EVT_BUTTON, self.CalculateAllMGH)

        self.entryNum += 1
        button.Bind(wx.EVT_BUTTON, self.OnAddPress)
        self.entryColButtonSizer.Add(button, 0, wx.EXPAND)


        if self.mode=="DEBUG":
            print name
        #Time col
        # tc = masked.TimeCtrl(self.timeValPanel, size=(self.colHeaderWidth, self.rowHeight), displaySeconds=False, name=otherName, style=wx.TE_CENTRE, fmt24hr=True)
        # tc.SetValue(wx.DateTime_Now().FormatTime())
        tc = DropdownTime(False, id = 200+self.entryNum, parent=self.timeValPanel, name=otherName, size=(-1, self.rowHeight))
        # tc.GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.OnTimeUpdateMGH)
        # tc.GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.OnTimeUpdateMGH)
        tc.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        tc.GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeUpdateMGH)
        tc.GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeUpdateMGH)
        tc.GetHourCtrl().Bind(wx.EVT_KEY_UP, self.OnTimeUpdateMGH)
        tc.GetMinuteCtrl().Bind(wx.EVT_KEY_UP, self.OnTimeUpdateMGH)


        tc.cBtn.Bind(wx.EVT_BUTTON, self.OnCBtn)

        # tc.Bind(wx.EVT_KILL_FOCUS, self.CalculateAllMGH)

        if time is not None:
            tc.SetValue(time)
            # print self.CompareTime(self.timeValSizer.GetItem(0).GetWindow().GetValue(), time)

        self.timeValSizer.Add(tc, 0, wx.EXPAND)


        #HG col
        hg = MyTextCtrl(self.stagePanel, id = 300+self.entryNum, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        self.stageSizer.Add(hg, 0, wx.EXPAND)

        hg.Bind(wx.EVT_TEXT, self.NumberControl)

        hg.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        hg.Bind(wx.EVT_KILL_FOCUS, self.OnHGCalculateMGH)
        hg.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        if logger1 != None:
            hg.SetValue(logger1)



        #HG col 2
        hg2 = MyTextCtrl(self.stagePanel2, id = 400+self.entryNum, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        hg2.Bind(wx.EVT_TEXT, self.NumberControl)
        hg2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        hg2.Bind(wx.EVT_KILL_FOCUS, self.OnHG2CalculateMGH)

        hg2.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        self.stageSizer2.Add(hg2, 0, wx.EXPAND)

        if logger2 != None:
            hg.SetValue(logger2)

        #wl col L
        wlL = MyTextCtrl(self.wlSubPanelL, id = 500+self.entryNum, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        wlL.Bind(wx.EVT_TEXT, self.NumberControl)
        wlL.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        wlL.Bind(wx.EVT_KILL_FOCUS, self.OnWlr1CalculateMGH)
        wlL.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        self.wlSubSizerL.Add(wlL, 0, wx.EXPAND)

        if wl1 != None:
            wlL.SetValue(wl1)

        #wl col R
        wlR = MyTextCtrl(self.wlSubPanelR, id = 600+self.entryNum, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        wlR.Bind(wx.EVT_TEXT, self.NumberControl)
        wlR.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        wlR.Bind(wx.EVT_KILL_FOCUS, self.OnWlr2CalculateMGH)
        wlR.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        self.wlSubSizerR.Add(wlR, 0, wx.EXPAND)

        if wl2 != None:
            wlR.SetValue(wl2)

        #SRC stuff
        src = MyTextCtrl(self.srcPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        # src.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        src.Bind(wx.EVT_TEXT, NumberControl.Round3)
        src.SetBackgroundColour((204,204,204))
        src.SetForegroundColour((0,0,204))
        # src.Bind(wx.EVT_TEXT, self.NumberControl)
        # src = wx.ComboBox(self.srcPanel, choices=self.srcChoices, value="", style=wx.CB_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        self.srcSizer.Add(src, 0, wx.EXPAND|wx.BOTTOM|wx.TOP)


        #SRC Applied stuff
        # srcApp = wx.CheckBox(self.srcAppPanel, style=wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        srcApp = wx.ComboBox(self.srcAppPanel, choices=sorted(self.srcChoices), value=self.srcChoices[0], style=wx.CB_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        srcApp.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)

        self.srcAppSizer.Add(srcApp, 1, wx.EXPAND|wx.BOTTOM|wx.TOP)



        #checkbox
        checkboxPanel = wx.Panel(self.mghAggValPanel, style=wx.SIMPLE_BORDER, name=otherName, size=(-1, self.rowHeight))
        checkboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        checkboxPanel.SetSizer(checkboxSizer)
        checkbox = wx.CheckBox(checkboxPanel, name=otherName, size=(15, self.rowHeight))
        checkbox.Enable(False)
        checkbox.Bind(wx.EVT_CHECKBOX, self.CalculateAllMGH)

        checkboxSizer.Add((15, -1), 0)
        checkboxSizer.Add(checkbox, 0 , wx.EXPAND)

        # checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckbox)
        self.mghAggValSizer.Add(checkboxPanel, 1, wx.EXPAND)

        self.layoutSizerV.Layout()
        self.Update()

        if self.manager is not None:
            tc.GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            tc.GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            hg.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            hg2.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            wlL.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            wlR.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            src.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            srcApp.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            checkbox.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)

        if self.entryNum > 4:
            self.Refresh()







    # When the '-' is clicked, remove that row
    def OnRemovePress(self, e):
        #Button col stuff
        button = e.GetEventObject()
        index = int(button.GetName())
        if self.mode=="DEBUG":
            print "index %s" % index

        if not self.IsEmptyRow(index):
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

        self.CalculateAllMGH(e)


    # Delete each column's item at the index of the clicked '-' button
    # Reorder the list of entries
    def RemoveEntry(self, index):
        if self.mode=="DEBUG":
            print "remove %s" % index

        self.entryColButtonSizer.Hide(index)
        self.entryColButtonSizer.Remove(index)
        self.entryNum -= 1

        #Time col stuff
        self.timeValSizer.Hide(index)
        self.timeValSizer.Remove(index)

        #HG col stuff
        self.stageSizer.Hide(index)
        self.stageSizer.Remove(index)

        #HG col stuff
        self.stageSizer2.Hide(index)
        self.stageSizer2.Remove(index)

        #WL STUFF
        self.wlSubSizerL.Hide(index)
        self.wlSubSizerL.Remove(index)
        self.wlSubSizerR.Hide(index)
        self.wlSubSizerR.Remove(index)

        #SRC stuff
        self.srcSizer.Hide(index)
        self.srcSizer.Remove(index)

        #SRC App stuff
        self.srcAppSizer.Hide(index)
        self.srcAppSizer.Remove(index)

        #MGH Agg
        self.mghAggValSizer.Hide(index)
        self.mghAggValSizer.Remove(index)

        self.RefreshSRC()

        self.RefreshName()

        self.layoutSizerV.Layout()
        self.Update()

    #Reset water level reference bench mark
    def updateBMs(self, items, indexList):


        self.bmLeft.Clear()

        self.bmRight.Clear()
        # print items
        # print indexList

        if len(indexList) > 0:
            updatedItems = []
            for i in range(len(items)):
                if i in indexList:
                    updatedItems.append(items[i])
            items = updatedItems
        else:
            items = []
        self.bmLeft.Append(items)
        self.bmRight.Append(items)
        self.wlSublabelPanelLSizer.Layout()
        self.wlSublabelPanelRSizer.Layout()
        self.Update()

    #compare two times return True if the second time greater than the first
    def CompareTime(self, time1, time2):
        time1 = strptime(time1, "%H:%M")
        time2 = strptime(time2, "%H:%M")
        if time2 > time1:
            return True
        else:
            return False
    #insert a empty line at position index
    def InsertEmptyEntry(self, index, time=None, logger1=None, logger2=None, wl1=None, wl2=None):
        self.RemoveAllEmpties()

        if index < 0:
            return
        if len(self.timeValSizer.GetChildren()) < index:
            return
        if index < len(self.timeValSizer.GetChildren()) and time is not None:
            for child in self.timeValSizer.GetChildren():
                if self.CompareTime(child.GetWindow().GetValue(), time):
                    index += 1
                else:
                    break

        #button col
        button = wx.Button(self.entryColButtonPanel, id=10101+index, label="-", name=str(index), size=(self.rowHeight, self.rowHeight))
        button.Bind(wx.EVT_BUTTON, self.OnRemovePress)
        self.entryNum += 1
        self.entryColButtonSizer.Insert(index, button, 0, wx.EXPAND)



        #Time col
        tc = DropdownTime(False, self.timeValPanel, name=str(index), size=(-1, self.rowHeight))
        # tc.GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.CalculateAllMGH)
        # tc.GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.CalculateAllMGH)

        tc.GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeUpdateMGH)
        tc.GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.OnTimeUpdateMGH)
        tc.GetHourCtrl().Bind(wx.EVT_KEY_DOWN, self.OnTimeUpdateMGH)
        tc.GetMinuteCtrl().Bind(wx.EVT_KEY_DOWN, self.OnTimeUpdateMGH)
        if time is not None:
            tc.SetValue(time)


        self.timeValSizer.Insert(index, tc, 0, wx.EXPAND)

        #HG col
        hg = MyTextCtrl(self.stagePanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=str(index))
        self.stageSizer.Insert(index, hg, 0, wx.EXPAND)
        hg.Bind(wx.EVT_TEXT, self.NumberControl)
        hg.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        hg.Bind(wx.EVT_KILL_FOCUS, self.OnHGCalculateMGH)


        #HG col 2
        hg2 = MyTextCtrl(self.stagePanel2, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=str(index))
        hg2.Bind(wx.EVT_TEXT, self.NumberControl)
        hg2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        hg2.Bind(wx.EVT_KILL_FOCUS, self.OnHG2CalculateMGH)
        self.stageSizer2.Insert(index, hg2, 0, wx.EXPAND)



        #wl col L
        wlL = MyTextCtrl(self.wlSubPanelL, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=str(index))
        wlL.Bind(wx.EVT_TEXT, self.NumberControl)
        wlL.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        wlL.Bind(wx.EVT_KILL_FOCUS, self.OnWlr1CalculateMGH)
        self.wlSubSizerL.Insert(index, wlL, 0, wx.EXPAND)



        #wl col R
        wlR = MyTextCtrl(self.wlSubPanelR, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=str(index))
        wlR.Bind(wx.EVT_TEXT, self.NumberControl)
        wlR.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        wlR.Bind(wx.EVT_KILL_FOCUS, self.OnWlr2CalculateMGH)
        self.wlSubSizerR.Insert(index, wlR, 0, wx.EXPAND)


        #SRC stuff
        src = MyTextCtrl(self.srcPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=str(index))
        # src.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        # src.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        src.Bind(wx.EVT_TEXT, NumberControl.Round3)
        src.SetBackgroundColour((204,204,204))
        src.SetForegroundColour((0,0,204))
        # src.Bind(wx.EVT_TEXT, self.NumberControl)
        # src = wx.ComboBox(self.srcPanel, choices=self.srcChoices, value="", style=wx.CB_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        self.srcSizer.Insert(index, src, 0, wx.EXPAND|wx.BOTTOM|wx.TOP)

        #SRC Applied stuff
        # srcApp = wx.CheckBox(self.srcAppPanel, style=wx.TE_CENTRE, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        srcApp = wx.ComboBox(self.srcAppPanel, choices=self.srcChoices, value=self.srcChoices[0], style=wx.CB_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=str(index))
        srcApp.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)


        self.srcAppSizer.Insert(index, srcApp, 1, wx.EXPAND|wx.BOTTOM|wx.TOP)






        #checkbox
        checkboxPanel = wx.Panel(self.mghAggValPanel, style=wx.SIMPLE_BORDER, name=str(index), size=(-1, self.rowHeight))
        checkboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        checkboxPanel.SetSizer(checkboxSizer)
        checkbox = wx.CheckBox(checkboxPanel, name=str(index), size=(15, self.rowHeight))
        checkbox.Enable(True)
        # checkbox.SetValue(True)
        checkbox.Bind(wx.EVT_CHECKBOX, self.CalculateAllMGH)

        checkboxSizer.Add((15, -1), 0)
        checkboxSizer.Add(checkbox, 0 , wx.EXPAND)
        # checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckbox)
        self.mghAggValSizer.Insert(index, checkboxPanel, 1, wx.EXPAND)


        # tc.Bind(wx.EVT_TEXT, self.OnTimeChange)
        #set the transferred value for each field
        if logger1 != None:
            hg.SetValue(logger1)
        if logger2 != None:
            hg2.SetValue(logger2)
        if wl1 != None:
            wlL.SetValue(wl1)
        if wl2 != None:
            wlR.SetValue(wl2)

        #calculate the src for the new row
        self.RefreshSRC()

        self.layoutSizerV.Layout()
        self.Update()

        if self.manager is not None:
            tc.GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            tc.GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            hg.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            hg2.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            wlL.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            wlR.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            src.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            srcApp.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            checkbox.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)


        self.Refresh()
        self.RefreshName()
        # self.PrintNames()

    def RefreshName(self):
        for index, child in enumerate(self.entryColButtonSizer.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.timeValSizer.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i!= index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.stageSizer.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.stageSizer2.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.wlSubSizerL.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.wlSubSizerR.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.srcSizer.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.srcAppSizer.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)

        for index, child in enumerate(self.mghAggValSizer.GetChildren()):
            i = int(child.GetWindow().GetName())
            if i != index:
                child.GetWindow().SetName("%s" % index)
                child.GetWindow().GetSizer().GetItem(1).GetWindow().SetName("%s" % index)


    def PrintNames(self):
        for child in self.entryColButtonSizer.GetChildren():
            print "button col" + child.GetWindow().GetName()
        for child in self.timeValSizer.GetChildren():
            print "time col" + child.GetWindow().GetName()
        for child in self.stageSizer.GetChildren():
            print "stage1 col" + child.GetWindow().GetName()
        for child in self.stageSizer2.GetChildren():
            print "stage2 col" + child.GetWindow().GetName()
        for child in self.wlSubSizerL.GetChildren():
            print "wll col" + child.GetWindow().GetName()
        for child in self.wlSubSizerR.GetChildren():
            print "wlr col" + child.GetWindow().GetName()
        for child in self.srcSizer.GetChildren():
            print "src col" + child.GetWindow().GetName()
        for child in self.srcAppSizer.GetChildren():
            print "srcApp col" + child.GetWindow().GetName()
        for child in self.mghAggValSizer.GetChildren():
            print "MGH Agg col" + child.GetWindow().GetSizer().GetItem(1).GetWindow().GetName()

    def RemoveAllEmpties(self):

        for index, child in reversed(list(enumerate(self.timeValSizer.GetChildren()))):
            # print index
            # print len(self.stageSizer.GetChildren())
            hg = self.stageSizer.GetItem(index).GetWindow().GetValue()
            hg2 = self.stageSizer2.GetItem(index).GetWindow().GetValue()
            wlL = self.wlSubSizerL.GetItem(index).GetWindow().GetValue()
            wlR = self.wlSubSizerR.GetItem(index).GetWindow().GetValue()
            if hg == '' and hg2 == '' and wlL == '' and wlR == '':
                self.RemoveEntry(index)



    #HG
    def GetStageLabelCtrl1(self):
        return self.stageLabelCtrl1.GetValue()


    def SetStageLabelCtrl1(self, stageLabelCtrl1):
        self.stageLabelCtrl1.SetValue(stageLabelCtrl1)

    #HG2
    def GetStageLabelCtrl2(self):
        return self.stageLabelCtrl2.GetValue()


    def SetStageLabelCtrl2(self, stageLabelCtrl2):
        self.stageLabelCtrl2.SetValue(stageLabelCtrl2)

    #BMLeft
    def GetBmLeft(self):
        return self.bmLeft.GetValue()

    def SetBmLeft(self, bmLeft):
        self.bmLeft.SetValue(bmLeft)

    #BMRight
    def GetBmRight(self):
        return self.bmRight.GetValue()

    def SetBmRight(self, bmRight):
        self.bmRight.SetValue(bmRight)



    #Time Val Sizer
    def GetTimeValSizer(self):
        return self.timeValSizer

    def SetTimeValSizer(self, timeValSizer):
        self.timeValSizer = timeValSizer

    #Time Val Getter
    def GetTimeVal(self, row):
        maxrow = len(self.GetTimeValSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetTimeValSizer().GetItem(row).GetWindow()
        return sizerItem.GetValue().replace(" ", "")

    #return the time panel object
    def GetTimePanel(self, row):
        maxrow = len(self.GetTimeValSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.GetTimeValSizer().GetItem(row).GetWindow()




    #Time Val Setter
    def SetTimeVal(self, row, val):
        maxrow = len(self.GetTimeValSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetTimeValSizer().GetItem(row).GetWindow()

        # time = wx.DateTime()
        # time.ParseTime(val)
        # print val
        # print time.hour
        sizerItem.SetValue(val)

    #Get hour value in string for given entry
    def GetTimeHour(self, row):
        return self.GetTimePanel(row).GetHourVal()
    #Get minute value in string for given entry
    def GetTimeMinute(self, row):
        return self.GetTimePanel(row).GetMinuteVal()



    #HG
    def GetStageSizer(self):
        return self.stageSizer

    def SetStageSizer(self, stageSizer):
        self.stageSizer = stageSizer

    #HG Val Getter
    def GetHGVal(self, row):
        maxrow = len(self.GetStageSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetStageSizer().GetItem(row).GetWindow()
        return sizerItem.GetValue()

    #HG Val Setter
    def SetHGVal(self, row, val):
        maxrow = len(self.GetStageSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetStageSizer().GetItem(row).GetWindow()
        sizerItem.SetValue(val)


    #HG2
    def GetStageSizer2(self):
        return self.stageSizer2

    def SetStageSizer2(self, stageSizer2):
        self.stageSizer2 = stageSizer2

    #HG2 Val Getter
    def GetHG2Val(self, row):
        maxrow = len(self.GetStageSizer2().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetStageSizer2().GetItem(row).GetWindow()
        return sizerItem.GetValue()

    #HG2 Val Setter
    def SetHG2Val(self, row, val):
        maxrow = len(self.GetStageSizer2().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetStageSizer2().GetItem(row).GetWindow()
        sizerItem.SetValue(val)


    #WL Col L
    def GetWlSubSizerL(self):
        return self.wlSubSizerL


    def SetWlSubSizerL(self, wlSubSizerL):
        self.wlSubSizerL = wlSubSizerL

    #WL Col L Getter
    def GetWLSubSizerLVal(self, row):
        maxrow = len(self.GetWlSubSizerL().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetWlSubSizerL().GetItem(row).GetWindow()
        return sizerItem.GetValue()

    #WL Col L Setter
    def SetWLSubSizerLVal(self, row, val):
        maxrow = len(self.GetWlSubSizerL().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetWlSubSizerL().GetItem(row).GetWindow()
        sizerItem.SetValue(val)


    #WL Col R
    def GetWlSubSizerR(self):
        return self.wlSubSizerR


    def SetWlSubSizerR(self, wlSubSizerR):
        self.wlSubSizerR = wlSubSizerR

    #WL Col R Getter
    def GetWLSubSizerRVal(self, row):
        maxrow = len(self.GetWlSubSizerR().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetWlSubSizerR().GetItem(row).GetWindow()
        return sizerItem.GetValue()

    #WL Col R Setter
    def SetWLSubSizerRVal(self, row, val):
        maxrow = len(self.GetWlSubSizerR().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetWlSubSizerR().GetItem(row).GetWindow()
        sizerItem.SetValue(val)


    #SRC col
    def GetSrcSizer(self):
        return self.srcSizer


    def SetSrcSizer(self, srcSizer):
        self.srcSizer = srcSizer

    #SRC col Getter
    def GetSrcSizerVal(self, row):
        maxrow = len(self.GetSrcSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetSrcSizer().GetItem(row).GetWindow()
        return sizerItem.GetValue()

    #SRC col Setter
    def SetSrcSizerVal(self, row, val):
        maxrow = len(self.GetSrcSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetSrcSizer().GetItem(row).GetWindow()
        sizerItem.SetValue(val)

    #SRC Applied col

    def GetSrcAppSizer(self):
        return self.srcAppSizer


    def SetSrcAppSizer(self, srcAppSizer):
        self.srcAppSizer = srcAppSizer

    #SRC Applied col Getter
    def GetSrcAppSizerVal(self, row):
        maxrow = len(self.GetSrcAppSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetSrcAppSizer().GetItem(row).GetWindow()
        return sizerItem.GetValue()

    #SRC Applied col Setter
    def SetSrcAppSizerVal(self, row, val):
        maxrow = len(self.GetSrcAppSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.GetSrcAppSizer().GetItem(row).GetWindow()
        sizerItem.SetValue(val)

    #mgh Aggregation
    def GetMghAggSizer(self):
        return self.mghAggValSizer

    def GetMghAggCheckbox(self, row):
        maxrow = len(self.GetMghAggSizer().GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        return self.GetMghAggSizer().GetItem(row).GetWindow().GetSizer().GetItem(1).GetWindow()




    #Weight MGH x
    #MGH x HG

    def GetMGHHG(self):
        return self.MGHHG.GetValue()


    def SetMGHHG(self, MGHHG):
        self.MGHHG.SetValue(MGHHG)

    #MGH x HG2
    def GetMGHHG2(self):
        return self.MGHHG2.GetValue()


    def SetMGHHG2(self, MGHHG2):
        self.MGHHG2.SetValue(MGHHG2)

    #MGH x WLRefL
    def GetMGHWLRefL(self):
        return self.MGHWLRefL.GetValue()


    def SetMGHWLRefL(self, MGHWLRefL):
        self.MGHWLRefL.SetValue(MGHWLRefL)

    #MGH x WLRefR
    def GetMGHWLRefR(self):
        return self.MGHWLRefR.GetValue()

    def SetMGHWLRefR(self, MGHWLRefR):
        self.MGHWLRefR.SetValue(MGHWLRefR)


    #SRC x
    #SRC x HG
    def GetSRCHG(self):
        return self.SRCHG.GetValue()


    def SetSRCHG(self, SRCHG):
        self.SRCHG.SetValue(SRCHG)

    #SRC x HG2
    def GetSRCHG2(self):
        return self.SRCHG2.GetValue()


    def SetSRCHG2(self, SRCHG2):
        self.SRCHG2.SetValue(SRCHG2)



    #GC x
    #GC x HG
    def GetGCHG(self):
        return self.GCHG.GetValue()


    def SetGCHG(self, GCHG):
        self.GCHG.SetValue(GCHG)

    #GC x HG2
    def GetGCHG2(self):
        return self.GCHG2.GetValue()

    def SetGCHG2(self, GCHG2):
        self.GCHG2.SetValue(GCHG2)

    #GC x GCWLRefL
    def GetGCWLRefL(self):
        return self.GCWLRefL.GetValue()


    def SetGCWLRefL(self, GCWLRefL):
        self.GCWLRefL.SetValue(GCWLRefL)

    #GC x GCWLRefR
    def GetGCWLRefR(self):
        return self.GCWLRefR.GetValue()

    def SetGCWLRefR(self, GCWLRefR):
        self.GCWLRefR.SetValue(GCWLRefR)



    #CMGH x
    #CMGH x HG
    def GetCMGHHG(self):
        return self.CMGHHG.GetValue()


    def SetCMGHHG(self, CMGHHG):
        self.CMGHHG.SetValue(CMGHHG)

    #CMGH x HG2
    def GetCMGHHG2(self):
        return self.CMGHHG2.GetValue()


    def SetCMGHHG2(self, CMGHHG2):
        self.CMGHHG2.SetValue(CMGHHG2)

    #CMGH x WLRefL
    def GetCMGHWLRefL(self):
        return self.CMGHWLRefL.GetValue()


    def SetCMGHWLRefL(self, CMGHWLRefL):
        self.CMGHWLRefL.SetValue(CMGHWLRefL)

    #CMGH x WLRefR
    def GetCMGHWLRefR(self):
        return self.CMGHWLRefR.GetValue()


    def SetCMGHWLRefR(self, CMGHWLRefR):
        self.CMGHWLRefR.SetValue(CMGHWLRefR)

    #return the mean time from all our non-empty child date inputs
    def CalculteMeanTime(self):
        hour = 0
        min = 0
        total = 0

        for row in range(self.entryNum):
            # check if the time of the row should be considered.
            if not self.rowHasMeasurement(row):
                continue
            time = self.GetTimeVal(row)
            # check if time input is empty
            if time == ":":
                continue
            total += 1
            hour += int(time[:2])
            min += int(time[3:])

        if total > 0:
            avg = (hour * 60 + min) / total
        else:
            avg = 0

        return str(avg/60) + ":" + str(avg%60)

    def GetStartTimeCtrl(self):
        result = self.GetTimeValSizer().GetItem(0).GetWindow()
        for index, item in enumerate(self.GetTimeValSizer().GetChildren()):
            result = item.GetWindow().FindSmallerTime(result)
        return result





    # #allow only the float number type inputs
    # def FloatNumberControl(self, evt):
    #     ctrl = evt.GetEventObject()
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
    #     evt.Skip()

    # #round to 3 decimal points
    # def Round(self, event):
    #     ctrl = event.GetEventObject()
    #     if ctrl.GetValue() == "":
    #         event.Skip()
    #         return
    #     if ctrl.GetValue() == "+" or ctrl.GetValue() == "-" or ctrl.GetValue() == "." \
    #     or ctrl.GetValue() == "+." or ctrl.GetValue() == "-.":
    #         ctrl.SetValue("")
    #         event.Skip()
    #         return
    #     ctrl.SetValue('{0:.3f}'.format(float(ctrl.GetValue()) + 10**(-10)))
    #     event.Skip()



    #allow only the float number type inputs && calculate SRC
    def NumberControl(self, evt):
        NumberControl.FloatNumberControl(evt)
        index = int(evt.GetEventObject().GetName())
        self.RefreshSRC()


    def IncompleteDischargeTime(self):
        if self.manager.manager.disMeasManager.IncompleteTimeCheck():
            info = wx.MessageDialog(None, self.incompleteDischargeTimeMsg, self.incompleteDischargeTimeTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            info.ShowModal()






    #event on HG column to calculate the "Corrected MGH"
    def OnHGCol(self, event):
        self.CalculateHGCorrectedMGH()
        event.Skip()

    #event on HG2 column to calculate the "Corrected MGH"
    def OnHG2Col(self, event):
        self.CalculateHG2CorrectedMGH()
        event.Skip()


    #event on WL1 column to calculate the "Corrected MGH"
    def OnWL1Col(self, event):
        self.CalculateWL1CorrectedMGH()
        event.Skip()


    #event on WL2 column to calculate the "Corrected MGH"
    def OnWL2Col(self, event):
        self.CalculateWL2CorrectedMGH()
        event.Skip()

    def CalculateHGCorrectedMGH(self):
        if self.MGHHG.GetValue() != "" and self.SRCHG.GetValue() != "" and self.GCHG.GetValue() != "":

            # result = float(self.MGHHG.GetValue()) + float(self.SRCHG.GetValue()) if self.SRCHG.GetValue() != "" else float(self.MGHHG.GetValue())
            result = float(self.MGHHG.GetValue()) + float(self.SRCHG.GetValue()) + float(self.GCHG.GetValue())
   
            result = float(str(result))
            result = str(round(result,3))
            digits = 3 - len(result.split(".")[-1])
            for i in range(digits):
                result += "0"

            self.CMGHHG.SetValue(str(result))
        else:
            self.CMGHHG.SetValue("")
        if self.manager is not None:
            self.manager.manager.disMeasManager.gui.UpdateMGHCtrl(None)

    def CalculateHG2CorrectedMGH(self):
        if self.MGHHG2.GetValue() != "" and self.SRCHG2.GetValue() != "" and self.GCHG2.GetValue() != "":

            # result = float(self.MGHHG2.GetValue()) + float(self.SRCHG2.GetValue()) if self.SRCHG2.GetValue() != "" else float(self.MGHHG2.GetValue())
            result = float(self.MGHHG2.GetValue()) + float(self.SRCHG2.GetValue()) + float(self.GCHG2.GetValue())
            result = float(str(result))
            result = str(round(result,3))
            digits = 3 - len(result.split(".")[-1])
            for i in range(digits):
                result += "0"
            self.CMGHHG2.SetValue(str(result))
        else:
            self.CMGHHG2.SetValue("")
        if self.manager is not None:
            self.manager.manager.disMeasManager.gui.UpdateMGHCtrl(None)

    def CalculateWL1CorrectedMGH(self):
        if self.MGHWLRefL.GetValue() != "" and self.GCWLRefL.GetValue() != "":

            result = float(self.MGHWLRefL.GetValue()) + float(self.GCWLRefL.GetValue())
            result = float(str(result))
            result = str(round(result,3))
            digits = 3 - len(result.split(".")[-1])
            for i in range(digits):
                result += "0"
            self.CMGHWLRefL.SetValue(str(result))
        else:
            self.CMGHWLRefL.SetValue("")
        if self.manager is not None:
            self.manager.manager.disMeasManager.gui.UpdateMGHCtrl(None)


    def CalculateWL2CorrectedMGH(self):
        if self.MGHWLRefR.GetValue() != "" and self.GCWLRefR.GetValue() != "":

            result = float(self.MGHWLRefR.GetValue()) + float(self.GCWLRefR.GetValue())
            result = float(str(result))
            result = str(round(result,3))
            digits = 3 - len(result.split(".")[-1])
            for i in range(digits):
                result += "0"
            self.CMGHWLRefR.SetValue(str(result))
        else:
            self.CMGHWLRefR.SetValue("")
        if self.manager is not None:
            self.manager.manager.disMeasManager.gui.UpdateMGHCtrl(None)


    #Check if wlr1 col is empty
    def IsWLR1Empty(self):
        for index, row in enumerate(self.wlSubSizerL.GetChildren()):
            if self.GetWLSubSizerLVal(index) != "":
                return False
        return True


    #Check if HG col is empty
    def IsHGEmpty(self):
        for index, row in enumerate(self.stageSizer.GetChildren()):
            if self.GetHGVal(index) != "":
                return False
        return True

    #Calculate all src
    def RefreshSRC(self):
        for index, row in enumerate(self.srcAppSizer.GetChildren()):
            self.CalculateSRC(index)

    def CalculateSRC(self, index):

        hg = self.GetHGVal(index)
        hg2 = self.GetHG2Val(index)
        wl1 = self.GetWLSubSizerLVal(index)
        wl2 = self.GetWLSubSizerRVal(index)
        # if wl1 != '' and wl2 != '':
        #     self.SetSrcSizerVal(index, "")
        #     return
        if wl1 == '' and wl2 == '':
            self.SetSrcSizerVal(index, "")
            return
        if hg == '' and hg2 == '':
            self.SetSrcSizerVal(index, "")
            return
        # if self.wlr1Ckbox.IsChecked() and self.wlr2Ckbox.IsChecked():
        #     self.SetSrcSizerVal(index, "")
        #     return
        if self.IsHGEmpty():
            if wl1 != "":
                try:
                    self.SetSrcSizerVal(index, str(float(wl1) - float(hg2)))
                except:
                    self.SetSrcSizerVal(index, "")

            else:
                try:
                    self.SetSrcSizerVal(index, str(float(wl2) - float(hg2)))
                except:
                    self.SetSrcSizerVal(index, "")
        else:
            if wl1 != "":
                try:
                    self.SetSrcSizerVal(index, str(float(wl1) - float(hg)))
                except:
                    self.SetSrcSizerVal(index, "")
            else:
                try:
                    self.SetSrcSizerVal(index, str(float(wl2) - float(hg)))
                except:
                    self.SetSrcSizerVal(index, "")



    #Reset the time ctrl to "00:00" by pressing 'R'
    def OnResetTime(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('R'):
            ctrl = event.GetEventObject()
            ctrl.SetValue("00:00")
        event.Skip()


    #Weighted MGH Formular by average:
    def MghFormularAve(self, sum, num):
            return sum / num

    #Calculate the Weighted MGH
    def MghFormularTimeWeighted(self, timeValues):
        length = len(timeValues)
        if length == 0:
            return
        elif length == 1:
            return  timeValues[timeValues.keys()[0]]
        elif length == 2:
            startTime = self.manager.manager.disMeasManager.startTimeCtrl
            endTime = self.manager.manager.disMeasManager.endTimeCtrl
            startTimeCtrl = self.manager.manager.disMeasManager.GetStartTimeCtrl()
            endTimeCtrl = self.manager.manager.disMeasManager.GetEndTimeCtrl()
            times = sorted(timeValues.keys())
            if startTimeCtrl.IsCompleted() and endTimeCtrl.IsCompleted():
                slop = (timeValues[times[1]] - timeValues[times[0]]) / self.GetIntervalMinute(times[0], times[1])
                # print "Slop: ", slop
                start = slop * (self.GetIntervalMinute(times[0], startTime)) + timeValues[times[0]]
                end = slop * (self.GetIntervalMinute(times[0], endTime)) + timeValues[times[0]]
                # print start
                # print end
                return (start + end) / 2
            else:
                return (timeValues[times[1]] + timeValues[times[0]]) / 2
        else:
            startTime = self.manager.manager.disMeasManager.startTimeCtrl
            endTime = self.manager.manager.disMeasManager.endTimeCtrl
            startTimeCtrl = self.manager.manager.disMeasManager.GetStartTimeCtrl()
            endTimeCtrl = self.manager.manager.disMeasManager.GetEndTimeCtrl()
            if startTimeCtrl.IsCompleted() and endTimeCtrl.IsCompleted():
                if self.GetIntervalMinute(startTime, endTime) <= 0:
                    warning = wx.MessageDialog(self.manager.manager.gui,"Invalid start time and end time of discharge",
                                                "Calculate MGH Error!", wx.OK | wx.ICON_EXCLAMATION)
                    cont = warning.ShowModal()
                    if cont == wx.ID_OK:
                        return
                    else:
                        return
            times = sorted(timeValues.keys())

            if times is not None:
                # if startTime != "00:00" and endTime != "00:00":
                if startTimeCtrl.IsCompleted() and endTimeCtrl.IsCompleted():
                    #find the mgh for start time
                    print "Find 'start time': ", times
                    firstClosest, secondClosest = self.FindClosestTime(times, startTime)

                    print firstClosest
                    print secondClosest

                    if firstClosest != secondClosest:
                        if self.GetIntervalMinute(firstClosest, secondClosest) < 0:
                            temp = firstClosest
                            firstClosest = secondClosest
                            secondClosest = temp

                        slop1 = (timeValues[secondClosest] - timeValues[firstClosest]) / self.GetIntervalMinute(firstClosest, secondClosest)
                        print "slop1 ", slop1
                        start = slop1 * self.GetIntervalMinute(firstClosest, startTime) + timeValues[firstClosest]
                        timeValues[startTime] = start


                    #find the mgh for end time
                    times = sorted(timeValues.keys())
                    print "Find 'end time': ", times

                    firstClosest, secondClosest = self.FindClosestTime(times, endTime)

                    print firstClosest
                    print secondClosest

                    if firstClosest != secondClosest:
                        if self.GetIntervalMinute(firstClosest, secondClosest) < 0:
                            temp = firstClosest
                            firstClosest = secondClosest
                            secondClosest = temp
                        slop2 = (timeValues[secondClosest] - timeValues[firstClosest]) / self.GetIntervalMinute(firstClosest, secondClosest)
                        print "slop2 ", slop2
                        end = slop2 * self.GetIntervalMinute(firstClosest, endTime) + timeValues[firstClosest]
                        timeValues[endTime] = end

                    times = sorted(timeValues.keys())
                    print "Sorting all selected times including start and end"
                    print times

                    #remove the times out of the start and end boundary
                    startIndex = times.index(startTime)
                    endIndex = times.index(endTime)
                    times = times[startIndex:endIndex + 1]
                    #remove the duplicates
                    times = sorted(list(set(times)))

                    self.factors = str(times) + "\n"
                    for i in times:
                        # print timeValues[i]
                        self.factors += (str(timeValues[i]) + "\n")
                    # print "****************"
                    print "All factors involved"
                    print self.factors
                    if times[0] == times[-1]:
                        return


                total = 0

                for i in range(len(times) - 1):
                    hDelta = (timeValues[times[i + 1]] + timeValues[times[i]]) / 2
                    total += self.GetIntervalMinute(times[i], times[i + 1]) * hDelta

                return total / self.GetIntervalMinute(times[0], times[-1])



    #find the nearest time from list
    def FindClosestTime(self, timeList, key):

        if len(timeList) == 0:
            return None, None
        elif len(timeList) == 1:
            return timeList[0], timeList[0]
        else:

            if key in timeList:
                return key, key
            else:
                timeList.append(key)
                timeList = sorted(timeList)
                index = timeList.index(key)
                if index == 0:
                    return timeList[1], timeList[2]
                elif index == len(timeList) - 1:
                    return timeList[-3], timeList[-2]
                else:
                    return timeList[index - 1], timeList[index + 1]




    #Return the time range in minute by two given times
    def GetIntervalMinute(self, time1, time2):

        minTime = time1.split(":")
        minMinute = int(minTime[0]) * 60 + int(minTime[1])

        maxTime = time2.split(":")
        maxMinute = int(maxTime[0]) * 60 + int(maxTime[1])

        return maxMinute - minMinute

    #change the background and foregound color for weighted MGH depends on the selection of MGH Aggregation combobox
    def OnAggComboChangeMGHColor(self):
        self.MGHHG.SetBackgroundColour("white")
        self.MGHHG.SetForegroundColour("black")
        self.MGHHG2.SetBackgroundColour("white")
        self.MGHHG2.SetForegroundColour("black")
        self.MGHWLRefL.SetBackgroundColour("white")
        self.MGHWLRefL.SetForegroundColour("black")
        self.MGHWLRefR.SetBackgroundColour("white")
        self.MGHWLRefR.SetForegroundColour("black")

        if self.mghAggCombobox.GetValue() == self.mghAggregationChoices[1]:
            self.MGHHG.SetBackgroundColour("#bfa36a")
            self.MGHHG.SetForegroundColour("black")
        elif self.mghAggCombobox.GetValue() == self.mghAggregationChoices[2]:
            self.MGHHG2.SetBackgroundColour("#bfa36a")
            self.MGHHG2.SetForegroundColour("black")
        elif self.mghAggCombobox.GetValue() == self.mghAggregationChoices[3]:
            self.MGHWLRefL.SetBackgroundColour("#bfa36a")
            self.MGHWLRefL.SetForegroundColour("black")
        elif self.mghAggCombobox.GetValue() == self.mghAggregationChoices[4]:
            self.MGHWLRefR.SetBackgroundColour("#bfa36a")
            self.MGHWLRefR.SetForegroundColour("black")
        self.Refresh()

    def OnTypeChangeColorBack(self, event):
        event.GetEventObject().SetBackgroundColour("white")
        self.Refresh()
        event.Skip()

    #hint button on weighted MGH
    def OnWMGHBtn(self, event):
        dlg = wx.MessageDialog(self, self.weightMGHBtnHint, 'Hint', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return

    # #hint button on corrected MGH
    # def OnCMGHBtn(self, event):
    #     dlg = wx.MessageDialog(self, self.correctMGHBtnHint, 'Hint', wx.OK)

    #     res = dlg.ShowModal()
    #     if res == wx.ID_OK:
    #         dlg.Destroy()
    #     else:
    #         dlg.Destroy()
    #     return

    def IsEmptyRow(self, index):
        if self.GetHGVal(index) == "" and self.GetHG2Val(index) == "" and self.GetWLSubSizerLVal(index) == "" \
        and self.GetWLSubSizerRVal(index) == "":
            return True
        else:
            return False





    def CalculateAllMGH(self, event):

        self.OnHGCalculateMGH(event)
        self.checkDischargeTime = False
        self.OnHG2CalculateMGH(event)
        self.OnWlr1CalculateMGH(event)
        self.OnWlr2CalculateMGH(event)
        self.checkDischargeTime = True

        # self.Layout()


    def OnHGCalculateMGH(self, event):
        if self.hgCkbox.IsChecked():
            self.CalHgMgh("hg")
            self.CalculateHGCorrectedMGH()

            # self.hg2Ckbox.SetValue(False)
        # for index, row in enumerate(self.srcAppSizer.GetChildren()):
        #     self.CalculateSRC(index)
        event.Skip()

    def OnHG2CalculateMGH(self, event):
        if self.hg2Ckbox.IsChecked():
            self.CalHgMgh("hg2")
            self.CalculateHG2CorrectedMGH()

            # self.hgCkbox.SetValue(False)
        # for index, row in enumerate(self.srcAppSizer.GetChildren()):
        #     self.CalculateSRC(index)
        event.Skip()

    def OnWlr1CalculateMGH(self, event):
        if self.wlr1Ckbox.IsChecked():
            self.CalHgMgh("wlr1")
            self.CalculateWL1CorrectedMGH()

        # for index, row in enumerate(self.srcAppSizer.GetChildren()):
        #     self.CalculateSRC(index)
        event.Skip()

    def OnWlr2CalculateMGH(self, event):
        if self.wlr2Ckbox.IsChecked():
            self.CalHgMgh("wlr2")
            self.CalculateWL2CorrectedMGH()

        # for index, row in enumerate(self.srcAppSizer.GetChildren()):
        #     self.CalculateSRC(index)
        event.Skip()

    #calculate the mgh for specific column type
    def CalHgMgh(self, mghType):
        mghSum = 0
        counter = 0
        # minimumD = 9 #only use for denymic length of decimal points
        times = []
        timeValues = {}
        result = None
        resultCtrl = None

        for index, ckboxItem in enumerate(self.mghAggValSizer.GetChildren()):
            ckbox = ckboxItem.GetWindow().GetSizer().GetItem(1).GetWindow()

            if ckbox.IsChecked():
                # if self.GetTimeVal(index) == "00:00":
                #     warning = wx.MessageDialog(self.manager.manager.gui,"The logger time cannot be '00:00'",
                #                             "Calculate MGH Error!", wx.OK | wx.ICON_EXCLAMATION)
                #     cont = warning.ShowModal()
                #     if cont == wx.ID_OK:
                #         return
                #     else:
                #         return

                # else:
                # print index
                if self.GetTimeHour(index) != "" and self.GetTimeMinute(index) != "":
                    value = None
                    if mghType == "hg":
                        if self.GetHGVal(index) != "":
                            value = float(self.GetHGVal(index))
                            mghSum += value
                            counter += 1
                        resultCtrl = self.MGHHG
                    elif mghType == "hg2":
                        if self.GetHG2Val(index) != "":
                            value = float(self.GetHG2Val(index))
                            mghSum += value
                            counter += 1
                        resultCtrl = self.MGHHG2
                    elif mghType == "wlr1":
                        if self.GetWLSubSizerLVal(index) != "":
                            value = float(self.GetWLSubSizerLVal(index))
                            mghSum += value
                            counter += 1
                        resultCtrl = self.MGHWLRefL
                    elif mghType == "wlr2":
                        if self.GetWLSubSizerRVal(index) != "":
                            value = float(self.GetWLSubSizerRVal(index))
                            mghSum += value
                            counter += 1
                        resultCtrl = self.MGHWLRefR


                    times.append(self.GetTimeVal(index))
                    if value is not None:
                        timeValues[self.GetTimeVal(index)] = value

                    # #minimum number of fractions
                    # digit = resultCtrl.GetValue()[::-1].find('.') if resultCtrl.GetValue() != "" else 9
                    # minimumD = digit if digit < minimumD else minimumD
        # if counter <= 0:
        #     warning = wx.MessageDialog(self.manager.manager.gui,"Please select entries from the logger table",
        #                                         "Calculate MGH Error!", wx.OK | wx.ICON_EXCLAMATION)
        #     cont = warning.ShowModal()
        #     if cont == wx.ID_OK:
        #         return
        #     else:
        #         return

        if counter > 0:
            if self.mghMethod.GetValue() == self.mghMethods[1]:
                result = self.MghFormularAve(mghSum, counter)

            elif self.mghMethod.GetValue() == self.mghMethods[2]:
                srtTimes = sorted(times)
                duplicated = False
                for t in range(len(srtTimes) - 1):
                    if srtTimes[t] == srtTimes[t + 1]:
                        duplicated = True
                        break
                if duplicated:
                    warning = wx.MessageDialog(self.manager.manager.gui,"Identical time stamp found",
                                                    "Calculate MGH Warning!", wx.OK)
                    cont = warning.ShowModal()
                    if cont == wx.ID_OK:
                        warning.Destroy()
                if self.checkDischargeTime:
                    self.IncompleteDischargeTime()
                result = self.MghFormularTimeWeighted(timeValues)

            if result is not None:

                result = float(str(result))
                result = str(round(result,3))
                digits = 3 - len(result.split(".")[-1])
                for i in range(digits):
                    result += "0"


                resultCtrl.SetValue(result)


        else:
            if resultCtrl is not None:
                resultCtrl.SetValue("")

    #Activate or Deactivate the row by row number
    #And call OnTimeUpdateMGH event
    def OnCBtn(self, event):
        timeObj = event.GetEventObject().GetParent()
        row = int(timeObj.GetName())
        self.GetMghAggCheckbox(row).Enable(True)

        timeObj.SetToCurrent()
        self.OnTimeUpdateMGH(event)
        event.Skip()


    #active or deactive the checkbox depends on the value of time
    def ActiveCheckbox(self, row):
  
        if self.GetTimeVal(row) == ":":
            # warning = wx.MessageDialog(self.manager.manager.gui,"The row will not be included for the MGH calculation",
            #                                     "Time Reset!", wx.OK | wx.ICON_EXCLAMATION)
            # cont = warning.ShowModal()
            self.GetMghAggCheckbox(row).SetValue(False)
            self.GetMghAggCheckbox(row).Enable(False)
        else:
            self.GetMghAggCheckbox(row).Enable(True)


    def OnTimeUpdateMGH(self, event):
        index = int(event.GetEventObject().GetParent().GetName())
        try:
            self.GetTimePanel(index).UpdateTime(event.GetKeyCode())
        except:
            pass
        self.ActiveCheckbox(index)
        if self.GetMghAggCheckbox(index).IsChecked():
            self.CalculateAllMGH(event)
        event.Skip()

    def GetFirstTime(self):
        times = []
        indexTimes = {}
        for index, time in enumerate(self.timeValSizer.GetChildren()):
            if time.GetWindow().IsCompleted():
                t = self.GetTimeVal(index)
                times.append(t)
                indexTimes[t] = index
        times = sorted(times)
        if len(times) > 0:
            return self.GetTimePanel(indexTimes[times[0]])

    def GetLastTime(self):
        times = []
        indexTimes = {}
        for index, time in enumerate(self.timeValSizer.GetChildren()):
            if time.GetWindow().IsCompleted():
                t = self.GetTimeVal(index)
                times.append(t)
                indexTimes[t] = index
        times = sorted(times, reverse=True)
        if len(times) > 0:
            return self.GetTimePanel(indexTimes[times[0]])


    # def OnTimeChange(self, event):
    #     ctrl = event.GetEventObject()
    #     row = int(ctrl.GetParent().GetName())
    #     try:
    #         self.GetTimePanel(row).UpdateTime(event.GetKeyCode())
    #     except:
    #         pass
    #     self.ActiveCheckbox(row)
    #     self.CalculateAllMGH(event)
    #     event.Skip()


    # #On press HG or HG2 button to change the priority for SRC and uploading
    # def OnHGButton(self, event):

    #     if event.GetEventObject() == self.stageLabelBtn:
    #         self.stageLabelBtn.SetBackgroundColour('yellow')
    #         self.stageLabelBtn2.SetBackgroundColour((240,240,240,255))
    #         self.hgButton = True
    #     else:
    #         self.stageLabelBtn2.SetBackgroundColour('yellow')
    #         self.stageLabelBtn.SetBackgroundColour((240,240,240,255))
    #         self.hgButton = False
    #     self.Refresh()
    #     for index, row in enumerate(self.srcAppSizer.GetChildren()):
    #         self.CalculateSRC(index)

    def OnTextUpdateDischargeMGH(self, event):

        self.UpdateDischargeMGH()
        event.Skip()

    def UpdateDischargeMGH(self):

        disPanel = self.manager.manager.disMeasManager.gui
        disCombo = disPanel.mghCmbo
        choices = [""]


        choices.append(self.CMGHHG.GetValue() + "  (HG)") if self.CMGHHG.GetValue() != "" else choices.append("  (HG)")
        choices.append(self.CMGHHG2.GetValue() + "  (HG2)") if self.CMGHHG2.GetValue() != "" else choices.append("  (HG2)")
        choices.append(self.CMGHWLRefL.GetValue() + "  (WLR1)") if self.CMGHWLRefL.GetValue() != "" else choices.append("  (WLR1)")
        choices.append(self.CMGHWLRefR.GetValue() + "  (WLR2)") if self.CMGHWLRefR.GetValue() != "" else choices.append("  (WLR2)")

        disPanel.mghChoices = choices

        index = disCombo.GetSelection()
        disCombo.Set(choices)
        disCombo.SetSelection(index)

    def rowHasMeasurement(self, row):
        return self.GetHGVal(row) or \
               self.GetHG2Val(row) or \
               self.GetWLSubSizerLVal(row) or \
               self.GetWLSubSizerRVal(row)

    def rowHasDataToUpload(self, row):
        return self.GetHGVal(row) or \
               self.GetHG2Val(row) or \
               self.GetWLSubSizerLVal(row) or \
               self.GetWLSubSizerRVal(row) or \
               self.GetSrcAppSizerVal(row)



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(520, 400))
    StageMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame)

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
