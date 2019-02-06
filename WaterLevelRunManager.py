# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from WaterLevelRunPanel import *
from WaterLevelNoteTransferDialog import *


class WaterLevelRunManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        self.emptyLNMessage = "You should check at least one Station/BM in the Level Notes table!"
        self.emptyDWLMessage = "You should check at least one Water Level Reference Point in the Direct water Level calculation table !"
        self.mode = mode


        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "WaterLevelRunControl"


    def GetBMs(self):
        return self.gui.BMs

    @property
    def levelNotes(self):
        return self.gui.levelNotes

    @levelNotes.setter
    def levelNotes(self, levelNotes):
        self.gui.levelNotes = levelNotes

    def GetSubRunPanel(self, index):
        return self.levelNotes.runSizer.GetItem(index).GetWindow()


    @property
    def runSizer(self):
        return self.levelNotes.runSizer

    @runSizer.setter
    def runSizer(self, runSizer):
        self.levelNotes.runSizer = runSizer


    def GetClosurePanel(self, index):
        return self.levelNotes.GetClosurePanel(index)

    def GetClosureButton(self, index):
        return self.levelNotes.GetClosureButton(index)

    def GetClosureText(self, index):
        return self.levelNotes.GetClosureText(index)


    def GetUploadCheckBox(self, index):
        return self.levelNotes.GetUploadCheckBox(index)

    def GetRemoveRunButton(self, index):
        return self.levelNotes.GetRemoveRunButton(index)



    def GetRunEntryNumber(self, run):
        return self.levelNotes.GetRunEntryNumber(run)

    def GetNumberOfRuns(self):
        return self.levelNotes.GetNumberOfRuns()



    def GetTransferSizer(self):
        return self.levelNotes.GetTransferSizer()

    def GetLevelNotesSizerV(self, run):
        return self.levelNotes.GetLevelNotesSizerV(run)

    def GetLevelNotesRowSizer(self, run, row):
        return self.levelNotes.GetRowSizer(run, row)





    #Return the button for specific circuit and row number:
    def GetLevelNotesButton(self, run, row):
        return self.levelNotes.GetButton(run, row)




    #Return the station for specific circuit and row number:
    def GetLevelNotesStation(self, run, row):

        return self.levelNotes.GetStation(run, row)



    #Return the backsight for specific circuit and row number:
    def GetLevelNotesBacksight(self, run, row):
        return self.levelNotes.GetBacksight(run, row)



    #Return the HI for specific circuit and row number:
    def GetLevelNotesHI(self, run, row):
        return self.levelNotes.GetHI(run, row)




    #Return the foresight for specific circuit and row number:
    def GetLevelNotesForesight(self, run, row):
        return self.levelNotes.GetForesight(run, row)



    #Return the elevation for specific circuit and row number:
    def GetLevelNotesElevation(self, run, row):
        return self.levelNotes.GetElevation(run, row)



    #Return the checkbox for specific circuit and row number:
    def GetLevelNotesEstablishCheckbox(self, run, row):
        return self.levelNotes.GetEstablishCheckbox(run, row)

    #Return the checkbox for specific circuit and row number:
    def GetLevelNotesElevationCheckbox(self, run, row):
        return self.levelNotes.GetElevationCheckbox(run, row)



    #Return the Established Elevation for specific circuit and row number:
    def GetLevelNotesEstablishedElevation(self, run, row):
        return self.levelNotes.GetEstablishedElevation(run, row)

    #Return the Established Elevation Button for specific circuit and row number:
    def GetEstablishedElevationBtn(self, run, row):
        return self.levelNotes.GetEstablishedElevationBtn(run, row)

    #Return the comments for specific circuit and row number:
    def GetLevelNotesComments(self, run, row):
        return self.levelNotes.GetComments(run, row)








    def OnTransferToSummary(self):
        find = False
        stations = []
        elevations = []
        establishedEles = []
        closures = []
        for circuitIndex, circuit in enumerate(self.runSizer.GetChildren()):
            stationList = []
            elevationList = []
            establishedEleList = []

            stations.append(stationList)
            elevations.append(elevationList)
            establishedEles.append(establishedEleList)

            closures.append(self.GetClosureText(circuitIndex).GetValue())

            for rowIndex, row in enumerate(self.GetLevelNotesSizerV(circuitIndex).GetChildren()):

                if rowIndex < len(self.GetLevelNotesSizerV(circuitIndex).GetChildren()) - 1:
                    ckbox1 = self.GetLevelNotesEstablishCheckbox(circuitIndex, rowIndex)
                    ckbox2 = self.GetLevelNotesElevationCheckbox(circuitIndex, rowIndex)
                    
                    if bool(ckbox1.GetValue()) or bool(ckbox2.GetValue()):
                        find = True
                        station = self.GetLevelNotesStation(circuitIndex, rowIndex).GetValue()
                        elevation = self.GetLevelNotesElevation(circuitIndex, rowIndex).GetValue()
                        establishedEle = self.GetLevelNotesEstablishedElevation(circuitIndex, rowIndex).GetValue()
                        stationList.append(station)
                        elevationList.append(elevation)
                        establishedEleList.append(establishedEle)
                        # if station != '' and elevation != '':
                        self.AddSummaryEntry()
                        index = len(self.wleValSizer.GetChildren()) - 1
                        self.SetWLRefVal(index, station)
                        if bool(ckbox1.GetValue()):
                            self.SetElevationVal(index, establishedEle)
                        else:
                            self.SetElevationVal(index, elevation)
        if len(stations) > 0 and find:

            td = TransferDialog(stations, elevations, establishedEles, closures, self.gui, size=(-1, 400), style=wx.RESIZE_BORDER|wx.CLOSE_BOX|wx.CAPTION)
            td.ShowModal()
            
        if not find:
            dlg = wx.MessageDialog(self.gui, self.emptyLNMessage, 'None', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
        # self.gui.levelNotes.UncheckAll()




    #Enable or disable the row by givin row and index
    def EnableEntry(self, run, row, enable):
        self.levelNotes.EnableEntry(run, row, enable)

    #Add a circuit to Level Notes panel
    def AddRun(self):
        self.levelNotes.AddRun()

    #Remove a circuit from level notes panel by index number
    def RemoveRun(self, index):
        self.levelNotes.RemoveRun(index)

    #Add an entry to circuit by index number
    def AddEntry(self, index):
        self.levelNotes.AddEntry(index)

    #remove an entry from a circuit by index numbers
    def RemoveEntry(self, runIndex, entryIndex):
        self.levelNotes.RemoveEntry(runIndex, entryIndex)

    #return true or false vale base on if the checkbox is checked or not
    def UploadIsChecked(self, index):
        return self.GetUploadCheckBox(index).IsChecked()
    
    #Add an entry for summary panel
    def AddSummaryEntry(self):
        self.gui.AddEntry()



    #Time Val Sizer
    @property
    def timeValSizer(self):
        return self.gui.timeValSizer

    @timeValSizer.setter
    def timeValSizer(self, timeValSizer):
        self.gui.timeValSizer = timeValSizer

    #Time Val Getter
    def GetTimeVal(self, row):
        return self.gui.GetTimeVal(row)
    
    #Time Val Setter
    def SetTimeVal(self, row, val):
        self.gui.SetTimeVal(row, val)
    
    #select sizer
    @property
    def selectSizer(self):
        return self.gui.selectSizer

    #select CheckBox
    def GetSelectCheckbox(self, row):
        return self.gui.GetCheckbox(row)

    def SetSelectCheckbox(self, row, val):
        self.GetSelectCheckbox(row).SetValue(val)
    

    #WLRef Sizer
    @property
    def WLRefValSizer(self):
        return self.gui.WLRefValSizer

    @WLRefValSizer.setter
    def WLRefValSizer(self, WLRefValSizer):
        self.gui.WLRefValSizer = WLRefValSizer

    #WLRef Val Getter
    def GetWLRefVal(self, row):
        return self.gui.GetWLRefVal(row)

    #WLRef Val Setter
    def SetWLRefVal(self, row, val):
        self.gui.SetWLRefVal(row, val)
    

    #Elevation Sizer
    @property
    def elevationValSizer(self):
        return self.gui.elevationValSizer

    @elevationValSizer.setter
    def elevationValSizer(self, elevationValSizer):
        self.gui.elevationValSizer = elevationValSizer

    #Elevation Val Getter
    def GetElevationVal(self, row):
        return self.gui.GetElevationVal(row)

    #Elevation Val Setter
    def SetElevationVal(self, row, val):
        self.gui.SetElevationVal(row, val)
    

    #DtWS Sizer
    @property
    def DtWSValSizer(self):
        return self.gui.DtWSValSizer

    @DtWSValSizer.setter
    def DtWSValSizer(self, DtWSValSizer):
        self.gui.DtWSValSizer = DtWSValSizer

    #DtWS Val Getter
    def GetDtWSVal(self, row):
        return self.gui.GetDtWSVal(row)

    #DtWS Val Setter
    def SetDtWSVal(self, row, val):
        self.gui.SetDtWSVal(row, val)


    #Surge Sizer
    @property
    def surgeValSizer(self):
        return self.gui.surgeValSizer

    @surgeValSizer.setter
    def surgeValSizer(self, surgeValSizer):
        self.gui.surgeValSizer = surgeValSizer

    #Surge Val Getter
    def GetSurgeVal(self, row):
        return self.gui.GetSurgeVal(row)

    #Surge Val Setter
    def SetSurgeVal(self, row, val):
        self.gui.SetSurgeVal(row, val)
    

    #WLElev Sizer
    @property
    def wleValSizer(self):
        return self.gui.wleValSizer

    @wleValSizer.setter
    def wleValSizer(self, wleValSizer):
        self.gui.wleValSizer = wleValSizer

    #WLElev Val Getter
    def GetWLElevVal(self, row):
        return self.gui.GetWLElevVal(row)

    #WLElev Val Setter
    def SetWLElevVal(self, row, val):
        self.gui.SetWLElevVal(row, val)

        
    #Datum Sizer
    @property
    def datumValSizer(self):
        return self.gui.datumValSizer

    @datumValSizer.setter
    def datumValSizer(self, datumValSizer):
        self.gui.datumValSizer = datumValSizer

    #Datum Val Getter
    def GetDatumVal(self, row):
        return self.gui.GetDatumVal(row)

    #Datum Val Setter
    def SetDatumVal(self, row, val):
        self.gui.SetDatumVal(row, val)
        
    #CorrectedWaterLevel Sizer
    @property
    def cwlValSizer(self):
        return self.gui.cwlValSizer

    @cwlValSizer.setter
    def cwlValSizer(self, cwlValSizer):
        self.gui.cwlValSizer = cwlValSizer

    #CorrectedWaterLevel Val Getter
    def GetCwlVal(self, row):
        return self.gui.GetCwlVal(row)

    #CorrectedWaterLevel Val Setter
    def SetCwlVal(self, row, val):
        self.gui.SetCwlVal(row, val)
        
        
        
    #LoggerReading Sizer
    @property
    def loggerValSizer(self):
        return self.gui.loggerValSizer

    @loggerValSizer.setter
    def loggerReadingValSizer(self, loggerValSizer):
        self.gui.loggerValSizer = loggerValSizer

    #LoggerReading Val Getter
    def GetLoggerReadingVal(self, row):
        return self.gui.GetLoggerReadingVal(row)

    #LoggerReading Val Setter
    def SetLoggerReadingVal(self, row, val):
        self.gui.SetLoggerReadingVal(row, val)



    #LoggerReading Sizer2
    @property
    def loggerValSizer2(self):
        return self.gui.loggerValSizer



    #LoggerReading Val Getter
    def GetLoggerReadingVal2(self, row):
        return self.gui.GetLoggerReadingVal2(row)

    #LoggerReading Val Setter
    def SetLoggerReadingVal2(self, row, val):
        self.gui.SetLoggerReadingVal2(row, val)




        

    #Comments Value
    @property
    def commentsCtrl(self):
        return self.gui.commentsCtrl.GetValue()

    @commentsCtrl.setter
    def commentsCtrl(self, commentsCtrl):
        self.gui.commentsCtrl.SetValue(commentsCtrl)

    #CompletedBy Value
    @property
    def completedByCtrl(self):
        return self.gui.completedByCtrl.GetValue()

    @completedByCtrl.setter
    def completedByCtrl(self, completedByCtrl):
        self.gui.completedByCtrl.SetValue(completedByCtrl)


    #Return HG name header
    @property
    def HGHeaderCtrl(self):
        return self.gui.GetHG().GetValue()

    @HGHeaderCtrl.setter
    def HGHeaderCtrl(self, val):
        self.gui.GetHG().SetValue(val)

    #Return HG2 name header
    @property
    def HG2HeaderCtrl(self):
        return self.gui.GetHG2().GetValue()

    @HG2HeaderCtrl.setter
    def HG2HeaderCtrl(self, val):
        self.gui.GetHG2().SetValue(val)

    #Get the levelling type (convention or total station)
    @property
    def LevelnoteType(self):
        return self.gui.levelNotes.type

    @LevelnoteType.setter
    def LevelnoteType(self, val):
        self.gui.levelNotes.type = val


    #Find the matching pairs by station name for level notes
    def FindMatchBM(self, parent):
        self.levelNotes.FindMatchBM(parent)

    #Return a list including all selected index number
    def GetSelectedList(self):
        resultList = []
        for i, item in enumerate(self.selectSizer.GetChildren()):
            if item.GetWindow().IsChecked():
                resultList.append(i)
        return resultList
        
    #transfer selected WL and logger value to stage measurement on front page
    def TransferToStageMeasurement(self, time=None, logger1=None, logger2=None, wl1=None, wl2=None):
        self.manager.stageMeasManager.InsertEmptyEntry(0, time, logger1, logger2, wl1, wl2)


    #Return the set of selected WL Reference name without duplicate, without empty string
    def GetSelectedWLRNames(self):
        wlList = []
        selected = self.GetSelectedList()
        for i in range(len(self.WLRefValSizer.GetChildren())):
            if i in selected:
                if self.GetWLRefVal(i) != "":
                    wlList.append(self.GetWLRefVal(i))
        return list(set(wlList))


    #Creating a toaster box message after transfer
    def CreateToasterBox(self, parent, msg, second, color, size):
        self.gui.levelNotes.CreateToasterBox(parent, msg, second, color, size)


    #Checking all selected entries with a time value
    #return false if any selected entry without a timestamp
    def TimeCheck(self):
        for time in self.timeValSizer.GetChildren():
            if self.GetSelectCheckbox(int(time.GetWindow().GetName())).IsChecked():
                if time.GetWindow().GetHourVal() == "" or time.GetWindow().GetMinuteVal() == "":
                    return False
        return True

    #If any upload checkbox is checked then return True 
    def IsUploaded(self):
        return self.gui.levelNotes.IsUploaded()

    def IsEmpty(self):
        return self.gui.levelNotes.IsEmpty()


    def GetRb1(self):
        return self.gui.rb1
    def GetRb2(self):
        return self.gui.rb2

    def GetHgText(self):
        return self.gui.hgText
    def GetHgText2(self):
        return self.gui.hgText2
    def GetCommentsCtrl(self):
        return self.gui.commentsCtrl
    def GetCompletedByCtrl(self):
        return self.gui.completedByCtrl

        
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 800))
    WaterLevelRunManager("DEBUG", WaterLevelRunPanel("DEBUG", wx.LANGUAGE_ENGLISH, frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
