# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html
from suds.client import Client
import suds
import datetime
import pytz
from AquariusMiscUploadDialogs import *
from suds.xsd.doctor import Import, ImportDoctor

import xml.etree.ElementTree as ET
# import pdb
# from dateutil.tz import *
import re
# import dateutil.parser


dischargeSensors = {'QR' : 'm^3/s',
                    'LA' : 'km^2',
                    'HL' : 'm',
                    'HG' : 'm',
                    'IC' : '%',
                    'IO' : 'km',
                    'IE' : 'km',
                    'RiverSectionArea' : 'm^2',
                    'RiverSectionWidth' : 'm',
                    'WS' : 'ppt',
                    'SoundVel' : 'm/s',
                    'TW' : u'\u00B0' + 'C',
                    'WV' : 'm/s',
                    }

stageSensors = {'HG' : 'm'}

environmentSensors = {'TA' : u'\u00B0' + 'C',
                      'PA' : 'kPa',
                      'IO' : 'km',
                      'PN' : 'mm',
                      'SL' : 'kg',
                      'STR' : 'kg/s',
                      'SA' : '%',
                      'SD' : 'cm',
                      'UD' : 'deg',
                      'TW' : u'\u00B0' + 'C',
                      'US' : 'km/hr'
                      }

stationhealthSensors = {'PA' : 'kPa',
                        'YBL' : 'V',
                        'InternalTemp' : u'\u00B0' + 'C',
                        'N2BubbleRate' : 'B./min',
                        'YR' : 'W',
                        'YSS' : 'dBm',
                        'SolarPanelVoltage' : 'V',
                        'YP' : 'psi',
                        'VB' : 'V',
                        'YP2' : 'psi',
                        'TW' : u'\u00B0' + 'C',
                        'TA' : u'\u00B0' + 'C',
                        'PC' : 'mm',
                        'SW' : 'cm',
                        'YF' : 'W',
                        'PN' : 'mm',
                        'IO' : 'km',
                        'SL' : 'kg',
                        'STR' : 'kg/s',
                        'SA' : '%',
                        'SD' : 'cm',
                        'UD' : 'deg',
                        'RN' : 'W/m^2',
                        'HD' : 'm',
                        'PP' : 'mm'

                        }



# timeZones = {'PST' : datetime.timedelta(hours=0),
             # 'MST' : datetime.timedelta(hours=0),
             # 'CST' : datetime.timedelta(hours=0),
             # 'EST' : datetime.timedelta(hours=0),
             # 'AST' : datetime.timedelta(hours=0),
             # 'NST' : datetime.timedelta(hours=0, minutes=0),
             # 'UTC' : datetime.timedelta(hours=0)}




isoTail = ".000-00:00"
resultType = 0
resultType_NA = 0
resultType_RC = 1
resultType_TS = 2
resultType_All = 2147483647

storedUserName = ''
storedPassword = ''






# Attempt to log into AQ,
# If unable to log in, return error
# If able to log in, return Client
def AquariusLogin(mode, server, username, password):


    try:
        aq = Client('http://' + server + '/aquarius/AQAcquisitionService.svc?wsdl')
        aq.set_options(headers={'AQAuthToken':aq.service.GetAuthToken(username, password)})


        return True, aq
    except suds.WebFault, e:
        if mode == "DEBUG":
            print str(e)
        return False, str(e)


#Check if the data already exist in the list by paramID
#return False if found the same paramID in the list given by the parameter 'list'
def FillInBlankDischarge(list, paramID):
    if paramID in list:
        return False
    else:
        return True




# Check if location exists (stationNum)
def AquariusCheckLocInfo(mode, aq, stationNum):
    locid = aq.service.GetLocationId(stationNum)

    locinf = aq.service.GetLocation(locid)


    if mode == "DEBUG":
        print locinf

    if locinf is not None:
        return True, locid
    else:
        return False, None

# Call AQ for Field Visit list
# Compare ALL Field Visits against given date
def AquariusFieldVisitExistsByDate(mode, aq, locid, fvDate):
    fvDate = datetime.datetime.strptime(str(fvDate), "%Y/%m/%d")

    if mode == "DEBUG":
        print "Checking existance of Field Visit for given date"

    #Find all field visits based on locid
    fv = aq.service.GetFieldVisitsByLocation(locid)

    if len(fv) < 1:
        return None, None

    #Parse field visit data as our own objects (SimpleFieldVisit)
    disList = []
    for i, visit in enumerate(fv[0]):
    # if fv[0][i].Measurements is not None:
        dt = datetime.datetime.strptime(str(visit.StartDate)[:19], "%Y-%m-%d %H:%M:%S")
        if mode == "DEBUG":
            print dt
            print unicode(dt.strftime("%Y/%m/%d"))
            print fvDate

        if dt.strftime("%Y/%m/%d") == fvDate.strftime("%Y/%m/%d"):
            if visit.Measurements is not None:
                for meas in visit.Measurements.FieldVisitMeasurement:

                    if "discharge" in meas.MeasurementType.lower():
                        disList.append(meas)
            return visit, disList

    ## for i in range(len(date_list)):
    # if fvDate.strftime("%Y/%m/%d") == date_list[i][0]:
    # return date_list[i][1]

    return 0, disList




# Return all the parameterID by given field visit
def GetParaIDByFV(discharge):
    results = []
    if discharge is None:
        return None
    if len(discharge) == 0:
        return results
    if discharge.Results is not None:
        for mea in discharge.Results.FieldVisitResult:
            results.append(mea.ParameterID)
    return results


# Creates the Field Visit object and sends to AQ
def ExportToAquarius(mode, ver, EHSN, aq, FIELDVISIT, locid, discharge, levelNote, list, dischargeResult, server):
    if mode == "DEBUG":
        print "Saving Field Visit in Aquarius"
    # try:

    visit = CreateFieldVisitObject(mode, ver, aq, locid, EHSN, FIELDVISIT, discharge, levelNote, list, dischargeResult, server)

    if mode == "DEBUG":
        print "before field visit save"
        print visit

    fieldV = aq.service.SaveFieldVisit(visit)

    if mode == "DEBUG":
        print fieldV
        print "after field visit save"

    return None

    # except suds.WebFault, e:
    #     if mode == "DEBUG":
    #         print str(e)

    #     return str(e)
    # except ValueError, e:
    #     if mode == "DEBUG":
    #         print str(e)
    #         print e.message

    #     return str(e)

# Creates Field Visit object
# Calls each of 4 FVMeasurements (Disch, Stage, StationHealth, EnvConidtions)
# if discharge is false than discharge/area/velocity/mean gauge height will not be included
def CreateFieldVisitObject(mode, ver, aq, locid, EHSN, FIELDVISIT, discharge, levelNote, list, dischargeResult, server):
    if FIELDVISIT == 0:
        FIELDVISIT_ID = 0
    else:
        FIELDVISIT_ID = FIELDVISIT.FieldVisitID

    src = "eHSN %s" % ver

    if mode == "DEBUG":
        print "Creating Field Visit"

    tz = EHSN.genInfoManager.tzCmbo



    #Convert to DateTime
    start = datetime.datetime.strptime(str(EHSN.genInfoManager.datePicker), "%Y/%m/%d")
    end = datetime.datetime.strptime(str(EHSN.genInfoManager.datePicker), "%Y/%m/%d")

    startTime = None
    endTime = None


#End Time

    if EHSN.disMeasManager.GetEndTimeCtrl().IsCompleted():
        endTime = EHSN.disMeasManager.gui.endTimeCtrl#.GetWxDateTime()
        end = end.replace(hour=int(endTime.GetHourVal()), minute=int(endTime.GetMinuteVal()))
        isoEnd = str(end.isoformat()) + isoTail



#Start time
    if EHSN.disMeasManager.GetStartTimeCtrl().IsCompleted():
        startTime = EHSN.disMeasManager.gui.startTimeCtrl#.GetWxDateTime()
        
        ##Here it assumes the date is the same day
        start = start.replace(hour=int(startTime.GetHourVal()), minute=int(startTime.GetMinuteVal()))
        isoStart = str(start.isoformat()) + isoTail
        
    else:
        startTime = EHSN.stageMeasManager.gui.GetFirstTime()


#Initialize time if it is none
    if startTime is not None:
        start = start.replace(hour=int(startTime.GetHourVal()), minute=int(startTime.GetMinuteVal()))
    else:
        # start time is null, so set the time to 0
        start = start.replace(
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0
        )


    if endTime is not None:
        end = end.replace(hour=int(endTime.GetHourVal()), minute=int(endTime.GetMinuteVal()))
    else:
        # end time is null, so set the time to 0
        end = end.replace(
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0
        )


    fvStartDate = str(start.isoformat()) + isoTail
    fvEndDate = str(end.isoformat()) + isoTail

    isoStart = fvStartDate
    isoEnd = fvEndDate









    #==============================================================
    dateInfo=start
    print dateInfo
    #Create New Field Visit
    visit = aq.factory.create("ns0:FieldVisit")

    visit.LocationID = locid
    visit.FieldVisitID = FIELDVISIT_ID
    visit.StartDate = fvStartDate


    visit.Party = EHSN.partyInfoManager.partyCtrl

    visit.Remarks = ""
    # visit.Remarks += "" if EHSN.instrDepManager.controlRemarksCtrl == "" else (EHSN.instrDepManager.controlRemarksCtrl + "\n")
    # visit.Remarks += "" if EHSN.instrDepManager.dischRemarksCtrl == "" else (EHSN.instrDepManager.dischRemarksCtrl + "\n")
    # visit.Remarks += EHSN.instrDepManager.genRemarksCtrl
    visit.Remarks += "" if visit.Remarks == "" else "\n"


    if FIELDVISIT_ID != 0:
        visit.HistoryLog = FIELDVISIT.HistoryLog
        if mode == "DEBUG":
            print FIELDVISIT.HistoryLog

    visit.Measurements = aq.factory.create("ns0:ArrayOfFieldVisitMeasurement")
    visit.Measurements.FieldVisitMeasurement = []

    #define measurement IDs
    dMeas = 0
    sMeas = 0
    shMeas = 0
    ecMeas = 0
    lsMeas = 0

    if str(EHSN.disMeasManager.mmtValTxt) == "" or str(EHSN.disMeasManager.mmtValTxt) is None:
        
        if EHSN.stageMeasManager.CalculteMeanTime() != ":" and EHSN.stageMeasManager.CalculteMeanTime() != "0:0":
            start = start.replace(hour=int(EHSN.stageMeasManager.GetFirstTime().GetHourVal()), minute=int(EHSN.stageMeasManager.GetFirstTime().GetMinuteVal()))
            end = end.replace(hour=int(EHSN.stageMeasManager.GetLastTime().GetHourVal()), minute=int(EHSN.stageMeasManager.GetLastTime().GetMinuteVal()))
            
            isoStart = str(start.isoformat()) + isoTail
            isoEnd = str(end.isoformat()) + isoTail




    if discharge:

        EHSN.gui.deleteProgressDialog()
        dmeasurement = CreateDischargeMeasurements(mode, src, aq, visit, dMeas, EHSN,dateInfo, isoStart, isoEnd, list, dischargeResult)
        EHSN.gui.createProgressDialog("Uploading Field Visit to AQUARIUS", "Creating field visit to be uploaded to AQUARIUS")
    else:
        dmeasurement = None

    smeasurement = CreateStageMeasurements(mode, src, aq, visit, sMeas, EHSN, dateInfo, fvStartDate, server)
    # print smeasurement
    shmeasurement = CreateStationHealthMeasurements(mode, src, aq, visit, shMeas, EHSN, dateInfo, fvStartDate)
    ecmeasurement = CreateEnvironmentConditionsMeasurements(mode, src, aq, visit, ecMeas, EHSN, dateInfo, fvStartDate)
    if levelNote:
        lsmeasurement = CreateLevelSurveyMeasurements(mode, src, aq, visit, lsMeas, EHSN, dateInfo, server, fvStartDate)
    else:
        lsmeasurement = None


    # Don't add the measurement if there was no results

    if dmeasurement is not None:
        visit.Measurements.FieldVisitMeasurement.append(dmeasurement)
    if smeasurement is not None:
        visit.Measurements.FieldVisitMeasurement.append(smeasurement)
    if shmeasurement is not None:
        visit.Measurements.FieldVisitMeasurement.append(shmeasurement)
    if ecmeasurement is not None:
        visit.Measurements.FieldVisitMeasurement.append(ecmeasurement)
    if lsmeasurement is not None:
        visit.Measurements.FieldVisitMeasurement.append(lsmeasurement)

    if len(visit.Measurements.FieldVisitMeasurement) <= 0 and visit.Remarks == "":
        raise ValueError("No valid measurements or remarks found. Cancelling upload.")

    return visit

# Check values of eHSN to see if it will generate any errors on Field Visit creation
def CheckFVVals(mode, EHSN):
    # #### DISCHARGE MEASUREMENTS CHECKS #### #
    # discharge check
    try:
        if EHSN.disMeasManager.dischCtrl != "":
            float(EHSN.disMeasManager.dischCtrl)
    except ValueError:
        raise ValueError("Discharge value: %s is not a float" % EHSN.disMeasManager.dischCtrl)

    # mgh check
    try:
        if EHSN.disMeasManager.mghCtrl != "":
            float(EHSN.disMeasManager.mghCtrl)
    except ValueError:
        raise ValueError("Mean Gauge Height: %s is not a float" % EHSN.disMeasManager.mghCtrl)

    # river x area
    try:
        if EHSN.disMeasManager.areaCtrl != "":
            float(EHSN.disMeasManager.areaCtrl)
    except ValueError:
        raise ValueError("Area: %s is not a float" % EHSN.disMeasManager.areaCtrl)

    # water velocity
    try:
        if EHSN.disMeasManager.meanVelCtrl != "":
            float(EHSN.disMeasManager.meanVelCtrl)
    except ValueError:
        raise ValueError("Water Velocity: %s is not a float" % EHSN.disMeasManager.meanVelCtrl)

    # water temperature
    try:
        if EHSN.disMeasManager.waterTempCtrl != "":
            float(EHSN.disMeasManager.waterTempCtrl)
    except ValueError:
        raise ValueError("Water Temp: %s is not a float" % EHSN.disMeasManager.waterTempCtrl)

    # ###Stage Measurements###
    for row in range(len(EHSN.stageMeasManager.timeValSizer.GetChildren())):
        try:
            if EHSN.stageMeasManager.GetHGVal(row) != "":
                float(EHSN.stageMeasManager.GetHGVal(row))
        except ValueError:
            raise ValueError("Stage measurement: %s is not a float" % EHSN.stageMeasManager.GetHGVal(row))



        try:
            if EHSN.stageMeasManager.GetWLSubSizerLVal(row) != "":
                float(EHSN.stageMeasManager.GetWLSubSizerLVal(row))
        except ValueError:
            raise ValueError("Stage measurement: %s is not a float" % EHSN.stageMeasManager.GetWLSubSizerLVal(row))

        try:
            if EHSN.stageMeasManager.GetWLSubSizerRVal(row) != "":
                float(EHSN.stageMeasManager.GetWLSubSizerRVal(row))
        except ValueError:
            raise ValueError("Stage measurement: %s is not a float" % EHSN.stageMeasManager.GetWLSubSizerRVal(row))

    # ###The rest###
    # N2 Bubble rate
    try:
        if EHSN.envCondManager.bpmrotCtrl != "":
            float(EHSN.envCondManager.bpmrotCtrl)
    except ValueError:
        raise ValueError("N2 bubble rate: %s is not float" % EHSN.envCondManager.bpmrotCtrl)

    # battery voltage
    try:
        if EHSN.envCondManager.batteryCtrl != "":
            float(EHSN.envCondManager.batteryCtrl)
    except ValueError:
        raise ValueError("Battery voltage: %s is not float" % EHSN.envCondManager.batteryCtrl)

    # Air Temp
    try:
        if EHSN.disMeasManager.airTempCtrl != "":
            float(EHSN.disMeasManager.airTempCtrl)
    except ValueError:
        raise ValueError("Air Temperature: %s is not float" % EHSN.disMeasManager.airTempCtrl)

    # Wind veloc
    try:
        if EHSN.envCondManager.windMagCtrl != "":
            float(EHSN.envCondManager.windMagCtrl)
    except ValueError:
        raise ValueError("Wind Velocity: %s is not float" % EHSN.envCondManager.windMagCtrl)


    # Remaining sensor values
    for index, sensorRefEntry in enumerate(EHSN.measResultsManager.sensorRefEntries):

        # Is this a "valid" measurement result that can be uploaded to Aquarius?
        if EHSN.measResultsManager.sensorRef.has_key(sensorRefEntry.GetValue().strip()):

            try:
                if EHSN.measResultsManager.observedVals[index].GetValue() != "":
                    float(EHSN.measResultsManager.observedVals[index].GetValue())
            except ValueError:
                raise ValueError("%s: %s is not float" % (sensorRefEntry.GetValue().strip(),
                                                          EHSN.measResultsManager.observedVals[index].GetValue()))
    # HG and Water Level Reference cannot both be empty in a row
    #if EHSN.stageMeasManager.emptyChecking():
    #    raise ValueError("Empty Stage measurement found")
    if not EHSN.stageMeasManager.timeChecking():
        raise ValueError("Invalid logger time found")
    if not EHSN.measResultsManager.IsEmpty():
        if EHSN.measResultsManager.timeCtrl == '00:00':
            raise ValueError("Invalid sensor time found")
    return True

# Escaping for spcial characters from xml
def repChar(str):
    mlist = list(str)
    nStr=""
    for char in range(len(mlist)):
        if(mlist[char] == '&'):
            nStr += "<![CDATA[&]]>"
        elif(mlist[char] == '<'):
            nStr += "<![CDATA[<]]>"
        elif(mlist[char] == '>'):
            nStr += "<![CDATA[>]]>"
        elif(mlist[char] == '\''):
            nStr += "<![CDATA[']]>"
        elif(mlist[char] == '\"'):
            nStr += "<![CDATA[\"]]>"
        else:
            nStr += mlist[char]

    return nStr

# Creates a FIeldVisitMeasurement with type WscFvtPlugin_ActivityTypeDischarge
def CreateDischargeMeasurements(mode, src, aq, visit, MEASUREMENT, EHSN, dateInfo, isoStart, isoEnd, list, dischargeResult):
    if mode == "DEBUG":
        print "Creating Discharge Measurements"

    # Used to replace / modify existing Measurements
    if MEASUREMENT == 0:
         MEASUREMENT_ID = 0
    else:
         MEASUREMENT_ID = MEASUREMENT.MeasurementID

    # Since we're not donig that, we just set to 0
    # MEASUREMENT_ID = 0
    hg = EHSN.stageMeasManager.MGHHG.strip()
    hg2 = EHSN.stageMeasManager.MGHHG2.strip()
    wl1 = EHSN.stageMeasManager.MGHWLRefL.strip()
    wl2 = EHSN.stageMeasManager.MGHWLRefR.strip()

    src1 = EHSN.stageMeasManager.SRCHG.strip()
    src2= EHSN.stageMeasManager.SRCHG2.strip()



    #Results
    meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"
    meanTime = datetime.datetime.strptime(meanTime, "%H:%M")
    meanTime = meanTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
    meanTime = str(meanTime.isoformat()) + isoTail

    checkList = EHSN.instrDepManager.methodCBListBox.GetCheckedStrings()
    method = "" if len(checkList) <= 0 else checkList[0]
    if method != "" and EHSN.instrDepManager.deploymentCmbo != "":
        method += "_" + EHSN.instrDepManager.deploymentCmbo
    compassCali = "" if str(EHSN.instrDepManager.compassCaliCB) == "False" else str(EHSN.instrDepManager.compassCaliCB)
    movingBedTest = str(EHSN.movingBoatMeasurementsManager.mbCmbo)+" Test" if EHSN.movingBoatMeasurementsManager.mbCmbo != "" else ""


    cdataParty = repChar(visit.Party)
    if dischargeResult is None:
        dmeasurement = aq.factory.create("ns0:FieldVisitMeasurement")
        dmeasurement.ApprovalLevelID = 3
        dmeasurement.MeasurementID = MEASUREMENT_ID
        dmeasurement.FieldVisitID = visit.FieldVisitID
        dmeasurement.MeasurementType = "WscFvtPlugin_ActivityTypeDischarge"
        dmeasurement.MeasurementTime = isoStart
        dmeasurement.MeasurementEndTime = isoEnd
        dmeasurement.LastModified = datetime.datetime(0001, 01, 01)


        if ('ADCP' in EHSN.instrDepManager.methodCBListBox.GetCheckedStrings() ) or ('ADCP' in EHSN.instrDepManager.instrumentCmbo):
            dmeasurement.MeasurementDetails = """<?xml version="1.0" encoding="UTF-8"?>
        <DiscreteMeasurementDetails xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <ControlCondition>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlCondition>
          <Method>""" + method + """</Method>
          <AdcpMeasurementDetails>
            <Party>""" + cdataParty + """</Party>
            <InstrumentType>""" + str(EHSN.instrDepManager.manufactureCmbo) + ' ' + str(EHSN.instrDepManager.modelCmbo) + ' ' + \
            str(EHSN.instrDepManager.frequencyCmbo) + """</InstrumentType>
            <TrackReference>""" + str(EHSN.movingBoatMeasurementsManager.trackRefCmbo) + """</TrackReference>
            <Method>""" + method + """</Method>
            <CompassCalibration>""" + compassCali + """</CompassCalibration>
            <CompassError>""" + '' + """</CompassError>
            <MovingBedTest>""" + movingBedTest + """</MovingBedTest>
            <MovingBedCorrection>""" + str(EHSN.movingBoatMeasurementsManager.mbCorrAppCtrl) + """</MovingBedCorrection>
            <SoftwareAndVersion>""" + str(EHSN.instrDepManager.softwareCtrl) + """</SoftwareAndVersion>
            <FirmwareVersion>""" + str(EHSN.instrDepManager.firmwareCmbo) + """</FirmwareVersion>
            <SerialNumber>""" + str(EHSN.instrDepManager.serialCmbo) + """</SerialNumber>
            <ControlCondition>""" + EHSN.instrDepManager.controlConditionCmbo + """</ControlCondition>
          </AdcpMeasurementDetails>
        </DiscreteMeasurementDetails>"""
        elif 'ADV' in EHSN.instrDepManager.instrumentCmbo:

            dmeasurement.MeasurementDetails = """<?xml version="1.0" encoding="UTF-8"?>
                <DiscreteMeasurementDetails xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                  <ControlCondition>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlCondition>
                  <Method>""" + method + """</Method>
                  <AdcpMeasurementDetails>
                    <Party>""" + cdataParty + """</Party>
                    <InstrumentType>""" + str(EHSN.instrDepManager.manufactureCmbo) + ' ' + str(EHSN.instrDepManager.modelCmbo) + """</InstrumentType>
                    <TrackReference>""" + str(EHSN.movingBoatMeasurementsManager.trackRefCmbo) + """</TrackReference>
                    <Method>""" + method + """</Method>
                    <CompassCalibration>""" + compassCali + """</CompassCalibration>
                    <CompassError>""" + '' + """</CompassError>
                    <MovingBedTest>""" + movingBedTest + """</MovingBedTest>
                    <MovingBedCorrection>""" + str(EHSN.movingBoatMeasurementsManager.mbCorrAppCtrl) + """</MovingBedCorrection>
                    <SoftwareAndVersion>""" + str(EHSN.instrDepManager.softwareCtrl) + """</SoftwareAndVersion>
                    <FirmwareVersion>""" + str(EHSN.instrDepManager.firmwareCmbo) + """</FirmwareVersion>
                    <SerialNumber>""" + str(EHSN.instrDepManager.serialCmbo) + """</SerialNumber>
                    <ControlCondition>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlCondition>
                  </AdcpMeasurementDetails>
                </DiscreteMeasurementDetails>"""

        else:

            dmeasurement.MeasurementDetails = """<?xml version="1.0" encoding="UTF-8"?>
                <DiscreteMeasurementDetails xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                  <ControlCondition>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlCondition>
                  <Method>""" + method + """</Method>
                  <AdcpMeasurementDetails>
                    <Party>""" + cdataParty + """</Party>
                    <InstrumentType>""" + str(EHSN.instrDepManager.modelCmbo) + """</InstrumentType>
                    <TrackReference>""" + str(EHSN.movingBoatMeasurementsManager.trackRefCmbo) + """</TrackReference>
                    <Method>""" + method + """</Method>
                    <CompassCalibration>""" + compassCali + """</CompassCalibration>
                    <CompassError>""" + '' + """</CompassError>
                    <MovingBedTest>""" + movingBedTest + """</MovingBedTest>
                    <MovingBedCorrection>""" + str(EHSN.movingBoatMeasurementsManager.mbCorrAppCtrl) + """</MovingBedCorrection>
                    <SoftwareAndVersion>""" + str(EHSN.instrDepManager.softwareCtrl) + """</SoftwareAndVersion>
                    <FirmwareVersion>""" + str(EHSN.instrDepManager.firmwareCmbo) + """</FirmwareVersion>
                    <SerialNumber>""" + str(EHSN.instrDepManager.serialCmbo) + """</SerialNumber>
                    <ControlCondition>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlCondition>
                  </AdcpMeasurementDetails>
                </DiscreteMeasurementDetails>"""


        dmeasurement.Remarks == ""
        if EHSN.instrDepManager.dischRemarksCtrl.strip() != "":
            dmeasurement.Remarks = "Discharge Remarks: " + EHSN.instrDepManager.dischRemarksCtrl.strip() + "\n"
            if EHSN.instrDepManager.controlConditionRemarksCtrl.strip() != "":
                dmeasurement.Remarks += ("Control Condition Remarks: " + EHSN.instrDepManager.controlConditionRemarksCtrl.strip() + "\n")


        dmeasurement.Remarks += ("Depth Ref: " + EHSN.movingBoatMeasurementsManager.depthRefCmbo) if EHSN.movingBoatMeasurementsManager.depthRefCmbo != "" else ""
        if 0 in EHSN.instrDepManager.methodCBListBox.GetCheckedItems():
            if EHSN.movingBoatMeasurementsManager.velocityTopCombo != "" or \
            EHSN.movingBoatMeasurementsManager.velocityBottomCombo != "" or \
            EHSN.movingBoatMeasurementsManager.velocityExponentCtrl != "":
                dmeasurement.Remarks += "\n" if dmeasurement.Remarks != "" else ""
                dmeasurement.Remarks += ("Extrapolation: \n\tTop: " + EHSN.movingBoatMeasurementsManager.velocityTopCombo + "; Bottom: " + EHSN.movingBoatMeasurementsManager.velocityBottomCombo + "; Exponent: " + EHSN.movingBoatMeasurementsManager.velocityExponentCtrl)
            dmeasurement.Remarks += ("\n% Difference in Q from extrap: " + EHSN.movingBoatMeasurementsManager.differenceCtrl) if EHSN.movingBoatMeasurementsManager.differenceCtrl != "" else ""
        if EHSN.instrDepManager.gaugeCtrl != '':
            dmeasurement.Remarks += "\n" if dmeasurement.Remarks != "" else ""
            dmeasurement.Remarks += EHSN.instrDepManager.gaugeCtrl + " "
            dmeasurement.Remarks += "metres " if EHSN.instrDepManager.lengthRadButBox == 0 else "kilometres "
            dmeasurement.Remarks += "above " if EHSN.instrDepManager.posRadButBox == 0 else "below "
            dmeasurement.Remarks += EHSN.instrDepManager.selectedGauge



        dmeasurement.Results = aq.factory.create("ns0:ArrayOfFieldVisitResult")
        dmeasurement.Results.FieldVisitResult = []
    else:
        dmeasurement = dischargeResult

        start = datetime.datetime.strptime(isoStart, "%Y-%m-%dT%H:%M:%S.000-00:00")
        end = datetime.datetime.strptime(isoEnd, "%Y-%m-%dT%H:%M:%S.000-00:00")

        dmeasurement.MeasurementTime = dmeasurement.MeasurementTime.strftime("%Y-%m-%dT%H:%M:%S.000-00:00") if dmeasurement.MeasurementTime < start else\
                isoStart
        dmeasurement.MeasurementEndTime = dmeasurement.MeasurementEndTime.strftime("%Y-%m-%dT%H:%M:%S.000-00:00") if dmeasurement.MeasurementEndTime \
        > end else\
                isoEnd


        start = datetime.datetime.strptime(dmeasurement.MeasurementTime, "%Y-%m-%dT%H:%M:%S.000-00:00")
        end = datetime.datetime.strptime(dmeasurement.MeasurementEndTime, "%Y-%m-%dT%H:%M:%S.000-00:00")
        df =  start + ((end - start) / 2)
        meanTime = df.strftime("%Y-%m-%dT%H:%M:%S.000-00:00")


        if dmeasurement.Results is None:
            dmeasurement.Results = aq.factory.create("ns0:ArrayOfFieldVisitResult")
            dmeasurement.Results.FieldVisitResult = []

    # if MEASUREMENT_ID != 0:
    #      if MEASUREMENT.Results is not None:
    #          for i in range(len(MEASUREMENT.Results[0])):
    #              MEASUREMENT.Results.FieldVisitResult[i].ResultID = -MEASUREMENT.Results.FieldVisitResult[i].ResultID
    #              dmeasurement.Results.FieldVisitResult.append(MEASUREMENT.Results.FieldVisitResult[i])



    # #Air Temp
    # if str(EHSN.disMeasManager.airTempCtrl) != "":
    #     ParamID = 'TA'

    #     airTempResult = aq.factory.create("ns0:FieldVisitResult")
    #     airTempResult.MeasurementID = dmeasurement.MeasurementID
    #     airTempResult.ResultID = 0
    #     airTempResult.StartTime = meanTime
    #     # airTempResult.EndTime = visit.EndDate
    #     airTempResult.ParameterID = ParamID
    #     airTempResult.UnitID = environmentSensors[ParamID]
    #     airTempResult.ResultType = resultType
    #     airTempResult.ObservedResult = float(EHSN.disMeasManager.airTempCtrl)
    #     airTempResult.Correction = 0.000
    #     cdataParty = repChar(visit.Party)
    #     airTempResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    # <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #   <Party>""" + cdataParty + """</Party>
    #   <Source>
    #     <SourceType>
    #       <Id>Import</Id>
    #       <DisplayName>""" + src + """</DisplayName>
    #     </SourceType>
    #     <DisplayName>""" + src + """</DisplayName>
    #     <Sequence>1</Sequence>
    #   </Source>
    # </DischargeResult>
    # """
    #     dmeasurement.Results.FieldVisitResult.append(airTempResult)



    # #SRC constraint for HG and HG2
    # if (hg != '' and src1 == '') or (hg2 != '' and src2 == ''):
    #     warning = wx.MessageDialog(None, "Warning",
    #         "S.R.C. is empty", wx.OK| wx.ICON_EXCLAMATION)
    #     cont = warning.ShowModal()
    #     if cont == wx.ID_OK:
    #         return







    #Mean Gauge Height
    # if str(EHSN.disMeasManager.mghCtrl).strip() != "":
    if str(EHSN.disMeasManager.mghCtrl).strip() != "" and str(EHSN.disMeasManager.mghCmbo).strip() != "":

        # eMGH = float(EHSN.disMeasManager.mghCtrl)
        ParamID = 'HG'

        # If we found the mgh in the field visit, then we ask and the user will choose
        # If we could not find the mgh in the field visit, then we add automatically
        mghFound = False

        # Make mgh, only add if we should
        mghResult = aq.factory.create("ns0:FieldVisitResult")
        mghResult.MeasurementID = dmeasurement.MeasurementID
        mghResult.ResultID = 0

        # mghResult.BenchmarkOrRefPointName = None
        # mghResult.EndTime = None
        mghResult.StartTime = meanTime
        # mghResult.PercentUncertainty = None
        # mghResult.Qualifier = None
        # mghResult.QualityCodeID = None
        # mghResult.Remarks = None

        mghResult.ParameterID = ParamID
        mghResult.UnitID = dischargeSensors[ParamID]


        mghCmbo = EHSN.disMeasManager.GetMghCmbo()
        selection = mghCmbo.GetSelection()
        if selection == 1:
            eMGH = float(src1) + float(hg)
            dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg + " + " + src1 + ")"
            gaugeCorrection = EHSN.stageMeasManager.GCHG
        elif selection == 2:
            eMGH = float(src2) + float(hg2)
            dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg2 + " + " + src2 + ")"
            gaugeCorrection = EHSN.stageMeasManager.GCHG2
        elif selection == 3:
            eMGH = float(wl1)
            gaugeCorrection = EHSN.stageMeasManager.GCWLRefL
        elif selection == 4:
            eMGH = float(wl2)
            gaugeCorrection = EHSN.stageMeasManager.GCWLRefR




        emptyTestList = [hg != '', hg2 != '', wl1 != '', wl2 != '']
        i = iter(emptyTestList)
        ##################################For use of pop up message, let user choose if there are more then one MGH############
        # #only one has value
        # if (any(i) and not any(i)):

        #     if hg != '':
        #         if src1 != '':
        #             eMGH = float(src1) + float(hg)
        #             dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg + " + " + src1 + ")"
        #         else:
        #             eMGH = float(hg)
        #         gaugeCorrection = EHSN.stageMeasManager.GCHG

        #     elif hg2 != '':

        #         if src2 != '':
        #             eMGH = float(src2) + float(hg2)
        #             dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg2 + " + " + src2 + ")"
        #         else:
        #             eMGH = float(hg2)
        #         gaugeCorrection = EHSN.stageMeasManager.GCHG2
        #     elif wl1 != '':
        #         eMGH = float(wl1)
        #         gaugeCorrection = EHSN.stageMeasManager.GCWLRefL
        #     elif wl2 != '':
        #         eMGH = float(wl2)
        #         gaugeCorrection = EHSN.stageMeasManager.GCWLRefR

        # #if only have hg values, uploading value from hg
        # elif wl1 == '' and wl2 == '':
        #     if src1 != '':
        #         eMGH = float(src1) + float(hg)
        #         dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg + " + " + src1 + ")"
        #     else:
        #         eMGH = float(hg)
        #     gaugeCorrection = EHSN.stageMeasManager.GCHG

        # #if they have the same value except the empty then shoulf follow the priority wl1 > wl2 > hg > hg2
        # #if wl1 is not empty and all value are the same
        # elif wl1 != '' and (wl2 == wl1 or wl2 == '') and (hg == wl1 or hg == '') and (hg2 == wl1 or hg2 == ''):
        #      eMGH = float(wl1)
        #      gaugeCorrection = EHSN.stageMeasManager.GCWLRefL
        # #if wl2 is not empty and all value are the same
        # elif wl2 != '' and (wl1 == wl2 or wl1 == '') and (hg == wl2 or hg == '') and (hg2 == wl2 or hg2 == ''):
        #      eMGH = float(wl2)
        #      gaugeCorrection = EHSN.stageMeasManager.GCWLRefR
        # #if hg is not empty and all value are the same
        # elif hg != '' and (wl1 == hg or wl1 == '') and (wl2 == hg or wl2 == '') and (hg2 == hg or hg2 == ''):
        #     if src1 != '':
        #         eMGH = float(src1) + float(hg)
        #         dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg + " + " + src1 + ")"
        #     else:
        #         eMGH = float(hg)
        #     gaugeCorrection = EHSN.stageMeasManager.GCHG
        # # #if hg2 is not empty and all value are the same
        # # elif hg2 != '' and (wl1 == hg2 or wl1 == '') and (wl2 == hg2 or wl2 == '') and (hg == hg2 or hg == ''):
        # #     if src2 != '':
        # #         eMGH = float(src2) + float(hg2)
        # #         dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg2 + " + " + src2 + ")"
        # #     else:
        # #         eMGH = float(hg2)
        # #     gaugeCorrection = EHSN.stageMeasManager.GCHG2




        # #case to leave the selection for the user
        # else:
        #     AMD = DuplicateMGHUpload(EHSN.gui.mode, emptyTestList[0], emptyTestList[1], emptyTestList[2], emptyTestList[3], parent=EHSN.gui.aquariusUploadDialog, title="Upload Field Visit to Aquarius")
        #     re = AMD.ShowModal()
        #     if re == ID_HG:
        #         if src1 != '':
        #             eMGH = float(src1) + float(hg)
        #             dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg + " + " + src1 + ")"
        #         else:
        #             eMGH = float(hg)
        #         gaugeCorrection = EHSN.stageMeasManager.GCHG
        #     elif re == ID_HG2:
        #         if src2 != '':
        #             eMGH = float(src2) + float(hg2)
        #             dmeasurement.Remarks += "\nMGH has had sensor reset applied at upload (" + hg2 + " + " + src2 + ")"
        #         else:
        #             eMGH = float(hg2)
        #         gaugeCorrection = EHSN.stageMeasManager.GCHG2
        #     elif re == ID_WL1:
        #         eMGH = float(wl1)
        #         gaugeCorrection = EHSN.stageMeasManager.GCWLRefL
        #     elif re == ID_WL2:
        #         eMGH = float(wl2)
        #         gaugeCorrection = EHSN.stageMeasManager.GCWLRefR
        #     else:
        #         print "wrong"
        #         eMGH = 0

        #     AMD.Destroy()
        ######################################################################################################

        # mghResult.ObservedResult = float(EHSN.disMeasManager.mghCtrl)
        mghResult.ObservedResult = eMGH
        mghResult.Correction = 0.000 if gaugeCorrection == '' else float(gaugeCorrection)

        mghResult.ResultType = resultType_RC
        mghResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </DischargeResult>
    """

        for mea in dmeasurement.Results.FieldVisitResult:

            val = True


            if mea.ParameterID == ParamID:
                aMGH = mea.ObservedResult
                mghFound = True

                if aMGH != eMGH:
                    aMGH = str(aMGH)
                    eMGH = str(eMGH)
                    AQResultDetails = mea.ResultDetails
                    source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text
                    AUD = AquariusConflictUploadDialog("DEBUG", None, eMGH + " m", aMGH + " m", "M.G.H", source, None, title="Upload Field Visit to Aquarius")

                    while val:
                        re = AUD.ShowModal()
                        if re == wx.ID_YES:

                            # Add mgh to field visit with measurement ID
                            mghResult.ResultID = mea.ResultID
                            dmeasurement.Results.FieldVisitResult.append(mghResult)
                            val = False
                            break
                        else:
                            print "Cancel"
                            val = False
                    AUD.Destroy()

            if not val:
                break


        # did not find mgh in the existing field visit, append to results list
        if not mghFound:
            mghResult.MeasurementID = 0
            dmeasurement.Results.FieldVisitResult.append(mghResult)

    else:
        warning = wx.MessageDialog(None, "No MGH will be uploaded", "Warning!", wx.OK| wx.ICON_EXCLAMATION)
        cont = warning.ShowModal()
        if cont == wx.ID_OK:
            warning.Destroy()

    #Discharge
    if str(EHSN.disMeasManager.dischCtrl).strip() != "":

        eQR = float(EHSN.disMeasManager.dischCtrl)
        ParamID = 'QR'

        # If we found the qr in the field visit, then we ask and the user will choose
        # If we could not find the qr in the field visit, then we add automatically
        qrFound = False


        dischargeResults = aq.factory.create("ns0:FieldVisitResult")
        dischargeResults.MeasurementID = dmeasurement.MeasurementID
        dischargeResults.ResultID = 0
        dischargeResults.StartTime = meanTime
        # dischargeResults.EndTime = visit.EndDate
        dischargeResults.ParameterID = ParamID
        dischargeResults.UnitID = dischargeSensors[ParamID]
        dischargeResults.ObservedResult = float(EHSN.disMeasManager.dischCtrl)
        dischargeResults.Correction = 0.000
        dischargeResults.ResultType = resultType_All
        dischargeResults.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </DischargeResult>
    """
        for mea in dmeasurement.Results.FieldVisitResult:

            val = True


            if mea.ParameterID == ParamID:
                aQR = mea.ObservedResult
                AQResultDetails = mea.ResultDetails
                source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text

                qrFound = True

                if aQR != eQR:

                    if "import" in source.lower():
                        break
                    else:

                        aQR = str(aQR)
                        eQR = str(eQR)

                        AUD = AquariusConflictUploadDialog("DEBUG", None, eQR + u" m\N{SUPERSCRIPT THREE}/s", aQR + u" m\N{SUPERSCRIPT THREE}/s", "Discharge", source, None, title="Upload Field Visit to Aquarius")

                        while val:
                            re = AUD.ShowModal()
                            # Overwrite
                            if re == wx.ID_YES:

                                # Add discharge to field visit with measurement ID
                                dischargeResults.ResultID = mea.ResultID
                                dmeasurement.Results.FieldVisitResult.append(dischargeResults)
                                val = False
                                break
                            else:
                                val = False
                                break
                        AUD.Destroy()
            if not val:
                break

        # did not find q in the existing field visit, append to results list
        if not qrFound:
            dischargeResults.MeasurementID = 0
            dmeasurement.Results.FieldVisitResult.append(dischargeResults)


    #River X Area
    if str(EHSN.disMeasManager.areaCtrl).strip() != "":
        eAR = float(EHSN.disMeasManager.areaCtrl)


        # If we found the qr in the field visit, then we ask and the user will choose
        # If we could not find the qr in the field visit, then we add automatically
        areaFound = False
        ParamID = 'RiverSectionArea'

        areaResult = aq.factory.create("ns0:FieldVisitResult")
        areaResult.MeasurementID = dmeasurement.MeasurementID
        areaResult.ResultID = 0
        areaResult.StartTime = meanTime
        # areaResult.EndTime = visit.EndDate
        areaResult.ParameterID = ParamID
        areaResult.UnitID = dischargeSensors[ParamID]
        areaResult.ObservedResult = float(EHSN.disMeasManager.areaCtrl)
        areaResult.Correction = 0.000
        areaResult.ResultType = resultType_RC
        areaResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </DischargeResult>
    """
        for mea in dmeasurement.Results.FieldVisitResult:

            val = True


            if mea.ParameterID == ParamID:
                aAR = mea.ObservedResult
                AQResultDetails = mea.ResultDetails
                source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text

                areaFound = True

                if aAR != eAR:

                    if "import" in source.lower():
                        break
                    else:

                        aAR = str(aAR)
                        eAR = str(eAR)

                        AUD = AquariusConflictUploadDialog("DEBUG", None, eAR + u" m\N{SUPERSCRIPT TWO}", aAR + u" m\N{SUPERSCRIPT TWO}", "Area", source, None, title="Upload Field Visit to Aquarius")

                        while val:
                            re = AUD.ShowModal()
                            if re == wx.ID_YES:

                                # Add mgh to field visit with measurement ID
                                areaResult.ResultID = mea.ResultID
                                dmeasurement.Results.FieldVisitResult.append(areaResult)
                                val = False
                                break
                            else:
                                val = False
                                break
                        AUD.Destroy()
            if not val:
                break

        # did not find q in the existing field visit, append to results list
        if not areaFound:
            areaResult.MeasurementID = 0
            dmeasurement.Results.FieldVisitResult.append(areaResult)







    #River X Width
    if str(EHSN.disMeasManager.widthCtrl).strip() != "":
        ParamID = 'RiverSectionWidth'
        eWidth = float(EHSN.disMeasManager.widthCtrl)


        # If we found the qr in the field visit, then we ask and the user will choose
        # If we could not find the qr in the field visit, then we add automatically
        widthFound = False

        widthResult = aq.factory.create("ns0:FieldVisitResult")
        widthResult.MeasurementID = dmeasurement.MeasurementID
        widthResult.ResultID = 0
        widthResult.StartTime = meanTime
        # widthResult.EndTime = visit.EndDate
        widthResult.ParameterID = ParamID
        widthResult.UnitID = dischargeSensors[ParamID]
        widthResult.ObservedResult = float(EHSN.disMeasManager.widthCtrl)
        widthResult.Correction = 0.000
        widthResult.ResultType = resultType_RC
        widthResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </DischargeResult>
    """
        for mea in dmeasurement.Results.FieldVisitResult:

            val = True


            if mea.ParameterID == ParamID:
                aWidth = mea.ObservedResult
                AQResultDetails = mea.ResultDetails
                source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text

                widthFound = True

                if aWidth != eWidth:

                    if "import" in source.lower():
                        break
                    else:

                        aWidth = str(aWidth)
                        eWidth = str(eWidth)

                        AUD = AquariusConflictUploadDialog("DEBUG", None, eWidth + " m", aWidth + " m", "Width", source, None, title="Upload Field Visit to Aquarius")

                        while val:
                            re = AUD.ShowModal()
                            if re == wx.ID_YES:

                                # Add mgh to field visit with measurement ID
                                widthResult.ResultID = mea.ResultID
                                dmeasurement.Results.FieldVisitResult.append(widthResult)
                                val = False
                                break
                            else:
                                val = False
                                break
                        AUD.Destroy()
            if not val:
                break

        # did not find q in the existing field visit, append to results list
        if not widthFound:
            widthResult.MeasurementID = 0
            dmeasurement.Results.FieldVisitResult.append(widthResult)




    #Water Velocity
    if str(EHSN.disMeasManager.meanVelCtrl).strip() != "":
        ParamID = 'WV'
        eWV = float(EHSN.disMeasManager.meanVelCtrl)


        # If we found the qr in the field visit, then we ask and the user will choose
        # If we could not find the qr in the field visit, then we add automatically
        wvFound = False

        waterVelResult = aq.factory.create("ns0:FieldVisitResult")
        waterVelResult.MeasurementID = dmeasurement.MeasurementID
        waterVelResult.ResultID = 0
        waterVelResult.StartTime = meanTime
        # waterVelResult.EndTime = visit.EndDate
        waterVelResult.ParameterID = ParamID
        waterVelResult.UnitID = dischargeSensors[ParamID]
        waterVelResult.ObservedResult = float(EHSN.disMeasManager.meanVelCtrl)
        waterVelResult.Correction = 0.000
        waterVelResult.ResultType = resultType_RC
        waterVelResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </DischargeResult>
    """



        for mea in dmeasurement.Results.FieldVisitResult:

            val = True


            if mea.ParameterID == ParamID:
                aWV = mea.ObservedResult
                AQResultDetails = mea.ResultDetails
                source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text

                wvFound = True

                if aWV != eWV:

                    if "import" in source.lower():
                        break
                    else:

                        aWV = str(aWV)
                        eWV = str(eWV)

                        AUD = AquariusConflictUploadDialog("DEBUG", None, eWV + " m/s", aWV + " m/s", "Water Velocity", source, None, title="Upload Field Visit to Aquarius")

                        while val:
                            re = AUD.ShowModal()
                            if re == wx.ID_YES:

                                # Add mgh to field visit with measurement ID
                                waterVelResult.ResultID = mea.ResultID
                                dmeasurement.Results.FieldVisitResult.append(waterVelResult)
                                val = False
                                break
                            else:
                                val = False
                                break
                        AUD.Destroy()
            if not val:
                break

        # did not find q in the existing field visit, append to results list
        if not wvFound:
            waterVelResult.MeasurementID = 0
            dmeasurement.Results.FieldVisitResult.append(waterVelResult)



    # #Water Temperature
    # if not EHSN.disMeasManager.IsEmpty():
    #     if str(EHSN.disMeasManager.waterTempCtrl).strip() != "":
    #         ParamID = 'TW'
    #         eTW = float(EHSN.disMeasManager.waterTempCtrl)


    #         # If we found the qr in the field visit, then we ask and the user will choose
    #         # If we could not find the qr in the field visit, then we add automatically
    #         twFound = False
    #         waterTempResult = aq.factory.create("ns0:FieldVisitResult")
    #         waterTempResult.MeasurementID = dmeasurement.MeasurementID
    #         waterTempResult.ResultID = 0
    #         waterTempResult.StartTime = meanTime
    #         # waterTempResult.EndTime = visit.EndDate
    #         waterTempResult.ParameterID = ParamID
    #         waterTempResult.UnitID = dischargeSensors[ParamID]
    #         waterTempResult.ObservedResult = float(EHSN.disMeasManager.waterTempCtrl)
    #         waterTempResult.Correction = 0.000
    #         waterTempResult.ResultType = resultType_RC
    #         waterTempResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    #     <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #       <Party>""" + cdataParty + """</Party>
    #       <Source>
    #         <SourceType>
    #           <Id>Import</Id>
    #           <DisplayName>""" + src + """</DisplayName>
    #         </SourceType>
    #         <DisplayName>""" + src + """</DisplayName>
    #         <Sequence>1</Sequence>
    #       </Source>
    #     </DischargeResult>
    #     """


    #         for mea in dmeasurement.Results.FieldVisitResult:

    #             val = True


    #             if mea.ParameterID == ParamID:
    #                 aTW = mea.ObservedResult
    #                 AQResultDetails = mea.ResultDetails
    #                 source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text

    #                 twFound = True

    #                 if aTW != eTW:

    #                     if "import" in source.lower():
    #                         break
    #                     else:

    #                         aTW = str(aTW)
    #                         eTW = str(eTW)

    #                         AUD = AquariusConflictUploadDialog("DEBUG", None, eTW + u" \N{DEGREE SIGN}C", aTW + u" \N{DEGREE SIGN}C", "Water Temp", source, None, title="Upload Field Visit to Aquarius")

    #                         while val:
    #                             re = AUD.ShowModal()
    #                             if re == wx.ID_YES:

    #                                 # Add mgh to field visit with measurement ID
    #                                 waterTempResult.ResultID = mea.ResultID
    #                                 dmeasurement.Results.FieldVisitResult.append(waterTempResult)
    #                                 val = False
    #                                 break
    #                             else:
    #                                 val = False
    #                                 break
    #                         AUD.Destroy()
    #             if not val:
    #                 break

    #         # did not find q in the existing field visit, append to results list
    #         if not twFound:
    #             waterTempResult.MeasurementID = 0
    #             dmeasurement.Results.FieldVisitResult.append(waterTempResult)



    #Recorded Sensor Values
    #Loop through each sensor val and check if it is a discharge measurement
    # startTime = datetime.datetime.strptime(str(EHSN.measResultsManager.timeCtrl), "%H:%M")
    # startTime = startTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
###########################################################################################
    # for index, sensorRefEntry in enumerate(EHSN.measResultsManager.sensorRefEntries):

    #     #Is this a "valid" measurement result that can be uploaded to Aquarius?
    #     if EHSN.measResultsManager.sensorRef.has_key(sensorRefEntry.GetValue().strip()):

    #         #Is this a discharge measurement?
    #         if dischargeSensors.has_key(EHSN.measResultsManager.sensorRef[sensorRefEntry.GetValue()]):
    #             ParamID = EHSN.measResultsManager.sensorRef[sensorRefEntry.GetValue()]

    #             observed = 0.000 if EHSN.measResultsManager.observedVals[index].GetValue() == "" else float(EHSN.measResultsManager.observedVals[index].GetValue())
    #             logger = "" if EHSN.measResultsManager.sensorVals[index].GetValue() == "" else str(EHSN.measResultsManager.sensorVals[index].GetValue())

    #             resultVal = aq.factory.create("ns0:FieldVisitResult")
    #             resultVal.MeasurementID = dmeasurement.MeasurementID
    #             resultVal.ResultID = 0
    #             resultVal.StartTime = startTime
    #             # resultVal.EndTime = visit.EndDate
    #             resultVal.ParameterID = ParamID
    #             resultVal.UnitID = dischargeSensors[ParamID]
    #             resultVal.ObservedResult = observed
    #             resultVal.Correction = 0.000
    #             resultVal.ResultType = resultType
    #             resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    #         <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #           <Party>""" + cdataParty + """</Party>
    #           <Source>
    #             <SourceType>
    #               <Id>Import</Id>
    #               <DisplayName>""" + src + """</DisplayName>
    #             </SourceType>
    #             <DisplayName>""" + src + """</DisplayName>
    #             <Sequence>1</Sequence>
    #           </Source>""" + ("" if logger == "" else """\n<LoggerValue>""" + logger + """</LoggerValue>\n""") + """
    #         </DischargeResult>"""
    #             dmeasurement.Results.FieldVisitResult.append(resultVal)

###########################################################################################
    if len(dmeasurement.Results.FieldVisitResult) <= 0 and dmeasurement.Remarks == "":
        return None

    # if MEASUREMENT_ID != 0:
    #     if len(dmeasurement.Results.FieldVisitResult) == len(MEASUREMENT.Results.FieldVisitResult):
    #         dmeasurement.MeasurementID = -dmeasurement.MeasurementID

    # When merging, make sure time is same for all measurements within discharge activity
    if dischargeResult is not None:
        for i in range(len(dmeasurement.Results.FieldVisitResult)):
            dmeasurement.Results.FieldVisitResult[i].StartTime = meanTime
            dmeasurement.Results.FieldVisitResult.append(dmeasurement.Results.FieldVisitResult[i])
            if i==len(dmeasurement.Results.FieldVisitResult)-1:
                break

    return dmeasurement


# Creates a FieldVisitMeasurement with type WscFvtPlugin_ActivityTypeStage
def CreateStageMeasurements(mode, src, aq, visit, MEASUREMENT, EHSN, dateInfo, fvStartDate, server):
    if mode == "DEBUG":
        print "Creating Stage Measurements"

    # # Used to replace / modify existing Measurements
    # if MEASUREMENT == 0:
    #     MEASUREMENT_ID = 0
    # else:
    #     MEASUREMENT_ID = MEASUREMENT.MeasurementID

    bms = GetBM(EHSN.genInfoManager.stnNumCmbo, aq, server)
    print bms

    # Set to 0 for new measurement
    MEASUREMENT_ID = 0
    if EHSN.disMeasManager.IsEmpty():
        meanTime = EHSN.stageMeasManager.CalculteMeanTime()

    else:
        meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"
    # meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"
    meanTime = datetime.datetime.strptime(meanTime, "%H:%M")
    meanTime = meanTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
    meanTime = str(meanTime.isoformat()) + isoTail

    # create stage measurement
    smeasurement = aq.factory.create("ns0:FieldVisitMeasurement")
    smeasurement.ApprovalLevelID = 3
    smeasurement.MeasurementID = MEASUREMENT_ID
    smeasurement.FieldVisitID = visit.FieldVisitID
    smeasurement.MeasurementType = "WscFvtPlugin_ActivityTypeStage"
    smeasurement.MeasurementTime = fvStartDate
    smeasurement.MeasurementEndTime = fvStartDate
    smeasurement.LastModified = datetime.datetime(0001, 01, 01)
    smeasurement.Remarks = EHSN.instrDepManager.stageRemarksCtrl
    smeasurement.Remarks += "" if smeasurement.Remarks == "" else "\n"
    smeasurement.Remarks += "" if EHSN.envCondManager.levelsCtrl == "" else "Levels: " + str(EHSN.envCondManager.levelsCtrl)

    surgeComments = EHSN.waterLevelRunManager.surgeValSizer.GetChildren()
    times = EHSN.waterLevelRunManager.timeValSizer.GetChildren()
    for i in range(len(surgeComments)):
        smeasurement.Remarks += "" if surgeComments[i].Window.GetValue() == "" else "\nSurge (+/- m)/Comment: @" + times[i].Window.GetValue() + "=" + surgeComments[i].Window.GetValue()

    smeasurement.Results = aq.factory.create("ns0:ArrayOfFieldVisitResult")
    smeasurement.Results.FieldVisitResult = []

    # if MEASUREMENT_ID != 0:
    #     if MEASUREMENT.Results is not None:
    #         for i in range(len(MEASUREMENT.Results[0])):
    #             MEASUREMENT.Results.FieldVisitResult[i].ResultID = -MEASUREMENT.Results.FieldVisitResult[i].ResultID
    #             smeasurement.Results.FieldVisitResult.append(MEASUREMENT.Results.FieldVisitResult[i])


    hasHG = False
    for row in range(len(EHSN.stageMeasManager.timeValSizer.GetChildren())):
        if EHSN.stageMeasManager.GetHGVal(row) != "":
            hasHG = True
            break

    #Recorded Sensor Values
    #Loop through each sensor val and check if it is a discharge measurement

    for row in range(len(EHSN.stageMeasManager.timeValSizer.GetChildren())):
            smeasurement.Remarks += "" if EHSN.stageMeasManager.GetHG2Val(row) == ""\
            else "\n@" + str(EHSN.stageMeasManager.GetTimeVal(row))\
             + "\tHG2: " + EHSN.stageMeasManager.GetHG2Val(row)
            ParamID = 'HG'

            # variables for storing data
            hgs = []
            refs = []
            hg2s = []
            refLeftOrRight = []

            # checks if the row has any data
            hasData = False

            if EHSN.stageMeasManager.GetHGVal(row) != "":
                hgs.append(EHSN.stageMeasManager.GetHGVal(row))
                hasData = True
            if EHSN.stageMeasManager.GetHG2Val(row) != "":
                hg2s.append(EHSN.stageMeasManager.GetHG2Val(row))
                hasData = True
            if EHSN.stageMeasManager.GetWLSubSizerLVal(row) != "":
                refs.append(EHSN.stageMeasManager.GetWLSubSizerLVal(row))
                refLeftOrRight.append('left')
                hasData = True
            if EHSN.stageMeasManager.GetWLSubSizerRVal(row) != "":
                refs.append(EHSN.stageMeasManager.GetWLSubSizerRVal(row))
                refLeftOrRight.append('right')
                hasData = True
            if EHSN.stageMeasManager.GetSrcAppSizerVal(row) != "":
                smeasurement.Remarks += "\n@" + EHSN.stageMeasManager.GetTimeVal(row) + "\t" + EHSN.stageMeasManager.GetSrcAppSizerVal(row)
                hasData = True

            if not hasData:
                print "Row %d has no data, skipping upload..." % (row + 1)
                continue

            # get time value. Important to do this after checking to see if we have data
            # since otherwise the time field may be empty
            measTime = datetime.datetime.strptime(str(EHSN.stageMeasManager.GetTimeVal(row)), "%H:%M")
            measTime = measTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
            measTime = str(measTime.isoformat()) + isoTail

            #if there is any HG value, HG2 will not be used
            if hasHG:
                if len(refs) == 0 and len(hgs) != 0:

                    for hg in hgs:
                        # correction = EHSN.stageMeasManager.GCHG
                        correction = 0.000 # if correction == '' else float(correction)

                        resultVal = aq.factory.create("ns0:FieldVisitResult")
                        #############for 3.10#########################
                        ##Need Logger here
                        resultVal.BenchmarkOrRefPointName = ""
                        if EHSN.stageMeasManager.GCHG!="":
                            correction = EHSN.stageMeasManager.GCHG
                        #if "*" in resultVal.BenchmarkOrRefPointName:
                        #    resultVal.BenchmarkOrRefPointName = resultVal.BenchmarkOrRefPointName.replace("*","")
                        resultVal.MeasurementID = smeasurement.MeasurementID
                        resultVal.ResultID = 0
                        resultVal.StartTime = measTime
                        # resultVal.EndTime = visit.EndDate
                        resultVal.ParameterID = ParamID
                        resultVal.UnitID = stageSensors[ParamID]
                        resultVal.ObservedResult = hg
                        resultVal.Correction = correction
                        resultVal.ResultType = resultType_TS
                        cdataParty = repChar(visit.Party)
                        resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
                        <StageResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <Party>""" + cdataParty + """</Party>
                          <Source>
                            <SourceType>
                              <Id>Import</Id>
                              <DisplayName>""" + src + """</DisplayName>
                            </SourceType>
                            <DisplayName>""" + src + """</DisplayName>
                            <Sequence>1</Sequence>
                          </Source>
                          <ControlConditions>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlConditions>""" \
                           + """\n<LoggerValue>""" + hg + """</LoggerValue>""" + """
                          <IsLoggerRefSelected>false</IsLoggerRefSelected>
                        </StageResult>
                        """

                        # if len(hgs) != 0:
                        smeasurement.Results.FieldVisitResult.append(resultVal)
                        print "append ", measTime
                        smeasurement.Remarks += "The Logger only stage value @" + measTime[11:16] + " was also used as observed value.\n"



                elif len(hgs) != 0 and len(refs) != 0:

                    for hg in hgs:
                        for ref in refs:


                            # correction = EHSN.stageMeasManager.GCHG
                            correction = 0.000 # if correction == '' else float(correction)

                            resultVal = aq.factory.create("ns0:FieldVisitResult")
                            #############for 3.10#########################
                            if refLeftOrRight[refs.index(ref)] == 'left':
                                bm = EHSN.stageMeasManager.bmLeft
                                if EHSN.stageMeasManager.GCWLRefL!="":
                                    correction = EHSN.stageMeasManager.GCWLRefL
                            else:
                                bm = EHSN.stageMeasManager.bmRight
                                if EHSN.stageMeasManager.GCWLRefR!="":
                                    correction = EHSN.stageMeasManager.GCWLRefR
                            if "*" in bm:
                                bm = bm.replace("*","")
                            if bm in bms:
                                resultVal.BenchmarkOrRefPointName = bm
                            resultVal.MeasurementID = smeasurement.MeasurementID
                            resultVal.ResultID = 0
                            resultVal.StartTime = measTime
                            # resultVal.EndTime = visit.EndDate
                            resultVal.ParameterID = ParamID
                            resultVal.UnitID = stageSensors[ParamID]
                            resultVal.ObservedResult = ref
                            resultVal.Correction = correction
                            resultVal.ResultType = resultType_TS
                            cdataParty = repChar(visit.Party)


                            resultVal.ResultDetails = """<?xml version="1.0" encoding="UTF-8"?>
                        <StageResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <Party>""" + cdataParty + """</Party>
                          <Source>
                            <SourceType>
                              <Id>Import</Id>
                              <DisplayName>""" + src + """</DisplayName>
                            </SourceType>
                            <DisplayName>""" + src + """</DisplayName>
                            <Sequence>1</Sequence>
                          </Source>
                          <ControlConditions>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlConditions>""" \
                           + """\n<LoggerValue>""" + hg + """</LoggerValue>""" + """
                          <IsLoggerRefSelected>false</IsLoggerRefSelected>
                        </StageResult>
                        """

                            if len(refs) != 0:# and len(hgs) != 0:
                                smeasurement.Results.FieldVisitResult.append(resultVal)
                                print "append ", measTime

                else:

                    for ref in refs:

                        # correction = EHSN.stageMeasManager.GCHG
                        correction = 0.000 # if correction == '' else float(correction)

                        resultVal = aq.factory.create("ns0:FieldVisitResult")
                        #############for 3.10#########################
                        if refLeftOrRight[refs.index(ref)] == 'left':
                            bm = EHSN.stageMeasManager.bmLeft
                            if EHSN.stageMeasManager.GCWLRefL!="":
                                correction = EHSN.stageMeasManager.GCWLRefL
                        else:
                            bm = EHSN.stageMeasManager.bmRight
                            if EHSN.stageMeasManager.GCWLRefR!="":
                                correction = EHSN.stageMeasManager.GCWLRefR
                        if "*" in bm:
                            bm = bm.replace("*","")
                        if bm in bms:
                            resultVal.BenchmarkOrRefPointName = bm
                        ################################################
                        resultVal.MeasurementID = smeasurement.MeasurementID
                        resultVal.ResultID = 0
                        resultVal.StartTime = measTime
                        # resultVal.EndTime = visit.EndDate
                        resultVal.ParameterID = ParamID
                        resultVal.UnitID = stageSensors[ParamID]
                        resultVal.ObservedResult = ref
                        resultVal.Correction = correction
                        resultVal.ResultType = resultType_TS
                        cdataParty = repChar(visit.Party)
                        resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
                        <StageResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <Party>""" + cdataParty + """</Party>
                          <Source>
                            <SourceType>
                              <Id>Import</Id>
                              <DisplayName>""" + src + """</DisplayName>
                            </SourceType>
                            <DisplayName>""" + src + """</DisplayName>
                            <Sequence>1</Sequence>
                          </Source>
                          <ControlConditions>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlConditions>""" \
                           + """
                          <IsLoggerRefSelected>false</IsLoggerRefSelected>
                        </StageResult>
                        """


                        if len(refs) != 0:
                            smeasurement.Results.FieldVisitResult.append(resultVal)
                            print "append ", measTime




            #if no HG value then treat HG2 as HG
            else:
                if len(refs) == 0 and len(hg2s) != 0:

                    for hg2 in hg2s:
                        # correction = EHSN.stageMeasManager.GCHG
                        correction = 0.000 # if correction == '' else float(correction)

                        resultVal = aq.factory.create("ns0:FieldVisitResult")
                        #############for 3.10#########################
                        ##Need Logger here
                        resultVal.BenchmarkOrRefPointName = ""
                        if EHSN.stageMeasManager.GCHG2!="":
                            correction = EHSN.stageMeasManager.GCHG2
                        #if "*" in resultVal.BenchmarkOrRefPointName:
                        #    resultVal.BenchmarkOrRefPointName = resultVal.BenchmarkOrRefPointName.replace("*","")
                        resultVal.MeasurementID = smeasurement.MeasurementID
                        resultVal.ResultID = 0
                        resultVal.StartTime = measTime
                        # resultVal.EndTime = visit.EndDate
                        resultVal.ParameterID = ParamID
                        resultVal.UnitID = stageSensors[ParamID]
                        resultVal.ObservedResult = hg2
                        resultVal.Correction = correction
                        resultVal.ResultType = resultType_TS
                        cdataParty = repChar(visit.Party)
                        resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
                        <StageResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <Party>""" + cdataParty + """</Party>
                          <Source>
                            <SourceType>
                              <Id>Import</Id>
                              <DisplayName>""" + src + """</DisplayName>
                            </SourceType>
                            <DisplayName>""" + src + """</DisplayName>
                            <Sequence>1</Sequence>
                          </Source>
                          <ControlConditions>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlConditions>""" \
                           + """\n<LoggerValue>""" + hg2 + """</LoggerValue>""" + """
                          <IsLoggerRefSelected>false</IsLoggerRefSelected>
                        </StageResult>
                        """

                        if len(hg2s) != 0:
                            smeasurement.Results.FieldVisitResult.append(resultVal)
                            print "append ", measTime


                elif len(refs) != 0 and len(hg2s) != 0:
                    for hg2 in hg2s:
                        for ref in refs:


                            # correction = EHSN.stageMeasManager.GCHG
                            correction = 0.000 # if correction == '' else float(correction)

                            resultVal = aq.factory.create("ns0:FieldVisitResult")
                            #############for 3.10#########################
                            if refLeftOrRight[refs.index(ref)] == 'left':
                                bm = EHSN.stageMeasManager.bmLeft
                                if EHSN.stageMeasManager.GCWLRefL!="":
                                    correction = EHSN.stageMeasManager.GCWLRefL
                            else:
                                bm = EHSN.stageMeasManager.bmRight
                                if EHSN.stageMeasManager.GCWLRefR!="":
                                    correction = EHSN.stageMeasManager.GCWLRefR
                            if "*" in bm:
                                bm = bm.replace("*","")
                            if bm in bms:
                                resultVal.BenchmarkOrRefPointName = bm
                            resultVal.MeasurementID = smeasurement.MeasurementID
                            resultVal.ResultID = 0
                            resultVal.StartTime = measTime
                            # resultVal.EndTime = visit.EndDate
                            resultVal.ParameterID = ParamID
                            resultVal.UnitID = stageSensors[ParamID]
                            resultVal.ObservedResult = ref
                            resultVal.Correction = correction
                            resultVal.ResultType = resultType_TS
                            cdataParty = repChar(visit.Party)


                            resultVal.ResultDetails = """<?xml version="1.0" encoding="UTF-8"?>
                        <StageResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <Party>""" + cdataParty + """</Party>
                          <Source>
                            <SourceType>
                              <Id>Import</Id>
                              <DisplayName>""" + src + """</DisplayName>
                            </SourceType>
                            <DisplayName>""" + src + """</DisplayName>
                            <Sequence>1</Sequence>
                          </Source>
                          <ControlConditions>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlConditions>""" \
                           + """\n<LoggerValue>""" + hg2 + """</LoggerValue>""" + """
                          <IsLoggerRefSelected>false</IsLoggerRefSelected>
                        </StageResult>
                        """

                            if len(hg2s) != 0 and len(refs) != 0:
                                smeasurement.Results.FieldVisitResult.append(resultVal)
                                print "append ", measTime

                else:

                    for ref in refs:

                        # correction = EHSN.stageMeasManager.GCHG
                        correction = 0.000 # if correction == '' else float(correction)

                        resultVal = aq.factory.create("ns0:FieldVisitResult")
                        #############for 3.10#########################
                        if refLeftOrRight[refs.index(ref)] == 'left':
                            bm = EHSN.stageMeasManager.bmLeft
                            if EHSN.stageMeasManager.GCWLRefL!="":
                                correction = EHSN.stageMeasManager.GCWLRefL
                        else:
                            bm = EHSN.stageMeasManager.bmRight
                            if EHSN.stageMeasManager.GCWLRefR!="":
                                correction = EHSN.stageMeasManager.GCWLRefR
                        if "*" in bm:
                            bm = bm.replace("*","")
                        if bm in bms:
                            resultVal.BenchmarkOrRefPointName = bm
                        ################################################
                        resultVal.MeasurementID = smeasurement.MeasurementID
                        resultVal.ResultID = 0
                        resultVal.StartTime = measTime
                        # resultVal.EndTime = visit.EndDate
                        resultVal.ParameterID = ParamID
                        resultVal.UnitID = stageSensors[ParamID]
                        resultVal.ObservedResult = ref
                        resultVal.Correction = correction
                        resultVal.ResultType = resultType_TS
                        cdataParty = repChar(visit.Party)
                        resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
                        <StageResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <Party>""" + cdataParty + """</Party>
                          <Source>
                            <SourceType>
                              <Id>Import</Id>
                              <DisplayName>""" + src + """</DisplayName>
                            </SourceType>
                            <DisplayName>""" + src + """</DisplayName>
                            <Sequence>1</Sequence>
                          </Source>
                          <ControlConditions>""" + str(EHSN.instrDepManager.controlConditionCmbo) + """</ControlConditions>""" \
                           + """
                          <IsLoggerRefSelected>false</IsLoggerRefSelected>
                        </StageResult>
                        """


                        if len(refs) != 0:
                            smeasurement.Results.FieldVisitResult.append(resultVal)
                            print "append ", measTime

    # check if we actually have any data to avoid uploading empty entry
    if len(smeasurement.Results.FieldVisitResult) == 0:
        return None
    # Sort by time
    smeasurement.Results.FieldVisitResult.sort(key=lambda f:f.StartTime)
    return smeasurement


# Creates a FieldVisitMeasurement with type WscFvtPlugin_ActivityTypeStationHealth
def CreateStationHealthMeasurements(mode, src, aq, visit, MEASUREMENT, EHSN, dateInfo, fvStartDate):
    if mode == "DEBUG":
        print "Creating Station Health Measurements"

    # # Used to replace / modify existing Measurements
    # if MEASUREMENT == 0:
    #     MEASUREMENT_ID = 0
    # else:
    #     MEASUREMENT_ID = MEASUREMENT.MeasurementID



    if EHSN.disMeasManager.IsEmpty():
        meanTime = EHSN.stageMeasManager.CalculteMeanTime()
    else:
        meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"

    meanTime = datetime.datetime.strptime(meanTime, "%H:%M")
    meanTime = meanTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
    meanTime = str(meanTime.isoformat()) + isoTail
    # Set to 0 for new measurement
    MEASUREMENT_ID = 0

    shmeasurement = aq.factory.create("ns0:FieldVisitMeasurement")
    shmeasurement.ApprovalLevelID = 3
    shmeasurement.MeasurementID = MEASUREMENT_ID
    shmeasurement.FieldVisitID = visit.FieldVisitID
    shmeasurement.MeasurementType = "WscFvtPlugin_ActivityTypeStationHealth"
    shmeasurement.MeasurementTime = fvStartDate
    shmeasurement.MeasurementEndTime = fvStartDate
    shmeasurement.LastModified = datetime.datetime(0001, 01, 01)
    shmeasurement.Remarks = ""
    shmeasurement.Remarks += EHSN.instrDepManager.stationHealthRemarksCtrl
    shmeasurement.Remarks += "\nIntake Flushed @" + EHSN.envCondManager.intakeTimeCtrl if EHSN.envCondManager.intakeCB else ""
    shmeasurement.Remarks += "\nOrifice Purged @" + EHSN.envCondManager.orificeTimeCtrl if EHSN.envCondManager.orificeCB else ""
    shmeasurement.Remarks += "\nDownloaded Program" if EHSN.envCondManager.programCB else ""
    shmeasurement.Remarks += "\nDownloaded Data" if EHSN.envCondManager.dataCB else ""

    if 'rot' in str(EHSN.envCondManager.bpmrotCmbo).lower() and str(EHSN.envCondManager.bpmrotCtrl) != "":
        shmeasurement.Remarks += "\nRot: " + str(EHSN.envCondManager.bpmrotCtrl)

    #logger time reset1
    if EHSN.measResultsManager.GetTime(5) != "" and EHSN.measResultsManager.GetTime(7) != "" \
                and EHSN.measResultsManager.loggerTimeCol1 != "":
        if shmeasurement.Remarks != "":
            shmeasurement.Remarks += "\n"
        shmeasurement.Remarks += EHSN.measResultsManager.loggerTimeCol1 + "\t" +  EHSN.measResultsManager.loggerTimeRemark1\
        + "\t" + EHSN.measResultsManager.GetTime(5) + "\t" + EHSN.measResultsManager.GetTime(7)
    #logger time reset2
    if EHSN.measResultsManager.GetTime(6) != "" and EHSN.measResultsManager.GetTime(8) != "" \
                and EHSN.measResultsManager.loggerTimeCol2 != "":
        if shmeasurement.Remarks != "":
            shmeasurement.Remarks += "\n"
        shmeasurement.Remarks += EHSN.measResultsManager.loggerTimeCol2 + "\t" +  EHSN.measResultsManager.loggerTimeRemark2\
        + "\t" + EHSN.measResultsManager.GetTime(6) + "\t" + EHSN.measResultsManager.GetTime(8)

    shmeasurement.Results = aq.factory.create("ns0:ArrayOfFieldVisitResult")
    shmeasurement.Results.FieldVisitResult = []

    # if MEASUREMENT_ID != 0:
    #     if MEASUREMENT.Results is not None:
    #         for i in range(len(MEASUREMENT.Results[0])):
    #             MEASUREMENT.Results.FieldVisitResult[i].ResultID = -MEASUREMENT.Results.FieldVisitResult[i].ResultID
    #             shmeasurement.Results.FieldVisitResult.append(MEASUREMENT.Results.FieldVisitResult[i])




    if str(EHSN.envCondManager.gasSysCtrl) != "":
        ParamID = 'YP'

        tankPressureResult = aq.factory.create("ns0:FieldVisitResult")
        tankPressureResult.MeasurementID = shmeasurement.MeasurementID
        tankPressureResult.ResultID = 0
        tankPressureResult.StartTime = meanTime
        # tankPressureResult.EndTime = visit.EndDate
        tankPressureResult.ParameterID = ParamID
        tankPressureResult.UnitID = stationhealthSensors[ParamID]
        tankPressureResult.ResultType = resultType_NA
        tankPressureResult.ObservedResult = float(EHSN.envCondManager.gasSysCtrl)
        tankPressureResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        tankPressureResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <StationHealthResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </StationHealthResult>
    """
        shmeasurement.Results.FieldVisitResult.append(tankPressureResult)




    if str(EHSN.envCondManager.feedCtrl) != "":
        ParamID = 'YP2'

        feedResult = aq.factory.create("ns0:FieldVisitResult")
        feedResult.MeasurementID = shmeasurement.MeasurementID
        feedResult.ResultID = 0
        feedResult.StartTime = meanTime
        # feedResult.EndTime = visit.EndDate
        feedResult.ParameterID = ParamID
        feedResult.UnitID = stationhealthSensors[ParamID]
        feedResult.ResultType = resultType_NA
        feedResult.ObservedResult = float(EHSN.envCondManager.feedCtrl)
        feedResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        feedResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <StationHealthResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </StationHealthResult>
    """
        shmeasurement.Results.FieldVisitResult.append(feedResult)



    if 'bpm' in str(EHSN.envCondManager.bpmrotCmbo).lower() and str(EHSN.envCondManager.bpmrotCtrl) != "":
        ParamID = 'N2BubbleRate'

        bubbleRateResult = aq.factory.create("ns0:FieldVisitResult")
        bubbleRateResult.MeasurementID = shmeasurement.MeasurementID
        bubbleRateResult.ResultID = 0
        bubbleRateResult.StartTime = meanTime
        # bubbleRateResult.EndTime = visit.EndDate
        bubbleRateResult.ParameterID = ParamID
        bubbleRateResult.UnitID = stationhealthSensors[ParamID]
        bubbleRateResult.ResultType = resultType_NA
        bubbleRateResult.ObservedResult = float(EHSN.envCondManager.bpmrotCtrl)
        bubbleRateResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        bubbleRateResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <StationHealthResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </StationHealthResult>
    """
        shmeasurement.Results.FieldVisitResult.append(bubbleRateResult)

    if str(EHSN.envCondManager.batteryCtrl) != "":
        ParamID = 'VB'

        voltageResult = aq.factory.create("ns0:FieldVisitResult")
        voltageResult.MeasurementID = shmeasurement.MeasurementID
        voltageResult.ResultID = 0
        voltageResult.StartTime = meanTime
        # voltageResult.EndTime = visit.EndDate
        voltageResult.ParameterID = ParamID
        voltageResult.UnitID = stationhealthSensors[ParamID]
        voltageResult.ResultType = resultType_NA
        voltageResult.ObservedResult = float(EHSN.envCondManager.batteryCtrl)
        voltageResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        voltageResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <StationHealthResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </StationHealthResult>
    """
        shmeasurement.Results.FieldVisitResult.append(voltageResult)

    #Recorded Sensor Values
    #Loop through each sensor val and check if it is a discharge measurement
    for index, sensorRefEntry in enumerate(EHSN.measResultsManager.sensorRefEntries):
        #Note the start time from the timectrl
        time = EHSN.measResultsManager.GetTime(index)
        if time!="":
            startTime = datetime.datetime.strptime(str(EHSN.measResultsManager.GetTime(index)), "%H:%M")
            startTime = startTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
            startTime = str(startTime.isoformat()) + isoTail
        else:
            startTime=""
        # print sensorRefEntry.GetValue()
        # print '======'
        #Is this a "valid" measurement result that can be uploaded to Aquarius?
        if EHSN.measResultsManager.sensorRef.has_key(sensorRefEntry.GetValue().strip()):
            # print sensorRefEntry.GetValue()
            #Is this a discharge measurement?
            if stationhealthSensors.has_key(EHSN.measResultsManager.sensorRef[sensorRefEntry.GetValue()]):
                ParamID = EHSN.measResultsManager.sensorRef[sensorRefEntry.GetValue()]
                # print ParamID
                observed = 0.000 if EHSN.measResultsManager.observedVals[index].GetValue() == "" else float(EHSN.measResultsManager.observedVals[index].GetValue())
                logger = "" if EHSN.measResultsManager.sensorVals[index].GetValue() == "" else str(EHSN.measResultsManager.sensorVals[index].GetValue())

                resultVal = aq.factory.create("ns0:FieldVisitResult")
                resultVal.MeasurementID = shmeasurement.MeasurementID
                resultVal.ResultID = 0
                if startTime!="":
                    resultVal.StartTime = startTime
                # resultVal.EndTime = visit.EndDate
                resultVal.ParameterID = ParamID
                resultVal.UnitID = stationhealthSensors[ParamID]
                resultVal.ObservedResult = observed
                resultVal.Correction = 0.000
                resultVal.ResultType = resultType_NA
                cdataParty = repChar(visit.Party)
                resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
            <StationHealthResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
              <Party>""" + cdataParty + """</Party>
              <Source>
                <SourceType>
                  <Id>Import</Id>
                  <DisplayName>""" + src + """</DisplayName>
                </SourceType>
                <DisplayName>""" + src + """</DisplayName>
                <Sequence>1</Sequence>
              </Source>""" + \
              ("" if logger == "" else """\n<LoggerValue>""" + logger + """</LoggerValue>""") + """
            </StationHealthResult>
            """
                shmeasurement.Results.FieldVisitResult.append(resultVal)


    if len(shmeasurement.Results.FieldVisitResult) <= 0:
        return None

    # if MEASUREMENT_ID != 0:
    #     if len(shmeasurement.Results.FieldVisitResult) == len(MEASUREMENT.Results.FieldVisitResult):
    #         shmeasurement.MeasurementID = -shmeasurement.MeasurementID

    return shmeasurement


# Creates a FieldVisitMeasurement with type WscFvtPlugin_ActivityTypeEnvCondition
def CreateEnvironmentConditionsMeasurements(mode, src, aq, visit, MEASUREMENT, EHSN, dateInfo, fvStartDate):

    if mode == "DEBUG":
        print "Creating Environment Conditions Measurements"

    # # Used to replace / modify existing Measurements
    # if MEASUREMENT == 0:
    #     MEASUREMENT_ID = 0
    # else:
    #     MEASUREMENT_ID = MEASUREMENT.MeasurementID

    # Set to 0 for new measurement
    MEASUREMENT_ID = 0



    if EHSN.disMeasManager.IsEmpty():
        meanTime = EHSN.stageMeasManager.CalculteMeanTime()

    else:
        meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"
    meanTime = datetime.datetime.strptime(meanTime, "%H:%M")
    meanTime = meanTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
    meanTime = str(meanTime.isoformat()) + isoTail

    ecmeasurement = aq.factory.create("ns0:FieldVisitMeasurement")
    ecmeasurement.ApprovalLevelID = 3
    ecmeasurement.MeasurementID = MEASUREMENT_ID
    ecmeasurement.FieldVisitID = visit.FieldVisitID
    ecmeasurement.MeasurementType = "WscFvtPlugin_ActivityTypeEnvCondition"
    ecmeasurement.MeasurementTime = fvStartDate
    ecmeasurement.MeasurementEndTime = fvStartDate
    ecmeasurement.LastModified = datetime.datetime(0001, 01, 01)
    ecmeasurement.Remarks = ""
    if EHSN.envCondManager.cloudCoverCmbo != "":
        ecmeasurement.Remarks += "Cloud Cover: " + str(EHSN.envCondManager.cloudCoverCmbo) + "\n"
    if EHSN.envCondManager.precipCmbo != "":
        ecmeasurement.Remarks += "Precipitation: " + str(EHSN.envCondManager.precipCmbo) + "\n"
    if EHSN.envCondManager.windMagCmbo != "":
        ecmeasurement.Remarks += "Wind Magnitude: " + str(EHSN.envCondManager.windMagCmbo) + "\n"
    if EHSN.envCondManager.windDirCmbo != "":
        ecmeasurement.Remarks += "Wind Direction: " + str(EHSN.envCondManager.windDirCmbo) + "\n"

    # ecmeasurement.Remarks += EHSN.instrDepManager.controlRemarksCtrl


    ecmeasurement.Results = aq.factory.create("ns0:ArrayOfFieldVisitResult")
    ecmeasurement.Results.FieldVisitResult = []

    # if MEASUREMENT_ID != 0:
    #     if MEASUREMENT.Results is not None:
    #         for i in range(len(MEASUREMENT.Results[0])):
    #             MEASUREMENT.Results.FieldVisitResult[i].ResultID = -MEASUREMENT.Results.FieldVisitResult[i].ResultID
    #             ecmeasurement.Results.FieldVisitResult.append(MEASUREMENT.Results.FieldVisitResult[i])




    #Air Temp
    if str(EHSN.disMeasManager.airTempCtrl) != "":
        ParamID = 'TA'

        airTempResult = aq.factory.create("ns0:FieldVisitResult")
        airTempResult.MeasurementID = ecmeasurement.MeasurementID
        airTempResult.ResultID = 0
        airTempResult.StartTime = meanTime
        # airTempResult.EndTime = visit.EndDate
        airTempResult.ParameterID = ParamID
        airTempResult.UnitID = environmentSensors[ParamID]
        airTempResult.ResultType = resultType_NA
        airTempResult.ObservedResult = float(EHSN.disMeasManager.airTempCtrl)
        airTempResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        airTempResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <EnvConditionResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </EnvConditionResult>
    """
        ecmeasurement.Results.FieldVisitResult.append(airTempResult)



    # #Water Temperature
    # if str(EHSN.disMeasManager.waterTempCtrl).strip() != "":
    #     ParamID = 'TW'
    #     eTW = float(EHSN.disMeasManager.waterTempCtrl)


    #     # If we found the qr in the field visit, then we ask and the user will choose
    #     # If we could not find the qr in the field visit, then we add automatically
    #     twFound = False
    #     waterTempResult = aq.factory.create("ns0:FieldVisitResult")
    #     waterTempResult.MeasurementID = dmeasurement.MeasurementID
    #     waterTempResult.ResultID = 0
    #     waterTempResult.StartTime = meanTime
    #     # waterTempResult.EndTime = visit.EndDate
    #     waterTempResult.ParameterID = ParamID
    #     waterTempResult.UnitID = dischargeSensors[ParamID]
    #     waterTempResult.ObservedResult = float(EHSN.disMeasManager.waterTempCtrl)
    #     waterTempResult.Correction = 0.000
    #     waterTempResult.ResultType = resultType_RC
    #     waterTempResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    # <DischargeResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #   <Party>""" + cdataParty + """</Party>
    #   <Source>
    #     <SourceType>
    #       <Id>Import</Id>
    #       <DisplayName>""" + src + """</DisplayName>
    #     </SourceType>
    #     <DisplayName>""" + src + """</DisplayName>
    #     <Sequence>1</Sequence>
    #   </Source>
    # </DischargeResult>
    # """
    #     ecmeasurement.Results.FieldVisitResult.append(waterTempResult)


        # for mea in dmeasurement.Results.FieldVisitResult:

        #     val = True


        #     if mea.ParameterID == ParamID:
        #         aTW = mea.ObservedResult
        #         AQResultDetails = mea.ResultDetails
        #         source = ET.fromstring(AQResultDetails).find("Source").find("SourceType").find("DisplayName").text

        #         twFound = True

        #         if aTW != eTW:

        #             if "import" in source.lower():
        #                 break
        #             else:

        #                 aTW = str(aTW)
        #                 eTW = str(eTW)

        #                 AUD = AquariusConflictUploadDialog("DEBUG", None, eTW + u" \N{DEGREE SIGN}C", aTW + u" \N{DEGREE SIGN}C", "Water Temp", source, None, title="Upload Field Visit to Aquarius")

        #                 while val:
        #                     re = AUD.ShowModal()
        #                     if re == wx.ID_YES:

        #                         # Add mgh to field visit with measurement ID
        #                         waterTempResult.ResultID = mea.ResultID
        #                         dmeasurement.Results.FieldVisitResult.append(waterTempResult)
        #                         val = False
        #                         break
        #                     else:
        #                         val = False
        #                         break
        #                 AUD.Destroy()
        #     if not val:
        #         break

        # # did not find q in the existing field visit, append to results list
        # if not twFound:
        #     waterTempResult.MeasurementID = 0
        #     dmeasurement.Results.FieldVisitResult.append(waterTempResult)







    # if EHSN.disMeasManager.IsEmpty():

    #Water Temp
    if str(EHSN.disMeasManager.waterTempCtrl) != "":
        ParamID = 'TW'

        waterTempResult = aq.factory.create("ns0:FieldVisitResult")
        waterTempResult.MeasurementID = ecmeasurement.MeasurementID
        waterTempResult.ResultID = 0
        waterTempResult.StartTime = meanTime
        # waterTempResult.EndTime = visit.EndDate
        waterTempResult.ParameterID = ParamID
        waterTempResult.UnitID = environmentSensors[ParamID]
        waterTempResult.ResultType = resultType_NA
        waterTempResult.ObservedResult = float(EHSN.disMeasManager.waterTempCtrl)
        waterTempResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        waterTempResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <EnvConditionResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </EnvConditionResult>
    """
        ecmeasurement.Results.FieldVisitResult.append(waterTempResult)

    #Wind Velocity
    if str(EHSN.envCondManager.windMagCtrl) != "":
        ParamID = 'US'

        windVelResult = aq.factory.create("ns0:FieldVisitResult")
        windVelResult.MeasurementID = ecmeasurement.MeasurementID
        windVelResult.ResultID = 0
        windVelResult.StartTime = meanTime
        # windVelResult.EndTime = visit.EndDate
        windVelResult.ParameterID = ParamID
        windVelResult.UnitID = environmentSensors[ParamID]
        windVelResult.ResultType = resultType_NA
        windVelResult.ObservedResult = float(EHSN.envCondManager.windMagCtrl)
        windVelResult.Correction = 0.000
        cdataParty = repChar(visit.Party)
        windVelResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    <EnvConditionResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Party>""" + cdataParty + """</Party>
      <Source>
        <SourceType>
          <Id>Import</Id>
          <DisplayName>""" + src + """</DisplayName>
        </SourceType>
        <DisplayName>""" + src + """</DisplayName>
        <Sequence>1</Sequence>
      </Source>
    </EnvConditionResult>
    """
        ecmeasurement.Results.FieldVisitResult.append(windVelResult)


    # #Recorded Sensor Values
    # #Loop through each sensor val and check if it is a discharge measurement
    # for index, sensorRefEntry in enumerate(EHSN.measResultsManager.sensorRefEntries):

    #     #Is this a "valid" measurement result that can be uploaded to Aquarius?
    #     if EHSN.measResultsManager.sensorRef.has_key(sensorRefEntry.GetValue().strip()):

    #         #Is this a discharge measurement?
    #         if environmentSensors.has_key(EHSN.measResultsManager.sensorRef[sensorRefEntry.GetValue()]):

    #             ParamID = EHSN.measResultsManager.sensorRef[sensorRefEntry.GetValue()]

    #             observed = 0.000 if EHSN.measResultsManager.observedVals[index].GetValue() == "" else float(EHSN.measResultsManager.observedVals[index].GetValue())
    #             logger = "" if EHSN.measResultsManager.sensorVals[index].GetValue() == "" else str(EHSN.measResultsManager.sensorVals[index].GetValue())

    #             resultVal = aq.factory.create("ns0:FieldVisitResult")
    #             resultVal.MeasurementID = ecmeasurement.MeasurementID
    #             resultVal.ResultID = 0
    #             resultVal.StartTime = startTime
    #             # resultVal.EndTime = startTime
    #             resultVal.ParameterID = ParamID
    #             resultVal.UnitID = environmentSensors[ParamID]
    #             resultVal.ObservedResult = observed
    #             resultVal.Correction = 0.000
    #             resultVal.ResultType = resultType
    #             cdataParty = repChar(visit.Party)
    #             resultVal.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
    #         <EnvConditionResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #           <Party>""" + cdataParty + """</Party>
    #           <Source>
    #             <SourceType>
    #               <Id>Import</Id>
    #               <DisplayName>""" + src + """</DisplayName>
    #             </SourceType>
    #             <DisplayName>""" + src + """</DisplayName>
    #             <Sequence>1</Sequence>
    #           </Source>""" + \
    #           ("" if logger == "" else """\n<LoggerValue>""" + logger + """</LoggerValue>""") + """
    #         </EnvConditionResult>
    #         """
    #             ecmeasurement.Results.FieldVisitResult.append(resultVal)

    if len(ecmeasurement.Results.FieldVisitResult) <= 0 and ecmeasurement.Remarks == "":
        return None

    # if MEASUREMENT_ID != 0:
    #     if len(ecmeasurement.Results.FieldVisitResult) == len(MEASUREMENT.Results.FieldVisitResult):
    #         ecmeasurement.MeasurementID = -ecmeasurement.MeasurementID

    return ecmeasurement

#Get the bench mark according to the station on the front page
def GetBM(stationID, aq, server):
    imp1 = Import('http://www.w3.org/2001/XMLSchema')
    doctor = ImportDoctor(imp1)
    aq2 = Client('http://' + server + '/AQUARIUS/AquariusDataService.svc?wsdl', doctor=doctor)

    # for each station
    station = stationID

    benchmarkList = []

    # Check if real station
    locid = aq.service.GetLocationId(station)

    # is not a real station
    if locid == 0:
        failedStations.append(station)


    # GetLocationBenchmarks
    benchmarks = aq2.service.GetLocationBenchmarks(locid)

    if benchmarks is None:
        return

    try:
        # list of benchmarks
        benchmarks = benchmarks[0]
    except IndexError:
        # has no benchmarks not active?
        failedStations.append(station)
    line = []
    for bm in benchmarks:
        # print "***", str(bm.Name), "***"
        bmName = unicode(bm.Name)
        # print "***", str(bmName), "***"
        if bm.History is not None:
            history = bm.History[0]
            latestBM = None
            for i, hist in enumerate(history):
                if i == 0:
                    latestBM = hist
                else:
                    if hist.StartDate > latestBM.StartDate:
                        latestBM = hist

            if latestBM is not None:
                if "inactive" not in latestBM.Status.lower():
                    # print "append bmName", bmName, "***"
                    line.append(bmName)
                    # line.append(latestBM.AcceptedElevation)
                    # benchmarkList.append(line)
    return line

# Creates a FieldVisitMeasurement with type WscFvtPlugin_ActivityTypeEnvCondition
def CreateLevelSurveyMeasurements(mode, src, aq, visit, MEASUREMENT, EHSN, dateInfo, server, fvStartDate):
    if mode == "DEBUG":
        print "Creating Level Survey Measurements"

    # # Used to replace / modify existing Measurements
    # if MEASUREMENT == 0:
    #     MEASUREMENT_ID = 0
    # else:
    #     MEASUREMENT_ID = MEASUREMENT.MeasurementID

    # Set to 0 for new measurement
    MEASUREMENT_ID = 0


    # if EHSN.disMeasManager.IsEmpty():
    meanTime = EHSN.stageMeasManager.CalculteMeanTime()

    # else:
    #     meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"
    # meanTime = str(EHSN.disMeasManager.mmtValTxt) if str(EHSN.disMeasManager.mmtValTxt) != '' else "00:00"
    meanTime = datetime.datetime.strptime(meanTime, "%H:%M")
    meanTime = meanTime.replace(dateInfo.year, dateInfo.month, dateInfo.day)
    meanTime = str(meanTime.isoformat()) + isoTail


    levelSurvey = aq.factory.create("ns0:FieldVisitMeasurement")
    levelSurvey.ApprovalLevelID = 3
    levelSurvey.MeasurementID = MEASUREMENT_ID
    levelSurvey.FieldVisitID = visit.FieldVisitID
    levelSurvey.MeasurementType = "LevelSurvey"
    levelSurvey.MeasurementTime = fvStartDate
    levelSurvey.MeasurementEndTime = fvStartDate
    levelSurvey.LastModified = datetime.datetime(0001, 01, 01)
    levelSurvey.Results.FieldVisitResult = []
    levelSurvey.Remarks = EHSN.waterLevelRunManager.commentsCtrl
    bmList = []
    cdataParty = repChar(visit.Party)
    bms = GetBM(EHSN.genInfoManager.stnNumCmbo, aq, server)
    if bms is not None:

        for index, run in enumerate(EHSN.waterLevelRunManager.runSizer.GetChildren()):
            if EHSN.waterLevelRunManager.UploadIsChecked(index):

                for rowIndex, entry in enumerate(EHSN.waterLevelRunManager.GetLevelNotesSizerV(index).GetChildren()):

                    if rowIndex < len(EHSN.waterLevelRunManager.GetLevelNotesSizerV(index).GetChildren()) - 1:
                        if EHSN.waterLevelRunManager.GetLevelNotesElevation(index, rowIndex).GetValue() != '':
                            bm = EHSN.waterLevelRunManager.GetLevelNotesStation(index, rowIndex).GetValue()
                            if "**" in bm:
                                bm = bm[2:]
                                # print bm
                            if bm not in bmList and bm in bms:
                                levelSurveyResult = aq.factory.create("ns0:FieldVisitResult")
                                levelSurveyResult.CorrectedResult = float(EHSN.waterLevelRunManager.GetLevelNotesElevation(index, rowIndex).GetValue())
                                levelSurveyResult.Correction = 0.0
                                levelSurveyResult.EndTime = None
                                levelSurveyResult.MeasurementID = levelSurvey.MeasurementID
                                levelSurveyResult.ObservedResult = float(EHSN.waterLevelRunManager.GetLevelNotesElevation(index, rowIndex).GetValue())
                                levelSurveyResult.ParameterID = "LevelSurveyResult"
                                levelSurveyResult.BenchmarkOrRefPointName = bm
                                # levelSurveyResult.PercentUncertainty = None
                                # levelSurveyResult.Qualifier = None
                                # levelSurveyResult.QualityCodeID = None
                                # levelSurveyResult.Remarks = None


                                levelSurveyResult.ResultDetails = r"""<?xml version="1.0" encoding="UTF-8"?>
                                    <LevelSurveyResult xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                                      <Party>""" + cdataParty + """</Party>
                                      <Source>
                                        <SourceType>
                                          <Id>Import</Id>
                                          <DisplayName>""" + src + """</DisplayName>
                                        </SourceType>
                                        <DisplayName>""" + src + """</DisplayName>
                                        <Sequence>1</Sequence>
                                      </Source>
                                    </LevelSurveyResult>
                                    """


                                levelSurveyResult.ResultID = 0
                                levelSurveyResult.ResultType = resultType_All
                                levelSurveyResult.StartTime = meanTime
                                levelSurveyResult.UnitID = "m"

                                levelSurvey.Results.FieldVisitResult.append(levelSurveyResult)
                                bmList.append(bm)



    levelSurvey = None if len(levelSurvey.Results.FieldVisitResult) == 0 else levelSurvey
    return levelSurvey
