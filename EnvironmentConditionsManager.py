# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from EnvironmentConditionsPanel import *

class EnvironmentConditionsManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print("EnvironmentConditionsControl")


    #Levels ctrl
    @property
    def levelsCtrl(self):
        return self.gui.GetLevelsCtrl()

    @levelsCtrl.setter
    def levelsCtrl(self, levelsCtrl):
        self.gui.SetLevelsCtrl(levelsCtrl)


    #Cloud Cover Cmbo
    @property
    def cloudCoverCmbo(self):
        return self.gui.GetCloudCoverCmbo()

    @cloudCoverCmbo.setter
    def cloudCoverCmbo(self, cloudCoverCmbo):
        self.gui.SetCloudCoverCmbo(cloudCoverCmbo)


    #Precipitation Cmbo
    @property
    def precipCmbo(self):
        return self.gui.GetPrecipCmbo()

    @precipCmbo.setter
    def precipCmbo(self, precipCmbo):
        self.gui.SetPrecipCmbo(precipCmbo)


    #Wind Magnitude Cmbo
    @property
    def windMagCmbo(self):
        return self.gui.GetWindMagCmbo()

    @windMagCmbo.setter
    def windMagCmbo(self, windMagCmbo):
        self.gui.SetWindMagCmbo(windMagCmbo)


    #Wind Magnitude Ctrl
    @property
    def windMagCtrl(self):
        return self.gui.GetWindMagCtrl()

    @windMagCtrl.setter
    def windMagCtrl(self, windMagCtrl):
        self.gui.SetWindMagCtrl(windMagCtrl)


    #Wind Direction Cmbo
    @property
    def windDirCmbo(self):
        return self.gui.GetWindDirCmbo()

    @windDirCmbo.setter
    def windDirCmbo(self, windDirCmbo):
        self.gui.SetWindDirCmbo(windDirCmbo)


    #Battery Ctrl
    @property
    def batteryCtrl(self):
        return self.gui.GetBatteryCtrl()

    @batteryCtrl.setter
    def batteryCtrl(self, batteryCtrl):
        self.gui.SetBatteryCtrl(batteryCtrl)



    #Gas System Ctrl
    @property
    def gasSysCtrl(self):
        return self.gui.GetGasSysCtrl()

    @gasSysCtrl.setter
    def gasSysCtrl(self, gasSysCtrl):
        self.gui.SetGasSysCtrl(gasSysCtrl)



    #Feed Ctrl
    @property
    def feedCtrl(self):
        return self.gui.GetFeedCtrl()

    @feedCtrl.setter
    def feedCtrl(self, feedCtrl):
        self.gui.SetFeedCtrl(feedCtrl)



    #BPM ROT ComboBox
    @property
    def bpmrotCmbo(self):
        return self.gui.GetBpmrotCmbo()

    @bpmrotCmbo.setter
    def bpmrotCmbo(self, bpmrotCmbo):
        self.gui.SetBpmrotCmbo(bpmrotCmbo)



    #BPM ROT Ctrl
    @property
    def bpmrotCtrl(self):
        return self.gui.GetBpmrotCtrl()

    @bpmrotCtrl.setter
    def bpmrotCtrl(self, bpmrotCtrl):
        self.gui.SetBpmrotCtrl(bpmrotCtrl)




    #Intake Time
    @property
    def intakeTimeCtrl(self):
        return self.gui.GetIntakeTimeCtrl()

    @intakeTimeCtrl.setter
    def intakeTimeCtrl(self, intakeTimeCtrl):
        self.gui.SetIntakeTimeCtrl(intakeTimeCtrl)


    #Orifice Time
    @property
    def orificeTimeCtrl(self):
        return self.gui.GetOrificeTimeCtrl()

    @orificeTimeCtrl.setter
    def orificeTimeCtrl(self, orificeTimeCtrl):
        self.gui.SetOrificeTimeCtrl(orificeTimeCtrl)





    #Intake CB
    @property
    def intakeCB(self):
        return self.gui.GetIntakeCB()

    @intakeCB.setter
    def intakeCB(self, intakeCB):
        self.gui.SetIntakeCB(intakeCB)



    #Orifice CB
    @property
    def orificeCB(self):
        return self.gui.GetOrificeCB()

    @orificeCB.setter
    def orificeCB(self, orificeCB):
        self.gui.SetOrificeCB(orificeCB)



    #Program Downloaded CB
    @property
    def programCB(self):
        return self.gui.GetProgramCB()

    @programCB.setter
    def programCB(self, programCB):
        self.gui.SetProgramCB(programCB)



    #Data Downloaded CB
    @property
    def dataCB(self):
        return self.gui.GetDataCB()

    @dataCB.setter
    def dataCB(self, dataCB):
        self.gui.SetDataCB(dataCB)



    #Data Period From
    @property
    def dataPeriodFromPicker(self):
        return self.gui.GetDataPeriodFromPicker()

    @dataPeriodFromPicker.setter
    def dataPeriodFromPicker(self, dataPeriodFromPicker):
        self.gui.SetDataPeriodFromPicker(dataPeriodFromPicker)



    #Data Period To
    @property
    def dataPeriodToPicker(self):
        return self.gui.GetDataPeriodToPicker()

    @dataPeriodToPicker.setter
    def dataPeriodToPicker(self, dataPeriodToPicker):
        self.gui.SetDataPeriodToPicker(dataPeriodToPicker)
        



    @property
    def gasSysDepCtrl(self):
        return self.gui.GetGasDepSysCtrl()

    @gasSysDepCtrl.setter
    def gasSysDepCtrl(self, gasSysDepCtrl):
        self.gui.SetGasDepSysCtrl(gasSysDepCtrl)

    @property
    def gasArrTime(self):
        return self.gui.GetGasArrTime()

    @gasArrTime.setter
    def gasArrTime(self, gasArrTime):
        self.gui.SetGasArrTime(gasArrTime)


    @property
    def gasDepTime(self):
        return self.gui.GetGasDepTime()

    @gasDepTime.setter
    def gasDepTime(self, gasDepTime):
        self.gui.SetGasDepTime(gasDepTime)

    @property
    def feedDepCtrl(self):
        return self.gui.GetFeedDepCtrl()

    @feedDepCtrl.setter
    def feedDepCtrl(self, feedDepCtrl):
        self.gui.SetFeedDepCtrl(feedDepCtrl)

    @property
    def feedArrTime(self):
        return self.gui.GetFeedArrTime()

    @feedArrTime.setter
    def feedArrTime(self, feedArrTime):
        self.gui.SetFeedArrTime(feedArrTime)

    @property
    def feedDepTime(self):
        return self.gui.GetFeedDepTime()

    @feedDepTime.setter
    def feedDepTime(self, feedDepTime):
        self.gui.SetFeedDepTime(feedDepTime)


    @property
    def bpmrotDepCtrl(self):
        return self.gui.GetBpmrotDepCtrl()

    @bpmrotDepCtrl.setter
    def bpmrotDepCtrl(self, bpmrotDepCtrl):
        self.gui.SetBpmrotDepCtrl(bpmrotDepCtrl)


    @property
    def bpmrotArrTime(self):
        return self.gui.GetBpmrotArrTime()

    @bpmrotArrTime.setter
    def bpmrotArrTime(self, bpmrotArrTime):
        self.gui.SetBpmrotArrTime(bpmrotArrTime)


    @property
    def bpmrotDepTime(self):
        return self.gui.GetBpmrotDepTime()

    @bpmrotDepTime.setter
    def bpmrotDepTime(self, bpmrotDepTime):
        self.gui.SetBpmrotDepTime(bpmrotDepTime)


    @property
    def stationHealthRemarksCtrl(self):
        return self.gui.stationHealthRemarksCtrl.GetValue()

    @stationHealthRemarksCtrl.setter
    def stationHealthRemarksCtrl(self, stationHealthRemarksCtrl):
        self.gui.stationHealthRemarksCtrl.SetValue(stationHealthRemarksCtrl)



    def GetLevelsCtrl(self):
        return self.gui.levelsCtrl

    def GetCloudCoverCmbo(self):
        return self.gui.cloudCoverCmbo

    def GetPrecipCmbo(self):
        return self.gui.precipCmbo

    def GetWindMagCmbo(self):
        return self.gui.windMagCmbo

    def GetWindmagCtrl(self):
        return self.gui.windMagCtrl

    def GetBatteryCtrl(self):
        return self.gui.batteryCtrl

    def GetGasSysCtrl(self):
        return self.gui.gasSysCtrl

    def GetFeedCtrl(self):
        return self.gui.feedCtrl

    def GetBpmrotCmbo(self):
        return self.gui.bpmrotCmbo

    def GetBpmrotCtrl(self):
        return self.gui.bpmrotCtrl

    def GetIntakeTimeCtrl(self):
        return self.gui.intakeTimeCtrl

    def GetOrificeTimeCtrl(self):
        return self.gui.orificeTimeCtrl

    def GetIntakeCB(self):
        return self.gui.intakeCB

    def GetOrificeCB(self):
        return self.gui.orificeCB

    def GetProgramCB(self):
        return self.gui.programCB

    def GetDataCB(self):
        return self.gui.dataCB

    def GetDataPeriodFromPicker(self):
        return self.gui.dataPeriodFromPicker

    def GetDataPeriodToPicker(self):
        return self.gui.dataPeriodToPicker



    #Gas Departure Ctrl
    def GetGasDepSysCtrl(self):
        return self.gui.gasSysDepCtrl

    #Gas Arrival Time
    def GetGasArrTime(self):
        return self.gui.gasArrTime

    #Gas Departure Time
    def GetGasDepTime(self):
        return self.gui.gasDepTime

    #Feed Departure Ctrl
    def GetFeedDepCtrl(self):
        return self.gui.feedDepCtrl

    #Feed Arrival time
    def GetFeedArrTime(self):
        return self.gui.feedArrTime

    #Feed Departure time
    def GetFeedDepTime(self):
        return self.gui.feedDepTime


    def GetBpmrotDepCtrl(self):
        return self.gui.bpmrotDepCtrl

    def GetBpmrotArrTime(self):
        return self.gui.bpmrotArrTime

    def GetBpmrotDepTime(self):
        return self.gui.bpmrotDepTime




def main():
    app = wx.App()

    frame = wx.Frame(None, size=(-1, 400))
    EnvironmentConditionsManager("DEBUG", EnvironmentConditionsPanel("DEBUG", frame))

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
