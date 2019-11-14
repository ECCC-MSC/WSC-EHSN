# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from AQUARIUSDataExtractionToolFrame import *
import subprocess
import os
import io
import sys
from suds.client import Client
from base64 import b64encode
from base64 import b64decode
import datetime

import StringIO
import csv

import requests
import re
import json

import heapq

from suds.xsd.doctor import Import, ImportDoctor
from operator import itemgetter



from xml.etree import ElementTree

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


class AQUARIUSDataExtractionToolManager(object):
    def __init__(self, mode, scriptLoc, gui, EHSNGui):
        self.gui = gui
        self.config_path = None
        if self.gui is not None:
            self.gui.manager = self
            if self.gui.GetParent() is not None:
                self.config_path = self.gui.GetParent().config_path

        self.timeZones = {'-8' : 'PST',
                          '-7' : 'MST',
                          '-6' : 'CST',
                          '-5' : 'EST',
                          '-4' : 'AST',
                          '-3' : 'NST',
                          '-0' : 'UTC'}

        self.scriptLoc = scriptLoc
        self.EHSNGui = EHSNGui
        self.mode = mode


        
        # if hasattr(sys, '_MEIPASS'):
        #     self.config_path = os.path.join(sys._MEIPASS, self.config_path)
        # else:
        #     self.config_path = os.getcwd() + "\\" + self.config_path

        # print self.config_path    
        if self.config_path is not None:
            self.configFile = ElementTree.parse(self.config_path).getroot().find('AQUARIUSDataExtractionToolManager')


            self.rctUser = self.configFile.find('rctUser').text
            self.rctPassword = self.configFile.find('rctPassword').text

    def RunScript(self, path):
        # counter = 0
        # while True:
            # Check authentication
        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()
        Server = self.gui.GetURL()

        if Login == "":
            self.gui.CreateErrorDialog("Username field cannot be left blank.  Please use your AQUARIUS username.")
            return
        elif Password == "":
            self.gui.CreateErrorDialog("Password field cannot be left blank.  Please use your AQUARIUS password.")
            return
        elif self.gui.StationListIsEmpty():
            self.gui.CreateErrorDialog("Station ID list field cannot be left blank.  Please enter the station ID that you are uploading.")
            return

        try:
            aq = Client(Server + '/aquarius/AQAcquisitionService.svc?wsdl')
            aq.set_options(headers={'AQAuthToken':aq.service.GetAuthToken(Login, Password)})

            authcode = aq.service.GetAuthToken(Login, Password)

        except:
            self.gui.CreateErrorDialog("User Login Failed, please use your AQUARIUS username and password.")
            return -1

        # # Check if stations exist
        # locations = self.GetStationList()
        # for station in locations:
        #     # Check if real station
        #     locid = aq.service.GetLocationId(station)
        #     print locid

        #     # is not a real station
        #     if locid == 0:
        #         self.gui.CreateErrorDialog("Station ID: " + station + " appears to be invalid")
        #         return -2

        # if the export file path does not exist, create a new folder
        if not os.path.exists(path):
            os.makedirs(path)

        # Lists of stations that go wrong per method
        failedStnInfo = []
        failedLvlInfo = []
        failedRatingInfo = []
        failedHistMmts = []

        # Check checkboxes for which items to retrieve
        # if StationInfo checked
        if self.gui.StnIsChecked():
            self.gui.CreateProgressDialog('Extraction In Progress...', 'Collecting data for Station Information (stations.txt)')

            res = self.GetStationInfo(aq, path, failedStnInfo)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Unable to write to file. Please make sure the file stations.txt is closed")
            elif res != 0:
                # unplanned response
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Something went wrong while collecting Levelling Information A few trouble shooting tips: \n" + \
"\t1. Try reducing the list of stations you're extracting data for and try again.\n "+\
"\t2. ometimes naming conventions within AQUARIUS are incorrect. Ensure that your naming conventions are correct.\n"+\
"\t3. Sometimes I try and extract data that doesn't exist (e.g., a rating curve for a stage only station).  This can mess me up.  Make sure what you're asking me to extract exisits.\n"+\
"If you're still having problems after this hint, please file a bug report.")


        # if LevelsInfo checked
        if self.gui.LvlIsChecked():
            if self.gui.ProgressDialogIsOpen():
                self.gui.UpdateProgressDialog('Collecting data for Levels Information (levels.txt)')
            else:
                self.gui.CreateProgressDialog('Extraction In Progress', 'Collecting data for Levels Information (levels.txt)')

            res = self.GetLevelsInfo(aq, path, failedLvlInfo)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
            elif res != 0:
                # unplanned response
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Something went wrong while collecting Levelling Information A few trouble shooting tips: \n" + \
"\t1. Try reducing the list of stations you're extracting data for and try again.\n "+\
"\t2. ometimes naming conventions within AQUARIUS are incorrect. Ensure that your naming conventions are correct.\n"+\
"\t3. Sometimes I try and extract data that doesn't exist (e.g., a rating curve for a stage only station).  This can mess me up.  Make sure what you're asking me to extract exisits.\n"+\
"If you're still having problems after this hint, please file a bug report.")


        # if GetRatingInfo checked
        if self.gui.RCIsChecked():
            if self.gui.ProgressDialogIsOpen():
                self.gui.UpdateProgressDialog('Collecting Rating Curve Information (StationID_ratingcurves.xml)')
            else:
                self.gui.CreateProgressDialog('Extraction In Progress...', 'Collecting Rating Curve Information (StationID_ratingcurves.xml)')

            res = self.GetRatingInfo(path, failedRatingInfo)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
            elif res != 0:
                # unplanned response
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Something went wrong while collecting Rating Curve Information  A few trouble shooting tips: \n" + \
"\t1. Try reducing the list of stations you're extracting data for and try again.\n "+\
"\t2. ometimes naming conventions within AQUARIUS are incorrect. Ensure that your naming conventions are correct.\n"+\
"\t3. Sometimes I try and extract data that doesn't exist (e.g., a rating curve for a stage only station).  This can mess me up.  Make sure what you're asking me to extract exisits.\n"+\
"If you're still having problems after this hint, please file a bug report.")


        # if GetHistField checked
        if self.gui.DataPeriodIsChecked():
            if self.gui.ProgressDialogIsOpen():
                self.gui.UpdateProgressDialog('Collecting Historical Field Mmts (StationID_FieldVisits.csv)')
            else:
                self.gui.CreateProgressDialog('Extraction In Progress...', 'Collecting Historical Field Mmts (StationID_FieldVisits.csv)')

            if self.gui.IncludeMinMaxIsChecked():
                numMinMax = self.gui.GetNumOfMinMax()
            else:
                numMinMax = None
            res = self.GetFieldVisit(path, failedHistMmts, numMinMax)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
            elif res != 0:
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Getting Field Visit from AQUARIUS Failed")

        if self.gui.ProgressDialogIsOpen():
            self.gui.DeleteProgressDialog()
            # counter += 1
            # print "*****************************" + str(counter) + "********************************"

        report = self.ReportOnFailedStations(failedStnInfo, failedLvlInfo, failedRatingInfo, failedHistMmts, path)

    def RunScriptNg(self, path):
        # counter = 0
        # while True:
        # Check authentication
        print "here"
        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()
        Server = self.gui.GetURL()
        print Server + "<-- Server name"
        print Password + " <-- Password"

        if Login == "":
            self.gui.CreateErrorDialog("Username field cannot be left blank.  Please use your AQUARIUS username.")
            return
        elif Password == "":
            self.gui.CreateErrorDialog("Password field cannot be left blank.  Please use your AQUARIUS password.")
            return
        elif self.gui.StationListIsEmpty():
            self.gui.CreateErrorDialog(
                "Station ID list field cannot be left blank.  Please enter the station ID that you are uploading.")
            return

        try:
            aq = requests.get(Server + "GetAuthToken?Username=" + Login + "&EncryptedPassword=" + Password)

            authcode = aq.text

            print authcode

        except:
            self.gui.CreateErrorDialog("User Login Failed, please use your AQUARIUS username and password.")
            return -1

        # # Check if stations exist
        # locations = self.GetStationList()
        # for station in locations:
        #     # Check if real station
        #     locid = aq.service.GetLocationId(station)
        #     print locid

        #     # is not a real station
        #     if locid == 0:
        #         self.gui.CreateErrorDialog("Station ID: " + station + " appears to be invalid")
        #         return -2

        # if the export file path does not exist, create a new folder

        if not os.path.exists(path):
            os.makedirs(path)

        # Lists of stations that go wrong per method
        failedStnInfo = []
        failedLvlInfo = []
        failedRatingInfo = []
        failedHistMmts = []

        # Check checkboxes for which items to retrieve
        # if StationInfo checked
        if self.gui.StnIsChecked():
            self.gui.CreateProgressDialog('Extraction In Progress...',
                                          'Collecting data for Station Information (stations.txt)')

            res = self.GetStationInfoNg(aq, path, failedStnInfo)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Unable to write to file. Please make sure the file stations.txt is closed")
            elif res != 0:
                # unplanned response
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog(
                    "Something went wrong while collecting Levelling Information A few trouble shooting tips: \n" + \
                    "\t1. Try reducing the list of stations you're extracting data for and try again.\n " + \
                    "\t2. ometimes naming conventions within AQUARIUS are incorrect. Ensure that your naming conventions are correct.\n" + \
                    "\t3. Sometimes I try and extract data that doesn't exist (e.g., a rating curve for a stage only station).  This can mess me up.  Make sure what you're asking me to extract exisits.\n" + \
                    "If you're still having problems after this hint, please file a bug report.")

        # if LevelsInfo checked
        if self.gui.LvlIsChecked():
            if self.gui.ProgressDialogIsOpen():
                self.gui.UpdateProgressDialog('Collecting data for Levels Information (levels.txt)')
            else:
                self.gui.CreateProgressDialog('Extraction In Progress',
                                              'Collecting data for Levels Information (levels.txt)')

            res = self.GetLevelsInfoNg(aq, path, failedLvlInfo)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
            elif res != 0:
                # unplanned response
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog(
                    "Something went wrong while collecting Levelling Information A few trouble shooting tips: \n" + \
                    "\t1. Try reducing the list of stations you're extracting data for and try again.\n " + \
                    "\t2. ometimes naming conventions within AQUARIUS are incorrect. Ensure that your naming conventions are correct.\n" + \
                    "\t3. Sometimes I try and extract data that doesn't exist (e.g., a rating curve for a stage only station).  This can mess me up.  Make sure what you're asking me to extract exisits.\n" + \
                    "If you're still having problems after this hint, please file a bug report.")

        # if GetRatingInfo checked
        if self.gui.RCIsChecked():
            if self.gui.ProgressDialogIsOpen():
                self.gui.UpdateProgressDialog('Collecting Rating Curve Information (StationID_ratingcurves.xml)')
            else:
                self.gui.CreateProgressDialog('Extraction In Progress...',
                                              'Collecting Rating Curve Information (StationID_ratingcurves.xml)')

            res = self.GetRatingInfoNg(path, failedRatingInfo)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
            elif res != 0:
                # unplanned response
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog(
                    "Something went wrong while collecting Rating Curve Information  A few trouble shooting tips: \n" + \
                    "\t1. Try reducing the list of stations you're extracting data for and try again.\n " + \
                    "\t2. ometimes naming conventions within AQUARIUS are incorrect. Ensure that your naming conventions are correct.\n" + \
                    "\t3. Sometimes I try and extract data that doesn't exist (e.g., a rating curve for a stage only station).  This can mess me up.  Make sure what you're asking me to extract exisits.\n" + \
                    "If you're still having problems after this hint, please file a bug report.")

        # if GetHistField checked
        if self.gui.DataPeriodIsChecked():
            if self.gui.ProgressDialogIsOpen():
                self.gui.UpdateProgressDialog('Collecting Historical Field Mmts (StationID_FieldVisits.csv)')
            else:
                self.gui.CreateProgressDialog('Extraction In Progress...',
                                              'Collecting Historical Field Mmts (StationID_FieldVisits.csv)')

            if self.gui.IncludeMinMaxIsChecked():
                numMinMax = self.gui.GetNumOfMinMax()
            else:
                numMinMax = None
            res = self.GetFieldVisitNg(path, failedHistMmts, numMinMax)
            self.CheckReturn(res)
            if res == -1 or res == -2:
                pass
            elif res != 0:
                self.gui.DeleteProgressDialog()
                self.gui.CreateErrorDialog("Getting Field Visit from AQUARIUS Failed")

        if self.gui.ProgressDialogIsOpen():
            self.gui.DeleteProgressDialog()
            # counter += 1
            # print "*****************************" + str(counter) + "********************************"

        report = self.ReportOnFailedStations(failedStnInfo, failedLvlInfo, failedRatingInfo, failedHistMmts, path)


    def GetStationInfo(self, aq, path, failedStations):
        # SOAP Acquisition API
        # Check Auth
        print "Get Station Info"

        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()
        Server = self.gui.GetURL()



        authcode = None

        stationsList = []

        # login
        try:
            aq2 = Client(Server+'/AQUARIUS/Publish/AquariusPublishService.svc?wsdl')

            authcode = aq2.service.GetAuthToken(Login, Password)
        except:
            return -1

        # print authcode

        # Rest Authentication
        ServerCall = Server + r"/aquarius/Publish/AquariusPublishRestService.svc/"
        command = ServerCall + r"GetAuthToken?user="
        command += Login + r"&encPwd=" + Password
        r = requests.get(command)
        MyAuthCode = r.text
        # print MyAuthCode

        # For each station in the stationlist
        locations = self.GetStationList()



        
        for station in locations:
            # Check if real station
            locid = aq.service.GetLocationId(station)
            # print locid

            if locid == 0:
                failedStations.append(station)
                continue

            # new line in the csv
            newStationLine = []

            # GetLocations for station name
            # stationID
            newStationLine.append(station)

            command = ServerCall + "GetLocations?token=" + MyAuthCode + "&filter=Identifier=" + station
            # print "Sending command: " + command
            r = requests.get(command)

            f = StringIO.StringIO(unicode(r.text).encode("utf8"))
            reader = csv.reader(f, delimiter=',')

            reader.next()
            locationName = None
            line = reader.next()

            # print line
            locationName = line[3]
            status = line[16]
            if status.lower() != "active":
                failedStations.append(station)
                continue


            # station name
            newStationLine.append(locationName)


            # Check row count
            row_count = sum(1 for row in reader)
            # print row_count

            # reset position in file
            f.seek(0)
            reader = csv.reader(f, delimiter=',')


            offsetVal = None
            if row_count > 1:
                reader.next()
                line = reader.next()

            #     # if station does not have any Data Sets (like meteorology stations)
            #     if not line:
            #         failedStations.append(station)
            #         continue
            #     # print line
            #     offset = str(line[7]).split('.')
            #     # print offset
            #     offset = offset[-1][-6:]
            #     offset = offset.split(':')[-2]
            #     # print "offset: ", offset
            #     # print self.timeZones[offset]
            #     offsetVal = self.timeZones[offset]


            # offset for station
            newStationLine.append(self.timeZones[line[12]])

            stationsList.append(newStationLine)


        # Maybe check if the file can be written to
        fileExists = None
        exportFile = None
        while True:
            try:
                if os.path.isfile(path + '\\stations.txt'):
                    fileExists = True
                    exportFile = open(path + '\\stations.txt', 'a+')
                else:
                    exportFile = open(path + '\\stations.txt', "wb")
                break
            except IOError:
                print "Could not open file! Please close Excel!"

                self.gui.DeleteProgressDialog()
                res = self.gui.CreateTryAgainDialog("Unable to write to file. Please close the file: stations.txt.\nTry again?")
                if res == 0:
                    self.gui.CreateProgressDialog('In Progress', 'Collecting data for Station Information (stations.txt)')
                else:
                    failedStations = locations
                    return


        if exportFile is not None:
            if not fileExists:
                exportFile.write("STATION ID,STATION NAME,TIMEZONE")

            else:
                # if file exists, read the file
                # reader = csv.reader(exportFile, delimiter='\n')



                readList = []

                with open(path + '\\stations.txt', 'a+') as f:
                    reader = csv.reader(f, delimiter=",")
                    for i, line in enumerate(reader):
                        if i > 0:
                            readList.append(line[0])



                # print "-----------------"
                # for j in readList:
                #     print j
                # print "-----------------"


                removeIndices = []

                for i, line in enumerate(stationsList):


                    if len(line) > 2:

                        for row in readList:
                            if line[0] == row:
                                print line[0] + " is in file"
                                removeIndices.append(i)
                                break

                        # exportFile.seek(0)
                        # reader = csv.reader(exportFile, delimiter=',')

                removeIndices.reverse()
                for i in removeIndices:
                    stationsList.remove(stationsList[i])

            writeList = []
            for line in stationsList:
                if len(line) > 2:
                    stationid = line[0]
                    stationName = line[1]
                    timezone = line[2]

                    outputLine = stationid + "," + unicode(stationName) + "," + timezone
                    writeList.append(outputLine)


            exportFile.close()
            exportFile = open(path + '\\stations.txt', 'a+')
            for line in writeList:
                exportFile.write("\n")
                exportFile.write(line.encode('utf8'))


            exportFile.close()

        return 0

    def GetStationInfoNg(self, aq, path, failedStations):
        # SOAP Acquisition API
        # Check Auth
        print "Get Station Info"

        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()
        Server = self.gui.GetURL()

        authcode = None

        stationsList = []

        # login
        try:
            aq2 = requests.get(Server + "GetAuthToken?Username=" + Login + "&EncryptedPassword=" + Password)

        except:
            return -1

        # print authcode

        # Rest Authentication
        r = requests.get(Server + "GetAuthToken?Username=" + Login + "&EncryptedPassword=" + Password)
        MyAuthCode = r.text
        # print MyAuthCode

        # For each station in the stationlist
        locations = self.GetStationList()
        # print locations

        writeList = []
        for station in locations:
            # Check if real station
            locid1 = requests.get(Server + "GetLocationData?Token=" + MyAuthCode + "&LocationIdentifier=" + station)
            locid = locid1.json()
            # print locid

            if 'ResponseStatus' in locid:
                print locid['ResponseStatus']['Message']
                failedStations.append(station)
                continue

            # new line in the csv
            newStationLine = []

            # GetLocations for station name
            # stationID
            newStationLine.append(station)

            # command = ServerCall + "GetLocations?token=" + MyAuthCode + "&filter=Identifier=" + station
            # # print "Sending command: " + command
            # r = requests.get(command)

            # f = StringIO.StringIO(unicode(r.text).encode("utf8"))
            stId = station
            stName = locid['LocationName']
            stUtc = self.timeZones[str(locid['UtcOffset'])]
            stIf = [stId, stName, stUtc]
            writeList.append(stIf)

        # print writeList

        # Maybe check if the file can be written to
        fileExists = None
        exportFile = None
        while True:
            try:
                if os.path.isfile(path + '\\stations.txt'):
                    fileExists = True

                    exportFile = open(path + '\\stations.txt', 'a+')
                else:
                    exportFile = open(path + '\\stations.txt', "wb")
                break
            except IOError:
                print "Could not open file! Please close Excel!"

                self.gui.DeleteProgressDialog()
                res = self.gui.CreateTryAgainDialog(
                    "Unable to write to file. Please close the file: stations.txt.\nTry again?")
                if res == 0:
                    self.gui.CreateProgressDialog('In Progress',
                                                  'Collecting data for Station Information (stations.txt)')
                else:
                    failedStations = locations
                    return

        if exportFile is not None:
            if not fileExists:
                exportFile.write("STATION ID,STATION NAME,TIMEZONE")

            else:
                readList = []

                with open(path + '\\stations.txt', 'a+') as f:
                    reader = csv.reader(f, delimiter=",")
                    for i, line in enumerate(reader):
                        if i > 0:
                            readList.append(line[0])

                # print "-----------------"
                # for j in readList:
                #     print j
                # print "-----------------"

                removeIndices = []

                for i in range(len(writeList)):

                    if len(writeList[i]) > 2:

                        for row in readList:
                            if writeList[i][0] == row:
                                print writeList[i][0] + " is in file"
                                removeIndices.append(i)
                                break

                        # exportFile.seek(0)
                        # reader = csv.reader(exportFile, delimiter=',')

                removeIndices.reverse()
                for i in removeIndices:
                    writeList.remove(writeList[i])
            exportFile.close()
            exportFile = open(path + '\\stations.txt', 'a+')
            for line in writeList:
                exportFile.write("\n")
                lineData = line[0] + ',' + line[1] + ',' + line[2]
                exportFile.write(lineData.encode('utf8'))

            exportFile.close()

        return 0

    # Taken from http://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python
    def unicode_csv_reader(self, utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect=dialect, skipinitialspace=True, **kwargs)

        for row in csv_reader:
            row_data = []
            for cell in row:
                if isinstance(cell, str):
                    cell = cell.decode('utf8')
                row_data.append(unicode(cell))

            yield row_data

        # yield cell_data




    def GetLevelsInfo(self, aq, path, failedStations):
        print "Level Info Checked"

        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()
        Server = self.gui.GetURL()


        totalBenchmarkList = []
        extractedBenchmarkList = []
        inactiveBMList = []

        # login
        imp1 = Import('http://www.w3.org/2001/XMLSchema')
        doctor = ImportDoctor(imp1)
        try:
            # aq2 = Client(Server + '/AQUARIUS/AquariusDataService.svc?wsdl')
            aq2 = Client(Server + '/AQUARIUS/AquariusDataService.svc?wsdl', doctor=doctor)
        except:
            print "Client(Server + '/AQUARIUS/AquariusDataService.svc?wsdl', doctor=doctor)"
            return

        # for each station
        locations = self.GetStationList()
        for station in locations:
            benchmarkList = []

            # Check if real station
            locid = aq.service.GetLocationId(station)
            # print locid

            # is not a real station
            if locid == 0:
                failedStations.append(station)
                continue

            # GetLocationBenchmarks
            benchmarks = aq2.service.GetLocationBenchmarks(locid)

            try:
                # list of benchmarks
                benchmarks = benchmarks[0]
            except IndexError:
                # has no benchmarks not active?
                failedStations.append(station)
                continue


            for bm in benchmarks:
                line = []
                addedBM = False

                bmName = unicode(bm.Name)
                desc = bm.LongName
                if isinstance(desc, str):
                    desc = desc.decode('utf8')
                desc = unicode(desc)
                latestBM = None
                if bm.History is not None:
                    history = bm.History[0]

                    for i, hist in enumerate(history):
                        if i == 0:
                            latestBM = hist
                        else:
                            if hist.StartDate > latestBM.StartDate:
                                latestBM = hist

                if latestBM is not None:
                    if "inactive" not in latestBM.Status.lower():
                        # add it to the master list of benchmarks

                        # Add info to line
                        # print str(bmName), "***"
                        if "primary" in latestBM.Status.lower():
                            bmName = "**" + str(bmName)
                        line.append(station)
                        line.append(bmName)
                        line.append(latestBM.AcceptedElevation)
                        line.append(desc)

                        benchmarkList.append(line)
                        addedBM = True

                if not addedBM:
                    line.append(station)
                    line.append(bmName)
                    line.append("")
                    line.append("")
                    inactiveBMList.append(line)

            # sort the list by benchmark names
            benchmarkList = sorted(benchmarkList, key=lambda bm: bm[1])
            extractedBenchmarkList.extend(benchmarkList)
            # print benchmarkList
            # print "============"

        # Maybe check if file can be written to
        fileExists = None
        exportFile = None
        while True:
            try:
                if os.path.isfile(path + '\\levels.txt'):
                    fileExists = True
                    exportFile = open(path + '\\levels.txt', 'rU')
                else:
                    exportFile = open(path + '\\levels.txt', "wb")
                break
            except IOError:
                print "Could not open file! Please close Excel!"
                self.gui.DeleteProgressDialog()
                res = self.gui.CreateTryAgainDialog("Unable to write to file. Please close the file: levels.txt.\nTry again?")
                if res == 0:
                    self.gui.CreateProgressDialog('Extraction In Progress...', 'Collecting data for Levels Information (levels.txt)')
                else:
                    failedStations = locations
                    return



        if exportFile is not None:
            if fileExists:
                # if file exists, read the file
                # import file (if exists) by parsing as csv
                # reader = csv.reader(exportFile, delimiter=',')

                reader = self.unicode_csv_reader(exportFile)

                fileBMList = []
                for row in reader:
                    fileBMList.append(row)

                fileBMList = fileBMList[1:]

                removeIndices = []

                # update lists
                for bm in fileBMList:
                    for ebm in extractedBenchmarkList:
                        if bm[0] == ebm[0] and bm[1] == ebm[1]:
                            bm[2] = ebm[2]
                            bm[3] = ebm[3]
                            break

                # combine lists
                for ebm in extractedBenchmarkList:
                    bmFound = False
                    for bm in fileBMList:
                        if bm[0] == ebm[0] and bm[1] == ebm[1]:
                            bmFound = True
                            break

                    if not bmFound:
                        fileBMList.append(ebm)


                # remove inactive bms
                for rbm in inactiveBMList:
                    for i, bm in enumerate(fileBMList):
                        if bm[0] == rbm[0] and bm[1] == rbm[1]:
                            removeIndices.append(i)

                removeIndices.sort()
                removeIndices.reverse()
                for i in removeIndices:

                    fileBMList.remove(fileBMList[i])


                exportFile.close()
                exportFile =  open(path + '\\levels.txt', "wb")

                totalBenchmarkList = sorted(fileBMList, key=itemgetter(0, 1))
            else:
                totalBenchmarkList = extractedBenchmarkList

            writeList = []
            for bm in totalBenchmarkList:
                stationid = bm[0]
                reference = bm[1]
                elevation = bm[2]
                desc = bm[3]
                desc = desc.replace("\"", "\"\"")

                outputLine = unicode(stationid) + "," + unicode(reference) + "," + unicode(elevation) + ",\"" + unicode(desc) + "\""
                writeList.append(outputLine)
                # print stationid + ", " + reference + ", " + elevation + ", " + desc

            # Write to file
            exportFile.write("STATION,REFERENCE,ELEVATION,DESCRIPTION\n")
            for line in writeList:
                # print line.encode("utf8")
                line += '\n'
                exportFile.write(line.encode('utf8'))

            exportFile.close()

        return 0

    def GetLevelsInfoNg(self, aq, path, failedStations):
        print "Level Info Checked"

        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()
        Server = self.gui.GetURL()

        totalBenchmarkList = []
        extractedBenchmarkList = []
        inactiveBMList = []

        # login
        try:
            req = requests.get(Server + "GetAuthToken?Username=" + Login + "&EncryptedPassword=" + Password)
            token = req.text
        except:
            return -1

        # for each station
        locations = self.GetStationList()
        for station in locations:
            req = requests.get(Server + "GetAuthToken?Username=" + Login + "&EncryptedPassword=" + Password)
            token = req.text
            try:
                req = requests.get(Server + "GetLocationData?LocationIdentifier=" + station + "&token=" + token)
            except:
                failedStations.append(station)
                return -1
            staInfo = req.json()['ReferencePoints']
            # print staInfo
            for benchMark in staInfo:
                benchMarkInfo = []
                try:
                    staRef = benchMark['Name']
                    staRef.replace('\n', ' ')
                except:
                    staRef = ''
                    print("The reference is empty.")

                try:
                    refPoint = benchMark['ReferencePointPeriods']
                    staElevation = refPoint[len(refPoint) - 1]['Elevation']
                except:
                    refPoint = ''
                    print("The elevation is empty.")

                try:
                    staDescription = benchMark['Description']
                    staDescription.replace('\n', ' ')
                except:
                    staDescription = ''
                    print("The description is empty.")

                benchMarkInfo.append(station)
                benchMarkInfo.append(str(staRef))
                benchMarkInfo.append(str(staElevation))
                benchMarkInfo.append(str(staDescription))

                totalBenchmarkList.append(benchMarkInfo)

            # print totalBenchmarkList

        # Maybe check if file can be written to

        fileExists = None
        exportFile = None
        extractedBenchmarkList = totalBenchmarkList
        while True:
            try:
                if os.path.isfile(path + '\\levels_Ng.txt'):
                    fileExists = True
                    exportFile = open(path + '\\levels_Ng.txt', 'rU')
                else:
                    exportFile = open(path + '\\levels_Ng.txt', "wb")
                break
            except IOError:
                print "Could not open file! Please close Excel!"
                self.gui.DeleteProgressDialog()
                res = self.gui.CreateTryAgainDialog(
                    "Unable to write to file. Please close the file: levels_Ng.txt.\nTry again?")
                if res == 0:
                    self.gui.CreateProgressDialog('Extraction In Progress...',
                                                  'Collecting data for Levels Information (levels.txt)')
                else:
                    failedStations = locations
                    return

        if exportFile is not None:
            if fileExists:

                # if file exists, read the file
                # import file (if exists) by parsing as csv
                # reader = csv.reader(exportFile, delimiter=',')

                reader = self.unicode_csv_reader(exportFile)
                # print reader

                fileBMList = []
                for row in reader:
                    fileBMList.append(row)
                # print fileBMList

                fileBMList = fileBMList[1:]

                removeIndices = []

                # update lists
                for bm in fileBMList:
                    for ebm in extractedBenchmarkList:
                        if bm[0] == ebm[0] and bm[1] == ebm[1]:
                            bm[2] = ebm[2]
                            bm[3] = ebm[3]
                            break

                # combine lists
                for ebm in extractedBenchmarkList:
                    bmFound = False
                    for bm in fileBMList:
                        if bm[0] == ebm[0] and bm[1] == ebm[1]:
                            bmFound = True
                            break

                    if not bmFound:
                        fileBMList.append(ebm)

                # totalBenchmarkList = sorted(fileBMList, key=itemgetter(0, 1))

            # Write to file
            exportFile.close()
            exportFile = open(path + '\\levels_Ng.txt', "wb")
            exportFile.close()
            exportFile = open(path + '\\levels_Ng.txt', "a+")
            exportFile.write("STATION,REFERENCE,ELEVATION,DESCRIPTION")
            for line in totalBenchmarkList:
                # print line
                exportFile.write("\n")
                lineData = line[0] + ',' + line[1] + ',' + line[2] + ',' + line[3]
                # print lineData
                exportFile.write(lineData.encode('utf8'))

            exportFile.close()

        return 0

    def GetRatingInfo(self, path, failedStations):
        if self.mode == "DEBUG":
            print "Manager Run Script"

        FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
        stationList = self.GetStationList()
        url = self.gui.GetURL()
        path = self.gui.GetPath()


        base_arg = "\"" + self.scriptLoc + "\""
        base_arg += " /username:" + self.rctUser + " /password:" + self.rctPassword + " /path:\"" + path + "\""
        # print base_arg

        # # if folder does not exist, make folder (folder should always exist since they're selecting it!
        # if not os.path.exists(path):
        #     os.makedirs(path)

        for station in stationList:
            arg = base_arg + " /station:" + station + " /url:" + "\"" + url + "\""

            if self.mode == "DEBUG":
                print arg

            CREATE_NO_WINDOW = 0x08000000
            re = subprocess.call(arg, creationflags=CREATE_NO_WINDOW)

            # re = subprocess.call(arg, stdout=FNULL, stderr=FNULL, shell=False)



            if re != 0:
                failedStations.append(station)
                continue

        # if not self.gui.DataPeriodIsChecked():
        #     self.gui.DeleteProgressDialog()
        #     self.gui.CreateMessageDialog("File saved to " + self.gui.path, "Done!")

        return 0

    def GetRatingInfoNg(self, path, failedStations):
        if self.mode == "DEBUG":
            print "Manager Run Script"

        stationList = self.GetStationList()
        Server = self.gui.GetURL()
        path = self.gui.GetPath()
        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()

        # login
        try:
            req = requests.get(Server+"GetAuthToken?Username="+Login+"&EncryptedPassword="+Password)
            token = req.text
        except:
            return -1


        for station in stationList:
            # Get token
            try:
                req = requests.get(Server + "GetAuthToken?Username=" + Login + "&EncryptedPassword=" + Password)
                token = req.text
                print "token --> " + token
            except:
                return -1

            # print token

            # Get rating curve Id
            try:
                req = requests.get(
                    Server + "GetRatingModelDescriptionList?LocationIdentifier=" + station + "&token=" + token)
                ratingCurveId = req.json()['RatingModelDescriptions'][0]['Identifier']
            except:
                failedStations.append(station)
                continue

            # Get rating curve data
            try:
                req = requests.get(
                    Server + "GetRatingCurveList?RatingModelIdentifier=" + ratingCurveId + "&token=" + token)
            except:
                failedStations.append(station)
                continue
            ratingCurveData = req.json()

            with io.open(path + '\\' + station + "_ratingcurves_Ng.json", 'w', encoding='utf8') as outfile:
                str_ = json.dumps(ratingCurveData, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
                outfile.write(to_unicode(str_))

        # if not self.gui.DataPeriodIsChecked():
        #     self.gui.DeleteProgressDialog()
        #     self.gui.CreateMessageDialog("File saved to " + self.gui.path, "Done!")

        return 0

    def GetFieldVisit(self, path, failedStations, numMinMax):
        Server = self.gui.GetURL()

        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()


        try:
            aq = Client(Server + '/aquarius/AQAcquisitionService.svc?wsdl')
            aq.set_options(headers={'AQAuthToken':aq.service.GetAuthToken(Login, Password)})

            # authcode = aq.service.GetAuthToken(Login, Password)
        except:
            return -1
        # print(authcode)

        locations = self.GetStationList()
        for location in locations:
            locid = aq.service.GetLocationId(location)
            # print location, "\t", locid
            locinf = aq.service.GetLocation(locid)

            if locinf is None:

                failedStations.append(location)
                continue

            offset = str(locinf.UtcOffset).split('.')

            offset = offset[0] + ':00' if len(offset[0]) > 2 else offset[0][:1] + '0' + offset[0][1:]  + ':00'
            start = self.gui.GetDataPeriodFrom().FormatISOCombined() + self.gui.isoTail + offset
            end = str(self.gui.GetDataPeriodTo())

            # print location
            # print start

            # print end
            try:
                endDatetime = datetime.datetime.strptime(end, "%d/%m/%Y %H:%M:%S")
            except ValueError as e:
                print e
                try:
                    endDatetime = datetime.datetime.strptime(end, "%m/%d/%Y %H:%M:%S")
                except ValueError as e:
                    print e
                    endDatetime = datetime.datetime.strptime(end, "%m/%d/%y %H:%M:%S")

            # print endDatetime
            # print locinf.UtcOffset
            table = []
            if numMinMax is not None:
                minMaxList = []
                try:
                    fv=aq.service.GetFieldVisitsByLocation(locid)
                except:
                    print "no fv in the location", locid
                    continue
            else:
                minMaxList = None
                fv=aq.service.GetFieldVisitsByLocationChangedSince(locid, start)



            for i in range(len(fv[0])):
                if fv[0][i].Measurements is not None:
                    if fv[0][i].Measurements[0] is not None:
                        for mea in fv[0][i].Measurements[0]:
                            if 'discharge' in mea.MeasurementType.lower():
                                line = []
                                area = None
                                width = None
                                waterVelo = None
                                hg = None
                                qr = None
                                startTime = None

                                if mea.Results is not None:

                                    measurementMean = self.CalMean(mea.MeasurementEndTime, mea.MeasurementTime)

                                    for fvr in mea.Results.FieldVisitResult:
                                        if fvr.ParameterID == 'HG':
                                            if fvr.StartTime == None:
                                                print fvr
                                            if fvr.ResultType == 1 or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                            # if fvr.ResultType == 1:

                                                hg = fvr.CorrectedResult
                                                # startTime = fvr.StartTime if startTime is None else startTime
                                                startTime = measurementMean
                                                if startTime != None:
                                                    startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")


                                        elif fvr.ParameterID == 'QR':
                                            if fvr.StartTime == None:
                                                print fvr
                                            if fvr.ResultType == 1  or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                            # if fvr.ResultType == 1 or fvr.ResultType == 2147483647:

                                                qr = fvr.CorrectedResult
                                                # startTime = fvr.StartTime if startTime is None else startTime
                                                startTime = measurementMean
                                                if startTime != None:
                                                    startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")

                                        elif fvr.ParameterID == 'RiverSectionArea':
                                            if fvr.ResultType == 1  or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                                area = fvr.CorrectedResult
                                            startTime = measurementMean
                                            if startTime != None:
                                                startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")

                                        elif fvr.ParameterID == 'RiverSectionWidth':
                                            if fvr.ResultType == 1  or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                                width = fvr.CorrectedResult
                                            startTime = measurementMean
                                            if startTime != None:
                                                startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")

                                        elif fvr.ParameterID == 'WV':
                                            if fvr.ResultType == 1  or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                                waterVelo = fvr.CorrectedResult
                                            startTime = measurementMean
                                            if startTime != None:
                                                startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")

                                hg = hg if hg is not None else ''
                                qr = qr if qr is not None else ''
                                area = area if area is not None else ''
                                width = width if width is not None else ''
                                waterVelo = waterVelo if waterVelo is not None else ''

                                if hg != '' and qr != '':

                                    if numMinMax is not None:
                                        minMaxLine=[startTimeDatetime.strftime('%Y-%m-%d %H:%M:%S [UTC') + offset + '],', str(hg) +',', str(qr) +',', str(width) +',', str(area) +',', str(waterVelo)+",", " "+"\n"]
                                        minMaxList.append(minMaxLine)

                                    if endDatetime > startTimeDatetime:
                                        startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
                                        year = startTime.year
                                        month = startTime.month
                                        day =  startTime.day
                                        newDate = wx.DateTime.FromDMY(day, month-1, year)
                                        if newDate.IsBetween(self.gui.GetDataPeriodFrom(), self.gui.GetDataPeriodTo()):
                                            line.append(startTime.strftime('%Y-%m-%d %H:%M:%S [UTC') + offset + '],')

                                            line.append(str(hg) + ',')
                                            line.append(str(qr) + ',')
                                            line.append(str(width) + ',')
                                            line.append(str(area) + ',')
                                            line.append(str(waterVelo) + ',')
                                            line.append(" " + "\n")
                                            table.append(line)

                                        # outputfile.write(mea.MeasurementTime.strftime('%Y-%m-%d %H:%M:%S [UTC-05:00]') + ',')
                                        # outputfile.write(str(qr) + ',')
                                        # outputfile.write(str(hg) + '\n')

            # Find min/max, if they're not already in table, append it to table.
            # If they are already in table, iterate through table and append the appropriate remarks.
            if numMinMax is not None:

                maxDischarge = heapq.nlargest(numMinMax, minMaxList, key=lambda x:float(x[2][:-1]))
                minDischarge = heapq.nsmallest(numMinMax, minMaxList, key=lambda x:float(x[2][:-1]))
                for line in maxDischarge:
                    if line not in table:
                        #line[-1].replace(" ", "Hist. max")
                        line[-1] = "Hist. max" + line[-1]
                        table.append(line)
                    else:
                        for tableLine in table:
                            if line == tableLine:
                                #tableLine[-1].replace(" ", "Hist. max")
                                tableLine[-1] = "Hist. max" + tableLine[-1]

                for line in minDischarge:
                    if line not in table:
                        #line[-1].replace(" ", "Hist. min")
                        line[-1] = "Hist. min" + line[-1]
                        table.append(line)
                    else:
                        for tableLine in table:
                            if line == tableLine:
                                #tableLine[-1].replace(" ", "Hist. min")
                                tableLine[-1] = "Hist. min" + tableLine[-1]

            table=sorted(table)

            if len(table) > 0:
                while True:
                    try:
                        outputfile = open(path + '\\' + location + "_FieldVisits.csv","wb")
                        outputfile.write('Date/Time, Stage|m, Discharge|m^3/s, Width|m, Area|m^2, Velocity|m/s, Remarks\n')
                        for m in table:
                            for n in m:
                                outputfile.write(n)
                        outputfile.close()
                        break
                    except IOError:
                        print "Could not open file! Please close Excel!"

                        self.gui.DeleteProgressDialog()
                        res = self.gui.CreateTryAgainDialog("Unable to write to file. Please close the file: " + location + "_FieldVisits.csv.\nTry again?")
                        self.gui.CreateProgressDialog('Extraction In Progress', 'Collecting Historical Field Mmts (StationID_FieldVisits.csv)')
                        if res == 0:
                            pass
                        else:
                            failedStations.append(location)
                            break
            else:

                failedStations.append(location)

        return 0

    def GetFieldVisitNg(self, path, failedStations, numMinMax):
        Server = self.gui.GetURL()

        Login = self.gui.GetUsername()
        Password = self.gui.GetPassword()

        try:
            req = requests.get(Server + 'GetAuthToken?Username=' + Login + '&EncryptedPassword=' + Password)
            token = req.text
            # print token


        except:
            return -1

        locations = self.GetStationList()
        timeFrom = str(self.gui.GetDataPeriodFrom()).replace("/", "-")
        timeTo = str(self.gui.GetDataPeriodTo()).replace("/", "-")
        formatdateFrom = timeFrom[6:10] + '-' + timeFrom[3:5] + '-' + timeFrom[0:2] + timeFrom[10:19]
        formatdateTo = timeTo[6:10] + '-' + timeTo[3:5] + '-' + timeTo[0:2]  + timeTo[10:19]
        print "time from:" + formatdateFrom
        print "time to:" + formatdateTo

        if numMinMax is not None:
            minMaxList = []
        else:
            minMaxList = None

        for location in locations:
            dataEmpty = True
            try:
                #req = requests.get(Server + 'GetFieldVisitDescriptionList?LocationIdentifier=' + location + '&QueryFrom=' + timeFrom + '&QueryTo=' + timeTo + '&token=' + token)
                req = requests.get(Server + 'GetFieldVisitDescriptionList?LocationIdentifier=' + location + '&token=' + token)
                fieldDescriptions = req.json()['FieldVisitDescriptions']
            except:
                failedStations.append(location)
                continue

            locids = []
            disChargeList = []
            fieldVisitInfoList = []
            startTimeList = []
            timeNum = 0
            for i in range(len(fieldDescriptions)):
                fieldVisitData = fieldDescriptions[i]
                fieldId = fieldVisitData['Identifier']
                locids.append(fieldId)
                fieldStartTime = str(fieldVisitData['StartTime'])
                fieldStartTime = fieldStartTime[0:10] + ' ' + fieldStartTime[11:19] + '[' + self.timeZones[
                    '-' + fieldStartTime[len(fieldStartTime) - 4:len(fieldStartTime) - 3]] + ']'
                # fieldStartTime = fieldStartTime[0:10]+' '+fieldStartTime[11:19]+'['+'UTC'+fieldStartTime[len(fieldStartTime)-6:len(fieldStartTime)]+']'
                startTimeList.append(fieldStartTime)

            # print locids
            for locid in locids:
                # print "+++++",locid
                req = requests.get(Server + 'GetFieldVisitData?FieldVisitIdentifier=' + locid + '&token=' + token)
                locinf = req.json()
                fieldVisitReadings = locinf['InspectionActivity']['Readings']

                if len(fieldVisitReadings) != 0:
                    '''
                    Add time in all section
                    '''

                    # Stage (m)
                    fieldVisitStage = ''
                    for i in fieldVisitReadings:
                        if i['Parameter'] == 'Stage':
                            fieldVisitStage = i['Value']['Numeric']
                            break

                    if fieldVisitStage == '':
                        # print("Stage value of id ",locid,"is empty")
                        pass

                    # Discharge (m^3/s)
                    try:
                        fieldVisitDischarge = locinf['DischargeActivities'][0]['DischargeSummary']['Discharge'][
                            'Numeric']
                    except:
                        # print("Discharge value of id ",locid,"is empty")
                        fieldVisitDischarge = ''

                    # width(m)
                    try:
                        fieldVisitWidth = \
                        locinf['DischargeActivities'][0]['PointVelocityDischargeActivities'][0]['Width']['Numeric']
                    except:
                        # print("Width value of id ",locid,"is empty")
                        fieldVisitWidth = ''

                    # Area(m^2)
                    try:
                        fieldVisitArea = \
                        locinf['DischargeActivities'][0]['PointVelocityDischargeActivities'][0]['Area']['Numeric']
                    except:
                        # print("Area value of id ",locid,"is empty")
                        fieldVisitArea = ''

                    # velocity(m/s)
                    try:
                        fieldVisitVelocity = \
                        locinf['DischargeActivities'][0]['PointVelocityDischargeActivities'][0]['VelocityAverage'][
                            'Numeric']
                    except:
                        # print("Velocity value of id ",locid,"is empty")
                        fieldVisitVelocity = ''

                    if str(fieldVisitStage) != '' and str(fieldVisitDischarge) != '':
                        newdate = startTimeList[timeNum]
                        date = newdate[0:19]
                        fieldDatalist = []

                        if numMinMax is not None:
                            minMaxLine = [startTimeList[timeNum]+ ',', str(fieldVisitStage) + ',', str(fieldVisitDischarge) + ',', str(fieldVisitWidth) + ',', str(fieldVisitArea) + ',', str(fieldVisitVelocity) + ',', ' ' + '\n']
                            minMaxList.append(minMaxLine)

                        # old
                        #disChargeList = []
                        #disChargeList.append(fieldVisitDischarge)
                        # old

                        if formatdateFrom <= date <= formatdateTo :
                           # print "#################################################################"
                           # print "ADDED : " + date
                           # print "#################################################################"
                            fieldDatalist.append(startTimeList[timeNum] + ',')
                            fieldDatalist.append(str(fieldVisitStage) + ',')
                            fieldDatalist.append(str(fieldVisitDischarge) + ',')
                            fieldDatalist.append(str(fieldVisitWidth) + ',')
                            fieldDatalist.append(str(fieldVisitArea) + ',')
                            fieldDatalist.append(str(fieldVisitVelocity) + ',')
                            fieldDatalist.append(' ' + '\n')
                            fieldVisitInfoList.append(fieldDatalist)
                        timeNum = timeNum + 1

            if numMinMax is not None:
                maxDischarge = heapq.nlargest(numMinMax, minMaxList, key=lambda x:float(x[2][:-1]))
                minDischarge = heapq.nsmallest(numMinMax, minMaxList, key=lambda x:float(x[2][:-1]))
                for line in maxDischarge:
                    if line not in fieldVisitInfoList:
                        line[-1] = 'Hist. max' + line[-1]
                        fieldVisitInfoList.append(line)
                    else:
                        for tableLine in fieldVisitInfoList:
                            if line == tableLine:
                                tableLine[-1] = 'Hist. max' + line[-1]

                for line in minDischarge:
                    if line not in fieldVisitInfoList:
                        line[-1] = 'Hist. min' + line[-1]
                        fieldVisitInfoList.append(line)
                    else:
                        for tableLine in fieldVisitInfoList:
                            if line == tableLine:
                                tableLine[-1] = 'Hist. min' + tableLine[-1]

            fieldVisitInfoList = sorted(fieldVisitInfoList)

            '''
            # print fieldVisitInfoList
            # print "!!!!",len(fieldVisitInfoList)
            if len(fieldVisitInfoList) > 0:
                # for min max checkbox
                # print location
                if numMinMax is not None:
                    disChargeList.sort()
                    nullNum = 0

                    for i in range(len(disChargeList)):
                        if disChargeList[i] != '':
                            continue
                        else:
                            nullNum = nullNum + 1

                    disChargeList = disChargeList[:len(disChargeList) - nullNum]
                    disChargeList = disChargeList[0:numMinMax] + disChargeList[
                                                                 len(disChargeList) - numMinMax:len(disChargeList)]
                    # print disChargeList

                    fieldDischargeList = []
                    for i in range(len(disChargeList)):
                        fieldDischargeList.append(str(disChargeList[i]) + ',')

                    if len(fieldDischargeList) < numMinMax:
                        # print("The number of information is less than the min/max number.")
                        pass
                    else:
                        for elem in fieldVisitInfoList:
                            if elem[2] in fieldDischargeList[0:numMinMax]:
                                elem[6] = 'Hint min \n'
                            if elem[2] in fieldDischargeList[numMinMax:]:
                                elem[6] = 'Hint max \n'
                # print fieldVisitInfoList
            else:
                failedStations.append(location)
            '''
            # print "####",len(fieldVisitInfoList)
            if len(fieldVisitInfoList) > 0:
                while True:
                    try:
                        outputfile = open(path + '\\' + location + "_FieldVisits_Ng.csv", "wb")
                        outputfile.write(
                            'Date/Time, Stage|m, Discharge|m^3/s, Width|m, Area|m^2, Velocity|m/s, Remarks\n')
                        for m in fieldVisitInfoList:
                            for n in m:
                                outputfile.write(n)
                        outputfile.close()
                        break
                    except IOError:
                        print "Could not open file! Please close Excel!"

                        self.gui.DeleteProgressDialog()
                        res = self.gui.CreateTryAgainDialog(
                            "Unable to write to file. Please close the file: " + location + "_FieldVisits.csv.\nTry again?")
                        self.gui.CreateProgressDialog('Extraction In Progress',
                                                      'Collecting Historical Field Mmts (StationID_FieldVisits.csv)')
                        if res == 0:
                            pass
                        else:
                            failedStations.append(location)
                            break
        return 0

    def CheckReturn(self, res):
        if res == -1:
            self.gui.DeleteProgressDialog()
            self.gui.CreateErrorDialog("Uh oh, Typo?, Unfortunately your user login failed, please try your AQUARIUS username and password again.")

        elif res == -2:
            self.gui.DeleteProgressDialog()
            self.gui.CreateErrorDialog("Please check that the location ID is right")


    def GetStationList(self):
        stationlist = self.gui.GetStationList()
        pattern = re.compile('[\W_]+')
        stationlist = pattern.sub(' ', stationlist).split()

        s = set(stationlist)
        return sorted(list(s))

    def ReportOnFailedStations(self, failedStnInfo, failedLvlInfo, failedRatingInfo, failedHistMmts, path):
        # report on which stations failed
        report = "Oh dear, some data was not successfully extracted:\n"
        stationTab = "          "
        stations = self.GetStationList()
        failedStations = set()
        failed = False


        if len(failedStnInfo) > 0:
            failed = True
            print "Locations that failed while getting station info:"
            print failedStnInfo

            report += "  1. Station metadata (stations.txt):\n" + stationTab
            for i, station in enumerate(failedStnInfo):
                failedStations.add(station)
                report += station
                if i < (len(failedStnInfo) - 1):
                    report += ", "
                    if (i+1) % 5 == 0:
                        report += "\n" + stationTab
            report += "\n"

        if len(failedLvlInfo) > 0:
            failed = True
            print "Locations that failed while getting levelling info:"
            print failedLvlInfo

            report += "  2. Benchmark/Reference Information (levels.txt):\n" + stationTab
            for i, station in enumerate(failedLvlInfo):
                failedStations.add(station)
                report += station
                if i < (len(failedLvlInfo) - 1):
                    report += ", "
                    if (i+1) % 5 == 0:
                        report += "\n" + stationTab
            report += "\n"

        if len(failedRatingInfo) > 0:
            failed = True
            print "Locations that failed while getting rating info:"
            print failedRatingInfo

            report += "  3. Rating Curves (StationID_ratingcurves.xml):\n" + stationTab
            for i, station in enumerate(failedRatingInfo):
                failedStations.add(station)
                report += station
                if i < (len(failedRatingInfo) - 1):
                    report += ", "
                    if (i+1) % 5 == 0:
                        report += "\n" + stationTab
            report += "\n"

        if len(failedHistMmts) > 0:
            failed = True
            print "Locations that failed while getting historical mmts:"
            print failedHistMmts

            report += "  4. Historical Field Visits (StationID_FieldVisits.csv):\n" + stationTab
            for i, station in enumerate(failedHistMmts):
                failedStations.add(station)
                report += station
                if i < (len(failedHistMmts) - 1):
                    report += ", "
                    if (i+1) % 5 == 0:
                        report += "\n" + stationTab
            report += "\n"

        # Display final message
        if failed:
            for s in failedStations:
                stations.remove(s)

            stn = stationTab
            for i, s in enumerate(stations):
                stn += s
                if i < (len(stations) - 1):
                    stn += ", "
                    if (i+1) % 5 == 0:
                        stn += "\n" + stationTab

            report = "All data successfully extracted for:\n" + stn + "\n\n" + report
            self.gui.CreateMessageDialog(report, "AQUARIUS Extraction Summary")
            self.gui.CreateMessageDialog("All files saved to: " + path, "AQUARIUS Extraction Summary")


            with open(path + "\\ExtractionErrorReport.txt","wb") as errorFile:
                errorFile.write(report)

            return -1
        else:
            self.gui.CreateMessageDialog("Success! All data successfully extracted for all stations! The files are saved to " + path, "AQUARIUS Extraction Summary")
            return 0


    def CalMean(self, start, end):
        start = str(start)
        end = str(end)

        if end == "None":
            print "end is none"
            return start
        elif start == "None":
            print "start is none"
            return end
        hour = int(start[11:13])
        minute = int(start[14:16])
        second = int(start[17:])

        hour += int(end[11:13])
        minute += int(end[14:16])
        second += int(end[17:])

        meanSecond = (3600 * hour + 60 * minute + second) / 2
        hour = str(meanSecond / 3600)
        minute = str(meanSecond % 3600 / 60)
        second = str(meanSecond % 3600 % 60)

        return start[:11] + hour + ":" + minute + ":" + second



def main():
    app = wx.App()

    frame = AQUARIUSDataExtractionToolFrame("DEBUG", os.getcwd() + "\\AQ_Extracted_Data",
                                           os.getcwd() + "\\EHSN_rating_curve.exe", None, None, size=(550, 470))
    frame.Show()
    app.MainLoop()




if __name__ == "__main__":
    main()
