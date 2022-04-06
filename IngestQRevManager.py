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
    date = channel.find('Transect').find('StartDateTime').text

    #06/28/2016 08:31:36
    dt = date[6:10] + "/" + date[:5]

    return dt

#Summary
def GetStartTime(filePath):
    return GetRoot(filePath).find('Transect').find('StartDateTime').text[11:16]

def GetEndTime(filePath):
    
    return GetRoot(filePath).findall('Transect')[-1].find('EndDateTime').text[11:16]

def GetWidth(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Other').find('MeanWidth').text

def GetArea(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Other').find('MeanArea').text

def GetVelocity(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Other').find('MeanQoverA').text

def GetDischarge(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Discharge').find('Total').text

def GetUncertainty(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Uncertainty').find('Total').text

def GetMBCorrection(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Discharge').find('MovingBedPercentCorrection').text

def GetWaterTemp(filePath):
    return GetRoot(filePath).find('QA').find('TemperatureCheck').find('VerificationTemperature').text

#Detail

def GetDiagTest(filePath):
    return GetRoot(filePath).find('QA').find('DiagnosticTestResult').text

def GetADCPDepth(filePath):
    return GetRoot(filePath).find('Processing').find('Depth').find('ADCPDepth').text

def GetMagDeclination(filePath):
    return GetRoot(filePath).find('Processing').find('Navigation').find('MagneticVariation').text

def GetSerialNum(filePath):
    return GetRoot(filePath).find('Instrument').find('SerialNumber').text

def GetManufacturer(filePath):
    return GetRoot(filePath).find('Instrument').find('Manufacturer').text

def GetModel(filePath):
    return GetRoot(filePath).find('Instrument').find('Model').text

def GetFrequency(filePath):
    return GetRoot(filePath).find('Instrument').find('Frequency').text

def GetFrequencyUnit(filePath):
    return GetRoot(filePath).find('Instrument').find('Frequency').attrib['unitsCode']
    
def GetFirmware(filePath):
    return GetRoot(filePath).find('Instrument').find('FirmwareVersion').text

def GetSoftware(filePath):
    return GetRoot(filePath).find('Processing').find('SoftwareVersion').text



#Moving Boat
def GetLoop(filePath):
    MovingBedTests = GetRoot(filePath).find('QA').findall('MovingBedTest')
    for movingBedTest in MovingBedTests:
        if movingBedTest.find('UserValid').text.lower() == "yes":
            return movingBedTest.find('TestType').text
    # return GetRoot(filePath).find('QA').find('MovingBedTest').find('TestType').text

def GetDetected(filePath):
    MovingBedTests = GetRoot(filePath).find('QA').findall('MovingBedTest')
    for movingBedTest in MovingBedTests:
        if movingBedTest.find('UserValid').text.lower() == "yes":
            return movingBedTest.find('PercentMovingBed').text


def GetReference(filePath):
    return GetRoot(filePath).find('Processing').find('Navigation').find('Reference').text

def GetCompTracks(filePath):
    return GetRoot(filePath).find('Processing').find('Navigation').find('CompositeTrack').text

def GetLeftType(filePath):
    return GetRoot(filePath).find('Processing').find('Edge').find('LeftType').text

def GetLeftCoeff(filePath):
    return GetRoot(filePath).find('Processing').find('Edge').find('LeftEdgeCoefficient').text

def GetRightType(filePath):
    return GetRoot(filePath).find('Processing').find('Edge').find('RightType').text

def GetRightCoeff(filePath):
    return GetRoot(filePath).find('Processing').find('Edge').find('RightEdgeCoefficient').text

def GetDepthRef(filePath):
    return GetRoot(filePath).find('Processing').find('Depth').find('Reference').text

def GetTopMethod(filePath):
    return GetRoot(filePath).find('Processing').find('Extrapolation').find('TopMethod').text

def GetBottomMethod(filePath):
    return GetRoot(filePath).find('Processing').find('Extrapolation').find('BottomMethod').text

def GetExponent(filePath):
    return GetRoot(filePath).find('Processing').find('Extrapolation').find('Exponent').text

def GetSDM(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Uncertainty').find('COV').text

def GetExtraUncer(filePath):
    return GetRoot(filePath).find('ChannelSummary').find('Uncertainty').find('Extrapolation').text



def GetAllTransects(filePath):
    results = []
    for i, row in enumerate(GetRoot(filePath).findall('Transect')):
        line = []
        tempName = row.find('Filename').text
        if len(tempName) >= 22:
            fileName = row.find('Filename').text[17:]
        else:
            fileName = tempName
        startEdge = row.find('Edge').find('StartEdge').text
        startDateTime = row.find('StartDateTime').text[11:]
        # endDateTime = row.find('EndDateTime').text[11:]
        leftDistance = row.find('Edge').find('LeftDistance').text
        rightDistance = row.find('Edge').find('RightDistance').text
        total = row.find('Discharge').find('Total').text

        line.append(fileName)
        line.append(startEdge)
        line.append(startDateTime)
        line.append(leftDistance)
        line.append(rightDistance)
        line.append(total)

        results.append(line)
        
    return results


def GetStartDateTime(filePath):
    return GetRoot(filePath).find('Transect').find('StartDateTime').text[11:]

def GetEndDateTime(filePath):
    return GetRoot(filePath).findall('Transect')[-1].find('EndDateTime').text[11:]

def GetMessage(filePath):
    MovingBedTests = GetRoot(filePath).find('QA').findall('MovingBedTest')
    for movingBedTest in MovingBedTests:
        if movingBedTest.find('UserValid').text.lower() == "yes":
            return movingBedTest.find('Message').text
    # return GetRoot(filePath).find('QA').find('MovingBedTest').find('Message').text

def GetQRevMessage(filePath):
    return GetRoot(filePath).find('QA').find('QRev_Message').text

def GetUserComment(filePath):
    return GetRoot(filePath).find('UserComment').text




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


def AddMovingBoat(filePath, movingBoatManager, evt):
    # movingBoatManager.Clear()

    loop = GetLoop(filePath)
    detected = GetDetected(filePath)
    reference = GetReference(filePath)
    compTracks = GetCompTracks(filePath)
    # leftType = GetLeftType(filePath)
    leftCoeff = GetLeftCoeff(filePath)
    # rightType = GetRightType(filePath)
    rightCoeff = GetRightCoeff(filePath)



    if float(leftCoeff) == 0.3535 or float(leftCoeff) == 0.353:
        leftType = movingBoatManager.gui.bankList[1]
    elif float(leftCoeff) == 0.91:
        leftType = movingBoatManager.gui.bankList[2]
    else:
        leftType = movingBoatManager.gui.bankList[3]

    if float(rightCoeff) == 0.3535 or float(rightCoeff) == 0.353:
        rightType = movingBoatManager.gui.bankList[1]
    elif float(rightCoeff) == 0.91:
        rightType = movingBoatManager.gui.bankList[2]
    else:
        rightType = movingBoatManager.gui.bankList[3]


    depthRef = GetDepthRef(filePath)

    if depthRef == "BT":
        depthRef = "Bottom Track"
    elif depthRef == "":
        depthRef = ""
    else:
        depthRef = ""

    topMethod = GetTopMethod(filePath)
    bottomMethod = GetBottomMethod(filePath)
    exponent = GetExponent(filePath)
    sdm = GetSDM(filePath)
    extrap = GetExtraUncer(filePath)
    # print "extrap {0}".format(extrap)

    allTransects = GetAllTransects(filePath)

    # for i in allTransects:
    #     print i



    color = movingBoatManager.manager.gui.importedBGColor

    # color = (210, 210, 210)


    for row, tran in enumerate(allTransects):
        if row > len(movingBoatManager.tableSizer.GetChildren()) - 3:
            movingBoatManager.gui.AddEntry()



        movingBoatManager.SetFontColor(row, 0, 'Black')


        movingBoatManager.SetTableValue(row, 1, "True")

        movingBoatManager.SetTableValue(row, 2, tran[0])
        movingBoatManager.SetTableColor(row, 2, color)

        movingBoatManager.SetTableValue(row, 3, tran[1][0])
        movingBoatManager.SetTableColor(row, 3, color)

        movingBoatManager.SetTableValue(row, 4, tran[2])

        if tran[1][0] == "L":
            movingBoatManager.SetTableValue(row, 6, tran[3])
            movingBoatManager.SetTableColor(row, 6, color)

            movingBoatManager.SetTableValue(row, 7, tran[4])
            movingBoatManager.SetTableColor(row, 7, color)
        else:
            movingBoatManager.SetTableValue(row, 6, tran[4])
            movingBoatManager.SetTableColor(row, 6, color)

            movingBoatManager.SetTableValue(row, 7, tran[3])
            movingBoatManager.SetTableColor(row, 7, color)

        movingBoatManager.SetTableValue(row, 8, tran[5])
        movingBoatManager.SetTableColor(row, 8, color)

        # movingBoatManager.SetTableValue(row, 8, tran[6])
        # movingBoatManager.SetTableColor(row, 8, color)









    startDateTime = GetStartDateTime(filePath)
    endDateTime = GetEndDateTime(filePath)


    
    try:
        message = GetMessage(filePath)
    except:
        message = ""
    try:
        qRevMessage = GetQRevMessage(filePath)
    except:
        qRevMessage = ""
    try:
        userComment = GetUserComment(filePath)
    except:
        userComment = ""


    movingBoatManager.mbCmbo = loop if loop is not None else movingBoatManager.mbCmbo
    if loop != "" or loop is not None:
        movingBoatManager.mbCB = True
    else:
        movingBoatManager.mbCB = False
    if detected is not None:
        movingBoatManager.detectedCtrl = detected
        movingBoatManager.GetDetectedCtrl().SetBackgroundColour(color)

    if reference is not None:
        movingBoatManager.trackRefCmbo = reference
        movingBoatManager.GetTrackRefCmbo().SetBackgroundColour(color)

    if compTracks is not None:
        movingBoatManager.compositeTrackCmbo = compTracks
        movingBoatManager.GetCompositeTrackCmbo().SetBackgroundColour(color)
    if leftType is not None:
        movingBoatManager.leftBankCmbo = leftType

    if rightType is not None:
        movingBoatManager.rightBankCmbo = rightType


    if leftType == movingBoatManager.gui.bankList[3]:
        movingBoatManager.leftBankOtherCtrl = leftCoeff
        movingBoatManager.GetLeftBankOtherCtrl().SetBackgroundColour(color)
    else:
        movingBoatManager.leftBankOtherCtrl = ""

    if rightType == movingBoatManager.gui.bankList[3]:
        movingBoatManager.rightBankOtherCtrl = rightCoeff
        movingBoatManager.GetRightBankCmbo().SetBackgroundColour(color)
    else:
        movingBoatManager.rightBankOtherCtrl = ""

    if depthRef is not None:
        movingBoatManager.depthRefCmbo = depthRef
        movingBoatManager.GetDepthRefCmbo().SetBackgroundColour(color)
    if topMethod is not None:
        movingBoatManager.velocityTopCombo = topMethod
        movingBoatManager.GetVelocityTopCombo().SetBackgroundColour(color)
    if bottomMethod is not None:
        movingBoatManager.velocityBottomCombo = bottomMethod
        movingBoatManager.GetVelocityBottomCombo().SetBackgroundColour(color)
    if exponent is not None:
        movingBoatManager.velocityExponentCtrl = exponent
        movingBoatManager.GetVelocityExponentCtrl().SetBackgroundColour(color)
    if sdm is not None:
        movingBoatManager.standDevMeanDischCtrl = sdm
        movingBoatManager.GetStandDevMeanDischCtrl().SetBackgroundColour(color)
    if extrap is not None:
        movingBoatManager.extrapUncerCtrl = extrap
        movingBoatManager.GetExtrapUncerCtrl().SetBackgroundColour(color)





    movingBoatManager.mmntStartTimeCtrl = startDateTime
    movingBoatManager.mmntEndTimeCtrl = endDateTime

    start = movingBoatManager.gui.mmntStartTimeCtrl
    end = movingBoatManager.gui.mmntEndTimeCtrl
    meanTime = mean(start, end)
    # print meanTime

    movingBoatManager.mmntMeanTimeCtrl = meanTime

    movingBoatManager.gui.UpdateSammury(evt)


    attrib = wx.TextAttr("black", colBack=color)


    # print movingBoatManager.GetCommentsCtrl().GetRange(0,2)
    # print movingBoatManager.GetCommentsCtrl().GetValue()

    if movingBoatManager.commentsCtrl != "":
        print("not empty comments")
        movingBoatManager.commentsCtrl += "\n"
    movingBoatManager.commentsCtrl += 'Moving Bed Test Message: ' +  message + '\n\n' if message is not None else ""
    movingBoatManager.commentsCtrl += 'QRev Message: ' +  qRevMessage + '\n\n' if qRevMessage is not None else ''
    movingBoatManager.commentsCtrl += 'User Comment: ' + userComment + '\n\n' if userComment is not None else ''



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
    mbCorrection = GetMBCorrection(filePath)


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
        dischargeUncertainty = '@ Uncertainty: NA, 2-sigma value (1 x Uncertainty Value reported in *.xml File). @'
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

    if mbCorrection is not None:
        disMeasManager.manager.movingBoatMeasurementsManager.mbCorrAppCtrl = mbCorrection
        myEvent = wx.FocusEvent(eventType=wx.wxEVT_KILL_FOCUS, id=wx.NewId())
        myEvent.SetEventObject(disMeasManager.manager.movingBoatMeasurementsManager.GetMbCorrAppCtrl())
        wx.PostEvent(disMeasManager.manager.movingBoatMeasurementsManager.GetMbCorrAppCtrl(), myEvent)
        disMeasManager.manager.movingBoatMeasurementsManager.gui.mbCorrAppCtrl.SetBackgroundColour(color)
        



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
        instrDepManager.frequencyCmbo = frequency
        instrDepManager.GetFrequencyCmbo().SetBackgroundColour(color)
    if firmware is not None:
        instrDepManager.firmwareCmbo = firmware
        instrDepManager.GetFirmwareCmbo().SetBackgroundColour(color)
    if software is not None:
        instrDepManager.softwareCtrl = software
        instrDepManager.GetSoftwareCtrl().SetBackgroundColour(color)