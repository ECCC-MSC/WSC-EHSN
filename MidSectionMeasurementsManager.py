# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from MidSectionMeasurementsPanel import *


class MidSectionMeasurementsManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager

        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "Midsection Measurements Manager"




    #start time
    @property
    def startTimeCtrl(self):
        return self.gui.header.startTimeCtrl.GetValue()

    @startTimeCtrl.setter
    def startTimeCtrl(self, startTimeCtrl):
        self.gui.header.startTimeCtrl.SetValue(startTimeCtrl)


    #end time
    @property
    def endTimeCtrl(self):
        return self.gui.header.endTimeCtrl.GetValue()

    @endTimeCtrl.setter
    def endTimeCtrl(self, endTimeCtrl):
        self.gui.header.endTimeCtrl.SetValue(endTimeCtrl)


    #measureSectionCtrl
    @property
    def measureSectionCtrl(self):
        return self.gui.header.measureSectionCtrl.GetValue()

    @measureSectionCtrl.setter
    def measureSectionCtrl(self, measureSectionCtrl):
        self.gui.header.measureSectionCtrl.SetValue(measureSectionCtrl)


    #deployMethodCtrl
    @property
    def deployMethodCtrl(self):
        return self.gui.header.deployMethodCtrl.GetValue()

    @deployMethodCtrl.setter
    def deployMethodCtrl(self, deployMethodCtrl):
        self.gui.header.deployMethodCtrl.SetValue(deployMethodCtrl)

    # #meter1Ckbox
    # @property
    # def meter1Ckbox(self):
    #     return self.gui.header.meter1Ckbox.GetValue()

    # @meter1Ckbox.setter
    # def meter1Ckbox(self, meter1Ckbox):
    #     self.gui.header.meter1Ckbox.SetValue(meter1Ckbox)

    #meter1MeterNoCtrl
    @property
    def meter1MeterNoCtrl(self):
        return self.gui.header.meter1MeterNoCtrl.GetValue()

    @meter1MeterNoCtrl.setter
    def meter1MeterNoCtrl(self, meter1MeterNoCtrl):
        self.gui.header.meter1MeterNoCtrl.SetValue(meter1MeterNoCtrl)

    #meter1SlopeCtrl1
    @property
    def meter1SlopeCtrl1(self):
        return self.gui.header.meter1SlopeCtrl1.GetValue()

    @meter1SlopeCtrl1.setter
    def meter1SlopeCtrl1(self, meter1SlopeCtrl1):
        self.gui.header.meter1SlopeCtrl1.SetValue(meter1SlopeCtrl1)


    #meter1InterceptCtrl1
    @property
    def meter1InterceptCtrl1(self):
        return self.gui.header.meter1InterceptCtrl1.GetValue()

    @meter1InterceptCtrl1.setter
    def meter1InterceptCtrl1(self, meter1InterceptCtrl1):
        self.gui.header.meter1InterceptCtrl1.SetValue(meter1InterceptCtrl1)

    #meter1SlopeCtrl2
    @property
    def meter1SlopeCtrl2(self):
        return self.gui.header.meter1SlopeCtrl2.GetValue()

    @meter1SlopeCtrl2.setter
    def meter1SlopeCtrl2(self, meter1SlopeCtrl2):
        self.gui.header.meter1SlopeCtrl2.SetValue(meter1SlopeCtrl2)

    #meter1InterceptCtrl2
    @property
    def meter1InterceptCtrl2(self):
        return self.gui.header.meter1InterceptCtrl2.GetValue()

    @meter1InterceptCtrl2.setter
    def meter1InterceptCtrl2(self, meter1InterceptCtrl2):
        self.gui.header.meter1InterceptCtrl2.SetValue(meter1InterceptCtrl2)


    #meter1CalibDateCtrl
    @property
    def meter1CalibDateCtrl(self):
        return self.gui.header.meter1CalibDateCtrl.GetValue()

    @meter1CalibDateCtrl.setter
    def meter1CalibDateCtrl(self, meter1CalibDateCtrl):
        self.gui.header.meter1CalibDateCtrl.SetValue(meter1CalibDateCtrl)

    #meter2MeterNoCtrl
    @property
    def meter2MeterNoCtrl(self):
        return self.gui.header.meter2MeterNoCtrl.GetValue()

    @meter2MeterNoCtrl.setter
    def meter2MeterNoCtrl(self, meter2MeterNoCtrl):
        self.gui.header.meter2MeterNoCtrl.SetValue(meter2MeterNoCtrl)


    #meter2SlopeCtrl1
    @property
    def meter2SlopeCtrl1(self):
        return self.gui.header.meter2SlopeCtrl1.GetValue()

    @meter2SlopeCtrl1.setter
    def meter2SlopeCtrl1(self, meter2SlopeCtrl1):
        self.gui.header.meter2SlopeCtrl1.SetValue(meter2SlopeCtrl1)

    #meter2InterceptCtrl1
    @property
    def meter2InterceptCtrl1(self):
        return self.gui.header.meter2InterceptCtrl1.GetValue()

    @meter2InterceptCtrl1.setter
    def meter2InterceptCtrl1(self, meter2InterceptCtrl1):
        self.gui.header.meter2InterceptCtrl1.SetValue(meter2InterceptCtrl1)


    #meter2SlopeCtrl2
    @property
    def meter2SlopeCtrl2(self):
        return self.gui.header.meter2SlopeCtrl2.GetValue()

    @meter2SlopeCtrl2.setter
    def meter2SlopeCtrl2(self, meter2SlopeCtrl2):
        self.gui.header.meter2SlopeCtrl2.SetValue(meter2SlopeCtrl2)

    #meter2InterceptCtrl2
    @property
    def meter2InterceptCtrl2(self):
        return self.gui.header.meter2InterceptCtrl2.GetValue()

    @meter2InterceptCtrl2.setter
    def meter2InterceptCtrl2(self, meter2InterceptCtrl2):
        self.gui.header.meter2InterceptCtrl2.SetValue(meter2InterceptCtrl2)

    #meter2CalibDateCtrl
    @property
    def meter2CalibDateCtrl(self):
        return self.gui.header.meter2CalibDateCtrl.GetValue()

    @meter2CalibDateCtrl.setter
    def meter2CalibDateCtrl(self, meter2CalibDateCtrl):
        self.gui.header.meter2CalibDateCtrl.SetValue(meter2CalibDateCtrl)


    #numOfPanelCtrl
    @property
    def numOfPanelCtrl(self):
        return self.gui.header.numOfPanelCtrl.GetValue()

    @numOfPanelCtrl.setter
    def numOfPanelCtrl(self, numOfPanelCtrl):
        self.gui.header.numOfPanelCtrl.SetValue(numOfPanelCtrl)

    #widthCtrl
    @property
    def widthCtrl(self):
        return self.gui.header.widthCtrl.GetValue()

    @widthCtrl.setter
    def widthCtrl(self, widthCtrl):
        self.gui.header.widthCtrl.SetValue(widthCtrl)

    #areaCtrl
    @property
    def areaCtrl(self):
        return self.gui.header.areaCtrl.GetValue()

    @areaCtrl.setter
    def areaCtrl(self, areaCtrl):
        self.gui.header.areaCtrl.SetValue(areaCtrl)

    #avgDepthCtrl
    @property
    def avgDepthCtrl(self):
        return self.gui.header.avgDepthCtrl.GetValue()

    @avgDepthCtrl.setter
    def avgDepthCtrl(self, avgDepthCtrl):
        self.gui.header.avgDepthCtrl.SetValue(avgDepthCtrl)

    #avgVelCtrl
    @property
    def avgVelCtrl(self):
        return self.gui.header.avgVelCtrl.GetValue()

    @avgVelCtrl.setter
    def avgVelCtrl(self, avgVelCtrl):
        self.gui.header.avgVelCtrl.SetValue(avgVelCtrl)

    #totalDisCtrl
    @property
    def totalDisCtrl(self):
        return self.gui.header.totalDisCtrl.GetValue()

    @totalDisCtrl.setter
    def totalDisCtrl(self, totalDisCtrl):
        self.gui.header.totalDisCtrl.SetValue(totalDisCtrl)

    #uncertaintyCtrl
    @property
    def uncertaintyCtrl(self):
        return self.gui.header.uncertaintyCtrl.GetValue()

    @uncertaintyCtrl.setter
    def uncertaintyCtrl(self, uncertaintyCtrl):
        self.gui.header.uncertaintyCtrl.SetValue(uncertaintyCtrl)

    #nextPid
    @property
    def nextPid(self):
        return self.gui.table.nextPid

    @nextPid.setter
    def nextPid(self, val):
        try:
            self.gui.table.nextPid = int(val)
        except:
            self.gui.table.nextPid = 0



    

    def GenerateNextPid(self):
        return self.gui.table.GenerateNextPid()
    



    def GetPanelObjs(self):
        return self.gui.table.panelObjs

    def SetPanelObjs(self, objs):
        self.gui.table.panelObjs = objs

    def GetNumberRows(self):
        return self.gui.table.summaryTable.GetNumberRows()

    def GetSummaryTable(self):
        return self.gui.table.summaryTable

    def TransferFromObjToTable(self):
        self.gui.table.summaryTable.TransferFromObjToTable()


    def UpdateObjInfoByRow(self, id):
        self.gui.table.UpdateObjInfoByRow(id)
    def TransferFromObjToTable(self):
        self.gui.table.TransferFromObjToTable()
    def RefreshFlow(self):
        self.gui.table.RefreshFlow()

    def AddRow(self, obj):
        self.gui.table.AddRow(obj)
        if isinstance(obj.panelNum, int):
            self.gui.table.nextPanelNum = obj.panelNum + 1





def main():
    app = wx.App()

    frame = wx.Frame(None, size=(940, 850))
    man = MidSectionMeasurementsManager("DEBUG", MidSectionMeasurementsPanel("DEBUG", wx.LANGUAGE_FRENCH, frame))
    frame.Centre()
    frame.Show()



    app.MainLoop()

if __name__ == "__main__":
    main()
