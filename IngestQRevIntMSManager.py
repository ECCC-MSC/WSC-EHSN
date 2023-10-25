import math
from xml.etree import ElementTree
import wx


def GetRoot(filePath):
    return ElementTree.parse(filePath).getroot()

def GetStationID(filePath):
    try:
        channel = GetRoot(filePath)
        stationID = channel.find('SiteInformation').find('SiteID').text
        return stationID
    except:
        print("Unable to read the xml file")
        return -1

def GetDate(filePath):
    channel = GetRoot(filePath)
    # find first vertical that has a StartDateTime field
    date = channel.find('./VerticalDetails/Vertical/StartDateTime').text

    #06/28/2016 08:31:36
    dt = date[6:10] + "/" + date[:5]

    return dt


#Summary
def GetArea(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('ChannelArea').text

def GetVelocity(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('MeanNormalVelocity').text

def GetDischarge(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('ChannelTotalQ').text

def GetWidth(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('ChannelWidth').text

def GetUncertainty(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Uncertainty').find('Total').text

def GetStartTime(filePath):
     # find first vertical that has a StartDateTime field
    return GetRoot(filePath).find('./VerticalDetails/Vertical/StartDateTime').text[11:16]

def GetEndTime(filePath):
    # find last vertical that has a EndDateTime field
    return GetRoot(filePath).findall('./VerticalDetails/Vertical/EndDateTime')[-1].text[11:16]


#Detail

def GetFirmware(filePath):
    return GetRoot(filePath).find('Instrument').find('FirmwareVersion').text

def GetSerialNum(filePath):
    return GetRoot(filePath).find('Instrument').find('SerialNumber').text

def GetSoftware(filePath):
    return GetRoot(filePath).find('Processing').find('SoftwareVersion').text

def GetManufacturer(filePath):
    return GetRoot(filePath).find('Instrument').find('Manufacturer').text

def GetModel(filePath):
    return GetRoot(filePath).find('Instrument').find('Model').text

def GetFrequency(filePath):
    return GetRoot(filePath).find('Instrument').find('Frequency').text

def GetFrequencyUnit(filePath):
    return GetRoot(filePath).find('Instrument').find('Frequency').attrib['unitsCode']

def GetADCPDepth(filePath):
    return GetRoot(filePath).find('VerticalDetails/Vertical/Processing/Depth/ADCPDepth').text

def GetDiagTest(filePath):
    return GetRoot(filePath).find('QA').find('DiagnosticTestResult').text

def GetMagDeclination(filePath):
    return GetRoot(filePath).find('VerticalDetails/Vertical/Processing/Navigation/MagneticVariation').text


#Calculate the mean time
def mean(start, end):
    startHour = int(start.GetHourVal())
    endHour = int(end.GetHourVal())
    startMin = int(start.GetMinuteVal())
    endMin = int(end.GetMinuteVal())
    startSec = int(start.GetSecondVal())
    endSec = int(end.GetSecondVal())


    start = float(startHour * 3600 + startMin * 60 + startSec)
    end = float(endHour * 3600 + endMin * 60 + endSec)

    mean = round((start + end) / 2)

    meanHour = int(mean / 3600)
    meanMin = int(mean % 3600 / 60)
    meanSec = int(mean % 3600 % 60)


    # if (startHour + endHour)%2 != 0:
    #     endMin += 60
    # if (startMin + endMin)%2 != 0:
    #     endSec += 60
    # meanHour = (startHour + endHour) / 2
    # meanMin = (startMin + endMin) / 2
    # meanSec = (startSec + endSec) / 2

    meanHour = str(meanHour) if meanHour > 9 else ("0" + str(meanHour))
    meanMin = str(meanMin) if meanMin > 9 else ("0" + str(meanMin))
    meanSec = str(meanSec) if meanSec > 9 else ("0" + str(meanSec))

    meanTime = meanHour + ':' + meanMin + ':' + meanSec

    return meanTime



def AddDischargeSummary(filePath, disMeasManager):
    color = disMeasManager.manager.gui.importedBGColor

    start = GetStartTime(filePath)
    end = GetEndTime(filePath)
    width = GetWidth(filePath)
    area = GetArea(filePath)
    vel = GetVelocity(filePath)
    dis = GetDischarge(filePath)

    uncert = str(round(float(GetUncertainty(filePath)), 2))
    # water = GetWaterTemp(filePath)


    disMeasManager.startTimeCtrl = start

    disMeasManager.endTimeCtrl = end

    if width is not None:
        disMeasManager.widthCtrl = width
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetWidthCtrl())
        wx.PostEvent(disMeasManager.GetWidthCtrl(), myEvent)
        disMeasManager.GetWidthCtrl().SetBackgroundColour(color)
    if area is not None:
        disMeasManager.areaCtrl = area
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetAreaCtrl())
        wx.PostEvent(disMeasManager.GetAreaCtrl(), myEvent)
        disMeasManager.GetAreaCtrl().SetBackgroundColour(color)
    if vel is not None:
        disMeasManager.meanVelCtrl = vel
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetMeanVelCtrl())
        wx.PostEvent(disMeasManager.GetMeanVelCtrl(), myEvent)
        disMeasManager.GetMeanVelCtrl().SetBackgroundColour(color)
    if dis is not None:
        disMeasManager.dischCtrl = dis
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetDischCtrl())
        wx.PostEvent(disMeasManager.GetDischCtrl(), myEvent)
        disMeasManager.GetDischCtrl().SetBackgroundColour(color)

        disMeasManager.manager.movingBoatMeasurementsManager.finalDischCtrl = dis
        disMeasManager.manager.movingBoatMeasurementsManager.gui.finalDischCtrl.SetBackgroundColour(color)

        
    if uncert is not None:
        disMeasManager.uncertaintyCtrl = uncert
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.GetUncertaintyCtrl())
        wx.PostEvent(disMeasManager.GetUncertaintyCtrl(), myEvent)
        disMeasManager.GetUncertaintyCtrl().SetBackgroundColour(color)
    
        # Adding uncertainty text to Discharge Activity Remarks
        dischargeUncertainty = '@ Uncertainty: QRev Uncertainty Analysis (DS Mueller, 2016), 2-sigma value (1 x Uncertainty Value reported in *.xml File). @'
        dischargeRemarks = disMeasManager.dischRemarksCtrl
        if dischargeRemarks != '':
            disMeasManager.dischRemarksCtrl = dischargeRemarks + '\n' + dischargeUncertainty
        else:
            disMeasManager.dischRemarksCtrl = dischargeUncertainty

    # if water is not None:
    #     disMeasManager.waterTempCtrl = water
    #     myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
    #     myEvent.SetEventObject(disMeasManager.GetWaterTempCtrl())
    #     wx.PostEvent(disMeasManager.GetWaterTempCtrl(), myEvent)
    #     disMeasManager.GetWaterTempCtrl().SetBackgroundColour(color)

    disMeasManager.gui.Refresh()
    # disMeasManager.GetStartTimeCtrl().SetBackgroundColour(color)

def AddDischargeDetail(filePath, instrDepManager):
    color = instrDepManager.manager.gui.importedBGColor
    diagTest = GetDiagTest(filePath)
    depth = GetADCPDepth(filePath)
    magDeclination = GetMagDeclination(filePath)

    serialNum = GetSerialNum(filePath)
    manufacturer = GetManufacturer(filePath)
    model = GetModel(filePath)
    frequency = GetFrequency(filePath)
    freUnit = GetFrequencyUnit(filePath)
    firmware = GetFirmware(filePath)
    software = GetSoftware(filePath)

    if diagTest is not None:
        if diagTest.lower() == "pass":
            instrDepManager.GetDiagTestCB().SetValue(True)        
        else:
            instrDepManager.GetDiagTestCB().SetValue(False)
        instrDepManager.GetDiagTestCB().SetBackgroundColour(color)

            
    if depth is not None:
        instrDepManager.adcpDepthCtrl = depth
        instrDepManager.GetAdcpDepthCtrl().SetBackgroundColour(color)
    if magDeclination is not None:
        instrDepManager.magnDeclCtrl = magDeclination
        instrDepManager.GetMagnDeclCtrl().SetBackgroundColour(color)
    if serialNum is not None:
        instrDepManager.serialCmbo = serialNum
        instrDepManager.GetSerialCmbo().SetBackgroundColour(color)
    if manufacturer is not None:
        instrDepManager.manufactureCmbo = manufacturer
        instrDepManager.GetManufactureCmbo().SetBackgroundColour(color)
    if model is not None:
        instrDepManager.modelCmbo = model
        instrDepManager.GetModelCmbo().SetBackgroundColour(color)
    if frequency is not None:
        if freUnit is not None:
            if "m" in freUnit.lower():
                # frequency = str(float(frequency) * 1000)
                frequency += "000"
        instrDepManager.frequencyCmbo = str(math.trunc(float(frequency)))
        instrDepManager.GetFrequencyCmbo().SetBackgroundColour(color)
    if firmware is not None:
        instrDepManager.firmwareCmbo = firmware
        instrDepManager.GetFirmwareCmbo().SetBackgroundColour(color)
    if software is not None:
        instrDepManager.softwareCtrl = software
        instrDepManager.GetSoftwareCtrl().SetBackgroundColour(color)