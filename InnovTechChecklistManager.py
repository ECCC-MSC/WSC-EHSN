# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from InnovTechChecklistPanel import *

class InnovTechChecklistManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def onMonitoringType(self, choice):
        self.gui.onMonitoringType(choice)
        
    def Init(self):
        if self.mode == "DEBUG":
            print("InnovTechTab")

    def PrintProperties(self):
        print(self.depType)
        print(self.monitoringType)

    def changeDepType(self, depType):
        self.gui.changeDepType(depType)


    #Deployment Type
    @property
    def depType(self):
        return self.gui.depTypeLbl.GetLabel()

    @depType.setter
    def depType(self, depType):
        self.gui.depTypeLbl.SetLabel(depType)
        self.changeDepType(depType)


    #Monitoring Type
    @property
    def monitoringType(self):
        return self.gui.monitoringTypeCtrl.GetValue()

    @monitoringType.setter
    def monitoringType(self, monitoringType):
        self.gui.monitoringTypeCtrl.SetValue(monitoringType)
        self.gui.onMonitoringTypeChange()


    #labelSizer
    @property
    def labelSizer(self):
        return self.gui.labelSizer

    @labelSizer.setter
    def labelSizer(self, labelSizer):
        self.gui.labelSizer = labelSizer

    #GetLabelSizerRowValue
    def GetLabelSizerVal(self, row):
        maxrow = len(self.labelSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.labelSizer.GetItem(row).GetWindow().GetSizer().GetItem(0).GetWindow()
        return sizerItem.GetLabel()

    def SetLabelSizerVal(self, row, val):
        maxrow = len(self.labelSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.labelSizer.GetItem(row).GetWindow().GetSizer().GetItem(0).GetWindow()
        sizerItem.SetLabel(val)


    #ctrlSizer
    @property
    def ctrlSizer(self):
        return self.gui.ctrlSizer

    @ctrlSizer.setter
    def ctrlSizer(self, ctrlSizer):
        self.gui.ctrlSizer = ctrlSizer
        
    #SetCBRowValue
    def GetCtrlSizerVal(self, row):
        maxrow = len(self.ctrlSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.ctrlSizer.GetItem(row).GetWindow()
        return sizerItem.GetValue()
        
    #SetCBRowValue
    def SetCtrlSizerVal(self, row, val):
        maxrow = len(self.ctrlSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.ctrlSizer.GetItem(row).GetWindow()
        sizerItem.SetValue(val)

    
    #Notes on Site Ctrl
    @property
    def notesCtrl(self):
        return self.gui.notesCtrl.GetValue()

    @notesCtrl.setter
    def notesCtrl(self, notesCtrl):
        self.gui.notesCtrl.SetValue(notesCtrl)

    def GetNotesCtrl(self):
        return self.gui.notesCtrl


                       
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(780, 700))
    InnovTechChecklistManager("DEBUG", InnovTechChecklistPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()
    
    app.MainLoop()

if __name__ == '__main__':
    main()
