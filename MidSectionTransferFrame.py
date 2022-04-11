import wx
import shutil


class MidSectionTransferFrame(wx.Frame):
    def __init__(self, mode, *args, **kwargs):
        super(MidSectionTransferFrame, self).__init__(*args, **kwargs)

        self.mode = mode
        self.widthLbl = "Width"
        self.areaLbl = "Area"
        self.meanVelocityLbl = "Mean Velocity"
        self.dischargeLbl = "Discharge"
        self.numberPanelsLbl = "Number of Panels"
        self.meterNumberLbl = "Meter Number"
        self.mmntTimeLbl = "Mmnt Start/End Time"
        self.uncertaintyLbl = 'Uncertainty'

        self.transferTitle = "Transfer selected values to the front page"

        self.transferBtnLbl = "Transfer"
        self.cancelBtnLbl = "Cancel"

        self.titleFont = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)



        self.InitUI()


    def InitUI(self):


        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        # self.SetSizer(self.layoutSizer)

        mainPanel = wx.Panel(self)
        mainPanel.SetSizer(self.layoutSizer)

        description = wx.StaticText(mainPanel, label=self.transferTitle, style=wx.ALIGN_LEFT)
        description.SetFont(self.titleFont)


        self.mmntTimeCkbox = wx.CheckBox(mainPanel, label=self.mmntTimeLbl, style=wx.ALIGN_LEFT)
        self.numberPanelsCkbox = wx.CheckBox(mainPanel, label=self.numberPanelsLbl, style=wx.ALIGN_LEFT)
        self.widthCkbox = wx.CheckBox(mainPanel, label=self.widthLbl, style=wx.ALIGN_LEFT)
        self.areaCkbox = wx.CheckBox(mainPanel, label=self.areaLbl, style=wx.ALIGN_LEFT)
        self.meanVelocityCkbox = wx.CheckBox(mainPanel, label=self.meanVelocityLbl, style=wx.ALIGN_LEFT)
        self.dischargeCkbox = wx.CheckBox(mainPanel, label=self.dischargeLbl, style=wx.ALIGN_LEFT)
        self.meterNumberCkbox = wx.CheckBox(mainPanel, label=self.meterNumberLbl, style=wx.ALIGN_LEFT)
        self.uncertaintyCkbox = wx.CheckBox(mainPanel, label=self.uncertaintyLbl, style=wx.ALIGN_LEFT)

        


        self.widthCkbox.SetValue(True)
        self.areaCkbox.SetValue(True)
        self.meanVelocityCkbox.SetValue(True)
        self.dischargeCkbox.SetValue(True)
        self.numberPanelsCkbox.SetValue(True)
        self.meterNumberCkbox.SetValue(True)
        self.uncertaintyCkbox.SetValue(True)
        self.mmntTimeCkbox.SetValue(True)

        self.cancelBtn = wx.Button(mainPanel, label=self.cancelBtnLbl)
        self.transferBtn = wx.Button(mainPanel, label=self.transferBtnLbl)

        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.transferBtn.Bind(wx.EVT_BUTTON, self.OnTransfer)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.transferBtn, 1, wx.EXPAND|wx.ALL, 5)
        btnSizer.Add(self.cancelBtn, 1, wx.EXPAND|wx.ALL, 5)
        

        self.layoutSizer.Add(description, 1, wx.EXPAND|wx.ALL, 5)

        self.layoutSizer.Add(self.mmntTimeCkbox, 1, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(self.numberPanelsCkbox, 1, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(self.widthCkbox, 1, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(self.areaCkbox, 1, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(self.meanVelocityCkbox, 1, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(self.dischargeCkbox, 1, wx.EXPAND|wx.ALL, 5)
        
        self.layoutSizer.Add(self.meterNumberCkbox, 1, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(self.uncertaintyCkbox, 1, wx.EXPAND|wx.ALL, 5)

        

        self.layoutSizer.Add(btnSizer, 1, wx.EXPAND|wx.ALL, 5)


    def OnCancel(self, evt):
        print("OnCancelBtn")
        self.Destroy()

    def OnTransfer(self, evt):
        eHSN = self.GetParent().GetParent().GetParent().GetParent().GetParent()
        dischargePanel = eHSN.disMeas
        instrDep = eHSN.instrDep
        
        width = None
        area = None
        avgVel = None
        discharge = None
        numOfPanels = None
        meterNum = None
        uncertainty = None

        transferCommon = False

        if self.widthCkbox.GetValue() and self.GetParent().widthCtrl.GetValue() != "":
            width = self.GetParent().widthCtrl.GetValue()
            dischargePanel.widthCtrl.SetValue(width)
            transferCommon = True

        if self.areaCkbox.GetValue() and self.GetParent().areaCtrl.GetValue() != "":
            area = self.GetParent().areaCtrl.GetValue()
            dischargePanel.areaCtrl.SetValue(area)
            transferCommon = True

        if self.meanVelocityCkbox.GetValue() and self.GetParent().avgVelCtrl.GetValue() != "":
            avgVel = self.GetParent().avgVelCtrl.GetValue()
            dischargePanel.meanVelCtrl.SetValue(avgVel)
            transferCommon = True

        if self.dischargeCkbox.GetValue() and self.GetParent().totalDisCtrl.GetValue() != "":
            discharge = self.GetParent().totalDisCtrl.GetValue()       
            dischargePanel.dischCtrl.SetValue(discharge)
            transferCommon = True

        if self.numberPanelsCkbox.GetValue() and self.GetParent().numOfPanelCtrl.GetValue() != "":
            numOfPanels = self.GetParent().numOfPanelCtrl.GetValue()
            instrDep.numOfPanelsScroll.SetValue(numOfPanels)
            transferCommon = True

        if self.meterNumberCkbox.GetValue() and self.GetParent().meter1MeterNoCtrl.GetValue() != "":
            meterNum = self.GetParent().meter1MeterNoCtrl.GetValue()
            instrDep.serialCmbo.SetValue(meterNum)
            transferCommon = True


        if self.uncertaintyCkbox.GetValue() and self.GetParent().uncertainty2Ctrl.GetValue() != "":
            uncertainty = str(round(float(self.GetParent().uncertainty2Ctrl.GetValue()), 2))
            dischargePanel.uncertaintyCtrl.SetValue(uncertainty)
            transferCommon = True

            # Adding uncertainty text to Discharge Activity Remarks
            dischargeUncertainty = '@ Uncertainty: IVE method, 2-sigma value (IVE Value). @'
            dischargeRemarks = dischargePanel.dischRemarksCtrl
            if dischargeRemarks != '':
                dischargePanel.dischRemarksCtrl = dischargeRemarks + '\n' + dischargeUncertainty
            else:
                dischargePanel.dischRemarksCtrl = dischargeUncertainty

        if self.mmntTimeCkbox.GetValue() and self.GetParent().startTimeCtrl.GetValue() != "" \
                and self.GetParent().endTimeCtrl.GetValue() != "":
            start = self.GetParent().startTimeCtrl.GetValue()
            end = self.GetParent().endTimeCtrl.GetValue()
            dischargePanel.startTimeCtrl.SetValue(start)
            dischargePanel.endTimeCtrl.SetValue(end)
            dischargePanel.UpdateMeanTime()
            transferCommon = True

        if transferCommon:
            # instrDep.methodCBListBox.Check(1)
            # instrDep.methodCBListBox.SetValue(instrDep.measurementMethods[1])
            instrDep.SetMethodCBListBox(instrDep.measurementMethods[1])
            instrDep.DeploymentCheckListCBCkecking4MidSection()

            instrDep.instrumentCmbo.SetValue("Current Meter")
            instrDep.modelCmbo.SetValue("Price AA")
            instrDep.softwareCtrl.SetValue("eHSN " + eHSN.version)

        self.Destroy()




def main():
    app = wx.App()

    frame = QRevOptionFrame(None, title="Dialog Test", size=(550, 270))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()