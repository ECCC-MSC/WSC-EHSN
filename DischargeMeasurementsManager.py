
# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html
from DischargeMeasurementsPanel import *


class DischargeMeasurementsManager(object):
    def __init__(self, mode, gui, manager=None):
        self.gui = gui
        self.gui.manager = self
        self.manager = manager

        self.fieldMissingTitle = "Mandatory Field Missing"
        self.airTempMissingMessage = "Air temprature is missing"
        self.waterTempMissingMessage = "Water temprature is missing"
        self.widthMissingMessage = "Width is missing"

        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "DischargeMeasurementsControl"


    def IsEmpty(self):
        return self.gui.IsEmpty()


    #Start Time Ctrl
    @property
    def startTimeCtrl(self):
        return self.gui.GetStartTimeCtrl()

    @startTimeCtrl.setter
    def startTimeCtrl(self, startTimeCtrl):
        self.gui.SetStartTimeCtrl(startTimeCtrl)


    #End Time Ctrl
    @property
    def endTimeCtrl(self):
        return self.gui.GetEndTimeCtrl()

    @endTimeCtrl.setter
    def endTimeCtrl(self, endTimeCtrl):
        self.gui.SetEndTimeCtrl(endTimeCtrl)


    #Air Temp Ctrl
    @property
    def airTempCtrl(self):
        return self.gui.GetAirTempCtrl()

    @airTempCtrl.setter
    def airTempCtrl(self, airTempCtrl):
        self.gui.SetAirTempCtrl(airTempCtrl)


    #Water Temp Ctrl
    @property
    def waterTempCtrl(self):
        return self.gui.GetWaterTempCtrl()

    @waterTempCtrl.setter
    def waterTempCtrl(self, waterTempCtrl):
        self.gui.SetWaterTempCtrl(waterTempCtrl)


    #Width Info ctrl
    @property
    def widthCtrl(self):
        return self.gui.GetWidthCtrl()

    @widthCtrl.setter
    def widthCtrl(self, widthCtrl):
        self.gui.SetWidthCtrl(widthCtrl)


    #Area Info Ctrl
    @property
    def areaCtrl(self):
        return self.gui.GetAreaCtrl()

    @areaCtrl.setter
    def areaCtrl(self, areaCtrl):
        self.gui.SetAreaCtrl(areaCtrl)


    #Mean Velocity Info
    @property
    def meanVelCtrl(self):
        return self.gui.GetMeanVelCtrl()

    @meanVelCtrl.setter
    def meanVelCtrl(self, meanVelCtrl):
        self.gui.SetMeanVelCtrl(meanVelCtrl)



    #MGH Ctrl
    @property
    def mghCtrl(self):
        return self.gui.GetMghCtrl()

    @mghCtrl.setter
    def mghCtrl(self, mghCtrl):
        self.gui.SetMghCtrl(mghCtrl)

    #MGH Combo
    @property
    def mghCmbo(self):
        return self.gui.GetMghCmbo()

    @mghCmbo.setter
    def mghCmbo(self, mghCmbo):
        self.gui.SetMghCmbo(mghCmbo)


    #Discharge Combobox
    @property
    def dischCombo(self):
        return self.gui.GetDischCombo()

    @dischCombo.setter
    def dischCombo(self, dischCombo):
        self.gui.SetDischCombo(dischCombo)



    #Discharge Ctrl
    @property
    def dischCtrl(self):
        return self.gui.GetDischCtrl()

    @dischCtrl.setter
    def dischCtrl(self, dischCtrl):
        self.gui.SetDischCtrl(dischCtrl)



    #Mmt Mean Time Ctrl
    @property
    def mmtValTxt(self):
        return self.gui.GetMmtValTxt()

    @mmtValTxt.setter
    def mmtValTxt(self, mmtValTxt):
        self.gui.SetMmtValTxt(mmtValTxt)



    #Calculate Shift Base Curve Ctrl
    @property
    def shiftCtrl(self):
        return self.gui.GetShiftCtrl()

    @shiftCtrl.setter
    def shiftCtrl(self, shiftCtrl):
        self.gui.SetShiftCtrl(shiftCtrl)



    #Diff Base Curve Info Ctrl
    @property
    def diffCtrl(self):
        return self.gui.GetDiffCtrl()

    @diffCtrl.setter
    def diffCtrl(self, diffCtrl):
        self.gui.SetDiffCtrl(diffCtrl)



    #Curve Info Ctrl
    @property
    def curveCtrl(self):
        return self.gui.GetCurveCtrl()

    @curveCtrl.setter
    def curveCtrl(self, curveCtrl):
        self.gui.SetCurveCtrl(curveCtrl)


    #Control Condition Combo
    @property
    def controlConditionCmbo(self):
        return self.gui.controlConditionCmbo.GetValue()

    @controlConditionCmbo.setter
    def controlConditionCmbo(self, controlConditionCmbo):
        self.gui.controlConditionCmbo.SetValue(controlConditionCmbo)



    #Control Remarks Control
    @property
    def ControlConditionRemarksCtrl(self):
        return self.gui.controlConditionRemarksCtrl.GetValue()

    @ControlConditionRemarksCtrl.setter
    def ControlConditionRemarksCtrl(self, ControlConditionRemarksCtrl):
        self.gui.controlConditionRemarksCtrl.SetValue(ControlConditionRemarksCtrl)


    @property
    def dischRemarksCtrl(self):
        return self.gui.dischRemarksCtrl.GetValue()

    @dischRemarksCtrl.setter
    def dischRemarksCtrl(self, dischRemarksCtrl):
        self.gui.dischRemarksCtrl.SetValue(dischRemarksCtrl)



    def GetMGHChoices(self):
        return self.gui.mghChoices

    def SetMghChoices(self, choices):
        self.gui.mghChoices = choices


    def mandatoryChecking(self):
        if (self.airTempCtrl == ""):
            empty = wx.MessageDialog(None, self.airTempMissingMessage, self.fieldMissingTitle, wx.OK)
            empty.ShowModal()
            return True
        elif (self.waterTempCtrl == ""):
            empty = wx.MessageDialog(None, self.waterTempMissingMessage, self.fieldMissingTitle, wx.OK)
            empty.ShowModal()
            return True
        elif (self.widthCtrl == ""):
            empty = wx.MessageDialog(None, self.widthMissingMessage, self.fieldMissingTitle, wx.OK)
            empty.ShowModal()
            return True
        else:
            return False


    def PrintEverything(self):
        print self.startTimeCtrl
        print self.endTimeCtrl
        print self.airTempCtrl
        print self.waterTempCtrl
        print self.widthCtrl
        print self.areaCtrl
        print self.meanVelCtrl
        print self.mghCtrl
        print self.dischCtrl
        print self.mmtValTxt
        print self.shiftCtrl
        print self.diffCtrl
        print self.curveCtrl
        


    def GetStartTimeCtrl(self):
        return self.gui.startTimeCtrl

    def GetEndTimeCtrl(self):
        return self.gui.endTimeCtrl

    def GetAirTempCtrl(self):
        return self.gui.airTempCtrl

    def GetWaterTempCtrl(self):
        return self.gui.waterTempCtrl

    def GetWidthCtrl(self):
        return self.gui.widthCtrl

    def GetAreaCtrl(self):
        return self.gui.areaCtrl

    def GetMeanVelCtrl(self):
        return self.gui.meanVelCtrl

    def GetMghCtrl(self):
        return self.gui.mghCtrl

    def GetMghCmbo(self):
        return self.gui.mghCmbo

    def GetDischCtrl(self):
        return self.gui.dischCtrl

    def GetDischCombo(self):
    	return self.gui.dischCombo

    def GetShiftCtrl(self):
        return self.gui.shiftCtrl

    def GetDiffCtrl(self):
        return self.gui.diffCtrl

    def GetCurveCtrl(self):
        return self.gui.curveCtrl


    def IncompleteTimeCheck(self):
        return self.gui.IncompleteTimeCheck()


    #Return TURE if discharge remarks is empty
    def dischargeRemarkEmpty(self):
        return self.gui.dischRemarksCtrl.GetValue() == ''




        
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 140))
    DischargeMeasurementsManager("DEBUG", DischargeMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()


    
