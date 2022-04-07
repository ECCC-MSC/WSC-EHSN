from NumberControl import *

#Get Station ID
def GetStationID(path):
    dataSet = []
    file = open(path)
    lines = file.readlines()

    for i, line in enumerate(lines):
        if line == "\n" or line is None or len(line) == 0:
            del lines[i]


    for i in lines:
        dataSet.append(i.split("; "))

    for data in dataSet:
        if data[0] == "Station Number":

            return data[1].rstrip()


    print("Unable to read the dis file")
    return -1


#Get field visit date
def GetDate(path):
    dataSet = []
    file = open(path)
    lines = file.readlines()

    for i, line in enumerate(lines):
        if line == "\n" or line is None or len(line) == 0:
            del lines[i]


    for i in lines:
        dataSet.append(i.split(":"))

    for data in dataSet:

        if data[0] == "Date Measured":
            date =  data[1]
            if date.count(",") == 2: #when the name of day, month and year are all provided (Ex: Saturday, February 25, 2019)
                month = date.split(", ")[1].split()[0]
                day = date.split(", ")[1].split()[1]
                year = date.split(", ")[2].rstrip()
            elif date.count(",") == 1: #when the name of the day is not included in date  (Ex: February 25, 2019)
                month = date.split(",")[0].split()[0]
                day = date.split(",")[0].split()[1]
                year = date.split(", ")[1]
            else:
                print("Date is not written in proper format in dis file")

            numMonth = {'january' : "01",
                        'february' : "02",
                        'march' : "03",
                        'april' : "04",
                        'may' : "05",
                        'june' : "06",
                        'july' : "07",
                        'august' : "08",
                        'september' : "09", 
                        'october' : "10",
                        'november' : "11",
                        'december' : "12"}

            return year + "/" + numMonth[month.lower()] + "/" + day




#Adding data to discharge panel
def AddDischargeSummary(path, disMeasManager):

    startTime = ""
    endTime = ""
    airTemp = ""
    waterTemp = ""
    width = ""
    area = ""
    meanVelocity = ""
    discharge = ""



    file = open(path)
    rawData = file.readlines()
    file.close()
    for i, line in enumerate(rawData):
        if line == "\n": #or line is None or len(line) == 0:

            del rawData[i]

    rawData = [x for x in rawData if x != []]


    finalData = []
    for i in rawData:
        finalData.append(i.split("; "))



    for index, data in enumerate(finalData):
        if len(data) > 0:


            if "Measurement Results" in data[0]:
                time = finalData[index+2][0].split()[1]
                time = "0" + time if len(time) < 8 else time
                sign = finalData[index+2][0].split()[2]
                startTime = time + " " + sign

            elif data[0] == "Comments":

                time = finalData[index-1][0].split()[1]
                time = "0" + time if len(time) < 8 else time
                sign = finalData[index-1][0].split()[2]
                endTime = time + " " + sign

    #         elif data[0] == "Mean_Temp":
    #             waterTemp = data[1]
            elif data[0] == "Total Width":
                width = data[1].rstrip()
            elif data[0] == "Total Area":
                area = data[1].rstrip()
            elif data[0] == "Mean Velocity":
                meanVelocity = data[1].rstrip()
            elif data[0] == "Total Q":
                discharge = data[1].rstrip()
            elif data[0] == "Overall":
                uncertainty = data[2].rstrip()[:-1]
                # print(uncertainty)

    color = disMeasManager.manager.gui.importedBGColor

    if startTime is not None and startTime != "":
        disMeasManager.startTimeCtrl = PmTo24H(startTime)
        # print disMeasManager.startTimeCtrl
    if endTime is not None and endTime != "":
        disMeasManager.endTimeCtrl = PmTo24H(endTime)
    # if waterTemp is not None and waterTemp != "":
    #     disMeasManager.waterTempCtrl = waterTemp
    if width is not None and width != "":
        # disMeasManager.gui.widthCtrl.SetValue(width)
        disMeasManager.widthCtrl = width
        SigByCtrl3(disMeasManager.gui.widthCtrl)
        disMeasManager.GetWidthCtrl().SetBackgroundColour(color)
    if area is not None and area != "":
        disMeasManager.areaCtrl = area
        SigByCtrl3(disMeasManager.gui.areaCtrl)
        disMeasManager.GetAreaCtrl().SetBackgroundColour(color)
    if meanVelocity is not None and meanVelocity != "":
        disMeasManager.meanVelCtrl = meanVelocity
        if float(meanVelocity) < 0.1:
            RoundByCtrl3(disMeasManager.GetMeanVelCtrl())
        else:
            SigByCtrl3(disMeasManager.GetMeanVelCtrl())
  
        disMeasManager.GetMeanVelCtrl().SetBackgroundColour(color)
    if discharge is not None and discharge != "":
        disMeasManager.dischCtrl = discharge
        if float(discharge) < 0.1:
            RoundByCtrl4(disMeasManager.GetDischCtrl())
        else:
            SigByCtrl3(disMeasManager.GetDischCtrl())
        disMeasManager.GetDischCtrl().SetBackgroundColour(color)

    if uncertainty is not None and uncertainty != "":
        disMeasManager.uncertaintyCtrl = str(round(float(uncertainty)*2, 2))
        disMeasManager.GetUncertaintyCtrl().SetBackgroundColour(color)
    
        # Adding uncertainty text to Discharge Activity Remarks
        dischargeUncertainty = '@ Uncertainty: IVE method, 2-sigma value (2 x Uncertainty Value reported in *.dis File). @'
        dischargeRemarks = disMeasManager.dischRemarksCtrl
        if dischargeRemarks != '':
            disMeasManager.dischRemarksCtrl = dischargeRemarks + '\n' + dischargeUncertainty
        else:
            disMeasManager.dischRemarksCtrl = dischargeUncertainty

    # print PmTo24H(startTime)
    # print PmTo24H(endTime)
    # # print waterTemp
    # print width, "width"
    # print area, "area"
    # print meanVelocity, "meanV"
    # print discharge, "discharge"



#Adding data to instrument panel
def AddDischargeDetail(path, instrDepManager, disManager):

    firmware = ""
    serial = ""
    model = ""
    comments = ""

    numberOfPanels = ""



    file = open(path)
    rawData = file.readlines()
    for i, line in enumerate(rawData):
        if line == "\n": # or line is None or len(line) == 0:
            del rawData[i]

    rawData = [x for x in rawData if x != []]


    finalData = []
    for i in rawData:
        finalData.append(i.split(";"))


    for index, data in enumerate(finalData):
        if len(data) > 0:
            # print data[0]
            if data[0] == "Firmware Version":
                firmware = data[1].rstrip()
            elif data[0] == "Serial Number":
                serial = data[1].rstrip()
            elif data[0] == "System Type":
                model = data[1].rstrip()
            elif "Comments" in data[0]:
                for i in finalData[index + 1:]:
                    comments += i[0]

                numberOfPanels = finalData[index-1][0].split()[0]
    color = instrDepManager.manager.gui.importedBGColor

    instrDepManager.instrumentCmbo = "ADCP"
    instrDepManager.GetInstrumentCmbo().SetBackgroundColour(color)

    instrDepManager.deploymentCmbo = "Wading"
    instrDepManager.GetDeploymentCmbo().SetBackgroundColour(color)

    instrDepManager.manufactureCmbo = "SonTek"
    instrDepManager.GetManufactureCmbo().SetBackgroundColour(color)
    if firmware is not None and firmware != "":
        instrDepManager.firmwareCmbo = firmware
        instrDepManager.GetFirmwareCmbo().SetBackgroundColour(color)
    if serial is not None and serial != "":
        instrDepManager.serialCmbo = serial
        instrDepManager.GetSerialCmbo().SetBackgroundColour(color)
    if model is not None and model != "":
        instrDepManager.modelCmbo = model
        instrDepManager.GetModelCmbo().SetBackgroundColour(color)
    if comments != "":
        if disManager.dischRemarksCtrl == "":
            disManager.dischRemarksCtrl += "RSSL Comments:\n" + comments
        else:
            disManager.dischRemarksCtrl += "\nRSSL Comments:\n" + comments

    if numberOfPanels != "":
        # Two panels are subtracted as the edges do not need to be considered
        instrDepManager.numOfPanelsScroll = str(int(numberOfPanels)-2)
        instrDepManager.GetNumOfPanelsScroll().SetBackgroundColour(color)


    


    # print firmware, "firmware"
    # print serial, "serial"
    # print model, "model"


#Convert 12 Hour format to 24 Hour
def PmTo24H(time):
    print(time)
    t = time.split()[0]
    sign = time.split()[1]
    if sign.upper() == "PM" and int(t[:2]) < 12:
        return str(int(t[:2]) + 12) + t[2:]
    else:
        return t 

# GetStationID("RSSL\\Test_20180301.dis")
# GetDate("RSSL\\Test_20180301.dis")
# AddDischargeSummary("RSSL\\Test_20180301.dis", None)
# AddDischargeDetail("RSSL\\Test_20180301.dis", None)



# print "-------------------"
# print PmTo24H("3:12 PM")
# print PmTo24H("3:12 AM")
# print PmTo24H("10:12 PM")
# print PmTo24H("10:12 AM")
# print PmTo24H("03:12 AM")
# print PmTo24H("03:12 PM")