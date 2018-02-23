from xml.etree.ElementTree import SubElement
from MidSectionSubPanelObj import *
import wx
import datetime
import math
import time
import ast


#Calculate the mean time
def mean(start, end):
    startHour = start.GetHour()
    endHour = end.GetHour()
    startMin = start.GetMinute()
    endMin = end.GetMinute()
    startSec = start.GetSecond()
    endSec = end.GetSecond()
    if (startHour + endHour)%2 != 0:
        endMin += 60
    if (startMin + endMin)%2 != 0:
        endSec += 60
    meanHour = (startHour + endHour) / 2
    meanMin = (startMin + endMin) / 2
    meanSec = (startSec + endSec) / 2
    meanTime = str(meanHour) + ':' + str(meanMin) + ':' + str(meanSec)

    return meanTime

# Create XML structure for Title Header info (enteredInHWS checkbox)
def TitleHeaderAsXMLTree(TitleHeader, titleHeaderManager):
    enteredInHWS = SubElement(TitleHeader, 'enteredInHWS')
    enteredInHWS.text = str(titleHeaderManager.enteredInHWSCB)

# Set Title Header info (enteredInHWS checkbox) from an existing XML structure
def TitleHeaderFromXML(TitleHeader, titleHeaderManager):
    enteredInHWSCB = TitleHeader.find('enteredInHWS').text
    titleHeaderManager.enteredInHWSCB = False if enteredInHWSCB is None else (False if enteredInHWSCB == "False" else True)

# Create XML structure for General Info
def GenInfoAsXMLTree( GenInfo, genInfoManager):
    station = SubElement(GenInfo, 'station', number=genInfoManager.stnNumCmbo)
    station.text = genInfoManager.stnName

    date = SubElement(GenInfo, 'date', timezone=genInfoManager.tzCmbo)
    date.text = str(genInfoManager.datePicker)

# Set General Info variables from existing XML structure
def GenInfoFromXML(GenInfo, genInfoManager):
    stationNumber = GenInfo.find('station').get('number')
    genInfoManager.stnNumCmbo = "" if stationNumber is None else stationNumber


    station = GenInfo.find('station').text
    genInfoManager.stnName = "" if station is None else station


    dateTimezone = GenInfo.find('date').get('timezone')
    genInfoManager.tzCmbo = "" if dateTimezone is None else dateTimezone

    date = GenInfo.find('date').text
    genInfoManager.datePicker = "" if date is None else date





# Create XML structure for Stage Measurements
def StageMeasAsXMLTree(StageMeas, stageMeasManager):

    # HgButton = SubElement(StageMeas, 'HgButton')
    # HgButton.text = stageMeasManager.hgButton

    HgCkbox = SubElement(StageMeas, 'HgCkbox')
    HgCkbox.text = str(stageMeasManager.GetHgCkbox().IsChecked())

    Hg2Ckbox = SubElement(StageMeas, 'Hg2Ckbox')
    Hg2Ckbox.text = str(stageMeasManager.GetHg2Ckbox().IsChecked())

    Wlr1Ckbox = SubElement(StageMeas, 'Wlr1Ckbox')
    Wlr1Ckbox.text = str(stageMeasManager.GetWlr1Ckbox().IsChecked())

    Wlr2Ckbox = SubElement(StageMeas, 'Wlr2Ckbox')
    Wlr2Ckbox.text = str(stageMeasManager.GetWlr2Ckbox().IsChecked())


    HG1Header = SubElement(StageMeas, 'HG1Header')
    HG1Header.text = str(stageMeasManager.stageLabelCtrl1)

    HG2Header = SubElement(StageMeas, 'HG2Header')
    HG2Header.text = str(stageMeasManager.stageLabelCtrl2)

    WL1Header = SubElement(StageMeas, 'WL1Header')
    WL1Header.text = str(stageMeasManager.bmLeft)

    WL2Header = SubElement(StageMeas, 'WL2Header')
    WL2Header.text = str(stageMeasManager.bmRight)


    StageMeasTable = SubElement(StageMeas, 'StageMeasTable')
    for row in range(len(stageMeasManager.timeValSizer.GetChildren())):
        StageMeasRow = SubElement(StageMeasTable, 'StageMeasRow', row=str(row))

        time = SubElement(StageMeasRow, 'time')
        time.text = str(stageMeasManager.GetTimeVal(row))

        HG1 = SubElement(StageMeasRow, 'HG1')
        HG1.text = str(stageMeasManager.GetHGVal(row))

        HG2 = SubElement(StageMeasRow, 'HG2')
        HG2.text = str(stageMeasManager.GetHG2Val(row))

        WL1 = SubElement(StageMeasRow, 'WL1')
        WL1.text = str(stageMeasManager.GetWLSubSizerLVal(row))

        WL2 = SubElement(StageMeasRow, 'WL2')
        WL2.text = str(stageMeasManager.GetWLSubSizerRVal(row))

        SRC = SubElement(StageMeasRow, 'SRC')
        SRC.text = str(stageMeasManager.GetSrcSizerVal(row))

        SRCApp = SubElement(StageMeasRow, 'SRCApp')
        SRCApp.text = str(stageMeasManager.GetSrcAppSizerVal(row))

        MghCkbox = SubElement(StageMeasRow, 'MghCkbox')
        MghCkbox.text = str(stageMeasManager.GetMghAggCheckboxVal(row))

    hgCkbox = SubElement(StageMeas, 'hgCkbox')
    hgCkbox.text = str(stageMeasManager.GetHgCkbox().GetValue())
    hg2Ckbox = SubElement(StageMeas, 'hg2Ckbox')
    hg2Ckbox.text = str(stageMeasManager.GetHg2Ckbox().GetValue())
    wlr1Ckbox = SubElement(StageMeas, 'wlr1Ckbox')
    wlr1Ckbox.text = str(stageMeasManager.GetWlr1Ckbox().GetValue())
    wlr2Ckbox = SubElement(StageMeas, 'wlr2Ckbox')
    wlr2Ckbox.text = str(stageMeasManager.GetWlr2Ckbox().GetValue())



    MGHHG1 = SubElement(StageMeas, 'MGHHG1')
    MGHHG1.text = str(stageMeasManager.MGHHG)
    MGHHG2 = SubElement(StageMeas, 'MGHHG2')
    MGHHG2.text = str(stageMeasManager.MGHHG2)
    MGHWL1 = SubElement(StageMeas, 'MGHWL1')
    MGHWL1.text = str(stageMeasManager.MGHWLRefL)
    MGHWL2 = SubElement(StageMeas, 'MGHWL2')
    MGHWL2.text = str(stageMeasManager.MGHWLRefR)

    SRCHG1 = SubElement(StageMeas, 'SRCHG1')
    SRCHG1.text = str(stageMeasManager.SRCHG)
    SRCHG2 = SubElement(StageMeas, 'SRCHG2')
    SRCHG2.text = str(stageMeasManager.SRCHG2)

    GCHG1 = SubElement(StageMeas, 'GCHG1')
    GCHG1.text = str(stageMeasManager.GCHG)
    GCHG2 = SubElement(StageMeas, 'GCHG2')
    GCHG2.text = str(stageMeasManager.GCHG2)
    GCWL1 = SubElement(StageMeas, 'GCWL1')
    GCWL1.text = str(stageMeasManager.GCWLRefL)
    GCWL2 = SubElement(StageMeas, 'GCWL2')
    GCWL2.text = str(stageMeasManager.GCWLRefR)

    CMGHHG1 = SubElement(StageMeas, 'CMGHHG1')
    CMGHHG1.text = str(stageMeasManager.CMGHHG)
    CMGHHG2 = SubElement(StageMeas, 'CMGHHG2')
    CMGHHG2.text = str(stageMeasManager.CMGHHG2)
    CMGHWL1 = SubElement(StageMeas, 'CMGHWL1')
    CMGHWL1.text = str(stageMeasManager.CMGHWLRefL)
    CMGHWL2 = SubElement(StageMeas, 'CMGHWL2')
    CMGHWL2.text = str(stageMeasManager.CMGHWLRefR)

    MghMethod = SubElement(StageMeas, 'MghMethod')
    MghMethod.text = str(stageMeasManager.GetMghMethod())


    # AggCombo = SubElement(StageMeas, 'AggCombo')
    # AggCombo.text = str(stageMeasManager.mghAggCombobox)

    Factors = SubElement(StageMeas, 'Factors')
    Factors.text = str(stageMeasManager.factors)

# Set Stage Measurements variables from existing XML structure
def StageMeasFromXML(StageMeas, stageMeasManager):
    HG1Header = StageMeas.find('HG1Header').text
    stageMeasManager.stageLabelCtrl1 = "" if HG1Header is None else HG1Header

    HG2Header = StageMeas.find('HG2Header').text
    stageMeasManager.stageLabelCtrl2 = "" if HG2Header is None else HG2Header

    WL1Header = StageMeas.find('WL1Header').text
    stageMeasManager.bmLeft = "" if WL1Header is None else WL1Header

    WL2Header = StageMeas.find('WL2Header').text
    stageMeasManager.bmRight = "" if WL2Header is None else WL2Header

    # try:
    #     HgButton = StageMeas.find('HgButton').text
    #     if HgButton == "True":
    #         stageMeasManager.SetToHG()
    #     else:
    #         stageMeasManager.SetToHG2()
    # except:
    #     stageMeasManager.SetToHG()




    #Remove all entries in table first
    for i in range(len(stageMeasManager.timeValSizer.GetChildren())):
        stageMeasManager.gui.RemoveEntry(0)

    try:
        hgCkbox = StageMeas.find('hgCkbox').text
        stageMeasManager.GetHgCkbox().SetValue(hgCkbox == 'True')
        hg2Ckbox = StageMeas.find('hg2Ckbox').text
        stageMeasManager.GetHg2Ckbox().SetValue(hg2Ckbox == 'True')
        wlr1Ckbox = StageMeas.find('wlr1Ckbox').text
        stageMeasManager.GetWlr1Ckbox().SetValue(wlr1Ckbox == 'True')
        wlr2Ckbox = StageMeas.find('wlr2Ckbox').text
        stageMeasManager.GetWlr2Ckbox().SetValue(wlr2Ckbox == 'True')
    except:
        pass


    StageMeasTable = StageMeas.find('StageMeasTable')
    for row, StageMeasRow in enumerate(StageMeasTable.findall('StageMeasRow')):
        stageMeasManager.gui.AddEntry()
        time = StageMeasRow.find('time').text
        HG1 = StageMeasRow.find('HG1').text
        HG2 = StageMeasRow.find('HG2').text
        WL1 = StageMeasRow.find('WL1').text
        WL2 = StageMeasRow.find('WL2').text
        SRC = StageMeasRow.find('SRC').text
        SRCApp = StageMeasRow.find('SRCApp')
        MghCkbox = StageMeasRow.find('MghCkbox')


        if SRCApp is not None:
            SRCApp = SRCApp.text
        if MghCkbox is not None:
            MghCkbox = MghCkbox.text

        stageMeasManager.SetTimeVal(row, "" if time is None else time)
        stageMeasManager.SetHGVal(row, "" if HG1 is None else HG1)
        stageMeasManager.SetHG2Val(row, "" if HG2 is None else HG2)
        stageMeasManager.SetWLSubSizerLVal(row, "" if WL1 is None else WL1)
        stageMeasManager.SetWLSubSizerRVal(row, "" if WL2 is None else WL2)
        stageMeasManager.SetSrcSizerVal(row, "" if SRC is None else SRC)
        stageMeasManager.SetSrcAppSizerVal(row, "" if SRCApp is None else SRCApp)
        stageMeasManager.SetMghAggCheckbox(row, "" if MghCkbox is None else MghCkbox)
        stageMeasManager.GetMghAggCheckbox(row).Enable(time.split(":")[0] != "" and time.split(":")[1] != "")


    # AggCombo = None
    # try:
    #     AggCombo = StageMeas.find('AggCombo').text
    # except:
    #     print "xml doesn't include MghMethod"

    # stageMeasManager.mghAggCombobox = "" if AggCombo is None else AggCombo

    Factors = None
    try:
        Factors = StageMeas.find('Factors').text
    except:
        print "xml doesn't include Factors"

    stageMeasManager.factors = "" if Factors is None else Factors

    ######new field from version 1.1.6###############
    try:
        HgCkbox = StageMeas.find('HgCkbox').text
        if HgCkbox == "True":
            stageMeasManager.GetHgCkbox().SetValue(True)
        else:
            stageMeasManager.GetHgCkbox().SetValue(False)

        Hg2Ckbox = StageMeas.find('Hg2Ckbox').text
        if Hg2Ckbox == "True":
            stageMeasManager.GetHg2Ckbox().SetValue(True)
        else:
            stageMeasManager.GetHg2Ckbox().SetValue(False)

        Wlr1Ckbox = StageMeas.find('Wlr1Ckbox').text
        if Wlr1Ckbox == "True":
            stageMeasManager.GetWlr1Ckbox().SetValue(True)
        else:
            stageMeasManager.GetWlr1Ckbox().SetValue(False)

        Wlr2Ckbox = StageMeas.find('Wlr2Ckbox').text
        if Wlr2Ckbox == "True":
            stageMeasManager.GetWlr2Ckbox().SetValue(True)
        else:
            stageMeasManager.GetWlr2Ckbox().SetValue(False)
    except:
        stageMeasManager.GetHgCkbox().SetValue(False)
        stageMeasManager.GetHg2Ckbox().SetValue(False)
        stageMeasManager.GetWlr1Ckbox().SetValue(False)
        stageMeasManager.GetWlr2Ckbox().SetValue(False)

    ##################################





    MGHHG1 = StageMeas.find('MGHHG1').text
    stageMeasManager.MGHHG = "" if MGHHG1 is None else MGHHG1
    MGHHG2 = StageMeas.find('MGHHG2').text
    stageMeasManager.MGHHG2 = "" if MGHHG2 is None else MGHHG2
    MGHWL1 = StageMeas.find('MGHWL1').text
    stageMeasManager.MGHWLRefL = "" if MGHWL1 is None else MGHWL1
    MGHWL2 = StageMeas.find('MGHWL2').text
    stageMeasManager.MGHWLRefR = "" if MGHWL2 is None else MGHWL2

    SRCHG1 = StageMeas.find('SRCHG1').text
    stageMeasManager.SRCHG = "" if SRCHG1 is None else SRCHG1
    SRCHG2 = StageMeas.find('SRCHG2').text
    stageMeasManager.SRCHG2 = "" if SRCHG2 is None else SRCHG2

    GCHG1 = StageMeas.find('GCHG1').text
    stageMeasManager.GCHG = "" if GCHG1 is None else GCHG1
    GCHG2 = StageMeas.find('GCHG2').text
    stageMeasManager.GCHG2 = "" if GCHG2 is None else GCHG2
    GCWL1 = StageMeas.find('GCWL1').text
    stageMeasManager.GCWLRefL = "" if GCWL1 is None else GCWL1
    GCWL2 = StageMeas.find('GCWL2').text
    stageMeasManager.GCWLRefR = "" if GCWL2 is None else GCWL2

    CMGHHG1 = StageMeas.find('CMGHHG1').text
    stageMeasManager.CMGHHG = "" if CMGHHG1 is None else CMGHHG1
    CMGHHG2 = StageMeas.find('CMGHHG2').text
    stageMeasManager.CMGHHG2 = "" if CMGHHG2 is None else CMGHHG2
    CMGHWL1 = StageMeas.find('CMGHWL1').text
    stageMeasManager.CMGHWLRefL = "" if CMGHWL1 is None else CMGHWL1
    CMGHWL2 = StageMeas.find('CMGHWL2').text
    stageMeasManager.CMGHWLRefR = "" if CMGHWL2 is None else CMGHWL2

    MghMethod = None
    try:
        MghMethod = StageMeas.find('MghMethod').text
    except:
        print "xml doesn't include MghMethod"
    if MghMethod is not None:
        stageMeasManager.SetMghMethod(MghMethod)
    else:
        stageMeasManager.SetMghMethod("")

    # stageMeasManager.gui.UpdateDischargeMGH()
    # print stageMeasManager.gui.CMGHHG.GetValue()

# Create XML structure for Discharge Measurements
def DischMeasAsXMLTree(DisMeas, disMeasManager):
    startTime = SubElement(DisMeas, 'startTime')
    startTime.text = str(disMeasManager.startTimeCtrl)

    endTime = SubElement(DisMeas, 'endTime')
    endTime.text = str(disMeasManager.endTimeCtrl)

    airTemp = SubElement(DisMeas, 'airTemp')
    airTemp.text = str(disMeasManager.airTempCtrl)

    waterTemp = SubElement(DisMeas, 'waterTemp')
    waterTemp.text = str(disMeasManager.waterTempCtrl)

    width = SubElement(DisMeas, 'width')
    width.text = str(disMeasManager.widthCtrl)

    area = SubElement(DisMeas, 'area')
    area.text = str(disMeasManager.areaCtrl)

    meanVel = SubElement(DisMeas, 'meanVel')
    meanVel.text = str(disMeasManager.meanVelCtrl)

    mgh = SubElement(DisMeas, 'mgh')
    mgh.text = str(disMeasManager.mghCtrl)


    mghCmbo = SubElement(DisMeas, 'mghCmbo')
    mghCmbo.text = str(disMeasManager.mghCmbo)


    # mghChoice1 = SubElement(DisMeas, 'mghChoice1')
    # mghChoice1.text = str(disMeasManager.GetMGHChoices()[1])
    # mghChoice2 = SubElement(DisMeas, 'mghChoice2')
    # mghChoice2.text = str(disMeasManager.GetMGHChoices()[2])
    # mghChoice3 = SubElement(DisMeas, 'mghChoice3')
    # mghChoice3.text = str(disMeasManager.GetMGHChoices()[3])
    # mghChoice4 = SubElement(DisMeas, 'mghChoice4')
    # mghChoice4.text = str(disMeasManager.GetMGHChoices()[4])

    discharge = SubElement(DisMeas, 'discharge')
    discharge.text = str(disMeasManager.dischCtrl)



    mmtTimeVal = SubElement(DisMeas, 'mmtTimeVal')
    mmtTimeVal.text = str(disMeasManager.mmtValTxt)

    shift = SubElement(DisMeas, 'shift')
    shift.text = str(disMeasManager.shiftCtrl)

    diff = SubElement(DisMeas, 'diff')
    diff.text = str(disMeasManager.diffCtrl)

    curve = SubElement(DisMeas, 'curve')
    curve.text = str(disMeasManager.curveCtrl)

# Set Discharge Measurements variables from existing XML structure
def DischMeasFromXML(DisMeas, disMeasManager):
    startTime = DisMeas.find('startTime').text
    disMeasManager.startTimeCtrl = "" if startTime is None else startTime

    endTime = DisMeas.find('endTime').text
    disMeasManager.endTimeCtrl = "" if endTime is None else endTime

    airTemp = DisMeas.find('airTemp').text
    disMeasManager.airTempCtrl = "" if airTemp is None else airTemp

    waterTemp = DisMeas.find('waterTemp').text
    disMeasManager.waterTempCtrl = "" if waterTemp is None else waterTemp

    width = DisMeas.find('width').text
    disMeasManager.widthCtrl = "" if width is None else width

    area = DisMeas.find('area').text
    disMeasManager.areaCtrl = "" if area is None else area

    meanVel = DisMeas.find('meanVel').text
    disMeasManager.meanVelCtrl = "" if meanVel is None else meanVel

    mgh = DisMeas.find('mgh').text
    disMeasManager.mghCtrl = "" if mgh is None else mgh



    discharge = DisMeas.find('discharge').text
    disMeasManager.dischCtrl = "" if discharge is None else discharge

    mmtTimeVal = DisMeas.find('mmtTimeVal').text
    disMeasManager.mmtValTxt = "" if mmtTimeVal is None else mmtTimeVal

    shift = DisMeas.find('shift').text
    disMeasManager.shiftCtrl = "" if shift is None else shift

    diff = DisMeas.find('diff').text
    disMeasManager.diffCtrl = "" if diff is None else diff

    curve = DisMeas.find('curve').text
    disMeasManager.curveCtrl = "" if curve is None else curve


    try:
        mghCmbo = DisMeas.find('mghCmbo').text
        disMeasManager.mghCmbo = "" if mghCmbo is None else mghCmbo
    except:
        pass



# Create XML structure for Environment Conditions (Station Health / Gauge Maintenance)
def EnvCondAsXMLTree(EnvCond, envCondManager):
    levels = SubElement(EnvCond, 'levels')
    levels.text = envCondManager.levelsCtrl

    cloudCover = SubElement(EnvCond, 'cloudCover')
    cloudCover.text = envCondManager.cloudCoverCmbo

    precip = SubElement(EnvCond, 'precipitation')
    precip.text = envCondManager.precipCmbo

    windMagnitude = SubElement(EnvCond, 'windMagnitude')
    windMagnitude.text = envCondManager.windMagCmbo

    windMagVel = SubElement(EnvCond, 'windMagnitudeSpeed')
    windMagVel.text = envCondManager.windMagCtrl

    windDir = SubElement(EnvCond, 'windDirection')
    windDir.text = envCondManager.windDirCmbo

    batteryVolt = SubElement(EnvCond, 'batteryVolt')
    batteryVolt.text = envCondManager.batteryCtrl

    gasSys = SubElement(EnvCond, 'gasSys')
    gasSys.text = envCondManager.gasSysCtrl

    feed = SubElement(EnvCond, 'feed')
    feed.text = envCondManager.feedCtrl

    bpmRotChoice = SubElement(EnvCond, 'bpmRotChoice')
    bpmRotChoice.text = envCondManager.bpmrotCmbo

    bpmRot = SubElement(EnvCond, 'bpmRot')
    bpmRot.text = envCondManager.bpmrotCtrl

    intakeFlushed = SubElement(EnvCond, 'intakeFlushed')
    intakeFlushed.text = str(envCondManager.intakeCB)

    intakeTime = SubElement(EnvCond, 'intakeTime')
    intakeTime.text = str(envCondManager.intakeTimeCtrl)


    orificeTime = SubElement(EnvCond, 'orificeTime')
    orificeTime.text = str(envCondManager.orificeTimeCtrl)

    orificePurged = SubElement(EnvCond, 'orificePurged')
    orificePurged.text = str(envCondManager.orificeCB)

    downloadedProgram = SubElement(EnvCond, 'downloadedProgram')
    downloadedProgram.text = str(envCondManager.programCB)

    downloadedData = SubElement(EnvCond, 'downloadedData')
    downloadedData.text = str(envCondManager.dataCB)

    dataPeriodStart = SubElement(EnvCond, 'dataPeriodStart')
    dataPeriodStart.text = str(envCondManager.dataPeriodFromPicker)

    dataPeriodEnd = SubElement(EnvCond, 'dataPeriodEnd')
    dataPeriodEnd.text = str(envCondManager.dataPeriodToPicker)

# Set Environment Conditions (Station Health / Gauge Maintenance) variables from existing XML structure
def EnvCondFromXML(EnvCond, envCondManager):
    levels = EnvCond.find('levels').text
    envCondManager.levelsCtrl = "" if levels is None else levels

    cloudCover = EnvCond.find('cloudCover').text
    envCondManager.cloudCoverCmbo = "" if cloudCover is None else cloudCover

    precip = EnvCond.find('precipitation').text
    envCondManager.precipCmbo = "" if precip is None else precip

    windMagnitude = EnvCond.find('windMagnitude').text
    envCondManager.windMagCmbo = "" if windMagnitude is None else windMagnitude

    windMagVel = EnvCond.find('windMagnitudeSpeed').text
    envCondManager.windMagCtrl = "" if windMagVel is None else windMagVel

    windDir = EnvCond.find('windDirection').text
    envCondManager.windDirCmbo = "" if windDir is None else windDir

    batteryVolt = EnvCond.find('batteryVolt').text
    envCondManager.batteryCtrl = "" if batteryVolt is None else batteryVolt

    gasSys = EnvCond.find('gasSys').text
    envCondManager.gasSysCtrl = "" if gasSys is None else gasSys

    feed = EnvCond.find('feed').text
    envCondManager.feedCtrl = "" if feed is None else feed

    bpmRotChoice = EnvCond.find('bpmRotChoice').text
    envCondManager.bpmrotCmbo = "" if bpmRotChoice is None else bpmRotChoice

    bpmRot = EnvCond.find('bpmRot').text
    envCondManager.bpmrotCtrl = "" if bpmRot is None else bpmRot

    intakeTime = EnvCond.find('intakeTime').text
    envCondManager.intakeTimeCtrl = "00:00:00" if intakeTime is None else intakeTime

    orificeTime = EnvCond.find('orificeTime').text
    envCondManager.orificeTimeCtrl = "00:00:00" if orificeTime is None else orificeTime


    intakeFlushed = EnvCond.find('intakeFlushed').text
    envCondManager.intakeCB = False if intakeFlushed is None else (False if intakeFlushed == 'False' else True)




    orificePurged = EnvCond.find('orificePurged').text
    envCondManager.orificeCB = False if orificePurged is None else (False if orificePurged == 'False' else True)

    downloadedProgram = EnvCond.find('downloadedProgram').text
    envCondManager.programCB = False if downloadedProgram is None else (False if downloadedProgram == 'False' else True)

    downloadedData = EnvCond.find('downloadedData').text
    if downloadedData == None or downloadedData == 'False':
        envCondManager.dataCB = False
    else:
        envCondManager.dataCB = True
        envCondManager.GetDataPeriodFromPicker().Enable(True)
        envCondManager.GetDataPeriodToPicker().Enable(True)



    dataPeriodStart = EnvCond.find('dataPeriodStart').text
    envCondManager.dataPeriodFromPicker = "" if dataPeriodStart is None else dataPeriodStart

    dataPeriodEnd = EnvCond.find('dataPeriodEnd').text
    envCondManager.dataPeriodToPicker = "" if dataPeriodEnd is None else dataPeriodEnd




    if intakeFlushed == 'True':
        envCondManager.gui.intakeTimeCtrl.Show()
    else:
        envCondManager.gui.intakeTimeCtrl.Hide()

    if orificePurged == 'True':
        envCondManager.gui.orificeTimeCtrl.Show()
    else:
        envCondManager.gui.orificeTimeCtrl.Hide()
    envCondManager.gui.layoutSizer.Layout()

# Create XML structure for Measurement Results (Sensor Calibrations)
def MeasResultsAsXMLTree(MeasResults, measResultsManager):
    # time = SubElement(MeasResults, 'time')
    # time.text = str(measResultsManager.timeCtrl)

    sensRefsExist = False

    SensorRefs = SubElement(MeasResults, 'SensorRefs')
    HourMinutes = SubElement(MeasResults, 'HourMinutes')
    Times = SubElement(MeasResults, 'Times')
    ObservedVals = SubElement(MeasResults, 'ObservedVals')
    SensorVals = SubElement(MeasResults, 'SensorVals')
    if measResultsManager.sensorRefEntry1 != "":
        sensRefsExist = True
        sensorRef1 = SubElement(SensorRefs, 'SensorRef', row="1")
        sensorRef1.text = measResultsManager.sensorRefEntry1

        hour1 = SubElement(HourMinutes, 'Hour', row="1")
        hour1.text = measResultsManager.hour1

        minute1 = SubElement(HourMinutes, 'Minute', row="1")
        minute1.text = measResultsManager.minute1

        time = SubElement(Times, 'Time', row="1")
        time.text = measResultsManager.GetTime(0)

        observedVal1 = SubElement(ObservedVals, 'ObservedVal', row="1")
        observedVal1.text = measResultsManager.observedVal1

        sensorVal1 = SubElement(SensorVals, 'SensorVal', row="1")
        sensorVal1.text = measResultsManager.sensorVal1


    if measResultsManager.sensorRefEntry2 != "":
        sensRefsExist = True
        sensorRef2 = SubElement(SensorRefs, 'SensorRef', row="2")
        sensorRef2.text = measResultsManager.sensorRefEntry2

        hour2 = SubElement(HourMinutes, 'Hour', row="2")
        hour2.text = measResultsManager.hour2

        minute2 = SubElement(HourMinutes, 'Minute', row="2")
        minute2.text = measResultsManager.minute2

        time = SubElement(Times, 'Time', row="2")
        time.text = measResultsManager.GetTime(1)

        observedVal2 = SubElement(ObservedVals, 'ObservedVal', row="2")
        observedVal2.text = measResultsManager.observedVal2

        sensorVal2 = SubElement(SensorVals, 'SensorVal', row="2")
        sensorVal2.text = measResultsManager.sensorVal2

    if measResultsManager.sensorRefEntry3 != "":
        sensRefsExist = True
        sensorRef3 = SubElement(SensorRefs, 'SensorRef', row="3")
        sensorRef3.text = measResultsManager.sensorRefEntry3

        hour3 = SubElement(HourMinutes, 'Hour', row="3")
        hour3.text = measResultsManager.hour3

        minute1 = SubElement(HourMinutes, 'Minute', row="3")
        minute1.text = measResultsManager.minute3

        time = SubElement(Times, 'Time', row="3")
        time.text = measResultsManager.GetTime(2)

        observedVal3 = SubElement(ObservedVals, 'ObservedVal', row="3")
        observedVal3.text = measResultsManager.observedVal3

        sensorVal3 = SubElement(SensorVals, 'SensorVal', row="3")
        sensorVal3.text = measResultsManager.sensorVal3

    if measResultsManager.sensorRefEntry4 != "":
        sensRefsExist = True
        sensorRef4 = SubElement(SensorRefs, 'SensorRef', row="4")
        sensorRef4.text = measResultsManager.sensorRefEntry4

        hour4 = SubElement(HourMinutes, 'Hour', row="4")
        hour4.text = measResultsManager.hour4

        minute4 = SubElement(HourMinutes, 'Minute', row="4")
        minute4.text = measResultsManager.minute4

        time = SubElement(Times, 'Time', row="4")
        time.text = measResultsManager.GetTime(3)

        observedVal4 = SubElement(ObservedVals, 'ObservedVal', row="4")
        observedVal4.text = measResultsManager.observedVal4

        sensorVal4 = SubElement(SensorVals, 'SensorVal', row="4")
        sensorVal4.text = measResultsManager.sensorVal4


    # if measResultsManager.sensorRefEntry5 != "":
    #     sensRefsExist = True
    #     sensorRef5 = SubElement(SensorRefs, 'SensorRef', row="5")
    #     sensorRef5.text = measResultsManager.sensorRefEntry5

    #     hour5 = SubElement(HourMinutes, 'Hour', row="5")
    #     hour5.text = measResultsManager.hour5

    #     minute5 = SubElement(HourMinutes, 'Minute', row="5")
    #     minute5.text = measResultsManager.minute5

    #     time = SubElement(Times, 'Time', row="5")
    #     time.text = measResultsManager.GetTime(4)

    #     observedVal5 = SubElement(ObservedVals, 'ObservedVal', row="5")
    #     observedVal5.text = measResultsManager.observedVal5

    #     sensorVal5 = SubElement(SensorVals, 'SensorVal', row="5")
    #     sensorVal5.text = measResultsManager.sensorVal5

    # if measResultsManager.sensorRefEntry6 != "":
    #     sensRefsExist = True
    #     sensorRef6 = SubElement(SensorRefs, 'SensorRef', row="6")
    #     sensorRef6.text = measResultsManager.sensorRefEntry6

    if not sensRefsExist:
        MeasResults.attrib['empty'] = 'True'


    # if measResultsManager.observedVal1 != "":
    #     observedVal1 = SubElement(ObservedVals, 'ObservedVal', row="1")
    #     observedVal1.text = measResultsManager.observedVal1

    # if measResultsManager.observedVal2 != "":
    #     observedVal2 = SubElement(ObservedVals, 'ObservedVal', row="2")
    #     observedVal2.text = measResultsManager.observedVal2

    # if measResultsManager.observedVal3 != "":
    #     observedVal3 = SubElement(ObservedVals, 'ObservedVal', row="3")
    #     observedVal3.text = measResultsManager.observedVal3

    # if measResultsManager.observedVal4 != "":
    #     observedVal4 = SubElement(ObservedVals, 'ObservedVal', row="4")
    #     observedVal4.text = measResultsManager.observedVal4

    # if measResultsManager.observedVal5 != "":
    #     observedVal5 = SubElement(ObservedVals, 'ObservedVal', row="5")
    #     observedVal5.text = measResultsManager.observedVal5

    # if measResultsManager.observedVal6 != "":
    #     observedVal6 = SubElement(ObservedVals, 'ObservedVal', row="6")
    #     observedVal6.text = measResultsManager.observedVal6



    # if measResultsManager.sensorVal1 != "":
    #     sensorVal1 = SubElement(SensorVals, 'SensorVal', row="1")
    #     sensorVal1.text = measResultsManager.sensorVal1

    # if measResultsManager.sensorVal2 != "":
    #     sensorVal2 = SubElement(SensorVals, 'SensorVal', row="2")
    #     sensorVal2.text = measResultsManager.sensorVal2

    # if measResultsManager.sensorVal3 != "":
    #     sensorVal3 = SubElement(SensorVals, 'SensorVal', row="3")
    #     sensorVal3.text = measResultsManager.sensorVal3

    # if measResultsManager.sensorVal4 != "":
    #     sensorVal4 = SubElement(SensorVals, 'SensorVal', row="4")
    #     sensorVal4.text = measResultsManager.sensorVal4

    # if measResultsManager.sensorVal5 != "":
    #     sensorVal5 = SubElement(SensorVals, 'SensorVal', row="5")
    #     sensorVal5.text = measResultsManager.sensorVal5

    # if measResultsManager.sensorVal6 != "":
    #     sensorVal6 = SubElement(SensorVals, 'SensorVal', row="6")
    #     sensorVal6.text = measResultsManager.sensorVal6

    loggerTimeTable = SubElement(MeasResults, 'loggerTimeTable')
    loggerTimeCol1Exist = False
    loggerTimeCol2Exist = False
    # if measResultsManager.loggerTimeCol1 != "":
    loggerTimeCol1Exist = True
    loggerTimeCol1 = SubElement(loggerTimeTable, 'loggerTimeCol1')
    loggerTimeCol1.text = measResultsManager.loggerTimeCol1

    loggerTimeRemark1 = SubElement(loggerTimeTable, 'loggerTimeRemark1')
    loggerTimeRemark1.text = measResultsManager.loggerTimeRemark1

    hour7 = SubElement(loggerTimeTable, 'Hour7')
    hour7.text = measResultsManager.hour7

    minute7 = SubElement(loggerTimeTable, 'Minute7')
    minute7.text = measResultsManager.minute7

    hour9 = SubElement(loggerTimeTable, 'Hour9')
    hour9.text = measResultsManager.hour9

    minute9 = SubElement(loggerTimeTable, 'Minute9')
    minute9.text = measResultsManager.minute9

    time7 = SubElement(loggerTimeTable, 'Time7')
    time7.text = measResultsManager.GetTime(5)

    time9 = SubElement(loggerTimeTable, 'Time9')
    time9.text = measResultsManager.GetTime(7)

    # if measResultsManager.loggerTimeCol2 != "":
    loggerTimeCol2Exist = True
    loggerTimeCol2 = SubElement(loggerTimeTable, 'loggerTimeCol2')
    loggerTimeCol2.text = measResultsManager.loggerTimeCol2

    loggerTimeRemark2 = SubElement(loggerTimeTable, 'loggerTimeRemark2')
    loggerTimeRemark2.text = measResultsManager.loggerTimeRemark2

    hour8 = SubElement(loggerTimeTable, 'Hour8')
    hour8.text = measResultsManager.hour8

    minute8 = SubElement(loggerTimeTable, 'Minute8')
    minute8.text = measResultsManager.minute8

    hour10 = SubElement(loggerTimeTable, 'Hour10')
    hour10.text = measResultsManager.hour10

    minute10 = SubElement(loggerTimeTable, 'Minute10')
    minute10.text = measResultsManager.minute10

    time8 = SubElement(loggerTimeTable, 'Time8')
    time8.text = measResultsManager.GetTime(6)

    time10 = SubElement(loggerTimeTable, 'Time10')
    time10.text = measResultsManager.GetTime(8)


# Set Measurement Results (Sensor Calibrations) variables from existing XML structure
def MeasResultsFromXML(MeasResults, measResultsManager):
    # time = MeasResults.find('time').text
    # measResultsManager.timeCtrl = "" if time is None else time

    # Reset all Sensor References
    measResultsManager.sensorRefEntry1 = ""
    measResultsManager.sensorRefEntry2 = ""
    measResultsManager.sensorRefEntry3 = ""
    measResultsManager.sensorRefEntry4 = ""
    # measResultsManager.sensorRefEntry5 = ""
    # measResultsManager.sensorRefEntry6 = ""

    # Reset all Observed Values
    measResultsManager.observedVal1 = ""
    measResultsManager.observedVal2 = ""
    measResultsManager.observedVal3 = ""
    measResultsManager.observedVal4 = ""
    # measResultsManager.observedVal5 = ""
    # measResultsManager.observedVal6 = ""

    # Reset all Sensor Values
    measResultsManager.sensorVal1 = ""
    measResultsManager.sensorVal2 = ""
    measResultsManager.sensorVal3 = ""
    measResultsManager.sensorVal4 = ""
    # measResultsManager.sensorVal5 = ""
    # measResultsManager.sensorVal6 = ""

    # Reset all time
    measResultsManager.hour1 = ""
    measResultsManager.hour2 = ""
    measResultsManager.hour3 = ""
    measResultsManager.hour4 = ""
    # measResultsManager.hour5 = ""
    measResultsManager.hour7 = ""
    measResultsManager.hour8 = ""


    measResultsManager.minute1 = ""
    measResultsManager.minute2 = ""
    measResultsManager.minute3 = ""
    measResultsManager.minute4 = ""
    # measResultsManager.minute5 = ""
    measResultsManager.minute7 = ""
    measResultsManager.minute8 = ""



    # Reset Logger Time Table
    measResultsManager.loggerTimeCol1 = ""
    measResultsManager.loggerTimeCol2 = ""
    measResultsManager.loggerTimeRemark1 = ""
    measResultsManager.loggerTimeRemark2 = ""
    measResultsManager.hour9 = ""
    measResultsManager.hour10 = ""
    measResultsManager.minute9 = ""
    measResultsManager.minute10 = ""

    #Sensor References Branch
    SensorRefs = MeasResults.find('SensorRefs')
    HourMinutes = MeasResults.find('HourMinutes')
    for SensorRef in SensorRefs.findall('SensorRef'):
        row = int(SensorRef.get('row'))

        if row == 1:
            sensorRef1 = SensorRef.text
            measResultsManager.sensorRefEntry1 = "" if sensorRef1 is None else sensorRef1
        if row == 2:
            sensorRef2 = SensorRef.text
            measResultsManager.sensorRefEntry2 = "" if sensorRef2 is None else sensorRef2
        if row == 3:
            sensorRef3 = SensorRef.text
            measResultsManager.sensorRefEntry3 = "" if sensorRef3 is None else sensorRef3
        if row == 4:
            sensorRef4 = SensorRef.text
            measResultsManager.sensorRefEntry4 = "" if sensorRef4 is None else sensorRef4
        # if row == 5:
        #     sensorRef5 = SensorRef.text
        #     measResultsManager.sensorRefEntry5 = "" if sensorRef5 is None else sensorRef5
        # if row == 6:
        #     sensorRef6 = SensorRef.text
        #     measResultsManager.sensorRefEntry6 = "" if sensorRef6 is None else sensorRef6

    try:
        for Hour in HourMinutes.findall('Hour'):
            row = int(Hour.get('row'))

            if row == 1:
                hour = Hour.text
                measResultsManager.hour1 = "" if hour is None else hour
            if row == 2:
                hour = Hour.text
                measResultsManager.hour2 = "" if hour is None else hour
            if row == 3:
                hour = Hour.text
                measResultsManager.hour3 = "" if hour is None else hour
            if row == 4:
                hour = Hour.text
                measResultsManager.hour4 = "" if hour is None else hour
            # if row == 5:
            #     hour = Hour.text
            #     measResultsManager.hour5 = "" if hour is None else hour

        for Minute in HourMinutes.findall('Minute'):
            row = int(Minute.get('row'))

            if row == 1:
                minute = Minute.text
                measResultsManager.minute1 = "" if minute is None else minute
            if row == 2:
                minute = Minute.text
                measResultsManager.minute2 = "" if minute is None else minute
            if row == 3:
                minute = Minute.text
                measResultsManager.minute3 = "" if minute is None else minute
            if row == 4:
                minute = Minute.text
                measResultsManager.minute4 = "" if minute is None else minute
            # if row == 5:
            #     minute = Minute.text
            #     measResultsManager.minute5 = "" if minute is None else minute
    except:
        pass


    #Observed Values Branch
    ObservedVals = MeasResults.find('ObservedVals')
    for ObservedVal in ObservedVals.findall('ObservedVal'):
        row = int(ObservedVal.get('row'))

        if row == 1:
            observedVal1 = ObservedVal.text
            measResultsManager.observedVal1 = "" if observedVal1 is None else observedVal1
        if row == 2:
            observedVal2 = ObservedVal.text
            measResultsManager.observedVal2 = "" if observedVal2 is None else observedVal2
        if row == 3:
            observedVal3 = ObservedVal.text
            measResultsManager.observedVal3 = "" if observedVal3 is None else observedVal3
        if row == 4:
            observedVal4 = ObservedVal.text
            measResultsManager.observedVal4 = "" if observedVal4 is None else observedVal4
        # if row == 5:
        #     observedVal5 = ObservedVal.text
        #     measResultsManager.observedVal5 = "" if observedVal5 is None else observedVal5
        # if row == 6:
        #     observedVal6 = ObservedVal.text
        #     measResultsManager.observedVal6 = "" if observedVal6 is None else observedVal6


    #Sensor Values Branch
    SensorVals = MeasResults.find('SensorVals')
    for SensorVal in SensorVals.findall('SensorVal'):
        row = int(SensorVal.get('row'))

        if row == 1:
            sensorVal1 = SensorVal.text
            measResultsManager.sensorVal1 = "" if sensorVal1 is None else sensorVal1
        if row == 2:
            sensorVal2 = SensorVal.text
            measResultsManager.sensorVal2 = "" if sensorVal2 is None else sensorVal2
        if row == 3:
            sensorVal3 = SensorVal.text
            measResultsManager.sensorVal3 = "" if sensorVal3 is None else sensorVal3
        if row == 4:
            sensorVal4 = SensorVal.text
            measResultsManager.sensorVal4 = "" if sensorVal4 is None else sensorVal4
        # if row == 5:
        #     sensorVal5 = SensorVal.text
        #     measResultsManager.sensorVal5 = "" if sensorVal5 is None else sensorVal5
        # if row == 6:
        #     sensorVal6 = SensorVal.text
        #     measResultsManager.sensorVal6 = "" if sensorVal6 is None else sensorVal6

    try:
        loggerTable = MeasResults.find('loggerTimeTable')

        loggerTimeCol1 = loggerTable.find('loggerTimeCol1').text
        loggerTimeRemark1 = loggerTable.find('loggerTimeRemark1').text
        hour7 = loggerTable.find('Hour7').text
        minute7 = loggerTable.find('Minute7').text
        hour8 = loggerTable.find('Hour8').text
        minute8 = loggerTable.find('Minute8').text
        loggerTimeCol2 = loggerTable.find('loggerTimeCol2').text
        loggerTimeRemark2 = loggerTable.find('loggerTimeRemark2').text
        hour9 = loggerTable.find('Hour9').text
        minute9 = loggerTable.find('Minute9').text
        hour10 = loggerTable.find('Hour10').text
        minute10 = loggerTable.find('Minute10').text
    except:
        loggerTable = None

    if loggerTable is not None:
        measResultsManager.loggerTimeCol1 = "" if loggerTimeCol1 is None else loggerTimeCol1
        measResultsManager.loggerTimeRemark1 = "" if loggerTimeRemark1 is None else loggerTimeRemark1
        measResultsManager.hour7 = "" if hour7 is None else hour7
        measResultsManager.minute7 = "" if minute7 is None else minute7
        measResultsManager.hour8 = "" if hour8 is None else hour8
        measResultsManager.minute8 = "" if minute8 is None else minute8
        measResultsManager.loggerTimeCol2 = "" if loggerTimeCol2 is None else loggerTimeCol2
        measResultsManager.loggerTimeRemark2 = "" if loggerTimeRemark2 is None else loggerTimeRemark2
        measResultsManager.hour9 = "" if hour9 is None else hour9
        measResultsManager.minute9 = "" if minute9 is None else minute9
        measResultsManager.hour10 = "" if hour10 is None else hour10
        measResultsManager.minute10 = "" if minute10 is None else minute10



# Create XML structure for Instrument and Deployment information
def InstrumentDepAsXMLTree(InstrumentDeployment, instrDepManager):
    checkList = instrDepManager.methodCBListBox.GetCheckedStrings()

    check = None
    if len(checkList) > 0:
        check = checkList[0]

    GeneralInfo = SubElement(InstrumentDeployment, 'GeneralInfo')
    method = SubElement(GeneralInfo, 'methodType')
    method.text = str(check)

    deployment = SubElement(GeneralInfo, 'deployment')
    deployment.text = instrDepManager.deploymentCmbo

    position = SubElement(GeneralInfo, 'position')
    position.text = instrDepManager.positionMethodCtrl

    instrument = SubElement(GeneralInfo, 'instrument')
    instrument.text = instrDepManager.instrumentCmbo

    serialNum = SubElement(GeneralInfo, 'serialNum')
    serialNum.text = instrDepManager.serialCmbo

    gauge1 = SubElement(GeneralInfo, 'gauge1')
    gauge1.text = instrDepManager.gaugeCtrl

    length = SubElement(GeneralInfo, 'length')
    length.text = str(instrDepManager.lengthRadButBox)

    gaugePos = SubElement(GeneralInfo, 'gaugePos')
    gaugePos.text = str(instrDepManager.posRadButBox)

    # gauge2 = SubElement(GeneralInfo, 'gauge2')
    # gauge2.text = str(instrDepManager.gaugeCtrl2)

    selectedGauge = SubElement(GeneralInfo, 'selectedGauge')
    selectedGauge.text = instrDepManager.selectedGauge
    # print instrDepManager.selectedGauge

    frequency = SubElement(GeneralInfo, 'frequency')
    frequency.text = instrDepManager.frequencyCmbo

    firmware = SubElement(GeneralInfo, 'firmware')
    firmware.text = instrDepManager.firmwareCmbo

    software = SubElement(GeneralInfo, 'software')
    software.text = instrDepManager.softwareCtrl

    manufacturer = SubElement(GeneralInfo, 'manufacturer')
    manufacturer.text = instrDepManager.manufactureCmbo

    model = SubElement(GeneralInfo, 'model')
    model.text = instrDepManager.modelCmbo

    #Midsection Panel
    MidsectionInfo = SubElement(InstrumentDeployment, 'MidsectionInfo', empty = 'False')
    panelsNum = SubElement(MidsectionInfo, 'panelsNum')
    panelsNum.text = str(instrDepManager.numOfPanelsScroll)

    flowAngle = SubElement(MidsectionInfo, 'flowAngle')
    flowAngle.text = str(instrDepManager.flowAngleCmbo)

    coeff = SubElement(MidsectionInfo, 'coeff')
    coeff.text = str(instrDepManager.coEffCtrl)

    method = SubElement(MidsectionInfo, 'method')
    method.text = instrDepManager.methodCmbo

    metres = SubElement(MidsectionInfo, 'metres')
    metres.text = instrDepManager.metresCtrl

    weight = SubElement(MidsectionInfo, 'weight')
    weight.text = instrDepManager.weightCtrl

    kglbs = SubElement(MidsectionInfo, 'kglbs')
    kglbs.text = str(instrDepManager.weightRadButBox)


    weightRadBut1 = SubElement(MidsectionInfo, 'weightRadBut1')
    weightRadBut1.text = str(instrDepManager.weightRadBut1)

    weightRadBut2 = SubElement(MidsectionInfo, 'weightRadBut2')
    weightRadBut2.text = str(instrDepManager.weightRadBut2)


    if flowAngle.text == '' and \
        coeff.text == '' and \
        method.text == '' and \
        metres.text == '' and \
        weight.text == '':
        MidsectionInfo.attrib['empty'] = 'True'
    if check is not None:
        if 'adcp' in check.lower():
            MidsectionInfo.attrib['empty'] = 'True'


    #ADCP Panel
    ADCPInfo = SubElement(InstrumentDeployment, 'ADCPInfo', empty = 'False')


    configChoice = SubElement(ADCPInfo, 'configChoice')
    configChoice.text = str(instrDepManager.configCmbo)

    configVal = SubElement(ADCPInfo, 'configVal')
    configVal.text = instrDepManager.configCtrl

    ADCPSetToClock = SubElement(ADCPInfo, 'ADCPSetToClock')
    ADCPSetToClock.text = str(instrDepManager.adcpSetToClockCB)

    diagnosticTest = SubElement(ADCPInfo, 'diagnosticTest')
    diagnosticTest.text = str(instrDepManager.diagTestCB)

    depth = SubElement(ADCPInfo, 'depth')
    depth.text = instrDepManager.adcpDepthCtrl

    magDecl = SubElement(ADCPInfo, 'magDecl')
    magDecl.text = instrDepManager.magnDeclCtrl

    compassCali = SubElement(ADCPInfo, 'compassCali')
    compassCali.text = str(instrDepManager.compassCaliCB)

    passedRev = SubElement(ADCPInfo, 'passedRev')
    passedRev.text = str(instrDepManager.passedFieldRevCB)

    # if frequency.text == '' and \
    #     firmware.text == '' and \
    #     software.text == '' and \
    if configChoice.text == '' and \
        configVal.text == '' and \
        not instrDepManager.adcpSetToClockCB and \
        not instrDepManager.diagTestCB and \
        depth.text == '' and \
        magDecl.text == '' and \
        not instrDepManager.compassCaliCB and \
        not instrDepManager.passedFieldRevCB:
        ADCPInfo.attrib['empty'] = 'True'


    #Control Panel
    Control = SubElement(InstrumentDeployment, 'Control')
    condition = SubElement(Control, 'condition')
    condition.text = str(instrDepManager.controlConditionCmbo)

##    effectCat = SubElement(Control, 'effectCat')
##    effectCat.text = str(instrDepManager.controlEffCatCmbo)

##    effectSubCat = SubElement(Control, 'effectSubCat')
##    effectSubCat.text = str(instrDepManager.controlEffSubCatCmbo)

    # controlRemark = SubElement(Control, 'controlRemark')
    # controlRemark.text = str(instrDepManager.controlRemarksCtrl)
    # print controlRemark.text
    # result = ''
    # for c in controlRemark.text:
    #     if c == '\n':
    #         c='<br/>'
    #     result += c
    # print result
    # controlRemark.text = result
    dischargeRemark = SubElement(Control, 'dischargeRemark')
    # dischargeRemark.text = str(instrDepManager.dischRemarksCtrl)
    dischargeRemark.text = instrDepManager.dischRemarksCtrl#.encode('utf-8')

    stageRemark = SubElement(Control, 'stageRemark')
    stageRemark.text = instrDepManager.stageRemarksCtrl#.encode('utf-8')
    # stageRemark.text = str(instrDepManager.stageRemarksCtrl)

    stationHealthRemark = SubElement(Control, 'stationHealthRemark')
    stationHealthRemark.text = instrDepManager.stationHealthRemarksCtrl#.encode('utf-8')
    # stationHealthRemark.text = str(instrDepManager.stationHealthRemarksCtrl)

    pictured = SubElement(Control, "pictured")
    pictured.text = str(instrDepManager.GetPicturedCkboxVal())


# Set Instrument and Deployment Information variables from existing XML structure
def InstrumentDepFromXML(InstrumentDeployment, instrDepManager):
    instrDepManager.gui.CheckListReset()

    GeneralInfo = InstrumentDeployment.find('GeneralInfo')
    method = GeneralInfo.find('methodType').text
    instrDepManager.methodCBListBox = "" if method is None else method
    instrDepManager.OnDeploymentUpdate()

    deployment = GeneralInfo.find('deployment').text
    instrDepManager.deploymentCmbo = "" if deployment is None else deployment

    position = GeneralInfo.find('position').text
    instrDepManager.positionMethodCtrl = "" if position is None else position

    serialNum = GeneralInfo.find('serialNum').text
    instrDepManager.serialCmboFromXml = "" if serialNum is None else serialNum

    instrument = GeneralInfo.find('instrument').text
    instrDepManager.instrumentCmbo = "" if instrument is None else instrument



    gauge1 = GeneralInfo.find('gauge1').text
    instrDepManager.gaugeCtrl = "" if gauge1 is None else gauge1

    length = GeneralInfo.find('length').text
    instrDepManager.lengthRadButBox = 0 if length is None else int(length)

    gaugePos = GeneralInfo.find('gaugePos').text
    instrDepManager.posRadButBox = 0 if gaugePos is None else int(gaugePos)

    # gauge2 = GeneralInfo.find('gauge2').text
    # instrDepManager.gaugeCtrl2 = "" if gauge2 is None else gauge2

    try:
        frequency = GeneralInfo.find('frequency').text
        instrDepManager.frequencyCmbo = "" if frequency is None else frequency

        firmware = GeneralInfo.find('firmware').text
        instrDepManager.firmwareCmbo = "" if firmware is None else firmware

        software = GeneralInfo.find('software').text
        instrDepManager.softwareCtrl = "" if software is None else software
    except:
        pass

    try:
        manufacturer = GeneralInfo.find('manufacturer').text
        instrDepManager.manufactureCmboFromXml = "" if manufacturer is None else manufacturer

        model = GeneralInfo.find('model').text
        instrDepManager.modelCmbo = "" if model is None else model
    except:
        pass

    try:

        selectedGauge = GeneralInfo.find('selectedGauge').text

        instrDepManager.selectedGauge = selectedGauge if selectedGauge != '' or not None else "gauge"

    except:
        instrDepManager.selectedGauge = "gauge"


    #MIDSECTION
    MidsectionInfo = InstrumentDeployment.find('MidsectionInfo')
    MidsectionInfo = InstrumentDeployment.find('MidsectionMethod') if MidsectionInfo is None else MidsectionInfo
    # panelsNum = MidsectionInfo.find('panelsNum').text
    # if panelsNum is not None:
    #     instrDepManager.numOfPanelsScroll = int(panelsNum)

    panelsNum = MidsectionInfo.find('panelsNum').text
    instrDepManager.numOfPanelsScroll = "" if panelsNum is None else panelsNum

    flowAngle = MidsectionInfo.find('flowAngle').text
    instrDepManager.flowAngleCmbo = "" if flowAngle is None else flowAngle

    coeff = MidsectionInfo.find('coeff').text
    instrDepManager.coEffCtrl = "" if coeff is None else coeff

    method = MidsectionInfo.find('method').text
    instrDepManager.methodCmbo = "" if method is None else method

    metres = MidsectionInfo.find('metres').text
    instrDepManager.metresCtrl = "" if metres is None else metres

    weight = MidsectionInfo.find('weight').text
    instrDepManager.weightCtrl = "" if weight is None else weight

    kglbs = MidsectionInfo.find('kglbs').text
    instrDepManager.weightRadButBox = 0 if kglbs is None else int(kglbs)


    try:
        weightRadBut1 = MidsectionInfo.find('weightRadBut1').text
        if weightRadBut1 == "True":
            instrDepManager.weightRadBut1 = True
        else:
            instrDepManager.weightRadBut2 = True
    except:
        pass

    #ADCP
    ADCPInfo = InstrumentDeployment.find('ADCPInfo')
    ADCPInfo = InstrumentDeployment.find('ADCPMethod') if ADCPInfo is None else ADCPInfo


    configChoice = ADCPInfo.find('configChoice').text
    instrDepManager.configCmbo = "" if configChoice is None else configChoice

    configVal = ADCPInfo.find('configVal').text
    instrDepManager.configCtrl = "" if configVal is None else configVal

    ADCPSetToClock = ADCPInfo.find('ADCPSetToClock').text
    instrDepManager.adcpSetToClockCB = False if ADCPSetToClock is None else (False if ADCPSetToClock == 'False' else True)

    diagnosticTest = ADCPInfo.find('diagnosticTest').text
    instrDepManager.diagTestCB = False if diagnosticTest is None else (False if diagnosticTest == 'False' else True)

    depth = ADCPInfo.find('depth').text
    instrDepManager.adcpDepthCtrl = "" if depth is None else depth

    magDecl = ADCPInfo.find('magDecl').text
    instrDepManager.magnDeclCtrl = "" if magDecl is None else magDecl

    compassCali = ADCPInfo.find('compassCali').text
    instrDepManager.compassCaliCB = False if compassCali is None else (False if compassCali == 'False' else True)

    passedRev = ADCPInfo.find('passedRev').text
    instrDepManager.passedFieldRevCB = False if passedRev is None else (False if passedRev == 'False' else True)


    #Control
    Control = InstrumentDeployment.find('Control')
    condition = Control.find('condition').text
    instrDepManager.controlConditionCmbo = "" if condition is None else condition

##    effectCat = Control.find('effectCat').text
##    instrDepManager.controlEffCatCmbo = "" if effectCat is None else effectCat

##    effectSubCat = Control.find('effectSubCat').text
##    instrDepManager.controlEffSubCatCmbo = "" if effectSubCat is None else effectSubCat

    # controlRemark = Control.find('controlRemark').text
    # instrDepManager.controlRemarksCtrl = "" if controlRemark is None else controlRemark

    dischargeRemark = Control.find('dischargeRemark').text
    instrDepManager.dischRemarksCtrl = "" if dischargeRemark is None else dischargeRemark

    stageRemark = Control.find('stageRemark').text
    instrDepManager.stageRemarksCtrl = "" if stageRemark is None else stageRemark

    try:
        stationHealthRemark = Control.find('stationHealthRemark').text
    except:
        stationHealthRemark = None
    instrDepManager.stationHealthRemarksCtrl = "" if stationHealthRemark is None else stationHealthRemark


    try:
        pictured = Control.find('pictured').text
        if pictured == "True":
            instrDepManager.SetPicturedCkboxVal(True)
        else:
            instrDepManager.SetPicturedCkboxVal(False)

    except:
        print "no pictured ckeckbox for field review in xml"


# Create XML structure for Party Information
def PartyInfoAsXMLTree(PartyInfo, partyInfoManager):
    party = SubElement(PartyInfo, 'party')
    party.text = partyInfoManager.partyCtrl

    completed = SubElement(PartyInfo, 'completed')
    completed.text = partyInfoManager.completeCtrl

    checked = SubElement(PartyInfo, 'checked')
    checked.text = partyInfoManager.checkCtrl

    reviewed = SubElement(PartyInfo, 'reviewed')
    reviewed.text = str(partyInfoManager.reviewedCB)

# Set Party Information variables from existing XML structure
def PartyInfoFromXML(PartyInfo, partyInfoManager):
    party = PartyInfo.find('party').text
    partyInfoManager.partyCtrl = "" if party is None else party

    completed = PartyInfo.find('completed').text
    partyInfoManager.completeCtrl = "" if completed is None else completed

    checked = PartyInfo.find('checked').text
    partyInfoManager.checkCtrl = "" if checked is None else checked

    reviewed = None if PartyInfo.find('reviewed') is None else PartyInfo.find('reviewed').text
    partyInfoManager.reviewedCB = False if reviewed is None else (False if reviewed == 'False' else True)


# Create XML structure for Level Checks
def LevelChecksAsXMLTree(LevelChecks, waterLevelRunManager):

    # LevelOrAnnual = SubElement(LevelChecks, 'LevelOrAnnual')
    # LevelOrAnnual.text = "GC" if waterLevelRunManager.gaugeCheck else ("DC" if waterLevelRunManager.datumCheck else "BC")


    runSizer = waterLevelRunManager.runSizer
    for i in range(len(runSizer.GetChildren())):
        notEmptyTable = False


        LevelChecksTable = SubElement(LevelChecks, 'LevelChecksTable', run=str(i))

        for j in range(len(waterLevelRunManager.GetLevelNotesSizerV(i).GetChildren()) - 1):


            stationText = waterLevelRunManager.GetLevelNotesStation(i, j).GetValue() if waterLevelRunManager.GetLevelNotesStation(i, j).GetValue() is not None else ''
            backsightText = waterLevelRunManager.GetLevelNotesBacksight(i, j).GetValue() if waterLevelRunManager.GetLevelNotesBacksight(i, j).GetValue() is not None else ''
            heightOfInstrumentText = waterLevelRunManager.GetLevelNotesHI(i, j).GetValue() if waterLevelRunManager.GetLevelNotesHI(i, j).GetValue() is not None else ''
            foresightText = waterLevelRunManager.GetLevelNotesForesight(i, j).GetValue() if waterLevelRunManager.GetLevelNotesForesight(i, j).GetValue() is not None else ''
            elevationText = waterLevelRunManager.GetLevelNotesElevation(i, j).GetValue() if waterLevelRunManager.GetLevelNotesElevation(i, j).GetValue() is not None else ''
            establishText = waterLevelRunManager.GetLevelNotesEstablishedElevation(i, j).GetValue() if waterLevelRunManager.GetLevelNotesEstablishedElevation(i, j).GetValue() is not None else ''
            commentsText = waterLevelRunManager.GetLevelNotesComments(i, j).GetValue() if waterLevelRunManager.GetLevelNotesComments(i, j).GetValue() is not None else ''


            notEmptyRow = False

            if stationText != "" and stationText is not None:
                notEmptyRow = True
            if backsightText != "" and backsightText is not None:
                notEmptyRow = True
            if heightOfInstrumentText != "" and heightOfInstrumentText is not None:
                notEmptyRow = True
            if foresightText != "" and foresightText is not None:
                notEmptyRow = True
            if elevationText != "" and elevationText is not None:
                notEmptyRow = True
            if establishText != "" and establishText is not None:
                notEmptyRow = True
            if commentsText != "" and commentsText is not None:
                notEmptyRow = True

            if notEmptyRow:
                # Add row to the LevelChecksTable

                LevelChecksRow = SubElement(LevelChecksTable, 'LevelChecksRow', row=str(j))
                station = SubElement(LevelChecksRow, 'station')
                station.text = stationText

                backsight = SubElement(LevelChecksRow, 'backsight')
                backsight.text = backsightText

                htInst = SubElement(LevelChecksRow, 'htInst')
                htInst.text = heightOfInstrumentText

                foresight = SubElement(LevelChecksRow, 'foresight')
                foresight.text = foresightText

                elevation = SubElement(LevelChecksRow, 'elevation')
                elevation.text = elevationText

                establish = SubElement(LevelChecksRow, 'establish')
                establish.text = establishText

                comments = SubElement(LevelChecksRow, 'comments')
                comments.text = commentsText

                notEmptyTable = True

        #Summary Info
        if notEmptyTable:
            closure = SubElement(LevelChecksTable, "closure")
            closure.text = str(waterLevelRunManager.GetClosureText(i).GetValue())



    #Level Checks Summary
    LevelChecksSummaryTable = SubElement(LevelChecks, "LevelChecksSummaryTable")

    for i in range(len(waterLevelRunManager.timeValSizer.GetChildren())):
        SummaryTableRow = SubElement(LevelChecksSummaryTable, "SummaryTableRow", row=str(i))

        time = SubElement(SummaryTableRow, "time")
        time.text = str(waterLevelRunManager.GetTimeVal(int(i)))

        reference = SubElement(SummaryTableRow, "reference")
        reference.text = waterLevelRunManager.GetWLRefVal(int(i))

        waterLevel = SubElement(SummaryTableRow, 'waterLevel')
        waterLevel.text = waterLevelRunManager.GetElevationVal(int(i))

        dist = SubElement(SummaryTableRow, "dist")
        dist.text = waterLevelRunManager.GetDtWSVal(int(i))

        # updown = SubElement(SummaryTableRow, "updown")
        # updown.text = str(waterLevelRunManager.GetUpDownVal(int(i)))

        surge = SubElement(SummaryTableRow, 'surge')
        surge.text = waterLevelRunManager.GetSurgeVal(int(i))

        wlElev = SubElement(SummaryTableRow, 'wlElev')
        wlElev.text = waterLevelRunManager.GetWLElevVal(int(i))


        datum = SubElement(SummaryTableRow, 'datum')
        datum.text = waterLevelRunManager.GetDatumVal(int(i))

        cwl = SubElement(SummaryTableRow, 'cwl')
        cwl.text = waterLevelRunManager.GetCwlVal(int(i))

        loggerReading = SubElement(SummaryTableRow, 'loggerReading')
        loggerReading.text = waterLevelRunManager.GetLoggerReadingVal(int(i))

        loggerReading2 = SubElement(SummaryTableRow, 'loggerReading2')
        loggerReading2.text = waterLevelRunManager.GetLoggerReadingVal2(int(i))



    comments = SubElement(LevelChecks, 'comments')
    comments.text = waterLevelRunManager.commentsCtrl

    loggerName = SubElement(LevelChecks, 'loggerName')
    loggerName.text = waterLevelRunManager.HGHeaderCtrl

    loggerName2 = SubElement(LevelChecks, 'loggerName2')
    loggerName2.text = waterLevelRunManager.HG2HeaderCtrl

# Set Level Checks variables from existing XML structure
def LevelChecksFromXML(LevelChecks, waterLevelRunManager):
    runSizer = waterLevelRunManager.runSizer
    #Reset Table

    for i in range(len(runSizer.GetChildren())):
        waterLevelRunManager.RemoveRun(0)

    #Remove all previous summaries
    for i in range(len(waterLevelRunManager.timeValSizer.GetChildren())):
        waterLevelRunManager.gui.RemoveEntry(0)

    waterLevelRunManager.commentsCtrl = ""
    index = 0
    for LevelChecksTable in LevelChecks.findall('LevelChecksTable'):

        waterLevelRunManager.AddRun()

        for LevelChecksRow in LevelChecksTable.findall('LevelChecksRow'):

            row = int(LevelChecksRow.get('row'))
            if row > 5:
                waterLevelRunManager.AddEntry(index)


        #Level Checks Summary + closure
        try:
            closure = LevelChecksTable.find('closure').text
            waterLevelRunManager.GetClosureText(index).SetValue(closure)
        except:
            waterLevelRunManager.GetClosureText(index).SetValue("")

        index += 1

    # waterLevelRunManager.manager.gui.LoadDefaultConfig()

    for LevelChecksTable in LevelChecks.findall('LevelChecksTable'):
        if LevelChecksTable.get('run') is not None:
            run = int(LevelChecksTable.get('run'))

            rowIndex = -1
            for LevelChecksRow in LevelChecksTable.findall('LevelChecksRow'):
                rowIndex += 1
                row = int(LevelChecksRow.get('row'))
                if rowIndex != row:
                    waterLevelRunManager.AddEntry(run)
                    rowIndex = row
                station = LevelChecksRow.find('station').text
                backsight = LevelChecksRow.find('backsight').text
                htInst = LevelChecksRow.find('htInst').text
                foresight = LevelChecksRow.find('foresight').text
                elevation = LevelChecksRow.find('elevation').text
                try:
                    establish = LevelChecksRow.find('establish').text
                except:
                    establish = None
                comments = LevelChecksRow.find('comments').text

                waterLevelRunManager.GetLevelNotesStation(run, row).ChangeValue("" if station is None else station)
                waterLevelRunManager.GetLevelNotesBacksight(run, row).ChangeValue("" if backsight is None else backsight)
                waterLevelRunManager.GetLevelNotesHI(run, row).ChangeValue("" if htInst is None else htInst)
                waterLevelRunManager.GetLevelNotesForesight(run, row).ChangeValue("" if foresight is None else foresight)
                waterLevelRunManager.GetLevelNotesElevation(run, row).SetValue("" if elevation is None else elevation)
                waterLevelRunManager.GetLevelNotesEstablishedElevation(run, row).SetValue("" if establish is None else establish)
                waterLevelRunManager.GetLevelNotesComments(run, row).ChangeValue("" if comments is None else comments)




                waterLevelRunManager.EnableEntry(run, row, True)

            waterLevelRunManager.FindMatchBM(run)






    # try:
    #     annual = LevelChecks.find('LevelOrAnnual').text
    # except (RuntimeError, AttributeError):
    #     annual = "GC"
    # if annual == "DC":
    #     waterLevelRunManager.datumCheck = True
    # elif annual == "BC":
    #     waterLevelRunManager.bothCheck = True
    # else:
    #     waterLevelRunManager.gaugeCheck = True




    LevelChecksSummaryTable = LevelChecks.find('LevelChecksSummaryTable')

    for row, SummaryTableRow in enumerate(LevelChecksSummaryTable.findall('SummaryTableRow')):
        waterLevelRunManager.gui.AddEntry()

        time = SummaryTableRow.find('time').text
        reference = SummaryTableRow.find('reference').text
        waterLevel = SummaryTableRow.find('waterLevel').text
        dist = SummaryTableRow.find('dist').text
        # updown = SummaryTableRow.find('updown').text
        surge = SummaryTableRow.find('surge').text
        wlElev = SummaryTableRow.find('wlElev').text
        try:
            datum = SummaryTableRow.find('datum').text
        except (RuntimeError, AttributeError):
            datum = ""
        try:
            cwl = SummaryTableRow.find('cwl').text
        except (RuntimeError, AttributeError):
            cwl = ""
        try:
            logger = SummaryTableRow.find('loggerReading').text
        except (RuntimeError, AttributeError):
            logger = ""

        try:
            logger2 = SummaryTableRow.find('loggerReading2').text
        except (RuntimeError, AttributeError):
            logger2 = ""

        waterLevelRunManager.SetTimeVal(row, "" if time is None else time)
        waterLevelRunManager.SetWLRefVal(row, "" if reference is None else reference)
        waterLevelRunManager.SetElevationVal(row, "" if waterLevel is None else waterLevel)
        waterLevelRunManager.SetDtWSVal(row, "" if dist is None else dist)
        # waterLevelRunManager.SetUpDownVal(row, "" if updown is None else updown)
        waterLevelRunManager.SetSurgeVal(row, "" if surge is None else surge)
        waterLevelRunManager.SetWLElevVal(row, "" if wlElev is None else wlElev)
        waterLevelRunManager.SetDatumVal(row, "" if datum is None else datum)
        waterLevelRunManager.SetCwlVal(row, "" if cwl is None else cwl)
        waterLevelRunManager.SetLoggerReadingVal(row, "" if logger is None else logger)
        waterLevelRunManager.SetLoggerReadingVal2(row, "" if logger2 is None else logger2)


    comments = LevelChecks.find('comments').text
    waterLevelRunManager.commentsCtrl = "" if comments is None else comments

    try:
        loggerName = LevelChecks.find('loggerName').text
        waterLevelRunManager.HGHeaderCtrl = "" if loggerName is None else loggerName
    except:
        waterLevelRunManager.HGHeaderCtrl = ""


    try:
        loggerName2 = LevelChecks.find('loggerName2').text
        waterLevelRunManager.HG2HeaderCtrl = "" if loggerName2 is None else loggerName2
    except:
        waterLevelRunManager.HG2HeaderCtrl = ""


# # Create XML structure for Annual Level Checks
# def AnnualLevelsAsXMLTree(AnnualLevels, annualLevelNotesManager):
#     AnnualLevelsTable = SubElement(AnnualLevels, 'AnnualLevelsTable')

#     #Water Level Notes Table
#     for i in range(1, len(annualLevelNotesManager.levelNotesSizer.GetChildren())):
#         stationText = str(annualLevelNotesManager.GetTableValue(i - 1, 0))
#         backsightText = str(annualLevelNotesManager.GetTableValue(i - 1, 1))
#         heightOfInstrumentText = str(annualLevelNotesManager.GetTableValue(i - 1, 2))
#         foresightText = str(annualLevelNotesManager.GetTableValue(i - 1, 3))
#         elevationText = str(annualLevelNotesManager.GetTableValue(i - 1, 4))
#         physDescText = str(annualLevelNotesManager.GetTableValue(i - 1, 5))
#         commentsText = unicode(annualLevelNotesManager.GetTableValue(i - 1, 6))

#         notEmptyRow = False
#         if stationText != "":
#             notEmptyRow = True
#         if backsightText != "":
#             notEmptyRow = True
#         if heightOfInstrumentText != "":
#             notEmptyRow = True
#         if foresightText != "":
#             notEmptyRow = True
#         if elevationText != "":
#             notEmptyRow = True
#         if physDescText != "":
#             notEmptyRow = True
#         if commentsText != "":
#             notEmptyRow = True


#         if notEmptyRow:
#             #Add row to the LevelChecksTable
#             AnnualLevelsRow = SubElement(AnnualLevelsTable, 'LevelChecksRow', row=str(i - 1))
#             station = SubElement(AnnualLevelsRow, 'station')
#             station.text = stationText

#             backsight = SubElement(AnnualLevelsRow, 'backsight')
#             backsight.text = backsightText

#             htInst = SubElement(AnnualLevelsRow, 'htInst')
#             htInst.text = heightOfInstrumentText

#             foresight = SubElement(AnnualLevelsRow, 'foresight')
#             foresight.text = foresightText

#             elevation = SubElement(AnnualLevelsRow, 'elevation')
#             elevation.text = elevationText

#             physDesc = SubElement(AnnualLevelsRow, 'physDesc')
#             physDesc.text = physDescText

#             comments = SubElement(AnnualLevelsRow, 'comments')
#             comments.text = commentsText

#     #Closure
#     closure = SubElement(AnnualLevelsTable, "closure")
#     closure.text = annualLevelNotesManager.closure

# # Set Annual Level Checks variables from existing XML structure
# def AnnualLevelsFromXML(AnnualLevels, annualLevelNotesManager):

#     for row in range(len(annualLevelNotesManager.levelNotesSizer.GetChildren()) - 1):
#         annualLevelNotesManager.SetTableValue(row, 0, "")
#         annualLevelNotesManager.SetTableValue(row, 1, "")
#         annualLevelNotesManager.SetTableValue(row, 2, "")
#         annualLevelNotesManager.SetTableValue(row, 3, "")
#         annualLevelNotesManager.SetTableValue(row, 4, "")
#         annualLevelNotesManager.SetTableValue(row, 5, "")
#         annualLevelNotesManager.SetTableValue(row, 6, "")

#     AnnualLevelsTable = AnnualLevels.find('AnnualLevelsTable')

#     for LevelChecksRow in AnnualLevelsTable.findall('LevelChecksRow'):
#         row = int(LevelChecksRow.get('row'))

#         station = LevelChecksRow.find('station').text
#         backsight = LevelChecksRow.find('backsight').text
#         htInst = LevelChecksRow.find('htInst').text
#         foresight = LevelChecksRow.find('foresight').text
#         elevation = LevelChecksRow.find('elevation').text
#         physDesc = LevelChecksRow.find('physDesc').text
#         comments = LevelChecksRow.find('comments').text

#         annualLevelNotesManager.SetTableValue(row, 0, "" if station is None else station)
#         annualLevelNotesManager.SetTableValue(row, 1, "" if backsight is None else backsight)
#         annualLevelNotesManager.SetTableValue(row, 2, "" if htInst is None else htInst)
#         annualLevelNotesManager.SetTableValue(row, 3, "" if foresight is None else foresight)
#         annualLevelNotesManager.SetTableValue(row, 4, "" if elevation is None else elevation)
#         annualLevelNotesManager.SetTableValue(row, 5, "" if physDesc is None else physDesc)
#         annualLevelNotesManager.SetTableValue(row, 6, "" if comments is None else comments)

#     closure = AnnualLevelsTable.find('closure').text
#     annualLevelNotesManager.closure = "" if closure is None else closure


# Create XML structure for Field Review Checklist
def FieldReviewAsXMLTree(FieldReview, frChecklistManager):
    passElement = SubElement(FieldReview, "pass")
    passElement.text = str(frChecklistManager.passCB)

    depType = SubElement(FieldReview, "dependencyType")
    depType.text = str(frChecklistManager.depType)

    midsecType = SubElement(FieldReview, "midsectionType")
    midsecType.text = str(frChecklistManager.midsecType)

    FieldReviewTable = SubElement(FieldReview, "FieldReviewTable")
    for i in range(len(frChecklistManager.cbCheckSizer.GetChildren())):
        FieldReviewTableRow = SubElement(FieldReviewTable, "FieldReviewTableRow", row=str(i))

        label = SubElement(FieldReviewTableRow, "label")
        label.text = unicode(frChecklistManager.GetLabelSizerVal(i))

        checked = SubElement(FieldReviewTableRow, "checked")
        checked.text = str(frChecklistManager.GetCBCheckSizerVal(i))

        reviewed = SubElement(FieldReviewTableRow, "reviewed")
        reviewed.text = str(frChecklistManager.GetCBRevSizerVal(i))

        text = SubElement(FieldReviewTableRow, "text")
        text.text = frChecklistManager.GetCtrlSizerVal(i)

    siteNotes = SubElement(FieldReview, "siteNotes")
    siteNotes.text = frChecklistManager.siteNotesCtrl

    # pictured = SubElement(FieldReview, "pictured")
    # pictured.text = str(frChecklistManager.GetPicturedCkbox())


# Set Field Review Checklist variables from existing XML structure
def FieldReviewFromXML(FieldReview, frChecklistManager):
    passVal = FieldReview.find('pass').text
    frChecklistManager.passCB = False if passVal is None else (False if passVal == 'False' else True)

    depType = FieldReview.find('dependencyType').text
    frChecklistManager.depType = "" if depType is None else depType
    midsecType = FieldReview.find('midsectionType').text
    frChecklistManager.midsecType = "" if midsecType is None else midsecType


    FieldReviewTable = FieldReview.find('FieldReviewTable')

    for FieldReviewTableRow in FieldReviewTable.findall('FieldReviewTableRow'):
        row = int(FieldReviewTableRow.get('row'))

        checked = FieldReviewTableRow.find('checked').text
        reviewed = FieldReviewTableRow.find('reviewed').text
        text = FieldReviewTableRow.find('text').text

        frChecklistManager.SetCBCheckSizerVal(row, False if checked is None else (False if checked == 'False' else True))
        frChecklistManager.SetCBRevSizerVal(row, False if reviewed is None else (False if reviewed == 'False' else True))
        frChecklistManager.SetCtrlSizerVal(row, "" if text is None else text)

    siteNotes = FieldReview.find('siteNotes').text
    frChecklistManager.siteNotesCtrl = "" if siteNotes is None else siteNotes

    # try:
    #     pictured = FieldReview.find('pictured').text
    #     if pictured == "True":
    #         frChecklistManager.SetPicturedCkbox(True)
    #     else:
    #         frChecklistManager.SetPicturedCkbox(False)

    # except:
    #     print "no pictured ckeckbox for field review in xml"

# Create XML structure for Moving Boat Method information
def MovingBoatMeasAsXMLTree(MovingBoatMeas, movingBoatMeasurementsManager):
    bedMaterial = SubElement(MovingBoatMeas, "bedMaterial")
    bedMaterial.text = movingBoatMeasurementsManager.bedMatCmbo

    mbTest = SubElement(MovingBoatMeas, "mbTest")
    mbTest.text = str(movingBoatMeasurementsManager.mbCB)

    mbTestChoice = SubElement(MovingBoatMeas, "mbTestChoice")
    mbTestChoice.text = movingBoatMeasurementsManager.mbCmbo

    detected = SubElement(MovingBoatMeas, "detected")
    detected.text = movingBoatMeasurementsManager.detectedCtrl

    trackRefChoice = SubElement(MovingBoatMeas, "trackRefChoice")
    trackRefChoice.text = movingBoatMeasurementsManager.trackRefCmbo

    leftBankChoice = SubElement(MovingBoatMeas, "leftBankChoice")
    leftBankChoice.text = movingBoatMeasurementsManager.leftBankCmbo
    leftBank = SubElement(MovingBoatMeas, "leftBank")
    leftBank.text = movingBoatMeasurementsManager.leftBankOtherCtrl

    rightBankChoice = SubElement(MovingBoatMeas, "rightBankChoice")
    rightBankChoice.text = movingBoatMeasurementsManager.rightBankCmbo
    rightBank = SubElement(MovingBoatMeas, "rightBank")
    rightBank.text = movingBoatMeasurementsManager.rightBankOtherCtrl

    edgeDistMmntMethod = SubElement(MovingBoatMeas, "edgeDistMmntMethod")
    edgeDistMmntMethod.text = movingBoatMeasurementsManager.edgeDistMmntCmbo


    compositeTrackCmbo = SubElement(MovingBoatMeas, "compositeTrackCmbo")
    compositeTrackCmbo.text = movingBoatMeasurementsManager.compositeTrackCmbo

    depthRefCmbo = SubElement(MovingBoatMeas, "depthRefCmbo")
    depthRefCmbo.text = movingBoatMeasurementsManager.depthRefCmbo

    velocityTopCombo = SubElement(MovingBoatMeas, "velocityTopCombo")
    velocityTopCombo.text = movingBoatMeasurementsManager.velocityTopCombo

    velocityBottomCombo = SubElement(MovingBoatMeas, "velocityBottomCombo")
    velocityBottomCombo.text = movingBoatMeasurementsManager.velocityBottomCombo

    velocityExponentCtrl = SubElement(MovingBoatMeas, "velocityExponentCtrl")
    velocityExponentCtrl.text = movingBoatMeasurementsManager.velocityExponentCtrl

    differenceCtrl = SubElement(MovingBoatMeas, "differenceCtrl")
    differenceCtrl.text = movingBoatMeasurementsManager.differenceCtrl


    # lock = SubElement(MovingBoatMeas, "lock")
    # lock.text = str(movingBoatMeasurementsManager.lockCB)

    ADCPMeasTable = SubElement(MovingBoatMeas, "ADCPMeasTable")
    for i in range(1, len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 1):
        checked = str(movingBoatMeasurementsManager.GetTableValue(i - 1, 1))
        transectIDText = movingBoatMeasurementsManager.GetTableValue(i - 1, 2)
        startBankText = str(movingBoatMeasurementsManager.GetTableValue(i - 1, 3))
        startTimeText = movingBoatMeasurementsManager.GetTableValue(i - 1, 4)
        startDistanceText = movingBoatMeasurementsManager.GetTableValue(i - 1, 5)
        endDistanceText = movingBoatMeasurementsManager.GetTableValue(i - 1, 6)
        rawDischargeText = movingBoatMeasurementsManager.GetTableValue(i - 1, 7)
        # finalDisText = movingBoatMeasurementsManager.GetTableValue(i - 1, 8)
        remarksText = movingBoatMeasurementsManager.GetTableValue(i - 1, 8)

        notEmptyRow = False
        if transectIDText == "True":
            notEmptyRow = True
        if transectIDText != "":
            notEmptyRow = True
        if startBankText != "" and startBankText != "None":
            notEmptyRow = True
        if  "00:00" not in startTimeText:
            notEmptyRow = True
        if startDistanceText != "":
            notEmptyRow = True
        if endDistanceText != "":
            notEmptyRow = True
        if rawDischargeText != "":
            notEmptyRow = True
        if remarksText != "":
            notEmptyRow = True
        # if finalDisText != "":
        #     notEmptyRow = True

        if notEmptyRow:
            ADCPMeasRow = SubElement(ADCPMeasTable, "ADCPMeasRow", row=str(i - 1))
            checkbox = SubElement(ADCPMeasRow, "checkbox")
            checkbox.text = checked

            transectID = SubElement(ADCPMeasRow, "transectID")
            transectID.text = transectIDText

            startBank = SubElement(ADCPMeasRow, "startBank")
            startBank.text = startBankText

            startTime = SubElement(ADCPMeasRow,"startTime")
            startTime.text = startTimeText

            startDistance = SubElement(ADCPMeasRow, "startDistance")
            startDistance.text = startDistanceText

            endDistance = SubElement(ADCPMeasRow, "endDistance")
            endDistance.text = endDistanceText

            rawDischarge = SubElement(ADCPMeasRow, "rawDischarge")
            rawDischarge.text = rawDischargeText

            # finalDischarge = SubElement(ADCPMeasRow, "finalDischarge")
            # finalDischarge.text = finalDisText

            remarks = SubElement(ADCPMeasRow, "remarks")
            remarks.text = remarksText

            white = 'White'
            grey = 'Grey'

            if movingBoatMeasurementsManager.GetTableColor(i - 1, 2) == (255, 255, 255, 255):
                transectID.attrib['color'] = white
            else:
                transectID.attrib['color'] = grey
            if movingBoatMeasurementsManager.GetTableColor(i - 1, 5) == (255, 255, 255, 255):
                startDistance.attrib['color'] = white
            else:
                startDistance.attrib['color'] = grey
            if movingBoatMeasurementsManager.GetTableColor(i - 1, 6) == (255, 255, 255, 255):
                endDistance.attrib['color'] = white
            else:
                endDistance.attrib['color'] = grey
            if movingBoatMeasurementsManager.GetTableColor(i - 1, 7) == (255, 255, 255, 255):
                rawDischarge.attrib['color'] = white
            else:
                rawDischarge.attrib['color'] = grey
            # if movingBoatMeasurementsManager.GetTableColor(i - 1, 8) == (255, 255, 255, 255):
            #     finalDischarge.attrib['color'] = white
            # else:
            #     finalDischarge.attrib['color'] = grey
            if movingBoatMeasurementsManager.GetTableColor(i - 1, 8) == (255, 255, 255, 255):
                remarks.attrib['color'] = white
            else:
                remarks.attrib['color'] = grey



    ADCPMeasResults = SubElement(MovingBoatMeas, "ADCPMeasResults")

    mmntStartTime = SubElement(ADCPMeasResults, "mmntStartTime")
    mmntStartTime.text = movingBoatMeasurementsManager.mmntStartTimeCtrl

    mmntEndTime = SubElement(ADCPMeasResults, "mmntEndTime")
    mmntEndTime.text = movingBoatMeasurementsManager.mmntEndTimeCtrl

    mmntMeanTime = SubElement(ADCPMeasResults, "mmntMeanTime")
    mmntMeanTime.text = movingBoatMeasurementsManager.mmntMeanTimeCtrl

    rawDischargeMean = SubElement(ADCPMeasResults, "rawDischargeMean")
    rawDischargeMean.text = movingBoatMeasurementsManager.rawDischMeanCtrl

    mbCorrectionApplied = SubElement(ADCPMeasResults, "mbCorrectionApplied")
    mbCorrectionApplied.text = movingBoatMeasurementsManager.mbCorrAppCtrl

    finalDischargeMean = SubElement(ADCPMeasResults, "finalDischargeMean")
    finalDischargeMean.text = movingBoatMeasurementsManager.finalDischCtrl

    correctedMeanGaugeHeight = SubElement(ADCPMeasResults, "correctedMeanGaugeHeight")
    correctedMeanGaugeHeight.text = movingBoatMeasurementsManager.corrMeanGHCtrl

    baseCurveGaugeHeight = SubElement(ADCPMeasResults, "baseCurveGaugeHeight")
    baseCurveGaugeHeight.text = movingBoatMeasurementsManager.baseCurveGHCtrl

    calcBaseCurveDischarge = SubElement(ADCPMeasResults, "calcBaseCurveDischarge")
    calcBaseCurveDischarge.text = movingBoatMeasurementsManager.baseCurveDischCtrl

    standardDevMeanDischarge = SubElement(ADCPMeasResults, "standardDevMeanDischarge")
    standardDevMeanDischarge.text = movingBoatMeasurementsManager.standDevMeanDischCtrl

    calculateShiftforBaseCurve = SubElement(ADCPMeasResults, "calculateShiftforBaseCurve")
    calculateShiftforBaseCurve.text = movingBoatMeasurementsManager.calcShiftBaseCurveCtrl

    dischargeDifferenceBaseCurve = SubElement(ADCPMeasResults, "dischargeDifferenceBaseCurve")
    dischargeDifferenceBaseCurve.text = movingBoatMeasurementsManager.dischDiffBaseCurveCtrl

    comments = SubElement(ADCPMeasResults, "comments")
    comments.text = movingBoatMeasurementsManager.commentsCtrl

    if bedMaterial.text == '' and \
        not movingBoatMeasurementsManager.mbCB and \
        mbTestChoice.text == '' and \
        detected.text == '' and \
        trackRefChoice.text == '' and \
        leftBankChoice.text == '' and \
        rightBankChoice.text == '' and \
        edgeDistMmntMethod.text == '' and \
        len(ADCPMeasTable.findall('ADCPMeasRow')) <= 0 and \
        rawDischargeMean.text == '' and \
        mbCorrectionApplied.text == '' and \
        finalDischargeMean.text == '' and \
        standardDevMeanDischarge.text == '' and \
        comments.text == '':
        # calculateShiftforBaseCurve.text == '' and \
        # correctedMeanGaugeHeight.text == '' and \
        # baseCurveGaugeHeight.text == '' and \
        # calcBaseCurveDischarge.text == '' and \
        # dischargeDifferenceBaseCurve.text == '':
        MovingBoatMeas.attrib['empty'] = "True"

# Set Moving Boat Information variables from existing XML structure
def MovingBoatMeasFromXML(MovingBoatMeas, movingBoatMeasurementsManager):
    bedMaterial = MovingBoatMeas.find('bedMaterial').text
    movingBoatMeasurementsManager.bedMatCmbo = "" if bedMaterial is None else bedMaterial

    mbTest = MovingBoatMeas.find('mbTest').text
    movingBoatMeasurementsManager.mbCB = False if mbTest is None else (False if mbTest == 'False' else True)

    mbTestChoice = MovingBoatMeas.find('mbTestChoice').text
    movingBoatMeasurementsManager.mbCmbo = "" if mbTestChoice is None else mbTestChoice

    detected = MovingBoatMeas.find('detected').text
    movingBoatMeasurementsManager.detectedCtrl = "" if detected is None else detected

    trackRefChoice = MovingBoatMeas.find('trackRefChoice').text
    movingBoatMeasurementsManager.trackRefCmbo = "" if trackRefChoice is None else trackRefChoice

    leftBankChoice = MovingBoatMeas.find('leftBankChoice').text
    movingBoatMeasurementsManager.leftBankCmbo = "" if leftBankChoice is None else leftBankChoice



    rightBankChoice = MovingBoatMeas.find('rightBankChoice').text
    movingBoatMeasurementsManager.rightBankCmbo = "" if rightBankChoice is None else rightBankChoice

    try:
        leftBank = MovingBoatMeas.find('leftBank').text
        movingBoatMeasurementsManager.leftBankOtherCtrl = "" if leftBank is None else leftBank
    except:
        leftBank = ""
        movingBoatMeasurementsManager.leftBankOtherCtrl = ""

    try:
        rightBank = MovingBoatMeas.find('rightBank').text
        movingBoatMeasurementsManager.rightBankOtherCtrl = "" if rightBank is None else rightBank
    except:
        rightBank = ""
        movingBoatMeasurementsManager.rightBankOtherCtrl = ""


    if leftBankChoice == "Other":
        movingBoatMeasurementsManager.GetLeftBankOtherCtrl().Show()
    if rightBankChoice == "Other":
        movingBoatMeasurementsManager.GetRightBankOtherCtrl().Show()



    edgeDistMmntMethod = MovingBoatMeas.find('edgeDistMmntMethod').text
    movingBoatMeasurementsManager.edgeDistMmntCmbo = "" if edgeDistMmntMethod is None else edgeDistMmntMethod

    try:
        compositeTrackCmbo = MovingBoatMeas.find('compositeTrackCmbo').text
    except:
        compositeTrackCmbo = ""
    movingBoatMeasurementsManager.compositeTrackCmbo = "" if compositeTrackCmbo is None else compositeTrackCmbo

    try:
        depthRefCmbo = MovingBoatMeas.find('depthRefCmbo').text
    except:
        depthRefCmbo = ""
    movingBoatMeasurementsManager.depthRefCmbo = "" if depthRefCmbo is None else depthRefCmbo

    try:
        velocityTopCombo = MovingBoatMeas.find('velocityTopCombo').text
    except:
        velocityTopCombo = ""
    movingBoatMeasurementsManager.velocityTopCombo = "" if velocityTopCombo is None else velocityTopCombo


    try:
        velocityBottomCombo = MovingBoatMeas.find('velocityBottomCombo').text
    except:
        velocityBottomCombo = ""
    movingBoatMeasurementsManager.velocityBottomCombo = "" if velocityBottomCombo is None else velocityBottomCombo


    try:
        velocityExponentCtrl = MovingBoatMeas.find('velocityExponentCtrl').text
    except:
        velocityExponentCtrl = ""
    movingBoatMeasurementsManager.velocityExponentCtrl = "" if velocityExponentCtrl is None else velocityExponentCtrl



    try:
        differenceCtrl = MovingBoatMeas.find('differenceCtrl').text
    except:
        differenceCtrl = ""
    movingBoatMeasurementsManager.differenceCtrl = "" if differenceCtrl is None else differenceCtrl

    # lock = MovingBoatMeas.find('lock').text
    # movingBoatMeasurementsManager.lockCB = "" if lock is None else lock


    for row in range(len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 2):

        movingBoatMeasurementsManager.SetTableValue(row, 1, "False")
        movingBoatMeasurementsManager.SetTableValue(row, 2, "")
        movingBoatMeasurementsManager.SetTableValue(row, 3, "")
        movingBoatMeasurementsManager.SetTableValue(row, 4, "00:00:00")
        movingBoatMeasurementsManager.SetTableValue(row, 5, "")
        movingBoatMeasurementsManager.SetTableValue(row, 6, "")
        movingBoatMeasurementsManager.SetTableValue(row, 7, "")
        movingBoatMeasurementsManager.SetTableValue(row, 8, "")
        # movingBoatMeasurementsManager.SetTableValue(row, 9, "")


    ADCPMeasTable = MovingBoatMeas.find('ADCPMeasTable')
    counter = 0
    for ADCPMeasRow in ADCPMeasTable.findall('ADCPMeasRow'):
    	if counter > len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 3:
    		movingBoatMeasurementsManager.gui.AddEntry()
    	counter += 1
        row = int(ADCPMeasRow.get('row'))
        checked =  ADCPMeasRow.find('checkbox').text
        transectID = ADCPMeasRow.find('transectID').text
        startBank = ADCPMeasRow.find('startBank').text
        startTime = ADCPMeasRow.find('startTime').text
        startDistance = ADCPMeasRow.find('startDistance').text
        endDistance = ADCPMeasRow.find('endDistance').text
        rawDischarge = ADCPMeasRow.find('rawDischarge').text
        # finalDischarge = ADCPMeasRow.find('finalDischarge').text
        remarks = ADCPMeasRow.find('remarks').text



        transectIDColor = ADCPMeasRow.find('transectID').get('color')
        startDistanceColor = ADCPMeasRow.find('startDistance').get('color')
        endDistanceColor = ADCPMeasRow.find('endDistance').get('color')
        rawDischargeColor = ADCPMeasRow.find('rawDischarge').get('color')
        # finalDischargeColor = ADCPMeasRow.find('finalDischarge').get('color')
        remarksColor = ADCPMeasRow.find('remarks').get('color')


        movingBoatMeasurementsManager.SetTableValue(row, 1, "False" if checked is None else checked)
        movingBoatMeasurementsManager.SetTableValue(row, 2, "" if transectID is None else transectID)
        movingBoatMeasurementsManager.SetTableValue(row, 3, "" if startBank is None else startBank)
        movingBoatMeasurementsManager.SetTableValue(row, 4, "" if startTime is None else startTime)
        movingBoatMeasurementsManager.SetTableValue(row, 5, "" if startDistance is None else startDistance)
        movingBoatMeasurementsManager.SetTableValue(row, 6, "" if endDistance is None else endDistance)
        movingBoatMeasurementsManager.SetTableValue(row, 7, "" if rawDischarge is None else rawDischarge)
        # movingBoatMeasurementsManager.SetTableValue(row, 8, "" if finalDischarge is None else finalDischarge)
        movingBoatMeasurementsManager.SetTableValue(row, 8, "" if remarks is None else remarks)

        grey = (210, 210, 210)
        greyStr = 'Grey'
        white = 'White'

        if transectIDColor == greyStr:
            movingBoatMeasurementsManager.SetTableColor(row, 2, grey)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 2, white)
        if startDistanceColor == greyStr:
            movingBoatMeasurementsManager.SetTableColor(row, 5, grey)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 5, white)
        if endDistanceColor == greyStr:
            movingBoatMeasurementsManager.SetTableColor(row, 6, grey)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 6, white)
        if rawDischargeColor == greyStr:
            movingBoatMeasurementsManager.SetTableColor(row, 7, grey)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 7, white)
        # if finalDischargeColor == greyStr:
        #     movingBoatMeasurementsManager.SetTableColor(row, 8, grey)
        # else:
        #     movingBoatMeasurementsManager.SetTableColor(row, 8, white)
        if remarksColor == greyStr:
            movingBoatMeasurementsManager.SetTableColor(row, 8, grey)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 8, white)


    ADCPMeasResults = MovingBoatMeas.find('ADCPMeasResults')
    mmntStartTime = ADCPMeasResults.find('mmntStartTime').text
    movingBoatMeasurementsManager.mmntStartTimeCtrl = "" if mmntStartTime is None else mmntStartTime

    mmntEndTime = ADCPMeasResults.find('mmntEndTime').text
    movingBoatMeasurementsManager.mmntEndTimeCtrl = "" if mmntEndTime is None else mmntEndTime

    mmntMeanTime = ADCPMeasResults.find('mmntMeanTime').text
    movingBoatMeasurementsManager.mmntMeanTimeCtrl = "" if mmntMeanTime is None else mmntMeanTime

    rawDischargeMean = ADCPMeasResults.find('rawDischargeMean').text
    movingBoatMeasurementsManager.rawDischMeanCtrl = "" if rawDischargeMean is None else rawDischargeMean

    mbCorrectionApplied = ADCPMeasResults.find('mbCorrectionApplied').text
    movingBoatMeasurementsManager.mbCorrAppCtrl = "" if mbCorrectionApplied is None else mbCorrectionApplied

    finalDischargeMean = ADCPMeasResults.find('finalDischargeMean').text
    movingBoatMeasurementsManager.finalDischCtrl = "" if finalDischargeMean is None else finalDischargeMean

    correctedMeanGaugeHeight = ADCPMeasResults.find('correctedMeanGaugeHeight').text
    movingBoatMeasurementsManager.corrMeanGHCtrl = "" if correctedMeanGaugeHeight is None else correctedMeanGaugeHeight

    baseCurveGaugeHeight = ADCPMeasResults.find('baseCurveGaugeHeight').text
    movingBoatMeasurementsManager.baseCurveGHCtrl = "" if baseCurveGaugeHeight is None else baseCurveGaugeHeight

    calcBaseCurveDischarge = ADCPMeasResults.find('calcBaseCurveDischarge').text
    movingBoatMeasurementsManager.baseCurveDischCtrl = "" if calcBaseCurveDischarge is None else calcBaseCurveDischarge

    standardDevMeanDischarge = ADCPMeasResults.find('standardDevMeanDischarge').text
    movingBoatMeasurementsManager.standDevMeanDischCtrl = "" if standardDevMeanDischarge is None else standardDevMeanDischarge

    calculateShiftforBaseCurve = ADCPMeasResults.find('calculateShiftforBaseCurve').text
    movingBoatMeasurementsManager.calcShiftBaseCurveCtrl = "" if calculateShiftforBaseCurve is None else calculateShiftforBaseCurve

    dischargeDifferenceBaseCurve = ADCPMeasResults.find('dischargeDifferenceBaseCurve').text
    movingBoatMeasurementsManager.dischDiffBaseCurveCtrl = "" if dischargeDifferenceBaseCurve is None else dischargeDifferenceBaseCurve

    comments = ADCPMeasResults.find('comments').text
    movingBoatMeasurementsManager.commentsCtrl = "" if comments is None else comments

# Create XML structure for Midsection Method Information
def MidsecMeasAsXMLTree(MidsecMeas, midsecMeasurementsManager):
     #Midsection Panel
    MidsectionInfo = SubElement(MidsecMeas, 'MidsectionInfo', empty = 'True')
    startTimeCtrl = SubElement(MidsectionInfo, 'startTimeCtrl')
    startTimeCtrl.text = str(midsecMeasurementsManager.startTimeCtrl)

    endTimeCtrl = SubElement(MidsectionInfo, 'endTimeCtrl')
    endTimeCtrl.text = str(midsecMeasurementsManager.endTimeCtrl)

    measureSectionCtrl = SubElement(MidsectionInfo, 'measureSectionCtrl')
    measureSectionCtrl.text = str(midsecMeasurementsManager.measureSectionCtrl)

    deployMethodCtrl = SubElement(MidsectionInfo, 'deployMethodCtrl')
    deployMethodCtrl.text = str(midsecMeasurementsManager.deployMethodCtrl)

    meter1MeterNoCtrl = SubElement(MidsectionInfo, 'meter1MeterNoCtrl')
    meter1MeterNoCtrl.text = str(midsecMeasurementsManager.meter1MeterNoCtrl)

    meter1SlopeCtrl1 = SubElement(MidsectionInfo, 'meter1SlopeCtrl1')
    meter1SlopeCtrl1.text = midsecMeasurementsManager.meter1SlopeCtrl1

    meter1InterceptCtrl1 = SubElement(MidsectionInfo, 'meter1InterceptCtrl1')
    meter1InterceptCtrl1.text = str(midsecMeasurementsManager.meter1InterceptCtrl1)


    meter1SlopeCtrl2 = SubElement(MidsectionInfo, 'meter1SlopeCtrl2')
    meter1SlopeCtrl2.text = str(midsecMeasurementsManager.meter1SlopeCtrl2)

    meter1InterceptCtrl2 = SubElement(MidsectionInfo, 'meter1InterceptCtrl2')
    meter1InterceptCtrl2.text = str(midsecMeasurementsManager.meter1InterceptCtrl2)

    meter1CalibDateCtrl = SubElement(MidsectionInfo, 'meter1CalibDateCtrl')
    meter1CalibDateCtrl.text = str(midsecMeasurementsManager.meter1CalibDateCtrl)

    meter2MeterNoCtrl = SubElement(MidsectionInfo, 'meter2MeterNoCtrl')
    meter2MeterNoCtrl.text = str(midsecMeasurementsManager.meter2MeterNoCtrl)

    meter2SlopeCtrl1 = SubElement(MidsectionInfo, 'meter2SlopeCtrl1')
    meter2SlopeCtrl1.text = str(midsecMeasurementsManager.meter2SlopeCtrl1)

    meter2InterceptCtrl1 = SubElement(MidsectionInfo, 'meter2InterceptCtrl1')
    meter2InterceptCtrl1.text = str(midsecMeasurementsManager.meter2InterceptCtrl1)

    meter2SlopeCtrl2 = SubElement(MidsectionInfo, 'meter2SlopeCtrl2')
    meter2SlopeCtrl2.text = str(midsecMeasurementsManager.meter2SlopeCtrl2)

    meter2InterceptCtrl2 = SubElement(MidsectionInfo, 'meter2InterceptCtrl2')
    meter2InterceptCtrl2.text = str(midsecMeasurementsManager.meter2InterceptCtrl2)

    meter2CalibDateCtrl = SubElement(MidsectionInfo, 'meter2CalibDateCtrl')
    meter2CalibDateCtrl.text = str(midsecMeasurementsManager.meter2CalibDateCtrl)

    numOfPanelCtrl = SubElement(MidsectionInfo, 'numOfPanelCtrl')
    numOfPanelCtrl.text = str(midsecMeasurementsManager.numOfPanelCtrl)


    widthCtrl = SubElement(MidsectionInfo, 'widthCtrl')
    widthCtrl.text = str(midsecMeasurementsManager.widthCtrl)

    areaCtrl = SubElement(MidsectionInfo, 'areaCtrl')
    areaCtrl.text = str(midsecMeasurementsManager.areaCtrl)

    avgDepthCtrl = SubElement(MidsectionInfo, 'avgDepthCtrl')
    avgDepthCtrl.text = midsecMeasurementsManager.avgDepthCtrl

    avgVelCtrl = SubElement(MidsectionInfo, 'avgVelCtrl')
    avgVelCtrl.text = midsecMeasurementsManager.avgVelCtrl

    totalDisCtrl = SubElement(MidsectionInfo, 'totalDisCtrl')
    totalDisCtrl.text = str(midsecMeasurementsManager.totalDisCtrl)


    uncertaintyCtrl = SubElement(MidsectionInfo, 'uncertaintyCtrl')
    uncertaintyCtrl.text = str(midsecMeasurementsManager.uncertaintyCtrl)


    panelObjs = midsecMeasurementsManager.GetPanelObjs()
    for i in range(len(panelObjs)):
        length = 1
        if panelObjs[i].panelType == 1:
            length = len(panelObjs[i].depths)

        panel = SubElement(MidsectionInfo, "Panel", row=str(i), depths=str(length))
        panelType = SubElement(panel, "panelType")
        panelType.text = str(panelObjs[i].panelType)

        panelNum = SubElement(panel, "panelNum")
        panelNum.text = str(panelObjs[i].panelNum)

        distance = SubElement(panel, "distance")
        distance.text = str(panelObjs[i].distance)

        width = SubElement(panel, "width")
        width.text = str(panelObjs[i].width)

        depth = SubElement(panel, "depth")
        depth.text = str(panelObjs[i].depth)

        time = SubElement(panel, "time")
        time.text = str(panelObjs[i].time)

        panelId = SubElement(panel, "panelId")
        panelId.text = str(panelObjs[i].panelId)

        index = SubElement(panel, "index")
        index.text = str(panelObjs[i].index)

        corrMeanVelocity = SubElement(panel, "corrMeanVelocity")
        corrMeanVelocity.text = str(panelObjs[i].corrMeanVelocity)

        area = SubElement(panel, "area")
        area.text = str(panelObjs[i].area)

        discharge = SubElement(panel, "discharge")
        discharge.text = str(panelObjs[i].discharge)

        flow = SubElement(panel, "flow")
        flow.text = str(panelObjs[i].flow)

        if panelObjs[i].panelType == 0:

            edgeType = SubElement(panel, "edgeType")
            edgeType.text = str(panelObjs[i].edgeType)

            startOrEnd = SubElement(panel, "startOrEnd")
            startOrEnd.text = str(panelObjs[i].startOrEnd)

            leftOrRight = SubElement(panel, "leftOrRight")
            leftOrRight.text = str(panelObjs[i].leftOrRight)

            depth = SubElement(panel, "depth")
            depth.text = str(panelObjs[i].depth)

            depthAdjacent = SubElement(panel, "depthAdjacent")
            depthAdjacent.text = str(panelObjs[i].depthAdjacent)

            velocityAdjacent = SubElement(panel, "velocityAdjacent")
            velocityAdjacent.text = str(panelObjs[i].velocityAdjacent)

        elif panelObjs[i].panelType == 1:

            currentMeter = SubElement(panel, "currentMeter")
            currentMeter.text = str(panelObjs[i].currentMeter)

            slopBtn1 = SubElement(panel, "slopBtn1")
            slopBtn1.text = str(panelObjs[i].slopBtn1)

            slop = SubElement(panel, "slop")
            slop.text = str(panelObjs[i].slop)

            intercept = SubElement(panel, "intercept")
            intercept.text = str(panelObjs[i].intercept)

            slop2 = SubElement(panel, "slop2")
            slop2.text = str(panelObjs[i].slop2)

            intercept2 = SubElement(panel, "intercept2")
            intercept2.text = str(panelObjs[i].intercept2)

            panelCondition = SubElement(panel, "panelCondition")
            panelCondition.text = str(panelObjs[i].panelCondition)

            openDepthRead = SubElement(panel, "openDepthRead")
            openDepthRead.text = str(panelObjs[i].openDepthRead)

            weight = SubElement(panel, "weight")
            weight.text = str(panelObjs[i].weight)

            offset = SubElement(panel, "offset")
            offset.text = str(panelObjs[i].offset)

            wldl = SubElement(panel, "wldl")
            wldl.text = str(panelObjs[i].wldl)

            dryAngle = SubElement(panel, "dryAngle")
            dryAngle.text = str(panelObjs[i].dryAngle)

            distWaterSurface = SubElement(panel, "distWaterSurface")
            distWaterSurface.text = str(panelObjs[i].distWaterSurface)

            dryCorrection = SubElement(panel, "dryCorrection")
            dryCorrection.text = str(panelObjs[i].dryCorrection)

            wetCorrection = SubElement(panel, "wetCorrection")
            wetCorrection.text = str(panelObjs[i].wetCorrection)

            openEffectiveDepth = SubElement(panel, "openEffectiveDepth")
            openEffectiveDepth.text = str(panelObjs[i].openEffectiveDepth)

            iceDepthRead = SubElement(panel, "iceDepthRead")
            iceDepthRead.text = str(panelObjs[i].iceDepthRead)

            iceAssembly = SubElement(panel, "iceAssembly")
            iceAssembly.text = str(panelObjs[i].iceAssembly)

            aboveFoot = SubElement(panel, "aboveFoot")
            aboveFoot.text = str(panelObjs[i].aboveFoot)

            belowFoot = SubElement(panel, "belowFoot")
            belowFoot.text = str(panelObjs[i].belowFoot)

            distAboveWeight = SubElement(panel, "distAboveWeight")
            distAboveWeight.text = str(panelObjs[i].distAboveWeight)

            iceThickness = SubElement(panel, "iceThickness")
            iceThickness.text = str(panelObjs[i].iceThickness)

            iceThicknessAdjusted = SubElement(panel, "iceThicknessAdjusted")
            iceThicknessAdjusted.text = str(panelObjs[i].iceThicknessAdjusted)

            wsBottomIce = SubElement(panel, "wsBottomIce")
            wsBottomIce.text = str(panelObjs[i].wsBottomIce)

            adjusted = SubElement(panel, "adjusted")
            adjusted.text = str(panelObjs[i].adjusted)

            slush = SubElement(panel, "slush")
            slush.text = str(panelObjs[i].slush)

            wsBottomSlush = SubElement(panel, "wsBottomSlush")
            wsBottomSlush.text = str(panelObjs[i].wsBottomSlush)

            thickness = SubElement(panel, "thickness")
            thickness.text = str(panelObjs[i].thickness)

            iceEffectiveDepth = SubElement(panel, "iceEffectiveDepth")
            iceEffectiveDepth.text = str(panelObjs[i].iceEffectiveDepth)

            velocityMethod = SubElement(panel, "velocityMethod")
            velocityMethod.text = str(panelObjs[i].velocityMethod)

            obliqueCorrection = SubElement(panel, "obliqueCorrection")
            obliqueCorrection.text = str(panelObjs[i].obliqueCorrection)

            velocityCorrFactor = SubElement(panel, "velocityCorrFactor")
            velocityCorrFactor.text = str(panelObjs[i].velocityCorrFactor)

            reverseFlow = SubElement(panel, "reverseFlow")
            reverseFlow.text = str(panelObjs[i].reverseFlow)

            for j in range(3):
                depths = SubElement(panel, "depths" + str(j))
                if j < len(panelObjs[i].depths):
                    depths.text = str(panelObjs[i].depths[j])


            for j in range(3):
                depthObs = SubElement(panel, "depthObs" + str(j))
                if j < len(panelObjs[i].depthObs):
                    depthObs.text = str(panelObjs[i].depthObs[j])

            for j in range(3):
                revs = SubElement(panel, "revs" + str(j))
                if j < len(panelObjs[i].revs):
                    revs.text = str(panelObjs[i].revs[j])

            for j in range(3):
                revTimes = SubElement(panel, "revTimes" + str(j))
                if j < len(panelObjs[i].revTimes):
                    revTimes.text = str(panelObjs[i].revTimes[j])

            for j in range(3):
                pointVels = SubElement(panel, "pointVels" + str(j))
                if j < len(panelObjs[i].pointVels):
                    pointVels.text = str(panelObjs[i].pointVels[j])

            meanVelocity = SubElement(panel, "meanVelocity")
            meanVelocity.text = str(panelObjs[i].meanVelocity)

            # end = SubElement(panel, "end")
            # end.text = str(panelObjs[i].end)

            # start = SubElement(panel, "start")
            # start.text = str(panelObjs[i].start)

            # sequence = SubElement(panel, "sequence")
            # sequence.text = str(panelObjs[i].sequence)


# Set Midsection Measurements Information variables from existing XML structure
def MidsecMeasFromXML(MidsecMeas, midsecMeasurementsManager):



    midsecMeasurementsManager.GetSummaryTable().DeleteRows(0, midsecMeasurementsManager.GetNumberRows())
    midsecMeasurementsManager.GetSummaryTable().AppendRows()
    panelObjs = []
    midsecMeasurementsManager.SetPanelObjs(panelObjs)

    MidsectionInfo = MidsecMeas.find('MidsectionInfo')

    startTimeCtrl = MidsectionInfo.find('startTimeCtrl').text
    midsecMeasurementsManager.startTimeCtrl = "" if startTimeCtrl is None else startTimeCtrl

    endTimeCtrl = MidsectionInfo.find('endTimeCtrl').text
    midsecMeasurementsManager.endTimeCtrl = "" if endTimeCtrl is None else endTimeCtrl

    measureSectionCtrl = MidsectionInfo.find('measureSectionCtrl').text
    midsecMeasurementsManager.measureSectionCtrl = "" if measureSectionCtrl is None else measureSectionCtrl

    deployMethodCtrl = MidsectionInfo.find('deployMethodCtrl').text
    midsecMeasurementsManager.deployMethodCtrl = "" if deployMethodCtrl is None else deployMethodCtrl

    meter1MeterNoCtrl = MidsectionInfo.find('meter1MeterNoCtrl').text
    midsecMeasurementsManager.meter1MeterNoCtrl = "" if meter1MeterNoCtrl is None else meter1MeterNoCtrl

    meter1SlopeCtrl1 = MidsectionInfo.find('meter1SlopeCtrl1').text
    midsecMeasurementsManager.meter1SlopeCtrl1 = "" if meter1SlopeCtrl1 is None else meter1SlopeCtrl1

    meter1InterceptCtrl1 = MidsectionInfo.find('meter1InterceptCtrl1').text
    midsecMeasurementsManager.meter1InterceptCtrl1 = "" if meter1InterceptCtrl1 is None else meter1InterceptCtrl1

    meter1SlopeCtrl2 = MidsectionInfo.find('meter1SlopeCtrl2').text
    midsecMeasurementsManager.meter1SlopeCtrl2 = "" if meter1SlopeCtrl2 is None else meter1SlopeCtrl2

    meter1InterceptCtrl2 = MidsectionInfo.find('meter1InterceptCtrl2').text
    midsecMeasurementsManager.meter1InterceptCtrl2 = "" if meter1InterceptCtrl2 is None else meter1InterceptCtrl2

    meter1CalibDateCtrl = MidsectionInfo.find('meter1CalibDateCtrl').text
    midsecMeasurementsManager.meter1CalibDateCtrl = "" if meter1CalibDateCtrl is None else meter1CalibDateCtrl

    meter2MeterNoCtrl = MidsectionInfo.find('meter2MeterNoCtrl').text
    midsecMeasurementsManager.meter2MeterNoCtrl = "" if meter2MeterNoCtrl is None else meter2MeterNoCtrl

    meter2SlopeCtrl1 = MidsectionInfo.find('meter2SlopeCtrl1').text
    midsecMeasurementsManager.meter2SlopeCtrl1 = "" if meter2SlopeCtrl1 is None else meter2SlopeCtrl1

    meter2InterceptCtrl1 = MidsectionInfo.find('meter2InterceptCtrl1').text
    midsecMeasurementsManager.meter2InterceptCtrl1 = "" if meter2InterceptCtrl1 is None else meter2InterceptCtrl1

    meter2SlopeCtrl2 = MidsectionInfo.find('meter2SlopeCtrl2').text
    midsecMeasurementsManager.meter2SlopeCtrl2 = "" if meter2SlopeCtrl2 is None else meter2SlopeCtrl2

    meter2InterceptCtrl2 = MidsectionInfo.find('meter2InterceptCtrl2').text
    midsecMeasurementsManager.meter2InterceptCtrl2 = "" if meter2InterceptCtrl2 is None else meter2InterceptCtrl2

    meter2CalibDateCtrl = MidsectionInfo.find('meter2CalibDateCtrl').text
    midsecMeasurementsManager.meter2CalibDateCtrl = "" if meter2CalibDateCtrl is None else meter2CalibDateCtrl

    numOfPanelCtrl = MidsectionInfo.find('numOfPanelCtrl').text
    midsecMeasurementsManager.numOfPanelCtrl = "" if numOfPanelCtrl is None else numOfPanelCtrl

    widthCtrl = MidsectionInfo.find('widthCtrl').text
    midsecMeasurementsManager.widthCtrl = "" if widthCtrl is None else widthCtrl

    areaCtrl = MidsectionInfo.find('areaCtrl').text
    midsecMeasurementsManager.areaCtrl = "" if areaCtrl is None else areaCtrl



    avgDepthCtrl = MidsectionInfo.find('avgDepthCtrl').text
    midsecMeasurementsManager.avgDepthCtrl = "" if avgDepthCtrl is None else avgDepthCtrl

    avgVelCtrl = MidsectionInfo.find('avgVelCtrl').text
    midsecMeasurementsManager.avgVelCtrl = "" if avgVelCtrl is None else avgVelCtrl

    totalDisCtrl = MidsectionInfo.find('totalDisCtrl').text
    midsecMeasurementsManager.totalDisCtrl = "" if totalDisCtrl is None else totalDisCtrl

    uncertaintyCtrl = MidsectionInfo.find('uncertaintyCtrl').text
    midsecMeasurementsManager.uncertaintyCtrl = "" if uncertaintyCtrl is None else uncertaintyCtrl


    summarytable = midsecMeasurementsManager.GetSummaryTable()

    for panel in MidsectionInfo.iter("Panel"):

        panelNum = panel.find("panelNum").text if panel.find("panelNum").text is not None else ""
        distance = panel.find("distance").text if panel.find("distance").text is not None else ""
        width = panel.find("width").text if panel.find("width").text is not None else ""
        depth = panel.find("depth").text if panel.find("depth").text is not None else ""
        time = panel.find("time").text if panel.find("time").text is not None else ""
        panelId = int(panel.find("panelId").text)
        panelType = panel.find("panelType").text if panel.find("panelType").text is not None else ""
        index = panel.find("index").text
        corrMeanVelocity = panel.find("corrMeanVelocity").text if panel.find("corrMeanVelocity").text is not None else ""
        area = panel.find("area").text if panel.find("area").text is not None else ""
        discharge = panel.find("discharge").text if panel.find("discharge").text is not None else ""
        flow = panel.find("flow").text if panel.find("flow").text is not None else ""
        obj = None
        if panelType == "0":
            edgeType = panel.find("edgeType").text if panel.find("edgeType").text is not None else ""
            startOrEnd = panel.find("startOrEnd").text if panel.find("startOrEnd").text is not None else ""
            leftOrRight = "Left Bank"
            try:
                leftOrRight = panel.find("leftOrRight").text if panel.find("leftOrRight").text is not None else ""
            except:
                pass
            depth = panel.find("depth").text if panel.find("depth").text is not None else ""
            depthAdjacent = panel.find("depthAdjacent").text
            depthAdjacent = True if depthAdjacent == "True" else False
            velocityAdjacent = panel.find("velocityAdjacent").text
            velocityAdjacent = True if velocityAdjacent == "True" else False

            obj = EdgeObj(edgeType=edgeType, time=time, distance=distance, startOrEnd=startOrEnd, leftOrRight=leftOrRight, panelNum=panelNum,\
            depth=depth, corrMeanVelocity=corrMeanVelocity, depthAdjacent=depthAdjacent, velocityAdjacent=velocityAdjacent,\
                     panelId=panelId, index=index)

            # panelObjs.append(obj)
            # if len(panelObjs) > 0:
            #     summarytable.AppendRows()

        elif panel.find("panelType").text == "1":

            currentMeter = panel.find("currentMeter").text
            slopBtn1 = panel.find("slopBtn1").text
            if slopBtn1 == "True":
                slopBtn1 = True
            else:
                slopBtn1 = False

            slop = panel.find("slop").text if panel.find("slop").text is not None else ""
            intercept = panel.find("intercept").text if panel.find("intercept").text is not None else ""
            slop2 = panel.find("slop2").text if panel.find("slop2").text is not None else ""
            intercept2 = panel.find("intercept2").text if panel.find("intercept2").text is not None else ""
            panelCondition = panel.find("panelCondition").text if panel.find("panelCondition").text is not None else ""
            velocityMethod = panel.find("velocityMethod").text if panel.find("velocityMethod").text is not None else ""
            obliqueCorrection = panel.find("obliqueCorrection").text if panel.find("obliqueCorrection").text is not None else ""
            velocityCorrFactor = panel.find("velocityCorrFactor").text if panel.find("velocityCorrFactor").text is not None else ""
            reverseFlow = panel.find("reverseFlow").text
            reverseFlow = True if reverseFlow == "True" else False


            # depths = panel.find("depths").text
            # depths = [str(i) for i in ast.literal_eval(depths)]
            # depthObs = panel.find("depthObs").text
            # depthObs = [str(i) for i in ast.literal_eval(depthObs)]
            # revs = panel.find("revs").text
            # revs = [str(i) for i in ast.literal_eval(revs)]
            # revTimes = panel.find("revTimes").text
            # revTimes = [str(i) for i in ast.literal_eval(revTimes)]
            # pointVels = panel.find("pointVels").text
            # pointVels = [str(i) for i in ast.literal_eval(pointVels)]

            try:
                depths0 = panel.find("depths0").text if panel.find("depths0").text is not None else ""
            except:
                pass
            try:
                depths1 = panel.find("depths1").text if panel.find("depths1").text is not None else ""
            except:
                pass
            try:
                depths2 = panel.find("depths2").text if panel.find("depths2").text is not None else ""
            except:
                pass
            try:
                depthObs0 = panel.find("depthObs0").text if panel.find("depthObs0").text is not None else ""
            except:
                pass
            try:
                depthObs1 = panel.find("depthObs1").text if panel.find("depthObs1").text is not None else ""
            except:
                pass
            try:
                depthObs2 = panel.find("depthObs2").text if panel.find("depthObs2").text is not None else ""
            except:
                pass
            try:
                revs0 = panel.find("revs0").text if panel.find("revs0").text is not None else ""
            except:
                pass
            try:
                revs1 = panel.find("revs1").text if panel.find("revs1").text is not None else ""
            except:
                pass
            try:
                revs2 = panel.find("revs2").text if panel.find("revs2").text is not None else ""
            except:
                pass
            try:
                revTimes0 = panel.find("revTimes0").text if panel.find("revTimes0").text is not None else ""
            except:
                pass
            try:
                revTimes1 = panel.find("revTimes1").text if panel.find("revTimes1").text is not None else ""
            except:
                pass
            try:
                revTimes2 = panel.find("revTimes2").text if panel.find("revTimes2").text is not None else ""
            except:
                pass
            try:
                pointVels0 = panel.find("pointVels0").text if panel.find("pointVels0").text is not None else ""
            except:
                pass
            try:
                pointVels1 = panel.find("pointVels1").text if panel.find("pointVels1").text is not None else ""
            except:
                pass
            try:
                pointVels2 = panel.find("pointVels2").text if panel.find("pointVels2").text is not None else ""
            except:
                pass


            meanVelocity = panel.find("meanVelocity").text

            depths = []
            depthObs = []
            revs = []
            revTimes = []
            pointVels = []

            if velocityMethod == "0.5" or velocityMethod == "0.6" or velocityMethod == "Surface":
                depths.append(depths0)
                depthObs.append(depthObs0)
                revs.append(revs0)
                revTimes.append(revTimes0)
                pointVels.append(pointVels0)


            elif velocityMethod == "0.2/0.8":
                depths.append(depths0)
                depths.append(depths1)
                depthObs.append(depthObs0)
                depthObs.append(depthObs1)
                revs.append(revs0)
                revs.append(revs1)
                revTimes.append(revTimes0)
                revTimes.append(revTimes1)
                pointVels.append(pointVels0)
                pointVels.append(pointVels1)

            elif velocityMethod == "0.2/0.6/0.8":
                depths.append(depths0)
                depths.append(depths1)
                depths.append(depths2)
                depthObs.append(depthObs0)
                depthObs.append(depthObs1)
                depthObs.append(depthObs2)
                revs.append(revs0)
                revs.append(revs1)
                revs.append(revs2)
                revTimes.append(revTimes0)
                revTimes.append(revTimes1)
                revTimes.append(revTimes2)
                pointVels.append(pointVels0)
                pointVels.append(pointVels1)
                pointVels.append(pointVels2)




            if panel.find("panelCondition").text == "Open":
                print "found an Open panelCondition Obj"
                openDepthRead = panel.find("openDepthRead").text if panel.find("openDepthRead").text is not None else ""
                weight = panel.find("weight").text if panel.find("weight").text is not None else ""
                offset = panel.find("offset").text if panel.find("offset").text is not None else ""
                wldl = panel.find("wldl").text if panel.find("wldl").text is not None else ""
                dryAngle = panel.find("dryAngle").text if panel.find("dryAngle").text is not None else ""
                distWaterSurface = panel.find("distWaterSurface").text if panel.find("distWaterSurface").text is not None else ""
                dryCorrection = panel.find("dryCorrection").text if panel.find("dryCorrection").text is not None else ""
                wetCorrection = panel.find("wetCorrection").text if panel.find("wetCorrection").text is not None else ""
                openEffectiveDepth = panel.find("openEffectiveDepth").text if panel.find("openEffectiveDepth").text is not None else ""

                obj = PanelObj(panelNum=panelNum, distance=distance, depth=depth, \
                depths=depths, depthObs=depthObs, revs=revs, revTimes=revTimes, pointVels=pointVels,\
                meanVelocity=meanVelocity, corrMeanVelocity=corrMeanVelocity,\
                velocityMethod=velocityMethod, panelCondition=panelCondition,\
                currentMeter=currentMeter, time=time,\
                slop=slop, intercept=intercept, slop2=slop2,\
                intercept2=intercept2, slopBtn1=slopBtn1,\
                openDepthRead=openDepthRead, weight=weight, \
                offset=offset, wldl=wldl, \
                dryAngle=dryAngle, distWaterSurface=distWaterSurface, \
                dryCorrection=dryCorrection, wetCorrection=wetCorrection, \
                openEffectiveDepth=openEffectiveDepth,\
                obliqueCorrection=obliqueCorrection, velocityCorrFactor=velocityCorrFactor, \
                reverseFlow=reverseFlow, panelId=panelId, index=index)


            elif panel.find("panelCondition").text == "Ice":
                iceDepthRead = panel.find("iceDepthRead").text if panel.find("iceDepthRead").text is not None else ""
                iceAssembly = panel.find("iceAssembly").text if panel.find("iceAssembly").text is not None else ""
                aboveFoot = panel.find("aboveFoot").text if panel.find("aboveFoot").text is not None else ""
                belowFoot = panel.find("belowFoot").text if panel.find("belowFoot").text is not None else ""
                distAboveWeight = panel.find("distAboveWeight").text if panel.find("distAboveWeight").text is not None else ""
                iceThickness = ""
                iceThicknessAdjusted=""
                try:
                    iceThickness = panel.find("iceThickness").text if panel.find("iceThickness").text is not None else ""
                    iceThicknessAdjusted = panel.find("iceThicknessAdjusted").text if panel.find("iceThicknessAdjusted").text is not None else ""
                except:
                    pass
                wsBottomIce = panel.find("wsBottomIce").text if panel.find("wsBottomIce").text is not None else ""
                adjusted = panel.find("adjusted").text if panel.find("adjusted").text is not None else ""
                slush = panel.find("slush").text if panel.find("slush").text is not None else ""
                slush = True if slush == "True" else False
                wsBottomSlush = panel.find("wsBottomSlush").text if panel.find("wsBottomSlush").text is not None else ""
                thickness = panel.find("thickness").text if panel.find("thickness").text is not None else ""
                iceEffectiveDepth = panel.find("iceEffectiveDepth").text if panel.find("iceEffectiveDepth").text is not None else ""

                obj = PanelObj(panelNum=panelNum, distance=distance, depth=depth, \
                depths=depths, depthObs=depthObs, revs=revs, revTimes=revTimes, pointVels=pointVels,\
                meanVelocity=meanVelocity, corrMeanVelocity=corrMeanVelocity,\
                velocityMethod=velocityMethod, panelCondition=panelCondition,\
                currentMeter=currentMeter, time=time,\
                slop=slop, intercept=intercept, slop2=slop2,\
                intercept2=intercept2, slopBtn1=slopBtn1,\
                iceDepthRead=iceDepthRead, iceAssembly=iceAssembly, \
                aboveFoot=aboveFoot, belowFoot=belowFoot, \
                distAboveWeight=distAboveWeight, wsBottomIce=wsBottomIce, \
                adjusted=adjusted, slush=slush, \
                wsBottomSlush=wsBottomSlush, thickness=thickness, iceEffectiveDepth=iceEffectiveDepth,\
                obliqueCorrection=obliqueCorrection, velocityCorrFactor=velocityCorrFactor, \
                reverseFlow=reverseFlow, panelId=panelId, index=index, \
                iceThickness=iceThickness, iceThicknessAdjusted=iceThicknessAdjusted)


        if obj is not None:
            midsecMeasurementsManager.AddRow(obj)
            print "Adding panel ", obj.panelId










    # try:
    #     totalDischarge = MidsecMeas.find('totalDischarge').text
    #     midsecMeasurementsManager.totalDischargeCtrl = "" if totalDischarge is None else totalDischarge
    # except:
    #     print "old version does not include totalDischarge mid-section"

    # MidsecMeasTable = MidsecMeas.find('MidsecMeasTable')
    # for MidsecMeasTableRow in MidsecMeasTable.findall('MidsecMeasTableRow'):
    #     row = int(MidsecMeasTableRow.get('row'))

    #     distText = MidsecMeasTableRow.find('distFromInitPoint').text
    #     widthText = MidsecMeasTableRow.find('width').text
    #     wsToBottomText = MidsecMeasTableRow.find('wsToBottomIce').text
    #     ofWaterText = MidsecMeasTableRow.find('ofWater').text
    #     ofObsText = MidsecMeasTableRow.find('ofObs').text
    #     revolText = MidsecMeasTableRow.find('revolutions').text
    #     timeText = MidsecMeasTableRow.find('time').text
    #     atPointText = MidsecMeasTableRow.find('atPoint').text
    #     meanText = MidsecMeasTableRow.find('mean').text
    #     areaText = MidsecMeasTableRow.find('area').text
    #     dischText = MidsecMeasTableRow.find('discharge').text

    #     midsecMeasurementsManager.SetTableValue(row, 0, "" if distText is None else distText)
    #     midsecMeasurementsManager.SetTableValue(row, 1, "" if widthText is None else widthText)
    #     midsecMeasurementsManager.SetTableValue(row, 2, "" if wsToBottomText is None else wsToBottomText)
    #     midsecMeasurementsManager.SetTableValue(row, 3, "" if ofWaterText is None else ofWaterText)
    #     midsecMeasurementsManager.SetTableValue(row, 4, "" if ofObsText is None else ofObsText)
    #     midsecMeasurementsManager.SetTableValue(row, 5, "" if revolText is None else revolText)
    #     midsecMeasurementsManager.SetTableValue(row, 6, "" if timeText is None else timeText)
    #     midsecMeasurementsManager.SetTableValue(row, 7, "" if atPointText is None else atPointText)
    #     midsecMeasurementsManager.SetTableValue(row, 8, "" if meanText is None else meanText)
    #     midsecMeasurementsManager.SetTableValue(row, 9, "" if areaText is None else areaText)
    #     midsecMeasurementsManager.SetTableValue(row, 10, "" if dischText is None else dischText)




#return the standard deviation of a list of numbers
def standardDeviation(nums):
    if len(nums) == 1:
        return 0
    if len(nums) > 0:
        mean = 0
        total = 0
        for i in range(len(nums)):
            mean += float(nums[i])
        mean = mean / len(nums)

        for i in range(len(nums)):
            total += (float(nums[i]) - mean) ** 2
        return math.sqrt(total / (len(nums) - 1))
    else:
        return 0



def UploadInfoAsXMLTree(UploadInfo, uploadInfo):
    record = SubElement(UploadInfo, "record")


    status = SubElement(record, "status")
    status.text = uploadInfo[0]

    time = SubElement(record, "time")
    time.text = uploadInfo[1]

    user = SubElement(record, "user")
    user.text = uploadInfo[2]



#####################################################################################
#Converting from seconds to HH:MM:SS
def convertEpochSecond(num):
	convertedTime = time.gmtime(float(num))
	h = convertedTime.tm_hour
	m = convertedTime.tm_min
	s = convertedTime.tm_sec


	return str(h) + ":" + str(m) + ":" + str(s)





# # Set transect info on moving boat from an existing XML structure
# def MovingBoatTransectFromMmt(winRiver, movingBoatMeasurementsManager):
#     SiteInformation = winRiver.find('Project').find('Site_Information')
#     DischargeSummary = winRiver.find('Project').find('Site_Discharge').find('Discharge_Summary')
#     QAQC = winRiver.find('Project').find('QA_QC')
#     Locked = winRiver.find('Project').find('Locked').text
#     TransectSiteDischarge = winRiver.find('Project').find('Site_Discharge').find('Transect')





#     locked = movingBoatMeasurementsManager.lockCB

#     if not locked:

#         movingBoatMeasurementsManager.lockCB = ''
#         movingBoatMeasurementsManager.mbCB = False
#         movingBoatMeasurementsManager.mbCmbo = ''
#         movingBoatMeasurementsManager.leftBankCmbo = ''
#         # movingBoatMeasurementsManager.leftBankOtherCtrl = ''
#         movingBoatMeasurementsManager.rightBankCmbo = ''
#         # movingBoatMeasurementsManager.rightBankOtherCtrl = ''
#         movingBoatMeasurementsManager.trackRefCmbo = ''
#         movingBoatMeasurementsManager.mmntStartTimeCtrl = '00:00:00'
#         movingBoatMeasurementsManager.mmntEndTimeCtrl = '00:00:00'
#         movingBoatMeasurementsManager.mmntMeanTimeCtrl = '00:00:00'
#         movingBoatMeasurementsManager.rawDischMeanCtrl = ''
#         movingBoatMeasurementsManager.finalDischCtrl = ''
#         movingBoatMeasurementsManager.mbCorrAppCtrl = ''
#         movingBoatMeasurementsManager.standDevMeanDischCtrl = ''
#         movingBoatMeasurementsManager.corrMeanGHCtrl = ''
#         movingBoatMeasurementsManager.calcShiftBaseCurveCtrl = ''
#         movingBoatMeasurementsManager.dischDiffBaseCurveCtrl = ''
#         movingBoatMeasurementsManager.baseCurveGHCtrl = ''
#         movingBoatMeasurementsManager.baseCurveDischCtrl = ''
#         movingBoatMeasurementsManager.commentsCtrl = ''

#         for row in range(1, len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 2):
#             movingBoatMeasurementsManager.SetTableValue(row, 1, 'False')
#             movingBoatMeasurementsManager.SetTableValue(row, 2, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 3, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 4, "00:00:00")
#             movingBoatMeasurementsManager.SetTableValue(row, 5, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 5, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 6, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 7, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 8, "")
#             movingBoatMeasurementsManager.SetTableValue(row, 10, "")




#     reference = SiteInformation.find('Reference').text
#     raw = DischargeSummary.find('None')
#     # ADCPDischargeMeasurement = movingBoat.find('ADCPDischargeMeasurement')
#     row = 0
#     mmntStart = ''
#     mmntEnd = ''
#     trackRef = reference.upper()
#     transect = QAQC.find('Moving_Bed_Test').find('Transect')
#     mbTestDoneCB = False if transect is None else True
#     mbTestText = ''
#     leftBank = ''
#     rightBank = ''
#     leftCoeff = ''
#     rightCoeff = ''
#     if mbTestDoneCB:
#         displayText = transect.attrib['DisplayText']
#         mbTestText = '' if displayText is None else displayText

#     comments = '' if SiteInformation.find('Remarks').text is None else 'Mmt Remarks: ' + SiteInformation.find('Remarks').text + '\n'

#     meanBT = 0
#     meanFinal = 0
#     counterBT = 0
#     counterFinal = 0
#     finals = []

#     for Transect in list(raw):
#         checked = Transect.find('UseInSummary').text
#         if checked == '1':
#             checked = 'True'

#             leftCoeff = Transect.find('LeftEdgeSlopeCoeff').text if leftCoeff == '' else leftCoeff
#             rightCoeff = Transect.find('RightEdgeSlopeCoeff').text if rightCoeff == '' else rightCoeff
#             if float(leftCoeff) == 0.3535 or float(leftCoeff) == 0.353:
#                 leftBank = 'Sloping'
#             elif float(leftCoeff) == 0.91:
#                 leftBank = 'Vertical'
#             else:
#                 leftBank = 'Other'

#             if float(rightCoeff) == 0.3535 or float(rightCoeff) == 0.353:
#                 rightBank = 'Sloping'
#             elif float(rightCoeff) == 0.91:
#                 rightBank = 'Vertical'
#             else:
#                 rightBank = 'Other'





#         else:
#             checked = 'False'
#         left = Transect.find('BeginLeft').text
#         number = Transect.find('TransectNmb').text
#         startTime = Transect.find('StartTime').text
#         startTime = convertEpochSecond(startTime)
#         endTime = Transect.find('EndTime').text
#         endTime = convertEpochSecond(endTime)
#         # startTime = time.gmtime(startTime)
#         mmntStart = startTime if mmntStart == "" and checked == "True" else mmntStart
#         mmntEnd = endTime
#         if left == '1':
#             startBank = 'L'
#             startDistance = Transect.find('LeftDistance').text
#             endDistance = Transect.find('RightDistance').text
#         else:
#             startBank = 'R'
#             startDistance = Transect.find('RightDistance').text
#             endDistance = Transect.find('LeftDistance').text

#         rawDischarge = Transect.find('TotalQ').text
#         if 'BT' in reference.upper():
#             finalDischarge = DischargeSummary.find('BottomTrack').find(Transect.tag).find('TotalQ').text

#         elif 'GGA' in reference.upper():
#             finalDischarge = DischargeSummary.find('GGA').find(Transect.tag).find('TotalQ').text

#         else:
#             finalDischarge = DischargeSummary.find('VTG').find(Transect.tag).find('TotalQ').text

#         comments += 'Transect_' + str(row) + ':'
#         comments += '\t-Depth Ref = ' + Transect.find('DepthRef').text
#         comments += '\t-Bin Size = ' + Transect.find('BinSize').text
#         comments += '\t-Mode = ' + Transect.find('BTMode').text + '\n'

#         color = (210, 210, 210)

#         if row > len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 3:
#             movingBoatMeasurementsManager.gui.AddEntry()


#         if checked == 'True':
#             movingBoatMeasurementsManager.SetFontColor(row, 0, 'Black')

#         if not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 1, checked)
#         if  movingBoatMeasurementsManager.GetTableValue(row, 2) == '' or not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 2, number)
#             movingBoatMeasurementsManager.SetTableColor(row, 2, color)
#         if movingBoatMeasurementsManager.GetTableValue(row, 3) is None or not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 3, startBank)
#             movingBoatMeasurementsManager.SetTableColor(row, 3, color)
#         if not locked or movingBoatMeasurementsManager.GetTableValue(row, 4) == '00:00:00':
#             movingBoatMeasurementsManager.SetTableValue(row, 4, startTime)
#         if  movingBoatMeasurementsManager.GetTableValue(row, 5) == '' or not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 5, startDistance)
#             movingBoatMeasurementsManager.SetTableColor(row, 5, color)
#         if  movingBoatMeasurementsManager.GetTableValue(row, 6) == '' or not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 6, endDistance)
#             movingBoatMeasurementsManager.SetTableColor(row, 6, color)
#         if  movingBoatMeasurementsManager.GetTableValue(row, 7) == '' or not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 7, rawDischarge)
#             movingBoatMeasurementsManager.SetTableColor(row, 7, color)
#         if  movingBoatMeasurementsManager.GetTableValue(row, 8) == '' or not locked:
#             movingBoatMeasurementsManager.SetTableValue(row, 8, finalDischarge)
#             movingBoatMeasurementsManager.SetTableColor(row, 8, color)
#         # if  movingBoatMeasurementsManager.GetTableValue(row, 9) == '' or not locked:
#         #     movingBoatMeasurementsManager.SetTableValue(row, 9, reference)
#         #     movingBoatMeasurementsManager.SetTableColor(row, 9, color)
#         # for i in range(8):
#         #     movingBoatMeasurementsManager.SetTableColor(row, i, 'Yellow')

#         if movingBoatMeasurementsManager.GetTableValue(row, 1):
#             meanBT += float(rawDischarge)
#             meanFinal += float(finalDischarge)
#             counterBT += 1
#             counterFinal += 1
#             finals.append(finalDischarge)

#         row += 1
#     if counterBT != 0:
#         meanBT = meanBT / counterBT
#     if counterFinal != 0:
#         meanFinal = meanFinal / counterFinal
#     if trackRef.upper() == 'BT':
#         MBCorrection = (float(format(meanFinal, '.3f')) - float(format(meanBT, '.3f'))) / float(format(meanFinal, '.3f')) * 100
#     else:
#         MBCorrection = 0

#     dischargeEstimateIndex = 0
#     for configuration in TransectSiteDischarge.iter('Configuration'):
#         topDischargeEst = configuration.find('Discharge').find('Top_Discharge_Estimate').text
#         bottomDischargeEst = configuration.find('Discharge').find('Bottom_Discharge_Estimate').text
#         powerCurveCoef = configuration.find('Discharge').find('Power_Curve_Coef').text

#         if configuration.find('Discharge').find('Top_Discharge_Estimate').attrib['Status'] == '0':
#             topDisResult = 'power'
#         elif configuration.find('Discharge').find('Top_Discharge_Estimate').attrib['Status'] == '1':
#             topDisResult = 'constant'
#         elif configuration.find('Discharge').find('Top_Discharge_Estimate').attrib['Status'] == ' 2':
#             topDisResult = '3-pt slope'
#         else:
#             topDisResult = configuration.find('Discharge').find('Top_Discharge_Estimate').attrib['Status']


#         if configuration.find('Discharge').find('Bottom_Discharge_Estimate').attrib['Status'] == '0':
#             bottomDisResult = 'power'
#         elif configuration.find('Discharge').find('Bottom_Discharge_Estimate').attrib['Status'] == ' 2':
#             bottomDisResult = 'no slip'
#         else:
#             bottomDisResult = configuration.find('Discharge').find('Bottom_Discharge_Estimate').attrib['Status']

#         comments += configuration.tag + str(dischargeEstimateIndex) + ':\t-Top_Dis_Est = ' + topDischargeEst + '\t-Bottom_Dis_Est = ' + bottomDischargeEst + '\t-Power_Cur_Coef = ' + powerCurveCoef + '\t-Result = ' + topDisResult + ' \\ ' + bottomDischargeEst + '\n'
#         dischargeEstimateIndex += 1

#     if not locked:

#         # movingBoatMeasurementsManager.lockCB = Locked
#         movingBoatMeasurementsManager.mbCB = mbTestDoneCB
#         movingBoatMeasurementsManager.mbCmbo = mbTestText
#         movingBoatMeasurementsManager.leftBankCmbo = leftBank
#         # movingBoatMeasurementsManager.leftBankOtherCtrl = '' if leftCoeff == '' else str(float(leftCoeff))
#         movingBoatMeasurementsManager.rightBankCmbo = rightBank
#         # movingBoatMeasurementsManager.rightBankOtherCtrl = '' if rightCoeff == '' else str(float(rightCoeff))
#         movingBoatMeasurementsManager.trackRefCmbo = trackRef




#         movingBoatMeasurementsManager.mmntStartTimeCtrl = mmntStart
#         movingBoatMeasurementsManager.mmntEndTimeCtrl = mmntEnd

#         start = movingBoatMeasurementsManager.gui.mmntStartTimeCtrl.GetWxDateTime()
#         end = movingBoatMeasurementsManager.gui.mmntEndTimeCtrl.GetWxDateTime()
#         meanTime = mean(start, end)

#         movingBoatMeasurementsManager.mmntMeanTimeCtrl = meanTime
#         movingBoatMeasurementsManager.rawDischMeanCtrl = str(format(meanBT, '.3f'))
#         movingBoatMeasurementsManager.finalDischCtrl = str(format(meanFinal, '.3f'))
#         movingBoatMeasurementsManager.mbCorrAppCtrl = str(format(MBCorrection, '.3f'))
#         if len(finals) > 0:
#             standDevMean = float(format(standardDeviation(finals) /float(meanFinal), '.3f')) * 100
#             movingBoatMeasurementsManager.standDevMeanDischCtrl = str(standDevMean)
#         else:
#             movingBoatMeasurementsManager.standDevMeanDischCtrl = '0.000'
#         movingBoatMeasurementsManager.commentsCtrl = comments


#         movingBoatMeasurementsManager.recalculate()



# def OnImportMmt(winRiver, movingBoatMeasurementsManager, locationID, date, gui):
#     desc = 'The date for this measurement file does not match the date on the front page.\nDo you still want to import the ADCP file?'
#     openTitle = 'Date does not match'

#     if locationID != '':
#         mmtLocationID = winRiver.find('Project').find('Site_Information').find('Number').text
#         mmtDate = winRiver.find('Project').find('Site_Information').find('Measurement_Date').text


#         if locationID != mmtLocationID.upper():
#             dlg = wx.MessageDialog(gui, "The Station ID in the measurement file does not match", 'Dismatch Station ID',
#                                         wx.OK | wx.ICON_QUESTION)
#             res = dlg.ShowModal()
#             if res == wx.OK:
#                 dlg.Destroy()
#             else:
#                 dlg.Destroy()
#         elif date != mmtDate:
#             dlg = wx.MessageDialog(gui, desc, openTitle, wx.YES_NO | wx.ICON_QUESTION)

#             res = dlg.ShowModal()
#             if res == wx.ID_YES:
#                 dlg.Destroy()
#                 MovingBoatTransectFromMmt(winRiver, movingBoatMeasurementsManager)
#             elif res == wx.wx.ID_NO:
#                 dlg.Destroy()
#             else:
#                 dlg.Destroy()
#         else:
#             MovingBoatTransectFromMmt(winRiver, movingBoatMeasurementsManager)

#     else:
#         dlg = wx.MessageDialog(gui, "Station ID and date cannot be empty on the front page", 'Empty Station ID',
#                                         wx.OK | wx.ICON_QUESTION)
#         res = dlg.ShowModal()
#         if res == wx.OK:
#             dlg.Destroy()
#         else:
#             dlg.Destroy()
