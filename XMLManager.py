# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from xml.etree.ElementTree import SubElement
from MidSectionSubPanelObj import *

import wx
import datetime
import math
import time
import ast
import sys, os
import traceback


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
    try:
        enteredInHWSCB = TitleHeader.find('enteredInHWS').text
        titleHeaderManager.enteredInHWSCB = False if enteredInHWSCB is None else (False if enteredInHWSCB == "False" else True)
    except:
        pass

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


def GetStationId(GenInfo):
    return GenInfo.find('station').get('number')

def GetDate(GenInfo):
    return GenInfo.find('date').text


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



    stageRemark = SubElement(StageMeas, 'stageRemark')
    stageRemark.text = stageMeasManager.stageRemarksCtrl


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


    try:
        stageRemark = StageMeas.find('stageRemark').text
        stageMeasManager.stageRemarksCtrl = "" if stageRemark is None else stageRemark
    except:
        pass

    # stageMeasManager.gui.UpdateDischargeMGH()
    # print stageMeasManager.gui.CMGHHG.GetValue()

# Create XML structure for Discharge Measurements
def DischMeasAsXMLTree(DisMeas, disMeasManager):
    bkColor =  disMeasManager.manager.gui.importedBGColor


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

    dischCombo = SubElement(DisMeas, 'dischCombo')
    dischCombo.text = str(disMeasManager.dischCombo)



    mmtTimeVal = SubElement(DisMeas, 'mmtTimeVal')
    mmtTimeVal.text = str(disMeasManager.mmtValTxt)

    shift = SubElement(DisMeas, 'shift')
    shift.text = str(disMeasManager.shiftCtrl)

    diff = SubElement(DisMeas, 'diff')
    diff.text = str(disMeasManager.diffCtrl)

    curve = SubElement(DisMeas, 'curve')
    curve.text = str(disMeasManager.curveCtrl)

    condition = SubElement(DisMeas, 'condition')
    condition.text = str(disMeasManager.controlConditionCmbo)

    dischargeRemark = SubElement(DisMeas, 'dischargeRemark')
    dischargeRemark.text = disMeasManager.dischRemarksCtrl

    controlConditionRemark = SubElement(DisMeas, 'controlConditionRemark')
    controlConditionRemark.text = disMeasManager.ControlConditionRemarksCtrl

    if disMeasManager.GetAirTempCtrl().GetBackgroundColour() == bkColor:
        airTemp.attrib['imported'] = "1"
    if disMeasManager.GetWaterTempCtrl().GetBackgroundColour() == bkColor:
        waterTemp.attrib['imported'] = "1"
    if disMeasManager.GetWidthCtrl().GetBackgroundColour() == bkColor:
        width.attrib['imported'] = "1"
    if disMeasManager.GetAreaCtrl().GetBackgroundColour() == bkColor:
        area.attrib['imported'] = "1"
    if disMeasManager.GetMeanVelCtrl().GetBackgroundColour() == bkColor:
        meanVel.attrib['imported'] = "1"
    if disMeasManager.GetMghCtrl().GetBackgroundColour() == bkColor:
        mgh.attrib['imported'] = "1"
    if disMeasManager.GetDischCtrl().GetBackgroundColour() == bkColor:
        discharge.attrib['imported'] = "1"
    if disMeasManager.GetShiftCtrl().GetBackgroundColour() == bkColor:
        shift.attrib['imported'] = "1"
    if disMeasManager.GetDiffCtrl().GetBackgroundColour() == bkColor:
        diff.attrib['imported'] = "1"
    if disMeasManager.GetCurveCtrl().GetBackgroundColour() == bkColor:
        curve.attrib['imported'] = "1"

# Set Discharge Measurements variables from existing XML structure
def DischMeasFromXML(DisMeas, disMeasManager):
    bkColor = disMeasManager.manager.gui.importedBGColor
    white = "white"
    startTime = DisMeas.find('startTime').text
    disMeasManager.startTimeCtrl = "" if startTime is None else startTime

    endTime = DisMeas.find('endTime').text
    disMeasManager.endTimeCtrl = "" if endTime is None else endTime

    airTemp = DisMeas.find('airTemp')
    if airTemp.text is None:
        disMeasManager.airTempCtrl = "" 
    else:
        disMeasManager.airTempCtrl = airTemp.text
        if "imported" in airTemp.attrib and airTemp.attrib['imported'] == "1":
            disMeasManager.GetAirTempCtrl().SetBackgroundColour(bkColor) 
        else:
            disMeasManager.GetAirTempCtrl().SetBackgroundColour(white)


    waterTemp = DisMeas.find('waterTemp')
    if waterTemp.text is None:
        disMeasManager.waterTempCtrl = ""
    else:
        disMeasManager.waterTempCtrl = waterTemp.text
        if "imported" in waterTemp.attrib and waterTemp.attrib['imported'] == "1":
            disMeasManager.GetWaterTempCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetWaterTempCtrl().SetBackgroundColour(white) 

    width = DisMeas.find('width')
    if width.text is None:
        disMeasManager.widthCtrl = ""  
    else:
        disMeasManager.widthCtrl = width.text
        if "imported" in width.attrib and width.attrib['imported'] == "1":
            disMeasManager.GetWidthCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetWidthCtrl().SetBackgroundColour(white)

    area = DisMeas.find('area')
    if area.text is None:
        disMeasManager.areaCtrl = ""  
    else:
        disMeasManager.areaCtrl = area.text
        if "imported" in area.attrib and area.attrib['imported'] == "1":
            disMeasManager.GetAreaCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetAreaCtrl().SetBackgroundColour(white)

    meanVel = DisMeas.find('meanVel')
    if meanVel.text is None:
        disMeasManager.meanVelCtrl = ""  
    else:
        disMeasManager.meanVelCtrl = meanVel.text
        if "imported" in meanVel.attrib and meanVel.attrib['imported'] == "1":
            disMeasManager.GetMeanVelCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetMeanVelCtrl().SetBackgroundColour(white)

    mgh = DisMeas.find('mgh')
    if mgh.text is None:
        disMeasManager.mghCtrl = ""  
    else:
        disMeasManager.mghCtrl = mgh.text
        if "imported" in mgh.attrib and mgh.attrib['imported'] == "1":
            disMeasManager.GetMghCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetMghCtrl().SetBackgroundColour(white)


    discharge = DisMeas.find('discharge')
    if discharge.text is None:
        disMeasManager.dischCtrl = ""  
    else:
        disMeasManager.dischCtrl = discharge.text
        if "imported" in discharge.attrib and discharge.attrib['imported'] == "1":
            disMeasManager.GetDischCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetDischCtrl().SetBackgroundColour(white)

    dischCombo = DisMeas.find('dischCombo')
    if dischCombo is None or dischCombo.text is None:
        disMeasManager.dischCombo = ""
    else:
        disMeasManager.dischCombo = dischCombo.text

    mmtTimeVal = DisMeas.find('mmtTimeVal').text
    disMeasManager.mmtValTxt = "" if mmtTimeVal is None else mmtTimeVal

    shift = DisMeas.find('shift')
    if shift.text is None:
        disMeasManager.shiftCtrl = ""  
    else:
        disMeasManager.shiftCtrl = shift.text
        if "imported" in shift.attrib and shift.attrib['imported'] == "1":
            disMeasManager.GetShiftCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetShiftCtrl().SetBackgroundColour(white)

    diff = DisMeas.find('diff')
    if diff.text is None:
        disMeasManager.diffCtrl = ""  
    else:
        disMeasManager.diffCtrl = diff.text
        if "imported" in diff.attrib and diff.attrib['imported'] == "1":
            disMeasManager.GetDiffCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetDiffCtrl().SetBackgroundColour(white)

    curve = DisMeas.find('curve')
    if curve.text is None:
        disMeasManager.curveCtrl = ""  
    else:
        disMeasManager.curveCtrl = curve.text
        if "imported" in curve.attrib and curve.attrib['imported'] == "1":
            disMeasManager.GetCurveCtrl().SetBackgroundColour(bkColor)
        else:
            disMeasManager.GetCurveCtrl().SetBackgroundColour(white)


    try:
        mghCmbo = DisMeas.find('mghCmbo').text
        disMeasManager.mghCmbo = "" if mghCmbo is None else mghCmbo
    except:
        pass

    try:
        condition = DisMeas.find('condition').text
        disMeasManager.controlConditionCmbo = "" if condition is None else condition

        dischargeRemark = DisMeas.find('dischargeRemark').text
        disMeasManager.dischRemarksCtrl = "" if dischargeRemark is None else dischargeRemark

        controlConditionRemark = DisMeas.find('controlConditionRemark').text
        disMeasManager.ControlConditionRemarksCtrl = "" if controlConditionRemark is None else controlConditionRemark

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



    gasSysDepCtrl = SubElement(EnvCond, 'gasSysDepCtrl')
    gasSysDepCtrl.text = envCondManager.gasSysDepCtrl

    gasArrTime = SubElement(EnvCond, 'gasArrTime')
    gasArrTime.text = envCondManager.gasArrTime

    gasDepTime = SubElement(EnvCond, 'gasDepTime')
    gasDepTime.text = envCondManager.gasDepTime

    feedDepCtrl = SubElement(EnvCond, 'feedDepCtrl')
    feedDepCtrl.text = envCondManager.feedDepCtrl

    feedArrTime = SubElement(EnvCond, 'feedArrTime')
    feedArrTime.text = envCondManager.feedArrTime

    feedDepTime = SubElement(EnvCond, 'feedDepTime')
    feedDepTime.text = envCondManager.feedDepTime

    bpmrotDepCtrl = SubElement(EnvCond, 'bpmrotDepCtrl')
    bpmrotDepCtrl.text = envCondManager.bpmrotDepCtrl

    bpmrotArrTime = SubElement(EnvCond, 'bpmrotArrTime')
    bpmrotArrTime.text = envCondManager.bpmrotArrTime

    bpmrotDepTime = SubElement(EnvCond, 'bpmrotDepTime')
    bpmrotDepTime.text = envCondManager.bpmrotDepTime


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


    stationHealthRemark = SubElement(EnvCond, 'stationHealthRemark')
    stationHealthRemark.text = envCondManager.stationHealthRemarksCtrl


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


    try:
        gasSysDepCtrl = EnvCond.find('gasSysDepCtrl').text
        envCondManager.gasSysDepCtrl = "" if gasSysDepCtrl is None else gasSysDepCtrl

        gasArrTime = EnvCond.find('gasArrTime').text
        envCondManager.gasArrTime = "" if gasArrTime is None else gasArrTime

        gasDepTime = EnvCond.find('gasDepTime').text
        envCondManager.gasDepTime = "" if gasDepTime is None else gasDepTime

        feedDepCtrl = EnvCond.find('feedDepCtrl').text
        envCondManager.feedDepCtrl = "" if feedDepCtrl is None else feedDepCtrl

        feedArrTime = EnvCond.find('feedArrTime').text
        envCondManager.feedArrTime = "" if feedArrTime is None else feedArrTime

        feedDepTime = EnvCond.find('feedDepTime').text
        envCondManager.feedDepTime = "" if feedDepTime is None else feedDepTime

        bpmrotDepCtrl = EnvCond.find('bpmrotDepCtrl').text
        envCondManager.bpmrotDepCtrl = "" if bpmrotDepCtrl is None else bpmrotDepCtrl

        bpmrotArrTime = EnvCond.find('bpmrotArrTime').text
        envCondManager.bpmrotArrTime = "" if bpmrotArrTime is None else bpmrotArrTime

        bpmrotDepTime = EnvCond.find('bpmrotDepTime').text
        envCondManager.bpmrotDepTime = "" if bpmrotDepTime is None else bpmrotDepTime
    except:
        pass



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



    try:
        stationHealthRemark = EnvCond.find('stationHealthRemark').text
    except:
        stationHealthRemark = None
    envCondManager.stationHealthRemarksCtrl = "" if stationHealthRemark is None else stationHealthRemark

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
    bkColor = instrDepManager.manager.gui.importedBGColor
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


    if panelsNum.text == '' and \
        flowAngle.text == '' and \
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


    #SiteConditions Panel
    SiteConditions = SubElement(InstrumentDeployment, 'SiteConditions')

    pictured = SubElement(SiteConditions, "pictured")
    pictured.text = str(instrDepManager.GetPicturedCkboxVal())

    preUseCable = SubElement(SiteConditions, "preUseCable")
    preUseCable.text = instrDepManager.preUseCableCmbo

    # condition = SubElement(Control, 'condition')
    # condition.text = str(instrDepManager.controlConditionCmbo)


    # dischargeRemark = SubElement(Control, 'dischargeRemark')

    # dischargeRemark.text = instrDepManager.dischRemarksCtrl

    # stageRemark = SubElement(Control, 'stageRemark')
    # stageRemark.text = instrDepManager.stageRemarksCtrl


    # stationHealthRemark = SubElement(Control, 'stationHealthRemark')
    # stationHealthRemark.text = instrDepManager.stationHealthRemarksCtrl


    

    # controlConditionRemark = SubElement(Control, 'controlConditionRemark')
    # controlConditionRemark.text = instrDepManager.SetControlConditionRemarksCtrl

    if instrDepManager.GetDeploymentCmbo().GetBackgroundColour() == bkColor:
        deployment.attrib['imported'] = "1"
    if instrDepManager.GetInstrumentCmbo().GetBackgroundColour() == bkColor:
        instrument.attrib['imported'] = "1"
    if instrDepManager.GetSerialCmbo().GetBackgroundColour() == bkColor:
        serialNum.attrib['imported'] = "1"
    if instrDepManager.GetFrequencyCmbo().GetBackgroundColour() == bkColor:
        frequency.attrib['imported'] = "1"
    if instrDepManager.GetFirmwareCmbo().GetBackgroundColour() == bkColor:
        firmware.attrib['imported'] = "1"
    if instrDepManager.GetSoftwareCtrl().GetBackgroundColour() == bkColor:
        software.attrib['imported'] = "1"
    if instrDepManager.GetManufactureCmbo().GetBackgroundColour() == bkColor:
        manufacturer.attrib['imported'] = "1"
    if instrDepManager.GetModelCmbo().GetBackgroundColour() == bkColor:
        model.attrib['imported'] = "1"
    if instrDepManager.GetNumOfPanelsScroll().GetBackgroundColour() == bkColor:
        panelsNum.attrib['imported'] = "1"
    if instrDepManager.GetConfigCmbo().GetBackgroundColour() == bkColor:
        configChoice.attrib['imported'] = "1"
    if instrDepManager.GetAdcpDepthCtrl().GetBackgroundColour() == bkColor:
        depth.attrib['imported'] = "1"
    if instrDepManager.GetMagnDeclCtrl().GetBackgroundColour() == bkColor:
        magDecl.attrib['imported'] = "1"
    if instrDepManager.GetDiagTestCB().GetBackgroundColour() == bkColor:
        diagnosticTest.attrib['imported'] = "1"





# Set Instrument and Deployment Information variables from existing XML structure
def InstrumentDepFromXML(InstrumentDeployment, instrDepManager):
    bkColor = instrDepManager.manager.gui.importedBGColor
    white = "white"
    instrDepManager.gui.CheckListReset()
    GeneralInfo = InstrumentDeployment.find('GeneralInfo')
    method = GeneralInfo.find('methodType').text
    instrDepManager.methodCBListBox = "" if method is None else method
    instrDepManager.OnDeploymentUpdate()

    deployment = GeneralInfo.find('deployment')
    if deployment.text is None:
        instrDepManager.deploymentCmbo = ""
    else:
        instrDepManager.deploymentCmbo = deployment.text
        if "imported" in deployment.attrib and deployment.attrib['imported'] == "1":
            instrDepManager.GetDeploymentCmbo().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetDeploymentCmbo().SetBackgroundColour(white)

    position = GeneralInfo.find('position').text
    if position is None:
        instrDepManager.positionMethodCtrl = ""
    else:
        instrDepManager.positionMethodCtrl = position

    serialNum = GeneralInfo.find('serialNum')
    if serialNum.text is None:
        instrDepManager.serialCmboFromXml = ""
    else:
        instrDepManager.serialCmboFromXml = serialNum.text
        if "imported" in serialNum.attrib and serialNum.attrib['imported'] == "1":
            instrDepManager.GetSerialCmbo().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetSerialCmbo().SetBackgroundColour(white)  

    instrument = GeneralInfo.find('instrument')
    if instrument.text is None:
        instrDepManager.instrumentCmbo = ""
    else:
        instrDepManager.instrumentCmbo = instrument.text
        if "imported" in instrument.attrib and instrument.attrib['imported'] == "1":
            instrDepManager.GetInstrumentCmbo().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetInstrumentCmbo().SetBackgroundColour(white)   



    gauge1 = GeneralInfo.find('gauge1').text
    if gauge1 is None:
        instrDepManager.gaugeCtrl = ""
    else:
        instrDepManager.gaugeCtrl = gauge1

    length = GeneralInfo.find('length').text
    if length is None:
        instrDepManager.lengthRadButBox = 0
    else:
        instrDepManager.lengthRadButBox = int(length)

    gaugePos = GeneralInfo.find('gaugePos').text
    if gaugePos is None:
        instrDepManager.posRadButBox = 0
    else:
        instrDepManager.posRadButBox = int(gaugePos)

    # gauge2 = GeneralInfo.find('gauge2').text
    # instrDepManager.gaugeCtrl2 = "" if gauge2 is None else gauge2

    try:
        frequency = GeneralInfo.find('frequency')
        if frequency.text is None:
            instrDepManager.frequencyCmbo = ""
        else:
            instrDepManager.frequencyCmbo = frequency.text
            if "imported" in frequency.attrib and frequency.attrib['imported'] == "1":
                instrDepManager.GetFrequencyCmbo().SetBackgroundColour(bkColor)
            else:
                instrDepManager.GetFrequencyCmbo().SetBackgroundColour(white) 

        firmware = GeneralInfo.find('firmware')
        if firmware.text is None:
            instrDepManager.firmwareCmbo = ""
        else:
            instrDepManager.firmwareCmbo = firmware.text
            if "imported" in firmware.attrib and firmware.attrib['imported'] == "1":
                instrDepManager.GetFirmwareCmbo().SetBackgroundColour(bkColor)
            else:
                instrDepManager.GetFirmwareCmbo().SetBackgroundColour(white)

        software = GeneralInfo.find('software')
        if software.text is None:
            instrDepManager.softwareCtrl = ""
        else:
            instrDepManager.softwareCtrl = software.text
            if "imported" in software.attrib and software.attrib['imported'] == "1":
                instrDepManager.GetSoftwareCtrl().SetBackgroundColour(bkColor)
            else:
                instrDepManager.GetSoftwareCtrl().SetBackgroundColour(white)    
    except:
        pass

    try:
        manufacturer = GeneralInfo.find('manufacturer')
        if manufacturer.text is None:
            instrDepManager.manufactureCmboFromXml = ""
        else:
            instrDepManager.manufactureCmboFromXml = manufacturer.text
            if "imported" in manufacturer.attrib and manufacturer.attrib['imported'] == "1":
                instrDepManager.GetManufactureCmbo().SetBackgroundColour(bkColor)
            else:
                instrDepManager.GetManufactureCmbo().SetBackgroundColour(white)  

        model = GeneralInfo.find('model')
        if model.text is None:
            instrDepManager.modelCmbo = ""
        else:
            instrDepManager.modelCmbo = model.text
            if "imported" in model.attrib and model.attrib['imported'] == "1":
                instrDepManager.GetModelCmbo().SetBackgroundColour(bkColor)
            else:
                instrDepManager.GetModelCmbo().SetBackgroundColour(white) 
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

    panelsNum = MidsectionInfo.find('panelsNum')
    if panelsNum.text is None:    
        instrDepManager.numOfPanelsScroll = ""  
    else:
        instrDepManager.numOfPanelsScroll = panelsNum.text
        if "imported" in panelsNum.attrib and panelsNum.attrib['imported'] == "1":
            instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(white)    

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


    configChoice = ADCPInfo.find('configChoice')
    if configChoice.text is None:
        instrDepManager.configCmbo = ""
    else:
        instrDepManager.configCmbo = configChoice.text
        if "imported" in configChoice.attrib and configChoice.attrib['imported'] == "1":
            instrDepManager.GetConfigCmbo().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetConfigCmbo().SetBackgroundColour(white)  

    configVal = ADCPInfo.find('configVal').text
    instrDepManager.configCtrl = "" if configVal is None else configVal

    ADCPSetToClock = ADCPInfo.find('ADCPSetToClock').text
    instrDepManager.adcpSetToClockCB = False if ADCPSetToClock is None else (False if ADCPSetToClock == 'False' else True)

    diagnosticTest = ADCPInfo.find('diagnosticTest')
    if diagnosticTest.text is None:
        instrDepManager.GetDiagTestCB().SetValue(False)
    else:
        if diagnosticTest.text.lower() == 'true':
            instrDepManager.GetDiagTestCB().SetValue(True)
        else:
            instrDepManager.GetDiagTestCB().SetValue(False)
        if "imported" in diagnosticTest.attrib and diagnosticTest.attrib['imported'] == "1":
            instrDepManager.GetDiagTestCB().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetDiagTestCB().SetBackgroundColour(white)


    depth = ADCPInfo.find('depth')
    if depth.text is None:
        instrDepManager.adcpDepthCtrl = ""  
    else:
        instrDepManager.adcpDepthCtrl = depth.text
        if "imported" in depth.attrib and depth.attrib['imported'] == "1":
            instrDepManager.GetAdcpDepthCtrl().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetAdcpDepthCtrl().SetBackgroundColour(white)  

    magDecl = ADCPInfo.find('magDecl')
    if magDecl.text is None:
        instrDepManager.magnDeclCtrl = ""  
    else:
        instrDepManager.magnDeclCtrl = magDecl.text
        if "imported" in magDecl.attrib and magDecl.attrib['imported'] == "1":
            instrDepManager.GetMagnDeclCtrl().SetBackgroundColour(bkColor)
        else:
            instrDepManager.GetMagnDeclCtrl().SetBackgroundColour(white) 
    

    compassCali = ADCPInfo.find('compassCali').text
    instrDepManager.compassCaliCB = False if compassCali is None else (False if compassCali == 'False' else True)

    passedRev = ADCPInfo.find('passedRev').text
    instrDepManager.passedFieldRevCB = False if passedRev is None else (False if passedRev == 'False' else True)


    #Site Conditions
    SiteConditions = InstrumentDeployment.find('SiteConditions')
    try:
        pictured = SiteConditions.find('pictured').text
        if pictured == "True":
            instrDepManager.SetPicturedCkboxVal(True)
        else:
            instrDepManager.SetPicturedCkboxVal(False)
    except:
        print "no pictured ckeckbox for field review in xml"

    try:
        preUseCable = SiteConditions.find('preUseCable')
        if preUseCable.text is None:
            instrDepManager.preUseCableCmboFromXml = ""
        else:
            instrDepManager.preUseCableCmboFromXml = preUseCable.text
    except:
        print "Failed to load preUseCable value"
        
    # Control = InstrumentDeployment.find('Control')
    # condition = Control.find('condition').text
    # instrDepManager.controlConditionCmbo = "" if condition is None else condition



    # dischargeRemark = Control.find('dischargeRemark').text
    # instrDepManager.dischRemarksCtrl = "" if dischargeRemark is None else dischargeRemark

    # stageRemark = Control.find('stageRemark').text
    # instrDepManager.stageRemarksCtrl = "" if stageRemark is None else stageRemark

    # try:
    #     stationHealthRemark = Control.find('stationHealthRemark').text
    # except:
    #     stationHealthRemark = None
    # instrDepManager.stationHealthRemarksCtrl = "" if stationHealthRemark is None else stationHealthRemark


    


    # try:
    #     controlConditionRemark = Control.find('controlConditionRemark').text
    # except:
    #     pass

    # try:
    #     instrDepManager.SetControlConditionRemarksCtrl = "" if controlConditionRemark is None else controlConditionRemark
    # except:
    #     pass


    
       


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
    conventionalLevellingRb = SubElement(LevelChecks, 'conventionalLevellingRb')
    conventionalLevellingRb.text = str(waterLevelRunManager.GetConventionalLevellingRb().GetValue())

    totalStationRb = SubElement(LevelChecks, 'totalStationRb')
    totalStationRb.text = str(waterLevelRunManager.GetTotalStationRb().GetValue())

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

            upload = SubElement(LevelChecksTable, "upload")
            upload.text = str(waterLevelRunManager.GetUploadCheckBox(i).GetValue())

        else:
            closure = SubElement(LevelChecksTable, "closure")
            upload = SubElement(LevelChecksTable, "upload")



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

    surveyedby = SubElement(LevelChecks, 'surveyedby')
    surveyedby.text = waterLevelRunManager.surveyedbyCtrl

    loggerName = SubElement(LevelChecks, 'loggerName')
    loggerName.text = waterLevelRunManager.HGHeaderCtrl

    loggerName2 = SubElement(LevelChecks, 'loggerName2')
    loggerName2.text = waterLevelRunManager.HG2HeaderCtrl

# Set Level Checks variables from existing XML structure
def LevelChecksFromXML(LevelChecks, waterLevelRunManager):
    print "LevelChecksFromXML"
    
    try:
        conventionalLevellingRb = LevelChecks.find('conventionalLevellingRb').text
        if conventionalLevellingRb == "True":
            waterLevelRunManager.SetConventionalLevellingRb(True)
        else:
            waterLevelRunManager.SetTotalStationRb(True)
    except:
        pass
    
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

        if LevelChecksTable is not None:
            #Level Checks Summary + closure
            try:
                if LevelChecksTable.find('closure') is not None:
                    closure = LevelChecksTable.find('closure').text if LevelChecksTable.find('closure').text is not None else ""
                    waterLevelRunManager.GetClosureText(index).SetValue(closure)

                if LevelChecksTable.find('upload') is not None:
                    upload = LevelChecksTable.find('upload').text if LevelChecksTable.find('upload').text is not None else ""
         
                    if upload == "True":

                        waterLevelRunManager.GetUploadCheckBox(index).SetValue(True)
                    else:
                        waterLevelRunManager.GetUploadCheckBox(index).SetValue(False)


            # except:
            #     print "except"
            #     waterLevelRunManager.GetClosureText(index).SetValue("")
            except Exception as e:
                print str(e)
                waterLevelRunManager.GetClosureText(index).SetValue("")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
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
        surveyedby = LevelChecks.find('surveyedby').text
        waterLevelRunManager.surveyedbyCtrl = "" if surveyedby is None else surveyedby
    except:
        waterLevelRunManager.surveyedbyCtrl = ""

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

    planNotes = SubElement(FieldReview, "planNotes")
    planNotes.text = frChecklistManager.planNotesCtrl

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
    try:
        planNotes = FieldReview.find('planNotes').text
        frChecklistManager.planNotesCtrl = "" if planNotes is None else planNotes
    except:
        print "no plan notes"

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

    bkColor = movingBoatMeasurementsManager.manager.gui.importedBGColor

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

    extrapUncerCtrl = SubElement(MovingBoatMeas, "extrapUncerCtrl")
    extrapUncerCtrl.text = movingBoatMeasurementsManager.extrapUncerCtrl


    if movingBoatMeasurementsManager.GetBedMatCmbo().GetBackgroundColour() == bkColor:
        bedMaterial.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetMbCB().GetBackgroundColour() == bkColor:
        mbTest.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetMbCmbo().GetBackgroundColour() == bkColor:
        mbTestChoice.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetDetectedCtrl().GetBackgroundColour() == bkColor:
        detected.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetTrackRefCmbo().GetBackgroundColour() == bkColor:
        trackRefChoice.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetLeftBankCmbo().GetBackgroundColour() == bkColor:
        leftBankChoice.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetLeftBankOtherCtrl().GetBackgroundColour() == bkColor:
        leftBank.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetRightBankCmbo().GetBackgroundColour() == bkColor:
        rightBankChoice.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetRightBankOtherCtrl().GetBackgroundColour() == bkColor:
        rightBank.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetEdgeDistMmntCmbo().GetBackgroundColour() == bkColor:
        edgeDistMmntMethod.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetCompositeTrackCmbo().GetBackgroundColour() == bkColor:
        compositeTrackCmbo.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetDepthRefCmbo().GetBackgroundColour() == bkColor:
        depthRefCmbo.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetVelocityTopCombo().GetBackgroundColour() == bkColor:
        velocityTopCombo.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetVelocityBottomCombo().GetBackgroundColour() == bkColor:
        velocityBottomCombo.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetVelocityExponentCtrl().GetBackgroundColour() == bkColor:
        velocityExponentCtrl.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetDifferenceCtrl().GetBackgroundColour() == bkColor:
        differenceCtrl.attrib['imported'] = "1"
    if movingBoatMeasurementsManager.GetExtrapUncerCtrl().GetBackgroundColour() == bkColor:
        extrapUncerCtrl.attrib['imported'] = "1"


    # lock = SubElement(MovingBoatMeas, "lock")
    # lock.text = str(movingBoatMeasurementsManager.lockCB)

    ADCPMeasTable = SubElement(MovingBoatMeas, "ADCPMeasTable")
    for i in range(1, len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 1):
        checked = str(movingBoatMeasurementsManager.GetTableValue(i - 1, 1))
        transectIDText = movingBoatMeasurementsManager.GetTableValue(i - 1, 2)
        startBankText = str(movingBoatMeasurementsManager.GetTableValue(i - 1, 3)) \
        if movingBoatMeasurementsManager.GetTableValue(i - 1, 3) is not None else ""
        startTimeText = movingBoatMeasurementsManager.GetTableValue(i - 1, 4)
        startDistanceText = movingBoatMeasurementsManager.GetTableValue(i - 1, 6)
        endDistanceText = movingBoatMeasurementsManager.GetTableValue(i - 1, 7)
        rawDischargeText = movingBoatMeasurementsManager.GetTableValue(i - 1, 8)
        # finalDisText = movingBoatMeasurementsManager.GetTableValue(i - 1, 8)
        remarksText = movingBoatMeasurementsManager.GetTableValue(i - 1, 9)

        notEmptyRow = False
        if transectIDText == "True":
            notEmptyRow = True
        if transectIDText != "":
            notEmptyRow = True
        # print startBankText != ""
        # print startBankText != "None"
        # print startBankText != None
        if startBankText != "" and startBankText != "None" and startBankText != None:
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

            # white = 'White'
            # grey = 'Grey'

            if movingBoatMeasurementsManager.GetTableColor(i - 1, 2) == bkColor:
                transectID.attrib['imported'] = "1"
            else:
                transectID.attrib['imported'] = "0"

            if movingBoatMeasurementsManager.GetTableColor(i - 1, 6) == bkColor:
                startDistance.attrib['imported'] =  "1"
            else:
                startDistance.attrib['imported'] = "0"

            if movingBoatMeasurementsManager.GetTableColor(i - 1, 7) == bkColor:
                endDistance.attrib['imported'] =  "1"
            else:
                endDistance.attrib['imported'] = "0"

            if movingBoatMeasurementsManager.GetTableColor(i - 1, 8) == bkColor:
                rawDischarge.attrib['imported'] =  "1"
            else:
                rawDischarge.attrib['imported'] =  "0"
            
            # if movingBoatMeasurementsManager.GetTableColor(i - 1, 8) == (255, 255, 255, 255):
            #     finalDischarge.attrib['color'] = white
            # else:
            #     finalDischarge.attrib['color'] = grey
            if movingBoatMeasurementsManager.GetTableColor(i - 1, 9) == bkColor:
                remarks.attrib['imported'] =  "1"
            else:
                remarks.attrib['imported'] =  "0"




    ADCPMeasResults = SubElement(MovingBoatMeas, "ADCPMeasResults")

    mmntStartTime = SubElement(ADCPMeasResults, "mmntStartTime")
    mmntStartTime.text = movingBoatMeasurementsManager.mmntStartTimeCtrl

    mmntEndTime = SubElement(ADCPMeasResults, "mmntEndTime")
    mmntEndTime.text = movingBoatMeasurementsManager.mmntEndTimeCtrl

    mmntMeanTime = SubElement(ADCPMeasResults, "mmntMeanTime")
    mmntMeanTime.text = movingBoatMeasurementsManager.mmntMeanTimeCtrl

    # rawDischargeMean = SubElement(ADCPMeasResults, "rawDischargeMean")
    # rawDischargeMean.text = movingBoatMeasurementsManager.rawDischMeanCtrl

    mbCorrectionApplied = SubElement(ADCPMeasResults, "mbCorrectionApplied")
    mbCorrectionApplied.text = movingBoatMeasurementsManager.mbCorrAppCtrl
    if movingBoatMeasurementsManager.GetMbCorrAppCtrl().GetBackgroundColour() == bkColor:
        mbCorrectionApplied.attrib['imported'] = "1"

    finalDischargeMean = SubElement(ADCPMeasResults, "finalDischargeMean")
    finalDischargeMean.text = movingBoatMeasurementsManager.finalDischCtrl
    if movingBoatMeasurementsManager.GetFinalDischCtrl().GetBackgroundColour() == bkColor:
        finalDischargeMean.attrib['imported'] = "1"

    correctedMeanGaugeHeight = SubElement(ADCPMeasResults, "correctedMeanGaugeHeight")
    correctedMeanGaugeHeight.text = movingBoatMeasurementsManager.corrMeanGHCtrl

    baseCurveGaugeHeight = SubElement(ADCPMeasResults, "baseCurveGaugeHeight")
    baseCurveGaugeHeight.text = movingBoatMeasurementsManager.baseCurveGHCtrl

    calcBaseCurveDischarge = SubElement(ADCPMeasResults, "calcBaseCurveDischarge")
    calcBaseCurveDischarge.text = movingBoatMeasurementsManager.baseCurveDischCtrl

    standardDevMeanDischarge = SubElement(ADCPMeasResults, "standardDevMeanDischarge")
    standardDevMeanDischarge.text = movingBoatMeasurementsManager.standDevMeanDischCtrl
    if movingBoatMeasurementsManager.GetStandDevMeanDischCtrl().GetBackgroundColour() == bkColor:
        standardDevMeanDischarge.attrib['imported'] = "1"

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
    bkColor = movingBoatMeasurementsManager.manager.gui.importedBGColor
    white = "white"

    bedMaterial = MovingBoatMeas.find('bedMaterial')
    if bedMaterial.text is None:
        movingBoatMeasurementsManager.bedMatCmbo = ""  
    else:
        movingBoatMeasurementsManager.bedMatCmbo = bedMaterial.text
        if "imported" in bedMaterial.attrib and bedMaterial.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetBedMatCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetBedMatCmbo().SetBackgroundColour(white)

    mbTest = MovingBoatMeas.find('mbTest')
    if mbTest.text is None or mbTest.text == 'False':
        movingBoatMeasurementsManager.mbCB = False  
    else:
        movingBoatMeasurementsManager.mbCB = True
    if mbTest.text is not None:
        if "imported" in mbTest.attrib and mbTest.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetMbCB().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetMbCB().SetBackgroundColour(white)

    mbTestChoice = MovingBoatMeas.find('mbTestChoice')
    if mbTestChoice.text is None:
        movingBoatMeasurementsManager.mbCmbo = ""  
    else: 
        movingBoatMeasurementsManager.mbCmbo = mbTestChoice.text
        if "imported" in mbTestChoice.attrib and mbTestChoice.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetMbCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetMbCmbo().SetBackgroundColour(white)

    

    detected = MovingBoatMeas.find('detected')
    if detected.text is None:
        movingBoatMeasurementsManager.detectedCtrl = ""  
    else:
        movingBoatMeasurementsManager.detectedCtrl = detected.text
        if "imported" in detected.attrib and detected.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetDetectedCtrl().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetDetectedCtrl().SetBackgroundColour(white)

    trackRefChoice = MovingBoatMeas.find('trackRefChoice')
    if trackRefChoice.text is None:
        movingBoatMeasurementsManager.trackRefCmbo = ""  
    else:
        movingBoatMeasurementsManager.trackRefCmbo = trackRefChoice.text
        if "imported" in trackRefChoice.attrib and trackRefChoice.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetTrackRefCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetTrackRefCmbo().SetBackgroundColour(white)

    leftBankChoice = MovingBoatMeas.find('leftBankChoice')
    if leftBankChoice.text is None:
        movingBoatMeasurementsManager.leftBankCmbo = ""  
    else:
        movingBoatMeasurementsManager.leftBankCmbo = leftBankChoice.text
        if "imported" in leftBankChoice.attrib and leftBankChoice.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetLeftBankCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetLeftBankCmbo().SetBackgroundColour(white)



    rightBankChoice = MovingBoatMeas.find('rightBankChoice')
    if rightBankChoice.text is None:
        movingBoatMeasurementsManager.rightBankCmbo = ""  
    else:
        movingBoatMeasurementsManager.rightBankCmbo = rightBankChoice.text
        if "imported" in rightBankChoice.attrib and rightBankChoice.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetRightBankCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetRightBankCmbo().SetBackgroundColour(white)

    try:
        leftBank = MovingBoatMeas.find('leftBank')
        if leftBank.text is None:
            movingBoatMeasurementsManager.leftBankOtherCtrl = ""  
        else:
            movingBoatMeasurementsManager.leftBankOtherCtrl = leftBank.text
            if "imported" in leftBank.attrib and leftBank.attrib['imported'] == "1":
                movingBoatMeasurementsManager.GetLeftBankOtherCtrl().SetBackgroundColour(bkColor)
            else:
                movingBoatMeasurementsManager.GetLeftBankOtherCtrl().SetBackgroundColour(white)

    except:
        leftBank = ""
        movingBoatMeasurementsManager.leftBankOtherCtrl = ""

    try:
        rightBank = MovingBoatMeas.find('rightBank')
        if rightBank.text is None:
            movingBoatMeasurementsManager.rightBankOtherCtrl = ""  
        else:
            movingBoatMeasurementsManager.rightBankOtherCtrl = rightBank.text
            if "imported" in rightBank.attrib and rightBank.attrib['imported'] == "1":
                movingBoatMeasurementsManager.GetRightBankOtherCtrl().SetBackgroundColour(bkColor)
            else:
                movingBoatMeasurementsManager.GetRightBankOtherCtrl().SetBackgroundColour(white)
    except:
        rightBank = ""
        movingBoatMeasurementsManager.rightBankOtherCtrl = ""


    if leftBankChoice == "Other":
        movingBoatMeasurementsManager.GetLeftBankOtherCtrl().Show()
    if rightBankChoice == "Other":
        movingBoatMeasurementsManager.GetRightBankOtherCtrl().Show()

    edgeDistMmntMethod = MovingBoatMeas.find('edgeDistMmntMethod')
    if edgeDistMmntMethod.text is None:
        movingBoatMeasurementsManager.edgeDistMmntCmbo = ""  
    else:
        movingBoatMeasurementsManager.edgeDistMmntCmbo = edgeDistMmntMethod.text
        if "imported" in edgeDistMmntMethod.attrib and edgeDistMmntMethod.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetEdgeDistMmntCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetEdgeDistMmntCmbo().SetBackgroundColour(white)

    try:
        compositeTrackCmbo = MovingBoatMeas.find('compositeTrackCmbo')
    except:
        compositeTrackCmbo = ""
    if compositeTrackCmbo.text is None:
        movingBoatMeasurementsManager.compositeTrackCmbo = ""  
    else:
        movingBoatMeasurementsManager.compositeTrackCmbo = compositeTrackCmbo.text
        if "imported" in compositeTrackCmbo.attrib and compositeTrackCmbo.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetCompositeTrackCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetCompositeTrackCmbo().SetBackgroundColour(white)

    try:
        depthRefCmbo = MovingBoatMeas.find('depthRefCmbo')
    except:
        depthRefCmbo = ""
    if depthRefCmbo.text is None:
        movingBoatMeasurementsManager.depthRefCmbo = ""  
    else:
        movingBoatMeasurementsManager.depthRefCmbo = depthRefCmbo.text
        if "imported" in depthRefCmbo.attrib and depthRefCmbo.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetDepthRefCmbo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetDepthRefCmbo().SetBackgroundColour(white)

    try:
        velocityTopCombo = MovingBoatMeas.find('velocityTopCombo')
    except:
        velocityTopCombo = ""
    if velocityTopCombo.text is None:
        movingBoatMeasurementsManager.velocityTopCombo = ""  
    else:
        movingBoatMeasurementsManager.velocityTopCombo = velocityTopCombo.text
        if "imported" in velocityTopCombo.attrib and velocityTopCombo.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetVelocityTopCombo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetVelocityTopCombo().SetBackgroundColour(white)


    try:
        velocityBottomCombo = MovingBoatMeas.find('velocityBottomCombo')
    except:
        velocityBottomCombo = ""
    if velocityBottomCombo.text is None:
        movingBoatMeasurementsManager.velocityBottomCombo = ""  
    else:
        movingBoatMeasurementsManager.velocityBottomCombo = velocityBottomCombo.text
        if "imported" in velocityBottomCombo.attrib and velocityBottomCombo.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetVelocityBottomCombo().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetVelocityBottomCombo().SetBackgroundColour(white)


    try:
        velocityExponentCtrl = MovingBoatMeas.find('velocityExponentCtrl')
    except:
        velocityExponentCtrl = ""
    if velocityExponentCtrl.text is None:
        movingBoatMeasurementsManager.velocityExponentCtrl = ""  
    else:
        movingBoatMeasurementsManager.velocityExponentCtrl = velocityExponentCtrl.text
        if "imported" in velocityExponentCtrl.attrib and velocityExponentCtrl.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetVelocityExponentCtrl().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetVelocityExponentCtrl().SetBackgroundColour(white)



    try:
        differenceCtrl = MovingBoatMeas.find('differenceCtrl')
    except:
        differenceCtrl = ""
    if differenceCtrl.text is None:
        movingBoatMeasurementsManager.differenceCtrl = ""  
    else:
        movingBoatMeasurementsManager.differenceCtrl = differenceCtrl.text
        if "imported" in differenceCtrl.attrib and differenceCtrl.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetDifferenceCtrl().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetDifferenceCtrl().SetBackgroundColour(white)



    try:
        extrapUncerCtrl = MovingBoatMeas.find('extrapUncerCtrl')
    except:
        extrapUncerCtrl = ""
    if extrapUncerCtrl is not None and extrapUncerCtrl.text is None:
        movingBoatMeasurementsManager.extrapUncerCtrl = ""  
    else:
        if extrapUncerCtrl is not None:
            movingBoatMeasurementsManager.extrapUncerCtrl = extrapUncerCtrl.text
            if "imported" in extrapUncerCtrl.attrib and extrapUncerCtrl.attrib['imported'] == "1":
                movingBoatMeasurementsManager.GetExtrapUncerCtrl().SetBackgroundColour(bkColor)
            else:
                movingBoatMeasurementsManager.GetExtrapUncerCtrl().SetBackgroundColour(white)






    # lock = MovingBoatMeas.find('lock').text
    # movingBoatMeasurementsManager.lockCB = "" if lock is None else lock


    for row in range(len(movingBoatMeasurementsManager.tableSizer.GetChildren()) - 2):

        movingBoatMeasurementsManager.SetTableValue(row, 1, "False")
        movingBoatMeasurementsManager.SetTableValue(row, 2, "")
        movingBoatMeasurementsManager.SetTableValue(row, 3, "")
        movingBoatMeasurementsManager.SetTableValue(row, 4, "00:00:00")
        movingBoatMeasurementsManager.SetTableValue(row, 6, "")
        movingBoatMeasurementsManager.SetTableValue(row, 7, "")
        movingBoatMeasurementsManager.SetTableValue(row, 8, "")
        movingBoatMeasurementsManager.SetTableValue(row, 9, "")
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



        transectIDColor = ADCPMeasRow.find('transectID').get('imported')
        startDistanceColor = ADCPMeasRow.find('startDistance').get('imported')
        endDistanceColor = ADCPMeasRow.find('endDistance').get('imported')
        rawDischargeColor = ADCPMeasRow.find('rawDischarge').get('imported')
        # finalDischargeColor = ADCPMeasRow.find('finalDischarge').get('color')
        remarksColor = ADCPMeasRow.find('remarks').get('imported')


        movingBoatMeasurementsManager.SetTableValue(row, 1, "False" if checked is None else checked)
        movingBoatMeasurementsManager.SetTableValue(row, 2, "" if transectID is None else transectID)
        movingBoatMeasurementsManager.SetTableValue(row, 3, "" if startBank is None else startBank)
        movingBoatMeasurementsManager.SetTableValue(row, 4, "" if startTime is None else startTime)
        movingBoatMeasurementsManager.SetTableValue(row, 6, "" if startDistance is None else startDistance)
        movingBoatMeasurementsManager.SetTableValue(row, 7, "" if endDistance is None else endDistance)
        movingBoatMeasurementsManager.SetTableValue(row, 8, "" if rawDischarge is None else rawDischarge)
        # movingBoatMeasurementsManager.SetTableValue(row, 8, "" if finalDischarge is None else finalDischarge)
        movingBoatMeasurementsManager.SetTableValue(row, 9, "" if remarks is None else remarks)

        # grey = (210, 210, 210)
        # "1" = 'Grey'
        # white = 'White'

        if transectIDColor == "1":
            movingBoatMeasurementsManager.SetTableColor(row, 2, bkColor)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 2, white)
        if startDistanceColor == "1":
            movingBoatMeasurementsManager.SetTableColor(row, 6, bkColor)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 6, white)
        if endDistanceColor == "1":
            movingBoatMeasurementsManager.SetTableColor(row, 7, bkColor)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 7, white)
        if rawDischargeColor == "1":
            movingBoatMeasurementsManager.SetTableColor(row, 8, bkColor)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 8, white)
        # if finalDischargeColor == "1":
        #     movingBoatMeasurementsManager.SetTableColor(row, 8, grey)
        # else:
        #     movingBoatMeasurementsManager.SetTableColor(row, 8, white)
        if remarksColor == "1":
            movingBoatMeasurementsManager.SetTableColor(row, 9, bkColor)
        else:
            movingBoatMeasurementsManager.SetTableColor(row, 9, white)


    ADCPMeasResults = MovingBoatMeas.find('ADCPMeasResults')
    mmntStartTime = ADCPMeasResults.find('mmntStartTime').text
    movingBoatMeasurementsManager.mmntStartTimeCtrl = "" if mmntStartTime is None else mmntStartTime

    mmntEndTime = ADCPMeasResults.find('mmntEndTime').text
    movingBoatMeasurementsManager.mmntEndTimeCtrl = "" if mmntEndTime is None else mmntEndTime

    mmntMeanTime = ADCPMeasResults.find('mmntMeanTime').text
    movingBoatMeasurementsManager.mmntMeanTimeCtrl = "" if mmntMeanTime is None else mmntMeanTime

    # rawDischargeMean = ADCPMeasResults.find('rawDischargeMean').text
    # movingBoatMeasurementsManager.rawDischMeanCtrl = "" if rawDischargeMean is None else rawDischargeMean

    mbCorrectionApplied = ADCPMeasResults.find('mbCorrectionApplied')
    if mbCorrectionApplied.text is None:

        movingBoatMeasurementsManager.mbCorrAppCtrl = "" 
    else:
        movingBoatMeasurementsManager.mbCorrAppCtrl = mbCorrectionApplied.text
        if "imported" in mbCorrectionApplied.attrib and mbCorrectionApplied.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetMbCorrAppCtrl().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetMbCorrAppCtrl().SetBackgroundColour(white)

    finalDischargeMean = ADCPMeasResults.find('finalDischargeMean')
    if finalDischargeMean.text is None:
        movingBoatMeasurementsManager.finalDischCtrl = ""
    else:
        movingBoatMeasurementsManager.finalDischCtrl = finalDischargeMean.text
        if "imported" in finalDischargeMean.attrib and finalDischargeMean.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetFinalDischCtrl().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetFinalDischCtrl().SetBackgroundColour(white)


    correctedMeanGaugeHeight = ADCPMeasResults.find('correctedMeanGaugeHeight').text
    movingBoatMeasurementsManager.corrMeanGHCtrl = "" if correctedMeanGaugeHeight is None else correctedMeanGaugeHeight

    baseCurveGaugeHeight = ADCPMeasResults.find('baseCurveGaugeHeight').text
    movingBoatMeasurementsManager.baseCurveGHCtrl = "" if baseCurveGaugeHeight is None else baseCurveGaugeHeight

    calcBaseCurveDischarge = ADCPMeasResults.find('calcBaseCurveDischarge').text
    movingBoatMeasurementsManager.baseCurveDischCtrl = "" if calcBaseCurveDischarge is None else calcBaseCurveDischarge

    standardDevMeanDischarge = ADCPMeasResults.find('standardDevMeanDischarge')
    if standardDevMeanDischarge.text is None:
        movingBoatMeasurementsManager.standDevMeanDischCtrl = ""  
    else:
        movingBoatMeasurementsManager.standDevMeanDischCtrl = standardDevMeanDischarge.text
        if "imported" in standardDevMeanDischarge.attrib and standardDevMeanDischarge.attrib['imported'] == "1":
            movingBoatMeasurementsManager.GetStandDevMeanDischCtrl().SetBackgroundColour(bkColor)
        else:
            movingBoatMeasurementsManager.GetStandDevMeanDischCtrl().SetBackgroundColour(white)

    calculateShiftforBaseCurve = ADCPMeasResults.find('calculateShiftforBaseCurve').text
    movingBoatMeasurementsManager.calcShiftBaseCurveCtrl = "" if calculateShiftforBaseCurve is None else calculateShiftforBaseCurve

    dischargeDifferenceBaseCurve = ADCPMeasResults.find('dischargeDifferenceBaseCurve').text
    movingBoatMeasurementsManager.dischDiffBaseCurveCtrl = "" if dischargeDifferenceBaseCurve is None else dischargeDifferenceBaseCurve

    comments = ADCPMeasResults.find('comments').text
    movingBoatMeasurementsManager.commentsCtrl = "" if comments is None else comments

# Create XML structure for Midsection Method Information
def MidsecMeasAsXMLTree(MidsecMeas, midsecMeasurementsManager):
    panelObjs = midsecMeasurementsManager.GetPanelObjs()
    #Midsection Panel
    date = midsecMeasurementsManager.manager.genInfoManager.datePicker
    date = date.replace("/", "-")

    # startTimeCtrl = date + "T" + str(midsecMeasurementsManager.startTimeCtrl) + ":00Z"
    # endTimeCtrl = date + "T" + str(midsecMeasurementsManager.endTimeCtrl) + ":00Z"

    startTimeCtrl = str(midsecMeasurementsManager.startTimeCtrl) if midsecMeasurementsManager.startTimeCtrl != ":" else ""
    endTimeCtrl = str(midsecMeasurementsManager.endTimeCtrl) if midsecMeasurementsManager.endTimeCtrl != ":" else ""


    #Level 1
    DischargeMeasurement = SubElement(MidsecMeas, 'DischargeMeasurement')

    #Level 2
    MmtInitAndSummary = SubElement(DischargeMeasurement, "MmtInitAndSummary")
    Channels = SubElement(DischargeMeasurement, 'Channels')

    #Level 3
    MmtInit = SubElement(MmtInitAndSummary, "MmtInit")
    MetersUsed = SubElement(MmtInitAndSummary, "MetersUsed")
    MmtSummary = SubElement(MmtInitAndSummary, "MmtSummary")



    deployMethodCtrl = SubElement(MmtInit, 'DeploymentMethod')
    deployMethodCtrl.text = str(midsecMeasurementsManager.deployMethodCtrl)

    StartingBank = SubElement(MmtInit, "StartingBank")
    for i in range(len(panelObjs)):
        # if panelObjs[i].panelType == 0:
        if isinstance(panelObjs[i], EdgeObj):
            if str(panelObjs[i].startOrEnd) == "True":
                if "Left" in panelObjs[i].leftOrRight:
                    StartingBank.text = "Left"
                else:
                    StartingBank.text = "Right"
                break

    TagMarkPolarity = SubElement(MmtInit, "TagMarkPolarity")

    InitialPoint = SubElement(MmtInit, "InitialPoint")

    UnmeasuredFlow = SubElement(MmtInit, "UnmeasuredFlow")

    TimeWeightedMeanWaterLevel = SubElement(MmtInit, "TimeWeightedMeanWaterLevel")


    measureSectionCtrl = SubElement(MmtInit, 'measureSectionCtrl')
    measureSectionCtrl.text = str(midsecMeasurementsManager.measureSectionCtrl)

    StartDate = SubElement(MmtSummary, "StartDate")
    StartDate.text = startTimeCtrl

    EndDate = SubElement(MmtSummary, "EndDate")
    EndDate.text = endTimeCtrl

    totalDisCtrl = SubElement(MmtSummary, 'TotalQ')
    totalDisCtrl.text = str(midsecMeasurementsManager.totalDisCtrl)

    areaCtrl = SubElement(MmtSummary, 'TotalArea')
    areaCtrl.text = str(midsecMeasurementsManager.areaCtrl)

    widthCtrl = SubElement(MmtSummary, 'TotalWidth')
    widthCtrl.text = str(midsecMeasurementsManager.widthCtrl)

    avgVelCtrl = SubElement(MmtSummary, 'AverageVelocity')
    avgVelCtrl.text = midsecMeasurementsManager.avgVelCtrl

    avgDepthCtrl = SubElement(MmtSummary, 'AverageDepth')
    avgDepthCtrl.text = midsecMeasurementsManager.avgDepthCtrl

    NumberOfPanels = SubElement(MmtSummary, "NumberOfPanels")
    NumberOfPanels.text = str(midsecMeasurementsManager.numOfPanelCtrl)

    Uncertainty = SubElement(MmtSummary, 'Uncertainty')
    Uncertainty.text = str(midsecMeasurementsManager.uncertaintyCtrl)

    nextPid = SubElement(MidsecMeas, 'nextPid')
    nextPid.text = str(midsecMeasurementsManager.nextPid)


    newChannel = True
    edgeCounter = 0

    for i in range(len(panelObjs)):
        if newChannel:
            Channel = SubElement(Channels, 'Channel')
            Panels = SubElement(Channel, "Panels")
            Edges = SubElement(Channel, "Edges")

            newChannel = False

        # if panelObjs[i].panelType == 1:
        if isinstance(panelObjs[i], PanelObj):
            dateTimeValue = date + "T" + str(panelObjs[i].time) + ":00Z"
            Panel = SubElement(Panels, "Panel", Date=dateTimeValue)

            panelId = SubElement(Panel, "panelId")
            panelId.text = str(panelObjs[i].pid) if panelObjs[i].pid is not None else str(midsecMeasurementsManager.GenerateNextPid())

            distance = SubElement(Panel, "Tagmark")
            distance.text = str(panelObjs[i].distance)

            reverseFlow = SubElement(Panel, "ReverseFlow")
            reverseFlow.text = str(panelObjs[i].reverseFlow)

            obliqueCorrection = SubElement(Panel, "AngleOfFlowCoefficient")
            obliqueCorrection.text = str(panelObjs[i].obliqueCorrection)

            DepthReading = SubElement(Panel, "DepthReading")

            DepthWithOffset = SubElement(Panel, "DepthWithOffset")
            

            width = SubElement(Panel, "Width")
            width.text = str(panelObjs[i].width) if panelObjs[i].width is not None else ""

            corrMeanVelocity = SubElement(Panel, "AverageVelocity")
            corrMeanVelocity.text = str(panelObjs[i].corrMeanVelocity) if panelObjs[i].corrMeanVelocity is not None else ""


            discharge = SubElement(Panel, "Discharge")
            discharge.text = str(panelObjs[i].discharge) if panelObjs[i].discharge is not None else ""

            PanelNum = SubElement(Panel, "PanelNum")
            PanelNum.text = str(panelObjs[i].panelNum) if panelObjs[i].panelNum is not None else ""

            panelCondition = str(panelObjs[i].panelCondition) if panelObjs[i].panelCondition is not None else ""

            slop = SubElement(Panel, "Slop")
            slop.text = str(panelObjs[i].slop) if panelObjs[i].slop is not None else ""

            slop2 = SubElement(Panel, "Slop2")
            slop2.text = str(panelObjs[i].slop2) if panelObjs[i].slop2 is not None else ""

            slopBtn1 = SubElement(Panel, "SlopBtn1")
            slopBtn1.text = str(panelObjs[i].slopBtn1) if panelObjs[i].slopBtn1 is not None else ""

            intercept = SubElement(Panel, "Intercept")
            intercept.text = str(panelObjs[i].intercept) if panelObjs[i].intercept is not None else ""

            intercept2 = SubElement(Panel, "Intercept2")
            intercept2.text = str(panelObjs[i].intercept2) if panelObjs[i].intercept2 is not None else ""

            wldl = SubElement(Panel, "Wldl")
            wldl.text = str(panelObjs[i].wldl) if panelObjs[i].wldl is not None else ""

            dryAngle = SubElement(Panel, "DryAngle")
            dryAngle.text = str(panelObjs[i].dryAngle) if panelObjs[i].dryAngle is not None else ""

            distWaterSurface = SubElement(Panel, "DistWaterSurface")
            distWaterSurface.text = str(panelObjs[i].distWaterSurface) if panelObjs[i].distWaterSurface is not None else ""


            dryCorrection = SubElement(Panel, "DryCorrection")
            dryCorrection.text = str(panelObjs[i].dryCorrection) if panelObjs[i].dryCorrection is not None else ""

            wetCorrection = SubElement(Panel, "WetCorrection")
            wetCorrection.text = str(panelObjs[i].wetCorrection) if panelObjs[i].wetCorrection is not None else ""

            # depthPanelLock = SubElement(Panel, "DepthPanelLock")
            # depthPanelLock.text = str(panelObjs[i].depthPanelLock) if panelObjs[i].depthPanelLock is not None else ""

            depthWithOffset = ""

            if panelCondition == "Open":
                Open = SubElement(Panel, "Open") 

                depthReading = panelObjs[i].openDepthRead  
                weightMeterOffset = panelObjs[i].offset

                deployMethodCtrl = SubElement(Open, 'DeploymentMethod')
                deployMethodCtrl.text = str(midsecMeasurementsManager.deployMethodCtrl)

                weight = SubElement(Open, "AmountOfWeight")
                weight.text = str(panelObjs[i].weight)

                offset = SubElement(Open, "DistanceAboveWeight")
                offset.text = weightMeterOffset

                TotalDepth = SubElement(Open, "TotalDepth")
                TotalDepth.text = str(panelObjs[i].openEffectiveDepth)

         
                if depthReading != "":
                    if weightMeterOffset == "":
                        depthWithOffset = depthReading
                    else:
                        depthWithOffset = str(float(depthReading) + float(weightMeterOffset))
            else:
                IceCovered = SubElement(Panel, "IceCovered")
                depthReading = panelObjs[i].iceDepthRead 

                IceAssembly = SubElement(IceCovered, "IceAssembly")
                IceAssembly.text = str(panelObjs[i].iceAssembly)

                DistanceAboveWeight = SubElement(IceCovered, "DistanceAboveWeight")
                DistanceAboveWeight.text = str(panelObjs[i].distAboveWeight)

                MeterAboveFooting = SubElement(IceCovered, "MeterAboveFooting")
                MeterAboveFooting.text = str(panelObjs[i].aboveFoot)

                MeterBelowFooting = SubElement(IceCovered, "MeterBelowFooting")
                MeterBelowFooting.text = str(panelObjs[i].belowFoot)

                IceThickness = SubElement(IceCovered, "IceThickness")
                IceThickness.text = str(panelObjs[i].iceThickness)

                WaterSurfaceToBottomOfIce = SubElement(IceCovered, "WaterSurfaceToBottomOfIce")
                WaterSurfaceToBottomOfIce.text = str(panelObjs[i].wsBottomIce)

                Slush = SubElement(IceCovered, "Slush")
                Slush.text = str(panelObjs[i].slush)

                WaterSurfaceToBottomOfSlush = SubElement(IceCovered, "WaterSurfaceToBottomOfSlush")
                WaterSurfaceToBottomOfSlush.text = str(panelObjs[i].wsBottomSlush)

                SlushThickness = SubElement(IceCovered, "SlushThickness")
                SlushThickness.text = str(panelObjs[i].thickness)

                EffectiveDepth = SubElement(IceCovered, "EffectiveDepth")
                EffectiveDepth.text = str(panelObjs[i].iceEffectiveDepth)

                IceAdjusted = SubElement(IceCovered, "IceAdjusted")
                IceAdjusted.text = str(panelObjs[i].iceThicknessAdjusted)

                WSToBottomOfIceAdjusted = SubElement(IceCovered, "WSToBottomOfIceAdjusted")
                WSToBottomOfIceAdjusted.text = str(panelObjs[i].adjusted)


            DepthReading.text = str(depthReading)
            DepthWithOffset.text = depthWithOffset
            
            MeterNumber = SubElement(Panel, "MeterNumber")
            MeterNumber.text = str(panelObjs[i].currentMeter)

            Flow = SubElement(Panel, "Flow")
            Flow.text = str(panelObjs[i].flow)

            PointMeasurements = SubElement(Panel, "PointMeasurements")

            # sequence = SubElement(Panel, "sequence")
            # sequence.text = str(panelObjs[i].sequence)

            for j in range(len(panelObjs[i].depths)):
                pointMeasurement = SubElement(PointMeasurements, "PointMeasurement")

                depths = SubElement(pointMeasurement, "SamplingDepthCoefficient")
                depths.text = str(panelObjs[i].depths[j])

                depthObs = SubElement(pointMeasurement, "MeasurementDepth")
                depthObs.text = str(panelObjs[i].depthObs[j])

                revs = SubElement(pointMeasurement, "Revolutions")
                revs.text = str(panelObjs[i].revs[j])

                revTimes = SubElement(pointMeasurement, "ElapsedTime")
                revTimes.text = str(panelObjs[i].revTimes[j])

                pointVels = SubElement(pointMeasurement, "Velocity")
                pointVels.text = str(panelObjs[i].pointVels[j])

                velocityCorrFactor = SubElement(pointMeasurement, "VelocityCoefficient")
                velocityCorrFactor.text = str(panelObjs[i].velocityCorrFactor) if panelObjs[i].velocityCorrFactor is not None else ""

                meanVelocity = SubElement(pointMeasurement, "MeanVelocity")
                meanVelocity.text = str(panelObjs[i].meanVelocity) if panelObjs[i].meanVelocity is not None else ""

        elif isinstance(panelObjs[i], EdgeObj):
        # elif panelObjs[i].panelType == 0:
            dateTimeValue = date + "T" + str(panelObjs[i].time) + ":00Z"

            Edge = SubElement(Edges, "Edge", Date=dateTimeValue)
            StartingEdge = SubElement(Edge, "StartingEdge")
            StartingEdge.text = str(panelObjs[i].startOrEnd)

            Tagmark = SubElement(Edge, "Tagmark")
            Tagmark.text = str(panelObjs[i].distance) if panelObjs[i].distance is not None else ""

            Depth = SubElement(Edge, "Depth")
            Depth.text = str(panelObjs[i].depth) if panelObjs[i].depth is not None else ""

            DepthSameAsAdjacent = SubElement(Edge, "DepthSameAsAdjacent")
            DepthSameAsAdjacent.text = str(panelObjs[i].depthAdjacent) if panelObjs[i].depthAdjacent is not None else ""

            Velocity = SubElement(Edge, "Velocity")
            Velocity.text = str(panelObjs[i].corrMeanVelocity) if panelObjs[i].corrMeanVelocity is not None else ""

            VelocitySameAsAdjacent = SubElement(Edge, "VelocitySameAsAdjacent")
            VelocitySameAsAdjacent.text = str(panelObjs[i].velocityAdjacent) if panelObjs[i].velocityAdjacent is not None else ""


            panelId = SubElement(Edge, "panelId")
            panelId.text = str(panelObjs[i].pid) if panelObjs[i].pid is not None else  str(midsecMeasurementsManager.GenerateNextPid())

            Width = SubElement(Edge, "Width")
            Area = SubElement(Edge, "Area")
            Discharge = SubElement(Edge, "Discharge")
            LeftOrRight = SubElement(Edge, "LeftOrRight")
            EdgeType = SubElement(Edge, "EdgeType")

            Flow = SubElement(Edge, "Flow")
            


            Width.text = str(panelObjs[i].width) if panelObjs[i].width is not None else ""
            Area.text = str(panelObjs[i].area) if panelObjs[i].area is not None else ""
            Discharge.text = str(panelObjs[i].discharge) if panelObjs[i].discharge is not None else ""
            LeftOrRight.text = str(panelObjs[i].leftOrRight) if panelObjs[i].leftOrRight is not None else ""
            EdgeType.text = str(panelObjs[i].edgeType) if panelObjs[i].edgeType is not None else ""

            Flow.text = str(panelObjs[i].flow)if panelObjs[i].flow is not None else ""


            edgeCounter += 1
            if edgeCounter%2 == 0:
                newChannel = True

    Meter1 = SubElement(MetersUsed, "Meter")
    Meter2 = SubElement(MetersUsed, "Meter")

    meter1MeterNoCtrl = SubElement(Meter1, 'Number')
    meter1MeterNoCtrl.text = str(midsecMeasurementsManager.meter1MeterNoCtrl)

    Equation1_1 = SubElement(Meter1, "Equation")
    Type1_1 = SubElement(Equation1_1, "Type")



    meter1SlopeCtrl1 = SubElement(Equation1_1, "Slope")
    meter1SlopeCtrl1.text = str(midsecMeasurementsManager.meter1SlopeCtrl1)

    meter1InterceptCtrl1 = SubElement(Equation1_1, 'Intercept')
    meter1InterceptCtrl1.text = str(midsecMeasurementsManager.meter1InterceptCtrl1)


    Equation1_2 = SubElement(Meter1, "Equation")
    Type1_2 = SubElement(Equation1_2, "Type")

    meter1SlopeCtrl2 = SubElement(Equation1_2, 'Slope')
    meter1SlopeCtrl2.text = str(midsecMeasurementsManager.meter1SlopeCtrl2)

    meter1InterceptCtrl2 = SubElement(Equation1_2, 'Intercept')
    meter1InterceptCtrl2.text = str(midsecMeasurementsManager.meter1InterceptCtrl2)

    MeterCalibDate = SubElement(Meter1, 'MeterCalibDate')
    MeterCalibDate.text = str(midsecMeasurementsManager.meter1CalibDateCtrl)


    meter2MeterNoCtrl = SubElement(Meter2, 'Number')
    meter2MeterNoCtrl.text = str(midsecMeasurementsManager.meter2MeterNoCtrl)



    Equation2_1 = SubElement(Meter2, "Equation")
    Type2_1 = SubElement(Equation2_1, "Type")



    meter2SlopeCtrl1 = SubElement(Equation2_1, "Slope")
    meter2SlopeCtrl1.text = str(midsecMeasurementsManager.meter2SlopeCtrl1)

    meter2InterceptCtrl1 = SubElement(Equation2_1, 'Intercept')
    meter2InterceptCtrl1.text = str(midsecMeasurementsManager.meter2InterceptCtrl1)


    Equation2_2 = SubElement(Meter2, "Equation")
    Type2_2 = SubElement(Equation2_2, "Type")

    meter2SlopeCtrl2 = SubElement(Equation2_2, 'Slope')
    meter2SlopeCtrl2.text = str(midsecMeasurementsManager.meter2SlopeCtrl2)

    meter2InterceptCtrl2 = SubElement(Equation2_2, 'Intercept')
    meter2InterceptCtrl2.text = str(midsecMeasurementsManager.meter2InterceptCtrl2)

    MeterCalibDate = SubElement(Meter2, 'MeterCalibDate')
    MeterCalibDate.text = str(midsecMeasurementsManager.meter2CalibDateCtrl)


# def MidsecMeasFromXML(MidsecMeas, midsecMeasurementsManager):
#     MidsecMeasFromXML124(MidsecMeas, midsecMeasurementsManager)


# Set Midsection Measurements Information variables from existing XML structure
def MidsecMeasFromXML(MidsecMeas, midsecMeasurementsManager):

    try:

        midsecMeasurementsManager.GetSummaryTable().DeleteRows(0, midsecMeasurementsManager.GetNumberRows())
        midsecMeasurementsManager.GetSummaryTable().AppendRows()
        panelObjs = []
        midsecMeasurementsManager.SetPanelObjs(panelObjs)


        DischargeMeasurement = MidsecMeas.find('DischargeMeasurement')

        # if DischargeMeasurement is not None:

        MmtInitAndSummary = DischargeMeasurement.find("MmtInitAndSummary")
        Channels = DischargeMeasurement.find('Channels')

        MmtInit = MmtInitAndSummary.find("MmtInit")
        MetersUsed = MmtInitAndSummary.find("MetersUsed")
        MmtSummary = MmtInitAndSummary.find("MmtSummary")

        nextPid = MidsecMeas.find("nextPid").text
        midsecMeasurementsManager.nextPid = nextPid


        DeploymentMethod = MmtInit.find('DeploymentMethod').text
        midsecMeasurementsManager.deployMethodCtrl = "" if DeploymentMethod is None else DeploymentMethod
        StartingBank = MmtInit.find('StartingBank').text if MmtInit.find('StartingBank').text is not None else ""
        StartingBank += " Bank"

        TotalQ = MmtSummary.find('TotalQ').text
        midsecMeasurementsManager.totalDisCtrl = "" if TotalQ is None else TotalQ
        TotalArea = MmtSummary.find('TotalArea').text
        midsecMeasurementsManager.areaCtrl = "" if TotalArea is None else TotalArea
        TotalWidth = MmtSummary.find('TotalWidth').text
        midsecMeasurementsManager.widthCtrl = "" if TotalWidth is None else TotalWidth
        AverageVelocity = MmtSummary.find('AverageVelocity').text
        midsecMeasurementsManager.avgVelCtrl = "" if AverageVelocity is None else AverageVelocity
        AverageDepth = MmtSummary.find('AverageDepth').text
        midsecMeasurementsManager.avgDepthCtrl = "" if AverageDepth is None else AverageDepth
        NumberOfPanels = MmtSummary.find('NumberOfPanels').text
        Uncertainty = MmtSummary.find('Uncertainty').text
        midsecMeasurementsManager.uncertaintyCtrl = "" if Uncertainty is None else Uncertainty

        measureSectionCtrl = MmtInit.find('measureSectionCtrl').text
        midsecMeasurementsManager.measureSectionCtrl = "" if measureSectionCtrl is None else measureSectionCtrl


        meters = MetersUsed.findall("Meter")
        meterIndex = 0
        for meter in meters:
            equationIndex = 0
            Number = meter.find("Number").text


            equations = meter.findall("Equation")
            for equation in equations:
                Type = equation.find("Type").text
                Slope = equation.find("Slope").text
                Intercept = equation.find("Intercept").text

                if meterIndex == 0 and equationIndex == 0:
                    midsecMeasurementsManager.meter1SlopeCtrl1 = Slope if Slope is not None else ""
                    midsecMeasurementsManager.meter1InterceptCtrl1 = Intercept if Intercept is not None else ""
                elif meterIndex == 0 and equationIndex == 1:
                    midsecMeasurementsManager.meter1SlopeCtrl2 = Slope if Slope is not None else ""
                    midsecMeasurementsManager.meter1InterceptCtrl2 = Intercept if Intercept is not None else ""
                elif meterIndex == 1 and equationIndex == 0:
                    midsecMeasurementsManager.meter2SlopeCtrl1 = Slope if Slope is not None else ""
                    midsecMeasurementsManager.meter2InterceptCtrl1 = Intercept if Intercept is not None else ""
                else:
                    midsecMeasurementsManager.meter2SlopeCtrl2 = Slope if Slope is not None else ""
                    midsecMeasurementsManager.meter2InterceptCtrl2 = Intercept if Intercept is not None else ""

                equationIndex += 1


            meterCalibDate = meter.find("MeterCalibDate").text



            if meterIndex == 0:
                midsecMeasurementsManager.meter1MeterNoCtrl = Number if Number is not None else ""
                midsecMeasurementsManager.meter1CalibDateCtrl = meterCalibDate if meterCalibDate is not None else ""
            else:
                midsecMeasurementsManager.meter2MeterNoCtrl = Number if Number is not None else ""
                midsecMeasurementsManager.meter2CalibDateCtrl = meterCalibDate if meterCalibDate is not None else ""

            meterIndex += 1

      
        channels = Channels.findall('Channel')

        for channel in channels:
            emptyChannel = True
            Panels = channel.find('Panels')
            Edges = channel.find('Edges')

            panels = Panels.findall('Panel')
            edges = Edges.findall('Edge')

            summarytable = midsecMeasurementsManager.GetSummaryTable()
            if emptyChannel:
                edge = edges[0]
                StartingEdge = edge.find('StartingEdge').text if edge.find("StartingEdge").text is not None else ""
                Tagmark = edge.find('Tagmark').text if edge.find("Tagmark").text is not None else ""
                Depth = edge.find('Depth').text if edge.find("Depth").text is not None else ""
                DepthSameAsAdjacent = edge.find('DepthSameAsAdjacent').text if edge.find("DepthSameAsAdjacent").text is not None else ""
                DepthSameAsAdjacent = True if DepthSameAsAdjacent == "True" else False
                Velocity = edge.find('Velocity').text if edge.find("Velocity").text is not None else ""
                VelocitySameAsAdjacent = edge.find('VelocitySameAsAdjacent').text if edge.find("VelocitySameAsAdjacent").text is not None else ""
                VelocitySameAsAdjacent = True if VelocitySameAsAdjacent == "True" else False
                Width = edge.find('Width').text if edge.find("Width").text is not None else ""
                Area = edge.find('Area').text if edge.find("Area").text is not None else ""
                Discharge = edge.find('Discharge').text if edge.find("Discharge").text is not None else ""
                LeftOrRight = edge.find("LeftOrRight").text if edge.find("LeftOrRight").text is not None else ""
                EdgeType = edge.find('EdgeType').text if edge.find("EdgeType").text is not None else ""
                Date = edge.get('Date')[11:16]
                panelId = edge.find("panelId").text if edge.find("panelId").text is not None else ""

                if "Edge" in str(EdgeType):
                    if StartingEdge == "True":
                        panelNum = "Start Edge"
                    else:
                        panelNum = "End Edge"
                else:
                    if StartingEdge == "True":
                        panelNum = "Start P / ISL"
                    else:
                        panelNum = "End P / ISL"

                obj = EdgeObj(edgeType=EdgeType, time=Date, distance=Tagmark, startOrEnd=StartingEdge, leftOrRight=LeftOrRight, panelNum=panelNum,\
                    depth=Depth, corrMeanVelocity=Velocity, depthAdjacent=True if DepthSameAsAdjacent=="True" else False, \
                    velocityAdjacent=True if VelocitySameAsAdjacent=="True" else False, \
                    pid=panelId)

                if obj is not None:
                    midsecMeasurementsManager.AddRow(obj)
                    emptyChannel = False
                    # midsecMeasurementsManager.GetNextPid()

            for panel in panels:
                Date = panel.get('Date')[11:16]
                distance = panel.find('Tagmark').text if panel.find("Tagmark").text is not None else ""
                reverseFlow = panel.find('ReverseFlow').text if panel.find("ReverseFlow").text is not None else ""
                obliqueCorrection = panel.find('AngleOfFlowCoefficient').text if panel.find("AngleOfFlowCoefficient").text is not None else ""
                DepthReading = panel.find('DepthReading').text if panel.find("DepthReading").text is not None else ""
                width = panel.find('Width').text if panel.find("Width").text is not None else ""
                corrMeanVelocity = panel.find('AverageVelocity').text if panel.find("AverageVelocity").text is not None else ""
                discharge = panel.find('Discharge').text if panel.find("Discharge").text is not None else ""
                panelNum = panel.find('PanelNum').text if panel.find("PanelNum").text is not None else ""



                MeterNumber = panel.find('MeterNumber').text if panel.find("MeterNumber").text is not None else ""
                slop = panel.find("Slop").text if panel.find("Slop").text is not None else ""
                slop2 = panel.find("Slop2").text if panel.find("Slop2").text is not None else ""
                slopBtn1 = panel.find("SlopBtn1").text if panel.find("SlopBtn1").text is not None else ""
                intercept = panel.find("Intercept").text if panel.find("Intercept").text is not None else ""
                intercept2 = panel.find("Intercept2").text if panel.find("Intercept2").text is not None else ""
                wldl = panel.find("Wldl").text if panel.find("Wldl").text is not None else ""
                dryAngle = panel.find("DryAngle").text if panel.find("DryAngle").text is not None else ""
                distWaterSurface = panel.find("DistWaterSurface").text if panel.find("DistWaterSurface").text is not None else ""
                dryCorrection = panel.find("DryCorrection").text if panel.find("DryCorrection").text is not None else ""
                wetCorrection = panel.find("WetCorrection").text if panel.find("WetCorrection").text is not None else ""
                panelId = panel.find("panelId").text if panel.find("panelId").text is not None else ""

                # depthPanelLock = panel.find("DepthPanelLock").text if panel.find("DepthPanelLock").text is not None else ""

                # depthPanelLock = True if depthPanelLock == "True" else False


                SamplingDepthCoefficients = []
                MeasurementDepths = []
                Revolutions = []
                ElapsedTimes = []
                Velocities = []
                VelocityCoefficient = ""
                MeanVelocity = ""
                velocityMethod = ""


                PointMeasurements = panel.find('PointMeasurements')
                pointMeasurements = PointMeasurements.findall('PointMeasurement')


                if len(pointMeasurements) > 0:
                    if len(pointMeasurements) == 2:
                        velocityMethod = "0.2/0.8"
                    elif len(pointMeasurements) == 3:
                        velocityMethod == "0.2/0.6/0.8"
                    else:
                        velocityMethod = pointMeasurements[0].find("SamplingDepthCoefficient").text


                    for pointMeasurement in pointMeasurements:
                        SamplingDepthCoefficients.append(pointMeasurement.find('SamplingDepthCoefficient').text if pointMeasurement.find('SamplingDepthCoefficient').text is not None else "")
                        MeasurementDepths.append(pointMeasurement.find('MeasurementDepth').text if pointMeasurement.find('MeasurementDepth').text is not None else "")
                        Revolutions.append(pointMeasurement.find('Revolutions').text if pointMeasurement.find('Revolutions').text is not None else "")
                        ElapsedTimes.append(pointMeasurement.find('ElapsedTime').text if pointMeasurement.find('ElapsedTime').text is not None else "")
                        Velocities.append(pointMeasurement.find('Velocity').text if pointMeasurement.find('Velocity').text is not None else "")
                        VelocityCoefficient = pointMeasurement.find('VelocityCoefficient').text if VelocityCoefficient == "" else VelocityCoefficient
                        VelocityCoefficient = "" if VelocityCoefficient is None else VelocityCoefficient
                        MeanVelocity = pointMeasurement.find('MeanVelocity').text if MeanVelocity == "" else MeanVelocity
                        MeanVelocity = "" if MeanVelocity is None else MeanVelocity


                PointMeasurements = panel.find("PointMeasurements")
                if panel.find('Open') is not None:
                    panelCondition = "Open"
                    Open = panel.find('Open')

                    deploymentMethod = Open.find("DeploymentMethod").text if Open.find("DeploymentMethod").text is not None else ""
                    weight = Open.find("AmountOfWeight").text if Open.find("AmountOfWeight").text is not None else ""
                    offset = Open.find("DistanceAboveWeight").text if Open.find("DistanceAboveWeight").text is not None else ""
                    TotalDepth = Open.find("TotalDepth").text if Open.find("TotalDepth").text is not None else ""



                    obj = PanelObj(panelNum=panelNum, distance=distance, #, depth=depth, \
                    depths=SamplingDepthCoefficients, depthObs=MeasurementDepths, revs=Revolutions, revTimes=ElapsedTimes, pointVels=Velocities,\
                    meanVelocity=MeanVelocity, corrMeanVelocity=corrMeanVelocity,\
                    velocityMethod=velocityMethod, panelCondition=panelCondition,\
                    currentMeter=MeterNumber, time=Date,\
                    slop=slop, intercept=intercept, slop2=slop2,\
                    intercept2=intercept2, slopBtn1=True if slopBtn1 == "True" else False,\
                    openDepthRead=DepthReading, weight=weight, \
                    offset=offset, wldl=wldl, \
                    dryAngle=dryAngle, distWaterSurface=distWaterSurface, \
                    dryCorrection=dryCorrection, wetCorrection=wetCorrection, \
                    openEffectiveDepth=TotalDepth,\
                    obliqueCorrection=obliqueCorrection, velocityCorrFactor=VelocityCoefficient, #depthPanelLock=depthPanelLock, \
                    reverseFlow=True if reverseFlow == "True" else False, pid=panelId)



                elif panel.find("IceCovered") is not None:
                    panelCondition = "Ice"
                    IceCovered = panel.find("IceCovered")

                    IceAssembly = IceCovered.find("IceAssembly").text if IceCovered.find("IceAssembly").text is not None else ""
                    DistanceAboveWeight = IceCovered.find("DistanceAboveWeight").text if IceCovered.find("DistanceAboveWeight").text is not None else ""
                    MeterAboveFooting = IceCovered.find("MeterAboveFooting").text if IceCovered.find("MeterAboveFooting").text is not None else ""
                    MeterBelowFooting = IceCovered.find("MeterBelowFooting").text if IceCovered.find("MeterBelowFooting").text is not None else ""
                    IceThickness = IceCovered.find("IceThickness").text if IceCovered.find("IceThickness").text is not None else ""
                    WaterSurfaceToBottomOfIce = IceCovered.find("WaterSurfaceToBottomOfIce").text if IceCovered.find("WaterSurfaceToBottomOfIce").text is not None else ""
                    Slush = IceCovered.find("Slush").text if IceCovered.find("Slush").text is not None else ""
                    EffectiveDepth = IceCovered.find("EffectiveDepth").text if IceCovered.find("EffectiveDepth").text is not None else ""

                    WaterSurfaceToBottomOfSlush = IceCovered.find("WaterSurfaceToBottomOfSlush").text if IceCovered.find("WaterSurfaceToBottomOfSlush").text is not None else ""
                    SlushThickness = IceCovered.find("SlushThickness").text if IceCovered.find("SlushThickness").text is not None else ""
                    IceAdjusted = IceCovered.find("IceAdjusted").text if IceCovered.find("IceAdjusted").text is not None else ""
                    WSToBottomOfIceAdjusted = IceCovered.find("WSToBottomOfIceAdjusted").text if IceCovered.find("WSToBottomOfIceAdjusted").text is not None else ""
                    

                    obj = PanelObj(panelNum=panelNum, distance=distance,# depth=depth, \
                    depths=SamplingDepthCoefficients, depthObs=MeasurementDepths, revs=Revolutions, revTimes=ElapsedTimes, pointVels=Velocities,\
                    meanVelocity=MeanVelocity, corrMeanVelocity=corrMeanVelocity,\
                    velocityMethod=velocityMethod, panelCondition=panelCondition,\
                    currentMeter=MeterNumber, time=Date,\
                    slop=slop, intercept=intercept, slop2=slop2,\
                    intercept2=intercept2, slopBtn1=slopBtn1,\
                    iceDepthRead=DepthReading, iceAssembly=IceAssembly, \
                    aboveFoot=MeterAboveFooting, belowFoot=MeterBelowFooting, \
                    distAboveWeight=DistanceAboveWeight, wsBottomIce=WaterSurfaceToBottomOfIce, \
                    adjusted=WSToBottomOfIceAdjusted, slush=Slush, \
                    wsBottomSlush=WaterSurfaceToBottomOfSlush, thickness=SlushThickness, iceEffectiveDepth=EffectiveDepth,\
                    obliqueCorrection=obliqueCorrection, velocityCorrFactor=VelocityCoefficient, #depthPanelLock=depthPanelLock, \
                    reverseFlow=True if reverseFlow == "True" else False, pid=panelId,# index=index, \
                    iceThickness=IceThickness, iceThicknessAdjusted=IceAdjusted)

            


                if obj is not None:
                    midsecMeasurementsManager.AddRow(obj)

            if len(edges) > 1:
                edge = edges[1]
                StartingEdge = edge.find('StartingEdge').text if edge.find("StartingEdge").text is not None else ""
                Tagmark = edge.find('Tagmark').text if edge.find("Tagmark").text is not None else ""
                Depth = edge.find('Depth').text if edge.find("Depth").text is not None else ""
                DepthSameAsAdjacent = edge.find('DepthSameAsAdjacent').text if edge.find("DepthSameAsAdjacent").text is not None else ""
                DepthSameAsAdjacent = True if DepthSameAsAdjacent == "True" else False
                Velocity = edge.find('Velocity').text if edge.find("Velocity").text is not None else ""
                VelocitySameAsAdjacent = edge.find('VelocitySameAsAdjacent').text if edge.find("VelocitySameAsAdjacent").text is not None else ""
                VelocitySameAsAdjacent = True if VelocitySameAsAdjacent == "True" else False
                Width = edge.find('Width').text if edge.find("Width").text is not None else ""
                Area = edge.find('Area').text if edge.find("Area").text is not None else ""
                Discharge = edge.find('Discharge').text if edge.find("Discharge").text is not None else ""
                LeftOrRight = edge.find("LeftOrRight").text if edge.find("LeftOrRight").text is not None else ""
                EdgeType = edge.find('EdgeType').text if edge.find("EdgeType").text is not None else ""
                Date = edge.get('Date')[11:16]
                panelId = edge.find("panelId").text if edge.find("panelId").text is not None else ""

                if "Edge" in str(EdgeType):
                    if StartingEdge == "True":
                        panelNum = "Start Edge"
                    else:
                        panelNum = "End Edge"
                else:
                    if StartingEdge == "True":
                        panelNum = "Start P / ISL"
                    else:
                        panelNum = "End P / ISL"

                obj = EdgeObj(edgeType=EdgeType, time=Date, distance=Tagmark, startOrEnd=StartingEdge, leftOrRight=LeftOrRight, panelNum=panelNum,\
                    depth=Depth, corrMeanVelocity=Velocity, depthAdjacent=True if DepthSameAsAdjacent=="True" else False, \
                    velocityAdjacent=True if VelocitySameAsAdjacent=="True" else False, \
                    pid=panelId)

                if obj is not None:
                    midsecMeasurementsManager.AddRow(obj)
    except Exception as e:
        #print str(e)
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        print "Reading XML from version lower than 1_2_5"
        MidsecMeasFromXML124(MidsecMeas, midsecMeasurementsManager)


# Set Midsection Measurements Information variables from version less than 1_2_5
def MidsecMeasFromXML124(MidsecMeas, midsecMeasurementsManager):
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
                     pid=panelId, index=index)

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
                reverseFlow=reverseFlow, pid=panelId, index=index)


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
                reverseFlow=reverseFlow, pid=panelId, index=index, \
                iceThickness=iceThickness, iceThicknessAdjusted=iceThicknessAdjusted)


        if obj is not None:
            midsecMeasurementsManager.AddRow(obj)

            # midsecMeasurementsManager.GetNextPid()




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


