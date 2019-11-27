# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from ElectronicFieldNotesGUI import *
from TitleHeaderManager import *
from GenInfoManager import *
from DischargeMeasurementsManager import *
from StageMeasurementsManager import *
from EnvironmentConditionsManager import *
from MeasurementResultsManager import *
from InstrumentDeploymentInfoManager import *
from PartyInfoManager import *
from WaterLevelRunManager import *
# from AnnualLevellingManager import *
from FRChecklistManager import *
from MovingBoatMeasurementsManager import *
from MidSectionMeasurementsManager import *
# from RemarksManager import *

from RatingCurveViewerToolManager import *

# from UserConfigManager import *
from AquariusMiscUploadDialogs import *
import VersionCheck
import XMLManager
import AquariusUploadManager

import IngestQRevManager
import IngestFlowTrackerDisManager
import IngestHfcManager
import IngestFt2Manager
import IngestSxsManager
import IngestRSSLDisManager

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

from xhtml2pdf import pisa             # import python module
from lxml import etree

import os
from os import chdir
from os import environ
from os.path import join
from os.path import dirname
import sys
import thread
import suds

import datetime
import sys
import threading
import requests
import re
import json



###########################################
#only used for generating excutable
if 0:
    # import common
    from reportlab.graphics.barcode import *
    import reportlab.graphics.barcode.common
    import reportlab.graphics.barcode.code128
    import reportlab.graphics.barcode.code93
    import reportlab.graphics.barcode.code39
    import reportlab.graphics.barcode.usps
    import reportlab.graphics.barcode.usps4s
    import reportlab.graphics.barcode.ecc200datamatrix
    import reportlab.graphics.barcode.eanbc
    import reportlab.graphics.barcode.fourstate
    import reportlab.graphics.barcode.lto
    import reportlab.graphics.barcode.qr
    import reportlab.graphics.barcode.qrencoder
    import reportlab.graphics.barcode.test
    import reportlab.graphics.barcode.widgets
##########################################



##mode = "DEBUG"
mode = "PRODUCTION"
EHSN_VERSION = "v1.3.2"
eHSN_WINDOW_SIZE = (965, 730)

# import wx.lib.inspection
# wx.lib.inspection.InspectionTool().Show()



class ElectronicHydrometricSurveyNotes:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.headerTitle = "Hydrometric Survey Notes " + EHSN_VERSION

        # Label variables
        self.exportAQTitle = "Uploading Field Visit to AQUARIUS"
        self.exportAQLoginMessage = "Logging into AQUARIUS..."
        self.exportAQLocMessage = "Checking location..."
        self.exportAQNoLoc = "Location does not exist. Please enter valid location number."
        self.exportAQFVMessage = "Checking if a Field Visit exists for selected date..."
        self.exportAQNoFV = "Could not find Field Visits for location:"
        self.exportAQNewFV = "Creating new Field Visit in AQUARIUS..."
        # self.exportAQAppendFV = "It appears that a Field Visit exists for this date. The data in this Hydrometric Survey note will be appended to the Field Visit. Continue?"
        self.exportAQAppendFV = "It appears that a Field Visit exists for this date.  Press OK to append the HSN to this field visit."
        self.exportAQWarning = "Upload Warning!"
        self.exportAQCancel = "Upload cancelled"
        self.exportAQExist = "Saving parsed data would result in duplicates!"
        self.exportAQFVUpdate = "Updating Field Visit in AQUARIUS"
        self.saveXMLErrorDesc = "Failed on saving to XML"
        self.saveXMLErrorTitle = "Failed on saving to XML"
        self.lockWarningTitle = "Are you sure?"
        self.lockWarningMessage = "If unlocked, it means that the user has made a decision to view or modify the uploaded xml file because any changes in the xml may not be reflected in AQUARIUS unless the file is uploaded again or modified manually in AQUARIUS."

        self.ctrlKeyDownFlag = False
        self.resizingLock = threading.Lock()

        self.stationNumProcessed = False

        
        self.InitUI()

        

    def InitUI(self):
        if mode == "DEBUG":
            print "EHSN"
        app = wx.App()
        self.uploadRecord = None
        self.gui = EHSNGui(mode, EHSN_VERSION, None, title=self.headerTitle, size=eHSN_WINDOW_SIZE)
        self.SetupManagers()
        self.stageMeasManager.AddEntry()
        self.waterLevelRunManager.AddRun()
        # 6 Entries
        for i in range(9):
            self.movingBoatMeasurementsManager.AddEntry()
        self.BindAutoSave()
        self.BindCorrectedMGH()
        self.gui.LoadDefaultConfig()
        self.midSectionDetailXml = {}
        self.midSectionRawData = None

        self.gui.titleHeader.enteredInHWSCB.Bind(wx.EVT_CHECKBOX, self.LockEvent)


        # try:
        #     self.gui.OpenStationFile('stations.csv')
        # except:
        #     pass
        # try:
        #     self.gui.OpenLevelFile('levels.csv')
        # except:
        #     pass
        # try:
        #     self.gui.OpenMeterFile('meters.csv')
        # except:
        #     pass

        self.DT_FORMAT = "%Y/%m/%d"
        ############################################
        #Version checking
        # latest = self.find(files)
        # if latest is not None:
        #   if not self.compare(EHSN_VERSION, self.find(files)):
        #       self.CreateDialog('System out of update, please download the newest version from the server.')

        ############################################

##        self.gui.Centre()

        app.Bind(wx.EVT_KEY_DOWN, self.OnKeyDownEvent)
        app.Bind(wx.EVT_KEY_UP, self.OnKeyUpEvent)
        self.gui.Show()
        # Muluken! if the new midsection is giving you problems, uncomment the below line!!
        #self.gui.form4.Disable()

        # atexit.register(self.OnExit())
        # wx.lib.inspection.InspectionTool().Show()
        try:
            app.MainLoop()
        except:
            if self.gui.fullname == '':
                self.ExportAsXML(str(os.getcwd()) + '\\' + self.genInfoManager.stnNumCmbo + "_CrashLog.xml", None)
            self.ExportAsXML(self.gui.fullname, None)

        # VersionCheck.Check(EHSN_VERSION, self, False)
    def GetLayout(self):
        return self.gui.layout


    # def OnExit(self):
    #     # if self.gui.fullname == '':
    #     #         self.ExportAsXML(str(os.getcwd()) + '\\' + self.genInfoManager.stnNumCmbo + "_CrashLog.xml")
    #     # self.ExportAsXML(self.gui.fullname)
    #     print "You are now leaving the eHSN, Have a nie day"


    # Instantiates all Managers and gives their respective GUIs
    def SetupManagers(self):
        self.gui.manager = self
        self.titleHeaderManager = TitleHeaderManager(mode, self.gui.titleHeader, self)
        self.genInfoManager = GenInfoManager(mode, self.gui.genInfo, self)
        self.disMeasManager = DischargeMeasurementsManager(mode, self.gui.disMeas, self)
        self.stageMeasManager = StageMeasurementsManager(mode, self.gui.stageMeas, self)
        self.envCondManager = EnvironmentConditionsManager(mode, self.gui.envCond, self)
        self.measResultsManager = MeasurementResultsManager(mode, self.gui.measResults, self)
        self.instrDepManager = InstrumentDeploymentInfoManager(mode, self.gui.instrDep, self)
        # self.remarksManager = RemarksManager(mode, self.gui.remarks, self)
        self.partyInfoManager = PartyInfoManager(mode, self.gui.partyInfo, self)
        self.waterLevelRunManager = WaterLevelRunManager(mode, self.gui.waterLevelRun, self)
        # self.annualLevelNotesManager = AnnualLevellingManager(mode, self.gui.annualLevelNotes, self)
        self.frChecklistManager = FRChecklistManager(mode, self.gui.frChecklist, self)
        self.movingBoatMeasurementsManager = MovingBoatMeasurementsManager(mode, self.gui.movingBoatMeasurements, self)
        self.midsecMeasurementsManager = MidSectionMeasurementsManager(mode, self.gui.midsecMeasurements, self)
        # self.ratingCurveExtractionToolmanager = RatingCurveExtractionToolManager()
        self.ratingCurveViewerToolManager = RatingCurveViewerToolManager(mode, self.gui.ratingFileDir, None, \
                                            self.disMeasManager, wx.LANGUAGE_ENGLISH, None, self)

        # self.userConfigManager = UserConfigManager(mode, self.gui.userConfig, self)











    # Update the Field Review Checklist with the value of depType
    def DeploymentUpdate(self, depType):
        self.frChecklistManager.changeDepType(depType)


    def FieldReviewChecklistUpdate(self, val):
        self.frChecklistManager.onInstrumentType(val)

    def ExportAsPDFWithoutOpen(self, filePath, xslPath):
        if mode == "DEBUG":
            print "Saving PDF"

##        pisa.showLogging()


        xml = self.EHSNToXML()
        print xslPath
        # transform = etree.XSLT(etree.parse(xslPath))
        transform = etree.XSLT(etree.parse(xslPath))
        result = transform(etree.fromstring(xml))

        # result = str(result).replace("%5C", "\\")
        result = str(result).replace("logo_path", self.gui.logo_path)
        result = result.replace("qr_path", self.gui.qr_path)

        # open output file for writing (truncated binary)
        resultFile = open(filePath, "w+b")

        # convert HTML to PDF
        pisa.CreatePDF(
                src=result,                # the HTML to convert
                dest=resultFile, show_error_as_pdf = True)           # file handle to receive result


                # pisa.CreatePDF(
                # src=result,                # the HTML to convert
                # dest=resultFile,           # file handle to receive result
                # encoding="UTF-8")
        resultFile.close()




    # Call EHSNToXML() to create xml tree
    # transform xml tree into html format (based on xsl)
    # create PDF based on html
    def ExportAsPDF(self, filePath, xslPath):

        self.ExportAsPDFWithoutOpen(filePath, xslPath)
        #Open the pdf

        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", filePath])
        else:
            os.startfile(filePath)

    #create pdf from a given xml file without open
    def ExportAsPDFFromXML(self, filePath, xslPath, xml):
        if mode == "DEBUG":
            print "Saving PDF"

##        pisa.showLogging()


        transform = etree.XSLT(etree.parse(xslPath))
        result = transform(etree.fromstring(xml))

        result = str(result).replace("logo_path", self.gui.logo_path)
        result = result.replace("qr_path", self.gui.qr_path)

        # open output file for writing (truncated binary)
        resultFile = open(filePath, "w+b")

        # convert HTML to PDF
        pisa.CreatePDF(
                src=result,                # the HTML to convert
                dest=resultFile, show_error_as_pdf = True)           # file handle to receive result

        # pisa.CreatePDF(
        #         src=result,                # the HTML to convert
        #         dest=resultFile,           # file handle to receive result
        #         encoding="UTF-8")
        

        resultFile.close()

    #After generating the pdf from xml, open the pdf
    def ExportAsPDFFromXMLOpen(self, filePath, xslPath, xml):

        self.ExportAsPDFFromXML(filePath, xslPath, xml)
        #Open the pdf

        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", filePath])
        else:
            os.startfile(filePath)


    #validate the mandatory value before uploading to AQ
    def CheckFVVals(self):

        AquariusUploadManager.CheckFVVals(mode, self)



    # Check if the values in the eHSN will cause an error during upload to AQ
    # Log in to AQ
    # Check Location (based on StationNumber)
    # Check if Field Visit exists for given date
    # If it exists, prompt user for append of info
    # If it doesn't exist, create new FV
    def ExportToAquarius(self, server, username, password, fvDate, discharge, levelNote):



        # Aquarius Login
        self.gui.createProgressDialog(self.exportAQTitle, self.exportAQLoginMessage)
        exists, value = AquariusUploadManager.AquariusLogin(mode, server, username, password)

        if exists:
            aq = value

            #See if location exists
            self.gui.updateProgressDialog(self.exportAQLocMessage)
            exists, locid = AquariusUploadManager.AquariusCheckLocInfo(mode, aq, self.genInfoManager.stnNumCmbo)

            if not exists:
                self.gui.deleteProgressDialog()
                return self.exportAQNoLoc

            # See if Field Visit Exists in Aquarius
            self.gui.updateProgressDialog(self.exportAQFVMessage)
            fv, val = AquariusUploadManager.AquariusFieldVisitExistsByDate(mode, aq, locid, fvDate)

            if val is None:
                self.gui.deleteProgressDialog()
                return self.exportAQNoFV + " %d" % locid


            if fv or len(val) > 0:
                self.gui.deleteProgressDialog()
                warning = wx.MessageDialog(None,
                                           self.exportAQAppendFV,
                                           self.exportAQWarning, wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
                cont = warning.ShowModal()
                if cont == wx.ID_CANCEL:
                    return self.exportAQCancel

                self.gui.createProgressDialog(self.exportAQTitle, self.exportAQFVUpdate)


            if len(val) >= 1:
                # make popup

                displayLis = []
                for dis in val:
                    disTime = dis.MeasurementTime
                    startDate = datetime.datetime.strptime(str(self.genInfoManager.datePicker), "%Y/%m/%d")
                    startDate = startDate.replace(hour=disTime.hour, minute=disTime.minute, second=disTime.second)

                    disName = startDate.strftime("%Y/%m/%d") + " discharge activity started at " + startDate.strftime("%H:%M:%S")
                    displayLis.append(disName)

                self.gui.deleteProgressDialog()
                if discharge:
                    AMDUD = AquariusMultDisUploadDialog("DEBUG", None, displayLis, None, title="Upload Field Visit to Aquarius")
                    AMDUD.Show()

                    re = AMDUD.ShowModal()


                    if re == wx.ID_YES:
                        if AMDUD.MergeRBIsSelected():
                            selectedDis = AMDUD.GetSelectedDisMeas()
                            index = displayLis.index(selectedDis)



                            val = [val[index]]
                        else:
                            val = []
                    else:
                        print "Cancel"
                        return "Cancelled out of field visit" + " %d" % locid

                    AMDUD.Destroy()
                self.gui.createProgressDialog(self.exportAQTitle, self.exportAQFVMessage)

            #There is no Field Visit for this day

            if len(val) == 0:
                self.gui.updateProgressDialog(self.exportAQNewFV)

                try:
                    emptyList = []

                    export = AquariusUploadManager.ExportToAquarius(mode, EHSN_VERSION, self, aq, fv, locid, discharge, levelNote, emptyList, None, server)

                    self.gui.deleteProgressDialog()

                    return export
                except suds.WebFault, e:
                    self.gui.deleteProgressDialog()

                    print e
                    return str(e)
                except ValueError, e:
                    self.gui.deleteProgressDialog()

                    return str(e)
            else:
                if mode == "DEBUG":
                    print "Field Visit for selected date"
                    print val

                paraList = AquariusUploadManager.GetParaIDByFV(val[0])
                export = AquariusUploadManager.ExportToAquarius(mode, EHSN_VERSION, self, aq, fv, locid, discharge, levelNote, paraList, val[0], server)
                self.gui.deleteProgressDialog()
                return export
        else:
            self.gui.deleteProgressDialog()
            return value

        # export ehsn to ng
    def ExportToAquariusNg(self, server, username, password, fvPath, fvDate):

            # print "NG"
            # Aquarius Login
            # self.gui.createProgressDialog(self.exportAQTitle, self.exportAQLoginMessage)

            # get token
        self.gui.createProgressDialog(self.exportAQTitle, self.exportAQLoginMessage)
        try:
            req = requests.get("http://" + server + "/AQUARIUS/Publish/v2/GetAuthToken?Username=" + username + "&EncryptedPassword=" + password)
            token = req.text
            try:
                toMessage = req.json()
                exists = False
                self.gui.deleteProgressDialog()
                return "The username or the password is incorrect."
            except:
                #print token
                exists = True
        except:
            print "http://" + server + "GetAuthToken?Username=" + username + "&EncryptedPassword=" + password
            exists = False
            self.gui.deleteProgressDialog()
            return "Failed to login."
            # print exists
        if exists:

                # See if location exists

                # print self.genInfoManager.stnNumCmbo
                # exists, locid = AquariusUploadManager.AquariusCheckLocInfo(mode, aq, self.genInfoManager.stnNumCmbo)
                # print "http://"+server+"/AQUARIUS/Publish/v2/GetLocationDescriptionList?Token="+token+"&LocationIdentifier="+self.genInfoManager.stnNumCmbo

                # get the station unique id
            try:
                req = requests.get("http://" + server + "/AQUARIUS/Publish/v2/GetLocationDescriptionList?Token=" + token + "&LocationIdentifier=" + self.genInfoManager.stnNumCmbo)
                try:
                    locid = req.json()['LocationDescriptions'][0]['UniqueId']
                    exists = True
                    # print locid
                except:
                    exists = False
                    # print "Id not exist1"
            except:
                exists = False
                # print "Id not exist"
            if not exists:
                self.gui.deleteProgressDialog()
                return self.exportAQNoLoc
            else:
                self.gui.updateProgressDialog(self.exportAQLocMessage)
                fvDate = str(datetime.datetime.strptime(str(fvDate), "%Y/%m/%d").strftime('%Y-%m-%d'))
                fvDate1 = fvDate[:-2]
                midtime = str(int(fvDate[-2:]) + 1)
                if len(midtime) == 1:
                    fvDate1 = fvDate1 + "0" + midtime
                else:
                    fvDate1 = fvDate1 + midtime

                    # get the field visit data from NG check if the fv already exist
                    # self.gui.updateProgressDialog(self.exportAQFVMessage)
                try:
                    req = requests.get("http://" + server + "/AQUARIUS/Publish/v2/GetFieldVisitDescriptionList?LocationIdentifier=" + self.genInfoManager.stnNumCmbo + "&QueryFrom=" + fvDate + "&QueryTo=" + fvDate1 + "&Token=" + token)
                    fvexData = req.json()['FieldVisitDescriptions'][0]['Identifier']
                    # print fvexData
                    exists = True
                except:
                    # print "field data doesn't exist."
                    exists = False

                    # upload to NG
                if exists:
                    self.gui.deleteProgressDialog()
                    return self.exportAQExist
                else:
                    self.gui.updateProgressDialog("Uploading...")
                    fvPath = fvPath.replace("\\", "\\\\")
                    fvPathPdf = fvPath.replace("\\", "\\\\")
                    fvPath = fvPath + ".xml"
                    fvPathPdf = fvPathPdf + ".pdf"

                    # print fvPath
                    files = {'file': open(fvPath, 'rb')}
                    filesPdf = {'file': open(fvPathPdf, 'rb')}

                    req = requests.post("http://" + server + "/AQUARIUS/Acquisition/v2/locations/" + locid + "/visits/upload/plugins?token=" + token, files=files)
                    visitUris = req.json()
                    # print visitUris
                    try:
                        visitUris = req.json()['ResponseStatus']['Message']
                        self.gui.deleteProgressDialog()
                        return visitUris
                    except:
                        try:
                            visitUris = visitUris['VisitUris'][0]
                            print visitUris
                        except:
                            self.gui.deleteProgressDialog()
                            return "Failed"

                    reqPdf = requests.post("http://" + server + "/AQUARIUS/Acquisition/v2/locations/" + locid + "/visits/upload/plugins?token=" + token, files=filesPdf)
                    visitUris = reqPdf.json()
                    # print visitUris
                    try:
                        visitUris = reqPdf.json()['ResponseStatus']['Message']
                        self.gui.deleteProgressDialog()
                        return visitUris
                    except:
                        try:
                            visitUris = visitUris['VisitUris'][0]
                            print visitUris
                        except:
                            self.gui.deleteProgressDialog()
                            return "Failed"
                # return self.exportAQWarning
        self.gui.deleteProgressDialog()
        return None

    # Checks the "Entered in HWS" checkbox at top of front page
    def ExportToAquariusSuccess(self):
        self.titleHeaderManager.enteredInHWSCB = True
        self.Lock()

    # Locks all the pages except the title header.
    def LockEvent(self, e):
        if self.gui.titleHeader.enteredInHWSCB.GetValue():
            self.Lock()
        elif e is not None:
            dlg = wx.MessageDialog(None, self.lockWarningMessage, self.lockWarningTitle, wx.YES_NO)
            res = dlg.ShowModal()
            if res==wx.ID_YES:
                for widget in self.gui.form.GetChildren():
                    widget.Enable()
                self.gui.form2_1.Enable()
                self.gui.form3.Enable()
                self.gui.form4.Enable()
                self.gui.form5.Enable()
            else:
                self.gui.titleHeader.enteredInHWSCB.SetValue(True)
        else:
            for widget in self.gui.form.GetChildren():
                widget.Enable()
            self.gui.form2_1.Enable()
            self.gui.form3.Enable()
            self.gui.form4.Enable()
            self.gui.form5.Enable()

    def Lock(self):
        for widget in self.gui.form.GetChildren():
            widget.Disable()
        self.gui.titleHeader.Enable()
        self.gui.form2_1.Disable()
        self.gui.form3.Disable()
        self.gui.form4.Disable()
        self.gui.form5.Disable()

    # Generates xml from all info from eHSN
    # Writes to file based on filePath
    def ExportAsXML(self, filePath, msg):
        if mode == "DEBUG":
            print "Saving File"

        #########################for testing without catching exceptions###################################
        pretty_xml = self.EHSNToXML() # Collects all info and puts into eTree

        if mode == "DEBUG":
            print pretty_xml
            print filePath

        output = open(filePath, 'wb')
        output.write( pretty_xml.encode('utf-8') )
        output.close()

        return pretty_xml
        ##################################################################################################


    # Creates xml tree based on eHSN values
    # Puts in human readable format
    def EHSNToXML(self):
        if mode == "DEBUG":
            print "To XML"

        #Page 1
        #Create XML Tree structure
        EHSN = Element('EHSN', version=EHSN_VERSION)

        # if hasattr(sys, '_MEIPASS'):
            # DirInfo = SubElement(EHSN, 'dirInfo')
            # DirInfo.text = (join(sys._MEIPASS, "icon_transparent.png"))

        #Title Header Branch
        TitleHeader = SubElement(EHSN, 'TitleHeader')
        self.TitleHeaderAsXMLTree(TitleHeader)

        #General Info Branch
        GenInfo = SubElement(EHSN, 'GenInfo')
        self.GenInfoAsXMLTree(GenInfo)



        #Stage Measurements Branch
        StageMeas = SubElement(EHSN, 'StageMeas')
        self.StageMeasAsXMLTree(StageMeas)

        #Discharge Measurements Branch
        DisMeas = SubElement(EHSN, 'DisMeas')
        self.DischMeasAsXMLTree(DisMeas)

        #Environment Conditions Branch
        EnvCond = SubElement(EHSN, 'EnvCond')
        self.EnvCondAsXMLTree(EnvCond)

        #Measurement Results Branch
        MeasResults = SubElement(EHSN, 'MeasResults', empty = 'False')
        self.MeasResultsAsXMLTree(MeasResults)

        #Instrument Deployment Branch
        InstrumentDeployment = SubElement(EHSN, 'InstrumentDeployment')
        self.InstrumentDepAsXMLTree(InstrumentDeployment)

        #Party Information Branch
        PartyInfo = SubElement(EHSN, 'PartyInfo')
        self.PartyInfoAsXMLTree(PartyInfo)


        #Page 2
        #LevelNotes
        LevelNotes = SubElement(EHSN, 'LevelNotes')

        #Level Checks
        LevelChecks = SubElement(LevelNotes, 'LevelChecks')
        self.LevelChecksAsXMLTree(LevelChecks)

        # #Annual Levels
        # AnnualLevels = SubElement(LevelNotes, 'AnnualLevels')
        # self.AnnualLevelsAsXMLTree(AnnualLevels)


        #Page 3
        #Checklist
        FieldReview = SubElement(EHSN, "FieldReview")
        self.FieldReviewAsXMLTree(FieldReview)


        #Page 4
        #ADCP Measurements
        MovingBoatMeas = SubElement(EHSN, "MovingBoatMeas", empty="False")
        self.MovingBoatMeasAsXMLTree(MovingBoatMeas)

        #Page 5
        #Midsection Measurements
        MidsecMeas = SubElement(EHSN, "MidsecMeas", empty="False")
        self.MidsecMeasAsXMLTree(MidsecMeas)

        #Imported
        #Midsection
        if len(self.midSectionDetailXml) != 0:
            Imported = SubElement(EHSN, "Imported")
            self.ImportedMidsectionAsXMLTree(Imported)

        #save current upload record
        if self.uploadRecord is not None:
            UploadRecord = SubElement(EHSN, "AQ_Upload_Record")
            for row in self.uploadRecord.findall('record'):
                details = []
                for col in row.getchildren():
                    details.append(col.text)
                self.UploadInfoAsXMLTree(UploadRecord, details)

            # EHSN.append(self.uploadRecord)


        doc_string = ElementTree.tostring(EHSN)
        reparsed = minidom.parseString(doc_string)
        style = reparsed.createProcessingInstruction('xml-stylesheet',
                                                     'type="text/xsl" href="WSC_EHSN.xsml"')
        root = reparsed.firstChild
        reparsed.insertBefore(style, root)
        pretty_xml = reparsed.toprettyxml(indent="\t")

        return pretty_xml




    #Read from external xml files for moving boat
    def OpenMovingBoatMmt(self, filePath):
        if mode == "DEBUG":
            print "Opening Moving Boat XML"

        winRiver = ElementTree.parse(filePath).getroot()
        # siteInformation = winRiver.find('Project').find('Site_Information')
        # dischargeSummary = winRiver.find('Project').find('Site_Discharge').find('Discharge_Summary')
        self.MovingBoatTransectFromMmt(winRiver)

    def OpenEHSNMidsection(self, filePath):

        if mode == "DEBUG":
            print "Opening File"


        EHSN = ElementTree.parse(filePath).getroot()

        MidsecMeas = EHSN.find('MidsecMeas')
        self.MidsecMeasFromXML(MidsecMeas)



    #Read xml file and place each val into text fields in eHSN
    def OpenFile(self, filePath):
        if mode == "DEBUG":
            print "Opening File"
        
        try:
            EHSN = ElementTree.parse(filePath).getroot()
            XML_version = EHSN.get('version') #get the eHSN version used to create the XML file
            
            if XML_version.split("_",1)[0] > EHSN_VERSION.split("_",1)[0]: #if eHSN version obtained from xml file is newer than user's eHSN version, display a warning
                dlg = wx.MessageDialog(self.gui, "You are attempting to open an XML file for "+XML_version+" of eHSN using "+EHSN_VERSION+" of eHSN. There is no guarantee an older version of eHSN will open the file successfully so please update to the newest version.","EHSN Version Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
        except:
            pass

        #First Page
        TitleHeader = EHSN.find('TitleHeader')
        self.TitleHeaderFromXML(TitleHeader)
 
        try:
            GenInfo = EHSN.find('GenInfo')
            self.GenInfoFromXML(GenInfo)
        except:
            dlg = wx.MessageDialog(self.gui,"The format of selected XML file is invalid.", "Invalid eHSN XML!", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return

        StageMeas = EHSN.find('StageMeas')
        self.StageMeasFromXML(StageMeas)

        DisMeas = EHSN.find('DisMeas')
        self.DischMeasFromXML(DisMeas)

        EnvCond = EHSN.find('EnvCond')
        self.EnvCondFromXML(EnvCond)

        MeasResults = EHSN.find('MeasResults')
        self.MeasResultsFromXML(MeasResults)

        InstrumentDeployment = EHSN.find('InstrumentDeployment')
        self.InstrumentDepFromXML(InstrumentDeployment) 



        PartyInfo = EHSN.find('PartyInfo')
        self.PartyInfoFromXML(PartyInfo)

        #Second Page
        LevelNotes = EHSN.find('LevelNotes')
        LevelChecks = LevelNotes.find('LevelChecks')
        self.LevelChecksFromXML(LevelChecks)

        # AnnualLevels = LevelNotes.find('AnnualLevels')
        # self.AnnualLevelsFromXML(AnnualLevels)

        #Third Page
        FieldReview = EHSN.find('FieldReview')
        self.FieldReviewFromXML(FieldReview)

        #Fourth Page
        MovingBoatMeas = EHSN.find('MovingBoatMeas')
        MovingBoatMeas = EHSN.find('ADCPMeas') if MovingBoatMeas is None else MovingBoatMeas
        self.MovingMeasFromXML(MovingBoatMeas)

        #Fifth Page
        MidsecMeas = EHSN.find('MidsecMeas')
        self.MidsecMeasFromXML(MidsecMeas)

        # for i in self.midsecMeasurementsManager.gui.table.panelObjs:
        #     i.ToString()

        #Upload Record

        self.uploadRecord = EHSN.find('AQ_Upload_Record')


        # try:
        #     MidSectionDetail = EHSN.find('Imported')
        #     if MidSectionDetail is not None:
        #         self.MidSectionDetailsFromXML(MidSectionDetail)
        # except Exception as e:
        #     print e


    def TitleHeaderAsXMLTree(self, TitleHeader):
        XMLManager.TitleHeaderAsXMLTree(TitleHeader, self.titleHeaderManager)

    def TitleHeaderFromXML(self, TitleHeader):
        XMLManager.TitleHeaderFromXML(TitleHeader, self.titleHeaderManager)


    def GenInfoAsXMLTree(self, GenInfo):
        XMLManager.GenInfoAsXMLTree(GenInfo, self.genInfoManager)

    def GenInfoFromXML(self, GenInfo):
        XMLManager.GenInfoFromXML(GenInfo, self.genInfoManager)





    def StageMeasAsXMLTree(self, StageMeas):
        XMLManager.StageMeasAsXMLTree(StageMeas, self.stageMeasManager)

    def StageMeasFromXML(self, StageMeas):
        XMLManager.StageMeasFromXML(StageMeas, self.stageMeasManager)

    def DischMeasAsXMLTree(self, DisMeas):
        XMLManager.DischMeasAsXMLTree(DisMeas, self.disMeasManager)

    def DischMeasFromXML(self, DisMeas):
        XMLManager.DischMeasFromXML(DisMeas, self.disMeasManager)


    def EnvCondAsXMLTree(self, EnvCond):
        XMLManager.EnvCondAsXMLTree(EnvCond, self.envCondManager)

    def EnvCondFromXML(self, EnvCond):
        XMLManager.EnvCondFromXML(EnvCond, self.envCondManager)


    def MeasResultsAsXMLTree(self, MeasResults):
        XMLManager.MeasResultsAsXMLTree(MeasResults, self.measResultsManager)

    def MeasResultsFromXML(self, MeasResults):
        XMLManager.MeasResultsFromXML(MeasResults, self.measResultsManager)



    def InstrumentDepAsXMLTree(self, InstrumentDeployment):
        XMLManager.InstrumentDepAsXMLTree(InstrumentDeployment, self.instrDepManager)

    def InstrumentDepFromXML(self, InstrumentDeployment):
        XMLManager.InstrumentDepFromXML(InstrumentDeployment, self.instrDepManager)


    def PartyInfoAsXMLTree(self, PartyInfo):
        XMLManager.PartyInfoAsXMLTree(PartyInfo, self.partyInfoManager)

    def PartyInfoFromXML(self, PartyInfo):
        XMLManager.PartyInfoFromXML(PartyInfo, self.partyInfoManager)


    def LevelChecksAsXMLTree(self, LevelChecks):
        XMLManager.LevelChecksAsXMLTree(LevelChecks, self.waterLevelRunManager)

    def LevelChecksFromXML(self, LevelChecks):
        XMLManager.LevelChecksFromXML(LevelChecks, self.waterLevelRunManager)
        # self.gui.LoadDefaultConfig()


    # def AnnualLevelsAsXMLTree(self, AnnualLevels):
    #     XMLManager.AnnualLevelsAsXMLTree(AnnualLevels, self.annualLevelNotesManager)

    # def AnnualLevelsFromXML(self, AnnualLevels):
    #     XMLManager.AnnualLevelsFromXML(AnnualLevels, self.annualLevelNotesManager)


    def FieldReviewAsXMLTree(self, FieldReview):
        XMLManager.FieldReviewAsXMLTree(FieldReview, self.frChecklistManager)

    def FieldReviewFromXML(self, FieldReview):
        XMLManager.FieldReviewFromXML(FieldReview, self.frChecklistManager)


    def MovingBoatMeasAsXMLTree(self, MovingBoatMeas):
        XMLManager.MovingBoatMeasAsXMLTree(MovingBoatMeas, self.movingBoatMeasurementsManager)

    def MovingMeasFromXML(self, MovingBoatMeas):
        XMLManager.MovingBoatMeasFromXML(MovingBoatMeas, self.movingBoatMeasurementsManager)


    def MidsecMeasAsXMLTree(self, MidsecMeas):
        XMLManager.MidsecMeasAsXMLTree(MidsecMeas, self.midsecMeasurementsManager)

    def MidsecMeasFromXML(self, MidsecMeas):
        XMLManager.MidsecMeasFromXML(MidsecMeas, self.midsecMeasurementsManager)

    def UploadInfoAsXMLTree(self, UploadInfo, uploadInfo):
        XMLManager.UploadInfoAsXMLTree(UploadInfo, uploadInfo)



    def MovingBoatTransectFromMmt(self, winRiver):
        date = self.genInfoManager.datePicker.split('/')
        convertedDate = date[1] + '/' + date[2] + '/' + date[0]
        XMLManager.OnImportMmt(winRiver, self.movingBoatMeasurementsManager, self.genInfoManager.stnNumCmbo, convertedDate, self.gui)


    # def ImportedMidsectionAsXMLTree(self, imported):
    #     XMLManager.MidSectionDetailsAsXMLTree(imported, self)

    def MidSectionDetailsFromXML(self, MidSectionDetail):
        XMLManager.MidSectionDetailsFromXML(MidSectionDetail, self)
    # def GenMidSectionAsXMLTreeFromHfc(self):
    #     self.midSectionDetailXml = IngestHfcManager.GenMidSectionAsXMLTree(self)


    def newEHSN(self):
        thread.start_new_thread(self.startNewEHSN(), ("new-thread", ))
    def startNewEHSN(self):
        app = wx.App()
        ElectronicHydrometricSurveyNotes()
        app.MainLoop()


    def CreateDialog(self, message):
        info = wx.MessageDialog(None, message, "Out of Update",
                                wx.OK | wx.ICON_EXCLAMATION)
        info.ShowModal()


    #return the name of the latest version of eHSN
    def find(self, names):
        for e in names:
            m = re.match("^.*_v\d+", e)
            if m:
                return e



    #compare current version to latest version of eHSN on the server
    #return false if need to be updated
    def compare(self, str1, str2):
        ver = str1.split('.')
        latest = str2.split('_')

        if int(ver[0][1:]) > int(latest[2][1:]):
            return True
        elif int(ver[0][1:]) == int(latest[2][1:]) and int(ver[1]) > int(latest[3]):
            return True
        elif int(ver[0][1:]) == int(latest[2][1:]) and int(ver[1]) == int(latest[3]) and int(ver[2]) >= int(latest[4]):
            return True
        else:
            return False

    @property
    def FlatNoteBook(self):
        return self.gui.GetFlatNoteBook()

    def GetGuiDir(self):
        return self.gui.dir

    def OnStationNumSelect(self):
        self.ProcessStationNum()

        self.stationNumProcessed = True


    def OnStationNumChange(self):
        if self.stationNumProcessed is False:
            self.ProcessStationNum()

            self.stationNumProcessed = True


    def ProcessStationNum(self):
        # Update RCVTManager with station num, then load rating file
        self.ratingCurveViewerToolManager.FindStationFile()

        # update rating curve dropdown in discharge measurements panel
        self.disMeasManager.SetCurveList(self.ratingCurveViewerToolManager.ratingCurveList)

        # attempt to calculate
        self.disMeasManager.OnUpdateHGQValues()



    #Bind the auto save event to each field from each model
    def BindAutoSave(self):
        #genInfor
        self.genInfoManager.GetStnNumCmboCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.genInfoManager.GetStnNameCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        #disMeas
        self.disMeasManager.GetStartTimeCtrl().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetEndTimeCtrl().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetStartTimeCtrl().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetEndTimeCtrl().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetAirTempCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetWaterTempCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetWidthCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetAreaCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetMeanVelCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetMghCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetDischCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetShiftCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetDiffCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.disMeasManager.GetCurveCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        #stageMeasManager
        self.stageMeasManager.GetHgCkbox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetHg2Ckbox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetWlr1Ckbox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetWlr2Ckbox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.stageMeasManager.GetStageLabelCtrl1().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetStageLabelCtrl2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetBmLeft().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetBmRight().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.stageMeasManager.GetMGHHG().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetMGHHG2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetMGHWLRefL().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetMGHWLRefR().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.stageMeasManager.GetSRCHG().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetSRCHG2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.stageMeasManager.GetGCHG().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetGCHG2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetGCWLRefL().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetGCWLRefR().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.stageMeasManager.GetCMGHHG().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetCMGHHG2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetCMGHWLRefL().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.stageMeasManager.GetCMGHWLRefR().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.stageMeasManager.GetMghMethodCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #envCondManager
        self.envCondManager.GetLevelsCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetCloudCoverCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetPrecipCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetWindMagCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetWindmagCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetBatteryCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetGasSysCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetFeedCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetBpmrotCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetBpmrotCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetIntakeTimeCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetOrificeTimeCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetIntakeCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetOrificeCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetProgramCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetDataCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetDataPeriodFromPicker().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.envCondManager.GetDataPeriodToPicker().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #measResultsManager
        self.measResultsManager.GetTimeCtrlPanel1().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel1().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel2().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel2().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel3().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel3().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel4().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel4().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorRefEntry1().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetObservedVal1().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorVal1().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorRefEntry2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetObservedVal2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorVal2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorRefEntry3().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetObservedVal3().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorVal3().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorRefEntry4().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetObservedVal4().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetSensorVal4().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        self.measResultsManager.GetCol1Combo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetCol2Combo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetReset1Combo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetReset2Combo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel7().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel7().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel8().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel8().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel9().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel9().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel10().GetHourCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.measResultsManager.GetTimeCtrlPanel10().GetMinuteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #instrDepManager

        self.instrDepManager.GetDeploymentCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetPositionMethodCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetGaugeCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetLengthRadButBox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetPosRadButBox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetGauge1RadButBox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetGauge2RadButBox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetGaugeOtherTxt().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetSerialCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetInstrumentCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetManufactureCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetModelCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetFrequencyCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetFirmwareCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetSoftwareCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetNumOfPanelsScroll().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetFlowAngleCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetCoEffCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetMethodCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetMetresCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetWeightCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetWeightRadButBox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetWeightRadBut2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetWeightRadBut1().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetConfigCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetConfigCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetAdcpSetToClockCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetDiagTestCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetAdcpDepthCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.instrDepManager.GetMagnDeclCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        # self.instrDepManager.GetControlConditionCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        # self.instrDepManager.GetDischRemarksCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        # self.instrDepManager.GetStageRemarksCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        # self.instrDepManager.GetStationHealthRemarksCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        # self.instrDepManager.GetPicturedCkbox().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #partyInfoManager
        self.partyInfoManager.GetPartyCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.partyInfoManager.GetCompleteCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.partyInfoManager.GetReviewedCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #waterLevelRunManager
        self.waterLevelRunManager.GetConventionalLevellingRb().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.waterLevelRunManager.GetTotalStationRb().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.waterLevelRunManager.GetHgText().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.waterLevelRunManager.GetHgText2().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.waterLevelRunManager.GetCommentsCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #movingBoatMeasurementsManager
        self.movingBoatMeasurementsManager.GetBedMatCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetMbCB().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetMbCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetTrackRefCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetCompositeTrackCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetLeftBankCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetLeftBankOtherCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetRightBankCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetRightBankOtherCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetEdgeDistMmntCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetDepthRefCmbo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetVelocityTopCombo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetVelocityBottomCombo().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetVelocityExponentCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetDifferenceCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetMmntStartTimeCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        # self.movingBoatMeasurementsManager.GetRawDischMeanCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetCorrMeanGHCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetStandDevMeanDischCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetMmntEndTimeCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetMbCorrAppCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetBaseCurveGHCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetCalcShiftBaseCurveCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetMmntMeanTimeCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetFinalDischCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetBaseCurveDischCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetDischDiffBaseCurveCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)
        self.movingBoatMeasurementsManager.GetCommentsCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)

        #frChecklistManager
        self.frChecklistManager.GetSiteNotesCtrl().Bind(wx.EVT_KILL_FOCUS, self.gui.OnAutoSave)


    def BindCorrectedMGH(self):
        self.disMeasManager.GetStartTimeCtrl().GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.stageMeasManager.gui.CalculateAllMGH)
        self.disMeasManager.GetStartTimeCtrl().GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.stageMeasManager.gui.CalculateAllMGH)
        self.disMeasManager.GetStartTimeCtrl().GetHourCtrl().Bind(wx.EVT_KEY_DOWN, self.stageMeasManager.gui.CalculateAllMGH)
        self.disMeasManager.GetStartTimeCtrl().GetMinuteCtrl().Bind(wx.EVT_KEY_DOWN, self.stageMeasManager.gui.CalculateAllMGH)

        self.disMeasManager.GetEndTimeCtrl().GetHourCtrl().Bind(wx.EVT_COMBOBOX, self.stageMeasManager.gui.CalculateAllMGH)
        self.disMeasManager.GetEndTimeCtrl().GetMinuteCtrl().Bind(wx.EVT_COMBOBOX, self.stageMeasManager.gui.CalculateAllMGH)
        self.disMeasManager.GetEndTimeCtrl().GetHourCtrl().Bind(wx.EVT_KEY_DOWN, self.stageMeasManager.gui.CalculateAllMGH)
        self.disMeasManager.GetEndTimeCtrl().GetMinuteCtrl().Bind(wx.EVT_KEY_DOWN, self.stageMeasManager.gui.CalculateAllMGH)


    #Ingest from QRev *.xml
    def GetStationIDFromQRev(self):
        return IngestQRevManager.GetStationID(self.GetQRevDir())

    def GetDateFromQRev(self):
        return IngestQRevManager.GetDate(self.GetQRevDir())





    def AddMovingBoatFromQRev(self, evt):
        IngestQRevManager.AddMovingBoat(self.GetQRevDir(), self.movingBoatMeasurementsManager, evt)

    def AddDischargeSummaryFromQRev(self):
        IngestQRevManager.AddDischargeSummary(self.GetQRevDir(), self.disMeasManager)

    def AddDischargeDetailFromQRev(self):
        IngestQRevManager.AddDischargeDetail(self.GetQRevDir(), self.instrDepManager)

    # def OpenDisFromFlowTracker(self, evt):
    #     IngestFlowTrackerDisManager.OpenDis(self.GetFlowTrackerDir(), self.disMeasManager, self.instrDepManager, evt)
    #     self.gui.disMeas.onTimeChange(evt)


    #Ingest from FlowTracker *.dis
    def AddDischargeSummaryFromFT(self):
        IngestFlowTrackerDisManager.AddDischargeSummary(self.GetFlowTrackerDir(), self.disMeasManager)

    def AddDischargeDetailFromFT(self):
        IngestFlowTrackerDisManager.AddDischargeDetail(self.GetFlowTrackerDir(), self.instrDepManager)


    def GetStationIdFromFlowTrackerDis(self):
        return IngestFlowTrackerDisManager.GetStationID(self.GetFlowTrackerDir())

    def GetDateFromFlowTrackerDis(self):
        return IngestFlowTrackerDisManager.GetDate(self.GetFlowTrackerDir())

    def GetMidSectionInfoFromFT(self):
        return IngestFlowTrackerDisManager.GetMidSectionInfo(self.GetFlowTrackerDir(), self)

    def GetRawDataFromFT(self):
        # rData = IngestFlowTrackerDisManager.GetRawData(self.GetFlowTrackerDir())
        rData = IngestFlowTrackerDisManager.GetRawDataSet(self.GetFlowTrackerDir())
        return rData




    #Ingest from HFC *.MQ*
    def AddDischargeSummaryFromHfc(self):
        IngestHfcManager.AddDischargeSummary(self.GetHfcDir(), self.disMeasManager, self.instrDepManager)

    def AddDischargeDetailFromHfc(self):
        IngestHfcManager.AddDischargeDetail(self.GetHfcDir(), self.instrDepManager)


    def GetStationIdFromHfc(self):
        return IngestHfcManager.GetStationID(self.GetHfcDir())

    def GetDateFromHfc(self):
        return IngestHfcManager.GetDate(self.GetHfcDir())


    def GetStationIdFromMidsection(self):
        return IngestHfcManager.GetStationID(self.GetHfcDir())

    def GetDateFromMidsection(self):
        return IngestHfcManager.GetDate(self.GetHfcDir())



    #HFC for MidSection
    def GetDateSpreadsheetFormatFromHfc(self):
        return IngestHfcManager.GetDateSpreadsheetFormat(self.GetHfcDir())


    def GetDeploymentMethodFromHfc(self):
        return IngestHfcManager.GetDeploymentMethod(self.GetHfcDir())
    def GetMeasurementSectionConditionFromHfc(self):
        return IngestHfcManager.GetMeasurementSectionCondition(self.GetHfcDir())
    def GetTotalDischargeFromHfc(self):
        return IngestHfcManager.GetTotalDischarge(self.GetHfcDir())
    def GetTotalAreaFromHfc(self):
        return IngestHfcManager.GetTotalArea(self.GetHfcDir())
    def GetTotalWidthFromHfc(self):
        return IngestHfcManager.GetTotalWidth(self.GetHfcDir())
    def GetMeanVelocityFromHfc(self):
        return IngestHfcManager.GetMeanVelocity(self.GetHfcDir())
    def GetMeanDepthFromHfc(self):
        return IngestHfcManager.GetMeanDepth(self.GetHfcDir())
    def GetSerialNumberFromHfc(self):
        return IngestHfcManager.GetSerialNumber(self.GetHfcDir())
    def GetMeasuredByFromHfc(self):
        return IngestHfcManager.GetMeasuredBy(self.GetHfcDir())
    def GetCalculationMethodFromHfc(self):
        return IngestHfcManager.GetCalculationMethod(self.GetHfcDir())

    def GetWaterTemperatureFromHfc(self):
        return IngestHfcManager.GetWaterTemperature(self.GetHfcDir())
    def GetAirTemperatureFromHfc(self):
        return IngestHfcManager.GetAirTemperature(self.GetHfcDir())
    def GetInitialPointFromHfc(self):
        return IngestHfcManager.GetInitialPoint(self.GetHfcDir())
    def GetStartingPointFromHfc(self):
        return IngestHfcManager.GetStartingPoint(self.GetHfcDir())
    def GetConditionFromHfc(self):
        return IngestHfcManager.GetCondition(self.GetHfcDir())
    def GetImportFileSoftwareNameFromHfc(self):
        return IngestHfcManager.GetImportFileSoftwareName(self.GetHfcDir())



    def GetPanelDatesFromHfc(self):
        return IngestHfcManager.GetPanelDates(self.GetHfcDir())
    def GetTaglinePositionsFromHfc(self):
        return IngestHfcManager.GetTaglinePositions(self.GetHfcDir())
    def GetDistanceToShoresFromHfc(self):
        return IngestHfcManager.GetDistanceToShores(self.GetHfcDir())
    def GetDepthReadingsFromHfc(self):
        return IngestHfcManager.GetDepthReadings(self.GetHfcDir())
    def GetWidthsFromHfc(self):
        return IngestHfcManager.GetWidths(self.GetHfcDir())
    def GetAreasFromHfc(self):
        return IngestHfcManager.GetAreas(self.GetHfcDir())
    def GetAverageVelocitiesFromHfc(self):
        return IngestHfcManager.GetAverageVelocities(self.GetHfcDir())
    def GetDischargesFromHfc(self):
        return IngestHfcManager.GetDischarges(self.GetHfcDir())
    def GetMeterNamesFromHfc(self):
        return IngestHfcManager.GetMeterNames(self.GetHfcDir())
    def GetAmountOfWeightsFromHfc(self):
        return IngestHfcManager.GetAmountOfWeights(self.GetHfcDir())
    def GetDistanceAboveWeightsFromHfc(self):
        return IngestHfcManager.GetDistanceAboveWeights(self.GetHfcDir())
    def GetVelocityMethodsFromHfc(self):
        return IngestHfcManager.GetVelocityMethods(self.GetHfcDir())
    def GetDepthsFromHfc(self):
        return IngestHfcManager.GetDepths(self.GetHfcDir())
    def GetVelocitysFromHfc(self):
        return IngestHfcManager.GetVelocitys(self.GetHfcDir())
    def GetCountsFromHfc(self):
        return IngestHfcManager.GetCounts(self.GetHfcDir(), self)
    def GetIntervalsFromHfc(self):
        return IngestHfcManager.GetIntervals(self.GetHfcDir())
    def GetDistanceToNextShoresFromHfc(self):
        return IngestHfcManager.GetDistanceToNextShores(self.GetHfcDir())
    def GetIslandWidthsFromHfc(self):
        return IngestHfcManager.GetIslandWidths(self.GetHfcDir(), self)

    def GetMidSectionInfoFromHfc(self):
        return IngestHfcManager.GetMidSectionInfo(self.GetHfcDir(), self)



    #Ingest from FlowTracker2 (*.json)
    def AddDischargeSummaryFromFt2(self):
        IngestFt2Manager.AddDischargeSummary(self.GetFT2JsonDir(), self.disMeasManager)

    def AddDischargeDetailFromFt2(self):
        IngestFt2Manager.AddDischargeDetail(self.GetFT2JsonDir(), self.instrDepManager) 


    def GetStationIdFromFt2(self):
        return IngestFt2Manager.GetStationID(self.GetFT2JsonDir())

    def GetDateFromFt2(self):
        return IngestFt2Manager.GetDate(self.GetFT2JsonDir())

    def GetLocalTimeUtcOffsetFromFt2(self):
        return IngestFt2Manager.GetLocalTimeUtcOffset(self.GetFT2JsonDir())

    #Ingest from Sxs (*.mmt)
    def AddDischargeSummaryFromSxs(self):
        IngestSxsManager.AddDischargeSummary(self.GetSxsDir(), self.disMeasManager)

    def AddDischargeDetailFromSxs(self):
        IngestSxsManager.AddDischargeDetail(self.GetSxsDir(), self.instrDepManager, self.disMeasManager) 


    def GetStationIdFromSxs(self):
        return IngestSxsManager.GetStationID(self.GetSxsDir())

    def GetDateFromSxs(self):
        return IngestSxsManager.GetDate(self.GetSxsDir())


    #Ingest from RSSL (*.dis)
    def AddDischargeSummaryFromRssl(self):
        IngestRSSLDisManager.AddDischargeSummary(self.GetRsslDir(), self.disMeasManager)

    def AddDischargeDetailFromRssl(self):
        IngestRSSLDisManager.AddDischargeDetail(self.GetRsslDir(), self.instrDepManager, self.disMeasManager) 


    def GetStationIdFromRssl(self):
        return IngestRSSLDisManager.GetStationID(self.GetRsslDir())

    def GetDateFromRssl(self):
        return IngestRSSLDisManager.GetDate(self.GetRsslDir())


    def GetStationIdFromEhsnMidsection(self):
        EHSN = ElementTree.parse(self.GetEhsnMidDir()).getroot()

        TitleHeader = EHSN.find('TitleHeader')
        self.TitleHeaderFromXML(TitleHeader)
 
        try:
            GenInfo = EHSN.find('GenInfo')

        except:
            dlg = wx.MessageDialog(self.gui, "The format of selected XML file is invalid.", "Invalid eHSN XML!", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return
        return XMLManager.GetStationId(GenInfo)


    def GetDateFromEhsnMidsection(self):
        EHSN = ElementTree.parse(self.GetEhsnMidDir()).getroot()

        TitleHeader = EHSN.find('TitleHeader')
        self.TitleHeaderFromXML(TitleHeader)
 
        return XMLManager.GetDate(EHSN.find('GenInfo'))



    def GetQRevDir(self):
        return self.gui.qRevDir

    def GetFlowTrackerDir(self):
        return self.gui.flowTrackerDir

    def GetHfcDir(self):
        return self.gui.hfcDir

    def GetFT2JsonDir(self):
        return self.gui.ft2JsonDir

    def GetSxsDir(self):
        return self.gui.sxsDir

    def GetRsslDir(self):
        return self.gui.rsslDir

    def GetEhsnMidDir(self):
        return self.gui.ehsnMidDir


    # def SetMidSectionDetailXml(self, midSection):
    #     self.midSectionDetailXml = midSection

    def GetMidSectionDetailXml(self):
        return self.midSectionDetailXml

    def GetMidSectionRawData(self):
        return self.midSectionRawData

    def SetMidSectionRawData(self, midSectionRawData):
        self.midSectionRawData = midSectionRawData
        ####Write to local disk for uploading to NG#######
        # f = open('C:\\Users\\zhangwen\\Desktop\\test.dis', 'w')
        # for i in midSectionRawData:
        #     for j in i:
        #         f.write(str(j) + " ")
        #     f.write("\n")
        # f.close()
        #######################################################



    def Increament(self):
        self.resizingLock.acquire()
        self.gui.ApplyFontToChildren(self.gui, 1)
        self.gui.ChangeFontToMidsectionGrid(1)
        self.resizingLock.release()

        



    def Decreament(self):
        self.resizingLock.acquire()
        self.gui.ApplyFontToChildren(self.gui, -1)
        self.gui.ChangeFontToMidsectionGrid(-1)
        self.resizingLock.release()



    def OnKeyDownEvent(self, event):
        if event.GetKeyCode() == 308:
            self.ctrlKeyDownFlag = True
        elif event.GetKeyCode() == 45 and self.ctrlKeyDownFlag:
            t = threading.Thread(target=self.Decreament(), args=(1,))
            t.start()
            
        elif event.GetKeyCode() == 61 and self.ctrlKeyDownFlag:
            t = threading.Thread(target=self.Increament(), args=(1,))
            t.start()
        event.Skip()
            
        return True



    def OnKeyUpEvent(self, event):
        if event.GetKeyCode() == 308:
            self.ctrlKeyDownFlag = False
        event.Skip()
        return True




# This is for the icon 
filename = 'myfilesname.type'
if hasattr(sys, '_MEIPASS'):
    # PyInstaller >= 1.6
    chdir(sys._MEIPASS)
    filename = join(sys._MEIPASS, filename)
elif '_MEIPASS2' in environ:
    # PyInstaller < 1.6 (tested on 1.5 only)
    chdir(environ['_MEIPASS2'])
    filename = join(environ['_MEIPASS2'], filename)
else:
    chdir(dirname(sys.argv[0]))
    filename = join(dirname(sys.argv[0]), filename)





def main():
    gui = ElectronicHydrometricSurveyNotes()


if __name__=='__main__':
    main()
