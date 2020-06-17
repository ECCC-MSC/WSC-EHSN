import wx
import shutil

from pdb import set_trace


class IngestOptionFrame(wx.Frame):
    def __init__(self, mode, inType, *args, **kwargs):
        super(IngestOptionFrame, self).__init__(*args, **kwargs)
        self.mode = mode
        self.inType = inType

        self.ID_HFC = self.GetParent().ID_IMPORT_HFC
        self.ID_FT = self.GetParent().ID_IMPORT_FTDIS
        self.ID_FT2 = self.GetParent().ID_IMPORT_FT2
        self.ID_QREV = self.GetParent().ID_IMPORT_QRXML
        self.ID_MMT = self.GetParent().ID_IMPORT_SXSMMT
        self.ID_RSSL = self.GetParent().ID_IMPORT_RSSDIS

        self.importQRevMsg = "Select one or more of the following checkmarks to import data from the external Qmmt files to eHSN. "
        self.importQRevOption1 = "Channel Results Summary [e.g. Total Q, Mean Vel., etc.]"
        self.importQRevOption2 = "Measurement and Equipment Details (Front page)"
        self.importQRevOption3 = "Moving Boat Page"
        self.importSucessMsg = "Data imported succesfully!"
        self.importSucessTitle = "Succesful"

        self.overwriteMsg = "Some of the information will be overwritten by the imported data. Countinue?"
        self.iverwriteTitle = "Overwrite"

        self.titleFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)



        self.InitUI()


    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(mainSizer)
        self.mainPanel = wx.Panel(self)
        mainSizer.Add(self.mainPanel, 1, wx.EXPAND)

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainPanel.SetSizer(self.layoutSizer)

        desciption = wx.StaticText(self.mainPanel, label=self.importQRevMsg, style=wx.ALIGN_LEFT)
        desciption.SetFont(self.titleFont)



        self.summaryCkbox = wx.CheckBox(self.mainPanel, label=self.importQRevOption1, style=wx.ALIGN_LEFT)
        self.dischargeDetailCkbox = wx.CheckBox(self.mainPanel, label=self.importQRevOption2, style=wx.ALIGN_LEFT)
        self.movingBoatCkbox = wx.CheckBox(self.mainPanel, label=self.importQRevOption3, style=wx.ALIGN_LEFT)

        self.summaryCkbox.SetValue(True)
        self.dischargeDetailCkbox.SetValue(True)
        self.movingBoatCkbox.SetValue(True)

        sizerH1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerH2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerH3 = wx.BoxSizer(wx.HORIZONTAL)

        sizerH1.Add((60,-1), 0, wx.EXPAND)
        sizerH1.Add(self.summaryCkbox, 1, wx.EXPAND)

        sizerH2.Add((60,-1), 0, wx.EXPAND)
        sizerH2.Add(self.dischargeDetailCkbox, 1, wx.EXPAND)

        sizerH3.Add((60,-1), 0, wx.EXPAND)
        sizerH3.Add(self.movingBoatCkbox, 1, wx.EXPAND)


        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.impBtn = wx.Button(self.mainPanel, label="Import")
        self.canBtn = wx.Button(self.mainPanel, label="Cancel")

        self.impBtn.Bind(wx.EVT_BUTTON, self.OnImport)
        self.canBtn.Bind(wx.EVT_BUTTON, self.OnCancel)


        self.buttonSizer.Add((300,-1), 0, wx.EXPAND|wx.ALL, 5)
        self.buttonSizer.Add(self.impBtn, 0, wx.ALL, 5)
        self.buttonSizer.Add(self.canBtn, 0, wx.ALL, 5)



        self.layoutSizer.Add(desciption, 1, wx.EXPAND|wx.ALL, 10)
        self.layoutSizer.Add(sizerH1, 0, wx.EXPAND|wx.TOP, 15)
        self.layoutSizer.Add(sizerH2, 0, wx.EXPAND|wx.TOP, 15)
        self.layoutSizer.Add(sizerH3, 0, wx.EXPAND|wx.TOP, 15)
        self.layoutSizer.Add(self.buttonSizer, 0, wx.EXPAND|wx.ALL, 10)

        if self.inType == self.ID_FT or self.inType == self.ID_HFC or self.inType == self.ID_FT2 or self.inType == self.ID_MMT or self.inType == self.ID_RSSL:
            self.movingBoatCkbox.Enable(False)
            self.movingBoatCkbox.Hide()
            self.movingBoatCkbox.SetValue(False)


    #Triggered when the import button pressed
    def OnImport(self, evt):
        #Double confirm from the user to overwrite the data from imported files on "Import" button clicked
        # if self.summaryCkbox.IsChecked() or self.dischargeDetailCkbox.IsChecked() or self.movingBoatCkbox.IsChecked():
        #     dlg = wx.MessageDialog(self, self.overwriteMsg, self.iverwriteTitle,
        #                              wx.YES_NO | wx.ICON_INFORMATION)
        #     res = dlg.ShowModal()
        #     if res == wx.ID_NO:
        #         dlg.Destroy()
        #         return

        if self.summaryCkbox.IsChecked():
            if self.inType == self.ID_QREV:
                self.GetParent().manager.AddDischargeSummaryFromQRev()
            elif self.inType == self.ID_FT:
                self.GetParent().manager.AddDischargeSummaryFromFT()
            elif self.inType == self.ID_HFC:
                self.GetParent().manager.AddDischargeSummaryFromHfc()
            elif self.inType == self.ID_FT2:
                self.GetParent().manager.AddDischargeSummaryFromFt2()
            elif self.inType == self.ID_MMT:
                self.GetParent().manager.AddDischargeSummaryFromSxs()
            elif self.inType == self.ID_RSSL:
                self.GetParent().manager.AddDischargeSummaryFromRssl()

            self.GetParent().disMeas.OnTimeChange(evt)
        
        overwrite = False
        if self.dischargeDetailCkbox.IsChecked():
            if self.inType == self.ID_QREV:
                # self.GetParent().manager.instrDepManager.GetMethodCBListBox().Check(0)
                overwrite = self.GetParent().instrDep.DeploymentCheckListCBCkecking4MovingBoat()

                    
            # elif self.inType == self.ID_FT or self.inType == self.ID_HFC or self.inType == self.ID_FT2 or self.inType == self.ID_MMT or self.inType == self.ID_RSSL:
            else:
                # self.GetParent().manager.instrDepManager.GetMethodCBListBox().Check(1)
                overwrite = self.GetParent().instrDep.DeploymentCheckListCBCkecking4MidSection()
            if overwrite:
                if self.inType == self.ID_QREV:
                    self.GetParent().manager.AddDischargeDetailFromQRev()
                if self.inType == self.ID_FT:
                    self.GetParent().manager.AddDischargeDetailFromFT()

                elif self.inType == self.ID_HFC:

                    self.GetParent().manager.AddDischargeDetailFromHfc()
                elif self.inType == self.ID_FT2:

                    self.GetParent().manager.AddDischargeDetailFromFt2()

                elif self.inType == self.ID_MMT:

                    self.GetParent().manager.AddDischargeDetailFromSxs()

                elif self.inType == self.ID_RSSL:

                    self.GetParent().manager.AddDischargeDetailFromRssl()
		# self.GetParent().instrDep.RefreshDeploymentMethod()

        if self.movingBoatCkbox.IsChecked():
            if self.inType == self.ID_QREV:
                self.GetParent().manager.AddMovingBoatFromQRev(evt)


        self.Destroy()



        if self.summaryCkbox.IsChecked() or overwrite or self.movingBoatCkbox.IsChecked():

            info = wx.MessageDialog(self, self.importSucessMsg, self.importSucessTitle,
                                     wx.OK | wx.ICON_INFORMATION)
            info.ShowModal()

        if self.inType == self.ID_FT2 and self.GetParent().ft2FtDir is not None and self.GetParent().ft2FtDir != "":

            shutil.rmtree(self.GetParent().ft2FtDir.split('.')[0])

        # #Change the Station Name accordingly about Station Number after import
        # self.GetParent().OnStationSelect(evt)



    def OnCancel(self, evt):
        if self.inType == self.ID_FT2 and self.GetParent().ft2FtDir is not None and self.GetParent().ft2FtDir != "":
            shutil.rmtree(self.GetParent().ft2FtDir.split('.')[0])
        self.Destroy()



def main():
    app = wx.App()

    frame = QRevOptionFrame(None, title="Dialog Test", size=(550, 270))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()