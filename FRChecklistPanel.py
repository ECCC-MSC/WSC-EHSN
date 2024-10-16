#!/usr/bin/python
# -*- coding: utf-8 -*-

# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class FRChecklistPanel(wx.Panel):
    def __init__(self, mode, *args, **kw):
        super(FRChecklistPanel, self).__init__(*args, **kw)

        self.fieldRevLbl = "FIELD REVIEW"
        self.passCBLbl = "Pass"
        self.cbRevLbl = "Review"
        self.cbCheckLbl = "Check"
        self.reviewCommentsLbl = "Review Comments"
        self.hint = "To activate the checklist the method (Mid-section or ADCP by moving boat) and Instrument Type must be indicated on the Front Page"

        self.adcpCheckList = ["Passed All Initial QA/QC?",
                              "Software Input Same as Notes*?",
                              "Difference in ADCP and Water T < 2\N{DEGREE SIGN}C?",
                              "Smooth Ship Track?",
                              "Boat Speed < Water Speed?",
                              "Pitch, Roll < 5\N{DEGREE SIGN}?",
                              "No Ambiguity Velocity?",
                              "Good Differential GPS Quality?",
                              "Bed Contours as Expected for Site?",
                              "Measured Q > 50%?",
                              "Missing Data < 10%",
                              "Missing Data Distributed?",
                              "Proper Edge Measurement Method?",
                              "Each Edge < 5% of Total Q?",
                              "Velocity Profile Checked with QRev?",
                              "Reciprocal Pairs?",
                              "Moving Bed Corrected If Any?",
                              "Directional Bias < 5%?",
                              "Total Exposure > 720s?",
                              "Standard Deviation/Mean < 5%?"]

        self.midsectionTypes = ["All", "Current Meter",
                                "Flow Tracker",
                                "ADCP"]

        self.midAllList = ["Passed All Instrument QA/QC?",
                                    "Software Input Same as Notes?",
                                    "Difference in ADCP and Water T < 2\N{DEGREE SIGN}C?",
                                    "Signal to Noise Ratio > 4",
                                    "Flow Angles Accounted for?",
                                    "Exposure Time/Location > 40s?",
                                    "Valid Ensembles/Panel > 30?",
                                    "No Boundary or Spike Problem?",
                                    "Bed Contour as Expected for Site?",
                                    "Ice/Slush Depth as Expected?",
                                    "Velocity Profile Checked with QRev?",
                                    "# Panels ≥ 20?",
                                    "No Panel Q > 10%?"]

        self.midsectionCurrMeter = ["Passed All Instrument QA/QC?",
                                    "Software Input Same as Notes?",
                                    "Flow Angles Accounted for?",
                                    "Exposure Time/Location > 40s?",
                                    "Bed Contour as Expected for Site?",
                                    "Ice/Slush Depth as Expected?",
                                    "Velocity Profile Suitable?",
                                    "# Panels ≥ 20?",
                                    "No Panel Q > 10%?"]

        self.midsectionFlowTrack = ["Passed All Instrument QA/QC?",
                                    "Software Input Same as Notes?",
                                    "Difference in ADCP and Water T < 2\N{DEGREE SIGN}C?",
                                    "Signal to Noise Ratio > 4",
                                    "Flow Angles Accounted for?",
                                    "Exposure Time/Location > 40s?",
                                    "No Boundary or Spike Problem?",
                                    "Bed Contour as Expected for Site?",
                                    "Ice/Slush Depth as Expected?",
                                    "Velocity Profile Suitable?",
                                    "# Panels ≥ 20?",
                                    "No Panel Q > 10%?"]

        self.midsectionADCP = ["Passed All Instrument QA/QC?",
                               "Software Input Same as Notes?",
                               "Difference in ADCP and Water T < 2\N{DEGREE SIGN}C?",
                               "Exposure Time/Location > 40s?",
                               "Valid Ensembles/Panel > 30?",
                               "Bed Contour as Expected for Site?",
                               "Ice/Slush Depth as Expected?",
                               "Velocity Profile Checked with QRev?",
                               "# Panels ≥ 20?",
                               "No Panel Q > 10%?"]

        self.fullList = ["Passed All Initial QA/QC?",
                         "Software Input Same as Notes*?",
                         "Difference in ADCP and Water T < 2\N{DEGREE SIGN}C?",
                         "Smooth Ship Track?",
                         "Boat Speed < Water Speed?",
                         "Pitch, Roll < 5\N{DEGREE SIGN}?",
                         "No Ambiguity Velocity?",
                         "Good Differential GPS Quality?",
                         "Bed Contours as Expected for Site?",
                         "Measured Q > 50%?",
                         "Missing Data < 10%",
                         "Missing Data Distributed?",
                         "Proper Edge Measurement Method?",
                         "Each Edge < 5% of Total Q?",
                         "Velocity Profile Checked with QRev?",
                         "Reciprocal Pairs?",
                         "Moving Bed Corrected If Any?",
                         "Directional Bias < 5%?",
                         "Total Exposure > 720s?",
                         "Standard Deviation/Mean < 5%?",
                         "Signal to Noise Ratio > 4",
                         "Flow Angles Accounted for?",
                         "Exposure Time/Location > 40s?",
                         "Valid Ensembles/Panel > 30?",
                         "No Boundary or Spike Problem?",
                         "Bed Contour as Expected for Site?",
                         "Ice/Slush Depth as Expected?",
                         "# Panels ≥ 20?",
                         "No Panel Q > 10%?"]

        self.notesOnSiteCondLbl = "Notes on Site Conditions Affecting Measurement Quality:"
        # self.picturedLbl = "Site and/or control pictures were taken."
        self.nextPlanLbl = "For Next trip Planning: Suggested repairs and Improvements, Comments and Actions."
        self.textHeaderColWidth = 223
        self.textLabelColWidth = 250
        self.textLabelRowHeight = 20

        #Font stuff
        f = self.GetFont()
        dc = wx.WindowDC(self)
        dc.SetFont(f)
        self.width, self.TextLabelRowHeight = dc.GetTextExtent("Ag")
        self.TextLabelRowHeight *= 1.34

        self.manager = None
        self.mode = mode
        
        self.InitUI()
        
    def InitUI(self):
        if self.mode == "DEBUG":
            print("In ADCPChecklist")

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.colSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.entrySizer = wx.BoxSizer(wx.HORIZONTAL)
        

        #Text Labels Column Header
        self.tlHeaderPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(220, self.textLabelRowHeight + 3))
        tlHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        fieldRevTxt = wx.StaticText(self.tlHeaderPanel, label=self.fieldRevLbl)
        self.passCB = wx.CheckBox(self.tlHeaderPanel, label=self.passCBLbl, style=wx.ALIGN_RIGHT)
        
        tlHeaderSizer.Add(fieldRevTxt, 2, wx.EXPAND|wx.LEFT, 5)
        tlHeaderSizer.Add(self.passCB, 2, wx.EXPAND)
        tlHeaderSizer.Add((-1, -1), 1, wx.EXPAND)
        self.tlHeaderPanel.SetSizer(tlHeaderSizer)

        headerSizer.Add(self.tlHeaderPanel, 0, wx.EXPAND)
        

        #Text Labels Column
        self.labelSizer = wx.BoxSizer(wx.VERTICAL)
        self.labelPanel = wx.Panel(self, style=wx.BORDER_NONE, size=(self.textLabelColWidth, -1))
        self.labelPanel.SetSizer(self.labelSizer)

        #Add to Sizer
        self.colSizer.Add(self.labelPanel, 0, wx.EXPAND)



        #Check Boxes Column
        #CB Headers
        cbHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cbRevLabelPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(54, self.textLabelRowHeight))
        cbRevLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        cbRevLabelTxt = wx.StaticText(self.cbRevLabelPanel, style=wx.ALIGN_RIGHT, label=self.cbRevLbl)
        cbRevLabelSizer.Add(cbRevLabelTxt, 1, wx.EXPAND|wx.RIGHT, 5)
        self.cbRevLabelPanel.SetSizer(cbRevLabelSizer)

        self.cbCheckLabelPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(54, self.textLabelRowHeight))
        cbCheckLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        cbCheckLabelTxt = wx.StaticText(self.cbCheckLabelPanel, label=self.cbCheckLbl, style=wx.ALIGN_LEFT)
        cbCheckLabelSizer.Add(cbCheckLabelTxt, 1, wx.EXPAND|wx.LEFT, 5)
        self.cbCheckLabelPanel.SetSizer(cbCheckLabelSizer)
        self.cbCheckLabelPanel.Hide()

        cbHeaderSizer.Add(self.cbRevLabelPanel, 1, wx.EXPAND)
        cbHeaderSizer.Add(self.cbCheckLabelPanel, 1, wx.EXPAND)
        cbHeaderSizer.Layout()
        
        headerSizer.Add(cbHeaderSizer, 0, wx.EXPAND)
        

        #CB Labels
        self.cbRevSizer = wx.BoxSizer(wx.VERTICAL)
        self.cbCheckSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.cbRevPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(24, -1))
        self.cbRevPanel.SetSizer(self.cbRevSizer)
        self.cbCheckPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(24, -1))
        self.cbCheckPanel.SetSizer(self.cbCheckSizer)
        self.cbCheckPanel.Hide()


        #Add to Sizer
        self.colSizer.Add(self.cbRevPanel, 0, wx.EXPAND)
        self.colSizer.Add(self.cbCheckPanel, 0, wx.EXPAND)


        #Text Ctrl Column
        #TextCtrl Header
        self.ctrlHeaderPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.textLabelRowHeight))
        ctrlHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrlHeaderTxt = wx.StaticText(self.ctrlHeaderPanel, label=self.reviewCommentsLbl, size=(120, -1))
        ctrlHeaderSizer.Add((20, -1), 0, wx.EXPAND)
        ctrlHeaderSizer.Add(ctrlHeaderTxt, 0, wx.EXPAND)
        self.ctrlHeaderPanel.SetSizer(ctrlHeaderSizer)
        
        headerSizer.Add(self.ctrlHeaderPanel, 1, wx.EXPAND)
        

        #TextCtrl Rows
        self.ctrlSizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrlValuePanel = wx.Panel(self, style=wx.BORDER_NONE, size=(150, -1))
        self.ctrlValuePanel.SetSizer(self.ctrlSizer)

        #Add to Sizer
        self.colSizer.Add(self.ctrlValuePanel, 1, wx.EXPAND)


        #Label for Deployment Type
        self.depTypeLbl = wx.StaticText(self.ctrlHeaderPanel, label="", size=(140, -1))
        self.depTypeLbl.Enable(False)
        ctrlHeaderSizer.Add(self.depTypeLbl, 0, wx.EXPAND|wx.RIGHT, 5)

        #Dropdown dependent on Deployment Type
        self.midsecTypeCtrl = wx.ComboBox(self.ctrlHeaderPanel, choices=self.midsectionTypes, style=wx.CB_READONLY)
        self.midsecTypeCtrl.Bind(wx.EVT_COMBOBOX, self.onMidsecTypeChangeEvent)
        self.midsecTypeCtrl.Enable(False)
        self.midsecTypeCtrl.Hide()
        ctrlHeaderSizer.Add(self.midsecTypeCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        

        #Add all possible checklist rows as default
        self.addChecklistRows(self.fullList)        

        #Notes on Site conditions
        notesSizer = wx.BoxSizer(wx.VERTICAL)
        

        siteNotesTxt = wx.StaticText(self, label=self.notesOnSiteCondLbl)
        self.siteNotesCtrl = wx.TextCtrl(self, size=(-1, 80), style=wx.TE_MULTILINE|wx.TE_BESTWRAP)

        planNotesTxt = wx.StaticText(self, label=self.nextPlanLbl)
        self.planNotesCtrl = wx.TextCtrl(self, size=(-1, 80), style=wx.TE_MULTILINE|wx.TE_BESTWRAP)

        notesSizer.Add(siteNotesTxt, 0, wx.EXPAND|wx.LEFT|wx.TOP, 10)
        notesSizer.Add(self.siteNotesCtrl, 1, wx.EXPAND|wx.TOP, 3)

        notesSizer.Add(planNotesTxt, 0, wx.EXPAND|wx.LEFT|wx.TOP, 10)
        notesSizer.Add(self.planNotesCtrl, 1, wx.EXPAND|wx.TOP, 3)

        # self.picturedCkbox = wx.CheckBox(self, label=self.picturedLbl)

        self.hintBar = wx.StaticText(self, label=self.hint, size=(-1, 20))
        self.hintBar.SetForegroundColour("Red")


        self.enableHeaderSizer(False)
        self.enableColSizer(False)

        self.layoutSizer.Add(self.hintBar, 0, wx.EXPAND)
        self.layoutSizer.Add(headerSizer, 0, wx.EXPAND)
        self.layoutSizer.Add(self.colSizer, 0, wx.EXPAND)
        # self.layoutSizer.Add(self.picturedCkbox, 0)
        self.layoutSizer.Add(notesSizer, 1, wx.EXPAND)

        self.SetSizer(self.layoutSizer)


    def enableHeaderSizer(self, en):
        self.tlHeaderPanel.Enable(en)
        self.cbRevLabelPanel.Enable(en)
        self.cbCheckLabelPanel.Enable(en)
        self.ctrlHeaderPanel.Enable(en)
        # self.picturedCkbox.Enable(en)

    def enableColSizer(self, en):
        self.labelPanel.Enable(en)
        self.cbRevPanel.Enable(en)
        self.cbCheckPanel.Enable(en)
        self.ctrlValuePanel.Enable(en)


    def activeFieldReview(self, en):

        self.enableHeaderSizer(en)
        # self.enableColSizer(en)
        # for child in self.labelPanel.GetSizer().GetChildren():
        #     child.GetWindow().Enable(en)


      
        if en:
            self.hintBar.Hide()
        else:

            self.hintBar.Show()
        self.layoutSizer.Layout()






    # When the deployment is changed, change the Field Review Checklist
    # to the specified labelTextList
    def addChecklistRows(self, labelTextList):

        for i in range(len(labelTextList)):
            if i == 0 or i == (len(labelTextList) - 1):
                sizerCBHeight = 18
            else:
                sizerCBHeight = 20

            labelPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
            labelPanel = wx.Panel(self.labelPanel, style=wx.SIMPLE_BORDER, size=(self.textLabelColWidth, self.textLabelRowHeight))
            labelPanel.SetSizer(labelPanelSizer)
            
            labelTextLbl = wx.StaticText(labelPanel, label=labelTextList[i])
            labelPanelSizer.Add(labelTextLbl, 0, wx.EXPAND)
            
            self.labelSizer.Add(labelPanel, 0, wx.EXPAND)


            revCB = wx.CheckBox(self.cbRevPanel, size=(-1, sizerCBHeight))
            self.cbRevSizer.Add(revCB, 0, wx.EXPAND|wx.LEFT, 4)
            
            checkCB = wx.CheckBox(self.cbCheckPanel, size=(-1, sizerCBHeight))
            self.cbCheckSizer.Add(checkCB, 0, wx.EXPAND|wx.LEFT, 4)
            
            
            entryCtrl = wx.TextCtrl(self.ctrlValuePanel, size=(-1, 20))
            self.ctrlSizer.Add(entryCtrl, 0, wx.EXPAND)
            if self.manager is not None:
            	if self.manager.manager is not None:
                            # if (not self.manager.manager.instrDepManager.gui.methodCBListBox.IsChecked(0) and \
                                    # not self.manager.manager.instrDepManager.gui.methodCBListBox.IsChecked(1)) or \
                        if (self.manager.manager.instrDepManager.gui.methodCBListBox.GetCurrentSelection() == 2 or \
                        self.manager.manager.instrDepManager.gui.methodCBListBox.GetCurrentSelection() == 1) \
                        and self.manager.manager.instrDepManager.gui.instrumentCmbo.GetValue().lower() != 'adv' and \
                        self.manager.manager.instrDepManager.gui.instrumentCmbo.GetValue().lower() != 'adcp' \
                        and self.manager.manager.instrDepManager.gui.instrumentCmbo.GetValue().lower() != 'current meter':
                                labelTextLbl.Enable(False)
                                labelPanel.Enable(False)
                                revCB.Enable(False)
                                checkCB.Enable(False)
                                self.activeFieldReview(False)
                        else:
                                self.enableHeaderSizer(True)
                                self.enableColSizer(True)
                                self.activeFieldReview(True)

        
    # Remove all rows so that the entries can be replaced
    # with another list of entries
    def removeAllChecklistRows(self):
        for index in range(len(self.labelSizer.GetChildren())):
            self.labelSizer.Hide(0)
            self.labelSizer.Remove(0)
            
            self.cbRevSizer.Hide(0)
            self.cbRevSizer.Remove(0)
            
            self.cbCheckSizer.Hide(0)
            self.cbCheckSizer.Remove(0)
            
            self.ctrlSizer.Hide(0)
            self.ctrlSizer.Remove(0)

    # Called when the deployement changes from the first page
    # remove the checklist rows and then add new ones according
    # to the appropriate and selected list
    def changeDepType(self, depType):
        # from pdb import set_trace
        # set_trace()
        self.depTypeLbl.SetLabel(str(depType))
        self.colSizer.Layout()

        if "mid-section" in str(depType).lower():
            # self.midsecTypeCtrl.Enable(False)
            self.midsecTypeCtrl.Show()
            self.midsecTypeCtrl.SetValue(self.midsectionTypes[0])
            
            self.removeAllChecklistRows()
            self.addChecklistRows(self.midAllList)
            
        elif "adcp" in  str(depType).lower():
            self.midsecTypeCtrl.Enable(False)
            self.midsecTypeCtrl.Hide()
            
            self.removeAllChecklistRows()
            self.addChecklistRows(self.adcpCheckList)

        else:
            self.midsecTypeCtrl.Enable(False)
            self.midsecTypeCtrl.Hide()
            
            self.removeAllChecklistRows()
            self.addChecklistRows(self.fullList)

        self.layoutSizer.Layout()

    def onInstrumentType(self, val):
      if val < len(self.midsectionTypes) and val >= 0:
        self.midsecTypeCtrl.SetValue(self.midsectionTypes[val])
        self.onMidsecTypeChange()
        self.midsecTypeCtrl.Enable(False)
      else:
        self.midsecTypeCtrl.Enable(False)
        self.layoutSizer.Layout()


    def onMidsecTypeChangeEvent(self, e):
        self.onMidsecTypeChange()


    # When the midsection type is changed
    # Update the checklist to the appropriate list
    def onMidsecTypeChange(self):
        if self.midsecTypeCtrl.IsShown():
            if "current" in str(self.midsecTypeCtrl.GetValue()).lower():
                self.removeAllChecklistRows()
                self.addChecklistRows(self.midsectionCurrMeter)

            elif "flow" in str(self.midsecTypeCtrl.GetValue()).lower():
                self.removeAllChecklistRows()
                self.addChecklistRows(self.midsectionFlowTrack)

            elif "adcp" in str(self.midsecTypeCtrl.GetValue()).lower():
                self.removeAllChecklistRows()
                self.addChecklistRows(self.midsectionADCP)
            else:
                self.removeAllChecklistRows()
                self.addChecklistRows(self.midAllList)

            self.layoutSizer.Layout()

        
                       
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(780, 700))
    FRChecklistPanel("DEBUG", frame)
    frame.Centre()
    frame.Show()
    
    app.MainLoop()    

if __name__ == '__main__':
    main()
