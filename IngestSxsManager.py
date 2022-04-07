from xml.etree import ElementTree
import wx
def GetRoot(filePath):
    return ElementTree.parse(filePath).getroot()



def GetStationID(filePath):
    try:
        channel = GetRoot(filePath)
        stationID = channel.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Station_No').text
        return stationID
    except:
        print("Unable to read the xml file")
        return -1




def GetDate(filePath):
    channel = GetRoot(filePath)
    date = channel.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Date').text
    if '/' in date:
        if len(date) == 10:
            year = date[6:]
            month = date[3:5]
            day = date[:2]
            return year + "/" + month + "/" + day
        elif len(date) == 9:
            if date[1] == "/":
                year = date[5:]
                month = date[2:4]
                day = str(0)+date[:1]
                return year + "/" + month + "/" + day

            else:
                year = date[5:]
                month = str(0)+date[3:4]
                day = date[:2]
                return year + "/" + month + "/" + day
        elif len(date) == 8:
            year = date[4:]
            month = str(0)+date[2:3]
            day = str(0)+date[:1]
            return year + "/" + month + "/" + day
        else:
            year ='0000'
            month = '00'
            day = '00'
            return year + "/" + month + "/" + day

    if '-' in date:
        if len(date) == 10:
            year = date[:4]
            month = date[5:7]
            day = date[8:]
            return year + "/" + month + "/" + day
        elif len(date) == 9:
            if date[8] == "-":
                year = date[:4]
                month = date[5:7]
                day = str(0) + date[8:]
                return year + "/" + month + "/" + day

            else:
                year = date[:4]
                month = str(0) + date[5:6]
                day = date[8:]
                return year + "/" + month + "/" + day
        elif len(date) == 8:
            year = date[:4]
            month = str(0) + date[5:6]
            day = str(0) + date[8:]
            return year + "/" + month + "/" + day
        else:
            year = '0000'
            month = '00'
            day = '00'
            return year + "/" + month + "/" + day





#Calculate the mean time
def mean(start, end):
    startHour = int(start.GetHourVal())
    endHour = int(end.GetHourVal())
    startMin = int(start.GetMinuteVal())
    endMin = int(end.GetMinuteVal())
    startSec = int(start.GetSecondVal())
    endSec = int(end.GetSecondVal())
    if (startHour + endHour)%2 != 0:
        endMin += 60
    if (startMin + endMin)%2 != 0:
        endSec += 60
    meanHour = (startHour + endHour) / 2
    meanMin = (startMin + endMin) / 2
    meanSec = (startSec + endSec) / 2

    meanHour = str(meanHour) if meanHour > 9 else ("0" + str(meanHour))
    meanMin = str(meanMin) if meanMin > 9 else ("0" + str(meanMin))
    meanSec = str(meanSec) if meanSec > 9 else ("0" + str(meanSec))

    meanTime = meanHour + ':' + meanMin + ':' + meanSec

    return meanTime

#Convert 12 Hour format to 24 Hour
def PmTo24H(time):
    # print time
    time = "0" + time if len(time) < 11 else time
    t = time.split()[0]
    sign = time.split()[1]
    if sign.upper() == "PM" and int(t[:2]) < 12:
        return str(int(t[:2]) + 12) + t[2:]
    else:
        return t




def AddDischargeSummary(filePath, disMeasManager):
    root = ElementTree.parse(filePath).getroot()

    areaTotal = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Total_Area').text
    averageVel = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Mean_Avg_V').text
    qtotal = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Total_Q').text
    widthTotal = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Total_Width').text
    uncertainty = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Quality_Control').text




    # qtotal = 0
    # widthTotal = 0
    # areaTotal = 0
    # totalVel = 0
    # counter = 0

    # for i in root.find('Summary').findall('Station'):
    #     qtotal += float(i.find('Stn_Q').text)
    #     widthTotal += float(i.find('Width').text)
    #     areaTotal += float(i.find('Area').text)

    #     print "i.find('Area').text", i.find('Area').text

    #     totalVel += float(i.find('Avg_V').text)
    #     counter += 1

    # averageVel = qtotal / areaTotal
    # print "--------------"
    # print "counter", counter
    # print "qtotal", qtotal
    # print "widthTotal", widthTotal
    # print "areaTotal", areaTotal
    # print "averageVel", averageVel
    # print "totalVel", totalVel
    # print "totalVel / (counter - 2)", totalVel / (counter - 2)
    # print "qtotal / areaTotal", qtotal / areaTotal


    times = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Start_End_Time').text.split("/")
    water = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Water_Temp').text
    air = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Air_Temp').text
    if 'M' in times[0]:
        start = PmTo24H(times[0])
    else:
        start = times[0]
    if 'M' in times[1]:
        end = PmTo24H(times[1])
    else:
        end = times[1]
    color = disMeasManager.manager.gui.importedBGColor
    disMeasManager.startTimeCtrl = start
    disMeasManager.endTimeCtrl = end

    if widthTotal is not None and widthTotal != "":

        disMeasManager.widthCtrl = str(widthTotal)


        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetDischCtrl())
        wx.PostEvent(disMeasManager.GetDischCtrl(), myEvent)



        disMeasManager.GetWidthCtrl().SetBackgroundColour(color)
    if areaTotal is not None and areaTotal != "":
        disMeasManager.areaCtrl = str(areaTotal)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetAreaCtrl())
        wx.PostEvent(disMeasManager.GetAreaCtrl(), myEvent)
        disMeasManager.GetAreaCtrl().SetBackgroundColour(color)
    if averageVel is not None and averageVel != "":
        disMeasManager.meanVelCtrl = str(averageVel)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetMeanVelCtrl())
        wx.PostEvent(disMeasManager.GetMeanVelCtrl(), myEvent)
        disMeasManager.GetMeanVelCtrl().SetBackgroundColour(color)
    if qtotal is not None and qtotal != "":
        disMeasManager.dischCtrl = str(qtotal)
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetDischCtrl())
        wx.PostEvent(disMeasManager.GetDischCtrl(), myEvent)
        disMeasManager.GetDischCtrl().SetBackgroundColour(color)
    # if water is not None and water != " " and water != "":
    #     disMeasManager.waterTempCtrl = water
    #     myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
    #     myEvent.SetEventObject(disMeasManager.GetWaterTempCtrl())
    #     wx.PostEvent(disMeasManager.GetWaterTempCtrl(), myEvent)
    #     disMeasManager.GetWaterTempCtrl().SetBackgroundColour(color)
    if air is not None and air != " " and air != "":
        disMeasManager.airTempCtrl = air
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetAirTempCtrl())
        wx.PostEvent(disMeasManager.GetAirTempCtrl(), myEvent)
        disMeasManager.GetAirTempCtrl().SetBackgroundColour(color)

    if uncertainty is not None and uncertainty != "":
        disMeasManager.uncertaintyCtrl = str(round(float(uncertainty), 2))
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetUncertaintyCtrl())
        wx.PostEvent(disMeasManager.GetUncertaintyCtrl(), myEvent)
        disMeasManager.GetUncertaintyCtrl().SetBackgroundColour(color)

        # Adding uncertainty text to Discharge Activity Remarks
        dischargeUncertainty = '@ Uncertainty: ISO method, 2-sigma value (1 x Uncertainty Value reported in *.xml File). @'
        dischargeRemarks = disMeasManager.dischRemarksCtrl
        if dischargeRemarks != '':
            disMeasManager.dischRemarksCtrl = dischargeRemarks + '\n' + dischargeUncertainty
        else:
            disMeasManager.dischRemarksCtrl = dischargeUncertainty
        


def AddDischargeDetail(filePath, instrDepManager, disManager):
    root = ElementTree.parse(filePath).getroot()
    instrument = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Instrument').text
    firmware = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Firmware_Version').text
    serialNum = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('ADCP_Serial_No').text
    software = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Software_Version').text
    frequency = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('System_Frequency').text
    comments = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Comments').text
    numberOfPanels = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('No_Stations').text
    adcpDepth = root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('ADCP_Depth').text

    # Remove * character from the number of panels
    #if '*' in numberOfPanels:
    #    Find index and remove by slicing the string
    #    char_index = numberOfPanels.find('*')
    #    numberOfPanels = numberOfPanels[0:char_index:] + numberOfPanels[char_index+1::]

    # print comments is None

    # counter = 0
    # for i in root.find('Summary').findall('Station'):
    #     counter += 1
    color = instrDepManager.manager.gui.importedBGColor

    instrDepManager.deploymentCmbo = ""
    instrDepManager.GetDeploymentCmbo().SetBackgroundColour(color)
    instrDepManager.instrumentCmbo = "ADCP"
    instrDepManager.GetInstrumentCmbo().SetBackgroundColour(color)
    instrDepManager.manufactureCmbo = "TRDI"
    instrDepManager.GetManufactureCmbo().SetBackgroundColour(color)

    if instrument is not None and instrument != "":
        instrDepManager.modelCmbo = instrument.split(" ")[0]
        instrDepManager.GetModelCmbo().SetBackgroundColour(color)

    if serialNum is not None and serialNum != "":
        instrDepManager.serialCmbo = serialNum
        instrDepManager.GetSerialCmbo().SetBackgroundColour(color)
    # if counter is not None:
    #     instrDepManager.numOfPanelsScroll = str(counter)

    if numberOfPanels is not None and numberOfPanels != "":
        # Two panels are subtracted as the edges do not need to be considered
        instrDepManager.numOfPanelsScroll = str(int(numberOfPanels)-2)
        instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(color)
    if frequency is not None and frequency != "":
        instrDepManager.frequencyCmbo = frequency
        instrDepManager.GetFrequencyCmbo().SetBackgroundColour(color)
    if firmware is not None and firmware != "":
        instrDepManager.firmwareCmbo = firmware
        instrDepManager.GetFirmwareCmbo().SetBackgroundColour(color)
    if software is not None and software != "":
        instrDepManager.softwareCtrl = software
        instrDepManager.GetSoftwareCtrl().SetBackgroundColour(color)
    if comments is not None and comments != "":
        disManager.dischRemarksCtrl += '\nSxS measurement notes: ' +  comments if disManager.dischRemarksCtrl != "" else 'SxS measurement notes: ' +  comments
        # instrDepManager.GetDischTxt().SetBackgroundColour(color)
        # instrDepManager.GetDischTxt().SetForegroundColour("blue")

        
        
    try:
        float(adcpDepth)
        if adcpDepth is not None and adcpDepth != "":
            # print adcpDepth
            # print len(adcpDepth)
            instrDepManager.adcpDepthCtrl = adcpDepth
            instrDepManager.GetAdcpDepthCtrl().SetBackgroundColour(color)
    except:
        pass


# root = ElementTree.parse("C:\\eHSN\\eHSN_Version_1_2_4_ReleasedVersion_Ingest\\SxsMmt\\09CD001_20160120_Good mmnt\\09CD001_20160120.sxs.xml").getroot()
# qtotal = 0
# widthTotal = 0
# areaTotal = 0
# averageVel = 0
# counter = 0
# for i in root.find('Summary').findall('Station'):
#     # print i.find('Stn_Q').text
#     # print i.find('Width').text
#     # print i.find('Area').text
#     # print i.find('Avg_V').text
#     qtotal += float(i.find('Stn_Q').text)
#     widthTotal += float(i.find('Width').text)
#     areaTotal += float(i.find('Area').text)
#     averageVel += float(i.find('Avg_V').text)
#     counter += 1
# print "--------------"
# print counter
# print qtotal
# print widthTotal
# print areaTotal
# print averageVel / (counter - 2)
# print qtotal / areaTotal


# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Start_End_Time').text
# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Instrument').text
# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Firmware_Version').text
# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('ADCP_Serial_No').text
# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Software_Version').text
# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('System_Frequency').text
# print root.find('Summary').find('WinRiver_II_Section_by_Section_Summary').find('Comments').text