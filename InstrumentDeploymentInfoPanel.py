# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import NumberControl
# import wx.lib.intctrl

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


class InstrumentDeploymentInfoPanel(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(InstrumentDeploymentInfoPanel, self).__init__(*args, **kwargs)

        self.adcpByMovingBoatLbl = "ADCP by Moving Boat"
        self.midsectionLbl = "Mid-section"
        self.deploymentLbl = "Deployment"
        self.deploymentMidsecList = ["", "Wading", "Bridge Upstream", "Bridge Downstream",
                                     "Tethered Bridge Upstream", "Tethered Bridge Downstream",
                                     "Tethered Cableway", "Cableway", "Manned Boat", "Ice Cover"]
        self.deploymentADCPList = ["", "Tethered Bridge Upstream", "Tethered Bridge Downstream",
                                   "Tethered Cableway", "Manned Boat", "Remote Control"]

        self.white = "white"
        self.metresLbl = "metres"
        self.kilometresLbl = "kilometres"
        self.aboveLbl = "u/s"
        self.belowLbl = "d/s"
        self.gaugeLbl = "gauge"
        self.selectedGauge = self.gaugeLbl
        self.instrumentLbl = "Instrument Type"
        self.instrumentList = ["", "ADCP", "ADV", "Current Meter"]
        self.instruments = []
        self.models = []
        self.modelLbl = "Model"
        self.modelList = ["", "Rio Grande", "RiverRay",
                               "StreamPro", "RiverPro", "M9", "S5", "FlowTracker",
                               "Price AA", "Pygmy"]
        self.modelList1 = ["", "Rio Grande", "RiverRay",
                               "StreamPro", "RiverPro", "M9", "S5"]
        self.modelList2 = ["", "Price AA", "Pygmy"]
        self.modelList3 = ["", "FlowTracker"]
        self.modelListSontek = ["", "Rio Grande", "RiverRay", "StreamPro", "RiverPro"]
        self.modelListTRDI = ["", "M9", "S5"]
        self.manufactureLbl = "Manufacturer"
        self.manufactureList = ["", 'SonTek', 'TRDI']
        self.serialNumLbl = "Serial/Meter Number"
        self.serialNumList = []
        self.frequnecies = []
        self.positionMethodLbl = "Position Method"
        self.positionMethodList = ["", "Tapeline", "GPS", "ENUF", "XYZ"]

        self.midsectionInfoLbl = "Mid-section Information"
        self.numOfPanelLbl = "Number of Panels"
        self.flowAngleLbl = "Flow Angle"
        self.flowAngleList = ["", "Perpendicular", "Varied"]
        self.coEffLbl = "Coefficient"
        self.coefficientList = ["","-1", "1", "0.88"]
        self.methodLbl = "Method"
        self.methodList = ["", "0.6", "0.2/0.8", "0.6+0.2/0.8", "0.5", "0.5+0.2/0.8", "Surface", "0.2/0.6/0.8", "0.2/0.5/0.8", "ADCP"]
        self.locatedLbl = "Located"
        self.metresAboveLbl = "metres above"
        self.weightList = ["", "15", "30", "50", "75", "100", "150", "300"]
        self.kilogramLbl = "kg"
        self.poundLbl = "lb"
        self.weightLbl = "weight"
        self.noweightLbl = "no weight"

        self.adcpInfoLbl = "ADCP Information"
        self.freqLbl = "Frequency(kHz)"
        self.firmwareLbl = "Firmware"
        self.softwareLbl = "Software"
        self.configLbl = "Config"
        self.configList = ["", "Vary/Panel", "Auto", "Manual"]
        self.adcpSetToClockLbl = "ADCP Set to Clock"
        self.diagTestLbl = "Diagnostic Test"
        self.adcpDepthLbl = "ADCP Depth*(m)"
        self.magnDeclLbl = "Magnetic Declination*"
        self.compCaliLbl = "Compass Calibration"
        self.passedFieldRevLbl = "Passed Field Review"
        self.firmware = []
        # self.controlLbl = "Control Condition"
        # self.contCondLbl = "Condition"
        self.contCondList = ["", "Not Observed", "No Flow", "Clear", "Altered", "Debris", "Algae",
                             "Weeds", "Fill", "Scour", "Shore Ice",
                             "Complete Ice Cover", "Anchor Ice"]
        self.deploymentWarning = "Unchecking %s will cause loss of entered data such as field review. Are you sure you want to uncheck this selection? "
        self.positionMethods = ["", "Tagline", "Marked bridge railing"]
        self.locatedList = ["On Rod"]
        self.numberOfPanelsList = []
        self.picturedLbl = "Site and/or control pictures were taken."
        self.preUseCableLbl = "Pre-use Cableway Inspection"
        self.preUseCableList = ["Not-required", "Passed", "Failed"]
        self.numberRange = list(range(20, 51))
        for i in self.numberRange:
            self.numberOfPanelsList.append(str(i))


        # Not Currently in use
        # self.contEffLbl = "Effect"
        # self.contEffCatList = ["Backwater", "Control Change", "Flow Influenced",
        #                         "Poorly Defined Range", "Undefined"]
        # self.contEffBackList = ["Ice", "Beaver", "Confluence", "Regulation",
        #                          "Debris", "Moss/Algae", "..."]
        # self.contEffChangeList = ["Debris", "Fill", "Scour", "Moss/Algae", "..."]
        # self.contEffFlowList = ["Wind", "Hysteresis", "..."]
        # self.contEffSubCatList = [self.contEffBackList, self.contEffChangeList, self.contEffFlowList,
        #                           [""], [""]]


        # self.contRemLbl = "Remarks"
        # self.dischLbl = "Discharge Activity Remarks"
        # self.controlConditionRemLbl = "Control Condition Remarks"
        # self.dischRemLbl = self.contRemLbl
        # self.stageLbl = "Stage Activity Summary Remarks"
        # self.stageRemLbl = self.contRemLbl
        # self.stnLbl = "Station Health Remarks"
        # self.genRemLbl = self.contRemLbl

        self.mode=mode
        self.manager = None

        self.InitUI()
        #disable the event to be triggered
    def do_nothing(self,evt):

          pass


    def onRadioGauge(self, e):
        if self.gauge1RadButBox.GetValue():
            self.gaugeOtherTxt.Enable(False)
            self.selectedGauge = self.gaugeLbl
        else:
            self.gaugeOtherTxt.Enable(True)
            self.selectedGauge = self.gaugeOtherTxt.GetValue()
        e.Skip()



    def OnGaugeTextChange(self, e):
        self.selectedGauge = self.gaugeOtherTxt.GetValue()
        e.Skip()

    def InitUI(self):
        if self.mode=="DEBUG":
            print "Setup InstrumentDeploymentInfoPanel"

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)

        #First Row of items
        #uses sizers and spacers to center items vertically
        horizontalSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        #Method Checkboxes
        methodListSizer = wx.BoxSizer(wx.VERTICAL)
        self.methodCBListBox = wx.CheckListBox(self, size=(-1, 45), choices=[self.adcpByMovingBoatLbl, self.midsectionLbl], style=wx.LB_SINGLE)
        self.methodCBListBox.Bind(wx.EVT_CHECKLISTBOX, self.OnDeploymentCheckListCB)
        self.methodCBListBox.Bind(wx.EVT_LISTBOX, self.OnDeploymentCheckListBox)

        methodListSizer.Add(self.methodCBListBox, 0, wx.EXPAND)




        #Deployment Combo Box
        self.deploymentTxt = wx.StaticText(self, label=self.deploymentLbl, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL)
        self.deploymentCmbo = wx.ComboBox(self, size=(155, 23), style=wx.CB_DROPDOWN)
        self.deploymentCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.deploymentCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        deploymentSizerV = wx.BoxSizer(wx.VERTICAL)
        deploymentSizer = wx.BoxSizer(wx.HORIZONTAL)
        deploymentSizer.Add(self.deploymentTxt, 0, wx.EXPAND|wx.RIGHT, 5)
        deploymentSizer.Add(self.deploymentCmbo, 0, wx.EXPAND|wx.LEFT, 5)

        deploymentSizerV.Add((-1, -1), 1, wx.EXPAND)
        deploymentSizerV.Add(deploymentSizer, 0, wx.EXPAND)
        deploymentSizerV.Add((-1, -1), 1, wx.EXPAND)

        # self.deploymentCmbo.Bind(wx.EVT_COMBOBOX, self.OnDeploymentSelect)










        horizontalSizer1.Add(methodListSizer, 0, wx.EXPAND|wx.LEFT, 5)
        horizontalSizer1.Add((5, -1), 1, wx.EXPAND)
        horizontalSizer1.Add(deploymentSizerV, 0, wx.EXPAND|wx.LEFT, 5)
        horizontalSizer1.Add((25, -1), 1, wx.EXPAND)

        # horizontalSizer1.Add(positionMethodSizerV, 0, wx.EXPAND|wx.LEFT, 5)
        # horizontalSizer1.Add((5, -1), 1, wx.EXPAND)





        #Second Row of items
        horizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)




        #Position method
        positionMethodSizer = wx.BoxSizer(wx.HORIZONTAL)
        positionMethodSizerV = wx.BoxSizer(wx.VERTICAL)

        self.positionMethodTxt = wx.StaticText(self, label=self.positionMethodLbl, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL)
        # self.positionMethodCtrl = wx.TextCtrl(self, size=(155, -1), style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.positionMethodCmbo = wx.ComboBox(self, size=(155, -1), choices=self.positionMethods, style=wx.CB_DROPDOWN)

        positionMethodSizer.Add(self.positionMethodTxt, 0, wx.EXPAND|wx.RIGHT, 5)
        positionMethodSizer.Add(self.positionMethodCmbo, 0, wx.EXPAND|wx.RIGHT, 5)

        positionMethodSizerV.Add((-1, -1), 1, wx.EXPAND)
        positionMethodSizerV.Add(positionMethodSizer, 0, wx.EXPAND)
        positionMethodSizerV.Add((-1, -1), 1, wx.EXPAND)



        #Gauge Ctrl
        gaugeCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        self.gaugeCtrl = MyTextCtrl(self, size=(25, -1), style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.gaugeCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.gaugeCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        gaugeCtrlSizer.Add((-1, -1), 1, wx.EXPAND)
        gaugeCtrlSizer.Add(self.gaugeCtrl, 0, wx.EXPAND)
        gaugeCtrlSizer.Add((-1, -1), 1, wx.EXPAND)

        #Metres/Kilmetres radio buttons - above/below radio buttons
        self.lengthRadButBox = wx.RadioBox(self, choices=[self.metresLbl, self.kilometresLbl], style=wx.RA_VERTICAL)
        self.posRadButBox = wx.RadioBox(self, choices=[self.aboveLbl, self.belowLbl], style=wx.RA_VERTICAL)

        gauge1RadButSizerV = wx.BoxSizer(wx.VERTICAL)
        gauge2RadButSizerV = wx.BoxSizer(wx.VERTICAL)

        gauge1RadButSizerV.Add((-1, -1), 1, wx.EXPAND)
        gauge1RadButSizerV.Add(self.lengthRadButBox, 0, wx.EXPAND)
        gauge1RadButSizerV.Add((-1, -1), 1, wx.EXPAND)

        gauge2RadButSizerV.Add((-1, -1), 1, wx.EXPAND)
        gauge2RadButSizerV.Add(self.posRadButBox, 0, wx.EXPAND)
        gauge2RadButSizerV.Add((-1, -1), 1, wx.EXPAND)

        #Gauge radio button
        gaugeSizerH = wx.BoxSizer(wx.HORIZONTAL)
        gaugeSizerV = wx.BoxSizer(wx.VERTICAL)

        self.gauge1RadButBox = wx.RadioButton(self, -1, self.gaugeLbl, style=wx.RB_GROUP)
        self.gauge2RadButBox = wx.RadioButton(self, -1, "")


        self.gaugeOtherTxt = wx.TextCtrl(self, size=(180, -1))
        gaugeSizerH.Add(self.gauge2RadButBox, 0, wx.EXPAND)
        gaugeSizerH.Add(self.gaugeOtherTxt, 0, wx.EXPAND)

        gaugeSizerV.Add((-1, -1), 1, wx.EXPAND)
        gaugeSizerV.Add(self.gauge1RadButBox, 0, wx.EXPAND)
        gaugeSizerV.Add(gaugeSizerH, 0, wx.EXPAND)
        gaugeSizerV.Add((-1, -1), 1, wx.EXPAND)
        self.gaugeOtherTxt.Enable(False)
        self.selectedGauge = self.gaugeLbl
        self.gaugeOtherTxt.Bind(wx.EVT_TEXT, self.OnGaugeTextChange)
        self.gauge1RadButBox.Bind(wx.EVT_RADIOBUTTON, self.onRadioGauge)
        self.gauge2RadButBox.Bind(wx.EVT_RADIOBUTTON, self.onRadioGauge)


        # gaugeTxtSizer = wx.BoxSizer(wx.VERTICAL)
        # self.gaugeTxt = wx.StaticText(self, label=self.gaugeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL)
        # gaugeTxtSizer.Add((-1, 10), 0, wx.EXPAND)
        # gaugeTxtSizer.Add(self.gaugeTxt, 0, wx.EXPAND|wx.CENTRE)


        # #after gauge text
        # gaugeCtrlSizer2 = wx.BoxSizer(wx.VERTICAL)
        # self.gaugeCtrl2 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        # gaugeCtrlSizer2.Add((-1, 10), 0, wx.EXPAND)
        # gaugeCtrlSizer2.Add(self.gaugeCtrl2, 0, wx.EXPAND)

        horizontalSizer2.Add(positionMethodSizerV, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer2.Add(gaugeCtrlSizer, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer2.Add(gauge1RadButSizerV, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer2.Add(gauge2RadButSizerV, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        # horizontalSizer2.Add(gaugeTxtSizer, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        horizontalSizer2.Add(gaugeSizerV, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)

        # horizontalSizer2.Add(gaugeCtrlSizer2, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        # horizontalSizer2.Add((40, -1), 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)




        #Third Row of items
        horizontalSizer3 = wx.BoxSizer(wx.HORIZONTAL)



        #Serial Number
        serialSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.serialTxt = wx.StaticText(self, label=self.serialNumLbl, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL)
        self.serialCmbo = wx.ComboBox(self, size=(75, 23), style=wx.CB_DROPDOWN, choices = self.serialNumList)
        self.serialCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.serialCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)
        # self.serialCmbo = cb.ComboCtrl(self, style=wx.CB_SORT|wx.TE_LEFT, size=(80, -1))
        # self.serialPopup = ComboCtrlPopup.ComboCtrlPopup()
        # self.serialCmbo.SetPopupControl(self.serialPopup)
        # # self.serialPopup.AddItems(self.serialNumList)
        # self.serialCmbo.SetPopupMinWidth(80)

        serialSizer.Add(self.serialTxt, 0, wx.EXPAND|wx.RIGHT, 5)
        serialSizer.Add(self.serialCmbo, 0, wx.EXPAND|wx.RIGHT, 5)

        serialSizerV = wx.BoxSizer(wx.VERTICAL)
        serialSizerV.Add((-1, -1), 1, wx.EXPAND)
        serialSizerV.Add(serialSizer, 0, wx.EXPAND)
        serialSizerV.Add((-1, -1), 1, wx.EXPAND)













        #Instrument Text and Combo
        # instrumentSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.instrumentTxt = wx.StaticText(self, label=self.instrumentLbl, style=wx.ALIGN_LEFT)
        self.instrumentCmbo = wx.ComboBox(self, size=(75, -1), choices=self.instrumentList, style=wx.CB_DROPDOWN)
        self.instrumentCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.instrumentCmbo.Bind(wx.EVT_TEXT, self.OnInstrumentChange)
        self.instrumentCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        # instrumentSizer.Add(self.instrumentTxt, 1, wx.EXPAND|wx.RIGHT, 5)
        # instrumentSizer.Add(self.instrumentCmbo, 2, wx.EXPAND|wx.LEFT, 5)



        #Manufacture Text and Combo
        # manufactureSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.manufactureTxt = wx.StaticText(self, label=self.manufactureLbl, style=wx.ALIGN_LEFT)
        self.manufactureCmbo = wx.ComboBox(self, size=(75, -1), choices=self.manufactureList, style=wx.CB_DROPDOWN)
        self.manufactureCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.manufactureCmbo.Bind(wx.EVT_TEXT, self.OnManufactruerChange)
        self.manufactureCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        # manufactureSizer.Add(self.manufactureTxt, 1, wx.EXPAND|wx.RIGHT, 5)
        # manufactureSizer.Add(self.manufactureCmbo, 2, wx.EXPAND|wx.LEFT, 5)



        #Model Text and Combo
        # modelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modelTxt = wx.StaticText(self, label=self.modelLbl, style=wx.ALIGN_LEFT)
        self.modelCmbo = wx.ComboBox(self, size=(75, -1), choices=self.modelList, style=wx.CB_DROPDOWN)
        self.modelCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)
        # self.modelCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)

        # modelSizer.Add(self.modelTxt, 1, wx.EXPAND|wx.RIGHT, 5)
        # modelSizer.Add(self.modelCmbo, 2, wx.EXPAND|wx.LEFT, 5)



        horizontalSizer3.Add(serialSizerV, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer3.Add(self.instrumentTxt, 1, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        horizontalSizer3.Add(self.instrumentCmbo, 2, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        horizontalSizer3.Add(self.manufactureTxt, 1, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        horizontalSizer3.Add(self.manufactureCmbo, 2, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        horizontalSizer3.Add(self.modelTxt, 1, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        horizontalSizer3.Add(self.modelCmbo, 2, wx.EXPAND|wx.TOP|wx.RIGHT, 5)






        #Forth Row of items
        horizontalSizer4 = wx.BoxSizer(wx.HORIZONTAL)


        #frequency text and ctrl
        self.frequencyTxt = wx.StaticText(self, label=self.freqLbl, style=wx.ALIGN_LEFT)
        self.frequencyCmbo = MyComboBox(self, size=(180, -1), choices=self.frequnecies, style=wx.CB_DROPDOWN)
        self.frequencyCmbo.Bind(wx.EVT_TEXT, self.OnIntText)
        self.frequencyCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        #firmware text and ctrl
        self.firmwareTxt = wx.StaticText(self, label=self.firmwareLbl, style=wx.ALIGN_LEFT)
        self.firmwareCmbo = wx.ComboBox(self, size=(180, -1), choices=self.firmware, style=wx.CB_DROPDOWN)
        self.firmwareCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        #software text and ctrl
        self.softwareTxt = wx.StaticText(self, label=self.softwareLbl, style=wx.ALIGN_LEFT)
        self.softwareCtrl = wx.TextCtrl(self, size=(180, -1), style=wx.TE_PROCESS_ENTER)
        self.softwareCtrl.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)


        horizontalSizer4.Add(self.frequencyTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer4.Add(self.frequencyCmbo, 2, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer4.Add(self.firmwareTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer4.Add(self.firmwareCmbo, 2, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer4.Add(self.softwareTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        horizontalSizer4.Add(self.softwareCtrl, 2, wx.EXPAND|wx.RIGHT|wx.TOP, 5)


        # horizontalSizer4V = wx.BoxSizer(wx.VERTICAL)
        # horizontalSizer4V.Add((-1,-1), 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        # horizontalSizer4V.Add(horizontalSizer4, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        # horizontalSizer4V.Add((-1,-1), 1, wx.EXPAND|wx.RIGHT|wx.TOP, 5)




        #Midsection Method Panel
        midsectionMethodSizer = wx.BoxSizer(wx.VERTICAL)

        self.midsectionMethodTxt = wx.StaticText(self, label=self.midsectionInfoLbl)

        self.midsectionMethodInfoPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        midsectionMethodInfoSizer = wx.BoxSizer(wx.VERTICAL)
        self.midsectionMethodInfoPanel.SetSizer(midsectionMethodInfoSizer)

        #First row of midsection method info
        mmiHorizontalSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        #number of panel text and scroll
        self.numOfPanelsTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.numOfPanelLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        # self.numOfPanelsScroll = wx.SpinCtrl(self.midsectionMethodInfoPanel, value='20', min=0, max=999, size=(50,-1))
        # self.numOfPanelsScroll = wx.lib.intctrl.IntCtrl(self.midsectionMethodInfoPanel, size=(50, -1))
        self.numOfPanelsScroll = MyComboBox(self.midsectionMethodInfoPanel, choices=self.numberOfPanelsList, size=(50, -1), style=wx.CB_DROPDOWN)
        # self.numOfPanelsScroll = MyTextCtrl(self.midsectionMethodInfoPanel, size=(50, -1))
        self.numOfPanelsScroll.Bind(wx.EVT_TEXT, self.OnIntText)
        self.numOfPanelsScroll.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)
        # self.numOfPanelsScroll.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.DefaultPanels)
        # self.numOfPanelsScroll.SetValue("20")

        #flow angle text and combo box
        self.flowAngleTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.flowAngleLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.flowAngleCmbo = wx.ComboBox(self.midsectionMethodInfoPanel, choices=self.flowAngleList, size=(180, -1), style=wx.CB_DROPDOWN)
        self.flowAngleCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.flowAngleCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        #coefficient text and ctrl
        self.coEffTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.coEffLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.coEffCtrl = MyComboBox(self.midsectionMethodInfoPanel, choices=self.coefficientList, style=wx.CB_DROPDOWN, size=(180, -1))
        # self.coEffCtrl = wx.TextCtrl(self.midsectionMethodInfoPanel, style=wx.TE_PROCESS_ENTER, size=(180, -1))
        # self.coEffCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.coEffCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        self.coEffCtrl.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)
        mmiHorizontalSizer1.Add(self.numOfPanelsTxt, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        mmiHorizontalSizer1.Add(self.numOfPanelsScroll, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        mmiHorizontalSizer1.Add((-1, -1), 1, wx.EXPAND)
        mmiHorizontalSizer1.Add(self.flowAngleTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        mmiHorizontalSizer1.Add(self.flowAngleCmbo, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        mmiHorizontalSizer1.Add((-1, -1), 1, wx.EXPAND)
        mmiHorizontalSizer1.Add(self.coEffTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        mmiHorizontalSizer1.Add(self.coEffCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)


        #Second row of midsection method info
        mmiHorizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        #method text and combo box
        self.methodTxtSizer = wx.BoxSizer(wx.VERTICAL)
        self.methodTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.methodLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.methodTxtSizer.Add((-1, -1), 1, wx.EXPAND)
        self.methodTxtSizer.Add(self.methodTxt, 0, wx.EXPAND)
        self.methodTxtSizer.Add((-1, -1), 1, wx.EXPAND)

        self.methodCmbSizer = wx.BoxSizer(wx.VERTICAL)
        self.methodCmbo = wx.ComboBox(self.midsectionMethodInfoPanel, choices=self.methodList, style=wx.CB_DROPDOWN)
        self.methodCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.methodCmbSizer.Add((-1, -1), 1, wx.EXPAND)
        self.methodCmbSizer.Add(self.methodCmbo, 0, wx.EXPAND)
        self.methodCmbSizer.Add((-1, -1), 1, wx.EXPAND)

        #located text
        self.locatedTxtSizer = wx.BoxSizer(wx.VERTICAL)
        self.locatedTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.locatedLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.locatedTxtSizer.Add((-1, -1), 1, wx.EXPAND)
        self.locatedTxtSizer.Add(self.locatedTxt, 0, wx.EXPAND)
        self.locatedTxtSizer.Add((-1, -1), 1, wx.EXPAND)

        #metres ctrl and metres above text
        self.metresCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        # self.metresCtrl = wx.TextCtrl(self.midsectionMethodInfoPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(80, -1))
        self.metresCtrl = wx.ComboBox(self.midsectionMethodInfoPanel, choices=self.locatedList, size=(80, -1), style=wx.CB_DROPDOWN)
        self.metresCtrlSizer.Add((-1, -1), 1, wx.EXPAND)
        self.metresCtrlSizer.Add(self.metresCtrl, 0, wx.EXPAND)
        self.metresCtrlSizer.Add((-1, -1), 1, wx.EXPAND)

        self.metresAboveTxtSizer = wx.BoxSizer(wx.VERTICAL)
        self.metresAboveTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.metresAboveLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metresAboveTxtSizer.Add((-1, -1), 1, wx.EXPAND)
        self.metresAboveTxtSizer.Add(self.metresAboveTxt, 0, wx.EXPAND)
        self.metresAboveTxtSizer.Add((-1, -1), 1, wx.EXPAND)

        #weight ctrl, and text after radio button box
        self.weightCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        #self.weightCtrl = MyTextCtrl(self.midsectionMethodInfoPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(40, -1))
        self.weightCtrl = MyComboBox(self.midsectionMethodInfoPanel, choices=self.weightList, size=(55, -1), style=wx.CB_DROPDOWN)
        self.weightCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.weightCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        self.weightCtrl.Enable(False)
        self.weightCtrlSizer.Add((-1, -1), 1, wx.EXPAND)
        self.weightCtrlSizer.Add(self.weightCtrl, 0, wx.EXPAND|wx.TOP, 5)
        self.weightCtrlSizer.Add((-1, -1), 1, wx.EXPAND)

        self.weightRadButBox = wx.RadioBox(self.midsectionMethodInfoPanel, choices=[self.poundLbl, self.kilogramLbl], style=wx.RA_HORIZONTAL)
        self.weightRadButBox.Enable(False)
        self.weightRadButBox.Bind(wx.EVT_RADIOBOX, self.OnWeightRadButBox)

        self.weightTxtSizer = wx.BoxSizer(wx.VERTICAL)
        self.weightTxt = wx.StaticText(self.midsectionMethodInfoPanel, label=self.weightLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.weightTxt.Enable(False)
        self.weightTxtSizer.Add((-1, -1), 1, wx.EXPAND)
        self.weightTxtSizer.Add(self.weightTxt, 0, wx.EXPAND)
        self.weightTxtSizer.Add((-1, -1), 1, wx.EXPAND)




        self.weightRadBut2Sizer = wx.BoxSizer(wx.VERTICAL)
        self.weightRadBut2 = wx.RadioButton(self.midsectionMethodInfoPanel, -1, self.noweightLbl, style=wx.RB_GROUP)
        self.weightRadBut2Sizer.Add((-1, -1), 1, wx.EXPAND)
        self.weightRadBut2Sizer.Add(self.weightRadBut2, 0, wx.EXPAND)
        self.weightRadBut2Sizer.Add((-1, -1), 1, wx.EXPAND)
        self.weightRadBut2.Bind(wx.EVT_RADIOBUTTON, self.OnWeightRadBut)

        self.weightRadBut1Sizer = wx.BoxSizer(wx.VERTICAL)
        self.weightRadBut1 = wx.RadioButton(self.midsectionMethodInfoPanel, -1, "")
        self.weightRadBut1Sizer.Add((-1, -1), 1, wx.EXPAND)
        self.weightRadBut1Sizer.Add(self.weightRadBut1, 0, wx.EXPAND)
        self.weightRadBut1Sizer.Add((-1, -1), 1, wx.EXPAND)
        self.weightRadBut1.Bind(wx.EVT_RADIOBUTTON, self.OnWeightRadBut)

        mmiHorizontalSizer2.Add(self.methodTxtSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT), 5
        mmiHorizontalSizer2.Add(self.methodCmbSizer, 0, wx.EXPAND|wx.LEFT, 5)
        # mmiHorizontalSizer2.Add((-1, -1), 1, wx.EXPAND)

        mmiHorizontalSizer2.Add(self.locatedTxtSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        mmiHorizontalSizer2.Add(self.metresCtrlSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        mmiHorizontalSizer2.Add(self.metresAboveTxtSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)

        mmiHorizontalSizer2.Add(self.weightRadBut1Sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        mmiHorizontalSizer2.Add(self.weightCtrlSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        mmiHorizontalSizer2.Add(self.weightRadButBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        mmiHorizontalSizer2.Add(self.weightTxtSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)

        #Third row of midsection method info
        mmiHorizontalSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        mmiHorizontalSizer3.Add((355, -1), 0, wx.EXPAND)
        mmiHorizontalSizer3.Add(self.weightRadBut2Sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)



        midsectionMethodInfoSizer.Add(mmiHorizontalSizer1, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        midsectionMethodInfoSizer.Add(mmiHorizontalSizer2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        midsectionMethodInfoSizer.Add(mmiHorizontalSizer3, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

        midsectionMethodSizer.Add(self.midsectionMethodTxt, 0, wx.EXPAND|wx.LEFT, 10)
        midsectionMethodSizer.Add(self.midsectionMethodInfoPanel, 0, wx.EXPAND)


        #ADCP info panel
        adcpSizer = wx.BoxSizer(wx.VERTICAL)

        self.adcpTxt = wx.StaticText(self, label=self.adcpInfoLbl)

        self.adcpInfoPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        adcpInfoSizer = wx.BoxSizer(wx.VERTICAL)
        self.adcpInfoPanel.SetSizer(adcpInfoSizer)



        #Second row of adcp info
        adcpHorizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        #config text, combo box, and ctrl
        self.configTxt = wx.StaticText(self.adcpInfoPanel, label=self.configLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.configCmbo = wx.ComboBox(self.adcpInfoPanel, choices=self.configList, size=(85, -1), style=wx.CB_DROPDOWN)
        self.configCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        self.configCmbo.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)
        self.configCtrl = wx.TextCtrl(self.adcpInfoPanel, size=(180, -1), style=wx.TE_PROCESS_ENTER)
        self.configCtrl.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        #ADCP set to clock and diagnostic test check
        self.adcpSetToClockCB = wx.CheckBox(self.adcpInfoPanel, label=self.adcpSetToClockLbl, style=wx.ALIGN_LEFT)
        self.diagTestCB = wx.CheckBox(self.adcpInfoPanel, label=self.diagTestLbl, style=wx.ALIGN_LEFT)
        self.diagTestCB.Bind(wx.EVT_CHECKBOX, self.OnChangeResetBGColour)
        self.adcpSetToClockCB.Bind(wx.EVT_CHECKBOX, self.OnChangeResetBGColour)


        adcpHorizontalSizer2.Add(self.configTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        adcpHorizontalSizer2.Add(self.configCmbo, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        adcpHorizontalSizer2.Add(self.configCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        adcpHorizontalSizer2.Add((-1, -1), 1, wx.EXPAND)
        adcpHorizontalSizer2.Add(self.adcpSetToClockCB, 0, wx.EXPAND|wx.LEFT, 20)
        adcpHorizontalSizer2.Add(self.diagTestCB, 0, wx.EXPAND|wx.LEFT, 23)


        #Third row of adcp info
        adcpHorizontalSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        #adcp depth text and ctrl
        self.adcpDepthTxt = wx.StaticText(self.adcpInfoPanel, label=self.adcpDepthLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.adcpDepthCtrl = MyTextCtrl(self.adcpInfoPanel, size=(50, -1), style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)

        self.adcpDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.adcpDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.adcpDepthCtrl.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        #magn decl text and ctrl
        self.magnDeclTxt = wx.StaticText(self.adcpInfoPanel, label=self.magnDeclLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.magnDeclCtrl = MyTextCtrl(self.adcpInfoPanel, size=(50, -1), style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.magnDeclCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.magnDeclCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round1)
        self.magnDeclCtrl.Bind(wx.EVT_TEXT, self.OnChangeResetBGColour)

        #ADCP set to clock and diagnostic test check
        self.compassCaliCB = wx.CheckBox(self.adcpInfoPanel, label=self.compCaliLbl, style=wx.ALIGN_LEFT)
        self.passedFieldRevCB = wx.CheckBox(self.adcpInfoPanel, label=self.passedFieldRevLbl, style=wx.ALIGN_LEFT)
        self.compassCaliCB.Bind(wx.EVT_CHECKBOX, self.OnChangeResetBGColour)
        self.passedFieldRevCB.Bind(wx.EVT_CHECKBOX, self.OnChangeResetBGColour)


        adcpHorizontalSizer3.Add(self.adcpDepthTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        adcpHorizontalSizer3.Add(self.adcpDepthCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        adcpHorizontalSizer3.Add((-1, -1), 1, wx.EXPAND)
        adcpHorizontalSizer3.Add(self.magnDeclTxt, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        adcpHorizontalSizer3.Add(self.magnDeclCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        adcpHorizontalSizer3.Add((-1, -1), 1, wx.EXPAND)
        adcpHorizontalSizer3.Add(self.compassCaliCB, 0, wx.EXPAND|wx.LEFT, 10)
        adcpHorizontalSizer3.Add(self.passedFieldRevCB, 0, wx.EXPAND)


        # adcpInfoSizer.Add(adcpHorizontalSizer1, 0, wx.EXPAND|wx.ALL, 3)
        adcpInfoSizer.Add(adcpHorizontalSizer2, 0, wx.EXPAND|wx.ALL, 3)
        adcpInfoSizer.Add(adcpHorizontalSizer3, 0, wx.EXPAND|wx.ALL, 3)

        adcpSizer.Add(self.adcpTxt, 0, wx.EXPAND|wx.LEFT, 10)
        adcpSizer.Add(self.adcpInfoPanel, 0, wx.EXPAND)






        #Control and Remarks
        controlRemarksSizer = wx.BoxSizer(wx.VERTICAL)

        controlConditionPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        controlConditionSizer = wx.BoxSizer(wx.HORIZONTAL)
        controlConditionPanel.SetSizer(controlConditionSizer)

        self.picturedCkbox = wx.CheckBox(controlConditionPanel, label=self.picturedLbl)
        self.preUseCableTxt = wx.StaticText(controlConditionPanel, label=self.preUseCableLbl)
        self.preUseCableCmbo = wx.ComboBox(controlConditionPanel, style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER, size=(100, -1), choices=self.preUseCableList)

        controlConditionSizer.Add(self.picturedCkbox, 0, wx.EXPAND|wx.ALL, 5)
        controlConditionSizer.Add(self.preUseCableTxt, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        controlConditionSizer.Add(self.preUseCableCmbo, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)

        


        # remarksPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        # remarksSizer = wx.BoxSizer(wx.HORIZONTAL)
        # remarksPanel.SetSizer(remarksSizer)

        # dischargeRemarkSizer = wx.BoxSizer(wx.VERTICAL)
        # self.dischTxt = wx.StaticText(remarksPanel, label=self.dischLbl)
        # self.dischRemarksCtrl = wx.TextCtrl(remarksPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, 200))
        # dischargeRemarkSizer.Add(self.dischTxt, 0)
        # dischargeRemarkSizer.Add(self.dischRemarksCtrl, 0, wx.EXPAND)
        
        
        # #control condition remarks
        # controlConditionRemarkSizer = wx.BoxSizer(wx.VERTICAL)
        # controlConditionTxt = wx.StaticText(remarksPanel, label=self.controlConditionRemLbl)
        # self.controlConditionRemarksCtrl = wx.TextCtrl(remarksPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, -1))
        # controlConditionRemarkSizer.Add(controlConditionTxt, 0, wx.EXPAND)
        # controlConditionRemarkSizer.Add(self.controlConditionRemarksCtrl, 1, wx.EXPAND)



        # stageRemarkSizer = wx.BoxSizer(wx.VERTICAL)
        # stageTxt = wx.StaticText(remarksPanel, label=self.stageLbl)
        # self.stageRemarksCtrl = wx.TextCtrl(remarksPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, 200))
        # stageRemarkSizer.Add(stageTxt, 0)
        # stageRemarkSizer.Add(self.stageRemarksCtrl, 0, wx.EXPAND)

        # stationRemarkSizer = wx.BoxSizer(wx.VERTICAL)
        # stationHealthTxt = wx.StaticText(remarksPanel, label=self.stnLbl)
        # self.stationHealthRemarksCtrl = wx.TextCtrl(remarksPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, 200))
        # stationRemarkSizer.Add(stationHealthTxt, 0)
        # stationRemarkSizer.Add(self.stationHealthRemarksCtrl, 0, wx.EXPAND)




        # remarksSizer.Add(dischargeRemarkSizer, 1, wx.EXPAND)
        # remarksSizer.Add(controlConditionRemarkSizer, 1, wx.EXPAND)
        # remarksSizer.Add(stageRemarkSizer, 1, wx.EXPAND)
        # remarksSizer.Add(stationRemarkSizer, 1, wx.EXPAND)

        controlRemarksSizer.Add(controlConditionPanel, 1, wx.EXPAND)
        # controlRemarksSizer.Add(remarksPanel, 0, wx.EXPAND)





        # #Control and Remarks
        # controlRemarksSizer = wx.BoxSizer(wx.HORIZONTAL)

#         #control
#         controlSizer = wx.BoxSizer(wx.VERTICAL)
#         controlTxt = wx.StaticText(self, label=self.controlLbl)

#         controlPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(200, 200))
#         controlPanelSizer = wx.BoxSizer(wx.VERTICAL)
#         controlPanel.SetSizer(controlPanelSizer)

#         #Control Condition
#         controlConditionSizer = wx.BoxSizer(wx.HORIZONTAL)
#         controlConditionTxt = wx.StaticText(controlPanel, label=self.contCondLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
#         self.controlConditionCmbo = wx.ComboBox(controlPanel, choices=self.contCondList, style=wx.CB_READONLY)
#         self.controlConditionCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
#         controlConditionSizer.Add((5, -1), 0, wx.EXPAND)
#         controlConditionSizer.Add(controlConditionTxt, 0, wx.EXPAND|wx.TOP, 8)
#         controlConditionSizer.Add(self.controlConditionCmbo, 1, wx.EXPAND|wx.ALL, 3)

# ##        #Effect combo boxes
# ##        controlEffSizer = wx.BoxSizer(wx.HORIZONTAL)
# ##        controlEffSizerV = wx.BoxSizer(wx.VERTICAL)
# ##        controlEffTxt = wx.StaticText(controlPanel, label=self.contEffLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
# ##        self.controlEffCatCmbo = wx.ComboBox(controlPanel, choices=self.contEffCatList, size=(140, -1), style=wx.CB_READONLY)
# ##        self.controlEffSubCatCmbo = wx.ComboBox(controlPanel, size=(60, -1), style=wx.TE_PROCESS_ENTER)
# ##        controlEffSizerV.Add(self.controlEffCatCmbo, 1, wx.EXPAND|wx.ALL, 3)
# ##        controlEffSizerV.Add(self.controlEffSubCatCmbo, 1, wx.EXPAND|wx.ALL, 3)
# ##        controlEffSizer.Add((5, -1), 0, wx.EXPAND)
# ##        controlEffSizer.Add(controlEffTxt, 0, wx.EXPAND|wx.TOP, 8)
# ##        controlEffSizer.Add(controlEffSizerV, 1, wx.EXPAND)
# ##
# ##        self.controlEffCatCmbo.Bind(wx.EVT_COMBOBOX, self.OnControlCategoryUpdate)

#         #control remarks
#         controlRemarksTxt = wx.StaticText(controlPanel, label=self.contRemLbl)
#         self.controlRemarksCtrl = wx.TextCtrl(controlPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP)


#         controlPanelSizer.Add(controlConditionSizer, 0, wx.EXPAND)
# ##        controlPanelSizer.Add(controlEffSizer, 0, wx.EXPAND)
#         controlPanelSizer.Add(controlRemarksTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         controlPanelSizer.Add(self.controlRemarksCtrl, 1, wx.EXPAND)

#         controlSizer.Add(controlTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         controlSizer.Add(controlPanel, 0, wx.EXPAND)

#         #Discharge
#         dischSizer = wx.BoxSizer(wx.VERTICAL)
#         self.dischTxt = wx.StaticText(self, label=self.dischLbl)

#         dischPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(100, 200))
#         dischPanelSizer = wx.BoxSizer(wx.VERTICAL)
#         dischPanel.SetSizer(dischPanelSizer)

#         dischRemarksTxt = wx.StaticText(dischPanel, label=self.dischRemLbl)
#         self.dischRemarksCtrl = wx.TextCtrl(dischPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP)

#         dischPanelSizer.Add(dischRemarksTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         dischPanelSizer.Add(self.dischRemarksCtrl, 1, wx.EXPAND)

#         dischSizer.Add(self.dischTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         dischSizer.Add(dischPanel, 0, wx.EXPAND)

#         #Stage
#         stageSizer = wx.BoxSizer(wx.VERTICAL)
#         stageTxt = wx.StaticText(self, label=self.stageLbl)

#         stagePanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(100, 200))
#         stagePanelSizer = wx.BoxSizer(wx.VERTICAL)
#         stagePanel.SetSizer(stagePanelSizer)

#         stageRemarksTxt = wx.StaticText(stagePanel, label=self.stageRemLbl)
#         self.stageRemarksCtrl = wx.TextCtrl(stagePanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP)

#         stagePanelSizer.Add(stageRemarksTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         stagePanelSizer.Add(self.stageRemarksCtrl, 1, wx.EXPAND)

#         stageSizer.Add(stageTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         stageSizer.Add(stagePanel, 0, wx.EXPAND)

#         #General
#         genSizer = wx.BoxSizer(wx.VERTICAL)
#         genTxt = wx.StaticText(self, label=self.genLbl)

#         genPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=(100, 200))
#         genPanelSizer = wx.BoxSizer(wx.VERTICAL)
#         genPanel.SetSizer(genPanelSizer)

#         genRemarksTxt = wx.StaticText(genPanel, label=self.genRemLbl)
#         self.genRemarksCtrl = wx.TextCtrl(genPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP)

#         genPanelSizer.Add(genRemarksTxt, 0, wx.EXPAND|wx.LEFT, 10)
#         genPanelSizer.Add(self.genRemarksCtrl, 1, wx.EXPAND)

#         genSizer.Add(genTxt, 0, wx.EXPAND|wx.LEFT, 0)
#         genSizer.Add(genPanel, 0, wx.EXPAND)


#         controlRemarksSizer.Add(controlSizer, 3, wx.EXPAND)
#         controlRemarksSizer.Add(dischSizer, 2, wx.EXPAND)
#         controlRemarksSizer.Add(stageSizer, 2, wx.EXPAND)
#         controlRemarksSizer.Add(genSizer, 2, wx.EXPAND)


        self.layoutSizer.Add(horizontalSizer1, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(horizontalSizer2, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(horizontalSizer3, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(horizontalSizer4, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(midsectionMethodSizer, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 5)
        self.layoutSizer.Add(adcpSizer, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 5)
        self.layoutSizer.Add(controlRemarksSizer, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 5)

        self.SetSizer(self.layoutSizer)
        self.InfoUpdate(None)


    # Reset Checklist so that neither checkbox is checked
    def CheckListReset(self):
        checked = list(self.methodCBListBox.GetCheckedItems())

        for i in checked:
            self.methodCBListBox.Check(i, check=False)

    # Check the checkbox according to the highlighted listbox item
    def OnDeploymentCheckListBox(self, event):


        index = self.methodCBListBox.GetSelection()
        self.methodCBListBox.Check(index, check=True)

        self.OnDeploymentCheckListCB(event)

    #After import from the *.dis, double checking the overwriting, and updating corresponding instrument panel and Field reveiw checklist 
    def DeploymentCheckListCBCkecking4MidSection(self):

        if len(list(self.methodCBListBox.GetCheckedItems())) > 1:
            dlg = wx.MessageDialog(self, self.deploymentWarning%'Moving Boat', 'Warning',
                              wx.YES_NO | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                dlg.Destroy()
                self.methodCBListBox.Check(1)
                self.methodCBListBox.Check(0, False)
                self.DeploymentCheckListUpdate()

                if self.manager is not None:
                    self.manager.OnDeploymentUpdate()
                return True

            elif res == wx.ID_NO:
                dlg.Destroy()
                self.methodCBListBox.Check(0)
                self.methodCBListBox.Check(1, False)

                self.DeploymentCheckListUpdate()

                if self.manager is not None:
                    self.manager.OnDeploymentUpdate()
                return False
        else:
            self.DeploymentCheckListUpdate()

            if self.manager is not None:
                self.manager.OnDeploymentUpdate()
            return True


    #After import from the *.dis, double checking the overwriting, and updating corresponding instrument panel and Field reveiw checklist 
    def DeploymentCheckListCBCkecking4MovingBoat(self):

        if len(list(self.methodCBListBox.GetCheckedItems())) > 1:
            dlg = wx.MessageDialog(self, self.deploymentWarning%'Midsection', 'Warning',
                              wx.YES_NO | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                dlg.Destroy()
                self.methodCBListBox.Check(0)
                self.methodCBListBox.Check(1, False)
                self.DeploymentCheckListUpdate()

                if self.manager is not None:
                    self.manager.OnDeploymentUpdate()
                return True

            elif res == wx.ID_NO:
                dlg.Destroy()
                self.methodCBListBox.Check(1)
                self.methodCBListBox.Check(0, False)

                self.DeploymentCheckListUpdate()

                if self.manager is not None:
                    self.manager.OnDeploymentUpdate()
                return False
        else:
            self.DeploymentCheckListUpdate()

            if self.manager is not None:
                self.manager.OnDeploymentUpdate()
            return True


    # Called when the deployment method is changed
    # update the FRChecklist to appropriate list
    # Enable the appropriate fields according to Deployment Type
    def OnDeploymentCheckListCB(self, e):
        selection = [self.adcpByMovingBoatLbl, self.midsectionLbl]
        if len(list(self.methodCBListBox.GetCheckedItems())) > 1:
            dlg = wx.MessageDialog(self, self.deploymentWarning%selection[(e.GetInt()+1)%2], 'Warning',
                              wx.YES_NO | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                dlg.Destroy()

            elif res == wx.ID_NO:
                dlg.Destroy()
                self.methodCBListBox.Check(e.GetInt(), check=False)
                return False


        if len(list(self.methodCBListBox.GetCheckedItems())) == 0:
            dlg = wx.MessageDialog(self, self.deploymentWarning%selection[e.GetInt()], 'Warning',
                              wx.YES_NO | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                dlg.Destroy()

            elif res == wx.ID_NO:
                dlg.Destroy()
                self.methodCBListBox.Check(e.GetInt(), check=True)
                return







        checked = list(self.methodCBListBox.GetCheckedItems())

        lenChecked = len(checked)

        if lenChecked > 0:
            checked.remove(e.GetInt())

        for i in checked:
            self.methodCBListBox.Check(i, check=False)

        self.DeploymentCheckListUpdate()

        if self.manager is not None:
            self.manager.OnDeploymentUpdate()

        e.Skip()
        return True




    # Enable appropriate fields according to Deployment Type
    # Update the Dropdown list of Deployment Methods
    def DeploymentCheckListUpdate(self):
        # print "DeploymentCheckListUpdate"
        checked = list(self.methodCBListBox.GetCheckedItems())
        lenChecked = len(checked)

        # print "checked length %s" % lenChecked

        if lenChecked > 0:
            checked = list(self.methodCBListBox.GetCheckedItems())
            check = checked[0]

            self.InfoUpdate(check)

            if check == 0: #ADCP
                self.UpdateComboBox(self.deploymentCmbo, self.deploymentADCPList)
                self.UpdateComboBox(self.modelCmbo, self.modelList1)
                self.UpdateComboBox(self.instrumentCmbo, ['ADCP'])
                self.instrumentCmbo.SetValue('ADCP')
                self.OnChangeUpdateMovingBoat()
                if self.manager is not None:
                    if self.manager.manager is not None:
                        self.manager.manager.FlatNoteBook.GetPage(2).Enable(True)
                        self.manager.manager.FlatNoteBook.GetPage(3).Enable(False)
            elif check == 1: #MidSection
                # self.instrumentCmbo.SetValue('')
                self.UpdateComboBox(self.deploymentCmbo, self.deploymentMidsecList)
                self.UpdateComboBox(self.modelCmbo, self.modelList)
                self.UpdateComboBox(self.instrumentCmbo, self.instrumentList)
                self.manager.OnInstrumentChange(-1)
                if self.manager is not None:
                    if self.manager.manager is not None:
                        self.manager.manager.FlatNoteBook.GetPage(2).Enable(False)
                        self.manager.manager.FlatNoteBook.GetPage(3).Enable(True)

        else:
            self.InfoUpdate(None)
            self.manager.manager.FlatNoteBook.GetPage(2).Enable(True)
            self.manager.manager.FlatNoteBook.GetPage(3).Enable(True)
        self.OnChangeUpdateMovingBoat()
        self.manager.manager.gui.Layout()


    # Updates the dropdown with the given lis
    def UpdateComboBox(self, combo, lis):
        combo.Clear()
        combo.AppendItems(lis)


    # Called to enable the appropriate fields
    def InfoUpdate(self, check):

        if check is None:
            self.EnableGeneralInfo(False)
            self.EnableMidsectionInfo(False)
            self.EnableAdcpInfo(False)
            self.instrumentCmbo.SetValue('')
        else:
            if check == 0: #ADCP
                self.EnableAdcpInfo(True)
                self.EnableMidsectionInfo(False)

            elif check == 1: #MidSection

                self.EnableMidsectionInfo(True)
                self.EnableAdcpInfo(True)

            self.EnableGeneralInfo(True)


    # When a checkbox is clicked, update the view accordingly
    def OnDeploymentSelect(self, evt):
        checked = list(self.methodCBListBox.GetCheckedItems())
        # print checked
        lenChecked = len(checked)

        if lenChecked > 0:
            check = checked[0]

            if check == 1: #1 = Midsection
                self.DeploymentUpdate()

    # Updates the view depending on which checkbox is clicked
    def DeploymentUpdate(self):

        selectedVal = str(self.deploymentCmbo.GetValue())

        if selectedVal != "":
            if selectedVal in self.deploymentADCPList:
                self.EnableAdcpInfo(True)
                self.EnableMidsectionInfo(False)
            else:
                self.EnableAdcpInfo(False)
                self.EnableMidsectionInfo(True)



    # def OnControlCategoryUpdate(self, evt):
    #     categoryIndex = self.controlEffCatCmbo.GetSelection()
    #
    #     self.UpdateComboBox(self.controlEffSubCatCmbo, self.contEffSubCatList[categoryIndex])


    def EnableGeneralInfo(self, en):
        self.deploymentTxt.Enable(en)
        self.deploymentCmbo.Enable(en)
        self.positionMethodTxt.Enable(en)
        self.positionMethodCmbo.Enable(en)
        self.instrumentTxt.Enable(en)
        self.instrumentCmbo.Enable(en)
        self.serialTxt.Enable(en)
        self.serialCmbo.Enable(en)
        self.manufactureTxt.Enable(en)
        self.modelTxt.Enable(en)
        self.frequencyTxt.Enable(en)
        self.firmwareTxt.Enable(en)
        self.softwareTxt.Enable(en)
        # self.gaugeTxt.Enable(en)
        self.gaugeCtrl.Enable(en)
        self.gaugeOtherTxt.Enable(en)
        # self.gaugeCtrl2.Enable(en)
        self.lengthRadButBox.Enable(en)
        self.posRadButBox.Enable(en)
        self.gauge1RadButBox.Enable(en)
        self.gauge2RadButBox.Enable(en)
        self.manufactureCmbo.Enable(en)
        self.modelCmbo.Enable(en)
        self.frequencyCmbo.Enable(en)
        self.firmwareCmbo.Enable(en)
        self.softwareCtrl.Enable(en)
        if not en:

            self.deploymentCmbo.ChangeValue("")
            self.positionMethodCmbo.ChangeValue("")
            self.instrumentCmbo.ChangeValue("")
            self.serialCmbo.ChangeValue("")
            self.gaugeCtrl.ChangeValue("")
            self.gaugeOtherTxt.ChangeValue("")
            self.manufactureCmbo.ChangeValue("")
            self.modelCmbo.ChangeValue("")
            self.frequencyCmbo.ChangeValue("")
            self.firmwareCmbo.ChangeValue("")
            self.softwareCtrl.ChangeValue("")
            self.ResetBGColorGeneralInfo()

    def EnableMidsectionInfo(self, en):

        self.midsectionMethodInfoPanel.Enable(en)
        self.midsectionMethodTxt.Enable(en)
        

        self.numOfPanelsTxt.Enable(en)
        self.numOfPanelsScroll.Enable(en)
        self.flowAngleTxt.Enable(en)
        self.flowAngleCmbo.Enable(en)
        self.coEffTxt.Enable(en)
        self.coEffCtrl.Enable(en)
        self.methodTxt.Enable(en)
        self.methodCmbo.Enable(en)
        self.locatedTxt.Enable(en)
        self.metresCtrl.Enable(en)
        self.metresAboveTxt.Enable(en)
        self.weightRadBut2.Enable(en)
        self.weightRadBut1.Enable(en)



        if not en:
            self.flowAngleCmbo.ChangeValue("")
            self.coEffCtrl.ChangeValue("")
            self.methodCmbo.SetValue("")
            self.metresCtrl.ChangeValue("")
            self.weightCtrl.ChangeValue("")
            self.numOfPanelsScroll.SetValue("")
            self.ResetBGColorMidSectionInfo()



    def EnableAdcpInfo(self, en):

        self.adcpTxt.Enable(en)
        self.adcpInfoPanel.Enable(en)
        if not en:
            self.configCmbo.ChangeValue("")
            self.configCtrl.ChangeValue("")
            self.adcpDepthCtrl.ChangeValue("")
            self.magnDeclCtrl.ChangeValue("")
            self.adcpSetToClockCB.SetValue(False)
            self.diagTestCB.SetValue(False)
            self.compassCaliCB.SetValue(False)
            self.passedFieldRevCB.SetValue(False)
            self.ResetBGColorADCPInfo()





    def EnableWeight(self, en):
        self.weightCtrl.Enable(en)
        self.weightRadButBox.Enable(en)
        self.weightTxt.Enable(en)



    def OnWeightRadBut(self, e):
        if self.weightRadBut2.GetValue():
            self.EnableWeight(False)
            self.weightCtrl.SetValue("")
        else:
            self.EnableWeight(True)
    def update(self, serialNum, instr, manu, model, fre):
        self.serialNumList = serialNum
        self.instruments = instr
        self.manufactureList = sorted(list(set(manu)))
        self.models = model
        self.frequnecyList = sorted(list(set(fre)))
        # self.firmware = sorted(list(set(firmware)))
        self.serialCmbo.Clear()
        self.serialCmbo.AppendItems(self.serialNumList)

        self.UpdateComboBox(self.manufactureCmbo, self.manufactureList)
        self.UpdateComboBox(self.frequencyCmbo, self.frequnecyList)
        # self.UpdateComboBox(self.firmwareCmbo, self.firmware)



    # def EnableMidADCP(self, enable):
    #     print "EnableMidADCP", enable

    #     if not enable and self.methodCBListBox.IsChecked(1):
    #         self.methodCmbo.SetValue("ADCP")
    #         self.metresCtrl.SetValue("")
    #         self.weightCtrl.SetValue("")
    #     else:
    #         self.methodCmbo.SetValue("")

    #     self.methodCmbo.Enable(enable)
    #     self.locatedTxt.Enable(enable)
    #     self.metresCtrl.Enable(enable)
    #     self.metresAboveTxt.Enable(enable)
    #     self.weightCtrl.Enable(enable)
    #     self.weightTxt.Enable(enable)
    #     self.weightRadBut2.Enable(enable)
    #     self.weightRadBut1.Enable(enable)
    #     self.weightRadButBox.Enable(enable)




    def ResetBGColorADCPInfo(self):
        self.configCmbo.SetBackgroundColour(self.white)
        self.adcpDepthCtrl.SetBackgroundColour(self.white)
        self.configCtrl.SetBackgroundColour(self.white)
        self.magnDeclCtrl.SetBackgroundColour(self.white)
        self.diagTestCB.SetBackgroundColour(self.white)


    def ResetBGColorMidSectionInfo(self):
        self.numOfPanelsScroll.SetBackgroundColour(self.white)
        self.flowAngleCmbo.SetBackgroundColour(self.white)
        self.coEffCtrl.SetBackgroundColour(self.white)
        self.methodCmbo.SetBackgroundColour(self.white)
        self.metresCtrl.SetBackgroundColour(self.white)
        self.weightCtrl.SetBackgroundColour(self.white)


    def ResetBGColorGeneralInfo(self):
        self.deploymentCmbo.SetBackgroundColour(self.white)
        self.positionMethodCmbo.SetBackgroundColour(self.white)
        self.serialCmbo.SetBackgroundColour(self.white)
        self.instrumentCmbo.SetBackgroundColour(self.white)
        self.manufactureCmbo.SetBackgroundColour(self.white)
        self.modelCmbo.SetBackgroundColour(self.white)
        self.frequencyCmbo.SetBackgroundColour(self.white)
        self.firmwareCmbo.SetBackgroundColour(self.white)
        self.softwareCtrl.SetBackgroundColour(self.white)



    def OnInstrumentChange(self, event):


        if self.instrumentCmbo.GetValue() == 'ADCP':
            self.UpdateComboBox(self.modelCmbo, self.modelList1)
            self.EnableAdcpInfo(True)
            if(self.methodCBListBox.GetCheckedStrings()[0]==self.adcpByMovingBoatLbl):
                self.EnableMidsectionInfo(False)
            else:
                self.EnableMidsectionInfo(True)
            if self.manager.manager.frChecklistManager.midsecType != 'ADCP':
                self.manager.OnInstrumentChange(3)

        elif self.instrumentCmbo.GetValue() == 'ADV':
            self.UpdateComboBox(self.modelCmbo, self.modelList3)
            self.modelCmbo.SetValue('FlowTracker')
            self.manufactureCmbo.SetValue('SonTek')
            self.EnableAdcpInfo(False)
            self.EnableMidsectionInfo(True)
            if self.manager.manager.frChecklistManager.midsecType != 'Flow Tracker':
                self.manager.OnInstrumentChange(2)
        elif self.instrumentCmbo.GetValue() == 'Current Meter':
            self.UpdateComboBox(self.modelCmbo, self.modelList2)
            self.manufactureCmbo.SetValue('')
            self.EnableAdcpInfo(False)
            self.EnableMidsectionInfo(True)
            if self.manager.manager.frChecklistManager.midsecType != 'Current Meter':
                self.manager.OnInstrumentChange(1)

        else:

            self.UpdateComboBox(self.modelCmbo, self.modelList2)
            self.manufactureCmbo.SetValue('')
            if self.methodCBListBox.IsChecked(1):
                self.EnableAdcpInfo(True)
                self.EnableMidsectionInfo(True)
            else:
                self.EnableAdcpInfo(False)
                self.EnableMidsectionInfo(False)
            if self.manager is not None:


                if self.manager.manager.frChecklistManager.midsecType != 'All':
                    self.manager.OnInstrumentChange(0)

        # if (self.instrumentCmbo.GetValue() == 'ADCP') or \
        #     not self.methodCBListBox.IsChecked(1):
        #     self.EnableAdcpInfo(True)
        # else:
        #     self.EnableAdcpInfo(False)

    def OnManufactruerChange(self, event):
        if self.instrumentCmbo.GetValue().lower() == 'adcp':
            if self.manufactureCmbo.GetValue().lower() == 'sontek':
                self.UpdateComboBox(self.modelCmbo, self.modelListTRDI)
            elif self.manufactureCmbo.GetValue().lower() == 'trdi':
                self.UpdateComboBox(self.modelCmbo, self.modelListSontek)
            else:
                self.UpdateComboBox(self.modelCmbo, self.modelList1)



    # Any update on discharge measurement will affect data on moving boat
    def OnChangeUpdateMovingBoat(self):
        if self.manager is not None:
            if self.methodCBListBox.IsChecked(0):
                self.manager.manager.movingBoatMeasurementsManager.recalculate()
            else:
                self.manager.manager.movingBoatMeasurementsManager.Clear()


    #Method Type Checkbox
    def GetMethodCBListBox(self):
        return self.methodCBListBox

    def SetMethodCBListBox(self, method):
        depMethodList = list(self.methodCBListBox.GetItems())
        if method in depMethodList:
            index = depMethodList.index(method)
            self.methodCBListBox.Check(index, check=True)
        self.DeploymentCheckListUpdate()





    #Deployment Combo
    def GetDeploymentCmbo(self):
        return self.deploymentCmbo.GetValue()


    def SetDeploymentCmbo(self, deploymentCmbo):
        self.deploymentCmbo.SetValue(deploymentCmbo)
        # self.gui.DeploymentUpdate()

        depMethodLen = len(self.methodCBListBox.GetCheckedStrings())
        if depMethodLen <= 0:
            self.InfoUpdate(None)

    #Position Method Ctrl
    def GetPositionMethodCtrl(self):
        return self.positionMethodCmbo.GetValue()


    def SetPositionMethodCtrl(self, positionMethodCmbo):
        self.positionMethodCmbo.SetValue(positionMethodCmbo)


    #Instrument Combo
    def GetInstrumentCmbo(self):
        return self.instrumentCmbo.GetValue()


    def SetInstrumentCmbo(self, instrumentCmbo):
        self.instrumentCmbo.SetValue(instrumentCmbo)


    #Instrument Combo for open saved xml
    def GetInstrumentCmboFromXml(self):
        return self.instrumentCmbo.GetValue()


    def SetInstrumentCmboFromXml(self, instrumentCmbo):
        self.instrumentCmbo.ChangeValue(instrumentCmbo)

    #Serial Number Combo
    def GetSerialCmbo(self):
        return self.serialCmbo.GetValue()
    def SetSerialCmbo(self, serialCmbo):
        self.serialCmbo.SetValue(serialCmbo)



    #Serial Number Combo for open saved xml
    def GetSerialCmboFromXml(self):
        return self.serialCmbo.GetValue()


    def SetSerialCmboFromXml(self, serialCmbo):
        self.serialCmbo.ChangeValue(serialCmbo)


    #Gauge Ctrl
    def GetGaugeCtrl(self):
        return self.gaugeCtrl.GetValue()
    def SetGaugeCtrl(self, gaugeCtrl):
        self.gaugeCtrl.SetValue(gaugeCtrl)

    #Length Radio Button Box
    def GetLengthRadButBox(self):

        return self.lengthRadButBox.GetSelection()


    def SetLengthRadButBox(self, index):
        self.lengthRadButBox.SetSelection(index)

    #Position Radio Button Box
    def GetPosRadButBox(self):
        return self.posRadButBox.GetSelection()
    def SetPosRadButBox(self, index):
        self.posRadButBox.SetSelection(index)

    # #Gauge Ctrl 2
    # def gaugeCtrl2(self):
    #     return self.gui.gaugeCtrl2.GetValue()
    # def gaugeCtrl2(self, gaugeCtrl2):
    #     self.gui.gaugeCtrl2.SetValue(gaugeCtrl2)


    #Midsection Method Info
    #Number of Panels SpinCtrl
    def GetNumOfPanelsScroll(self):
        return self.numOfPanelsScroll.GetValue()


    def SetNumOfPanelsScroll(self, numOfPanelsScroll):
        self.numOfPanelsScroll.SetValue(numOfPanelsScroll)

    #Flow Angle Combo
    def GetFlowAngleCmbo(self):
        return self.flowAngleCmbo.GetValue()

    def SetFlowAngleCmbo(self, flowAngleCmbo):
        self.flowAngleCmbo.SetValue(flowAngleCmbo)

    #Co-efficient Ctrl
    def GetCoEffCtrl(self):
        return self.coEffCtrl.GetValue()
    def SetCoEffCtrl(self, coEffCtrl):
        self.coEffCtrl.SetValue(coEffCtrl)

    #Method Combo
    def GetMethodCmbo(self):
        return self.methodCmbo.GetValue()
    def SetMethodCmbo(self, methodCmbo):
        self.methodCmbo.SetValue(methodCmbo)

    #Metres Ctrl
    def GetMetresCtrl(self):
        return self.metresCtrl.GetValue()
    def SetMetresCtrl(self, metresCtrl):
        self.metresCtrl.SetValue(metresCtrl)

    #Weight Ctrl
    def GetWeightCtrl(self):
        return self.weightCtrl.GetValue()
    def SetWeightCtrl(self, weightCtrl):
        self.weightCtrl.SetValue(weightCtrl)

    #Weight Radio Button Box
    def GetWeightRadButBox(self):
        return self.weightRadButBox.GetSelection()


    def SetWeightRadButBox(self, index):
        self.weightRadButBox.SetSelection(index)



    #ADCP Info
    #Frequency Control
    def GetFrequencyCmbo(self):

        return self.frequencyCmbo.GetValue()

    def SetFrequencyCmbo(self, frequencyCmbo):
        self.frequencyCmbo.SetValue(frequencyCmbo)

    #Firmware Control
    def GetFirmwareCmbo(self):
        return self.firmwareCmbo.GetValue()
    def SetFirmwareCmbo(self, firmwareCmbo):
        self.firmwareCmbo.SetValue(firmwareCmbo)

    #Software Control
    def GetSoftwareCtrl(self):
        return self.softwareCtrl.GetValue()
    def SetSoftwareCtrl(self, softwareCtrl):
        self.softwareCtrl.SetValue(softwareCtrl)


    #Config Combo Box
    def GetConfigCmbo(self):
        return self.configCmbo.GetValue()
    def SetConfigCmbo(self, configCmbo):
        self.configCmbo.SetValue(configCmbo)

    #Config Control
    def GetConfigCtrl(self):
        return self.configCtrl.GetValue()
    def SetConfigCtrl(self, configCtrl):
        self.configCtrl.SetValue(configCtrl)

    #ADCP Set to Clock Checkbox
    def GetAdcpSetToClockCB(self):
        return self.adcpSetToClockCB.GetValue()


    def SetAdcpSetToClockCB(self, adcpSetToClockCB):
        self.adcpSetToClockCB.SetValue(adcpSetToClockCB)

    #Diagnostic Test Checkbox
    def GetDiagTestCB(self):
        return self.diagTestCB.GetValue()
    def SetDiagTestCB(self, diagTestCB):
        self.diagTestCB.SetValue(diagTestCB)



    # ADCP Depth Checkbox
    def GetAdcpDepthCtrl(self):
        return self.adcpDepthCtrl.GetValue()

    def SetAdcpDepthCtrl(self, adcpDepthCtrl):
        self.adcpDepthCtrl.SetValue(adcpDepthCtrl)

    #Magnetic Declination Control
    def GetMagnDeclCtrl(self):
        return self.magnDeclCtrl.GetValue()
    def SetMagnDeclCtrl(self, magnDeclCtrl):
        self.magnDeclCtrl.SetValue(magnDeclCtrl)

    #Compass Calibration CB
    def GetCompassCaliCB(self):
        return self.compassCaliCB.GetValue()

    def SetCompassCaliCB(self, compassCaliCB):
        self.compassCaliCB.SetValue(compassCaliCB)

    #Passed Field Review CB
    def GetPassedFieldRevCB(self):
        return self.passedFieldRevCB.GetValue()


    def SetPassedFieldRevCB(self, passedFieldRevCB):
        self.passedFieldRevCB.SetValue(passedFieldRevCB)



    #Control and Remarks
    #Control Condition Combo
    def GetControlConditionCmbo(self):
        return self.controlConditionCmbo.GetValue()


    def SetControlConditionCmbo(self, controlConditionCmbo):
        self.controlConditionCmbo.SetValue(controlConditionCmbo)

    #Control Effect Category and Sub-Categories not currently stored
    #Control Effect Cat
    def GetControlEffCatCmbo(self):
        return self.controlEffCatCmbo.GetValue()


    def SetControlEffCatCmbo(self, controlEffCatCmbo):
        self.controlEffCatCmbo.SetValue(controlEffCatCmbo)

    #Control Effect Sub-Categories
    def GetControlEffSubCatCmbo(self):
        return self.controlEffSubCatCmbo.GetValue()


    def SetControlEffSubCatCmbo(self, controlEffSubCatCmbo):
        self.controlEffSubCatCmbo.SetValue(controlEffSubCatCmbo)

    # #Control Remarks Control
    # def controlRemarksCtrl(self):
    #     return self.gui.controlRemarksCtrl.GetValue()

    #
    # def controlRemarksCtrl(self, controlRemarksCtrl):
    #     self.gui.controlRemarksCtrl.SetValue(controlRemarksCtrl)



    #Discharge, Stage, Station Health Remarks
    def GetDischRemarksCtrl(self):
        return self.dischRemarksCtrl.GetValue()


    def SetDischRemarksCtrl(self, dischRemarksCtrl):
        self.dischRemarksCtrl.SetValue(dischRemarksCtrl)

    def GetStageRemarksCtrl(self):
        return self.stageRemarksCtrl.GetValue()


    def SetStageRemarksCtrl(self, stageRemarksCtrl):
        self.stageRemarksCtrl.SetValue(stageRemarksCtrl)

    #General
    def GetStationHealthRemarksCtrl(self):
        return self.stationHealthRemarksCtrl.GetValue()


    def SetStationHealthRemarksCtrl(self, stationHealthRemarksCtrl):
        self.stationHealthRemarksCtrl.SetValue(stationHealthRemarksCtrl)

    #Gauge or other
    def GetSelectedGauge(self):
        return self.selectedGauge

    def SetSelectedGauge(self, selectedGauge):

        self.selectedGauge = selectedGauge

        if selectedGauge == "gauge" or selectedGauge == "":

            self.gaugeOtherTxt.ChangeValue("")
            self.selectedGauge = "gauge"

            self.gauge1RadButBox.SetValue(True)
        else:
            self.gauge2RadButBox.SetValue(True)
            self.gaugeOtherTxt.SetValue(selectedGauge)



    #Gauge Display
    def GetGaugeOtherTxt(self):
        return self.gaugeOtherTxt.GetValue()

    def SetGaugeOtherTxt(self, gaugeOtherTxt):
        self.gaugeOtherTxt.SetValue(gaugeOtherTxt)


    #Gauge Radio Button 1
    def GetGauge1RadButBox(self):
        return self.gauge1RadButBox.GetValue()


    def SetGauge1RadButBox(self, val):
        self.gauge1RadButBox.SetValue(val)
        self.gaugeOtherTxt.Enable(False)



    #Gauge Radio Button 2
    def GetGauge2RadButBox(self):
        return self.gauge2RadButBox.GetValue()


    def SetGauge2RadButBox(self, val):
        self.gauge2RadButBox.SetValue(val)
        self.gaugeOtherTxt.Enable(True)




    #Weight Radio Button 1
    def GetWeightRadBut1(self):
        return self.weightRadBut1.GetValue()

    def SetWeightRadBut1(self, val):
        self.weightRadBut1.SetValue(val)
        self.EnableWeight(True)



    #Weight Radio Button 2
    def GetWeightRadBut2(self):
        return self.weightRadBut2.GetValue()

    def SetWeightRadBut2(self, val):
        self.weightRadBut2.SetValue(val)
        self.weightCtrl.SetValue("")
        self.weightRadButBox.SetSelection(0)
        self.EnableWeight(False)

    #PreUseCable combo box
    def GetPreUseCableCmbo(self):
        return self.preUseCableCmbo.GetValue()

    def SetPreUseCableCmbo(self, preUseCableCmbo):
        self.preUseCableCmbo.SetValue(preUseCableCmbo)

    #PreUseCable combo box from Xml
    def GetPreUseCableCmboFromXml(self):
        return self.preUseCableCmbo.GetValue()

    def SetPreUseCableCmboFromXml(self, preUseCableCmbo):
        self.preUseCableCmbo.ChangeValue(preUseCableCmbo)


    #Manufacturer combo box
    def GetManufactureCmbo(self):
        return self.manufactureCmbo.GetValue()


    def SetManufactureCmbo(self, manufactureCmbo):
        self.manufactureCmbo.SetValue(manufactureCmbo)

    #Manufacturer combo box from Xml
    def GetManufactureCmboFromXml(self):
        return self.manufactureCmbo.GetValue()

    def SetManufactureCmboFromXml(self, manufactureCmbo):
        self.manufactureCmbo.ChangeValue(manufactureCmbo)

    #Model combo box
    def GetModelCmbo(self):
        return self.modelCmbo.GetValue()
    def SetModelCmbo(self, modelCmbo):
        self.modelCmbo.SetValue(modelCmbo)

    #firmwareCmbo combo box
    def GetFirmwareCmbo(self):
        return self.firmwareCmbo.GetValue()
    def SetFirmwareCmbo(self, firmwareCmbo):
        self.firmwareCmbo.SetValue(firmwareCmbo)


    #ControlCondition Ctrl
    def GetControlConditionRemarksCtrl(self):
        return self.controlConditionRemarksCtrl.GetValue()

    def SetControlConditionRemarksCtrl(self, val):
        self.controlConditionRemarksCtrl.SetValue(val)



    #allow only the Integer number type inputs
    def OnIntText(self, evt):
        ctrl = evt.GetEventObject()
        value = ctrl.GetValue().strip()

        if value == "":
            ctrl.preValue = value
            evt.Skip()
            return

        try:
            int(value)
            ctrl.preValue = value
            insertPoint = ctrl.GetInsertionPoint()
            ctrl.ChangeValue(value)
            ctrl.SetInsertionPoint(insertPoint)
        except:
            insertPoint = ctrl.GetInsertionPoint() - 1
            ctrl.SetValue(ctrl.preValue)
            ctrl.SetInsertionPoint(insertPoint)
        evt.Skip()


    def OnWeightRadButBox(self, event):
        self.weightCtrl.Unbind(wx.EVT_KILL_FOCUS)
        if self.weightRadButBox.GetSelection() == 0:
            self.weightCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)

        else:
            self.weightCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        event.Skip()

    def EnableMidsectionInfoGroup2(self, en):
        self.numOfPanelsTxt.Enable(en)
        self.numOfPanelsScroll.Enable(en)
        self.flowAngleTxt.Enable(en)
        self.flowAngleCmbo.Enable(en)
        self.coEffTxt.Enable(en)
        self.coEffCtrl.Enable(en)
        self.methodTxt.Enable(en)
        self.methodCmbo.Enable(en)
        self.locatedTxt.Enable(en)
        self.metresCtrl.Enable(en)
        self.metresAboveTxt.Enable(en)
        self.weightCtrl.Enable(en)
        self.weightRadButBox.Enable(en)
        self.weightTxt.Enable(en)
        self.weightRadBut2.Enable(en)
        self.weightRadBut1.Enable(en)

    # def DefaultPanels(self, event):
    #     self.numOfPanelsScroll.SetCurrentSelection("20")
    #     print "set default selection"
    #     event.Skip()


    # #Return TURE if discharge remarks is empty
    # def dischargeRemarkEmpty(self):
    #     if self.GetDischRemarksCtrl() == '':
    #         return True
    #     else:
    #         return False


    def OnChangeResetBGColour(self, evt):
        ctrl = evt.GetEventObject()
        ctrl.SetBackgroundColour("white")
        ctrl.Refresh()
        evt.Skip()

    # def OnDiagTestCB(self, evt):
    #     ctrl = evt.GetEventObject()



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(790, 600))
    InstrumentDeploymentInfoPanel("DEBUG", frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
