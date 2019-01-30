from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element

from datetime import datetime, timedelta
import wx

def GetRawDataSet(path):
    dataSet = []

    file = open(path, 'r')
    lines = file.readlines()

    for i, line in enumerate(lines):
        if line == "\n" or line is None or len(line) == 0:
            del lines[i]
    lines = [x for x in lines if x != []]

    for i in lines:
        if i is not None or i != "": 
            dataSet.append(i.split())

    for index, i in enumerate(dataSet):
        if len(i) == 0:
            del dataSet[index]

    file.close()
    return dataSet

# def GetRawData(path):
#     return open(path, 'r').readlines()

def GetStationID(path):
    dataSet = GetRawDataSet(path)

    for data in dataSet:

        if data[0] == "File_Name":
            return data[1][:7]


    print "Unable to read the dis file"
    return -1

def GetDate(path):
    dataSet = GetRawDataSet(path)

    for data in dataSet:

        if data[0] == "Start_Date_and_Time":
            ConvertToSerialDate(path)
            return data[1][:10]


    
def AddDischargeSummary(path, disMeasManager):

    # startTime, endTime, airTemp, waterTemp, width, area, meanVelocity, discharge = GetDischargeSummary(path)
    startTime, endTime, airTemp, width, area, meanVelocity, discharge = GetDischargeSummary(path)
    color = disMeasManager.manager.gui.importedBGColor

    if startTime is not None and startTime != "":
        disMeasManager.startTimeCtrl = startTime
    if endTime is not None and endTime != "":
        disMeasManager.endTimeCtrl = endTime
    # if waterTemp is not None and waterTemp != "":
    #     disMeasManager.waterTempCtrl = waterTemp
    #     myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
    #     myEvent.SetEventObject(disMeasManager.GetWaterTempCtrl())
    #     wx.PostEvent(disMeasManager.GetWaterTempCtrl(), myEvent)
    #     disMeasManager.GetWaterTempCtrl().SetBackgroundColour(color)
    if width is not None and width != "":
        disMeasManager.widthCtrl = width
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetWidthCtrl())
        wx.PostEvent(disMeasManager.GetWidthCtrl(), myEvent)
        disMeasManager.GetWidthCtrl().SetBackgroundColour(color)
    if area is not None and area != "":
        disMeasManager.areaCtrl = area
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetAreaCtrl())
        wx.PostEvent(disMeasManager.GetAreaCtrl(), myEvent)
        disMeasManager.GetAreaCtrl().SetBackgroundColour(color)
    if meanVelocity is not None and meanVelocity != "":
        disMeasManager.meanVelCtrl = meanVelocity
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetMeanVelCtrl())
        wx.PostEvent(disMeasManager.GetMeanVelCtrl(), myEvent)
        disMeasManager.GetMeanVelCtrl().SetBackgroundColour(color)
    if discharge is not None and discharge != "":
        disMeasManager.dischCtrl = discharge
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetDischCtrl())
        wx.PostEvent(disMeasManager.GetDischCtrl(), myEvent)
        disMeasManager.GetDischCtrl().SetBackgroundColour(color)



def AddDischargeDetail(path, instrDepManager):

    firmware, software, serial, startEdge, numberOfPanels, uncertainISO = GetInstrumentValues(path)
    deployment = "Wading"
    color = instrDepManager.manager.gui.importedBGColor
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
        instrDepManager.numOfPanelsScroll = numberOfPanels
        instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(color)

    instrDepManager.instrumentCmbo = "ADV"
    instrDepManager.GetInstrumentCmbo().SetBackgroundColour(color)
    instrDepManager.GetManufactureCmbo().SetBackgroundColour(color)
    instrDepManager.GetModelCmbo().SetBackgroundColour(color)
    instrDepManager.deploymentCmbo = deployment
    instrDepManager.GetDeploymentCmbo().SetBackgroundColour(color)


        


def GetInstrumentValues(path):
    firmware = ""
    software = ""
    serial = ""
    startEdge = ""
    numberOfPanels = ""
    uncertainISO = ""

    # file = open(path)
    # rawData = file.readlines()
    # for i, line in enumerate(rawData):
    #     if line == "\n": # or line is None or len(line) == 0:
    #         del rawData[i]

    # rawData = [x for x in rawData if x != []]


    # finalData = []
    # for i in rawData:
    #     finalData.append(i.split())

    finalData = GetRawDataSet(path)


    for index, data in enumerate(finalData):
        if len(data) > 0:

            if data[0] == "CPU_Firmware_Version":
                firmware = data[1]

            elif data[0] == "Software_Ver":
                software = data[1]

            elif data[0] == "Serial_#":
                serial = data[1]

            elif data[0] == "Start_Edge":
                startEdge = data[1]
            elif data[0] == "#_Stations" and finalData[index-1][0] == "Start_Edge":
                numberOfPanels = str(int(data[1])-2)

            elif "ISO" in data[0] and finalData[index+1][0] == "Overall":
                uncertainISO = finalData[index+1][1]

    # print uncertainISO, "uncertainISO"



    return firmware, software, serial, startEdge, numberOfPanels, uncertainISO



def GetDischargeSummary(path):

    startTime = ""
    endTime = ""
    airTemp = ""
    waterTemp = ""
    width = ""
    area = ""
    meanVelocity = ""
    discharge = ""
    timesArray = []
    count = 0



    finalData = GetRawDataSet(path)



    for data in finalData:
        if len(data) > 0:

            if data[0] == "Start_Date_and_Time":

                startTime = data[2][:5]

            #elif data[0] == "Mean_Temp":
                #waterTemp = data[1]
            elif data[0] == "Total_Width":
                width = data[1]
            elif data[0] == "Total_Area":
                area = data[1]
            elif data[0] == "Mean_Velocity":
                meanVelocity = data[1]
            elif data[0] == "Total_Discharge":
                discharge = data[1]

            if data[0] == "00":
                for time in finalData[count:len(finalData)]:
                    timesArray.append(time[1]) #store all times from dis file into timesArray

                timesArray = sorted(timesArray) #sorts time values in ascending order
                endTime = timesArray[len(timesArray)-1] #ensures the correct endtime is stored even if times are not recorded in order 
            
            count=count+1

    #print(timesArray)
    #endTime = finalData[-1][1]
    
    

    # return startTime, endTime, airTemp, waterTemp, width, area, meanVelocity, discharge
    return startTime, endTime, airTemp, width, area, meanVelocity, discharge




def GetStartDateTime(path):
    dataSet = GetRawDataSet(path)

    for data in dataSet:

        if data[0] == "Start_Date_and_Time":
            # print data[1].split("/")
            # print data[2].split(":")
            return data[1].split("/"), data[2].split(":")


def ConvertToSerialDate(path):
    date, time = GetStartDateTime(path)
    yy = date[0]
    mm = date[1]
    dd = date[2]
    hh = time[0]
    mi = time[1]
    sec = time[2]
    start = datetime(1899, 12, 30)
    end = datetime(int(yy), int(mm), int(dd), int(hh), int(mi), int(sec))
    # print (end-start).days + float((end-start).seconds)/86400
    return (end-start).days + float((end-start).seconds)/86400


def CreateDiscreteMeasurementDetailsXML():
    imported = Element('Imported')
    discreteMeasurementDetails = SubElement(imported, 'DiscreteMeasurementDetails')
    enteredInHWS.text = str(titleHeaderManager.enteredInHWSCB)



def GetPanelDates(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(GetDate(path) + "T" + i[1] + ":00")
    print res
    print len(res)
    print "-----PanelDates"
    return res

def GetTaglinePositions(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[2])
    print res
    print len(res)
    print "----TaglinePositions"
    return res

# def GetDistanceToShores(path):
#     res = []
#     dataSet = GetRawDataSet(path)
#     readFromNext = False
#     for index, i in enumerate(dataSet):
#         if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
#             readFromNext = True
#             continue
#         if readFromNext:
#             res.append(i[2])
#     print res
#     print len(res)
#     return res


def GetDepths(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[3])
    print res
    print len(res)
    print "----Depths"
    return res


def GetAreas(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[17])
    print res
    print len(res)
    print "----Areas"
    return res

def GetWidths(path):
    tagLines = GetTaglinePositions(path)
    widths = []
    if len(tagLines) != 0:
        for i in range(len(tagLines)):
            if i == 0: 
                widths.append(str(abs((float(tagLines[1]) - float(tagLines[0]))) / 2))
            elif i == len(tagLines) - 1:
                widths.append(str(abs((float(tagLines[-1]) - float(tagLines[-2]))) / 2))
            else:
                widths.append(str(abs((float(tagLines[i+1]) - float(tagLines[i]))) / 2 + abs((float(tagLines[i]) - float(tagLines[i-1]))) / 2))

            # if float(depths[i]) != 0:
            #     widths.append(str(float(areas[i]) / float(depths[i])))
            # else:
            #     widths.append("0")

    print widths
    print len(widths)
    print "-----Widths"
    return widths



def GetAverageVelocities(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[16])
    print res
    print len(res)
    print "-----AverageVelocities"
    return res


def GetDischarges(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[18])
    print res
    print len(res)
    print "------Discharges"
    return res


# def GetMeterNames(path):
#     res = []
#     counter = 0
#     panelNum = 1
#     dataSet = GetRawDataSet(path)
#     for index, i in enumerate(dataSet):
#         if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
#             counter += 1
#             if panelNum < counter:
#                 res.append("")
#                 panelNum += 1

#         elif "MMT." in i[0] and "TIME" in i[1]:
#             if len(i) > 1:
#                 res.append(i[2])
#             else:
#                 res.append("")
#             panelNum += 1
#         elif "--SUMMARY" in i[0]:
#             if panelNum == counter:
#                 res.append("")
#             break
#     # print res
#     # print len(res)
#     return res
# def GetAmountOfWeights(path):
#     res = []
#     counter = 0
#     panelNum = 1
#     dataSet = GetRawDataSet(path)
#     for index, i in enumerate(dataSet):
#         if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
#             counter += 1
#             if panelNum < counter:
#                 res.append("")
#                 panelNum += 1

#         elif "MMT." in i[0] and "TIME" in i[1]:
#             if len(i) > 1:
#                 res.append(i[2])
#             else:
#                 res.append("")
#             panelNum += 1
#         elif "--SUMMARY" in i[0]:
#             if panelNum == counter:
#                 res.append("")
#             break
#     # print res
#     # print len(res)
#     return res
def GetDistanceAboveWeights(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[5])
    print res
    print len(res)
    print "----DistanceAboveWeights"
    return res


# def GetVelocityMethods(path):
#     res = []
#     counter = 0
#     panelNum = 1
#     dataSet = GetRawDataSet(path)
#     for index, i in enumerate(dataSet):
#         if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
#             counter += 1
#             if panelNum < counter:
#                 res.append("")
#                 panelNum += 1

#         elif "MMT." in i[0] and "TIME" in i[1]:
#             if len(i) > 1:
#                 res.append(i[2])
#             else:
#                 res.append("")
#             panelNum += 1
#         elif "--SUMMARY" in i[0]:
#             if panelNum == counter:
#                 res.append("")
#             break
#     # print res
#     # print len(res)
#     return res

def GetDepthReadings(path):
    res = []
    depths = GetDepths(path)
    distances = GetDistanceAboveWeights(path)
    if len(depths) > 0:
        for i in range(len(depths)):
            res.append(str(float(depths[i]) * float(distances[i])))
    print res
    print len(res)
    print "----DepthReadings"
    return res


def GetVelocities(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[9])
    print res
    print len(res)
    print "----Velocities"
    return res


def GetCounts(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[7])
    print res
    print len(res)
    print "----Counts"
    return res

def GetIceCovereds(path):
    res = []
    dataSet = GetRawDataSet(path)
    readFromNext = False
    for index, i in enumerate(dataSet):
        if len(i) > 1 and "()" in i[0] and "()" in i[1]:# or "--SUMMARY" in i[0]:
            readFromNext = True
            continue
        if readFromNext:
            res.append(i[4])
    print res
    print len(res)
    print "----Ice Covered"
    return res


# def GetIntervals(path):
#     res = []
#     counter = 0
#     panelNum = 1
#     dataSet = GetRawDataSet(path)
#     for index, i in enumerate(dataSet):
#         if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
#             counter += 1
#             if panelNum < counter:
#                 res.append("")
#                 panelNum += 1

#         elif "MMT." in i[0] and "TIME" in i[1]:
#             if len(i) > 1:
#                 res.append(i[2])
#             else:
#                 res.append("")
#             panelNum += 1
#         elif "--SUMMARY" in i[0]:
#             if panelNum == counter:
#                 res.append("")
#             break
#     # print res
#     # print len(res)
#     return res

def GetMeanSectionWidths(path):
    meanSectionWidths = []
    taglines = GetTaglinePositions(path)
    if len(taglines) > 0:
        for i in range(len(taglines)):
            if i == 0:
                meanSectionWidths.append("0")
            else:
                meanSectionWidths.append(str(abs((float(taglines[i]) - float(taglines[i-1])))))
    print meanSectionWidths
    print len(meanSectionWidths)
    print "----meanSectionWidths"
    return meanSectionWidths

def GetStartTime(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Start_Date_and_Time" and len(i) > 2:           
            return i[2]

    return ""


def GetDateSpreadsheetFormat(path, eManager):
    time = GetStartTime(path).split(":")
    date = eManager.genInfoManager.datePicker.split("/")

    # print date
    yy = date[0]
    mm = date[1]
    dd = date[2]
    hh = time[0]
    mi = time[1]
    # sec = time[2]
    start = datetime(1899, 12, 30)
    end = datetime(int(yy), int(mm), int(dd), int(hh), int(mi))
    print (end-start).days + float((end-start).seconds)/86400
    return str((end-start).days + float((end-start).seconds)/86400)

# def GetDeploymentMethod(path):
#     dataSet = GetRawDataSet(path)
#     for index, i in enumerate(dataSet):
#         if i[0] == "Start_Date_and_Time" and len(i) > 2:           
#             return i[2]
#     else:
#         return ""

def GetWaterTemperature(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Mean_Temp" and len(i) > 1:
            # print dataSet[1]
            return i[1]    


    return ""

def GetTotalArea(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Total_Area" and len(i) > 1:
            # print dataSet[1]
            return i[1]           

    return ""

def GetTotalWidth(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Total_Width" and len(i) > 1:
            # print dataSet[1]
            return i[1]           

    return ""

def GetMeanVelocity(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Mean_Velocity" and len(i) > 1:
            # print dataSet[1]
            return i[1]           

    return ""

def GetTotalDischarge(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Total_Discharge" and len(i) > 1:
            # print dataSet[1]
            return i[1]           

    return ""

def GetMeanDepth(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Mean_Depth" and len(i) > 1:
            # print dataSet[1]
            return i[1]           

    return ""

def GetStartingBank(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Start_Edge" and len(i) > 1:
            if "L" in i[1]:
            # print dataSet[1]
                return "Left" 
            else:
                return "Right"
    
    return ""


def GetImportFileSoftwareVersion(path):
    dataSet = GetRawDataSet(path)
    version = ""
    for index, i in enumerate(dataSet):
        if i[0] == "Software_Ver" and len(i) > 1:
            for j in range(len(i) - 1):
                tail = "" if j == len(i) else " "
                version += i[j + 1] + tail
    return version

def GetMeasuredBy(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "Operator" in i[0] and len(i) > 1:
            return i[1]
    
    return ""

def GetDischargeUncertaintyISO(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Discharge_Uncertainty_(ISO)":
            if dataSet[index + 1][0] == "Overall" and len(dataSet[index + 1]) > 1:
                return dataSet[index + 1][1]

    return ""


def GetInstrumentType(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Sensor_Type" and len(i) > 1:
            return i[1]

    return ""


        
# def GetMidSectionInfo(path, EHSN):
#     res = {}
#     #String
#     res["DateSpreadsheetFormat"] = GetDateSpreadsheetFormat(path, EHSN)
#     # res["DeploymentMethod"] = GetDeploymentMethod(path)
#     # res["MeasurementSectionCondition"] = GetMeasurementSectionCondition(path)
#     res["TotalDischarge"] = GetTotalDischarge(path)
#     res["TotalArea"] = GetTotalArea(path)
#     res["TotalWidth"] = GetTotalWidth(path)
#     res["MeanVelocity"] = GetMeanVelocity(path)
#     res["MeanDepth"] = GetMeanDepth(path)
#     # res["SerialNumber"] = GetSerialNumber(path)
#     res["MeasuredBy"] = GetMeasuredBy(path)
#     # res["CalculationMethod"] = GetCalculationMethod(path)
#     res["WaterTemperature"] = GetWaterTemperature(path)
#     # res["AirTemperature"] = GetAirTemperature(path)
#     # res["InitialPoint"] = GetInitialPoint(path)
#     # res["StartingPoint"] = GetStartingPoint(path)
#     # res["Condition"] = GetCondition(path)
#     # res["ImportFileSoftwareName"] = GetImportFileSoftwareName(path)
#     res["ImportFileSoftwareVersion"] = GetImportFileSoftwareVersion(path)
#     res["StartingBank"] = GetStartingBank(path)
#     res["DischargeUncertaintyISO"] = GetDischargeUncertaintyISO(path)
#     res["InstrumentType"] = GetInstrumentType(path)

#     print res["TotalDischarge"]
#     print res["TotalArea"]
#     print res["TotalWidth"]
#     print res["MeanVelocity"]
#     print res["WaterTemperature"]
#     print res["MeanDepth"]
#     print res["StartingBank"]
#     print res["ImportFileSoftwareVersion"]
#     print res["MeasuredBy"]
#     print res["DischargeUncertaintyISO"]
#     print res["InstrumentType"]

#     res["PanelDates"] = GetPanelDates(path)
#     # res["TaglinePositions"] = GetTaglinePositions(path)
#     res["Depths"] = GetDepths(path)
#     res["Areas"] = GetAreas(path)
#     res["Widths"] = GetWidths(path)
#     res["AverageVelocities"] = GetAverageVelocities(path)
#     res["Discharges"] = GetDischarges(path)
#     res["DepthReadings"] = GetDepthReadings(path)
#     # res["DistanceAboveWeights"] = GetDistanceAboveWeights(path)
#     res["Counts"] = GetCounts(path)
#     res["Velocities"] = GetVelocities(path)
#     res["MeanSectionWidths"] = GetMeanSectionWidths(path)
#     res["IceCovereds"] = GetIceCovereds(path)

        
#     return res
