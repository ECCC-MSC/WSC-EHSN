# import wx
from datetime import datetime, timedelta
from xml.etree.ElementTree import SubElement
import wx
def GetRawDataSet(path):
    dataSet = []
    file = open(path)
    rawData = file.readlines()
    result = []

    for i, line in enumerate(rawData):
        if line == "\n" or line is None or len(line) == 0:
            del rawData[i]

    rawData = [x for x in rawData if x != []]

    for i in rawData:
        if i is not None or i != "": 
            dataSet.append(i.split())


    for index, i in enumerate(dataSet):
        if len(i) == 0:
            del dataSet[index]
        for j in i:
            if j == ":":
                del i[i.index(j)]


    # for i in result:
    #     print i
    

    file.close()

    return dataSet


def GetStationID(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        # print i[0]
        if i[0] == "STN.NUM":
            
            if len(i) < 2:
                return -1
            
            return i[1]

    return -1



def GetDate(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "RECORDED:":
            if len(i) < 2:
                return -1
            
            return i[1].replace("-", "/")

    return -1

def AddDischargeSummary(path, disMeasManager, instrDepManager):
    color = disMeasManager.manager.gui.importedBGColor
    startTime = ""
    endTime = ""

    width = ""
    depth = ""
    area = ""
    meanVelocity = ""
    discharge = ""



    comments = ""



    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "START":
            startTime = i[2]

        elif i[0] == "END":
            endTime = i[2]

        elif i[0] == "WIDTH" and dataSet[index - 1][0] == "IP":
            width = i[1]

        elif i[0] == "Avg":
            depth = i[2]

        elif i[0] == "AREA" and dataSet[index - 1][0] == "Avg":
            area = i[1]

        elif i[0] == "AvgVELOCITY:":
            meanVelocity = i[1]

        elif i[0] == "DISCHARGE" and dataSet[index - 1][0] == "AvgVELOCITY:":
            
            discharge = i[1]

        

        elif i[0] == "-------COMMENTS-------":

            comments += "HFC Comments:\n"
            for line in dataSet[index+1:]:
                comments += ' '.join(str(x) for x in line) 


    if startTime is not None and startTime != "":
        disMeasManager.startTimeCtrl = startTime
    if endTime is not None and endTime != "":
        disMeasManager.endTimeCtrl = endTime
    # if depth is not None and depth != "":
    #     disMeasManager.waterTempCtrl = depth
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


    if comments is not None and comments != "":
        disMeasManager.dischRemarksCtrl += "\n" if disMeasManager.dischRemarksCtrl != "" else ""
        disMeasManager.dischRemarksCtrl += comments








def GetDeploymentMethod(path):
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "MMT.PROC" in i[0]:
            if len(i) > 1:
                return i[1]



def GetMeasurementSectionCondition(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "MMT.TYPE" in i[0]:
            if len(i) > 1 and "OPEN" in i[2]:
                return "Open"
            else:
                return "Ice"

def GetCondition(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "MMT.TYPE" in i[0]:
            return " ".join(i[1:])



def GetTotalDischarge(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "DISCHARGE" and dataSet[index - 1][0] == "AvgVELOCITY:" and len(dataSet[index - 1]) > 1:         
            return i[1]
    else:
        return ""

def GetTotalArea(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "AREA" and dataSet[index - 1][0] == "Avg" and len(dataSet[index - 1]) > 1:       
            return i[1]
    else:
        return ""

def GetTotalWidth(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "WIDTH" and dataSet[index - 1][0] == "IP" and len(dataSet[index - 1]) > 1:
            return i[1]
    else:
        return ""


def GetMeanVelocity(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "AvgVELOCITY:" and len(i) > 1:           
            return i[1]
    else:
        return ""

def GetMeanDepth(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "Avg" and len(i) > 2:            
            return i[2]
    else:
        return ""


def GetStartTime(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "START" and i[1] == "TIME" and len(i) > 2:           
            return i[2]
    else:
        return ""



def GetSerialNumber(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "METERS" in i[0]:
            if dataSet[index+1][0] == "METER" and dataSet[index+1][1] == "USED" and len(dataSet[index+1]) > 2:           
                return dataSet[index+1][2]
    else:
        return ""

def GetMeasuredBy(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "PRS.NAME" in i[0] and len(i) > 1:           
            return i[1]
    else:
        return ""


def GetCalculationMethod(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "AffraCal" in i[0] and i[1] == "N":            
            return "No-Recalculation"
    else:
        return ""


def GetWaterTemperature(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "WATER" and i[1] == "TEMP" and len(i) > 2:            
                return i[2]
    else:
        return ""


def GetAirTemperature(path):
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if i[0] == "AIR" and i[1] == "TEMP" and len(i) > 2:            
            return i[2]
    else:
        return ""



def GetInitialPoint(path):
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "IP" in i[0] and "to" in i[1] and "SHORE" in i[2] and len(i) > 3:
            return i[3]
    else:
        return ""


def GetStartingPoint(path):
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if len(i) > 2:
            if "RIV.BANK" in i[0] and i[1] == "R":
                return "Right"
            elif "RIV.BANK" in i[0] and i[1] == "L":
                return "Left"
    else:
        return ""


def GetImportFileSoftwareName(path):
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "-S/W" in i[0]:
            if "VER" in i[1]:
                return " ".join(i[2:])
            else:
                return " ".join(i[1:])
    else:
        return ""







def GetPanelDates(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "MMT." in i[0] and "TIME" in i[1]:
            if len(i) > 1:
                res.append(i[2])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res

def GetTaglinePositions(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "TAGMARK" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res


def GetDistanceToShores(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "DISTtoSHORE" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res


def GetDepthReadings(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "DEPTH" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res

def GetWidths(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "WIDTH" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res


def GetAreas(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "AREA" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res


def GetAverageVelocities(path):



    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "VELOCITY" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res

def GetDischarges(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "DISCHARGE" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res



def GetMeterNames(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "METER" in i[0] and "USED" in i[1]:
            if len(i) > 1:
                res.append(i[2])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res


def GetAmountOfWeights(path):   
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "AMTofWT" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res

def GetDistanceAboveWeights(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "DisMtABW" in i[0]:
            if len(i) > 1:
                res.append(i[1])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res



def GetVelocityMethods(path):
    res = []
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "%D" in i[0]:
            measurments = []
            if len(i) > 1:
                measurments.append(dataSet[index+1][0])
                
                if index < len(dataSet) - 1 and len(dataSet[index+2]) > 0 and "DISTtoSHORE" not in dataSet[index+2][0]:
                    measurments.append(dataSet[index+2][0])
                    if index < len(dataSet) - 2 and len(dataSet[index+3]) > 0 and "DISTtoSHORE" not in dataSet[index+3][0]:
                        measurments.append(dataSet[index+3][0])
                # print dataSet[index+2]
                res.append(measurments)

    # print res
    # print len(res)
    return res


def GetDepths(path):
    res = []
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "%D" in i[0]:
            measurments = []
            if len(i) > 1:
                measurments.append(dataSet[index+1][1])
                
                if index < len(dataSet) - 1 and len(dataSet[index+2]) > 1 and "DISTtoSHORE" not in dataSet[index+2][1]:
                    measurments.append(dataSet[index+2][1])
                    if index < len(dataSet) - 2 and len(dataSet[index+3]) > 1 and "DISTtoSHORE" not in dataSet[index+3][1]:
                        measurments.append(dataSet[index+3][1])
                # print dataSet[index+2]
                res.append(measurments)



def GetVelocitys(path):
    res = []
    dataSet = GetRawDataSet(path)
    result = []

    for i in dataSet:
        print(i)

    for index, i in enumerate(dataSet):
        if "%D" in i[0]:
            measurments = []
            if len(i) > 1:
                if len(dataSet[index+1]) == 4:
                    vels = dataSet[index+1][3].split("-")
                    if len(vels) > 1:
                        measurments.append("-" + vels[1])
                    else:
                        measurments.append("")
                elif len(dataSet[index+1]) > 4:
                    measurments.append(dataSet[index+1][4])
                else:
                    measurments.append("")

                if index < len(dataSet) - 1 and len(dataSet[index+2]) > 0 and "DISTtoSHORE" not in dataSet[index+2][0]:
                    if len(dataSet[index+2]) == 4:
                        vels = dataSet[index+2][3].split("-")
                        if len(vels) > 1:
                            measurments.append("-" + vels[1])
                        else:
                            measurments.append("")
                    elif len(dataSet[index+2]) > 4:
                        measurments.append(dataSet[index+2][4])
                    else:
                        measurments.append("")
                    if index < len(dataSet) - 2 and len(dataSet[index+3]) > 0 and "DISTtoSHORE" not in dataSet[index+3][0]:
                        if len(dataSet[index+3]) == 4:
                            vels = dataSet[index+3][3].split("-")
                            if len(vels) > 1:
                                measurments.append("-" + vels[1])
                            else:
                                measurments.append("")
                        elif len(dataSet[index+3]) > 4:
                            measurments.append(dataSet[index+3][4])
                        else:
                            measurments.append("")

                res.append(measurments)

    return res

def GetCounts(path, eManager):
    res = []
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "%D" in i[0]:

            if len(dataSet[index+1]) < 5:
                res.append("")

                info = wx.MessageDialog(eManager.gui, "Input string is not in a correct format. 'Count' for some panels may not imported.", "Error",
                                     wx.OK | wx.ICON_WARNING)
                info.ShowModal()
                # if int(dataSet[index+1][2][:1]) < 5:
                #     res.append(dataSet[index+1][2][:2])
                # else:
                #     res.append(dataSet[index+1][2][:1])
            else:
                res.append(dataSet[index+1][2])
    # print res
    # print len(res)
    return res

def GetIntervals(path, eManager):
    res = []
    dataSet = GetRawDataSet(path)

    for index, i in enumerate(dataSet):
        if "%D" in i[0]:

            if len(dataSet[index+1]) < 5:
                # if int(dataSet[index+1][2][:1]) < 5:
                #     res.append(dataSet[index+1][2][2:])
                # else:
                #     res.append(dataSet[index+1][2][1:])
                res.append("")
                info = wx.MessageDialog(eManager.gui, "Input string is not in a correct format. 'Interval' for some panels may not imported.", "Error",
                                     wx.OK | wx.ICON_WARNING)
                info.ShowModal()
            else:
                res.append(dataSet[index+1][3])
    # print res
    # print len(res)
    return res


def GetDistanceToNextShores(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "DisToN" in i[0] and "P/Sh" in i[1]:
            if len(i) > 1:
                res.append(i[2])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res

def GetIslandWidths(path):
    res = []
    counter = 0
    panelNum = 1
    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):
        if "--PANEL" in i[0]:# or "--SUMMARY" in i[0]:
            counter += 1
            if panelNum < counter:
                res.append("")
                panelNum += 1

        elif "P/ISL" in i[0] and "WIDTH" in i[1]:
            if len(i) > 1:
                res.append(i[2])
            else:
                res.append("")
            panelNum += 1
        elif "--SUMMARY" in i[0]:
            if panelNum == counter:
                res.append("")
            break
    # print res
    # print len(res)
    return res




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
    # print (end-start).days + float((end-start).seconds)/86400
    return str((end-start).days + float((end-start).seconds)/86400)




def AddDischargeDetail(path, instrDepManager):
    color = instrDepManager.manager.gui.importedBGColor
    serial = ""
    numOfPanels = ""
    deployment = ""

    softwareNum = GetImportFileSoftwareName(path)

    dataSet = GetRawDataSet(path)
    for index, i in enumerate(dataSet):

        if i[0] == "METER" and dataSet[index - 1][0] == "--METERS":
            serial = i[2]

        elif i[0] == "NUM.":
            numOfPanels = i[2]
        elif i[0] == "MMT.PROC:":
            deployment = i[1]


    if serial is not None and serial != "":
        instrDepManager.serialCmbo = serial
        instrDepManager.GetSerialCmbo().SetBackgroundColour(color)
    if numOfPanels is not None and numOfPanels != "":
        instrDepManager.numOfPanelsScroll = numOfPanels
        instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(color)
    if deployment is not None and deployment != "":
        instrDepManager.deploymentCmbo = deployment
        instrDepManager.GetDeploymentCmbo().SetBackgroundColour(color)

    if softwareNum != "":
        instrDepManager.softwareCtrl = softwareNum
        instrDepManager.GetSoftwareCtrl().SetBackgroundColour(color)

    instrDepManager.instrumentCmbo = "Current Meter"
    instrDepManager.GetInstrumentCmbo().SetBackgroundColour(color)
    instrDepManager.modelCmbo = "Price AA"
    instrDepManager.GetModelCmbo().SetBackgroundColour(color)

# def GetMidSectionInfo(path, eManager):
#     midSectionInfo = {}


#     #String
#     midSectionInfo["DateSpreadsheetFormat"] = GetDateSpreadsheetFormat(path, eManager)
#     midSectionInfo["DeploymentMethod"] = GetDeploymentMethod(path)
#     midSectionInfo["MeasurementSectionCondition"] = GetMeasurementSectionCondition(path)
#     midSectionInfo["TotalDischarge"] = GetTotalDischarge(path)
#     midSectionInfo["TotalArea"] = GetTotalArea(path)
#     midSectionInfo["TotalWidth"] = GetTotalWidth(path)
#     midSectionInfo["MeanVelocity"] = GetMeanVelocity(path)
#     midSectionInfo["MeanDepth"] = GetMeanDepth(path)
#     midSectionInfo["SerialNumber"] = GetSerialNumber(path)
#     midSectionInfo["MeasuredBy"] = GetMeasuredBy(path)
#     midSectionInfo["CalculationMethod"] = GetCalculationMethod(path)
#     midSectionInfo["WaterTemperature"] = GetWaterTemperature(path)
#     midSectionInfo["AirTemperature"] = GetAirTemperature(path)
#     midSectionInfo["InitialPoint"] = GetInitialPoint(path)
#     midSectionInfo["StartingPoint"] = GetStartingPoint(path)
#     midSectionInfo["Condition"] = GetCondition(path)
#     midSectionInfo["ImportFileSoftwareName"] = GetImportFileSoftwareName(path)

#     #Array Objects
#     midSectionInfo["PanelDates"] = GetPanelDates(path)
#     midSectionInfo["TaglinePositions"] = GetTaglinePositions(path)
#     midSectionInfo["DistanceToShores"] = GetDistanceToShores(path)
#     midSectionInfo["DepthReadings"] = GetDepthReadings(path)
#     midSectionInfo["Widths"] = GetWidths(path)
#     midSectionInfo["Areas"] = GetAreas(path)
#     midSectionInfo["AverageVelocities"] = GetAverageVelocities(path)
#     midSectionInfo["Discharges"] = GetDischarges(path)
#     midSectionInfo["MeterNames"] = GetMeterNames(path)
#     midSectionInfo["AmountOfWeights"] = GetAmountOfWeights(path)
#     midSectionInfo["DistanceAboveWeights"] = GetDistanceAboveWeights(path)
#     midSectionInfo["VelocityMethods"] = GetVelocityMethods(path)
#     midSectionInfo["Depths"] = GetDepths(path)
#     midSectionInfo["Velocitys"] = GetVelocitys(path)
#     midSectionInfo["Counts"] = GetCounts(path, eManager)
#     midSectionInfo["Intervals"] = GetIntervals(path, eManager)

#     #Dictionary Objects
#     midSectionInfo["DistanceToNextShores"] = GetDistanceToNextShores(path)
#     midSectionInfo["IslandWidths"] = GetIslandWidths(path)

#     print midSectionInfo["VelocityMethods"]
#     print midSectionInfo["Velocitys"]

    # return midSectionInfo
