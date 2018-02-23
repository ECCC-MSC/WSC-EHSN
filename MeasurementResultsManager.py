from MeasurementResultsPanel import *


class MeasurementResultsManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager

        #Display id : parameter id
        self.sensorRef = {'Atmos Pres (kPa)':'PA',
                          'Battery Voltage Under Load (V)':'YBL',
                          u'Internal Temp (\N{DEGREE SIGN}C)':'InternalTemp',
                          # 'Lake Area (km^2)':'LA',
                          # 'Lake Stage (m)':'HL',
                          'Open Water Extent (km)':'IO',
                          'Precip (mm)':'PN',
                          # 'R Ice Cover (%)':'IC',
                          # 'R Ice Cover Extent (km)':'IE',
                          'Reflective Power (W)':'YR',
                          # 'Salinity (ppt)':'WS',
                          'Sediment Load (kg)':'SL',
                          'Sediment Transport Rate (kg/s)':'STR',
                          'Signal Strength(dBm)':'YSS',
                          'Snow Cover (%)':'SA',
                          'Snow Depth (cm)':'SD',
                          'Solar Panel Voltage (V)':'SolarPanelVoltage',
                          # 'Sound Vel In Water (m/s)':'SoundVel',
                          'Tank Pressure(psi)':'YP',
                          'Wind Dir (deg)':'UD',
                          'Water Temp (' + u'\u00B0' + 'C)': 'TW',
                          u'Air Temp (\u00B0C)': 'TA',
                          'Accumulated Precip (mm)': 'PC',
                          'Snow Water Equivalent (cm)': 'SW',
                          'Forward Power (W)': 'YF',
                          'Voltage (V)':'VB',
                          'Radiation (W/m^2)': 'RN',
                          'Head Stage (m)': 'HD',
                          'Precip Inc (mm)': 'PP'
                          }

        sensorRefList = sorted(self.sensorRef.keys())
        self.gui.sensorRef = sensorRefList
        
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry1, self.gui.sensorRefEntry1Popup, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry2, self.gui.sensorRefEntry2Popup, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry3, self.gui.sensorRefEntry3Popup, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry4, self.gui.sensorRefEntry4Popup, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry5, self.gui.sensorRefEntry5Popup, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry6, self.gui.sensorRefEntry6Popup, sensorRefList)

        self.SetSensorRefCmbo(self.gui.sensorRefEntry1, sensorRefList)
        self.SetSensorRefCmbo(self.gui.sensorRefEntry2, sensorRefList)
        self.SetSensorRefCmbo(self.gui.sensorRefEntry3, sensorRefList)
        self.SetSensorRefCmbo(self.gui.sensorRefEntry4, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry5, sensorRefList)
        # self.SetSensorRefCmbo(self.gui.sensorRefEntry6, sensorRefList)

        self.sensorRefEntries = [self.gui.sensorRefEntry1,
                                 self.gui.sensorRefEntry2,
                                 self.gui.sensorRefEntry3,
                                 self.gui.sensorRefEntry4]
                                 # self.gui.sensorRefEntry5,
                                 # self.gui.sensorRefEntry6]

        self.sensorVals = [self.gui.sensorVal1,
                           self.gui.sensorVal2,
                           self.gui.sensorVal3,
                           self.gui.sensorVal4]
                           # self.gui.sensorVal5,
                           # self.gui.sensorVal6]
        
        self.observedVals = [self.gui.observedVal1,
                             self.gui.observedVal2,
                             self.gui.observedVal3,
                             self.gui.observedVal4]
                             # self.gui.observedVal5,
                             # self.gui.observedVal6]
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "MeasurementResultsControl"


    # #Time stuff
    # @property
    # def timeCtrl(self):
    #     return self.gui.GetTimeCtrl()

    # @timeCtrl.setter
    # def timeCtrl(self, timeCtrl):
    #     self.gui.SetTimeCtrl(timeCtrl)

    def SetSensorRefCmbo(self, sensorRefEntry, lis):
        # sensorRefPopup.ClearAll()
        # sensorRefPopup.AddItems(lis)
        sensorRefEntry.Clear()
        try:
            sensorRefEntry.GetPopupControl().AppendItems(lis)
        except:
            sensorRefEntry.AppendItems(lis)
        

    #Sensor Vals
    @property
    def sensorRefEntry1(self):
        return self.gui.GetSensorRefEntry1()

    @sensorRefEntry1.setter
    def sensorRefEntry1(self, sensorRefEntry1):
        self.gui.SetSensorRefEntry1(sensorRefEntry1)
        
    @property
    def sensorRefEntry2(self):
        return self.gui.GetSensorRefEntry2()

    @sensorRefEntry2.setter
    def sensorRefEntry2(self, sensorRefEntry2):
        self.gui.SetSensorRefEntry2(sensorRefEntry2)
        
    @property
    def sensorRefEntry3(self):
        return self.gui.GetSensorRefEntry3()

    @sensorRefEntry3.setter
    def sensorRefEntry3(self, sensorRefEntry3):
        self.gui.SetSensorRefEntry3(sensorRefEntry3)
        
    @property
    def sensorRefEntry4(self):
        return self.gui.GetSensorRefEntry4()

    @sensorRefEntry4.setter
    def sensorRefEntry4(self, sensorRefEntry4):
        self.gui.SetSensorRefEntry4(sensorRefEntry4)
        
    # @property
    # def sensorRefEntry5(self):
    #     return self.gui.GetSensorRefEntry5()

    # @sensorRefEntry5.setter
    # def sensorRefEntry5(self, sensorRefEntry5):
    #     self.gui.SetSensorRefEntry5(sensorRefEntry5)
        
    # @property
    # def sensorRefEntry6(self):
    #     return self.gui.GetSensorRefEntry6()

    # @sensorRefEntry6.setter
    # def sensorRefEntry6(self, sensorRefEntry6):
    #     self.gui.SetSensorRefEntry6(sensorRefEntry6)


    #Observed Val
    @property
    def observedVal1(self):
        return self.gui.GetObservedVal1()

    @observedVal1.setter
    def observedVal1(self, observedVal1):
        self.gui.SetObservedVal1(observedVal1)
        
    @property
    def observedVal2(self):
        return self.gui.GetObservedVal2()

    @observedVal2.setter
    def observedVal2(self, observedVal2):
        self.gui.SetObservedVal2(observedVal2)
        
    @property
    def observedVal3(self):
        return self.gui.GetObservedVal3()

    @observedVal3.setter
    def observedVal3(self, observedVal3):
        self.gui.SetObservedVal3(observedVal3)
        
    @property
    def observedVal4(self):
        return self.gui.GetObservedVal4()

    @observedVal4.setter
    def observedVal4(self, observedVal4):
        self.gui.SetObservedVal4(observedVal4)
        
    # @property
    # def observedVal5(self):
    #     return self.gui.GetObservedVal5()

    # @observedVal5.setter
    # def observedVal5(self, observedVal5):
    #     self.gui.SetObservedVal5(observedVal5)
        
    # @property
    # def observedVal6(self):
    #     return self.gui.GetObservedVal6()

    # @observedVal6.setter
    # def observedVal6(self, observedVal6):
    #     self.gui.SetObservedVal6(observedVal6)


    #Sensor Val
    @property
    def sensorVal1(self):
        return self.gui.GetSensorVal1()

    @sensorVal1.setter
    def sensorVal1(self, sensorVal1):
        self.gui.SetSensorVal1(sensorVal1)
        
    @property
    def sensorVal2(self):
        return self.gui.GetSensorVal2()

    @sensorVal2.setter
    def sensorVal2(self, sensorVal2):
        self.gui.SetSensorVal2(sensorVal2)
        
    @property
    def sensorVal3(self):
        return self.gui.GetSensorVal3()

    @sensorVal3.setter
    def sensorVal3(self, sensorVal3):
        self.gui.SetSensorVal3(sensorVal3)
        
    @property
    def sensorVal4(self):
        return self.gui.GetSensorVal4()

    @sensorVal4.setter
    def sensorVal4(self, sensorVal4):
        self.gui.SetSensorVal4(sensorVal4)
        
    # @property
    # def sensorVal5(self):
    #     return self.gui.GetSensorVal5()

    # @sensorVal5.setter
    # def sensorVal5(self, sensorVal5):
    #     self.gui.SetSensorVal5(sensorVal5)
        
    # @property
    # def sensorVal6(self):
    #     return self.gui.GetSensorVal6()

    # @sensorVal6.setter
    # def sensorVal6(self, sensorVal6):
    #     self.gui.SetSensorVal6(sensorVal6)

    @property
    def hour1(self):
        return self.gui.GetHour1()
    @hour1.setter
    def hour1(self, val):
        self.gui.SetHour1(val)

    @property
    def hour2(self):
        return self.gui.GetHour2()
    @hour2.setter
    def hour2(self, val):
        self.gui.SetHour2(val)

    @property
    def hour3(self):
        return self.gui.GetHour3()
    @hour3.setter
    def hour3(self, val):
        self.gui.SetHour3(val)

    @property
    def hour4(self):
        return self.gui.GetHour4()
    @hour4.setter
    def hour4(self, val):
        self.gui.SetHour4(val)

    # @property
    # def hour5(self):
    #     return self.gui.GetHour5()
    # @hour5.setter
    # def hour5(self, val):
    #     self.gui.SetHour5(val)

    @property
    def hour7(self):
        return self.gui.GetHour7()
    @hour7.setter
    def hour7(self, val):
        self.gui.SetHour7(val)

    @property
    def hour8(self):
        return self.gui.GetHour8()
    @hour8.setter
    def hour8(self, val):
        self.gui.SetHour8(val)

    @property
    def hour9(self):
        return self.gui.GetHour9()
    @hour9.setter
    def hour9(self, val):
        self.gui.SetHour9(val)

    @property
    def hour10(self):
        return self.gui.GetHour10()
    @hour10.setter
    def hour10(self, val):
        self.gui.SetHour10(val)

    @property
    def minute1(self):
        return self.gui.GetMinute1()
    @minute1.setter
    def minute1(self, val):
        self.gui.SetMinute1(val)

    @property
    def minute2(self):
        return self.gui.GetMinute2()
    @minute2.setter
    def minute2(self, val):
        self.gui.SetMinute2(val)

    @property
    def minute3(self):
        return self.gui.GetMinute3()
    @minute3.setter
    def minute3(self, val):
        self.gui.SetMinute3(val)

    @property
    def minute4(self):
        return self.gui.GetMinute4()
    @minute4.setter
    def minute4(self, val):
        self.gui.SetMinute4(val)

    # @property
    # def minute5(self):
    #     return self.gui.GetMinute5()
    # @minute5.setter
    # def minute5(self, val):
    #     self.gui.SetMinute5(val)

    @property
    def minute7(self):
        return self.gui.GetMinute7()
    @minute7.setter
    def minute7(self, val):
        self.gui.SetMinute7(val)

    @property
    def minute8(self):
        return self.gui.GetMinute8()
    @minute8.setter
    def minute8(self, val):
        self.gui.SetMinute8(val)

    @property
    def minute9(self):
        return self.gui.GetMinute9()
    @minute9.setter
    def minute9(self, val):
        self.gui.SetMinute9(val)

    @property
    def minute10(self):
        return self.gui.GetMinute10()
    @minute10.setter
    def minute10(self, val):
        self.gui.SetMinute10(val)

    @property
    def loggerTimeCol1(self):
        return self.gui.col1Combo.GetValue()
    @loggerTimeCol1.setter
    def loggerTimeCol1(self, val):
        self.gui.col1Combo.SetValue(val)

    @property
    def loggerTimeCol2(self):
        return self.gui.col2Combo.GetValue()
    @loggerTimeCol2.setter
    def loggerTimeCol2(self, val):
        self.gui.col2Combo.SetValue(val)

    @property
    def loggerTimeRemark1(self):
        return self.gui.reset1Combo.GetValue()
    @loggerTimeRemark1.setter
    def loggerTimeRemark1(self, val):
        self.gui.reset1Combo.SetValue(val)

    @property
    def loggerTimeRemark2(self):
        return self.gui.reset2Combo.GetValue()
    @loggerTimeRemark2.setter
    def loggerTimeRemark2(self, val):
        self.gui.reset2Combo.SetValue(val)


    def GetTime(self, index):
        if index == 0:
            if self.hour1 != "" and self.minute1 != "":
                return self.hour1 + ":" + self.minute1
            else:
                return ""
        elif index == 1:
            if self.hour2 != "" and self.minute2 != "":
                return self.hour2 + ":" + self.minute2
            else:
                return ""
        elif index == 2:
            if self.hour3 != "" and self.minute3 != "":
                return self.hour3 + ":" + self.minute3
            else:
                return ""
        elif index == 3:
            if self.hour4 != "" and self.minute4 != "":
                return self.hour4 + ":" + self.minute4
            else:
                return ""
        # elif index == 4:
        #     if self.hour5 != "" and self.minute5 != "":
        #         return self.hour5 + ":" + self.minute5
        #     else:
        #         return ""

        #Logger Time
        elif index == 5:
            if self.hour7 != "" and self.minute7 != "":
                return self.hour7 + ":" + self.minute7
            else:
                return ""
        elif index == 6:
            if self.hour8 != "" and self.minute8 != "":
                return self.hour8 + ":" + self.minute8
            else:
                return ""
        elif index == 7:
            if self.hour9 != "" and self.minute9 != "":
                return self.hour9 + ":" + self.minute9
            else:
                return ""
        elif index == 8:
            if self.hour10 != "" and self.minute10 != "":
                return self.hour10 + ":" + self.minute10
            else:
                return ""



    def PrintAllMeasurements(self):
        print "Time: %s" % self.timeCtrl
        
        print "Sensor Ref Entry 1: %s" % self.sensorRefEntry1
        print "Sensor Ref Entry 2: %s" % self.sensorRefEntry2
        print "Sensor Ref Entry 3: %s" % self.sensorRefEntry3
        print "Sensor Ref Entry 4: %s" % self.sensorRefEntry4
        # print "Sensor Ref Entry 5: %s" % self.sensorRefEntry5
        # print "Sensor Ref Entry 6: %s" % self.sensorRefEntry6

        print "Observed Value 1: %s" % self.observedVal1
        print "Observed Value 2: %s" % self.observedVal2
        print "Observed Value 3: %s" % self.observedVal3
        print "Observed Value 4: %s" % self.observedVal4
        # print "Observed Value 5: %s" % self.observedVal5
        # print "Observed Value 6: %s" % self.observedVal6

        print "Sensor Value 1: %s" % self.sensorVal1
        print "Sensor Value 2: %s" % self.sensorVal2
        print "Sensor Value 3: %s" % self.sensorVal3
        print "Sensor Value 4: %s" % self.sensorVal4
        # print "Sensor Value 5: %s" % self.sensorVal5
        # print "Sensor Value 6: %s" % self.sensorVal6

    def IsEmpty(self):
        for index, item in enumerate(self.gui.GetSizer().GetChildren()):
            if index != 0 and index != 1 and index != 8 and index != 9 and index != 16 and index != 17:
                if item.GetWindow().GetValue() != '':
                    return False
        else:
            return True

    def GetTimeCtrlPanel1(self):
        return self.gui.timeCtrlPanel1
    def GetTimeCtrlPanel2(self):
        return self.gui.timeCtrlPanel2
    def GetTimeCtrlPanel3(self):
        return self.gui.timeCtrlPanel3
    def GetTimeCtrlPanel4(self):
        return self.gui.timeCtrlPanel4

    def GetSensorRefEntry1(self):
        return self.gui.sensorRefEntry1
    def GetObservedVal1(self):
        return self.gui.observedVal1
    def GetSensorVal1(self):
        return self.gui.sensorVal1

    def GetSensorRefEntry2(self):
        return self.gui.sensorRefEntry2
    def GetObservedVal2(self):
        return self.gui.observedVal2
    def GetSensorVal2(self):
        return self.gui.sensorVal2

    def GetSensorRefEntry3(self):
        return self.gui.sensorRefEntry3
    def GetObservedVal3(self):
        return self.gui.observedVal3
    def GetSensorVal3(self):
        return self.gui.sensorVal3

    def GetSensorRefEntry4(self):
        return self.gui.sensorRefEntry4
    def GetObservedVal4(self):
        return self.gui.observedVal4
    def GetSensorVal4(self):
        return self.gui.sensorVal4

    def GetCol1Combo(self):
        return self.gui.col1Combo

    def GetCol2Combo(self):
        return self.gui.col2Combo

    def GetReset1Combo(self):
        return self.gui.reset1Combo

    def GetReset2Combo(self):
        return self.gui.reset2Combo

    def GetTimeCtrlPanel7(self):
        return self.gui.timeCtrlPanel7

    def GetTimeCtrlPanel8(self):
        return self.gui.timeCtrlPanel8

    def GetTimeCtrlPanel9(self):
        return self.gui.timeCtrlPanel9

    def GetTimeCtrlPanel10(self):
        return self.gui.timeCtrlPanel10






def main():
    app = wx.App()

    frame = wx.Frame(None, size=(500, 200))
    MeasurementResultsManager("DEBUG", MeasurementResultsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame))

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()

