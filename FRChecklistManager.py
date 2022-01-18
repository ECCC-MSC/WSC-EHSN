# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from FRChecklistPanel import *

class FRChecklistManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def onInstrumentType(self, val):
        self.gui.onInstrumentType(val)
        
    def Init(self):
        if self.mode == "DEBUG":
            print("FRChecklistControl")

    def PrintProperties(self):
        print(self.depType)
        print(self.midsecType)

    def changeDepType(self, depType):
        self.gui.changeDepType(depType)

    #PassCB
    @property
    def passCB(self):
        return self.gui.passCB.GetValue()

    @passCB.setter
    def passCB(self, passCB):
        self.gui.passCB.SetValue(passCB)

    #Deployment Type
    @property
    def depType(self):
        return self.gui.depTypeLbl.GetLabel()

    @depType.setter
    def depType(self, depType):
        self.gui.depTypeLbl.SetLabel(depType)
        self.changeDepType(depType)


    #Midsection Type
    @property
    def midsecType(self):
        return self.gui.midsecTypeCtrl.GetValue()

    @midsecType.setter
    def midsecType(self, midsecType):
        self.gui.midsecTypeCtrl.SetValue(midsecType)
        self.gui.onMidsecTypeChange()


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


    #cbCheckSizer
    @property
    def cbCheckSizer(self):
        return self.gui.cbCheckSizer

    @cbCheckSizer.setter
    def cbCheckSizer(self, cbCheckSizer):
        self.gui.cbCheckSizer = cbCheckSizer
        
    #GetCBRowValue
    def GetCBCheckSizerVal(self, row):
        maxrow = len(self.cbCheckSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.cbCheckSizer.GetItem(row).GetWindow()
        return sizerItem.GetValue()
        
    #SetCBRowValue
    def SetCBCheckSizerVal(self, row, val):
        maxrow = len(self.cbCheckSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.cbCheckSizer.GetItem(row).GetWindow()
        sizerItem.SetValue(val)


    #cbRevSizer
    @property
    def cbRevSizer(self):
        return self.gui.cbRevSizer

    @cbRevSizer.setter
    def cbRevSizer(self, cbRevSizer):
        self.gui.cbRevSizer = cbRevSizer
        
    #GetCBRowValue
    def GetCBRevSizerVal(self, row):
        maxrow = len(self.cbRevSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.cbRevSizer.GetItem(row).GetWindow()
        return sizerItem.GetValue()
        
    #SetCBRowValue
    def SetCBRevSizerVal(self, row, val):
        maxrow = len(self.cbRevSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1

        sizerItem = self.cbRevSizer.GetItem(row).GetWindow()
        sizerItem.SetValue(val)
        

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
    def siteNotesCtrl(self):
        return self.gui.siteNotesCtrl.GetValue()

    @siteNotesCtrl.setter
    def siteNotesCtrl(self, siteNotesCtrl):
        self.gui.siteNotesCtrl.SetValue(siteNotesCtrl)

    #Notes on Next Trip
    @property
    def planNotesCtrl(self):
        return self.gui.planNotesCtrl.GetValue()

    @planNotesCtrl.setter
    def planNotesCtrl(self, planNotesCtrl):
        self.gui.planNotesCtrl.SetValue(planNotesCtrl)

    # def GetPicturedCkbox(self):
    #     return self.gui.picturedCkbox.IsChecked()

    # def SetPicturedCkbox(self, val):
    #     self.gui.picturedCkbox.SetValue(val)



    def GetSiteNotesCtrl(self):
        return self.gui.siteNotesCtrl
    def GetPlanNotesCtrl(self):
        return self.gui.planNotesCtrl

    # def GetPicturedCkbox(self):
    #     return self.gui.picturedCkbox


    

        
                       
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(780, 700))
    FRChecklistManager("DEBUG", FRChecklistPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()
    
    app.MainLoop()

if __name__ == '__main__':
    main()
