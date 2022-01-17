# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from StageMeasurementsPanel import *
from pdb import set_trace


class StageMeasurementsManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "StageMeasurementsControl"

    #HG
    @property
    def stageLabelCtrl1(self):
        return self.gui.GetStageLabelCtrl1()

    @stageLabelCtrl1.setter
    def stageLabelCtrl1(self, stageLabelCtrl1):
        self.gui.SetStageLabelCtrl1(stageLabelCtrl1)

    #HG2
    @property
    def stageLabelCtrl2(self):
        return self.gui.GetStageLabelCtrl2()

    @stageLabelCtrl2.setter
    def stageLabelCtrl2(self, stageLabelCtrl2):
        self.gui.SetStageLabelCtrl2(stageLabelCtrl2)
        
    #BMLeft
    @property
    def bmLeft(self):
        return self.gui.GetBmLeft()

    @bmLeft.setter
    def bmLeft(self, bmLeft):
        self.gui.SetBmLeft(bmLeft)

    #BMRight
    @property
    def bmRight(self):
        return self.gui.GetBmRight()

    @bmRight.setter
    def bmRight(self, bmRight):
        self.gui.SetBmRight(bmRight)



    #Time Val Sizer
    @property
    def timeValSizer(self):
        return self.gui.GetTimeValSizer()

    @timeValSizer.setter
    def timeValSizer(self, timeValSizer):
        self.gui.SetTimeValSizer(timeValSizer)

    #Time Val Getter
    def GetTimeVal(self, row):

        return self.gui.GetTimeVal(row).replace(" ", "")
    
    #Time Val Setter
    def SetTimeVal(self, row, val):
        self.gui.SetTimeVal(row, val)

    def GetTimeHour(self, row):
        return self.gui.GetTimeHour(row)

    def GetTimeMinute(self, row):
        return self.gui.GetTimeMinute(row)
    

    #HG
    @property
    def stageSizer(self):
        return self.gui.GetStageSizer()

    @stageSizer.setter
    def stageSizer(self, stageSizer):
        self.gui.SetStageSizer(stageSizer)

    #HG Val Getter
    def GetHGVal(self, row):
        return self.gui.GetHGVal(row)

    #HG Val Setter
    def SetHGVal(self, row, val):
        self.gui.SetHGVal(row, val)

    #HG2
    @property
    def stageSizer2(self):
        return self.gui.GetStageSizer2()

    @stageSizer2.setter
    def stageSizer2(self, stageSizer2):
        self.gui.SetStageSizer2(stageSizer2)

    #HG2 Val Getter
    def GetHG2Val(self, row):
        return self.gui.GetHG2Val(row)

    #HG2 Val Setter
    def SetHG2Val(self, row, val):
        self.gui.SetHG2Val(row, val)
    

    #WL Col L
    @property
    def wlSubSizerL(self):
        return self.gui.GetWlSubSizerL()

    @wlSubSizerL.setter
    def wlSubSizerL(self, wlSubSizerL):
        self.gui.SetWlSubSizerL(wlSubSizerL)

    #WL Col L Getter
    def GetWLSubSizerLVal(self, row):
        return self.gui.GetWLSubSizerLVal(row)

    #WL Col L Setter
    def SetWLSubSizerLVal(self, row, val):
        self.gui.SetWLSubSizerLVal(row, val)
    

    #WL Col R
    @property
    def wlSubSizerR(self):
        return self.gui.GetWlSubSizerR()

    @wlSubSizerR.setter
    def wlSubSizerR(self, wlSubSizerR):
        self.gui.SetWlSubSizerR(wlSubSizerR)

    #WL Col R Getter
    def GetWLSubSizerRVal(self, row):
        return self.gui.GetWLSubSizerRVal(row)

    #WL Col R Setter
    def SetWLSubSizerRVal(self, row, val):
        self.gui.SetWLSubSizerRVal(row, val)

    # Surge
    @property
    def surgeSizer(self):
        return self.gui.GetSurgeSizer()

    @surgeSizer.setter
    def surgeSizer(self, surgeSizer):
        self.gui.SetSurgeSizer(surgeSizer)

    # Surge Val Getter
    def GetSurgeVal(self, row):
        return self.gui.GetSurgeVal(row)

    # Surge Val Setter
    def SetSurgeVal(self, row, val):
        self.gui.SetSurgeVal(row, val)

    #SRC col
    @property
    def srcSizer(self):
        return self.gui.GetSrcSizer()

    @srcSizer.setter
    def srcSizer(self, srcSizer):
        self.gui.SetSrcSizer(srcSizer)

    #SRC col Getter
    def GetSrcSizerVal(self, row):
        return self.gui.GetSrcSizerVal(row)

    #SRC col Setter
    def SetSrcSizerVal(self, row, val):
        self.gui.SetSrcSizerVal(row, val)

    #SRC Applied col
    @property
    def srcAppSizer(self):
        return self.gui.GetSrcAppSizer()

    @srcAppSizer.setter
    def srcAppSizer(self, srcAppSizer):
        self.gui.SetSrcAppSizer(srcAppSizer)

    #SRC Applied col Getter
    def GetSrcAppSizerVal(self, row):
        return self.gui.GetSrcAppSizerVal(row)

    #SRC Applied col Setter
    def SetSrcAppSizerVal(self, row, val):
        self.gui.SetSrcAppSizerVal(row, val)

    # #Mgh Aggregation Combobox
    # @property
    # def mghAggCombobox(self):
    #     return self.gui.mghAggCombobox.GetValue()

    # @mghAggCombobox.setter
    # def mghAggCombobox(self, val):
    #     self.gui.mghAggCombobox.SetValue(val)
    @property
    def factors(self):
        return self.gui.factors

    @factors.setter
    def factors(self, factor):
        self.gui.factors = factor

    def GetReadingTypeVal(self, row):
        return self.gui.GetReadingTypeVal(row)

    def SetReadingTypeVal(self, row, val):
        self.gui.SetReadingTypeVal(row, val)


    #Mgh Aggregation Checkbox
    def GetMghAggCheckbox(self, row):
        return self.gui.GetMghAggCheckbox(row)


    def GetMghAggCheckboxVal(self, row):
        return self.GetMghAggCheckbox(row).IsChecked()

    def SetMghAggCheckbox(self, row, val):
        if val == "True":
            self.GetMghAggCheckbox(row).SetValue(True)
        else:
            self.GetMghAggCheckbox(row).SetValue(False)


    def GetMghMethod(self):
        return self.gui.mghMethod.GetValue()

    def SetMghMethod(self, val):
        self.gui.mghMethod.SetValue(val)


    #Weight MGH x
    #MGH x HG
    @property
    def MGHHG(self):
        return self.gui.GetMGHHG()
    
    @MGHHG.setter
    def MGHHG(self, MGHHG):
        self.gui.SetMGHHG(MGHHG)

    #MGH x HG2
    @property
    def MGHHG2(self):
        return self.gui.GetMGHHG2()

    @MGHHG2.setter
    def MGHHG2(self, MGHHG2):
        self.gui.SetMGHHG2(MGHHG2)

    #MGH x WLRefL
    @property
    def MGHWLRefL(self):
        return self.gui.GetMGHWLRefL()

    @MGHWLRefL.setter
    def MGHWLRefL(self, MGHWLRefL):
        self.gui.SetMGHWLRefL(MGHWLRefL)

    #MGH x WLRefR
    @property
    def MGHWLRefR(self):
        return self.gui.GetMGHWLRefR()

    @MGHWLRefR.setter
    def MGHWLRefR(self, MGHWLRefR):
        self.gui.SetMGHWLRefR(MGHWLRefR)

    
    #SRC x
    #SRC x HG
    @property
    def SRCHG(self):
        return self.gui.GetSRCHG()

    @SRCHG.setter
    def SRCHG(self, SRCHG):
        self.gui.SetSRCHG(SRCHG)
        
    #SRC x HG2
    @property
    def SRCHG2(self):
        return self.gui.GetSRCHG2()

    @SRCHG2.setter
    def SRCHG2(self, SRCHG2):
        self.gui.SetSRCHG2(SRCHG2)



    #GC x
    #GC x HG
    @property
    def GCHG(self):
        return self.gui.GetGCHG()

    @GCHG.setter
    def GCHG(self, GCHG):
        self.gui.SetGCHG(GCHG)

    #GC x HG2
    @property
    def GCHG2(self):
        return self.gui.GetGCHG2()

    @GCHG2.setter
    def GCHG2(self, GCHG2):
        self.gui.SetGCHG2(GCHG2)

    #GC x GCWLRefL
    @property
    def GCWLRefL(self):
        return self.gui.GetGCWLRefL()

    @GCWLRefL.setter
    def GCWLRefL(self, GCWLRefL):
        self.gui.SetGCWLRefL(GCWLRefL)

    #GC x GCWLRefR
    @property
    def GCWLRefR(self):
        return self.gui.GetGCWLRefR()

    @GCWLRefR.setter
    def GCWLRefR(self, GCWLRefR):
        self.gui.SetGCWLRefR(GCWLRefR)



    #CMGH x
    #CMGH x HG
    @property
    def CMGHHG(self):
        return self.gui.GetCMGHHG()

    @CMGHHG.setter
    def CMGHHG(self, CMGHHG):
        self.gui.SetCMGHHG(CMGHHG)

    #CMGH x HG2
    @property
    def CMGHHG2(self):
        return self.gui.GetCMGHHG2()

    @CMGHHG2.setter
    def CMGHHG2(self, CMGHHG2):
        self.gui.SetCMGHHG2(CMGHHG2)

    #CMGH x WLRefL
    @property
    def CMGHWLRefL(self):
        return self.gui.GetCMGHWLRefL()

    @CMGHWLRefL.setter
    def CMGHWLRefL(self, CMGHWLRefL):
        self.gui.SetCMGHWLRefL(CMGHWLRefL)

    #CMGH x WLRefR
    @property
    def CMGHWLRefR(self):
        return self.gui.GetCMGHWLRefR()

    @CMGHWLRefR.setter
    def CMGHWLRefR(self, CMGHWLRefR):
        self.gui.SetCMGHWLRefR(CMGHWLRefR)



    @property
    def stageRemarksCtrl(self):
        return self.gui.stageRemarksCtrl.GetValue()

    @stageRemarksCtrl.setter
    def stageRemarksCtrl(self, stageRemarksCtrl):
        self.gui.stageRemarksCtrl.SetValue(stageRemarksCtrl)







    # #Is HG is the primary column for SRC and uploading 
    # @property
    # def hgButton(self):
    #     return "True" if self.gui.hgButton else "False"

    # @hgButton.setter
    # def hgButton(self, val):
    #     if val == "True":
    #         self.gui.hgButton == True
    #     else:
    #         self.gui.hgButton == False

    # #return the HG label button
    # def GetStageLabelBtn(self):
    #     return self.gui.stageLabelBtn

    # #return the HG2 label button
    # def GetStageLabelBtn2(self):
    #     return self.gui.stageLabelBtn2

    # #Set HG as primary for calculate the SRC and uploading
    # def SetToHG(self):
    #     self.GetStageLabelBtn().SetBackgroundColour('yellow')
    #     self.GetStageLabelBtn2().SetBackgroundColour((240,240,240,255))
    #     self.hgButton = True
    #     self.gui.Refresh()

    # #Set HG2 as primary for calculate the SRC and uploading
    # def SetToHG2(self):
    #     self.GetStageLabelBtn2().SetBackgroundColour('yellow')
    #     self.GetStageLabelBtn().SetBackgroundColour((240,240,240,255))
    #     self.hgButton = False
    #     self.gui.Refresh()

    #Ckeck if there is an empty row in stage measurament 
    def emptyChecking(self):
        if self.gui.entryNum == 1:
            return True
        else:

            for row in range(len(self.gui.stageSizer.GetChildren())):
                hg = True if self.GetHGVal(row) == "" else False
                hg2 = True if self.GetHG2Val(row) == "" else False
                wlr = True if self.GetWLSubSizerLVal(row) == "" else False
                wlr2 = True if self.GetWLSubSizerRVal(row) == "" else False
                if hg and hg2 and wlr and wlr2:
                    return True
            return False

    #logger time checking return true if all the time is valid
    def timeChecking(self):
        for row in range(len(self.gui.stageSizer.GetChildren())):
            # check if any data is present on the row, since empty rows don't need time
           if self.rowHasDataToUpload(row):
                # this row has data, but if it is the first row, then we don't need time either
                # since one empty row is created by default
                if row == 0 and self.gui.entryNum == 1:
                    continue
                if self.GetTimeHour(row) == '' or self.GetTimeMinute(row) == '':
                    return False
        return True

    def rowHasMeasurement(self, row):
        return self.gui.rowHasMeasurement(row)

    def rowHasDataToUpload(self, row):
        return self.gui.rowHasDataToUpload(row)

    def InsertEmptyEntry(self, index, time=None, logger1=None, logger2=None, wl1=None, wl2=None, surge=None):
        self.gui.InsertEmptyEntry(index, time, logger1, logger2, wl1, wl2, surge)
    #return the mean time
    def CalculteMeanTime(self):
        return self.gui.CalculteMeanTime()

    def GetHgCkbox(self):
        return self.gui.hgCkbox
    def GetHg2Ckbox(self):
        return self.gui.hg2Ckbox
    def GetWlr1Ckbox(self):
        return self.gui.wlr1Ckbox
    def GetWlr2Ckbox(self):
        return self.gui.wlr2Ckbox


    def GetStageLabelCtrl1(self):
        return self.gui.stageLabelCtrl1

    def GetStageLabelCtrl2(self):
        return self.gui.stageLabelCtrl2

    def GetBmLeft(self):
        return self.gui.bmLeft

    def GetBmRight(self):
        return self.gui.bmRight



    def GetMGHHG(self):
        return self.gui.MGHHG

    def GetMGHHG2(self):
        return self.gui.MGHHG2

    def GetMGHWLRefL(self):
        return self.gui.MGHWLRefL

    def GetMGHWLRefR(self):
        return self.gui.MGHWLRefR

    def GetSRCHG(self):
        return self.gui.SRCHG

    def GetSRCHG2(self):
        return self.gui.SRCHG2

    def GetGCHG(self):
        return self.gui.GCHG

    def GetGCHG2(self):
        return self.gui.GCHG2

    def GetGCWLRefL(self):
        return self.gui.GCWLRefL

    def GetGCWLRefR(self):
        return self.gui.GCWLRefR

    def GetCMGHHG(self):
        return self.gui.CMGHHG

    def GetCMGHHG2(self):
        return self.gui.CMGHHG2

    def GetCMGHWLRefL(self):
        return self.gui.CMGHWLRefL

    def GetCMGHWLRefR(self):
        return self.gui.CMGHWLRefR


    def GetMghMethodCmbo(self):
        return self.gui.mghMethod

    def AddEntry(self):
        self.gui.AddEntry()





    def GetFirstTime(self):
        return self.gui.GetFirstTime()

    def GetLastTime(self):
        return self.gui.GetLastTime()





def main():
    app = wx.App()

    frame = wx.Frame(None, size=(500, 400))
    StageMeasurementsManager("DEBUG", StageMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame))

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
