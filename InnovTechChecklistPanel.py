#!/usr/bin/python
# -*- coding: utf-8 -*-

# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class InnovTechChecklistPanel(wx.Panel):
    def __init__(self, mode, *args, **kw):
        super(InnovTechChecklistPanel, self).__init__(*args, **kw)

        self.hint = "To activate the checklist the Measurement Method (Other Methods) and Monitoring Method (Salt Dilution or Image Velocimetry) must be indicated on the Front Page"

        # Default options list
        self.defaultList = ['',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''
                            ]

        # Image velocimetry options list
        self.imageVelocimetryList = ["1_Video: Video file(s) correctly named (with timestamp) and ready for upload to Sharepoint",
                            "1_Video: Framerate (record in comments)",
                            "1_Video: Perspective (record in comments) (Options: Nadir or Oblique)",
                            "1_Video: Camera used (record in comments)",
                            "2_GRPs: Type of Orthorectification (record in comments) (Options: 1D, 2D, or 3D)",
                            "2_GRPs: Photo attached to FV package that shows labelled GRPs (XS can also be labelled in this photo)? (Options: yes or no)",
                            "2_GRPs: Surveyed GRPs are in same datum as stage datum? If no, provide conversion in comments. (Options: NA, yes, conversion value)",
                            "2_GRPs: Distances between (1D or 2D), or coordinates of GRPs in csv attached to FV package. If no file provided, reference previous FV where GRP data is located (record in comments)",
                            "3_XS: Starting Bank of XS (record in comments) (Options: Left or Right)",
                            "3_XS: Starting Point (record in comments) (Options: GRP, Water Edge, other identifier (name this))",
                            "3_XS: XS is in same datum as stage datum? If no provide conversion in comments. (Options: yes, conversion value)",
                            "3_XS: XS file attached to FV package. If no file provided, reference previous FV where XS data is located (record in comments)",
                            "4_Stage: Stage at XS is recorded on Front Sheet. Record XS stage in comments if different than on Front Sheet.",
                            "5_Alpha: Alpha (record in comments) and indicate how it was/will be determined. Attach supporting mmt files to FV package if warranted."
                            ]

        # Salt dilution options list
        self.saltDilutionList = ["Calibration - Initial Volume",
                        "Calibration - Addition Volume",
                        "Calibration - Addition Concentration",
                        "Calibration - Calibration Std. Date Created",
                        "Calibration - Probe A (Temperature; Base Conductivity; Coefficient; Correlation)",
                        "Calibration - Probe B (Temperature; Base Conductivity; Coefficient; Correlation)",
                        "Dosing Calculation - Calculated Expected Discharge using rating equation and projected shifts",
                        "Dosing Calculation - Max. allowable chloride concentration for the region",
                        "Measurement - Probe Location (Probe A - LB/RB ; Probe B - LB/RB)",
                        "Measurement - Tracer Weight",
                        "Measurement - Probe Deviation (less than or equal to 5%?)",
                        "Measurement - Mixing Length",
                        "Field Review - Calibration correlation greater or equal to 0.99 for both probes?",
                        "Field Review - Difference in temperature ≤ 2 °C between probes and between independent (thermometer) temperature measurement?",
                        "Field Review - Background conductivity changing?",
                        "Field Review - Smooth breakthrough curve?",
                        "Field Review - Ice or vegetative influence?",
                        "Field Review - Describe any changes made to the breakthrough curve post measurement."
                        ]
        
        # Monitoring types
        self.monitoringTypes = ['', 'Salt Dilution', 'Image Velocimetry'] 

        self.textHeaderColWidth = 223
        self.textLabelColWidth = 375
        self.textLabelRowHeight = 20

        f = self.GetFont()
        dc = wx.WindowDC(self)
        dc.SetFont(f)
        self.width, self.TextLabelRowHeight = dc.GetTextExtent("Ag")
        self.TextLabelRowHeight *= 1.34

        self.manager = None
        self.mode = mode
        
        self.InitUI()


    def InitUI(self):

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.colSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.entrySizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #Text Labels Column Header
        self.tlHeaderPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(375, self.textLabelRowHeight + 3))
        tlHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerTxt = wx.StaticText(self.tlHeaderPanel, label="DETAILS:")
        tlHeaderSizer.Add(self.headerTxt, 2, wx.EXPAND|wx.LEFT, 5)
        tlHeaderSizer.Add((-1, -1), 1, wx.EXPAND)
        self.tlHeaderPanel.SetSizer(tlHeaderSizer)
        headerSizer.Add(self.tlHeaderPanel, 0, wx.EXPAND)

        #Text Labels Column
        self.labelSizer = wx.BoxSizer(wx.VERTICAL)
        self.labelPanel = wx.Panel(self, style=wx.BORDER_NONE, size=(self.textLabelColWidth, -1))
        self.labelPanel.SetSizer(self.labelSizer)
        self.colSizer.Add(self.labelPanel, 0, wx.EXPAND)

        # Text Ctrl Column
        # TextCtrl Header
        self.ctrlHeaderPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(-1, self.textLabelRowHeight))
        ctrlHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrlHeaderTxt = wx.StaticText(self.ctrlHeaderPanel, label="Comments:", size=(120, -1))
        ctrlHeaderSizer.Add((20, -1), 0, wx.EXPAND)
        ctrlHeaderSizer.Add(ctrlHeaderTxt, 0, wx.EXPAND)
        self.ctrlHeaderPanel.SetSizer(ctrlHeaderSizer)
        headerSizer.Add(self.ctrlHeaderPanel, 1, wx.EXPAND)

        # TextCtrl Rows
        self.ctrlSizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrlValuePanel = wx.Panel(self, style=wx.BORDER_NONE, size=(150, -1))
        self.ctrlValuePanel.SetSizer(self.ctrlSizer)
        self.colSizer.Add(self.ctrlValuePanel, 1, wx.EXPAND)

        # Label for Deployment Type (always hidden)
        self.depTypeLbl = wx.StaticText(self.ctrlHeaderPanel, label="", size=(140, -1))
        self.depTypeLbl.Enable(False)
        self.depTypeLbl.Hide()
        ctrlHeaderSizer.Add(self.depTypeLbl, 0, wx.EXPAND|wx.RIGHT, 5)

        # Dropdown dependent on monitoring method type (always hidden)
        self.monitoringTypeCtrl = wx.ComboBox(self.ctrlHeaderPanel, choices=self.monitoringTypes, style=wx.CB_READONLY)
        self.monitoringTypeCtrl.Bind(wx.EVT_COMBOBOX, self.onMonitoringTypeChangeEvent)
        self.monitoringTypeCtrl.Enable(False)
        self.monitoringTypeCtrl.Hide()
        ctrlHeaderSizer.Add(self.monitoringTypeCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        
        # Add the empty list as default
        self.addChecklistRows(self.defaultList)        

        # Notes on Site conditions
        notesSizer = wx.BoxSizer(wx.VERTICAL)
        siteNotesTxt = wx.StaticText(self, label="Comments:")
        self.notesCtrl = wx.TextCtrl(self, size=(-1, 80), style=wx.TE_MULTILINE|wx.TE_BESTWRAP)
        self.notesCtrl.Disable()
        notesSizer.Add(siteNotesTxt, 0, wx.EXPAND|wx.LEFT|wx.TOP, 10)
        notesSizer.Add(self.notesCtrl, 1, wx.EXPAND|wx.TOP, 3)

        # Set the hint bar
        self.hintBar = wx.StaticText(self, label=self.hint, size=(-1, 20))
        self.hintBar.SetForegroundColour("Red")

        self.enableHeaderSizer(False)
        self.enableColSizer(False)

        self.layoutSizer.Add(self.hintBar, 0, wx.EXPAND)
        self.layoutSizer.Add(headerSizer, 0, wx.EXPAND)
        self.layoutSizer.Add(self.colSizer, 0, wx.EXPAND)
        self.layoutSizer.Add(notesSizer, 1, wx.EXPAND)

        self.SetSizer(self.layoutSizer)


    def enableHeaderSizer(self, en):
        self.tlHeaderPanel.Enable(en)
        self.ctrlHeaderPanel.Enable(en)

    def enableColSizer(self, en):
        self.labelPanel.Enable(en)
        self.ctrlValuePanel.Enable(en)


    # Activate the table
    def activeInnovTechTable(self, en):
        self.enableHeaderSizer(en)
        self.enableColSizer(en)
        if en:
            self.hintBar.Hide()
            self.notesCtrl.Disable()
        else:
            self.hintBar.Show()
            self.notesCtrl.Enable()
        self.layoutSizer.Layout()


    # When the deployment is changed, update the InnovTech Checklist
    # to the specified labelTextList
    def addChecklistRows(self, labelTextList):

        for i in range(len(labelTextList)):

            labelPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
            labelPanel = wx.Panel(self.labelPanel, style=wx.SIMPLE_BORDER, size=(self.textLabelColWidth, self.textLabelRowHeight + 40))
            labelPanel.SetSizer(labelPanelSizer)
            labelTextLbl = wx.StaticText(labelPanel, label=labelTextList[i])
            labelPanelSizer.Add(labelTextLbl, 0, wx.EXPAND)
            self.labelSizer.Add(labelPanel, 0, wx.EXPAND)

            entryCtrl = wx.TextCtrl(self.ctrlValuePanel, size=(-1, 60))
            self.ctrlSizer.Add(entryCtrl, 0, wx.EXPAND)
            if self.manager is not None:
            	if self.manager.manager is not None:
                    # 3 is Other Methods
                    if (self.manager.manager.instrDepManager.gui.methodCBListBox.GetCurrentSelection() == 3 \
                    and \
                    # 3 is 'Salt Dilution'
                    (self.manager.manager.instrDepManager.gui.monitoringMethodCombo.GetCurrentSelection() == 3 \
                    or \
                    # 5 is 'Image Velocimetry​'
                    self.manager.manager.instrDepManager.gui.monitoringMethodCombo.GetCurrentSelection() == 5)):
                        self.enableHeaderSizer(True)
                        self.enableColSizer(True)
                        self.activeInnovTechTable(True)
                    else:
                        labelTextLbl.Enable(False)
                        labelPanel.Enable(False)
                        self.activeInnovTechTable(False)

        
    # Remove all rows so that the entries can be replaced
    # with another list of entries
    def removeAllChecklistRows(self):
        for index in range(len(self.labelSizer.GetChildren())):
            self.labelSizer.Hide(0)
            self.labelSizer.Remove(0)
            
            self.ctrlSizer.Hide(0)
            self.ctrlSizer.Remove(0)


    # Called when the deployement changes from the first page
    # remove the checklist rows and then add new ones according
    # to the appropriate and selected list
    def changeDepType(self, depType):
        self.depTypeLbl.SetLabel(str(depType))
        self.colSizer.Layout()

        if "other methods" in str(depType).lower():
            self.monitoringTypeCtrl.SetValue(self.monitoringTypes[0])
            self.monitoringTypeCtrl.Hide()
        else:
            self.monitoringTypeCtrl.Enable(False)
            self.monitoringTypeCtrl.Hide()
            
        self.removeAllChecklistRows()
        self.addChecklistRows(self.defaultList)
        self.notesCtrl.Disable()

        self.layoutSizer.Layout()


    # Change the monitoring type value
    def onMonitoringType(self, choice):
        if "salt dilution" in str(choice).lower():
            self.monitoringTypeCtrl.SetValue(self.monitoringTypes[1])
            self.onMonitoringTypeChange()
            self.monitoringTypeCtrl.Enable(False)
            self.notesCtrl.Enable() 
        elif "image velocimetry" in str(choice).lower():
            self.monitoringTypeCtrl.SetValue(self.monitoringTypes[2])
            self.onMonitoringTypeChange()
            self.monitoringTypeCtrl.Enable(False)
            self.notesCtrl.Enable()
        else:
            self.monitoringTypeCtrl.SetValue(self.monitoringTypes[0])
            self.onMonitoringTypeChange()
            self.monitoringTypeCtrl.Enable(False)
            self.notesCtrl.Disable()
        
        self.layoutSizer.Layout()


    def onMonitoringTypeChangeEvent(self, e):
        self.onMonitoringTypeChange()


    # When the monitoring method is changed
    # Update the checklist to the appropriate list
    def onMonitoringTypeChange(self):
        if "salt dilution" in str(self.monitoringTypeCtrl.GetValue()).lower():
            self.removeAllChecklistRows()
            self.addChecklistRows(self.saltDilutionList)
            self.headerTxt.SetLabel("DETAILS: Salt Dilution")
            self.notesCtrl.Enable()
        elif "image velocimetry" in str(self.monitoringTypeCtrl.GetValue()).lower():
            self.removeAllChecklistRows()
            self.addChecklistRows(self.imageVelocimetryList)
            self.headerTxt.SetLabel("DETAILS: Image Velocimetry")
            self.notesCtrl.Enable()
        else:
            self.removeAllChecklistRows()
            self.addChecklistRows(self.defaultList)
            self.headerTxt.SetLabel("DETAILS:")
            self.notesCtrl.Disable()

        self.notesCtrl.SetValue("")
        self.layoutSizer.Layout()


     
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(780, 700))
    InnovTechChecklistPanel("DEBUG", frame)
    frame.Centre()
    frame.Show()
    
    app.MainLoop()    

if __name__ == '__main__':
    main()
