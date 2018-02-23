import wx
import wx.lib.masked as masked
import wx.lib.scrolledpanel as scrolledpanel
import os
import sys

class UserConfigPanel(wx.Panel):
    def __init__(self, mode, lang, *args, **kwargs):
        super(UserConfigPanel, self).__init__(*args, **kwargs)

        self.stationNumLbl = 'Station Number'
        self.stationNameLbl = 'Station Name'
        self.saveLbl = 'Save'
        self.openLbl = 'Open'
        self.stationTitLbl = 'STATIONS'
        self.stationSaveTitle = 'Save stations'
        self.fileOpenTitle = 'Open stations'

        self.entryNum = 0
        self.rowHeight = 30

        self.stations = None

        self.mode=mode
        self.manager = None

        self.lang = lang
        self.InitUI()




    def InitUI(self):
        if self.mode=="DEBUG":
            print "In StationConfigPanel"


        self.layoutSizerV = wx.BoxSizer(wx.VERTICAL)


        

        self.subPanel1 = wx.Panel(self, style=wx.SIMPLE_BORDER)
        self.subPanel2 = wx.Panel(self, style=wx.SIMPLE_BORDER)

        self.subLayoutSizerH1 = wx.BoxSizer(wx.HORIZONTAL)
        self.subLayoutSizerH2 = wx.BoxSizer(wx.HORIZONTAL)

        self.subPanel1.SetSizer(self.subLayoutSizerH1)
        self.subPanel2.SetSizer(self.subLayoutSizerH2)


        self.subLayoutSizerV1 = wx.BoxSizer(wx.VERTICAL)
        self.subLayoutSizerV2 = wx.BoxSizer(wx.VERTICAL)
        self.subLayoutSizerV3 = wx.BoxSizer(wx.VERTICAL)
        self.subLayoutSizerV4 = wx.BoxSizer(wx.VERTICAL)

        self.layoutSizerV.Add(self.subPanel1, 1, wx.EXPAND)
        self.layoutSizerV.Add(self.subPanel2, 1, wx.EXPAND)


        #Station Panel
        self.stationScrollPanel = scrolledpanel.ScrolledPanel(self.subPanel1, size=(-1, 200), style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.stationScrollPanel.SetBackgroundColour('#FDDF99')
        self.stationScrollPanel.SetupScrolling()
        self.stationScrollPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)



        #1 Panel
        self.temScrollPanel1 = scrolledpanel.ScrolledPanel(self.subPanel1, size=(-1, 200), style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.temScrollPanel1.SetupScrolling()
        self.temScrollPanel1.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        #1 Panel
        self.temScrollPanel2 = scrolledpanel.ScrolledPanel(self.subPanel2, size=(-1, 200), style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.temScrollPanel2.SetupScrolling()
        self.temScrollPanel2.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        #1 Panel
        self.temScrollPanel3 = scrolledpanel.ScrolledPanel(self.subPanel2, size=(-1, 200), style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.temScrollPanel3.SetupScrolling()
        self.temScrollPanel3.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)


        stationSizerV = wx.BoxSizer(wx.VERTICAL)
        stationSizerH = wx.BoxSizer(wx.HORIZONTAL)
        

        #Station Title
        stationTitlePanel = wx.Panel(self.stationScrollPanel, size=(-1, self.rowHeight), style=wx.SIMPLE_BORDER)
        stationTitlePanel.SetBackgroundColour('#D7D0D0')
        stationTitleSizerH = wx.BoxSizer(wx.HORIZONTAL)
        stationTitlePanel.SetSizer(stationTitleSizerH)
        self.stationTitleText = wx.StaticText(stationTitlePanel, label=self.stationTitLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        stationTitleSizerH.Add(self.stationTitleText,1,wx.EXPAND)




        #Entry Adding Column
        self.entryColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.entryColumnPanel = wx.Panel(self.stationScrollPanel, style=wx.BORDER_NONE, size=(self.rowHeight, -1))
        
        entryColPanel = wx.Panel(self.entryColumnPanel, style=wx.SIMPLE_BORDER)
        wx.StaticText(entryColPanel, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.rowHeight, self.rowHeight))
        
        #For dynamically added entries
        self.entryColButtonPanel = wx.Panel(self.entryColumnPanel, style=wx.SIMPLE_BORDER)
        self.entryColButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.entryColButtonPanel.SetSizer(self.entryColButtonSizer)
        
        #Add a default button
        name = "%s" % self.entryNum
        button = wx.Button(self.entryColButtonPanel, id=10101+self.entryNum, label="+", name=name, size=(self.rowHeight, self.rowHeight))
        self.entryNum += 1
        button.Bind(wx.EVT_BUTTON, self.OnAddPress)
        self.entryColButtonSizer.Add(button, 0, wx.EXPAND)

        self.entryColumnSizer.Add(entryColPanel, 0, wx.EXPAND)
        self.entryColumnSizer.Add(self.entryColButtonPanel, 0, wx.EXPAND)
        self.entryColumnPanel.SetSizer(self.entryColumnSizer)


        font = wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.BOLD)


        #Station Number Column
        self.stationNumColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.stationNumColumnPanel = wx.Panel(self.stationScrollPanel, style=wx.BORDER_NONE)
        
        stationNumColPanel = wx.Panel(self.stationNumColumnPanel, style=wx.SIMPLE_BORDER, size=(-1, self.rowHeight))
        stationNumColSizerV = wx.BoxSizer(wx.VERTICAL)
        stationNumColPanel.SetSizer(stationNumColSizerV)
        stationNumText = wx.StaticText(stationNumColPanel, label=self.stationNumLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        stationNumText.SetFont(font)
        stationNumColSizerV.Add(stationNumText, 1, wx.EXPAND)
        
        #For dynamically added entries
        self.stationNumColPanel = wx.Panel(self.stationNumColumnPanel, style=wx.SIMPLE_BORDER)
        self.stationNumColSizer = wx.BoxSizer(wx.VERTICAL)
        self.stationNumColPanel.SetSizer(self.stationNumColSizer)
        
        button = wx.Button(self.stationNumColumnPanel, label=self.saveLbl, size=(-1, self.rowHeight))
        button.Bind(wx.EVT_BUTTON, self.OnStationSave)

        self.stationNumColumnSizer.Add(stationNumColPanel, 0, wx.EXPAND)
        self.stationNumColumnSizer.Add(self.stationNumColPanel, 0, wx.EXPAND)
        self.stationNumColumnSizer.Add(button, 0, wx.EXPAND)
        self.stationNumColumnPanel.SetSizer(self.stationNumColumnSizer)



        #Station Name Column
        self.stationNameColumnSizer = wx.BoxSizer(wx.VERTICAL)
        self.stationNameColumnPanel = wx.Panel(self.stationScrollPanel, style=wx.BORDER_NONE)
        
        stationNameColPanel = wx.Panel(self.stationNameColumnPanel, style=wx.SIMPLE_BORDER, size=(-1, self.rowHeight))
        stationNameColSizerV = wx.BoxSizer(wx.VERTICAL)
        stationNameColPanel.SetSizer(stationNameColSizerV)
        stationNameText = wx.StaticText(stationNameColPanel, label=self.stationNameLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        stationNameText.SetFont(font)
        stationNameColSizerV.Add(stationNameText, 1, wx.EXPAND)
        
        #For dynamically added entries
        self.stationNameColPanel = wx.Panel(self.stationNameColumnPanel, style=wx.SIMPLE_BORDER)
        self.stationNameColSizer = wx.BoxSizer(wx.VERTICAL)
        self.stationNameColPanel.SetSizer(self.stationNameColSizer)
        
        self.stationOpenButton = wx.Button(self.stationNameColumnPanel, label=self.openLbl, size=(-1, self.rowHeight))
        self.stationOpenButton.Bind(wx.EVT_BUTTON, self.OnOpenPress)

        self.stationNameColumnSizer.Add(stationNameColPanel, 0, wx.EXPAND)
        self.stationNameColumnSizer.Add(self.stationNameColPanel, 0, wx.EXPAND)
        self.stationNameColumnSizer.Add(self.stationOpenButton, 0, wx.EXPAND)
        self.stationNameColumnPanel.SetSizer(self.stationNameColumnSizer)










        stationSizerH.Add(self.entryColumnPanel, 0, wx.EXPAND)
        stationSizerH.Add(self.stationNumColumnPanel, 1, wx.EXPAND)
        stationSizerH.Add(self.stationNameColumnPanel, 1, wx.EXPAND)


        self.stationScrollPanel.SetSizer(stationSizerV)


        self.subLayoutSizerH1.Add(self.stationScrollPanel, 1, wx.EXPAND)
        self.subLayoutSizerH1.Add(self.temScrollPanel1, 1, wx.EXPAND)
        self.subLayoutSizerH2.Add(self.temScrollPanel2, 1, wx.EXPAND)
        self.subLayoutSizerH2.Add(self.temScrollPanel3, 1, wx.EXPAND)


        stationSizerV.Add(stationTitlePanel, 0, wx.EXPAND) 
        stationSizerV.Add(stationSizerH, 1, wx.EXPAND)   
        self.SetSizer(self.layoutSizerV)

        self.layoutSizerV.Layout()
        self.Update()
        self.Refresh()


    def OnAddPress(self, event):    
        self.AddEntry('', '')

    def AddEntry(self, stationNumber, stationName):
        #Button col
        name = "%s" % self.entryNum
        otherName = "%s" % (self.entryNum - 1)
        button = wx.Button(self.entryColButtonPanel, id=10101+self.entryNum, label="+", name=name, size=(self.rowHeight, self.rowHeight))

        oldButton = self.entryColButtonSizer.GetItem(self.entryNum-1).GetWindow()
        oldButton.SetLabel('-')
        oldButton.Bind(wx.EVT_BUTTON, self.OnRemovePress)
        
        self.entryNum += 1
        button.Bind(wx.EVT_BUTTON, self.OnAddPress)
        self.entryColButtonSizer.Add(button, 0, wx.EXPAND)

        if self.mode=="DEBUG":
            print name


        #Station Number col
        stationNumCtrl = wx.TextCtrl(self.stationNumColPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(-1, self.rowHeight), name=otherName)
        stationNumCtrl.SetBackgroundColour('#F2EBEB')
        stationNumCtrl.SetValue(stationNumber)
        self.stationNumColSizer.Add(stationNumCtrl, 0, wx.EXPAND)
        stationNumCtrl.Bind(wx.EVT_TEXT, self.OnTextType)

        #Station Name col
        stationNameCtrl = wx.TextCtrl(self.stationNameColPanel, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE, size=(-1, self.rowHeight), name=otherName)
        stationNameCtrl.SetValue(stationName)
        self.stationNameColSizer.Add(stationNameCtrl, 0, wx.EXPAND)
        stationNameCtrl.Bind(wx.EVT_TEXT, self.OnTextType)

        self.layoutSizerV.Layout()
        self.Update()

        if self.entryNum > 4:
            self.Refresh()

    def readStationNums(self):
        self.StationNums = []
        for item in self.stationNumColSizer.GetChildren():
            self.StationNums.append(item.GetWindow().GetValue())


    def readStationNames(self):
        self.StationNames = []
        for item in self.stationNameColSizer.GetChildren():
            self.StationNames.append(item.GetWindow().GetValue())

    def SaveStations(self, name):
        if self.entryNum > 0:
            self.readStationNames()
            self.readStationNums()
            target = open(name, 'w')
            for index in range(len(self.StationNums)):
                target.write("%s\t%s\n" % (self.StationNums[index], self.StationNames[index]))


            target.close()


    # When the '-' is clicked, remove that row
    def OnRemovePress(self, e):
        #Button col stuff
        button = e.GetEventObject()
        index = int(button.GetName())
        if self.mode=="DEBUG":
            print "index %s" % index
        
        self.RemoveEntry(index)
        
    def stationsClear(self):
        if self.entryNum > 0:
            for i in range(self.entryNum - 1):
                self.RemoveEntry(0)
   

    # Delete each column's item at the index of the clicked '-' button
    # Reorder the list of entries
    def RemoveEntry(self, index):
        if self.mode=="DEBUG":
            print "remove %s" % index

        self.entryColButtonSizer.Hide(index)
        self.entryColButtonSizer.Remove(index)
        self.entryNum -= 1


        #Station Number col stuff
        self.stationNumColSizer.Hide(index)
        self.stationNumColSizer.Remove(index)

        #station Name col stuff
        self.stationNameColSizer.Hide(index)
        self.stationNameColSizer.Remove(index)

        for child in self.entryColButtonSizer.GetChildren():
            i = int(child.GetWindow().GetName())
            if i > index:
                child.GetWindow().SetName("%s" % (i - 1))  
                
        for child in self.stationNumColSizer.GetChildren():
            i = int(child.GetWindow().GetName())
            if i > index:
                child.GetWindow().SetName("%s" % (i - 1)) 

        for child in self.stationNameColSizer.GetChildren():
            i = int(child.GetWindow().GetName())
            if i > index:
                child.GetWindow().SetName("%s" % (i - 1))     


        self.layoutSizerV.Layout()
        self.Update()
        self.Refresh() 

    #convert to upper case
    def OnTextType(self, event):
        textCtr=event.GetEventObject()
        textCtr.ChangeValue(unicode.upper(textCtr.GetValue()))
        textCtr.SetInsertionPointEnd()



    def OnOpenPress(self, evt):


        fileOpenDialog = wx.FileDialog(self, self.fileOpenTitle, os.getcwd(), '',
                            'eHSN Station Config (*.txt)|*.txt',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return
        
        if self.manager is not None:
            path = fileOpenDialog.GetPath()

            if self.mode == "DEBUG":
                print "path open"
                print path
                
            if path != "":
          
                fileName = fileOpenDialog.GetFilename()
                self.stationTitleText.SetLabel(self.stationTitLbl + '\n' + path + '\\' + fileName)
                self.OpenFile(fileName)

        fileOpenDialog.Destroy()

        self.layoutSizerV.Layout()
        self.Update()
        self.Refresh() 
        return None






    def OpenFile(self, file):
        with open(file) as stations:
            lines = stations.readlines()
        self.numsRead = []
        self.namesRead = []
        for item in lines:
            items = item.split('\t')
            self.numsRead.append(items[0])
            self.namesRead.append(items[1].rstrip())
        self.stationsClear()
        for i in range(len(lines)):
            self.AddEntry(self.numsRead[i], self.namesRead[i])
        # self.manager.parent.genInfoManager.updateNumbers(numsRead)

    def OnStationSave(self, evt):

        

        fileSaveDialog = wx.FileDialog(self, self.stationSaveTitle, os.getcwd(), '',
                            'eHSN Config(*.txt)|*.txt',
                                         style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)

        if fileSaveDialog.ShowModal() == wx.ID_CANCEL:
            fileSaveDialog.Destroy()
            return wx.ID_CANCEL
        
        if self.manager is not None:
            path = fileSaveDialog.GetPath()
            fileName = fileSaveDialog.GetFilename()
            if self.mode == "DEBUG":
                print path
            # if path != "":
            #     self.manager.ExportAsXML(path)
            self.stationTitleText.SetLabel(self.stationTitLbl + '\n' + path + '\\' + fileName)
            self.SaveStations(fileName)
        fileSaveDialog.Destroy()
        self.layoutSizerV.Layout()
        self.Update()
        self.Refresh() 
        return None






def main():
    app = wx.App()

    frame = wx.Frame(None, size=(400, 400))
    UserConfigPanel("DEBUG", wx.LANGUAGE_FRENCH, frame)

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
