# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import wx.lib.masked as masked
import wx.adv as adv
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



class EnvironmentConditionsPanel(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(EnvironmentConditionsPanel, self).__init__(*args, **kwargs)

        self.levelsTxtLbl = "Levels"
        self.cloudCoverTxtLbl = "Cloud Cover"
        self.cloudCoverList = ["", "Clear", "Partly Cloudy", "Mostly Cloudy", "Cloudy", "Smokey"]
        self.precipTxtLbl = "Precipitation"
        self.precipList = ["", "No Precipitation", "Light Rain", "Moderate Rain", "Heavy Rain",
                           "Mist", "Light Snow", "Moderate Snow", "Heavy Snow", "Flurries",
                           "Sleet", "Freezing Rain", "Hail"]
        self.windMagTxtLbl = "Wind Conditions"
        self.windMagList = ["", "Calm Wind", "Very Light Wind", "Light Wind",
                            "Moderate Wind", "Heavy Wind", "Very Heavy Wind"]
        self.windMagSpeedTxtLbl = "Wind Speed (km/h)"
        self.windDirTxtLbl = "Wind Direction"
        self.windDirList = ["", "Blowing Upstream", "Blowing Downstream",
                            "Blowing Cross Stream", "Swirling/Variable"]
        self.batteryVoltageTxtLbl = "Battery Voltage (VB)"
        self.gasSystemTxtLbl = "Gas System:\nCyl."
        self.feedTxtLbl = "Feed"
        self.bpmrotTxtLbl = ["", "BPM", "Rot"]
        self.intakeTxtLbl = "Intake Flushed"
        self.orificeTxtLbl = "Orifice Purged"
        self.programTxtLbl = "Downloaded\nProgram"
        self.dataTxtLbl = "Downloaded\nData"
        self.dataPeriodTxtLbl = "Data Period"
        self.dataPeriodFromTxtLbl = "From"
        self.dataPeriodToTxtLbl = "To"
        self.intakeTimeLbl = "@"

        self.arrivalLbl = "Arrival(Found)"
        self.departLbl = "Departure(Left)"
        self.bmpList = ["BMP/POT"]

        self.stnRemarkLbl = "Station Health\nRemarks"


        self.SetSize((325, -1))
        self.mode=mode
        self.manager = None

        self.lang = wx.LANGUAGE_ENGLISH
        self.InitUI()
#disable the mouse scrolling
    def do_nothing(self,evt):
        pass
#enable or disable the data period
    def OnDownloadedData(self, e):
        pick = self.dataCB.GetValue()
        self.dataPeriodFromPicker.Enable(pick)
        self.dataPeriodToPicker.Enable(pick)
        
    def InitUI(self):
        if self.mode=="DEBUG":
            print "In EnvironmentConditionsPanel"

        self.locale = wx.Locale(self.lang)

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)

        #Levels Txt and Ctrl
        levelsSizer = wx.BoxSizer(wx.HORIZONTAL)
        levelsTxt = wx.StaticText(self, label=self.levelsTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.levelsCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(100, -1))
        levelsSizer.Add(levelsTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        levelsSizer.Add(self.levelsCtrl, 1, wx.EXPAND|wx.LEFT, 5)
        

        #Cloud Cover Text and Combo
        cloudCoverSizer = wx.BoxSizer(wx.HORIZONTAL)
        cloudCoverTxt = wx.StaticText(self, label=self.cloudCoverTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.cloudCoverCmbo = wx.ComboBox(self, choices=self.cloudCoverList, style=wx.CB_READONLY, size=(100, -1))
        self.cloudCoverCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        cloudCoverSizer.Add(cloudCoverTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        cloudCoverSizer.Add(self.cloudCoverCmbo, 1, wx.EXPAND|wx.LEFT, 5)

        #Precipitation Text and Combo
        precipSizer = wx.BoxSizer(wx.HORIZONTAL)
        precipTxt = wx.StaticText(self, label=self.precipTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.precipCmbo = wx.ComboBox(self, choices=self.precipList, style=wx.CB_READONLY, size=(100, -1))
        self.precipCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        precipSizer.Add(precipTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        precipSizer.Add(self.precipCmbo, 1, wx.EXPAND|wx.LEFT, 5)


        #Wind Magnitude Text, Combo
        windMagSizer = wx.BoxSizer(wx.HORIZONTAL)
        windMagTxt = wx.StaticText(self, label=self.windMagTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.windMagCmbo = wx.ComboBox(self, choices=self.windMagList, style=wx.CB_READONLY, size=(100, -1))
        self.windMagCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        windMagSizer.Add(windMagTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        windMagSizer.Add(self.windMagCmbo, 1, wx.EXPAND|wx.LEFT, 5)
        
        #Wind Mag Speed Text and Ctrl
        windMagSpeedSizer = wx.BoxSizer(wx.HORIZONTAL)
        windMagSpeedTxt = wx.StaticText(self, label=self.windMagSpeedTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.windMagCtrl = MyTextCtrl(self, size=(80, -1))
        self.windMagCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.windMagCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        windMagSpeedSizer.Add(windMagSpeedTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        windMagSpeedSizer.Add(self.windMagCtrl, 1, wx.EXPAND|wx.LEFT, 5)
        


        #Wind Direction Text and Cmbo
        windDirSizer = wx.BoxSizer(wx.HORIZONTAL)
        windDirTxt = wx.StaticText(self, label=self.windDirTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.windDirCmbo = wx.ComboBox(self, choices=self.windDirList ,style=wx.CB_READONLY, size=(100, -1))
        self.windDirCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)
        windDirSizer.Add(windDirTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        windDirSizer.Add(self.windDirCmbo, 1, wx.EXPAND|wx.LEFT, 5)

        #Battery Voltage Text and Ctrl
        batterySizer = wx.BoxSizer(wx.HORIZONTAL)
        batteryTxt = wx.StaticText(self, label=self.batteryVoltageTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.batteryCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(100, -1))
        self.batteryCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.batteryCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round1)
        batterySizer.Add(batteryTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        batterySizer.Add(self.batteryCtrl, 1, wx.EXPAND|wx.LEFT, 5)



        #Gas Pressure Sizer
        gasPressureSizer = wx.BoxSizer(wx.HORIZONTAL)
        gasPressureV1 = wx.BoxSizer(wx.VERTICAL)
        gasPressureV2 = wx.BoxSizer(wx.VERTICAL)
        gasPressureV3 = wx.BoxSizer(wx.VERTICAL)


        gasPressV1H1 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV1H2 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV1H3 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV1H4 = wx.BoxSizer(wx.HORIZONTAL)

        gasPressV2H1 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV2H2 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV2H3 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV2H4 = wx.BoxSizer(wx.HORIZONTAL)

        gasPressV3H1 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV3H2 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV3H3 = wx.BoxSizer(wx.HORIZONTAL)
        gasPressV3H4 = wx.BoxSizer(wx.HORIZONTAL)

        gasPressureV1.Add(gasPressV1H1, 0, wx.EXPAND)
        gasPressureV1.Add(gasPressV1H2, 0, wx.EXPAND)
        gasPressureV1.Add(gasPressV1H3, 0, wx.EXPAND|wx.TOP, 5)
        gasPressureV1.Add(gasPressV1H4, 0, wx.EXPAND|wx.TOP, 5)

        gasPressureV2.Add(gasPressV2H1, 0, wx.EXPAND)
        gasPressureV2.Add(gasPressV2H2, 0, wx.EXPAND)
        gasPressureV2.Add(gasPressV2H3, 0, wx.EXPAND|wx.TOP, 5)
        gasPressureV2.Add(gasPressV2H4, 0, wx.EXPAND|wx.TOP, 5)

        gasPressureV3.Add(gasPressV3H1, 0, wx.EXPAND)
        gasPressureV3.Add(gasPressV3H2, 0, wx.EXPAND)
        gasPressureV3.Add(gasPressV3H3, 0, wx.EXPAND|wx.TOP, 5)
        gasPressureV3.Add(gasPressV3H4, 0, wx.EXPAND|wx.TOP, 5)


        gasPressureSizer.Add(gasPressureV1, 0, wx.EXPAND)
        gasPressureSizer.Add(gasPressureV2, 1, wx.EXPAND)
        gasPressureSizer.Add(gasPressureV3, 1, wx.EXPAND)


        arrivalTxt = wx.StaticText(self, label=self.arrivalLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        departureTxt = wx.StaticText(self, label=self.departLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        font = wx.Font(wx.FontInfo(8).FaceName("Helvetica").Bold())
        arrivalTxt.SetFont(font)
        departureTxt.SetFont(font)

        arrivalTxt.SetForegroundColour((164,64,43))
        departureTxt.SetForegroundColour((164,64,43))

        gasPressV1H1.Add((-255,-255), 1, wx.EXPAND)
        gasPressV2H1.Add(arrivalTxt, 1, wx.EXPAND)
        gasPressV3H1.Add(departureTxt, 1, wx.EXPAND)







        ###########################################




        #Gas Text and Ctrl
       
        gasSysTxt = wx.StaticText(self, label=self.gasSystemTxtLbl)#, style=wx.ALIGN_CENTRE_HORIZONTAL)

        gasSysAtTxt = wx.StaticText(self, label=self.intakeTimeLbl)
        gasSysAt2Txt = wx.StaticText(self, label=self.intakeTimeLbl)
        font2 = wx.Font(wx.FontInfo(7))
        gasSysTxt.SetFont(font2)

        #v1h1
        self.gasSysCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(40, -1))
        self.gasSysCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.gasSysCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        self.gasArrTime = DropdownTime(False, parent=self, size=(-1, -1))


        
        #v2h1
        self.bpmrotCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(40, -1))
        self.bpmrotCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.bpmrotCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig2)
        self.bpmrotArrTime = DropdownTime(False, parent=self, size=(-1, -1))


        #v1h3
        feedTxt = wx.StaticText(self, label=self.feedTxtLbl)#, style=wx.ALIGN_CENTRE_HORIZONTAL)
        feedAtTxt = wx.StaticText(self, label=self.intakeTimeLbl)
        feedAt2Txt = wx.StaticText(self, label=self.intakeTimeLbl)
        self.feedCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(40, -1))
        self.feedCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.feedCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig2)
        self.feedArrTime = DropdownTime(False, parent=self, size=(-1, -1))




        #v1h2
        self.gasSysDepCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(40, -1))
        self.gasSysDepCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.gasSysDepCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)

        
        self.gasDepTime = DropdownTime(False, parent=self, size=(-1, -1))

        #v2h2
        self.bpmrotDepCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(40, -1))
        self.bpmrotDepCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.bpmrotDepCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig2)

        
        self.bpmrotDepTime = DropdownTime(False, parent=self, size=(-1, -1))


        #v3h2
        self.feedDepCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(40, -1))
        self.feedDepCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.feedDepCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig2)

        
        self.feedDepTime = DropdownTime(False, parent=self, size=(-1, -1))



        #v0h0
        self.bpmrotCmbo = wx.ComboBox(self, choices=self.bpmrotTxtLbl, style=wx.CB_READONLY, size=(50, -1))
        self.bpmrotCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)


        gasPressV1H2.Add(gasSysTxt, 0, wx.EXPAND|wx.TOP, 20)
        gasPressV2H2.Add(self.gasSysCtrl, 0, wx.EXPAND|wx.LEFT, 5)
        gasPressV2H2.Add(gasSysAtTxt, 0, wx.LEFT, 5)
        gasPressV2H2.Add(self.gasArrTime, 0)

        gasPressV3H2.Add(self.gasSysDepCtrl, 0, wx.EXPAND|wx.LEFT, 5)
        gasPressV3H2.Add(gasSysAt2Txt, 0, wx.LEFT, 5)
        gasPressV3H2.Add(self.gasDepTime, 0)



        #BPM/ROT Cmbo and Ctrl
        
        
        bpmrotAtTxt = wx.StaticText(self, label=self.intakeTimeLbl)
        bpmrotAt2Txt = wx.StaticText(self, label=self.intakeTimeLbl)

        
        

        

        gasPressV1H3.Add(self.bpmrotCmbo, 0, wx.EXPAND|wx.TOP, 10)
        gasPressV2H3.Add(self.bpmrotCtrl, 0, wx.EXPAND|wx.LEFT, 5)
        gasPressV2H3.Add(bpmrotAtTxt, 0, wx.LEFT, 5)
        gasPressV2H3.Add(self.bpmrotArrTime, 0)

        gasPressV3H3.Add(self.bpmrotDepCtrl, 0, wx.EXPAND|wx.LEFT, 5)
        gasPressV3H3.Add(bpmrotAt2Txt, 0, wx.LEFT, 5)
        gasPressV3H3.Add(self.bpmrotDepTime, 0)





        #Feed Ctrl
        
        

        

        gasPressV1H4.Add(feedTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)
        gasPressV2H4.Add(self.feedCtrl, 0, wx.EXPAND|wx.LEFT, 5)
        gasPressV2H4.Add(feedAtTxt, 0, wx.LEFT, 5)
        gasPressV2H4.Add(self.feedArrTime, 0)

        gasPressV3H4.Add(self.feedDepCtrl, 0, wx.EXPAND|wx.LEFT, 5)
        gasPressV3H4.Add(feedAt2Txt, 0, wx.LEFT, 5)
        gasPressV3H4.Add(self.feedDepTime, 0)






        #Intake/Orifice checkboxes
        intakeOrificeSizerH = wx.BoxSizer(wx.HORIZONTAL)
        
        intakeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.intakeCB = wx.CheckBox(self, label=self.intakeTxtLbl)
        self.intakeCB.Bind(wx.EVT_CHECKBOX, self.OnIntakeCheck)
        intakeSizer.Add(self.intakeCB, 1, wx.EXPAND)

        intakeTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.intakeTimeTxt = wx.StaticText(self, label=self.intakeTimeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, 10))
        self.intakeTimeTxt.Hide()
        self.intakeTimeCtrl = masked.TimeCtrl(self, 2, size=(-1, 10), displaySeconds=False, style=wx.TE_CENTRE, fmt24hr=True)
        self.intakeTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        self.intakeTimeCtrl.Hide()
        intakeTimeSizer.Add(self.intakeTimeTxt, 0, wx.EXPAND)
        intakeTimeSizer.Add(self.intakeTimeCtrl, 1, wx.EXPAND)


        orificeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.orificeCB = wx.CheckBox(self, label=self.orificeTxtLbl)
        self.orificeCB.Bind(wx.EVT_CHECKBOX, self.OnOrificeCheck)
        orificeSizer.Add(self.orificeCB, 1, wx.EXPAND)



        orificeTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.orificeTimeTxt = wx.StaticText(self, label=self.intakeTimeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(-1, 10))
        self.orificeTimeTxt.Hide()
        self.orificeTimeCtrl = masked.TimeCtrl(self, 2, size=(-1, 10), displaySeconds=False, style=wx.TE_CENTRE, fmt24hr=True)
        self.orificeTimeCtrl.Bind(wx.EVT_KEY_DOWN, self.OnResetTime)
        self.orificeTimeCtrl.Hide()
        orificeTimeSizer.Add(self.orificeTimeTxt, 0, wx.EXPAND)
        orificeTimeSizer.Add(self.orificeTimeCtrl, 1, wx.EXPAND)

        intakeOrificeSizerH.Add(intakeSizer, 1, wx.EXPAND)
        intakeOrificeSizerH.Add(orificeSizer, 1, wx.EXPAND)

        self.intakeOrificeTimeSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.intakeOrificeTimeSizerH.Add(intakeTimeSizer, 1, wx.EXPAND)
        self.intakeOrificeTimeSizerH.Add(orificeTimeSizer, 1, wx.EXPAND)


        #Program/Data checkboxes
        programDataSizerH = wx.BoxSizer(wx.HORIZONTAL)

        programSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.programCB = wx.CheckBox(self, label=self.programTxtLbl, size=(85, -1))
        programSizer.Add(self.programCB, 1, wx.EXPAND)

        dataSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dataCB = wx.CheckBox(self, label=self.dataTxtLbl, size=(-1, -1))
        self.dataCB.Bind(wx.EVT_CHECKBOX, self.OnDownloadedData)
        dataSizer.Add(self.dataCB, 1, wx.EXPAND)

        programDataSizerH.Add(programSizer, 1, wx.EXPAND)
        programDataSizerH.Add(dataSizer, 1, wx.EXPAND)

        #Data period From/To
        dataPeriodSizer = wx.BoxSizer(wx.VERTICAL)
        dataPeriodTxt = wx.StaticText(self, label=self.dataPeriodTxtLbl)

        dataPeriodRangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        dataPeriodFromTxt = wx.StaticText(self, label=self.dataPeriodFromTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.dataPeriodFromPicker = adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN, size=(30, -1))
        self.dataPeriodFromPicker.Enable(False)
        dataPeriodToTxt = wx.StaticText(self, label=self.dataPeriodToTxtLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.dataPeriodToPicker = adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN, size=(30, -1))
        self.dataPeriodToPicker.Enable(False)

        dataPeriodRangeSizer.Add(dataPeriodFromTxt, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        dataPeriodRangeSizer.Add(self.dataPeriodFromPicker, 1, wx.EXPAND)
        dataPeriodRangeSizer.Add(dataPeriodToTxt, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        dataPeriodRangeSizer.Add(self.dataPeriodToPicker, 1, wx.EXPAND)

        dataPeriodSizer.Add(dataPeriodTxt, 0, wx.EXPAND)
        dataPeriodSizer.Add(dataPeriodRangeSizer, 1, wx.EXPAND)

        #Station Health Remark
        stationHealthRemarkPanel = wx.Panel(self, style=wx.NO_BORDER)
        stationRemarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        stationHealthRemarkPanel.SetSizer(stationRemarkSizer)
        stationHealthTxt = wx.StaticText(stationHealthRemarkPanel, label=self.stnRemarkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.stationHealthRemarksCtrl = wx.TextCtrl(stationHealthRemarkPanel, style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_BESTWRAP, size=(-1, -1))
        stationRemarkSizer.Add(stationHealthTxt, 0)
        stationRemarkSizer.Add(self.stationHealthRemarksCtrl, 1, wx.EXPAND)

        

        #Add all to layout Sizer
        self.layoutSizer.Add(levelsSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(cloudCoverSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(precipSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(windMagSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(windMagSpeedSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(windDirSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(batterySizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)

        self.layoutSizer.Add(gasPressureSizer, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)

        # self.layoutSizer.Add(gasSysSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        # self.layoutSizer.Add(machineSizerH, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(intakeOrificeSizerH, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add(self.intakeOrificeTimeSizerH, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        
        self.layoutSizer.Add(programDataSizerH, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        self.layoutSizer.Add((1, 10))
        self.layoutSizer.Add(dataPeriodSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)


        self.layoutSizer.Add(stationHealthRemarkPanel, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        
        
        self.SetSizer(self.layoutSizer)

    def OnIntakeCheck(self, event):
        if event.GetEventObject().IsChecked():
            self.intakeTimeCtrl.SetValue(wx.DateTime.Now().FormatTime())
            self.intakeTimeCtrl.Show()
            self.intakeTimeTxt.Show()
            self.layoutSizer.Layout()
            if self.manager is not None:
                self.manager.manager.GetLayout().Layout()
        else:
            self.intakeTimeCtrl.SetValue("00:00")
            self.intakeTimeCtrl.Hide()
            self.intakeTimeTxt.Hide()
            self.layoutSizer.Layout()
            if self.manager is not None:
                self.manager.manager.GetLayout().Layout()


    def OnOrificeCheck(self, event):
        if event.GetEventObject().IsChecked():
            self.orificeTimeCtrl.SetValue(wx.DateTime.Now().FormatTime())
            self.orificeTimeCtrl.Show()
            self.orificeTimeTxt.Show()
            self.layoutSizer.Layout()
            if self.manager is not None:
                self.manager.manager.GetLayout().Layout()
        else:
            self.orificeTimeCtrl.SetValue("00:00")
            self.orificeTimeCtrl.Hide()
            self.orificeTimeTxt.Hide()
            self.layoutSizer.Layout()
            if self.manager is not None:
                self.manager.manager.GetLayout().Layout()





    #Levels ctrl
    def GetLevelsCtrl(self):
        return self.levelsCtrl.GetValue()

    def SetLevelsCtrl(self, levelsCtrl):
        self.levelsCtrl.SetValue(levelsCtrl)


    #Cloud Cover Cmbo
    def GetCloudCoverCmbo(self):
        return self.cloudCoverCmbo.GetValue()

   
    def SetCloudCoverCmbo(self, cloudCoverCmbo):
        self.cloudCoverCmbo.SetValue(cloudCoverCmbo)


    #Precipitation Cmbo
    def GetPrecipCmbo(self):
        return self.precipCmbo.GetValue()

    def SetPrecipCmbo(self, precipCmbo):
        self.precipCmbo.SetValue(precipCmbo)


    #Wind Magnitude Cmbo
    def GetWindMagCmbo(self):
        return self.windMagCmbo.GetValue()


    def SetWindMagCmbo(self, windMagCmbo):
        self.windMagCmbo.SetValue(windMagCmbo)


    #Wind Magnitude Ctrl
    def GetWindMagCtrl(self):
        return self.windMagCtrl.GetValue()


    def SetWindMagCtrl(self, windMagCtrl):
        self.windMagCtrl.SetValue(windMagCtrl)


    #Wind Direction Cmbo
    def GetWindDirCmbo(self):
        return self.windDirCmbo.GetValue()


    def SetWindDirCmbo(self, windDirCmbo):
        self.windDirCmbo.SetValue(windDirCmbo)


    #Battery Ctrl
    def GetBatteryCtrl(self):
        return self.batteryCtrl.GetValue()


    def SetBatteryCtrl(self, batteryCtrl):
        self.batteryCtrl.SetValue(batteryCtrl)





    #Gas System Ctrl
    def GetGasSysCtrl(self):
        return self.gasSysCtrl.GetValue()

    def SetGasSysCtrl(self, gasSysCtrl):
        self.gasSysCtrl.SetValue(gasSysCtrl)


    #Gas Departure Ctrl
    def GetGasDepSysCtrl(self):
        return self.gasSysDepCtrl.GetValue()

    def SetGasDepSysCtrl(self, SetGasDepSysCtrl):
        self.gasSysDepCtrl.SetValue(SetGasDepSysCtrl)


    #Gas Arrival Time
    def GetGasArrTime(self):
        return self.gasArrTime.GetValue()

    def SetGasArrTime(self, gasArrTime):
        self.gasArrTime.SetValue(gasArrTime)


    #Gas Departure Time
    def GetGasDepTime(self):
        return self.gasDepTime.GetValue()

    def SetGasDepTime(self, gasDepTime):
        self.gasDepTime.SetValue(gasDepTime)


    #Feed Departure Ctrl
    def GetFeedDepCtrl(self):
        return self.feedDepCtrl.GetValue()

    def SetFeedDepCtrl(self, feedDepCtrl):
        self.feedDepCtrl.SetValue(feedDepCtrl)

    #Feed Arrival time
    def GetFeedArrTime(self):
        return self.feedArrTime.GetValue()

    def SetFeedArrTime(self, feedArrTime):
        self.feedArrTime.SetValue(feedArrTime)


    #Feed Departure time
    def GetFeedDepTime(self):
        return self.feedDepTime.GetValue()

    def SetFeedDepTime(self, feedDepTime):
        self.feedDepTime.SetValue(feedDepTime)



    def GetBpmrotDepCtrl(self):
        return self.bpmrotDepCtrl.GetValue()

    def SetBpmrotDepCtrl(self, bpmrotDepCtrl):
        self.bpmrotDepCtrl.SetValue(bpmrotDepCtrl)

    def GetBpmrotArrTime(self):
        return self.bpmrotArrTime.GetValue()

    def SetBpmrotArrTime(self, bpmrotArrTime):
        self.bpmrotArrTime.SetValue(bpmrotArrTime)

    def GetBpmrotDepTime(self):
        return self.bpmrotDepTime.GetValue()

    def SetBpmrotDepTime(self, bpmrotDepTime):
        self.bpmrotDepTime.SetValue(bpmrotDepTime)






    #Feed Ctrl
    def GetFeedCtrl(self):
        return self.feedCtrl.GetValue()
    def SetFeedCtrl(self, feedCtrl):
        self.feedCtrl.SetValue(feedCtrl)



    #BPM ROT ComboBox
    def GetBpmrotCmbo(self):
        return self.bpmrotCmbo.GetValue()

    def SetBpmrotCmbo(self, bpmrotCmbo):
        self.bpmrotCmbo.SetValue(bpmrotCmbo)



    #BPM ROT Ctrl
    def GetBpmrotCtrl(self):
        return self.bpmrotCtrl.GetValue()

    def SetBpmrotCtrl(self, bpmrotCtrl):
        self.bpmrotCtrl.SetValue(bpmrotCtrl)




    #Intake Time
    def GetIntakeTimeCtrl(self):
        return self.intakeTimeCtrl.GetValue()

   
    def SetIntakeTimeCtrl(self, intakeTimeCtrl):
        self.intakeTimeCtrl.SetValue(intakeTimeCtrl)


    #Orifice Time
    def GetOrificeTimeCtrl(self):
        return self.orificeTimeCtrl.GetValue()

    
    def SetOrificeTimeCtrl(self, orificeTimeCtrl):
        self.orificeTimeCtrl.SetValue(orificeTimeCtrl)





    #Intake CB
    def GetIntakeCB(self):
        return self.intakeCB.GetValue()
    def SetIntakeCB(self, intakeCB):
        self.intakeCB.SetValue(intakeCB)



    #Orifice CB
    def GetOrificeCB(self):
        return self.orificeCB.GetValue()
    def SetOrificeCB(self, orificeCB):
        self.orificeCB.SetValue(orificeCB)



    #Program Downloaded CB
    def GetProgramCB(self):
        return self.programCB.GetValue()
    def SetProgramCB(self, programCB):
        self.programCB.SetValue(programCB)



    #Data Downloaded CB
    def GetDataCB(self):
        return self.dataCB.GetValue()
    def SetDataCB(self, dataCB):
        self.dataCB.SetValue(dataCB)


    #Data Period From
    def GetDataPeriodFromPicker(self):
        if self.manager is not None:
            fm = "%Y/%m/%d" if self.manager.manager is None else self.manager.manager.DT_FORMAT
        else:
            fm = "%Y/%m/%d"
        return self.dataPeriodFromPicker.GetValue().Format(fm)


    def SetDataPeriodFromPicker(self, dataPeriodFromPicker):
        date = wx.DateTime()
        if self.manager is not None:
            fm = "%Y/%m/%d" if self.manager.manager is None else self.manager.manager.DT_FORMAT
        else:
            fm = "%Y/%m/%d"
        date.ParseFormat(dataPeriodFromPicker, fm)
        self.dataPeriodFromPicker.SetValue(date)


    #Data Period To
    def GetDataPeriodToPicker(self):
        if self.manager is not None:
            fm = "%Y/%m/%d" if self.manager.manager is None else self.manager.manager.DT_FORMAT
        else:
            fm = "%Y/%m/%d"
        return self.dataPeriodToPicker.GetValue().Format(fm)


    def SetDataPeriodToPicker(self, dataPeriodToPicker):
        date = wx.DateTime()
        if self.manager is not None:
            fm = "%Y/%m/%d" if self.manager.manager is None else self.manager.manager.DT_FORMAT
        else:
            fm = "%Y/%m/%d"

        date.ParseFormat(dataPeriodToPicker, fm)
        self.dataPeriodToPicker.SetValue(date)
        



    #Reset the time ctrl to "00:00" by pressing 'R'
    def OnResetTime(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('R'):
            ctrl = event.GetEventObject()
            ctrl.SetValue("00:00")
        event.Skip()










def main():
    app = wx.App()

    frame = wx.Frame(None, size=(-1, 450))
    EnvironmentConditionsPanel("DEBUG", frame)

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
