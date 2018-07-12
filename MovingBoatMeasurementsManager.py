# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from MovingBoatMeasurementsPanel import *

class MovingBoatMeasurementsManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "MovingBoatMeasurementsControl"

    #bedMatCmbo
    @property
    def bedMatCmbo(self):
        return self.gui.bedMatCmbo.GetValue()

    @bedMatCmbo.setter
    def bedMatCmbo(self, bedMatCmbo):
        self.gui.bedMatCmbo.SetValue(bedMatCmbo)


    #mb checkbox
    @property
    def mbCB(self):
        return self.gui.mbCB.GetValue()

    @mbCB.setter
    def mbCB(self, mbCB):
        self.gui.mbCB.SetValue(mbCB)
        

    #mb test
    @property
    def mbCmbo(self):
        return self.gui.mbCmbo.GetValue()

    @mbCmbo.setter
    def mbCmbo(self, mbCmbo):
        self.gui.mbCmbo.SetValue(mbCmbo)


    #Detected ctrl
    @property
    def detectedCtrl(self):
        return self.gui.detectedCtrl.GetValue()

    @detectedCtrl.setter
    def detectedCtrl(self, detectedCtrl):
        self.gui.detectedCtrl.SetValue(detectedCtrl)


    #Track Ref Selected Cmbo
    @property
    def trackRefCmbo(self):
        return self.gui.trackRefCmbo.GetValue()

    @trackRefCmbo.setter
    def trackRefCmbo(self, trackRefCmbo):
        self.gui.trackRefCmbo.SetValue(trackRefCmbo)


    #left bank
    @property
    def leftBankCmbo(self):
        return self.gui.leftBankCmbo.GetValue()

    @leftBankCmbo.setter
    def leftBankCmbo(self, leftBankCmbo):
        self.gui.leftBankCmbo.SetValue(leftBankCmbo)


    # @property
    # def leftBankOtherCtrl(self):
    #     return self.gui.leftBankOtherCtrl.GetValue()

    # @leftBankOtherCtrl.setter
    # def leftBankOtherCtrl(self, leftBankOtherCtrl):
    #     self.gui.leftBankOtherCtrl.SetValue(leftBankOtherCtrl)


    #right bank
    @property
    def rightBankCmbo(self):
        return self.gui.rightBankCmbo.GetValue()

    @rightBankCmbo.setter
    def rightBankCmbo(self, rightBankCmbo):
        self.gui.rightBankCmbo.SetValue(rightBankCmbo)


    # @property
    # def rightBankOtherCtrl(self):
    #     return self.gui.rightBankOtherCtrl.GetValue()

    # @rightBankOtherCtrl.setter
    # def rightBankOtherCtrl(self, rightBankOtherCtrl):
    #     self.gui.rightBankOtherCtrl.SetValue(rightBankOtherCtrl)


    #Edge Dist mmnt method
    @property
    def edgeDistMmntCmbo(self):
        return self.gui.edgeDistMmntCmbo.GetValue()

    @edgeDistMmntCmbo.setter
    def edgeDistMmntCmbo(self, edgeDistMmntCmbo):
        self.gui.edgeDistMmntCmbo.SetValue(edgeDistMmntCmbo)


    #Sizer that holds all table values
    @property
    def tableSizer(self):
        return self.gui.tableSizerV

    @tableSizer.setter
    def tableSizer(self, tableSizer):
        self.gui.tableSizerV = tableSizer

    #Gets table val for given row/col
    #row/col start at 0
    #row max val 11
    #col max val 6
    def GetTableValue(self, row, col):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.tableSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.tableSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1
            
        sizerItem = self.tableSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()
        if col == 1:
            return sizerItem.IsChecked()
        return sizerItem.GetValue()

    #Set table val for given row/col
    #row/col start at 0
    #row max val 11
    #col max val 6
    def SetTableValue(self, row, col, val):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.tableSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.tableSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1


        sizerItem = self.tableSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()

        if col == 4:
            time = wx.DateTime()
            time.ParseTime(val)
            val = time
        elif col == 1:
            if val == 'True':
                val = True
                for i in range(1, 8):
                    self.SetFontColor(row - 1, i, 'Black')
            else:
                val = False
                for i in range(1, 8):
                    self.SetFontColor(row - 1, i, 'Red')
        sizerItem.SetValue(val)


    #mmnt start time ctrl
    @property
    def mmntStartTimeCtrl(self):
        return self.gui.mmntStartTimeCtrl.GetValue()

    @mmntStartTimeCtrl.setter
    def mmntStartTimeCtrl(self, mmntStartTimeCtrl):
        # time = wx.DateTime()
        # time.ParseTime(mmntStartTimeCtrl)
        # val = time

        self.gui.mmntStartTimeCtrl.SetValue(mmntStartTimeCtrl)


    @property
    def mmntEndTimeCtrl(self):
        return self.gui.mmntEndTimeCtrl.GetValue()

    @mmntEndTimeCtrl.setter
    def mmntEndTimeCtrl(self, mmntEndTimeCtrl):
        # time = wx.DateTime()
        # time.ParseTime(mmntEndTimeCtrl)
        # val = time
        self.gui.mmntEndTimeCtrl.SetValue(mmntEndTimeCtrl)


    @property
    def mmntMeanTimeCtrl(self):
        return self.gui.mmntMeanTimeCtrl.GetValue()

    @mmntMeanTimeCtrl.setter
    def mmntMeanTimeCtrl(self, mmntMeanTimeCtrl):
        self.gui.mmntMeanTimeCtrl.SetValue(mmntMeanTimeCtrl)


    # @property
    # def rawDischMeanCtrl(self):
    #     return self.gui.rawDischMeanCtrl.GetValue()

    # @rawDischMeanCtrl.setter
    # def rawDischMeanCtrl(self, rawDischMeanCtrl):
    #     self.gui.rawDischMeanCtrl.SetValue(rawDischMeanCtrl)


    @property
    def mbCorrAppCtrl(self):
        return self.gui.mbCorrAppCtrl.GetValue()

    @mbCorrAppCtrl.setter
    def mbCorrAppCtrl(self, mbCorrAppCtrl):
        self.gui.mbCorrAppCtrl.SetValue(mbCorrAppCtrl)


    @property
    def finalDischCtrl(self):
        return self.gui.finalDischCtrl.GetValue()

    @finalDischCtrl.setter
    def finalDischCtrl(self, finalDischCtrl):
        self.gui.finalDischCtrl.SetValue(finalDischCtrl)


    @property
    def corrMeanGHCtrl(self):
        return self.gui.corrMeanGHCtrl.GetValue()

    @corrMeanGHCtrl.setter
    def corrMeanGHCtrl(self, corrMeanGHCtrl):
        self.gui.corrMeanGHCtrl.SetValue(corrMeanGHCtrl)


    @property
    def baseCurveGHCtrl(self):
        return self.gui.baseCurveGHCtrl.GetValue()

    @baseCurveGHCtrl.setter
    def baseCurveGHCtrl(self, baseCurveGHCtrl):
        self.gui.baseCurveGHCtrl.SetValue(baseCurveGHCtrl)


    @property
    def calcShiftBaseCurveCtrl(self):
        return self.gui.calcShiftBaseCurveCtrl.GetValue()

    @calcShiftBaseCurveCtrl.setter
    def calcShiftBaseCurveCtrl(self, calcShiftBaseCurveCtrl):
        self.gui.calcShiftBaseCurveCtrl.SetValue(calcShiftBaseCurveCtrl)


    @property
    def standDevMeanDischCtrl(self):
        return self.gui.standDevMeanDischCtrl.GetValue()

    @standDevMeanDischCtrl.setter
    def standDevMeanDischCtrl(self, standDevMeanDischCtrl):
        self.gui.standDevMeanDischCtrl.SetValue(standDevMeanDischCtrl)


    @property
    def baseCurveDischCtrl(self):
        return self.gui.baseCurveDischCtrl.GetValue()

    @baseCurveDischCtrl.setter
    def baseCurveDischCtrl(self, baseCurveDischCtrl):
        self.gui.baseCurveDischCtrl.SetValue(baseCurveDischCtrl)


    @property
    def dischDiffBaseCurveCtrl(self):
        return self.gui.dischDiffBaseCurveCtrl.GetValue()

    @dischDiffBaseCurveCtrl.setter
    def dischDiffBaseCurveCtrl(self, dischDiffBaseCurveCtrl):
        self.gui.dischDiffBaseCurveCtrl.SetValue(dischDiffBaseCurveCtrl)

    @property
    def commentsCtrl(self):
        return self.gui.commentsCtrl.GetValue()

    @commentsCtrl.setter
    def commentsCtrl(self, commentsCtrl):
        self.gui.commentsCtrl.SetValue(commentsCtrl)

    #compositeTrackCmbo
    @property
    def compositeTrackCmbo(self):
        return self.gui.compositeTrackCmbo.GetValue()

    @compositeTrackCmbo.setter
    def compositeTrackCmbo(self, compositeTrackCmbo):
        self.gui.compositeTrackCmbo.SetValue(compositeTrackCmbo)

    #depthRefCmbo
    @property
    def depthRefCmbo(self):
        return self.gui.depthRefCmbo.GetValue()

    @depthRefCmbo.setter
    def depthRefCmbo(self, depthRefCmbo):
        self.gui.depthRefCmbo.SetValue(depthRefCmbo)

    #velocityTopCombo
    @property
    def velocityTopCombo(self):
        return self.gui.velocityTopCombo.GetValue()

    @velocityTopCombo.setter
    def velocityTopCombo(self, velocityTopCombo):
        self.gui.velocityTopCombo.SetValue(velocityTopCombo)

    #velocityBottomCombo
    @property
    def velocityBottomCombo(self):
        return self.gui.velocityBottomCombo.GetValue()

    @velocityBottomCombo.setter
    def velocityBottomCombo(self, velocityBottomCombo):
        self.gui.velocityBottomCombo.SetValue(velocityBottomCombo)

    #velocityExponentCtrl
    @property
    def velocityExponentCtrl(self):
        return self.gui.velocityExponentCtrl.GetValue()

    @velocityExponentCtrl.setter
    def velocityExponentCtrl(self, velocityExponentCtrl):
        self.gui.velocityExponentCtrl.SetValue(velocityExponentCtrl)

    #differenceCtrl
    @property
    def differenceCtrl(self):
        return self.gui.differenceCtrl.GetValue()

    @differenceCtrl.setter
    def differenceCtrl(self, differenceCtrl):
        self.gui.differenceCtrl.SetValue(differenceCtrl)



    #extrapoloation uncertainty
    @property
    def extrapUncerCtrl(self):
        return self.gui.extrapUncerCtrl.GetValue()

    @extrapUncerCtrl.setter
    def extrapUncerCtrl(self, val):
        self.gui.extrapUncerCtrl.SetValue(val)

    #leftBankOtherCtrl
    @property
    def leftBankOtherCtrl(self):
        return self.gui.leftBankOtherCtrl.GetValue()
    @leftBankOtherCtrl.setter
    def leftBankOtherCtrl(self, leftBankOtherCtrl):
        self.gui.leftBankOtherCtrl.SetValue(leftBankOtherCtrl)

    #rightBankOtherCtrl
    @property
    def rightBankOtherCtrl(self):
        return self.gui.rightBankOtherCtrl.GetValue()
    @rightBankOtherCtrl.setter
    def rightBankOtherCtrl(self, rightBankOtherCtrl):
        self.gui.rightBankOtherCtrl.SetValue(rightBankOtherCtrl)

    def GetLeftBankOtherCtrl(self):
        return self.gui.leftBankOtherCtrl

    def GetRightBankOtherCtrl(self):
        return self.gui.rightBankOtherCtrl

    # @property
    # def lockCB(self):
    #     return self.gui.lockCB.GetValue()

    # @lockCB.setter
    # def lockCB(self, lockCB):
    #     if lockCB.lower() == 'true':
    #         self.gui.lockCB.SetValue(True)
    #     else:
    #         self.gui.lockCB.SetValue(False)


    def SetTableColor(self, row, col, color):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.tableSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.tableSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1


        sizerItem = self.tableSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()


        sizerItem.SetBackgroundColour(color)
        sizerItem.Refresh()





    def GetTableColor(self, row, col):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.tableSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.tableSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1
            
        sizerItem = self.tableSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()
        return sizerItem.GetBackgroundColour()





    def SetFontColor(self, row, col, color):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.tableSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.tableSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1


        sizerItem = self.tableSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()


        sizerItem.SetForegroundColour(color)
        sizerItem.Refresh()


    def GetFontColor(self, row, col):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.tableSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.tableSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1
            
        sizerItem = self.tableSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()
        return sizerItem.GetForegroundColour()


    #recalculate Corrected Mean Gauge, Curve Gauge Height, Base Curve Discharge, Calculate Shift from Base Curve, Discharge Difference Base Curve
    #Base on front page
    def recalculate(self):
        if self.manager is not None:
            self.corrMeanGHCtrl = self.manager.gui.disMeas.mghCtrl.GetValue()
            self.calcShiftBaseCurveCtrl = self.manager.gui.disMeas.shiftCtrl.GetValue()
            self.dischDiffBaseCurveCtrl = self.manager.gui.disMeas.diffCtrl.GetValue()
            if self.manager.gui.disMeas.mghCtrl.GetValue() != '' and self.manager.gui.disMeas.shiftCtrl.GetValue() != '':
                self.baseCurveGHCtrl = str(format(float(self.manager.gui.disMeas.mghCtrl.GetValue()) + float(self.manager.gui.disMeas.shiftCtrl.GetValue()), '.3f'))
            if self.manager.gui.disMeas.dischCtrl.GetValue() != '' and self.manager.gui.disMeas.diffCtrl.GetValue() != '':
                disc = float(self.manager.gui.disMeas.dischCtrl.GetValue())
                diff = float(self.manager.gui.disMeas.diffCtrl.GetValue()) * 0.01 + 1 
                baseCurveDisc = disc / diff
                self.baseCurveDischCtrl = format(baseCurveDisc, '.3f')


    def Clear(self):
        self.gui.Clear()
        # self.corrMeanGHCtrl = ''
        # self.calcShiftBaseCurveCtrl = ''
        # self.dischDiffBaseCurveCtrl = ''
        # self.baseCurveGHCtrl = ''
        # self.baseCurveDischCtrl = ''

    def AddEntry(self):
        self.gui.AddEntry()

    def GetDetectedCtrl(self):
        return self.gui.detectedCtrl


    def GetBedMatCmbo(self):
        return self.gui.bedMatCmbo
    def GetMbCB(self):
        return self.gui.mbCB
    def GetMbCmbo(self):
        return self.gui.mbCmbo
    def GetTrackRefCmbo(self):
        return self.gui.trackRefCmbo
    def GetCompositeTrackCmbo(self):
        return self.gui.compositeTrackCmbo
    def GetLeftBankCmbo(self):
        return self.gui.leftBankCmbo
    def GetLeftBankOtherCtrl(self):
        return self.gui.leftBankOtherCtrl
    def GetRightBankCmbo(self):
        return self.gui.rightBankCmbo
    def GetRightBankOtherCtrl(self):
        return self.gui.rightBankOtherCtrl
    def GetEdgeDistMmntCmbo(self):
        return self.gui.edgeDistMmntCmbo
    def GetDepthRefCmbo(self):
        return self.gui.depthRefCmbo
    def GetVelocityTopCombo(self):
        return self.gui.velocityTopCombo
    def GetVelocityBottomCombo(self):
        return self.gui.velocityBottomCombo
    def GetVelocityExponentCtrl(self):
        return self.gui.velocityExponentCtrl
    def GetDifferenceCtrl(self):
        return self.gui.differenceCtrl


    def GetMmntStartTimeCtrl(self):
        return self.gui.mmntStartTimeCtrl
    # def GetRawDischMeanCtrl(self):
    #     return self.gui.rawDischMeanCtrl
    def GetCorrMeanGHCtrl(self):
        return self.gui.corrMeanGHCtrl
    def GetStandDevMeanDischCtrl(self):
        return self.gui.standDevMeanDischCtrl
    def GetMmntEndTimeCtrl(self):
        return self.gui.mmntEndTimeCtrl
    def GetMbCorrAppCtrl(self):
        return self.gui.mbCorrAppCtrl
    def GetBaseCurveGHCtrl(self):
        return self.gui.baseCurveGHCtrl
    def GetCalcShiftBaseCurveCtrl(self):
        return self.gui.calcShiftBaseCurveCtrl
    def GetMmntMeanTimeCtrl(self):
        return self.gui.mmntMeanTimeCtrl
    def GetFinalDischCtrl(self):
        return self.gui.finalDischCtrl
    def GetBaseCurveDischCtrl(self):
        return self.gui.baseCurveDischCtrl
    def GetDischDiffBaseCurveCtrl(self):
        return self.gui.dischDiffBaseCurveCtrl

    def GetExtrapUncerCtrl(self):
        return self.gui.extrapUncerCtrl

    def GetCommentsCtrl(self):
        return self.gui.commentsCtrl



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(780, 700))
    MovingBoatMeasurementsManager("DEBUG", MovingBoatMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
