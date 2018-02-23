from InstrumentDeploymentInfoPanel import *


class InstrumentDeploymentInfoManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "InstrumentDeploymentInfoControl"



    def OnInstrumentChange(self, val):
        self.manager.FieldReviewChecklistUpdate(val)

    #Method Type Checkbox
    @property
    def methodCBListBox(self):
        return self.gui.GetMethodCBListBox()

    @methodCBListBox.setter
    def methodCBListBox(self, method):
        self.gui.SetMethodCBListBox(method)


    def GetPicturedCkboxVal(self):
        return self.gui.picturedCkbox.IsChecked()

    def SetPicturedCkboxVal(self, val):
        self.gui.picturedCkbox.SetValue(val)

    def GetPicturedCkbox(self):
        return self.gui.picturedCkbox






    # #Method Type Checkbox for xml
    # @property
    # def methodCBListBoxFromXml(self):
    #     return self.gui.methodCBListBox

    # @methodCBListBoxFromXml.setter
    # def methodCBListBoxFromXml(self, method):
    #     depMethodList = list(self.methodCBListBox.GetItems())
    #     if method in depMethodList:
    #         index = depMethodList.index(method)
    #         self.gui.methodCBListBox.Check(index, check=True)








    # Called from InstrumentDeploymentInfoPanel -> OnDeploymentCheckListCB()
    # When the Method Deployment is changed, update the Field Review Checklist
    #   with the appropriate list
    def OnDeploymentUpdate(self):
        if self.manager is not None:
            checkList = self.methodCBListBox.GetCheckedStrings()
            
            check = None
            if len(checkList) > 0:
                check = checkList[0]

            self.manager.DeploymentUpdate(str(check))

            # if not self.gui.methodCBListBox.IsChecked(0) and not self.gui.methodCBListBox.IsChecked(1) or \
            # (self.gui.methodCBListBox.IsChecked(1) and self.instrumentCmbo.lower() != 'adcp' and \
            #     self.instrumentCmbo.lower() != 'adv' and self.instrumentCmbo.lower() != 'current meter'):
            #     print 'for loops'
            #     for child in self.manager.gui.frChecklist.labelPanel.GetSizer().GetChildren():
            #         child.GetWindow().Enable(False)
            #     for child in self.manager.gui.frChecklist.cbRevPanel.GetSizer().GetChildren():
            #         child.GetWindow().Enable(False)
            #     for child in self.manager.gui.frChecklist.cbCheckPanel.GetSizer().GetChildren():
            #         child.GetWindow().Enable(False)
            #     for child in self.manager.gui.frChecklist.ctrlValuePanel.GetSizer().GetChildren():
            #         child.GetWindow().Enable(False)


    #Deployment Combo
    @property
    def deploymentCmbo(self):
        return self.gui.GetDeploymentCmbo()

    @deploymentCmbo.setter
    def deploymentCmbo(self, deploymentCmbo):
        self.gui.SetDeploymentCmbo(deploymentCmbo)


    #Position Method Ctrl
    @property
    def positionMethodCtrl(self):
        return self.gui.GetPositionMethodCtrl()

    @positionMethodCtrl.setter
    def positionMethodCtrl(self, positionMethodCtrl):
        self.gui.SetPositionMethodCtrl(positionMethodCtrl)
        

    #Instrument Combo
    @property
    def instrumentCmbo(self):
        return self.gui.GetInstrumentCmbo()

    @instrumentCmbo.setter
    def instrumentCmbo(self, instrumentCmbo):
        self.gui.SetInstrumentCmbo(instrumentCmbo)


    #Instrument Combo for open saved xml
    @property
    def instrumentCmboFromXml(self):
        return self.gui.GetInstrumentCmboFromXml()

    @instrumentCmboFromXml.setter
    def instrumentCmboFromXml(self, instrumentCmbo):
        self.gui.SetInstrumentCmboFromXml(instrumentCmbo)

    #Serial Number Combo
    @property
    def serialCmbo(self):
        return self.gui.GetSerialCmbo()

    @serialCmbo.setter
    def serialCmbo(self, serialCmbo):
        self.gui.SetSerialCmbo(serialCmbo)



    #Serial Number Combo for open saved xml
    @property
    def serialCmboFromXml(self):
        return self.gui.GetSerialCmboFromXml()

    @serialCmboFromXml.setter
    def serialCmboFromXml(self, serialCmbo):
        self.gui.SetSerialCmboFromXml(serialCmbo)
        

    #Gauge Ctrl
    @property
    def gaugeCtrl(self):
        return self.gui.GetGaugeCtrl()

    @gaugeCtrl.setter
    def gaugeCtrl(self, gaugeCtrl):
        self.gui.SetGaugeCtrl(gaugeCtrl)

    #Length Radio Button Box
    @property
    def lengthRadButBox(self):
        return self.gui.GetLengthRadButBox()

    @lengthRadButBox.setter
    def lengthRadButBox(self, index):
        self.gui.SetLengthRadButBox(index)

    #Position Radio Button Box
    @property
    def posRadButBox(self):
        return self.gui.GetPosRadButBox()

    @posRadButBox.setter
    def posRadButBox(self, index):
        self.gui.SetPosRadButBox(index)

    # #Gauge Ctrl 2
    # @property
    # def gaugeCtrl2(self):
    #     return self.gui.gaugeCtrl2()

    # @gaugeCtrl2.setter
    # def gaugeCtrl2(self, gaugeCtrl2):
    #     self.gui.gaugeCtrl2(gaugeCtrl2)


    #Midsection Method Info
    #Number of Panels SpinCtrl
    @property
    def numOfPanelsScroll(self):
        return self.gui.GetNumOfPanelsScroll()

    @numOfPanelsScroll.setter
    def numOfPanelsScroll(self, numOfPanelsScroll):
        self.gui.SetNumOfPanelsScroll(numOfPanelsScroll)

    #Flow Angle Combo
    @property
    def flowAngleCmbo(self):
        return self.gui.GetFlowAngleCmbo()

    @flowAngleCmbo.setter
    def flowAngleCmbo(self, flowAngleCmbo):
        self.gui.SetFlowAngleCmbo(flowAngleCmbo)

    #Co-efficient Ctrl
    @property
    def coEffCtrl(self):
        return self.gui.GetCoEffCtrl()

    @coEffCtrl.setter
    def coEffCtrl(self, coEffCtrl):
        self.gui.SetCoEffCtrl(coEffCtrl)
    
    #Method Combo
    @property
    def methodCmbo(self):
        return self.gui.GetMethodCmbo()

    @methodCmbo.setter
    def methodCmbo(self, methodCmbo):
        self.gui.SetMethodCmbo(methodCmbo)

    #Metres Ctrl
    @property
    def metresCtrl(self):
        return self.gui.GetMetresCtrl()

    @metresCtrl.setter
    def metresCtrl(self, metresCtrl):
        self.gui.SetMetresCtrl(metresCtrl)

    #Weight Ctrl
    @property
    def weightCtrl(self):
        return self.gui.GetWeightCtrl()

    @weightCtrl.setter
    def weightCtrl(self, weightCtrl):
        self.gui.SetWeightCtrl(weightCtrl)

    #Weight Radio Button Box
    @property
    def weightRadButBox(self):
        return self.gui.GetWeightRadButBox()

    @weightRadButBox.setter
    def weightRadButBox(self, index):
        self.gui.SetWeightRadButBox(index)



    #ADCP Info
    #Frequency Control
    @property
    def frequencyCmbo(self):
        
        return self.gui.GetFrequencyCmbo()

    @frequencyCmbo.setter
    def frequencyCmbo(self, frequencyCmbo):
        self.gui.SetFrequencyCmbo(frequencyCmbo)

    #Firmware Control
    @property
    def firmwareCmbo(self):
        return self.gui.GetFirmwareCmbo()

    @firmwareCmbo.setter
    def firmwareCmbo(self, firmwareCmbo):
        self.gui.SetFirmwareCmbo(firmwareCmbo)

    #Software Control
    @property
    def softwareCtrl(self):
        return self.gui.GetSoftwareCtrl()

    @softwareCtrl.setter
    def softwareCtrl(self, softwareCtrl):
        self.gui.SetSoftwareCtrl(softwareCtrl)
        

    #Config Combo Box
    @property
    def configCmbo(self):
        return self.gui.GetConfigCmbo()

    @configCmbo.setter
    def configCmbo(self, configCmbo):
        self.gui.SetConfigCmbo(configCmbo)

    #Config Control
    @property
    def configCtrl(self):
        return self.gui.GetConfigCtrl()

    @configCtrl.setter
    def configCtrl(self, configCtrl):
        self.gui.SetConfigCtrl(configCtrl)

    #ADCP Set to Clock Checkbox
    @property
    def adcpSetToClockCB(self):
        return self.gui.GetAdcpSetToClockCB()

    @adcpSetToClockCB.setter
    def adcpSetToClockCB(self, adcpSetToClockCB):
        self.gui.SetAdcpSetToClockCB(adcpSetToClockCB)

    #Diagnostic Test Checkbox
    @property
    def diagTestCB(self):
        return self.gui.GetDiagTestCB()

    @diagTestCB.setter
    def diagTestCB(self, diagTestCB):
        self.gui.SetDiagTestCB(diagTestCB)

        

    # ADCP Depth Checkbox
    @property
    def adcpDepthCtrl(self):
        return self.gui.GetAdcpDepthCtrl()

    @adcpDepthCtrl.setter
    def adcpDepthCtrl(self, adcpDepthCtrl):
        self.gui.SetAdcpDepthCtrl(adcpDepthCtrl)
    
    #Magnetic Declination Control
    @property
    def magnDeclCtrl(self):
        return self.gui.GetMagnDeclCtrl()

    @magnDeclCtrl.setter
    def magnDeclCtrl(self, magnDeclCtrl):
        self.gui.SetMagnDeclCtrl(magnDeclCtrl)
    
    #Compass Calibration CB
    @property
    def compassCaliCB(self):
        return self.gui.GetCompassCaliCB()

    @compassCaliCB.setter
    def compassCaliCB(self, compassCaliCB):
        self.gui.SetCompassCaliCB(compassCaliCB)
    
    #Passed Field Review CB
    @property
    def passedFieldRevCB(self):
        return self.gui.GetPassedFieldRevCB()

    @passedFieldRevCB.setter
    def passedFieldRevCB(self, passedFieldRevCB):
        self.gui.SetPassedFieldRevCB(passedFieldRevCB)



    #Control and Remarks
    #Control Condition Combo
    @property
    def controlConditionCmbo(self):
        return self.gui.GetControlConditionCmbo()

    @controlConditionCmbo.setter
    def controlConditionCmbo(self, controlConditionCmbo):
        self.gui.SetControlConditionCmbo(controlConditionCmbo)

    #Control Effect Category and Sub-Categories not currently stored
    #Control Effect Cat
    @property
    def controlEffCatCmbo(self):
        return self.gui.GetControlEffCatCmbo()

    @controlEffCatCmbo.setter
    def controlEffCatCmbo(self, controlEffCatCmbo):
        self.gui.SetControlEffCatCmbo(controlEffCatCmbo)

    #Control Effect Sub-Categories
    @property
    def controlEffSubCatCmbo(self):
        return self.gui.GetControlEffSubCatCmbo()

    @controlEffSubCatCmbo.setter
    def controlEffSubCatCmbo(self, controlEffSubCatCmbo):
        self.gui.SetControlEffSubCatCmbo(controlEffSubCatCmbo)

    # #Control Remarks Control
    # @property
    # def controlRemarksCtrl(self):
    #     return self.gui.controlRemarksCtrl()

    # @controlRemarksCtrl.setter
    # def controlRemarksCtrl(self, controlRemarksCtrl):
    #     self.gui.controlRemarksCtrl(controlRemarksCtrl)
        


    #Discharge, Stage, Station Health Remarks
    @property
    def dischRemarksCtrl(self):
        return self.gui.GetDischRemarksCtrl()

    @dischRemarksCtrl.setter
    def dischRemarksCtrl(self, dischRemarksCtrl):
        self.gui.SetDischRemarksCtrl(dischRemarksCtrl)

    @property
    def stageRemarksCtrl(self):
        return self.gui.GetStageRemarksCtrl()

    @stageRemarksCtrl.setter
    def stageRemarksCtrl(self, stageRemarksCtrl):
        self.gui.SetStageRemarksCtrl(stageRemarksCtrl)

    #General
    @property
    def stationHealthRemarksCtrl(self):
        return self.gui.GetStationHealthRemarksCtrl()

    @stationHealthRemarksCtrl.setter
    def stationHealthRemarksCtrl(self, stationHealthRemarksCtrl):
        self.gui.SetStationHealthRemarksCtrl(stationHealthRemarksCtrl)

    #Gauge or other
    @property
    def selectedGauge(self):
        return self.gui.GetSelectedGauge()

    @selectedGauge.setter
    def selectedGauge(self, selectedGauge):

        self.gui.SetSelectedGauge(selectedGauge)




    #Gauge Display
    @property
    def gaugeOtherTxt(self):
        return self.gui.GetGaugeOtherTxt()

    @gaugeOtherTxt.setter
    def gaugeOtherTxt(self, gaugeOtherTxt):
        self.gui.SetGaugeOtherTxt(gaugeOtherTxt)


    #Gauge Radio Button 1
    @property
    def gauge1RadButBox(self):
        return self.gui.GetGauge1RadButBox()

    @gauge1RadButBox.setter
    def gauge1RadButBox(self, val):
        self.gui.SetGauge1RadButBox(val)



    #Gauge Radio Button 2
    @property
    def gauge2RadButBox(self):
        return self.gui.GetGauge2RadButBox()

    @gauge2RadButBox.setter
    def gauge2RadButBox(self, val):
        self.gui.SetGauge2RadButBox(val)




    #Weight Radio Button 1
    @property
    def weightRadBut1(self):
        return self.gui.GetWeightRadBut1()

    @weightRadBut1.setter
    def weightRadBut1(self, val):
        self.gui.SetWeightRadBut1(val)



    #Weight Radio Button 2
    @property
    def weightRadBut2(self):
        return self.gui.GetWeightRadBut2()

    @weightRadBut2.setter
    def weightRadBut2(self, val):
        self.gui.SetWeightRadBut2(val)



    #Manufacturer combo box
    @property
    def manufactureCmbo(self):
        return self.gui.GetManufactureCmbo()

    @manufactureCmbo.setter
    def manufactureCmbo(self, manufactureCmbo):
        self.gui.SetManufactureCmbo(manufactureCmbo)

    #Manufacturer combo box from Xml
    @property
    def manufactureCmboFromXml(self):
        return self.gui.GetManufactureCmboFromXml()

    @manufactureCmboFromXml.setter
    def manufactureCmboFromXml(self, manufactureCmbo):
        self.gui.SetManufactureCmboFromXml(manufactureCmbo)

    #Model combo box
    @property
    def modelCmbo(self):
        return self.gui.GetModelCmbo()

    @modelCmbo.setter
    def modelCmbo(self, modelCmbo):
        self.gui.SetModelCmbo(modelCmbo)

    #firmwareCmbo combo box
    @property
    def firmwareCmbo(self):
        return self.gui.GetFirmwareCmbo()

    @firmwareCmbo.setter
    def firmwareCmbo(self, firmwareCmbo):
        self.gui.SetFirmwareCmbo(firmwareCmbo)

    def PrintEverything(self):
        checkList = self.methodCBListBox.GetCheckedStrings()
        
        check = None
        if len(checkList) > 0:
            check = checkList[0]

            
        print "Method: %s" %  check
        print "Deployment: %s" % self.deploymentCmbo
        print "Position: %s" % self.positionMethodCtrl
        print "Instrument: %s" % self.instrumentCmbo
        print "Serial/Meter Num: %s" % self.serialCmbo
        print "Gauge1: %s" % self.gaugeCtrl
        print "Length Radio Box: %s" % self.lengthRadButBox
        print "Position Radio Box: %s" % self.posRadButBox
        # print "Gauge2: %s" % self.gaugeCtrl2

        print "\nMidsection Method"
        print "Num of Panels: %s" % self.numOfPanelsScroll
        print "Flow Angle: %s" % self.flowAngleCmbo
        print "Coefficient: %s" % self.coEffCtrl
        print "Method: %s" % self.methodCmbo
        print "Located: %s" % self.metresCtrl
        print "Metres above: %s" % self.weightCtrl
        print "Weight Radio Box: %s" % self.weightRadButBox

        print "\nADCP Method"
        print "Frequency: %s" % self.frequencyCtrl
        print "Firmware: %s" % self.firmwareCmbo
        print "Software: %s" % self.softwareCtrl
        print "Config Combo: %s" % self.configCmbo
        print "Config Ctrl: %s" % self.configCtrl
        print "ADCP Set to Clock: %s" % self.adcpSetToClockCB
        print "Diagnostic Test: %s" % self.diagTestCB
        print "ADCP Depth: %s" % self.adcpDepthCtrl
        print "Magnetic Decl: %s" % self.magnDeclCtrl
        print "Compass Cali: %s" % self.compassCaliCB
        print "Passed Field Rev: %s" % self.passedFieldRevCB

        print "\nControl"
        print "Condition: %s" % self.controlConditionCmbo
        print "Effect Cat: %s" % self.controlEffCatCmbo
        print "Effect Sub-Cat: %s" % self.controlEffSubCatCmbo
        # print "Control Remarks: %s" % self.controlRemarksCtrl
        print "Discharge Remarks: %s" % self.dischRemarksCtrl
        print "Stage Remarks: %s" % self.stageRemarksCtrl
        print "General Remarks: %s" % self.stationHealthRemarksCtrl
                                         
        





    def GetMethodCBListBox(self):
        return self.gui.methodCBListBox
    def GetDeploymentCmbo(self):
        return self.gui.deploymentCmbo
    def GetPositionMethodCmbo(self):
        return self.gui.positionMethodCmbo
    def GetGaugeCtrl(self):
        return self.gui.gaugeCtrl
    def GetLengthRadButBox(self):
        return self.gui.lengthRadButBox
    def GetPosRadButBox(self):
        return self.gui.posRadButBox
    def GetGauge1RadButBox(self):
        return self.gui.gauge1RadButBox
    def GetGauge2RadButBox(self):
        return self.gui.gauge2RadButBox
    def GetGaugeOtherTxt(self):
        return self.gui.gaugeOtherTxt
    def GetSerialCmbo(self):
        return self.gui.serialCmbo
    def GetInstrumentCmbo(self):
        return self.gui.instrumentCmbo
    def GetManufactureCmbo(self):
        return self.gui.manufactureCmbo
    def GetModelCmbo(self):
        return self.gui.modelCmbo
    def GetFrequencyCmbo(self):
        return self.gui.frequencyCmbo
    def GetFirmwareCmbo(self):
        return self.gui.firmwareCmbo
    def GetSoftwareCtrl(self):
        return self.gui.softwareCtrl
    def GetNumOfPanelsScroll(self):
        return self.gui.numOfPanelsScroll
    def GetFlowAngleCmbo(self):
        return self.gui.flowAngleCmbo
    def GetCoEffCtrl(self):
        return self.gui.coEffCtrl
    def GetMethodCmbo(self):
        return self.gui.methodCmbo
    def GetMetresCtrl(self):
        return self.gui.metresCtrl
    def GetWeightCtrl(self):
        return self.gui.weightCtrl
    def GetWeightRadButBox(self):
        return self.gui.weightRadButBox
    def GetWeightRadBut2(self):
        return self.gui.weightRadBut2
    def GetWeightRadBut1(self):
        return self.gui.weightRadBut1
    def GetConfigCmbo(self):
        return self.gui.configCmbo
    def GetConfigCtrl(self):
        return self.gui.configCtrl
    def GetAdcpSetToClockCB(self):
        return self.gui.adcpSetToClockCB
    def GetDiagTestCB(self):
        return self.gui.diagTestCB
    def GetAdcpDepthCtrl(self):
        return self.gui.adcpDepthCtrl
    def GetMagnDeclCtrl(self):
        return self.gui.magnDeclCtrl
    def GetControlConditionCmbo(self):
        return self.gui.controlConditionCmbo
    def GetDischRemarksCtrl(self):
        return self.gui.dischRemarksCtrl
    def GetStageRemarksCtrl(self):
        return self.gui.stageRemarksCtrl
    def GetStationHealthRemarksCtrl(self):
        return self.gui.stationHealthRemarksCtrl


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(790, 600))
    InstrumentDeploymentInfoManager("DEBUG", InstrumentDeploymentInfoPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
