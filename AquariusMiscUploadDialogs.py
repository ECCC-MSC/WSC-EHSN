import wx

# To be created if there are multiple discharge values
class AquariusMultDisUploadDialog(wx.Dialog):
    def __init__(self, mode, manager, disMeasList, *args, **kwargs):
        super(AquariusMultDisUploadDialog, self).__init__(*args, **kwargs)
        self.manager = manager
        self.mode = mode
        self.disMeasList = disMeasList

        self.Title = "AQUARIUS Upload Tool"
        self.header = "Interesting... a Discharge Activity for this station on this date already exists in AQUARIUS FVT"
        self.selectLbl = "Would you like to Merge with the existing activity or create a new Discharge Activity? Merging will recalculate the start and end times."
        # str(len(disMeasList)) + " Discharge Activit" + ("y was" if len(disMeasList) == 1 else "ies were") +  \
        #    " already detected for this field visit date in AQUARIUS FVT.

        self.mergeLbl = "Merge"
        self.createLbl = "Create new Discharge Activity"
        self.selectButtonLbl = "Select"
        self.cancelButtonLbl = "Cancel"

        self.sizeWidth = 380
        self.sizeHeight = 270
        self.SetSize((self.sizeWidth, self.sizeHeight))

        self.InitUI()


    def InitUI(self):
        if self.mode == "DEBUG":
            print "Aquarius Multiple Discharge Upload Dialog"

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        headerTxt = wx.StaticText(self, size=(-1, -1), label=self.header)
        headerTxt.Wrap(self.sizeWidth)
        font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        headerTxt.SetFont(font)

        selectTxt = wx.StaticText(self, size=(-1, 50), label=self.selectLbl)

        # Create and Merge Radioboxes
        self.createRB = wx.RadioButton(self, label=self.createLbl)
        self.createRB.Bind(wx.EVT_RADIOBUTTON, self.OnRBClick)
        self.mergeRB = wx.RadioButton(self, label=self.mergeLbl)
        self.mergeRB.Bind(wx.EVT_RADIOBUTTON, self.OnRBClick)

        # List of Field Visits
        fvSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fvCombo = wx.ComboBox(self, choices=self.disMeasList, value=self.disMeasList[0], style=wx.CB_READONLY)
        self.fvCombo.Enable(False)
        fvSizer.Add((30, -1), 0, wx.EXPAND)
        fvSizer.Add(self.fvCombo, 1, wx.EXPAND)


        # Select and Cancel buttons
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.selectButton = wx.Button(self, label=self.selectButtonLbl)
        self.cancelButton = wx.Button(self, label=self.cancelButtonLbl)
        buttonSizer.Add((-1, -1), 1, wx.EXPAND)
        buttonSizer.Add(self.selectButton, 0, wx.EXPAND|wx.ALL, 3)
        buttonSizer.Add(self.cancelButton, 0, wx.EXPAND|wx.ALL, 3)

        self.selectButton.SetDefault()
        self.selectButton.Bind(wx.EVT_BUTTON, self.Select)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.Cancel)

        # Add to Sizer
        layoutSizer.Add(headerTxt, 0, wx.EXPAND|wx.ALL, 5)
        layoutSizer.Add(selectTxt, 0, wx.EXPAND|wx.ALL, 5)
        layoutSizer.Add((-1, 5), 0, wx.EXPAND)
        # layoutSizer.Add(mergeCB, 0, wx.EXPAND|wx.LEFT|wx.TOP, 5)
        layoutSizer.Add(self.createRB, 0, wx.EXPAND|wx.ALL, 5)
        layoutSizer.Add(self.mergeRB, 0, wx.EXPAND|wx.LEFT|wx.TOP, 5)
        layoutSizer.Add(fvSizer, 0, wx.EXPAND|wx.ALL, 5)
        # layoutSizer.Add(createCB, 0, wx.EXPAND|wx.ALL, 5)
        layoutSizer.Add((-1, -1), 1, wx.EXPAND)
        layoutSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        layoutSizer.Add(buttonSizer, 0, wx.EXPAND)

        self.SetSizer(layoutSizer)

    def GetSelectedDisMeas(self):
        return self.fvCombo.GetStringSelection()

    def OnRBClick(self, evt):
        rb = evt.GetEventObject()
        rbLabel = rb.GetLabel()
        if rbLabel == self.createLbl:
            self.fvCombo.Enable(False)
        else:
            self.fvCombo.Enable(True)

    def MergeRBIsSelected(self):
        return self.mergeRB.GetValue()

    def CreateRBIsSelected(self):
        return self.createRB.GetValue()

    def Select(self, evt):
        self.EndModal(wx.ID_YES)
        self.Show()

    def Cancel(self, evt):
        self.EndModal(wx.ID_CANCEL)


class AquariusConflictUploadDialog(wx.Dialog):
    def __init__(self, mode, manager, eVal, aVal, paramName, source, *args, **kwargs):
        super(AquariusConflictUploadDialog, self).__init__(*args, **kwargs)
        self.manager = manager
        self.mode = mode
        self.eVal = eVal
        self.aVal = aVal
        self.paramName = paramName
        self.source = "source: " + source

        self.Title = "Upload Field Visit to Aquarius"
        self.headerLbl = "Conflict Detected for " + paramName
        # self.bodyLbl = "A value of " + str(self.aVal) + " for " + \
        #                 self.paramName + " is detected in FVT. Would you like to Overwrite this value with the eHSN value of " + str(self.eVal) + " (source: "\
        #                 + self.source + ")?"

        self.aquariusFVTLbl = "AQUARIUS FVT has a value of: "
        self.ehsnLbl = "eHSN has a value of: "

        # self.overwriteLbl = "Overwrite FVT value with eHSN value"
        # self.keepLbl = "Keep FVT value"
        self.overwriteButtonLbl = "Overwrite FVT value with eHSN value"
        self.keepButtonLbl = "Keep FVT value"

        self.sizeWidth = 360
        self.sizeHeight = 180
        self.SetSize((self.sizeWidth, self.sizeHeight))

        self.InitUI()


    def InitUI(self):
        if self.mode == "DEBUG":
            print "Aquarius Multiple Discharge Upload Dialog"

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        headerTxt = wx.StaticText(self, size=(-1, 25), label=self.headerLbl)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        headerTxt.SetFont(font)

        # bodyTxt = wx.StaticText(self, size=(-1, 45), label=self.bodyLbl)
        # headerTxt.Wrap(self.sizeWidth)
        # font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        # headerTxt.SetFont(font)

        # Display Values
        conflictSizer = wx.BoxSizer(wx.HORIZONTAL)

        # labels
        textSizer = wx.BoxSizer(wx.VERTICAL)
        aqTxt = wx.StaticText(self, label=self.aquariusFVTLbl, style=wx.ALIGN_RIGHT)
        ehsnTxt = wx.StaticText(self, label=self.ehsnLbl, style=wx.ALIGN_RIGHT)
        textSizer.Add(aqTxt, 0, wx.EXPAND|wx.ALL, 3)
        textSizer.Add(ehsnTxt, 0, wx.EXPAND|wx.ALL, 3)

        # values
        valueSizer = wx.BoxSizer(wx.VERTICAL)
        aValTxt = wx.StaticText(self, label=self.aVal, style=wx.ALIGN_RIGHT)
        eValTxt = wx.StaticText(self, label=self.eVal, style=wx.ALIGN_RIGHT)
        valueSizer.Add(aValTxt, 0, wx.EXPAND|wx.ALL, 3)
        valueSizer.Add(eValTxt, 0, wx.EXPAND|wx.ALL, 3)

        # source
        sourceSizer = wx.BoxSizer(wx.VERTICAL)
        sourceTxt = wx.StaticText(self, label=self.source)
        sourceSizer.Add(sourceTxt, 0, wx.EXPAND|wx.ALL, 3)
        sourceSizer.Add((-1, -1), 1, wx.EXPAND)

        conflictSizer.Add(textSizer, 0, wx.EXPAND)
        conflictSizer.Add(valueSizer, 0, wx.EXPAND)
        conflictSizer.Add((3, -1), 0, wx.EXPAND)
        conflictSizer.Add(sourceSizer, 0, wx.EXPAND)


        # # Above buttons
        # aboveButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        # overwriteTxt = wx.StaticText(self, size=(-1, -1), label=self.overwriteLbl)
        # keepTxt = wx.StaticText(self, size=(-1, -1), label=self.keepLbl)
        #
        # font = wx.Font(9, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        # overwriteTxt.SetFont(font)
        # keepTxt.SetFont(font)
        #
        # aboveButtonsSizer.Add(overwriteTxt, 0, wx.EXPAND|wx.ALL, 3)
        # aboveButtonsSizer.Add((-1, -1), 1, wx.EXPAND)
        # aboveButtonsSizer.Add(keepTxt, 0, wx.EXPAND|wx.ALL, 3)


        # Select and Cancel buttons
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.overwriteButton = wx.Button(self, label=self.overwriteButtonLbl)
        self.keepButton = wx.Button(self, label=self.keepButtonLbl)
        buttonSizer.Add(self.overwriteButton, 0, wx.EXPAND|wx.ALL, 3)
        buttonSizer.Add((-1, -1), 1, wx.EXPAND)
        buttonSizer.Add(self.keepButton, 0, wx.EXPAND|wx.ALL, 3)

        self.overwriteButton.Bind(wx.EVT_BUTTON, self.Overwrite)
        self.keepButton.Bind(wx.EVT_BUTTON, self.Keep)
        self.keepButton.SetFocus()
        self.keepButton.SetDefault()

        # Add to Sizer
        layoutSizer.Add(headerTxt, 0, wx.EXPAND|wx.ALL, 5)
        layoutSizer.Add((10, -1), 0, wx.EXPAND)
        layoutSizer.Add(conflictSizer, 0, wx.EXPAND|wx.ALL, 10)
        layoutSizer.Add((-1, -1), 1, wx.EXPAND)
        # layoutSizer.Add(aboveButtonsSizer, 1, wx.EXPAND)
        layoutSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        layoutSizer.Add(buttonSizer, 0, wx.EXPAND)

        self.SetSizer(layoutSizer)


    def Overwrite(self, evt):
        self.EndModal(wx.ID_YES)
        self.Show()

    def Keep(self, evt):
        self.EndModal(wx.ID_CANCEL)


ID_HG = wx.NewId()
ID_HG2 = wx.NewId()
ID_WL1 = wx.NewId()
ID_WL2 = wx.NewId()

class DuplicateMGHUpload(wx.Dialog):


    def __init__(self, mode, hg, hg2, wl1, wl2, *args, **kwargs):
        super(DuplicateMGHUpload, self).__init__(*args, **kwargs)

        self.mode = mode

        self.descLbl = "Duplicated MGH detected, please select one from the following to upload"
        self.hgBtnLbl = "HG"
        self.hg2BtnLbl = "HG2"
        self.wl1BtnLbl = "WL1"
        self.wl2BtnLbl = "WL2"
        self.buttonSize = (100, 50)


        self.InitUI(hg, hg2, wl1, wl2)

    def InitUI(self, hg, hg2, wl1, wl2):
        if self.mode == "DEBUG":
            print "Duplicate MGH Upload Dialog"


        mySizer = wx.BoxSizer(wx.VERTICAL)

        descTxt = wx.StaticText(self, label=self.descLbl, size=(350, 100))
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        descTxt.SetFont(font)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        hgBtn = wx.Button(self, label=self.hgBtnLbl, id=ID_HG, size=self.buttonSize)
        hgBtn.Hide()
        hg2Btn = wx.Button(self, label=self.hg2BtnLbl, id=ID_HG2, size=self.buttonSize)
        hg2Btn.Hide()
        wl1Btn = wx.Button(self, label=self.wl1BtnLbl, id=ID_WL1, size=self.buttonSize)
        wl1Btn.Hide()
        wl2Btn = wx.Button(self, label=self.wl2BtnLbl, id=ID_WL2, size=self.buttonSize)
        wl2Btn.Hide()


        hgBtn.Bind(wx.EVT_BUTTON, self.OnHG)
        hg2Btn.Bind(wx.EVT_BUTTON, self.OnHG2)
        wl1Btn.Bind(wx.EVT_BUTTON, self.OnWL1)
        wl2Btn.Bind(wx.EVT_BUTTON, self.OnWL2)


        if hg:
            buttonSizer.Add(hgBtn, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
            hgBtn.Show()
        elif hg2:
            buttonSizer.Add(hg2Btn, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
            hg2Btn.Show()
        if wl1:
            buttonSizer.Add(wl1Btn, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
            wl1Btn.Show()
        if wl2:
            buttonSizer.Add(wl2Btn, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
            wl2Btn.Show()


        mySizer.Add(descTxt, 1, wx.EXPAND|wx.ALL, 20)
        mySizer.Add(buttonSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 20)

        self.SetSizer(mySizer)


    def OnHG(self, evt):
        self.EndModal(ID_HG)

    def OnHG2(self, evt):
        self.EndModal(ID_HG2)

    def OnWL1(self, evt):
        self.EndModal(ID_WL1)

    def OnWL2(self, evt):
        self.EndModal(ID_WL2)




class AquariusConflictMGHDialog(wx.Dialog):
    def __init__(self, mode, manager, HG, WLR, paramName, *args, **kwargs):
        super(AquariusConflictMGHDialog, self).__init__(*args, **kwargs)
        self.manager = manager
        self.mode = mode
        self.HG = HG
        self.WLR = WLR
        self.paramName = paramName


        self.Title = "Duplicate MGH"
        self.headerLbl = "Duplicate Detected for " + paramName
        # self.bodyLbl = "A value of " + str(self.aVal) + " for " + \
        #                 self.paramName + " is detected in FVT. Would you like to Overwrite this value with the eHSN value of " + str(self.eVal) + " (source: "\
        #                 + self.source + ")?"

        self.aquariusFVTLbl = "Weighted M.G.H. from HG: "
        self.ehsnLbl = "Weighted M.G.H. from Water Level Reference: "

        # self.overwriteLbl = "Overwrite FVT value with eHSN value"
        # self.keepLbl = "Keep FVT value"
        self.overwriteButtonLbl = "HG"
        self.keepButtonLbl = "Water Level Reference"

        self.sizeWidth = 360
        self.sizeHeight = 180
        self.SetSize((self.sizeWidth, self.sizeHeight))

        self.InitUI()


    def InitUI(self):
        if self.mode == "DEBUG":
            print "Aquarius Multiple Discharge Upload Dialog"

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        headerTxt = wx.StaticText(self, size=(-1, 25), label=self.headerLbl)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        headerTxt.SetFont(font)

        # bodyTxt = wx.StaticText(self, size=(-1, 45), label=self.bodyLbl)
        # headerTxt.Wrap(self.sizeWidth)
        # font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        # headerTxt.SetFont(font)

        # Display Values
        conflictSizer = wx.BoxSizer(wx.HORIZONTAL)

        # labels
        textSizer = wx.BoxSizer(wx.VERTICAL)
        aqTxt = wx.StaticText(self, label=self.aquariusFVTLbl, style=wx.ALIGN_RIGHT)
        ehsnTxt = wx.StaticText(self, label=self.ehsnLbl, style=wx.ALIGN_RIGHT)
        textSizer.Add(aqTxt, 0, wx.EXPAND|wx.ALL, 3)
        textSizer.Add(ehsnTxt, 0, wx.EXPAND|wx.ALL, 3)

        # values
        valueSizer = wx.BoxSizer(wx.VERTICAL)
        aValTxt = wx.StaticText(self, label=self.WLR, style=wx.ALIGN_RIGHT)
        eValTxt = wx.StaticText(self, label=self.HG, style=wx.ALIGN_RIGHT)
        valueSizer.Add(aValTxt, 0, wx.EXPAND|wx.ALL, 3)
        valueSizer.Add(eValTxt, 0, wx.EXPAND|wx.ALL, 3)



        conflictSizer.Add(textSizer, 0, wx.EXPAND)
        conflictSizer.Add(valueSizer, 0, wx.EXPAND)
        conflictSizer.Add((3, -1), 0, wx.EXPAND)



        # # Above buttons
        # aboveButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        # overwriteTxt = wx.StaticText(self, size=(-1, -1), label=self.overwriteLbl)
        # keepTxt = wx.StaticText(self, size=(-1, -1), label=self.keepLbl)
        #
        # font = wx.Font(9, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        # overwriteTxt.SetFont(font)
        # keepTxt.SetFont(font)
        #
        # aboveButtonsSizer.Add(overwriteTxt, 0, wx.EXPAND|wx.ALL, 3)
        # aboveButtonsSizer.Add((-1, -1), 1, wx.EXPAND)
        # aboveButtonsSizer.Add(keepTxt, 0, wx.EXPAND|wx.ALL, 3)


        # Select and Cancel buttons
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.overwriteButton = wx.Button(self, label=self.overwriteButtonLbl)
        self.keepButton = wx.Button(self, label=self.keepButtonLbl)
        buttonSizer.Add(self.overwriteButton, 0, wx.EXPAND|wx.ALL, 3)
        buttonSizer.Add((-1, -1), 1, wx.EXPAND)
        buttonSizer.Add(self.keepButton, 0, wx.EXPAND|wx.ALL, 3)

        self.overwriteButton.Bind(wx.EVT_BUTTON, self.Overwrite)
        self.keepButton.Bind(wx.EVT_BUTTON, self.Keep)
        self.keepButton.SetFocus()
        self.keepButton.SetDefault()

        # Add to Sizer
        layoutSizer.Add(headerTxt, 0, wx.EXPAND|wx.ALL, 5)
        layoutSizer.Add((10, -1), 0, wx.EXPAND)
        layoutSizer.Add(conflictSizer, 0, wx.EXPAND|wx.ALL, 10)
        layoutSizer.Add((-1, -1), 1, wx.EXPAND)
        # layoutSizer.Add(aboveButtonsSizer, 1, wx.EXPAND)
        layoutSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        layoutSizer.Add(buttonSizer, 0, wx.EXPAND)

        self.SetSizer(layoutSizer)


    def Overwrite(self, evt):
        self.EndModal(wx.ID_YES)
        self.Show()

    def Keep(self, evt):
        self.EndModal(wx.ID_CANCEL)





def main():
    app = wx.App()



    AUD = DuplicateMGHUpload("DEBUG", False, True, False, True,parent=None)

    AUD.Show()

    # # AUD = AquariusMultDisUploadDialog("DEBUG", None, ["2016-05-17 activity started at: 09:01:01", "2016-05-17 activity started at: 17:21:33"], None, title="Upload Field Visit to Aquarius")
    # # AUD = AquariusConflictUploadDialog("DEBUG", None, "20 m", "21.3 m", "M.G.H", "eHSN v1.1.3", None, title="Upload Field Visit to Aquarius")
    # AUD.Show()
    # val = True
    # while val:
    #     re = AUD.ShowModal()
    #     if re == wx.ID_YES:
    #         print "YES"
    #     else:
    #         print "Cancel"
    #         val = False
    #         AUD.Destroy()

    # print "TEST"

    # AUD.Destroy()

    app.MainLoop()

if __name__ == '__main__':
    main()
