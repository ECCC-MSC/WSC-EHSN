import json
import wx

from collections import Counter



def GetData(filePath):
    with open(filePath, 'r') as jFile:
        data = json.load(jFile)
    return data


def GetStationID(filePath):
    return GetData(filePath)['Properties']['SiteNumber']


def GetDate(filePath):
    return GetData(filePath)['Properties']['StartTime'][:10].replace("-","/")


def GetLocalTimeUtcOffset(filePath):
    # print GetData(filePath)['Properties']['LocalTimeUtcOffset']
    return GetData(filePath)['Properties']['LocalTimeUtcOffset']


def AddDischargeSummary(filePath, disMeasManager, editedFile):
    print("importing discharge summary from ft2")
    color = disMeasManager.manager.gui.importedBGColor
    properties = GetData(filePath)['Properties']

    # print properties['SiteNumber']

    allTimes = []
    allTypes = []
    for st in GetData(filePath)['Stations']:
        allTimes.append(st['CreationTime'])
        allTypes.append(st['StationType'])
    startTime = allTimes[0][11:16]
    endTime = allTimes[-1][11:16]
        
    # If the starting location is the right bank and the ending location is the left bank
    # and the file has been edited, then swap the starting and ending times
    startLocation = allTypes[0]
    endLocation = allTypes[-1]
    if startLocation == 'RightBank' and endLocation == 'LeftBank' and editedFile:
        temp_time = startTime
        startTime = endTime
        endTime = temp_time

    offset = properties['LocalTimeUtcOffset'][:3]
    if offset[0] != '+' and offset[0] != '-':
        offset = offset[:2]

    
    sHour = int(startTime[:2])
    sMinute = int(startTime[3:])

    eHour = int(endTime[:2])
    eMinute = int(endTime[3:])


    if offset == "-03":
        sMinute = int(startTime[3:]) - 30
        eMinute = int(endTime[3:]) - 30

        sHour = sHour - 4 if sMinute < 0 else sHour - 3
        sMinute = sMinute + 60 if sMinute < 0 else sMinute

        eHour = eHour - 4 if eMinute < 0 else eHour - 3
        eMinute = eMinute + 60 if eMinute < 0 else eMinute
    else:
        # print('offset:{}'.format(offset))
        sHour += int(offset)
        eHour += int(offset)

    # Add 0 if the hour is single digit after offset calculation
    sHour_str = str(sHour)
    eHour_str = str(eHour)
    sMinute_str = str(sMinute)
    eMinute_str = str(eMinute)

    if len(sHour_str) < 2:
        sHour_str = "0" + sHour_str
    else:
        sHour_str = sHour_str

    if len(eHour_str) < 2:
        eHour_str = "0" + eHour_str
    else:
        eHour_str = eHour_str

    if len(sMinute_str) < 2:
        sMinute_str = "0" + sMinute_str
    else:
        sMinute_str = sMinute_str

    if len(eMinute_str) < 2:
        eMinute_str = "0" + eMinute_str
    else:
        eMinute_str = eMinute_str


    finalStartTime = sHour_str + ":" + sMinute_str
    finalEndTime = eHour_str + ":" + eMinute_str

    # print finalStartTime
    # print finalEndTime

    #finalStartTime = "0" + finalStartTime if len(finalStartTime) < 5 else finalStartTime
    #finalEndTime = "0" + finalEndTime if len(finalEndTime) < 5 else finalEndTime


    calculations = (GetData(filePath)['Calculations'])

    # depth = calculations['Depth (m)']
    # waterTemp = calculations['Temperature (C)']
    area = calculations['Area (m2)']
    discharge = calculations['Discharge (m3/s)']
    width = calculations['Width (m)']
    meanVelocity = calculations['Velocity (m/s)']['X']
    uncertainty = calculations['UncertaintyIve']['Overall']

    if finalStartTime is not None and finalStartTime != "":
        disMeasManager.startTimeCtrl = finalStartTime
    if finalEndTime is not None and finalEndTime != "":
        disMeasManager.endTimeCtrl = finalEndTime
    # if waterTemp is not None and waterTemp != "":
    #     disMeasManager.waterTempCtrl = str(waterTemp)
    #     myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
    #     myEvent.SetEventObject(disMeasManager.GetWaterTempCtrl())
    #     wx.PostEvent(disMeasManager.GetWaterTempCtrl(), myEvent)
    #     disMeasManager.GetWaterTempCtrl().SetBackgroundColour(color)
    if width is not None and width != "":
        disMeasManager.widthCtrl = str(width)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetWidthCtrl())
        wx.PostEvent(disMeasManager.GetWidthCtrl(), myEvent)
        disMeasManager.GetWidthCtrl().SetBackgroundColour(color)
    if area is not None and area != "":
        disMeasManager.areaCtrl = str(area)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetAreaCtrl())
        wx.PostEvent(disMeasManager.GetAreaCtrl(), myEvent)
        disMeasManager.GetAreaCtrl().SetBackgroundColour(color)
    if meanVelocity is not None and meanVelocity != "":
        disMeasManager.meanVelCtrl = str(meanVelocity)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetMeanVelCtrl())
        wx.PostEvent(disMeasManager.GetMeanVelCtrl(), myEvent)
        disMeasManager.GetMeanVelCtrl().SetBackgroundColour(color)
    if discharge is not None and discharge != "":
        disMeasManager.dischCtrl = str(discharge)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetDischCtrl())
        wx.PostEvent(disMeasManager.GetDischCtrl(), myEvent)
        disMeasManager.GetDischCtrl().SetBackgroundColour(color)
    if uncertainty is not None and uncertainty != "":
        disMeasManager.uncertaintyCtrl = str(round(float(uncertainty)*200, 2))
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetUncertaintyCtrl())
        wx.PostEvent(disMeasManager.GetUncertaintyCtrl(), myEvent)
        disMeasManager.GetUncertaintyCtrl().SetBackgroundColour(color)
    
        # Adding uncertainty text to Discharge Activity Remarks
        dischargeUncertainty = '@ Uncertainty: IVE method, 2-sigma value (2 x Uncertainty Value reported in *.ft File). @'
        dischargeRemarks = disMeasManager.dischRemarksCtrl
        if dischargeRemarks != '':
            disMeasManager.dischRemarksCtrl = dischargeRemarks + '\n' + dischargeUncertainty
        else:
            disMeasManager.dischRemarksCtrl = dischargeUncertainty




#Import information from FlowTracker2 to instrument page
def AddDischargeDetail(filePath, instrDepManager):
    color = instrDepManager.manager.gui.importedBGColor
    data = GetData(filePath)
    stations = Counter(st['StationType'] for st in data['Stations'])
    # print stations
    numberOfPanels = sum(stations.values())

    serial = data['HandheldInfo']['SerialNumber']

    software = data['HandheldInfo']['SoftwareVersion']

    for st in data['Stations']:
        if 'PointMeasurements' in st:
            for pt in st['PointMeasurements']:
                if 'ProbeInfo' in pt:
                    firmware = pt['ProbeInfo']['FirmwareVersion']
                    break


    if firmware is not None and firmware != "":
        instrDepManager.firmwareCmbo = firmware
        instrDepManager.GetFirmwareCmbo().SetBackgroundColour(color)
    if software is not None and software != "":
        instrDepManager.softwareCtrl = software
        instrDepManager.GetSoftwareCtrl().SetBackgroundColour(color)
    if serial is not None and serial != "":
        instrDepManager.serialCmbo = serial
        instrDepManager.GetSerialCmbo().SetBackgroundColour(color)
    if numberOfPanels is not None and numberOfPanels != "":
        # Two panels are subtracted as the edges do not need to be considered
        instrDepManager.numOfPanelsScroll = str(numberOfPanels-2)
        instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(color)

    instrDepManager.instrumentCmbo = "ADV"
    instrDepManager.GetInstrumentCmbo().SetBackgroundColour(color)
    instrDepManager.deploymentCmbo = "Wading"
    instrDepManager.GetDeploymentCmbo().SetBackgroundColour(color)
    instrDepManager.manufactureCmbo = "SonTek"
    instrDepManager.GetManufactureCmbo().SetBackgroundColour(color)
    instrDepManager.modelCmbo = "FlowTracker2"
    instrDepManager.GetModelCmbo().SetBackgroundColour(color)
    instrDepManager.frequencyCmbo = "10000"
    instrDepManager.GetFrequencyCmbo().SetBackgroundColour(color)


# a= GetData("C:\\eHSN\\eHSN_Version_1_2_4_ReleasedVersion_Ingest\\FT2_02KF013_20170328\\02KF013_20170328\\DataFile.json")



if __name__ == '__main__':
    from pdb import set_trace
    calculations = (GetData('imports\\DataFile.json')['Calculations'])
    uncert = calculations['UncertaintyIve']['Overall']
    set_trace()
