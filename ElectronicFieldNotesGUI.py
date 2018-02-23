# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from TitleHeaderPanel import *
from GenInfoPanel import *
from DischargeMeasurementsPanel import *
from StageMeasurementsPanel import *
from EnvironmentConditionsPanel import *
from MeasurementResultsPanel import *
from InstrumentDeploymentInfoPanel import *
from PartyInfoPanel import *
# from AnnualLevellingPanel import *
from WaterLevelRunPanel import *
from FRChecklistPanel import *
from MovingBoatMeasurementsPanel import *
from MidSectionMeasurementsPanel import *
from CalcPanel import *
from AquariusUploadDialog import *

from ConfigPanel import *
# from RatingCurveExtractionToolFrame import *
from AQUARIUSDataExtractionToolFrame import *
from RatingCurveViewerToolFrame import *
# from AquariusUploadDialog2 import *
import VersionCheck
import wx.lib.scrolledpanel as scrolledpanel
import wx.lib.agw.flatnotebook as fnb
import os
import sys
import datetime
from wx import adv
import thread
import os.path
import multiprocessing
import csv
from xml.etree.ElementTree import Element
import wx.lib.agw.zoombar as zb
import qrcode
# import painting

ID_FILE_NEW = wx.NewId()
ID_FILE_OPEN = wx.NewId()
ID_FILE_SAVE = wx.NewId()
ID_FILE_EXIT = wx.NewId()
ID_FILE_EXPORT_PDF = wx.NewId()
ID_FILE_EXPORT_PDF_SUMM = wx.NewId()
ID_FILE_EXPORT_PDF_VIEW = wx.NewId()
ID_FILE_EXPORT_XML = wx.NewId()
ID_FILE_EXPORT_AQUARIUS = wx.NewId()
ID_EDIT_PREF = wx.NewId()
ID_HELP_ABOUT = wx.NewId()
ID_HELP_EHELP = wx.NewId()
ID_HELP_UPDATE = wx.NewId()
ID_CONF_CONF = wx.NewId()
ID_CONF_ADET = wx.NewId()
# ID_IMPORT_DIS = wx.NewId()
# ID_IMPORT_XML = wx.NewId()
ID_TOOLS_CALC = wx.NewId()
ID_TOOLS_RCVT = wx.NewId()
ID_FILE_SAVE_EXIT = wx.NewId()
# ID_TOOLS_DRAW = wx.NewId()


# def resource_path(relative):
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative)
#     return os.path.join(relative)



class SpecialScrolledPanel(scrolledpanel.ScrolledPanel):
    def OnChildFocus(event, other):
        pass

class EHSNGui(wx.Frame):
    def __init__(self, mode, ver, *args, **kwargs):
        super(EHSNGui, self).__init__(*args, **kwargs)


        self.version = ver
        self.noteHeaderTxt = "Hydrometric Survey Notes" + " " + self.version
        self.timezone = ""
        self.lang = wx.LANGUAGE_ENGLISH
        self.mode = mode
        self.name = ""
        self.fullname = ""

        # self.dir = os.getcwd()
        # print self.dir
        self.dir = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.uploadDir = self.dir
        self.ratingFileDir = self.dir + '\\AQ_Extracted_Data'
        self.saveDir = self.dir
        self.scriptLoc = 'EHSN_rating_curve.exe'
        if hasattr(sys, '_MEIPASS'):
            self.scriptLoc = os.path.join(sys._MEIPASS, self.scriptLoc)
        else:
            self.scriptLoc = os.getcwd() + "\\" + self.scriptLoc
        # Label variables
        self.fNewLabel = 'New\tCtrl+N'
        self.fNewDesc = 'Start a new eHSN application'
        self.fOpenLabel = '&Open\tCtrl+O'
        self.fOpenDesc = "Open an existing field note (this will be in XML format)"
        self.fXmlLabel = '&Save As\tCtrl+A'
        self.fXmlDesc = 'Save the current eHSN field note as an XML file.'
        self.fSaveLabel = 'Save\tCtrl+S'
        self.fSaveDesc = 'Save the current eHSN field note as an XML file.'
        self.fPdfLabel = 'Generate PDF - Complete Note\tCtrl+P'
        self.fPdfDesc = 'Generate a PDF of the current field note in the same size format as previous paper field notes.'
        self.fPdfsLabel = "Generate PDF - Front Page Only"
        self.fPdfsDesc = "Generate a PDF of the front page of the current field note(good for providing to partners and clients)."
        self.fPdfvLabel = "Generate PDF - Complete Note on Full Page"
        self.fPdfvDesc = "Generate pdf for the current field visit as 8.5 x 11 size format."
        self.fAquLabel = '&Upload eHSN to AQUARIUS\tCtrl+U'
        self.fAquDesc = 'Upload this Field Visit\'s information to AQUARIUS'
        self.fExitLabel = '&Quit\tCtrl+Q'
        self.fExitDesc = 'Exit Program'
        self.hAboutLabel = '&About'
        self.hAboutDesc = 'About eHSN'
        self.heHelpLabel = 'eHSN &Help'
        self.fSaveExitLabel = 'Save && Exit\tCtrl+E'
        self.fSaveExitDesc = 'Save and Exit'
        self.heHelpDesc = "Instructions for the completion of eHSN"
        self.tCalcLabel = "Calculator"
        self.tCalcDesc = "A simple calculator."
        self.iDisLabel = 'Import MB ADCP (*.dis) Files'
        self.iDisDesc = 'Import MB ADCP (*.dis) Files'
        self.iMmtLabel = 'Import MB ADCP (*.mmt) Files'
        self.iMmtDesc = 'Import MB ADCP (*.mmt) Files'
        self.cConfLabel = 'Configure Stations, Meters and BM/Ref file locations'
        self.cConfDesc = 'Optionally set the file locations for the stations metadata, meters, and Bench Mark configuration Files.'
        self.tRcvtLabel = 'Rating Curve Viewer Tool'
        self.tRcvtDesc = 'use this tool to view your measurement in comparison to previous discharge measurements graphically, as well as the shift and % differences from the curve.'
        self.cAdetLabel = 'AQUARIUS Data Extraction Tool'
        self.cAdetDesc = 'Run this tool first while in the office. It will extract data from AQUARIUS so you can take it into the field.'
        self.hUpdatelabel = 'Updates/Messages'
        self.hUpdateDesc = 'Update eHSN'
        self.fullStyleSheetFileName = 'WSC_EHSN.xsml'
        self.summStyleSheetFileName = 'WSC_EHSN_Summary.xsml'
        self.viewStyleSheetFileName = 'WSC_EHSN_VIEW.xsml'
        # self.stylesheetPath = "Saved Field Visits"

        self.fileSaveTitle = 'Save As'
        self.fileSavePDFStylesheetMessage = "Stylesheet not found, please locate stylesheet file: " + self.fullStyleSheetFileName
        self.fileSavePDFStylesheetTitle = "Locate Stylesheet"
        self.fileSavePDFStylesheetSummMessage = "Stylesheet not found, please locate stylesheet file: " + self.summStyleSheetFileName
        self.fileSavePDFStylesheetViewMessage = "Stylesheet not found, please locate stylesheet file: " + self.viewStyleSheetFileName
        self.fileSavePDFSaveTitle = 'Export Survey'
        self.fileOpenTitle = 'Open'
        self.fileExitMessage = 'Save Hydrometric Field Notes before exit?'
        self.fileExitTitle = 'Save before exit?'
        self.fileAQStnMessage = "Please enter a Station Number"
        self.fileAQStnTitle = "Information"
        self.fileAQTZMessage = "Please select timezone"
        self.fileAQTZTitle = "Information"
        self.fileAQUploadTitle = "Upload eHSN to AQUARIUS"
        self.fileAQUpSuccessMessage = "Upload Successful!"
        self.fileAQUpSuccessTitle = "Upload Complete"
        self.errorTitle = "Error"
        self.fileOpenMessage = "Do you want to save the changes?"

        self.helpAboutTitle = 'Hydrometric Field Notes'
        self.helpAboutBaseDesc = 'Version: '
        self.helpHelpTitle = "Hydrometric Field Notes Help"
        self.helpHelpMessage = "The help documentation and SOP for the eHSN is currently available in " \
                               "the pdf document packaged with this release as well as the NHS ecollab library."

        self.movingBoatOpenTitle = 'Open a saved moving boat from an external file'
        self.saveBeforeUploadDesc = 'Do you want to save before uploading to AQUARIUS'
        self.noSaveBeforeUploadMsg = 'Continue Without Saving'
        self.saveBeforeUploadTitle = 'Save before uploading'
        self.iconName = "icon_transparent.ico"
        self.logoName = "icon_transparent.jpg"
        self.closeRCVDesc = "Please close the plot window first"
        self.closeRCVTitle = "Message from Rating Curve View Tool"
        self.startTimeErrorMsg = "Start & end time cannot be '00:00'"
        self.qrName = "qr.jpg"
        self.icon_path = self.iconName
        self.qr_path = self.qrName
        self.logo_path = self.logoName
        self.uploadOpenPdf = False


        self.path = ''
        self.savedName = ''
        self.savedPassword = ''

        self.savedStationsPath = ''
        self.savedMetersPath = ''
        self.savedLevelsPath = ''


        self.notReviewedUploadWarning = """There is no indication that this field note has been reviewed. Please ensure this field note has been reviewed, and that the "Reviewed" checkbox at the bottom of the Front Page has been checked."""

        self.RatingCurveViewerToolFrame = None
        self.ratingCurveExtraction = None
        self.calc = None
        self.config = None

        self.manager = None
        self.configpath = ''

        # subprocess.Popen([file],shell=True)
        os.chdir(self.dir)

        self.numsRead = []
        self.namesRead = []
        self.tz = []

        self.stationLevel = []
        self.bm = []
        self.ele = []
        self.desc = []

        self.bmIndex = []


        self.serialNumbers = []
        self.instrumentTypes = []
        self.manufactruers = []
        self.models = []
        self.frequencies = []
        self.firmware = []



        self.emptyStation = False
        self.emptyMeter = False
        self.emptyLevel = False

        self.InitUI()


        self.Show(True)

        self.Update()
        self.Refresh()




    def InitUI(self):
        if self.mode=="DEBUG":
            print "Setup the Frame"

        self.locale = wx.Locale(self.lang)

        self.CreateStatusBar(style=wx.STB_SIZEGRIP|wx.STB_SHOW_TIPS|wx.STB_ELLIPSIZE_END|wx.FULL_REPAINT_ON_RESIZE)
        self.SetStatusText("Welcome to the Hydrometric Survey Notes")

        fileMenu = wx.Menu()
        fnew = fileMenu.Append(ID_FILE_NEW, self.fNewLabel, self.fNewDesc)
        fopen = fileMenu.Append(ID_FILE_OPEN, self.fOpenLabel, self.fOpenDesc)
        fileMenu.AppendSeparator()
        fsave = fileMenu.Append(ID_FILE_SAVE, self.fSaveLabel, self.fXmlDesc)
        fxml = fileMenu.Append(ID_FILE_EXPORT_XML, self.fXmlLabel, self.fXmlDesc)
        fileMenu.AppendSeparator()
        fpdf = fileMenu.Append(ID_FILE_EXPORT_PDF, self.fPdfLabel, self.fPdfDesc)
        fpdfs = fileMenu.Append(ID_FILE_EXPORT_PDF_SUMM, self.fPdfsLabel, self.fPdfsDesc)
        fileMenu.AppendSeparator()
        fpdfview = fileMenu.Append(ID_FILE_EXPORT_PDF_VIEW, self.fPdfvLabel, self.fPdfvDesc)
        fileMenu.AppendSeparator()
        faqu = fileMenu.Append(ID_FILE_EXPORT_AQUARIUS, self.fAquLabel, self.fAquDesc)
        fileMenu.AppendSeparator()
        # fsexit = fileMenu.Append(ID_FILE_SAVE_EXIT, self.fSaveExitLabel, self.fSaveExitDesc)
        fsexit = fileMenu.Append(wx.MenuItem(fileMenu, ID_FILE_SAVE_EXIT, self.fSaveExitLabel, self.fSaveExitDesc))
        fexit = wx.MenuItem(fileMenu, ID_FILE_EXIT, self.fExitLabel, self.fExitDesc)
        fileMenu.Append(fexit)
        # fexit = fileMenu.Append(ID_FILE_EXIT, self.fExitLabel, self.fExitDesc)


        configMenu = wx.Menu()

        cConfig = configMenu.Append(ID_CONF_CONF, self.cConfLabel, self.cConfDesc)

        # importMenu.AppendSeparator()
        # iMmt = importMenu.Append(ID_IMPORT_XML, self.iMmtLabel, self.iMmtDesc)
        # iDis = importMenu.Append(ID_IMPORT_DIS, self.iDisLabel, self.iDisDesc)

        toolMenu = wx.Menu()
        cAdet = toolMenu.Append(ID_CONF_ADET, self.cAdetLabel, self.cAdetDesc)
        tRcvt = toolMenu.Append(ID_TOOLS_RCVT, self.tRcvtLabel, self.tRcvtDesc)
        toolMenu.AppendSeparator()
        tCalc = toolMenu.Append(ID_TOOLS_CALC, self.tCalcLabel, self.tCalcDesc)
        # tSkatch = toolMenu.Append(ID_TOOLS_DRAW, "Paint", "Draw")




        # editMenu = wx.Menu()
        # epref = editMenu.Append(ID_EDIT_PREF, '&Preferences', "Edit eHSN Preferences (Currently does nothing)")

        helpMenu = wx.Menu()

        habout = helpMenu.Append(ID_HELP_ABOUT, self.hAboutLabel, self.hAboutDesc)
        hehelp = helpMenu.Append(ID_HELP_EHELP, self.heHelpLabel, self.heHelpDesc)
        helpMenu.AppendSeparator()
        hupdate = helpMenu.Append(ID_HELP_UPDATE, self.hUpdatelabel, self.hUpdateDesc)



        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(configMenu, '&Configuration')
        menuBar.Append(toolMenu, '&Tools')
        # menuBar.Append(editMenu, '&Edit')
        menuBar.Append(helpMenu, '&Help')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNew, fnew)
        self.Bind(wx.EVT_MENU, self.OnFileOpen, fopen)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAs, fxml)
        self.Bind(wx.EVT_MENU, self.OnFileSave, fsave)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAsPDF, fpdf)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAsPDFSumm, fpdfs)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAsPDFView, fpdfview)
        self.Bind(wx.EVT_MENU, self.OnAquariusUpload, faqu)
        self.Bind(wx.EVT_MENU, self.OnFileExit, fexit)
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, habout)
        self.Bind(wx.EVT_MENU, self.OnHelpEHelp, hehelp)
        self.Bind(wx.EVT_CLOSE, self.OnFileExit)
        self.Bind(wx.EVT_MENU, self.OnCalc, tCalc)
        # self.Bind(wx.EVT_MENU, self.OnImportMovingBoaiMmt, iMmt)
        self.Bind(wx.EVT_MENU, self.OnConfig, cConfig)
        # self.Bind(wx.EVT_MENU, self.OnMovingBoaiDis, iDis)
        self.Bind(wx.EVT_MENU, self.OnRatingCurveViewerToolFrame, tRcvt)
        self.Bind(wx.EVT_MENU, self.OnAQUARIUSDataExtractionToolFrame, cAdet)
        self.Bind(wx.EVT_MENU, self.OnUpdate, hupdate)
        self.Bind(wx.EVT_MENU, self.OnSaveExit, fsexit)
        # self.Bind(wx.EVT_MENU, self.OnDraw, tSkatch)
        self.layout = None

        #Icon Path

        if hasattr(sys, '_MEIPASS'):
            self.qr_path = os.path.join(sys._MEIPASS, self.qr_path)
            self.icon_path = os.path.join(sys._MEIPASS, self.icon_path)
            self.logo_path = os.path.join(sys._MEIPASS, self.logo_path)
        else:
            self.qr_path = os.path.join(self.dir, self.qr_path)
            self.icon_path = os.path.join(self.dir, self.icon_path)
            self.logo_path = os.path.join(self.dir, self.logo_path)


        if os.path.exists(self.icon_path):
            png = wx.Image(self.icon_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.icon = wx.Icon(png)
            self.SetIcon(self.icon)
        self.CreateFrames()



    def CreateFrames(self):

        if self.layout is not None:
            self.layout.Show(False)
            self.layout.Destroy()

        self.layout = fnb.FlatNotebook(self, style=wx.NB_TOP, agwStyle=fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_NAV_BUTTONS)

        #First Page
        formSizer = wx.BoxSizer(wx.VERTICAL)
        self.form = SpecialScrolledPanel(self.layout, style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.form.SetupScrolling()

        self.titleHeader = TitleHeaderPanel(self.mode, self.form, style=wx.NO_BORDER)
        self.genInfo = GenInfoPanel(self.mode, self.form, style=wx.SIMPLE_BORDER)
        self.disMeas = DischargeMeasurementsPanel(self.mode, self.lang, self.form, style=wx.SIMPLE_BORDER)

        midSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.stageMeas = StageMeasurementsPanel(self.mode, self.lang, self.form, style=wx.BORDER_NONE, size=(-1, -1))


        self.envCond = EnvironmentConditionsPanel(self.mode, self.form, style=wx.SIMPLE_BORDER, size=(1, -1))

        midSizer.Add(self.stageMeas, 14, wx.EXPAND)
        midSizer.Add(self.envCond, 6, wx.EXPAND)

        self.measResults = MeasurementResultsPanel(self.mode, self.lang, self.form, style=wx.SIMPLE_BORDER, size=(1, -1))

        self.instrDep = InstrumentDeploymentInfoPanel(self.mode, self.form, style=wx.SIMPLE_BORDER, size=(720, -1))
        # self.instrDep.methodCBListBox.Bind(wx.EVT_CHECKLISTBOX, self.OnAdcpMid)
        # self.instrDep.instrumentCmbo.Bind(wx.EVT_COMBOBOX, self.OnAdcpMid)
        # self.instrDep.methodCBListBox.Bind(wx.EVT_CHECKLISTBOX, self.instrDep.OnDeploymentCheckListCB)

        self.partyInfo = PartyInfoPanel(self.mode, self.form, style=wx.BORDER_NONE, size=(-1, 32))

        formSizer.Add(self.titleHeader, 0, wx.EXPAND|wx.ALL, 3)
        formSizer.Add(self.genInfo, 0, wx.EXPAND|wx.ALL, 3)
        formSizer.Add(self.disMeas, 0, wx.EXPAND|wx.ALL, 3)
        formSizer.Add(midSizer, 0, wx.EXPAND|wx.ALL, 3)
        formSizer.Add(self.measResults, 0, wx.EXPAND|wx.ALL, 3)
        formSizer.Add(self.instrDep, 0, wx.EXPAND|wx.ALL, 3)
        formSizer.Add(self.partyInfo, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 3)

        self.form.SetSizerAndFit(formSizer)


        #Second Page
        self.form2 = fnb.FlatNotebook(self.layout, style=wx.NB_TOP, agwStyle=fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_NAV_BUTTONS)
        #Hidding Annual Levelling tabs
        self.form2.HideTabs()

        form2_1 = wx.Panel(self.form2, style=wx.SIMPLE_BORDER)
        form2_1Sizer = wx.BoxSizer(wx.VERTICAL)

        self.waterLevelRun = WaterLevelRunPanel(self.mode, self.lang, self.dir, form2_1, style=wx.BORDER_NONE)

        form2_1Sizer.Add(self.waterLevelRun, 1, wx.EXPAND)
        form2_1.SetSizerAndFit(form2_1Sizer)


        # form2_2 = SpecialScrolledPanel(form2, style=wx.SIMPLE_BORDER)
        # form2_2.SetupScrolling()

        # form2_2Sizer = wx.BoxSizer(wx.VERTICAL)
        # self.annualLevelNotes = AnnualLevellingPanel(self.mode, form2_2, style=wx.SIMPLE_BORDER, size=(1, -1))
        # form2_2Sizer.Add(self.annualLevelNotes, 0, wx.EXPAND)
        # form2_2.SetSizerAndFit(form2_2Sizer)


        self.form2.AddPage(form2_1, "Level Checks")
        # form2.AddPage(form2_2, "Annual levelling")




        #Moving Boat Page
        form3Sizer = wx.BoxSizer(wx.VERTICAL)
        self.form3 = SpecialScrolledPanel(self.layout, style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.form3.SetupScrolling()

        self.movingBoatMeasurements = MovingBoatMeasurementsPanel(self.mode, self.lang, self.form3, style=wx.SIMPLE_BORDER, size=(1, -1))

        form3Sizer.Add(self.movingBoatMeasurements, 1, wx.EXPAND)
        self.form3.SetSizerAndFit(form3Sizer)

        #Midsec Page
        form4Sizer = wx.BoxSizer(wx.VERTICAL)
        self.form4 = SpecialScrolledPanel(self.layout, style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.form4.SetupScrolling()

        self.midsecMeasurements = MidSectionMeasurementsPanel(self.mode, self.lang, self.form4, style=wx.SIMPLE_BORDER, size=(1, -1))

        form4Sizer.Add(self.midsecMeasurements, 1, wx.EXPAND)
        self.form4.SetSizerAndFit(form4Sizer)


        #Checklist third page
        form5Sizer = wx.BoxSizer(wx.VERTICAL)
        self.form5 = SpecialScrolledPanel(self.layout, style=wx.SIMPLE_BORDER|wx.VSCROLL)
        self.form5.SetupScrolling()

        self.frChecklist = FRChecklistPanel(self.mode, self.form5, style=wx.SIMPLE_BORDER, size=(1, -1))

        form5Sizer.Add(self.frChecklist, 1, wx.EXPAND)
        self.form5.SetSizerAndFit(form5Sizer)

        # #Config page
        # form6Sizer = wx.BoxSizer(wx.VERTICAL)
        # form6 = SpecialScrolledPanel(self.layout, style=wx.SIMPLE_BORDER|wx.VSCROLL)
        # form6.SetupScrolling()

        # self.userConfig = UserConfigPanel(self.mode, self.lang, form6, style=wx.SIMPLE_BORDER, size=(1, -1))
        # self.userConfig.stationOpenButton.Bind(wx.EVT_BUTTON, self.OnOpenPress)

        # form6Sizer.Add(self.userConfig, 1, wx.EXPAND)
        # form6.SetSizerAndFit(form6Sizer)

        self.layout.AddPage(self.form, "Front Page")
        self.layout.AddPage(self.form2, "Level Notes")
        self.layout.AddPage(self.form3, "Moving Boat")
        self.layout.AddPage(self.form4, "Mid-section")
        self.layout.AddPage(self.form5, "Field Review")
        # self.layout.AddPage(form6, "User Config")
        self.layout.Show(True)
        self.Show(True)
        self.layout.Layout()
        self.layout.Fit()
        self.SendSizeEvent()
        self.Update()
        self.Refresh()
        self.Layout()


        self.genInfo.stnNumCmbo.Bind(wx.EVT_TEXT, self.OnStationSelect)
        self.genInfo.stnNameCtrl.Bind(wx.EVT_TEXT, self.OnStationNameSelect)

        # self.LoadDefaultConfig()



    #Auto save an xml file in the the same directory of the eHSN folder for every seperate model
    #(the event will be placed on each common filed for each model, after the focus leaving the event will be triggered)
    #The saved xml will be seperate than the original xml file and only overwrite the autosave.xml
    def OnAutoSave(self, event):

        self.AutoSave(str(event.GetEventObject().GetValue()))
        event.Skip()

    def AutoSave(self, msg):
        self.manager.ExportAsXML(self.dir + "\\AutoSave.xml", msg)


        defaultName = "AutoSave.xml"
        if self.manager is not None:
            date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
            date = date.strftime("%Y%m%d")
            defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV.xml"
        folder = "c:\\temp\\eHSN\\"
        name = folder + defaultName
        if not os.path.isdir(folder):
            os.makedirs(folder)
        self.manager.ExportAsXML(name, msg)
        # print "Save to AutoSave.xml"


    def OnAQUARIUSDataExtractionToolFrame(self, event):
        self.AutoSave(None)
        VersionCheck.Check(self.version, self, False)
        self.ratingCurveExtraction = AQUARIUSDataExtractionToolFrame(self.mode, self.ratingFileDir, self.scriptLoc, self, self, size=(555, 500))
        self.ratingCurveExtraction.Show()
        #self.LoadDefaultConfig()

        # app.MainLoop()


    def OnRatingCurveViewerToolFrame(self, event):
        self.AutoSave(None)
        if self.RatingCurveViewerToolFrame is None:
            self.RatingCurveViewerToolFrame = RatingCurveViewerToolFrame(self.mode, self.ratingFileDir, self.manager.genInfoManager.stnNumCmbo,\
                                            self.manager.disMeasManager, wx.LANGUAGE_ENGLISH, self, size=(770, 578))

            self.RatingCurveViewerToolFrame.Bind(wx.EVT_CLOSE, self.closeRatingCurveViewWindow)
            self.RatingCurveViewerToolFrame.exitButton.Bind(wx.EVT_BUTTON, self.closeRatingCurveViewWindow)
            self.RatingCurveViewerToolFrame.Show()
        else:
            self.RatingCurveViewerToolFrame.SetFocus()
    #Calling the calculator
    def OnCalc(self,e):
        if self.calc is None:
            self.calc = CalcPanel(self)
            thread.start_new_thread(self.calc.mainloop, ())
        elif self.calc.quitFlag:
            self.calc = CalcPanel(self)
            thread.start_new_thread(self.calc.mainloop, ())
        else:
            self.calc.exit()
            self.calc = CalcPanel(self)
            thread.start_new_thread(self.calc.mainloop, ())

    def closeConfigWindow(self, event):
        self.config.Destroy() #This will close the app window.
        self.config = None

    def closeRatingCurveViewWindow(self, event):

        if not self.RatingCurveViewerToolFrame.plotControl:
            info = wx.MessageDialog(None, self.closeRCVDesc, self.closeRCVTitle,
                                     wx.OK | wx.ICON_INFORMATION)
            info.ShowModal()
        else:
            self.RatingCurveViewerToolFrame.Destroy() #This will close the app window.
            self.RatingCurveViewerToolFrame = None


    #On new menu button pressed
    def OnNew(self, evt):
        # self.CreateFrames()
        # self.manager.SetupManagers()
        dlg = wx.MessageDialog(self, self.fileOpenMessage, 'New',
                              wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)

        res = dlg.ShowModal()
        if res == wx.ID_YES:
            dlg.Destroy()
            re = self.OnFileSaveAs(evt)
            if re:

                self.ResetGUI()
        elif res == wx.ID_NO:
            dlg.Destroy()

            self.ResetGUI()
        elif res == wx.ID_CANCEL:
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.Destroy()


    #Reset user interface from scratch
    def ResetGUI(self):
        self.DestroySubWindows()
        self.CreateFrames()
        self.manager.SetupManagers()
        self.SetTitle(self.noteHeaderTxt)
        self.name = ""
        self.fullname = ""
        self.LoadDefaultConfig()
        self.manager.BindAutoSave()
        self.manager.stageMeasManager.AddEntry()
        self.manager.waterLevelRunManager.AddRun()
        # 6 Entries
        for i in range(9):
            self.manager.movingBoatMeasurementsManager.AddEntry()


    def OnConfig(self, event):
        self.OpenConfig()

    def GetFlatNoteBook(self):
        return self.layout


    def OpenConfig(self):
        if self.config is None:
            self.config = ConfigPanel(self, 'Configure Stations, Meters and BM/Ref file locations')
            if self.savedStationsPath != '':
                self.config.stationsPathText.SetLabel(self.savedStationsPath)
            if self.savedMetersPath != '':
                self.config.metersPathText.SetLabel(self.savedMetersPath)
            if self.savedLevelsPath != '':
                self.config.levelsPathText.SetLabel(self.savedLevelsPath)
            self.config.stationsResetButton.Bind(wx.EVT_BUTTON, self.OnStationReset)
            self.config.stationsButton.Bind(wx.EVT_BUTTON, self.OnStationBrowse)
            self.config.levelsButton.Bind(wx.EVT_BUTTON, self.OnLevelBrowse)
            self.config.metersButton.Bind(wx.EVT_BUTTON, self.OnMeterBrowse)
            self.configpath = os.getcwd()
            self.config.Bind(wx.EVT_CLOSE, self.closeConfigWindow)
            self.config.closeButton.Bind(wx.EVT_BUTTON, self.closeConfigWindow)
            self.config.clearButton.Bind(wx.EVT_BUTTON, self.OnClearAll)
            if self.emptyStation:
                self.config.stationsPathText.SetForegroundColour("Red")
                self.config.stationsPathText.SetLabel('None')
            if self.emptyMeter:
                self.config.metersPathText.SetForegroundColour("Red")
                self.config.metersPathText.SetLabel('None')
            if self.emptyLevel:
                self.config.levelsPathText.SetForegroundColour("Red")
                self.config.levelsPathText.SetLabel('None')


            self.config.Layout()
        else:
            self.config.SetFocus()

    def configExit(self):
        self.config.destroy()
        self.config = None

    def OnSaveExit(self, event):

        if self.OnFileSave(event):
            self.Destroy()



    def OnFileSave(self, e):

        # if self.manager.disMeasManager.mandatoryChecking():
        #     return
        if self.name == "":
            if self.OnFileSaveAs(e):
                return True
            else:
                return False

        else:
            #mandatory field checking
            if self.manager.genInfoManager.mandatoryChecking():
                return
            if self.manager is not None:

                self.manager.ExportAsXML(self.fullname, None)
                print "File saved"
                return True
        return False



    # Export eHSN as XML file
    # Default name is STATIONNUM_YYYYMMDD_FV.xml
    def OnFileSaveAs(self, evt):
        #mandatory field checking
        if self.manager.genInfoManager.mandatoryChecking():
            return
        # if self.manager.disMeasManager.mandatoryChecking():
        #     return
        #defaultName = ''
        if self.manager is not None and self.name=="":
            date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
            date = date.strftime("%Y%m%d")
            self.name = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV"
        directory = os.getcwd()#self.saveDir
        # directory = self.saveDir + "\\" + str(self.manager.genInfoManager.stnNumCmbo)
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        fileSaveDialog = wx.FileDialog(self, self.fileSaveTitle, directory, str(self.name),
                            'Hydrometric Survey Notes (*.xml)|*.xml',
                                         style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
        # print self.fileSaveTitle, os.getcwd() + "\\" + str(self.manager.genInfoManager.stnNumCmbo)
        if fileSaveDialog.ShowModal() == wx.ID_CANCEL:
            fileSaveDialog.Destroy()


        if self.manager is not None:
            path = fileSaveDialog.GetPath()
            fileName = fileSaveDialog.GetFilename()
            if self.mode == "DEBUG":
                print "path exp"
                print path
            if path != "":
                self.manager.ExportAsXML(path, None)
                self.SetTitle(self.noteHeaderTxt + "   " + path)
                self.name = fileName
                self.fullname = path
                print "XML file saved"
                return True

        fileSaveDialog.Destroy()

        return False



    #Save as pdf and xml before uploading to AQ
    def SaveAsPDFAndXML4Upload(self, path, success):
        try:
	        if success:
	            self.createProgressDialog('In Progress', 'Uploading Successful. Saving Field Visit to pdf & xml.........')
	            name = self.SaveAsXMLAtUpload(path, success).split('.')[0]
	            self.deleteProgressDialog()
	            info = wx.MessageDialog(None, "Upload: Successful\nThe xml and pdf files has also been saved.\n" \
                    + name + ".xml\n" + name + ".pdf", "Done!",
	                                wx.OK)
	        else:
	            self.createProgressDialog('In Progress', 'Uploading failed. Saving Field Visit to pdf & xml.........')
	            name = self.SaveAsXMLAtUpload(path, success).split('.')[0]
	            self.deleteProgressDialog()
	            info = wx.MessageDialog(None, "Upload: Failed\nThe xml and pdf files has also been have saved.\n" \
                    + name + ".xml\n" + name + ".pdf", "Done!",
	                                wx.OK)


        except:

            self.deleteProgressDialog()
            info = wx.MessageDialog(None, "Failed to save files", "Error!",
                                wx.OK)
        info.ShowModal()

    #Save as XML before uploading to AQ
    def SaveAsXMLAtUpload(self, path, success):
        oldUploadRecord = None
        if self.name == '':
            defaultName = ''
            if self.manager is not None:
                date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
                date = date.strftime("%Y%m%d")
                defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV.xml"
##                if success:
##                    defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_eHSN_Upload.xml"
##                else:
##                    defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_eHSN_Failed.xml"
        else:
            defaultName = self.name.split(".")[0] + ".xml"
##
##            if success:
##                defaultName = self.name.split(".")[0] + "_Upload.xml"
##            else:
##                defaultName = self.name.split(".")[0] + "_Failed.xml"




        if path != "":
            newpath = path + '\\' + defaultName
            xml = self.manager.ExportAsXML(newpath, None)
            self.SaveAsPDFAtUpload(path, success, xml)
            self.SetTitle(self.noteHeaderTxt + "   " + newpath)
            self.name = defaultName
            self.fullname = newpath

        return defaultName


    #Save as PDF before uploading to AQ
    def SaveAsPDFAtUpload(self, path, success, xml):
        stylesheet_path = self.fullStyleSheetFileName

        # determine if application is a script file or frozen exe

        if hasattr(sys, '_MEIPASS'):
            stylesheet_path = os.path.join(sys._MEIPASS, stylesheet_path)

        # else:
            # stylesheet_path = self.stylesheetPath + os.sep + stylesheet_path


        # Locate stylesheet based on stylesheet_path
        found_stylesheet = os.path.exists(stylesheet_path)

        # If it exists, run fileSaveDialog
        # Else, run fileOpenDialog, then fileSaveDialog
        if not found_stylesheet:

            info = wx.MessageDialog(None, self.fileSavePDFStylesheetMessage, self.fileSavePDFStylesheetTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            info.ShowModal()

            fileOpenDialog = wx.FileDialog(self, self.fileSavePDFStylesheetTitle, os.getcwd(), '',
                                           'EHSN (*.xsml)|*.xsml',
                                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

            if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
                fileOpenDialog.Destroy()
                return

            if self.manager is not None:
                styleSheetPath = fileOpenDialog.GetPath()
                if self.mode == "DEBUG":
                    print "styleSheetPath exp"
                    print styleSheetPath
                if styleSheetPath != "":
                    stylesheet_path = styleSheetPath

            fileOpenDialog.Destroy()


        if self.mode == "DEBUG":
            print "path for export pdf before upload to AQ"
            print path

        if self.name == '':
            defaultName = ''
            if self.manager is not None:
                date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
                date = date.strftime("%Y%m%d")
                defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV.pdf"
##                if success:
##                    defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_eHSN_Uploaded.pdf"
##                else:
##                    defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_eHSN_Uploaded_Failed.pdf"
        else:
            defaultName = self.name.split(".")[0] + ".pdf"
##            if success:
##                defaultName = self.name.split(".")[0] + "_Uploaded.pdf"
##            else:
##                defaultName = self.name.split(".")[0] + "_Uploaded_Failed.pdf"

        if path != "":
            path = path + '\\' + defaultName
            if self.uploadOpenPdf:
                self.manager.ExportAsPDFFromXMLOpen(path, stylesheet_path, xml)
            else:
                self.manager.ExportAsPDFFromXML(path, stylesheet_path, xml)
        self.uploadOpenPdf = False





    def UploadingChecking(self):



    	# Check the starting time of the filed visit
        if not self.disMeas.IsEmpty():
            if self.disMeas.startTimeCtrl.GetValue() == "00:00" or self.disMeas.endTimeCtrl.GetValue() == "00:00":
                # print self.disMeas.startTimeCtrl.GetValue()
                warning = wx.MessageDialog(None,self.startTimeErrorMsg,
                                            "Upload Warning!", wx.OK | wx.ICON_EXCLAMATION)
                cont = warning.ShowModal()
                if cont == wx.ID_OK:
                    return

            elif self.disMeas.GetMmtValTxt() == "" or self.disMeas.GetMmtValTxt() == "00:00":
                # print self.disMeas.startTimeCtrl.GetValue()
                warning = wx.MessageDialog(None,"Mmt Mean Time Error",
                                            "Upload Warning!", wx.OK | wx.ICON_EXCLAMATION)
                cont = warning.ShowModal()
                if cont == wx.ID_OK:
                    return


        if self.manager.genInfoManager.stnNumCmbo == '':
                error = wx.MessageDialog(None, self.fileAQStnMessage, self.fileAQStnTitle,
                                         wx.OK | wx.ICON_EXCLAMATION)
                error.ShowModal()
                return


        if self.manager.genInfoManager.tzCmbo == '':
            error = wx.MessageDialog(None, self.fileAQTZMessage, self.fileAQTZTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            error.ShowModal()
            return
        #mandatory field checking
        if self.manager.genInfoManager.mandatoryChecking():
            return
        result = None
        try:
            self.manager.CheckFVVals()
        except ValueError, e:
            # result = ValueError
            result = str(e)


        if result is not None:
            error = wx.MessageDialog(None, result, self.errorTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            error.ShowModal()
            return



        # Field note must be reviewed before being able to upload
        if not self.partyInfo.ReviewedIsChecked():
            print "Reviewed is not checked"
            warning = wx.MessageDialog(None,
                                        self.notReviewedUploadWarning,
                                        "Upload Warning!", wx.OK | wx.ICON_EXCLAMATION)
            cont = warning.ShowModal()
            if cont == wx.ID_OK:
                return




        return 1


    # Save eHSN as PDF as designated by stylesheet
    # Prompts user to locate stylesheet if the default is not in same folder
    # default name is STATIONNUM_YYYYMMDD_eHSN.pdf
    def OnFileSaveAsPDF(self, evt):
        stylesheet_path = self.fullStyleSheetFileName

        # determine if application is a script file or frozen exe

        if hasattr(sys, '_MEIPASS'):
            stylesheet_path = os.path.join(sys._MEIPASS, stylesheet_path)

        # else:
            # stylesheet_path = self.stylesheetPath + os.sep + stylesheet_path


        # Locate stylesheet based on stylesheet_path
        found_stylesheet = os.path.exists(stylesheet_path)

        # If it exists, run fileSaveDialog
        # Else, run fileOpenDialog, then fileSaveDialog
        if not found_stylesheet:

            info = wx.MessageDialog(None, self.fileSavePDFStylesheetMessage, self.fileSavePDFStylesheetTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            info.ShowModal()

            fileOpenDialog = wx.FileDialog(self, self.fileSavePDFStylesheetTitle, os.getcwd(), '',
                                           'EHSN (*.xsml)|*.xsml',
                                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

            if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
                fileOpenDialog.Destroy()
                return

            if self.manager is not None:
                path = fileOpenDialog.GetPath()
                if self.mode == "DEBUG":
                    print "path exp"
                    print path
                if path != "":
                    stylesheet_path = path

            fileOpenDialog.Destroy()

        # Save
        if self.name == '':
            defaultName = ''
            if self.manager is not None:
                date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
                date = date.strftime("%Y%m%d")
                defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV"
        else:
            defaultName = self.name.split(".")[0]
        fileSaveDialog = wx.FileDialog(self, self.fileSavePDFSaveTitle, os.getcwd(), defaultName,
                                           'eHSN (*.pdf)|*.pdf',
                                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)


        if fileSaveDialog.ShowModal() == wx.ID_CANCEL:
            fileSaveDialog.Destroy()
            return

        if self.manager is not None:
            path = fileSaveDialog.GetPath()
            if self.mode == "DEBUG":
                print "path exp"
                print path
            if path != "":
                self.manager.ExportAsPDF(path, stylesheet_path)

        fileSaveDialog.Destroy()


    # Save eHSN as PDF as designated by stylesheet
    # Prompts user to locate stylesheet if the default is not in same folder
    # Stylesheet to be used to is be only the first page
    # default name is STATIONNUM_YYYYMMDD_eHSN_SUMMARY.pdf
    def OnFileSaveAsPDFSumm(self, evt):
        stylesheet_path = self.summStyleSheetFileName

        # determine if application is a script file or frozen exe

        if hasattr(sys, '_MEIPASS'):
            stylesheet_path = os.path.join(sys._MEIPASS, stylesheet_path)

        # else:
            # stylesheet_path = self.stylesheetPath + os.sep + stylesheet_path




        # Locate stylesheet based on stylesheet_path
        found_stylesheet = os.path.exists(stylesheet_path)

        # If it exists, run fileSaveDialog
        # Else, run fileOpenDialog, then fileSaveDialog
        if not found_stylesheet:
            info = wx.MessageDialog(None, self.fileSavePDFStylesheetSummMessage, self.fileSavePDFStylesheetTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            info.ShowModal()

            fileOpenDialog = wx.FileDialog(self, self.fileSavePDFStylesheetTitle, os.getcwd(), '',
                                           'EHSN (*.xsml)|*.xsml',
                                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

            if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
                fileOpenDialog.Destroy()
                return

            if self.manager is not None:
                path = fileOpenDialog.GetPath()
                if self.mode == "DEBUG":
                    print "path exp"
                    print path
                if path != "":
                    stylesheet_path = path

            fileOpenDialog.Destroy()

        # Save
        defaultName = ''
        if self.manager is not None:
            date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
            date = date.strftime("%Y%m%d")
            defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV_FRONTPAGE"

        fileSaveDialog = wx.FileDialog(self, self.fileSavePDFSaveTitle, os.getcwd(), defaultName,
                                       'eHSN (*.pdf)|*.pdf',
                                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)

        if fileSaveDialog.ShowModal() == wx.ID_CANCEL:
            fileSaveDialog.Destroy()
            return

        if self.manager is not None:
            path = fileSaveDialog.GetPath()
            if self.mode == "DEBUG":
                print "path exp"
                print path
            if path != "":
                self.CreateQR()
                self.manager.ExportAsPDF(path, stylesheet_path)

        fileSaveDialog.Destroy()




    def OnFileSaveAsPDFView(self, evt):
        stylesheet_path = self.viewStyleSheetFileName

        # determine if application is a script file or frozen exe

        if hasattr(sys, '_MEIPASS'):
            stylesheet_path = os.path.join(sys._MEIPASS, stylesheet_path)

        # else:
            # stylesheet_path = self.stylesheetPath + os.sep + stylesheet_path




        # Locate stylesheet based on stylesheet_path
        found_stylesheet = os.path.exists(stylesheet_path)

        # If it exists, run fileSaveDialog
        # Else, run fileOpenDialog, then fileSaveDialog
        if not found_stylesheet:

            info = wx.MessageDialog(None, self.fileSavePDFStylesheetViewMessage, self.fileSavePDFStylesheetTitle,
                                     wx.OK | wx.ICON_EXCLAMATION)
            info.ShowModal()

            fileOpenDialog = wx.FileDialog(self, self.fileSavePDFStylesheetTitle, os.getcwd(), '',
                                           'EHSN (*.xsml)|*.xsml',
                                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

            if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
                fileOpenDialog.Destroy()
                return

            if self.manager is not None:
                path = fileOpenDialog.GetPath()
                if self.mode == "DEBUG":
                    print "path exp"
                    print path
                if path != "":
                    stylesheet_path = path

            fileOpenDialog.Destroy()

        # Save
        defaultName = ''
        if self.manager is not None:
            date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
            date = date.strftime("%Y%m%d")
            defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV_VIEW"

        fileSaveDialog = wx.FileDialog(self, self.fileSavePDFSaveTitle, os.getcwd(), defaultName,
                                       'eHSN (*.pdf)|*.pdf',
                                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)

        if fileSaveDialog.ShowModal() == wx.ID_CANCEL:
            fileSaveDialog.Destroy()
            return

        if self.manager is not None:
            path = fileSaveDialog.GetPath()
            if self.mode == "DEBUG":
                print "path exp"
                print path
            if path != "":
                self.manager.ExportAsPDF(path, stylesheet_path)

        fileSaveDialog.Destroy()


    # This is executed when the user clicks the 'Open eHSN file (*.xml)' option
    # under the 'File' menu. For now, automatically exports as XML
    def OnFileOpen(self, evt):
        dlg = wx.MessageDialog(self, self.fileOpenMessage, self.fileOpenTitle,
                              wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)

        res = dlg.ShowModal()
        if res == wx.ID_YES:
            dlg.Destroy()
            re = self.OnFileSaveAs(evt)
            if re:
                self.FileOpen(evt)
        elif res == wx.ID_NO:
            dlg.Destroy()
            self.FileOpen(evt)
        elif res == wx.ID_CANCEL:
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.Destroy()




    def FileOpen(self, evt):
        self.DestroySubWindows()

        fileOpenDialog = wx.FileDialog(self, self.fileOpenTitle, os.getcwd(), '',
                            'Hydrometric Survey Notes (*.xml)|*.xml',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        if self.manager is not None:
            path = fileOpenDialog.GetPath()
            if self.mode == "DEBUG":
                print "path open"
                print path

            if path != "":


                self.path = path
                self.LoadDefaultConfig()
                self.manager.OpenFile(path)

                # After loading XML, If lock was checked, lock everything
                #if self.titleHeader.enteredInHWSCB.GetValue():
                #    self.manager.Lock()
                #else:
                self.manager.LockEvent(e=None)

                self.SetTitle(self.noteHeaderTxt + "   " + path)
                fileName = fileOpenDialog.GetFilename()

                self.name = fileName
                self.fullname = path

        fileOpenDialog.Destroy()
        self.manager.BindAutoSave()
        self.layout.Layout()



    # This is executed when the user clicks the 'Exit' option
    # under the 'File' menu.  We ask the user if they *really*
    # want to exit, then close everything down if they do.
    def OnFileExit(self, evt):
        dlg = wx.MessageDialog(self, self.fileExitMessage, self.fileExitTitle,
                              wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)

        res = dlg.ShowModal()
        if res == wx.ID_YES:
            dlg.Destroy()
            re = self.OnFileSaveAs(evt)
            if re is None:
                if self.calc is not None:
                    if not self.calc.quitFlag:
                        self.calc.quit()
                self.Destroy()
        elif res == wx.ID_CANCEL:
            dlg.Destroy()
        else:

            if self.calc is not None:
                if not self.calc.quitFlag:
                    self.calc.quit()

            dlg.Destroy()
            self.Destroy()







    # This is executed when the user clicks the 'Save Field Visit to Aquarius' option
    # under the 'File' menu.  We ask the user if they *really*
    # want to exit, then close everything down if they do.
    def OnAquariusUpload(self, evt):

        self.AutoSave(None)
        if VersionCheck.Check(self.version, self, False) > 2:
            return


        if self.UploadingChecking() == 1:

            # Save XML before uploading in case eHSN crashes.
            #if self.SaveBeforeUpload(evt):
            self.aquariusUploadDialog = AquariusUploadDialog(self.mode, self.uploadDir, self, title=self.fileAQUploadTitle, style=wx.RESIZE_BORDER)
            if self.manager.disMeasManager.IsEmpty() and self.manager.instrDepManager.dischargeRemarkEmpty():
                self.aquariusUploadDialog.dischargeCkbox.Enable(False)
            else:
                self.aquariusUploadDialog.dischargeCkbox.Enable(True)
                self.aquariusUploadDialog.dischargeCkbox.SetValue(False)
                self.aquariusUploadDialog.includeDischarge = False

            if not self.manager.waterLevelRunManager.IsEmpty():
                self.aquariusUploadDialog.levelNoteCkbox.SetValue(True)
                self.aquariusUploadDialog.includeLevelNote = True
            else:
                self.aquariusUploadDialog.levelNoteCkbox.Enable(False)
            self.aquariusUploadDialog.usernameCtrl.SetValue(self.savedName)
            self.aquariusUploadDialog.passwordCtrl.SetValue(self.savedPassword)
            # Set name of changeCtrl in upload dialog.
            if self.name=='':
                date = datetime.datetime.strptime(str(self.manager.genInfoManager.datePicker), self.manager.DT_FORMAT)
                date = date.strftime("%Y%m%d")
                defaultName = str(self.manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV.pdf"
                self.aquariusUploadDialog.changeCtrl.SetValue(self.dir +"\\" + defaultName)
            else:
                self.aquariusUploadDialog.changeCtrl.SetValue(self.dir + "\\" + self.name.replace("xml", "pdf"))
            # self.aquariusUploadDialog.usernameCtrl.SetValue("wenbin.zhang")
            # self.aquariusUploadDialog.passwordCtrl.SetValue("wenbin1")
            show_dialog = True
            show_error = False
            result = "Error occured during upload to AQUARIUS "

            while show_dialog:
                re = self.aquariusUploadDialog.ShowModal()

                if re == wx.ID_CANCEL:
                    break

                self.aquariusUploadDialog.EnableButtons(False)

                if self.manager is not None:
                    server = self.aquariusUploadDialog.GetServer()
                    username = self.aquariusUploadDialog.usernameCtrl.GetValue()
                    password = self.aquariusUploadDialog.passwordCtrl.GetValue()
                    fvDate = self.manager.genInfoManager.datePicker
                    withDischarge = self.aquariusUploadDialog.includeDischarge
                    withLevelNote = self.aquariusUploadDialog.includeLevelNote
################################################################################

                    # Let manager take care of all AquariusManager calls
                    # try:
    	               #  result = self.manager.ExportToAquarius(server, username, password, fvDate, withDischarge)

    	               #  if result is not None:
    		              #   if "password" in result:
    		            		# error = wx.MessageDialog(None, result, self.errorTitle,
    		              #                           wx.OK | wx.ICON_EXCLAMATION)
    		            		# re = error.ShowModal()
    		            		# if re == wx.ID_OK:

    		            		# 	aquariusUploadDialog.Destroy()
    		            		# 	return

                    # except:
                    #     print "Error during the uploading"
############################################################################

                    result = self.manager.ExportToAquarius(server, username, password, fvDate, withDischarge, withLevelNote)

                    if result is not None:
                        if "password" in result:
                            error = wx.MessageDialog(None, result, self.errorTitle,
                                                wx.OK | wx.ICON_EXCLAMATION)
                            re = error.ShowModal()
                            if re == wx.ID_OK:

                                self.aquariusUploadDialog.Destroy()
                                return

#######################################################

                    uploadInfo = []

                    if result is None:
                        self.manager.ExportToAquariusSuccess()

                        self.aquariusUploadDialog.EnableButtons(True)


                        # message = "Successful"
                        # success = wx.MessageDialog(None, self.fileAQUpSuccessMessage, self.fileAQUpSuccessTitle, wx.OK)
                        # success.ShowModal()

                        self.savedName = username
                        self.savedPassword = password

                        uploadInfo.append("Successful")
                        uploadInfo.append(str(datetime.datetime.now()))
                        uploadInfo.append(username)


                        if self.manager.uploadRecord is None:
                            self.manager.uploadRecord = Element('AQ_Upload_Record')
                        self.manager.UploadInfoAsXMLTree(self.manager.uploadRecord, uploadInfo)

                        self.SaveAsPDFAndXML4Upload(self.uploadDir, True)

                        break
                    else:
                        print "Error: %s" % result
                        show_error = True
                        uploadInfo.append("Failed")
                        uploadInfo.append(str(datetime.datetime.now()))
                        uploadInfo.append(username)
                        # message = "Failed"
                        if self.manager.uploadRecord is None:
                            self.manager.uploadRecord = Element('AQ_Upload_Record')
                        self.manager.UploadInfoAsXMLTree(self.manager.uploadRecord, uploadInfo)

                        self.SaveAsPDFAndXML4Upload(self.uploadDir, False)
                        break
                #Re enable access to dialog
                self.aquariusUploadDialog.EnableButtons(True)





                if show_error:
                    error = wx.MessageDialog(None, result, self.errorTitle,
                                                wx.OK | wx.ICON_EXCLAMATION)
                    error.ShowModal()
                    show_error = False
                    # aquariusUploadDialog.Destroy()

            self.aquariusUploadDialog.Destroy()

    def createProgressDialog(self, title, message):
        self.dialog = wx.ProgressDialog(title, message, 1, parent=self.aquariusUploadDialog, style=wx.PD_AUTO_HIDE|wx.PD_APP_MODAL)
        self.dialog.Pulse()

    def updateProgressDialog(self, message):
        self.dialog.Pulse(message)

    def deleteProgressDialog(self):
        self.dialog.Update(1)
        self.dialog.Destroy()


    # This is executed when the user clicks the 'About' option
    # under the 'Help' menu. Show information about the software.
    def OnHelpAbout(self, evt):
        if hasattr(sys, '_MEIPASS'):
            location = os.path.join(sys._MEIPASS)
        else:
            location = os.getcwd()
        icon = wx.Icon(location + '/icon.ico', wx.BITMAP_TYPE_ICO)
        description = self.helpAboutBaseDesc
        if self.manager is not None:
            description += self.version
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName(self.helpAboutTitle)
        aboutInfo.SetVersion(self.version)
        aboutInfo.SetDescription(description)
        aboutInfo.SetCopyright("This code was developed specifically for the Water Survey of Canada. \nFor support please submit an issue to: ")
        aboutInfo.SetWebSite("https://watersurveyofcanada.atlassian.net/")
        aboutInfo.AddDeveloper("Wenbin Zhang")
        aboutInfo.AddDeveloper("Yugo Brunet")
        aboutInfo.AddDeveloper("Vincent Vallee")
        aboutInfo.AddDeveloper("Taewan Kang")
        aboutInfo.SetArtists(["Project Management, testing and thanks to:\nMuluken Yeheyis", "Doug Stiff, Elizabeth Jamieson, Tim Andrews, Tim Antonio, Zachary Bishop, Andrew Creighton, Adam Dowler, Debbie Forlanski, Malyssa Maurer, Colin McCann, Mark Scott"])
        aboutInfo.SetLicence("This software has no license restrictions and is used at your own risk.")
        aboutInfo.SetIcon(icon)

        wx.adv.AboutBox(aboutInfo)
        # description = self.helpAboutBaseDesc
        # if self.manager is not None:
        #      description += self.version

        # info = adv.AboutDialogInfo()

        # info.SetName(self.helpAboutTitle)
        # info.SetDescription(description)

        # adv.AboutBox(info)


    # This is executed when the user clicks the 'About' option
    # under the 'Help' menu. Show information about the software.
    def OnHelpEHelp(self, evt):

        info = wx.MessageDialog(None, self.helpHelpMessage, self.helpHelpTitle,
                                     wx.OK | wx.ICON_INFORMATION)
        info.ShowModal()

        # panel = wx.Panel(info)
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # zoombar = zb.ZoomBar(panel, size=(300, 60))
        # sizer.Add(zoombar)
        # panel.SetSizer(sizer)


    def OnImportMovingBoaiMmt(self, event):
        movingBoatOpenDialog = wx.FileDialog(self, self.movingBoatOpenTitle, os.getcwd(), '',
                            'Moving Boat (*.mmt)|*.mmt',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if movingBoatOpenDialog.ShowModal() == wx.ID_CANCEL:
            movingBoatOpenDialog.Destroy()
            return

        if self.manager is not None:
            path = movingBoatOpenDialog.GetPath()
            if self.mode == "DEBUG":
                print "path open"
                print path

            if path != "":

                self.manager.OpenMovingBoatMmt(path)

        movingBoatOpenDialog.Destroy()



    # def OnOpenPress(self, evt):


    #     fileOpenDialog = wx.FileDialog(self.userConfig, 'Open Config', os.getcwd(), '',
    #                         'eHSN Station Config (*.txt)|*.txt',
    #                                    style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

    #     if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
    #         fileOpenDialog.Destroy()
    #         return

    #     if self.manager is not None:
    #         path = fileOpenDialog.GetPath()

    #         if self.mode == "DEBUG":
    #             print "path open"
    #             print path

    #         if path != "":

    #             fileName = fileOpenDialog.GetFilename()
    #             self.userConfig.stationTitleText.SetLabel(self.userConfig.stationTitLbl + '\n' + path)
    #             self.OpenFile(fileName)

    #     fileOpenDialog.Destroy()

    #     self.userConfig.layoutSizerV.Layout()
    #     self.userConfig.Update()
    #     self.userConfig.Refresh()
    #     return None






    # def OpenFile(self, file):
    #     with open(file) as stations:
    #         lines = stations.readlines()

    #     for item in lines:
    #         items = item.split('\t')
    #         self.numsRead.append(items[0])
    #         self.namesRead.append(items[1].rstrip())
    #     self.userConfig.stationsClear()
    #     for i in range(len(lines)):
    #         self.userConfig.AddEntry(self.numsRead[i], self.namesRead[i])
    #     self.genInfo.updateNumbers(self.numsRead)
    #     self.genInfo.stnNumCmbo.Bind(wx.EVT_TEXT, self.OnStationSelect)

    def OnLevelNoteEstablishedBtn(self, event):

        objBtn = event.GetEventObject()
        wlManager = self.manager.waterLevelRunManager

        for runIndex in range(len(wlManager.runSizer.GetChildren())):
            for row in range(len(wlManager.GetLevelNotesSizerV(runIndex).GetChildren()) - 1):

                button = wlManager.GetEstablishedElevationBtn(runIndex, row)

                if button == objBtn:
                    for index in range(len(self.bm)):

                        if wlManager.GetLevelNotesStation(runIndex, row).GetValue() == self.bm[index] and self.stationLevel[index] == self.genInfo.stnNumCmbo.GetValue():
                            # wlManager.CreateToasterBox(self, self.desc[index], len(self.desc[index])/30*1000, "#DFD996", (200,200))
                            dlg = wx.MessageDialog(self, self.desc[index], 'BM Reference', wx.OK)

                            res = dlg.ShowModal()
                            if res == wx.ID_OK:
                                dlg.Destroy()
                            else:
                                dlg.Destroy()
                            event.Skip()
                            return
        event.Skip()





    def OnLevelNoteStationSelect(self, event):

        observedCmbo = event.GetEventObject()
        wlManager = self.manager.waterLevelRunManager

        if len(self.bm) > 0 and  len(self.ele) == len(self.bm) and len(self.desc) == len(self.bm):
            for runIndex in range(len(wlManager.runSizer.GetChildren())):

                for row in range(len(wlManager.GetLevelNotesSizerV(runIndex).GetChildren()) - 1):

                    rowSizer = wlManager.GetLevelNotesRowSizer(runIndex, row)
                    stationsCmbo = wlManager.GetLevelNotesStation(runIndex, row)
                    if stationsCmbo == observedCmbo:
                        if observedCmbo.GetValue() in self.bm:
                            for index in range(len(self.bm)):

                                if observedCmbo.GetValue() == self.bm[index] and self.stationLevel[index] == self.genInfo.stnNumCmbo.GetValue():

                                    if self.ele[index] != '':

                                        wlManager.GetLevelNotesEstablishedElevation(runIndex, row).SetValue(self.ele[index])
                                        if row == 0:
                                            wlManager.GetLevelNotesElevation(runIndex, row).SetValue(self.ele[index])
                                    else:
                                        wlManager.GetLevelNotesEstablishedElevation(runIndex, row).SetValue('')
                                    break
                        else:
                            wlManager.GetLevelNotesEstablishedElevation(runIndex, row).SetValue('')
                            if row == 0:
                                wlManager.GetLevelNotesElevation(runIndex, row).SetValue('')

        event.Skip()

    def OnClearAll(self, event):
        del self.numsRead[:]
        del self.bm[:]
        del self.serialNumbers[:]
        del self.instrumentTypes[:]
        del self.manufactruers[:]
        del self.models[:]
        del self.frequencies[:]
        del self.bmIndex[:]
        self.genInfo.updateNumbers(self.numsRead)
        self.stageMeas.updateBMs(self.bm, self.bmIndex)
        self.waterLevelRun.levelNotes.updateBMs(self.bm, self.bmIndex)
        self.waterLevelRun.updateBMs(self.bm, self.bmIndex)
        self.instrDep.update(self.serialNumbers, self.instrumentTypes, self.manufactruers, self.models, self.frequencies)
        self.config.stationsPathText.SetForegroundColour("Red")
        self.config.metersPathText.SetForegroundColour("Red")
        self.config.levelsPathText.SetForegroundColour("Red")
        self.config.stationsPathText.SetLabel('None')
        self.config.metersPathText.SetLabel('None')
        self.config.levelsPathText.SetLabel('None')
        self.emptyStation = True
        self.emptyLevel = True
        self.emptyMeter = True




    def OnStationSelect(self, event):

        insertPoint = self.genInfo.stnNumCmbo.GetInsertionPoint()
        self.genInfo.stnNumCmbo.ChangeValue(unicode.upper(self.genInfo.stnNumCmbo.GetValue()))
        self.genInfo.stnNumCmbo.SetInsertionPoint(insertPoint)

        if len(self.numsRead) > 0 and len(self.namesRead) > 0:
            if self.genInfo.stnNumCmbo.GetValue() in self.numsRead:
                self.genInfo.stnNameCtrl.SetValue(self.namesRead[self.numsRead.index(self.genInfo.stnNumCmbo.GetValue())])
                self.genInfo.tzCmbo.SetValue(self.tz[self.numsRead.index(self.genInfo.stnNumCmbo.GetValue())])
            #else:
            #    self.genInfo.stnNameCtrl.ChangeValue("")
            #    self.genInfo.tzCmbo.SetValue("")
        if len(self.stationLevel) > 0:
            self.bmIndex = []
            for i in range(len(self.stationLevel)):
                if self.genInfo.stnNumCmbo.GetValue() == self.stationLevel[i]:
                    self.bmIndex.append(i)
            self.stageMeas.updateBMs(self.bm, self.bmIndex)
            self.waterLevelRun.levelNotes.updateBMs(self.bm, self.bmIndex)
            self.waterLevelRun.updateBMs(self.bm, self.bmIndex)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)




    def OnStationNameSelect(self, event):

        insertPoint = self.genInfo.stnNameCtrl.GetInsertionPoint()
        self.genInfo.stnNameCtrl.ChangeValue(unicode.upper(self.genInfo.stnNameCtrl.GetValue()))
        self.genInfo.stnNameCtrl.SetInsertionPoint(insertPoint)

        if len(self.numsRead) > 0 and len(self.namesRead) > 0:
            if self.genInfo.stnNameCtrl.GetValue() in self.namesRead:
                self.genInfo.stnNumCmbo.ChangeValue(self.numsRead[self.namesRead.index(self.genInfo.stnNameCtrl.GetValue())])
                self.genInfo.tzCmbo.SetValue(self.tz[self.namesRead.index(self.genInfo.stnNameCtrl.GetValue())])
            #else:
            #    self.genInfo.stnNumCmbo.ChangeValue("")
            #    self.genInfo.tzCmbo.SetValue("")
        if len(self.stationLevel) > 0:
            self.bmIndex = []
            for i in range(len(self.stationLevel)):
                if self.genInfo.stnNumCmbo.GetValue() == self.stationLevel[i]:
                    self.bmIndex.append(i)
            self.stageMeas.updateBMs(self.bm, self.bmIndex)
            self.waterLevelRun.levelNotes.updateBMs(self.bm, self.bmIndex)
            self.waterLevelRun.updateBMs(self.bm, self.bmIndex)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)





    def OnStationReset(self, event):
    	file = self.config.stationsDefaultPath
    	file = self.path + '\\' + file
    	self.config.stationsPathText.SetLabel(file)
    	self.config.stationsPathSizerV.Layout()
    	self.OpenStationFile(file)

    def OnStationBrowse(self, event):
        fileOpenDialog = wx.FileDialog(self.config, 'Open Config', os.getcwd(), '',
                            'eHSN Station Config (*.txt)|*.txt|eHSN Station Config (*.csv)|*.csv',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        if self.manager is not None:
            path = fileOpenDialog.GetPath()

            if self.mode == "DEBUG":
                print "path open"
                print path

            if path != "":

                fileName = fileOpenDialog.GetFilename()
                self.config.stationsPathText.SetLabel(path)
                self.config.stationsPathText.SetForegroundColour("#5E9811")
                self.OpenStationFile(fileName)
                self.savedStationsPath = path

        fileOpenDialog.Destroy()

        self.config.stationsPathSizerV.Layout()
        self.config.Update()
        self.config.Refresh()
        self.config.SetFocus()
        # print self.savedStationsPath
        return None

    def LoadDefaultConfig(self):
        try:
            self.OpenStationFile(self.ratingFileDir + '\\stations.txt')
            self.savedStationsPath = self.ratingFileDir + '\\stations.txt'
        except:
            pass
        try:
            self.OpenLevelFile(self.ratingFileDir + '\\levels.txt')
            self.savedLevelsPath = self.ratingFileDir + '\\levels.txt'
        except:
            pass
        try:
            print self.ratingFileDir
            self.OpenMeterFile(self.ratingFileDir + '\\meters.csv')
            self.savedMetersPath = self.ratingFileDir + '\\meters.csv'

        except:
            pass



    def OpenStationFile(self, file):

        self.numsRead = []
        self.namesRead = []
        self.tz = []

        if os.path.isfile(file):

            with open(file) as stations:
                lines = stations.readlines()
                # lines = [unicode(x) for y in lines for x in y]

            for item in lines:
                items = item.split(',')
                self.numsRead.append(items[0])
                self.namesRead.append(items[1].rstrip())
                self.tz.append(items[2].rstrip())

            self.numsRead = self.numsRead[1:]
            self.namesRead = self.namesRead[1:]
            self.tz = self.tz[1:]

            newNums = sorted(self.numsRead)

            newNames = []
            newTz = []
            for i in newNums:

                newNames.append(self.namesRead[self.numsRead.index(i)])
                newTz.append(self.tz[self.numsRead.index(i)])
            self.numsRead = newNums
            self.namesRead = newNames
            self.tz = newTz


            self.genInfo.updateNumbers(self.numsRead)
            self.genInfo.UpdateNames(sorted(self.namesRead))
            self.genInfo.stnNumCmbo.Bind(wx.EVT_TEXT, self.OnStationSelect)
            self.genInfo.stnNameCtrl.Bind(wx.EVT_TEXT, self.OnStationNameSelect)
            self.emptyStation = False




    def OpenLevelFile(self, file):

        self.stationLevel = []
        self.bm = []
        self.ele = []
        self.desc = []
        if os.path.isfile(file):

            with open(file, 'rU') as csvfile:
                for line in csv.reader(csvfile, delimiter=','):
                    if len(line) > 3:
                        self.stationLevel.append(line[0].rstrip())
                        # self.bm.append(line[1].rstrip())
                        self.bm.append(line[1])
                        self.ele.append(line[2].rstrip())
                        self.desc.append(line[3].rstrip())

            self.stationLevel = self.stationLevel[1:]
            self.bm = self.bm[1:]
            self.ele = self.ele[1:]
            self.desc = self.desc[1:]

            self.stageMeas.updateBMs(self.bm, self.bmIndex)
            self.waterLevelRun.levelNotes.updateBMs(self.bm, self.bmIndex)
            self.waterLevelRun.updateBMs(self.bm, self.bmIndex)
            wlrManager = self.manager.waterLevelRunManager
            for i in range(len(wlrManager.runSizer.GetChildren())):
                for rowIndex in range(len(wlrManager.GetLevelNotesSizerV(i).GetChildren()) - 1):
                    wlrManager.GetLevelNotesStation(i, rowIndex).Bind(wx.EVT_TEXT, self.OnLevelNoteStationSelect)
                    # wlrManager.GetEstablishedElevationBtn(i, rowIndex).Bind(wx.EVT_BUTTON, self.OnLevelNoteEstablishedBtn)


            self.emptyLevel = False



    def OnLevelBrowse(self, event):
        fileOpenDialog = wx.FileDialog(self.config, 'Open Config', os.getcwd(), '',
                            'eHSN Level Config (*.txt)|*.txt|eHSN Level Config (*.csv)|*.csv',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        if self.manager is not None:
            path = fileOpenDialog.GetPath()

            if self.mode == "DEBUG":
                print "path open"
                print path

            if path != "":

                fileName = fileOpenDialog.GetFilename()
                self.config.levelsPathText.SetLabel(path)
                self.config.levelsPathText.SetForegroundColour("#5E9811")
                self.OpenLevelFile(fileName)
                self.OnStationSelect(event)
                self.savedLevelsPath = path

        fileOpenDialog.Destroy()

        self.config.levelsPathSizerV.Layout()
        self.config.Update()
        self.config.Refresh()
        self.config.SetFocus()
        return None




    def OnMeterBrowse(self, event):
        fileOpenDialog = wx.FileDialog(self.config, 'Open Config', os.getcwd(), '',
                            'eHSN Meter Config (*.csv)|*.csv|eHSN Meter Config (*.txt)|*.txt',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        if self.manager is not None:
            path = fileOpenDialog.GetPath()

            if self.mode == "DEBUG":
                print "path open"
                print path

            if path != "":

                fileName = fileOpenDialog.GetFilename()
                self.config.metersPathText.SetLabel(path)
                self.config.metersPathText.SetForegroundColour("#5E9811")
                self.OpenMeterFile(fileName)
                self.savedMetersPath = path

        fileOpenDialog.Destroy()

        self.config.metersPathSizerV.Layout()
        self.config.Update()
        self.config.Refresh()
        self.config.SetFocus()

        return None

    def OpenMeterFile(self, file):
        self.serialNumbers = []
        self.instrumentTypes = []
        self.manufactruers = []
        self.models = []
        self.frequencies = []
        self.firmware = []

        # for mid-section tab
        self.midsecMeasurements.header.meterNoList = [""]
        self.midsecMeasurements.header.slope1List = [""]
        self.midsecMeasurements.header.intercept1List = [""]
        self.midsecMeasurements.header.slope2List = [""]
        self.midsecMeasurements.header.intercept2List = [""]
        self.midsecMeasurements.header.calibDateList = [""]

        if os.path.isfile(file):
            with open(file) as levels:
                lines = levels.readlines()

            for item in lines:
                items = item.split(',')
                self.serialNumbers.append(items[0].rstrip())
                self.instrumentTypes.append(items[1].rstrip())
                self.manufactruers.append(items[2].rstrip())
                self.models.append(items[3].rstrip())
                self.frequencies.append(items[4].rstrip())
                # self.firmware.append(items[5].rstrip())

                # for mid-section tab
                if (("1" == items[0].strip()[0] or "6" == items[0].strip()[0]) and "-" == items[0].strip()[1]) or ("current meter" in items[1].lower().strip()):
                    self.midsecMeasurements.header.meterNoList.append(items[0].strip())
                    self.midsecMeasurements.header.slope1List.append(items[5].strip())
                    self.midsecMeasurements.header.intercept1List.append(items[6].strip())
                    self.midsecMeasurements.header.slope2List.append(items[7].strip())
                    self.midsecMeasurements.header.intercept2List.append(items[8].strip())
                    self.midsecMeasurements.header.calibDateList.append(items[9].strip())

            #remove title
            self.serialNumbers = self.serialNumbers[1:]
            self.instrumentTypes = self.instrumentTypes[1:]
            self.manufactruers = self.manufactruers[1:]
            self.models = self.models[1:]
            self.frequencies = self.frequencies[1:]
            # self.firmware = self.firmware[1:]

            #self.midsecMeasurements.header.meterNoList = self.midsecMeasurements.header.meterNoList[1:]
            #self.midsecMeasurements.header.slope1List = self.midsecMeasurements.header.slope1List[1:]
            #self.midsecMeasurements.header.intercept1List = self.midsecMeasurements.header.intercept1List[1:]
            #self.midsecMeasurements.header.slope2List = self.midsecMeasurements.header.slope2List[1:]
            #self.midsecMeasurements.header.intercept2List = self.midsecMeasurements.header.intercept2List[1:]
            #self.midsecMeasurements.header.calibDateList = self.midsecMeasurements.header.calibDateList[1:]

            self.instrDep.update(self.serialNumbers, self.instrumentTypes,  self.manufactruers, self.models, self.frequencies)
            self.instrDep.serialCmbo.Bind(wx.EVT_TEXT, self.OnSerialNumberSelect)

            self.midsecMeasurements.header.UpdateMeterNo()

            self.emptyMeter = False



    def OnSerialNumberSelect(self, evt):
        if len(self.serialNumbers) > 0 and len(self.instrumentTypes) == len(self.serialNumbers) == len(self.manufactruers) == len(self.models) == len(self.frequencies):
            if self.instrDep.serialCmbo.GetValue() in self.serialNumbers:
                self.instrDep.instrumentCmbo.SetValue(self.instrumentTypes[self.serialNumbers.index(self.instrDep.serialCmbo.GetValue())])
                self.instrDep.manufactureCmbo.SetValue(self.manufactruers[self.serialNumbers.index(self.instrDep.serialCmbo.GetValue())])
                self.instrDep.modelCmbo.SetValue(self.models[self.serialNumbers.index(self.instrDep.serialCmbo.GetValue())])
                self.instrDep.frequencyCmbo.SetValue(self.frequencies[self.serialNumbers.index(self.instrDep.serialCmbo.GetValue())])
                # self.instrDep.firmwareCmbo.SetValue(self.firmware[self.serialNumbers.index(self.instrDep.serialCmbo.GetValue())])




    def SaveBeforeUpload(self, evt):
        dlg = wx.MessageDialog(self, self.saveBeforeUploadDesc, self.saveBeforeUploadTitle,
                              wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
        dlg.SetYesNoCancelLabels('Save', self.noSaveBeforeUploadMsg, 'Cancel')
        res = dlg.ShowModal()
        if res == wx.ID_YES:
            dlg.Destroy()
            self.OnFileSave(evt)
            return True

        elif res == wx.ID_NO:
            dlg.Destroy()
            return True

        else:
            dlg.Destroy()
            return False

    #Start time for each transction from dis file
    def startTime(self, time):
        start = time[:-3]
        if time[-2:] == 'AM':
            return start
        else:
            times = time[:-3].split(':')
            head = (int(times[0]) + 12) % 24
            return str(head) + ':' + times[1] + ':' + times[2]

    #End time for each transction from dis file
    def endTime(self, time, duration):
        time = time.split(':')
        hh = int(time[0])
        mm = int(time[1])
        ss = int(time[2])
        duration = duration.split(':')
        durationhh = int(duration[0])
        durationmm = int(duration[1])
        durationss = int(duration[2])

        second = (ss + durationss) % 60
        minute = (mm + durationmm + (ss + durationss) / 60) % 60
        hour = (hh + durationhh + (mm + durationmm + (ss + durationss) / 60) / 60) % 60

        second = '0' + str(second) if second < 10 else str(second)
        minute = '0' + str(minute) if minute < 10 else str(minute)
        hour = '0' + str(hour) if hour < 10 else str(hour)

        return hour + ":" + minute + ":" + second


    #Calculate the mean time
    def mean(self, start, end):
        startHour = start.GetHour()
        endHour = end.GetHour()
        startMin = start.GetMinute()
        endMin = end.GetMinute()
        startSec = start.GetSecond()
        endSec = end.GetSecond()
        if (startHour + endHour)%2 != 0:
            endMin += 60
        if (startMin + endMin)%2 != 0:
            endSec += 60
        meanHour = (startHour + endHour) / 2
        meanMin = (startMin + endMin) / 2
        meanSec = (startSec + endSec) / 2
        meanTime = str(meanHour) + ':' + str(meanMin) + ':' + str(meanSec)

        return meanTime



    # def OnMovingBoaiDis(self, event):
    #     movingBoatOpenDialog = wx.FileDialog(self, self.movingBoatOpenTitle, os.getcwd(), '',
    #                         'Moving Boat (*.dis)|*.dis',
    #                                    style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

    #     if movingBoatOpenDialog.ShowModal() == wx.ID_CANCEL:
    #         movingBoatOpenDialog.Destroy()
    #         return

    #     if self.manager is not None:
    #         path = movingBoatOpenDialog.GetPath()
    #         if self.mode == "DEBUG":
    #             print "path open"
    #             print path

    #         if path != "":

    #             self.OpenMovingBoaiDis(path, event)

    #     movingBoatOpenDialog.Destroy()



    def ConvertDateFromDis(self, date):
        dateDis = date.split(' ')
        day = dateDis[2].split(',')[0]
        year = dateDis[3].split('\n')[0].strip()
        if 'Jan' in dateDis[1]:
            return year + '/01/' + day
        elif 'Feb' in dateDis[1]:
            return year + '/02/' + day
        elif 'Mar' in dateDis[1]:
            return year + '/03/' + day
        elif 'May' in dateDis[1]:
            return year + '/04/' + day
        elif 'Apr' in dateDis[1]:
            return year + '/05/' + day
        elif 'Jun' in dateDis[1]:
            return year + '/06/' + day
        elif 'Jul' in dateDis[1]:
            return year + '/07/' + day
        elif 'Aug' in dateDis[1]:
            return year + '/08/' + day
        elif 'Sep' in dateDis[1]:
            return year + '/09/' + day
        elif 'Oct' in dateDis[1]:
            return year + '/10/' + day
        elif 'Nov' in dateDis[1]:
            return year + '/11/' + day
        elif 'Dec' in dateDis[1]:
            return year + '/12/' + day
        else:
            print 'error date format from dis'
            return ''




    def OnUpdate(self, evt):
        print "On Update"
        VersionCheck.Check(self.version, self, True)

    def DestroySubWindows(self):
        if self.RatingCurveViewerToolFrame != None:
            self.RatingCurveViewerToolFrame.Destroy()
            self.RatingCurveViewerToolFrame = None
        if self.calc != None:
            self.calc.quit()
            self.calc = None
        if self.config != None:
            self.config.Destroy()
            self.config = None

        if self.ratingCurveExtraction != None:
            self.ratingCurveExtraction.Destroy()
            self.ratingCurveExtraction = None
        if self.waterLevelRun.miniFrame != None:
            self.waterLevelRun.miniFrame.Destroy()
            self.waterLevelRun.miniFrame = None


    def CreateQR(self):
        manager = self.manager
        code = "MATMSG:TO:dougstiff@gmail.com;SUB: Field visit for: " + manager.genInfoManager.datePicker + ";BODY: <?xml version="'"1.0"'"?><?xml-stylesheet type="'"text/xsl"'" href="'"WSC_EHSN.xsml"'"?><EHSN version="'"v1.2.1.1"'"><TitleHeader><enteredInHWS>False</enteredInHWS></TitleHeader><GenInfo><station number="'"08OA003"'">PREMIER CREEK NEAR QUEEN CHARLOTTE</station><date>timezone="'"PST"'">2016/05/09</date></GenInfo><StageMeas><HgCkbox>True</HgCkbox><Hg2Ckbox>False</Hg2Ckbox><Wlr1Ckbox>False</Wlr1Ckbox><Wlr2Ckbox>False</Wlr2Ckbox><HG1Header/><HG2Header/><WL1Header/><WL2Header/><StageMeasTable><StageMeasRow row="'"0"'"><time>15:23</time><HG1>12.000</HG1><HG2/><WL1/><WL2/><SRC/><SRCApp/><MghCkbox>True</MghCkbox></StageMeasRow></StageMeasTable><hgCkbox>True</hgCkbox><hg2Ckbox>False</hg2Ckbox><wlr1Ckbox>False</wlr1Ckbox><wlr2Ckbox>False</wlr2Ckbox><MGHHG1>12.0</MGHHG1><MGHHG2/><MGHWL1/><MGHWL2/><SRCHG1>0.000</SRCHG1><SRCHG2/><GCHG1>0.000</GCHG1><GCHG2/><GCWL1/><GCWL2/><CMGHHG1>12.0</CMGHHG1><CMGHHG2/><CMGHWL1/><CMGHWL2/><MghMethod>Average</MghMethod><Factors/></StageMeas><DisMeas><startTime>15:44</startTime><endTime>04:00</endTime><airTemp/><waterTemp/><width/><area/><meanVel/><mgh/><mghCmbo/><discharge>12.0</discharge><mmtTimeVal>21:52</mmtTimeVal><shift>3</shift><diff>3</diff><curve>3</curve></DisMeas><PartyInfo><party/><completed/><checked/><reviewed>True</reviewed></PartyInfo></EHSN>;;"

        self.img = qrcode.make(code)
        self.img.save(self.qr_path, "jpeg")

    # def OpenMovingBoaiDis(self, path, evt):
    #     locked = self.movingBoatMeasurements.lockCB.GetValue()





    #     mmntStart = ''
    #     mmntEnd = ''
    #     stationNumber = ''
    #     dateDis = ''
    #     transducer = None
    #     depRef =None
    #     topMethod = None
    #     botMethod = None


    #     ## Open the file with read only permit
    #     f = open(path)
    #     ## Read the first line
    #     line = f.readline()
    #     Transections = []
    #     summary = []
    #     hasNextLine = False
    #     ## If the file is not empty keep reading line one at a time
    #     ## till the file is empty
    #     while line:
    #         if ';' in line:
    #             row = line.split(';')
    #             row[1] = row[1].strip()
    #             key = row[0]
    #             val = row[1]
    #             if key == 'Track Reference':
    #                 if 'Bottom-Track' in val:
    #                     trackRef = 'BT'
    #                 elif val == 'GPS-GGA':
    #                     trackRef = 'GGA'
    #                 elif val == 'GPS-VTG':
    #                     trackRef = 'VTG'
    #                 else:
    #                     trackRef = ''
    #             elif key == 'Left Method':

    #                 if val == 'Sloped Bank':
    #                     leftBank = 'Sloping'
    #                 elif val == 'Vertical Bank':
    #                     leftBank = 'Vertical'
    #                 elif val == 'User Input':
    #                     leftBank = 'Other'
    #                 else:
    #                     leftBank = ''
    #             elif key == 'Right Method':

    #                 if val == 'Sloped Bank':
    #                     rightBank = 'Sloping'
    #                 elif val == 'Vertical Bank':
    #                     rightBank = 'Vertical'
    #                 elif val == 'User Input':
    #                     rightBank = 'Other'
    #                 else:
    #                     rightBank = ''
    #             elif key == 'Station Number':
    #                 stationNumber = val
    #             elif 'Transducer' in key:
    #                 transducer = val
    #             elif 'Depth Reference' in key:
    #                 depRef = val
    #             elif 'Top Fit' in key:
    #                 topMethod = val
    #             elif 'Bottom Fit' in key:
    #                 botMethod = val
    #         comments = ''
    #         comments += 'Transducer Depth: ' + transducer + '\n' if transducer is not None else ''
    #         comments += 'Depth Reference: ' + depRef + '\n' if depRef is not None else ''
    #         comments += 'Top Discharge Est: ' + topMethod + '\n' if topMethod is not None else ''
    #         comments += 'Bottom Discharge Est: ' + botMethod + '\n' if botMethod is not None else ''
    #         comments += '\n'

    #         if ":" in line:
    #             dateline = line.split(':')
    #             if dateline[0] == 'Date Measured':
    #                 dateDis = self.ConvertDateFromDis(dateline[1])



    #         if "Transect\t" in line or hasNextLine:
    #             # print line
    #             line = line.split("\t")

    #             line.pop()

    #             Transections.append(line)
    #             hasNextLine = True

    #         line = f.readline()
    #         if "\t\t\t\t" in line:
    #             hasNextLine = False
    #             line = line.split("\t")
    #             line.pop()
    #             summary.append(line)

    #     f.close()

    #     if self.LocationCheckBeforeImporiDis(stationNumber, dateDis):





    #         if not locked:


    #             self.movingBoatMeasurements.manager.lockCB = ''
    #             self.movingBoatMeasurements.manager.mbCB = False
    #             self.movingBoatMeasurements.manager.mbCmbo = ''
    #             self.movingBoatMeasurements.manager.leftBankCmbo = ''
    #             # movingBoatMeasurements.leftBankOtherCtrl = ''
    #             self.movingBoatMeasurements.manager.rightBankCmbo = ''
    #             # movingBoatMeasurements.rightBankOtherCtrl = ''
    #             self.movingBoatMeasurements.manager.trackRefCmbo = ''
    #             self.movingBoatMeasurements.manager.mmntStartTimeCtrl = '00:00:00'
    #             self.movingBoatMeasurements.manager.mmntEndTimeCtrl = '00:00:00'
    #             self.movingBoatMeasurements.manager.mmntMeanTimeCtrl = '00:00:00'
    #             self.movingBoatMeasurements.manager.rawDischMeanCtrl = ''
    #             self.movingBoatMeasurements.manager.finalDischCtrl = ''
    #             self.movingBoatMeasurements.manager.mbCorrAppCtrl = ''
    #             self.movingBoatMeasurements.manager.standDevMeanDischCtrl = ''
    #             self.movingBoatMeasurements.manager.corrMeanGHCtrl = ''
    #             self.movingBoatMeasurements.manager.calcShiftBaseCurveCtrl = ''
    #             self.movingBoatMeasurements.manager.dischDiffBaseCurveCtrl = ''
    #             self.movingBoatMeasurements.manager.baseCurveGHCtrl = ''
    #             self.movingBoatMeasurements.manager.baseCurveDischCtrl = ''
    #             self.movingBoatMeasurements.manager.commentsCtrl = ''

    #             for row in range(len(self.movingBoatMeasurements.tableSizerV.GetChildren()) - 2):
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 1, 'False')
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 2, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 3, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 4, "00:00:00")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 5, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 6, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 7, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 8, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 9, "")
    #                 self.movingBoatMeasurements.manager.SetTableValue(row, 10, "")







    #         self.movingBoatMeasurements.trackRefCmbo.SetValue(trackRef)
    #         self.movingBoatMeasurements.leftBankCmbo.SetValue(leftBank)
    #         self.movingBoatMeasurements.rightBankCmbo.SetValue(rightBank)
    #         color = (210, 210, 210)
    #         for index in range(1, len(Transections)):
    #             start = self.startTime(Transections[index][4])
    #             end = self.endTime(start, Transections[index][5])
    #             transectID = Transections[index][0]
    #             startBank = 'L' if Transections[index][2] == 'Left Bank' else 'R'
    #             finalDischarge = Transections[index][18]

    #             mmntStart = start if mmntStart == '' else mmntStart
    #             mmntEnd = end

    #             if index > len(self.movingBoatMeasurements.tableSizerV.GetChildren()) - 2:
    #             		self.movingBoatMeasurements.AddEntry()
    #             if not locked:

    #                 self.movingBoatMeasurements.manager.SetTableValue(index-1, 1, 'True')
    #                 self.movingBoatMeasurements.manager.SetTableValue(index-1, 2, transectID)
    #                 self.movingBoatMeasurements.manager.SetTableValue(index-1, 3, startBank)
    #                 self.movingBoatMeasurements.manager.SetTableValue(index-1, 4, start)
    #                 self.movingBoatMeasurements.manager.SetTableValue(index-1, 8, finalDischarge)
    #                 self.movingBoatMeasurements.manager.commentsCtrl = comments

    #                 self.movingBoatMeasurements.manager.SetTableColor(index-1, 2, color)
    #                 self.movingBoatMeasurements.manager.SetTableColor(index-1, 8, color)
    #             else:

    #                 # self.movingBoatMeasurements.manager.SetTableValue(index-1, 0, 'True')
    #                 if self.movingBoatMeasurements.manager.GetTableValue(index-1, 2) == '':
    #                     self.movingBoatMeasurements.manager.SetTableValue(index-1, 2, transectID)
    #                     self.movingBoatMeasurements.manager.SetTableColor(index-1, 2, color)
    #                 if self.movingBoatMeasurements.manager.GetTableValue(index-1, 3) == '':
    #                     self.movingBoatMeasurements.manager.SetTableValue(index-1, 3, startBank)
    #                 if self.movingBoatMeasurements.manager.GetTableValue(index-1, 4) == '00:00:00':
    #                     self.movingBoatMeasurements.manager.SetTableValue(index-1, 4, start)
    #                 if self.movingBoatMeasurements.manager.GetTableValue(index-1, 8) == '':
    #                     self.movingBoatMeasurements.manager.SetTableValue(index-1, 8, finalDischarge)
    #                     self.movingBoatMeasurements.manager.SetTableColor(index-1, 8, color)
    #         meanFinal = 0
    #         counterFinal = 0
    #         finals = []
    #         for tran in range(len(self.movingBoatMeasurements.tableSizerV.GetChildren()) - 2):
    #             if self.movingBoatMeasurements.manager.GetTableValue(tran, 1):

    #                 meanFinal += float(self.movingBoatMeasurements.manager.GetTableValue(tran, 8))
    #                 counterFinal += 1
    #                 finals.append(self.movingBoatMeasurements.manager.GetTableValue(tran, 8))
    #         if counterFinal > 0:
    #             meanFinal = meanFinal / counterFinal
    #         if len(finals) > 0:
    #             standDevMean = float(format(self.standardDeviation(finals) /float(meanFinal), '.3f')) * 100
    #             self.movingBoatMeasurements.standDevMeanDischCtrl.SetValue(str(standDevMean))
    #         else:
    #             self.movingBoatMeasurements.standDevMeanDischCtrl.SetValue('0.000')

    #         self.movingBoatMeasurements.mmntStartTimeCtrl.SetValue(mmntStart)
    #         self.movingBoatMeasurements.mmntEndTimeCtrl.SetValue(mmntEnd)

    #         startFromTimeCtrl = self.movingBoatMeasurements.mmntStartTimeCtrl.GetWxDateTime()
    #         endFromTimeCtrl = self.movingBoatMeasurements.mmntEndTimeCtrl.GetWxDateTime()
    #         meanTime = self.mean(startFromTimeCtrl, endFromTimeCtrl)

    #         self.movingBoatMeasurements.mmntMeanTimeCtrl.SetValue(meanTime)
    #         if not locked :
    #             self.movingBoatMeasurements.finalDischCtrl.SetValue(summary[0][18])
    #             self.movingBoatMeasurements.standDevMeanDischCtrl.SetValue(str(float(summary[2][18]) * 100))
    #         else:
    #             self.movingBoatMeasurements.OnFinalDischargeMean(evt)
    #             self.movingBoatMeasurements.OnStandardDev(evt)
    #         self.movingBoatMeasurements.manager.recalculate()


    #return the standard deviation of a list of numbers
    def standardDeviation(self, nums):
        if len(nums) == 1:
            return 0
        if len(nums) > 0:
            mean = 0
            total = 0
            for i in range(len(nums)):
                mean += float(nums[i])
            mean = mean / len(nums)

            for i in range(len(nums)):
                total += (float(nums[i]) - mean) ** 2
            return math.sqrt(total / (len(nums) - 1))
        else:
            return 0


    # def OnDraw(self, event):
    #     # skatch.MainApp().run()
    #     self.p = painting.MyPaint()
    #     self.p.Run()



    # #Check if station ID matched before import a dis file
    # def LocationCheckBeforeImporiDis(self, locationID, date):
    #     desc = 'The date for this measurement file does not match the date on the front page.\nDo you still want to import the ADCP file?'
    #     openTitle = 'Date does not match'

    #     if locationID != '':

    #         locationIDFrontPage = self.manager.genInfoManager.stnNumCmbo
    #         dateFrontPage = self.manager.genInfoManager.datePicker

    #         if locationID.upper() != locationIDFrontPage:
    #             dlg = wx.MessageDialog(self, "The Station ID in the measurement file does not match", 'Dismatch Station ID',
    #                                         wx.OK | wx.ICON_QUESTION)
    #             res = dlg.ShowModal()
    #             if res == wx.OK:
    #                 dlg.Destroy()
    #                 return False
    #             else:
    #                 dlg.Destroy()
    #                 return False
    #         elif date != dateFrontPage:
    #             dlg = wx.MessageDialog(self, desc, openTitle, wx.YES_NO | wx.ICON_QUESTION)

    #             res = dlg.ShowModal()
    #             if res == wx.ID_YES:
    #                 dlg.Destroy()
    #                 return True
    #             elif res == wx.wx.ID_NO:
    #                 dlg.Destroy()
    #                 return False
    #             else:
    #                 dlg.Destroy()
    #                 return False
    #         else:
    #             return True

    #     else:
    #         dlg = wx.MessageDialog(self, "Station ID and date cannot be empty on the front page", 'Empty Station ID',
    #                                         wx.OK | wx.ICON_QUESTION)
    #         res = dlg.ShowModal()
    #         if res == wx.OK:
    #             dlg.Destroy()
    #             return False
    #         else:
    #             dlg.Destroy()
    #             return False




    # def OnAdcpMid(self, event):
    #     print self.instrDep.methodCBListBox.GetCheckedStrings()

    #     # self.instrDep.OnDeploymentCheckListCB(event)
    #     if self.instrDep.methodCBListBox.IsChecked(0):
    #         self.frChecklist.activeFieldReview(True)

    #     elif self.instrDep.methodCBListBox.IsChecked(1):

    #         if  self.instrDep.instrumentCmbo.GetValue().lower() == 'adcp' or self.instrDep.instrumentCmbo.GetValue().lower() == 'adv'\
    #         or self.instrDep.instrumentCmbo.GetValue().lower() == 'current meter':

    #             self.frChecklist.activeFieldReview(True)

    #         else:

    #             self.frChecklist.activeFieldReview(False)


    #     else:
    #         self.frChecklist.activeFieldReview(False)

    #     event.Skip()


def main():
    headerTitle = "Hydrometric Survey Notes"

    app = wx.App()
    EHSN = EHSNGui("DEBUG", "V1.0.6", None, title = headerTitle, size=(780, 650))
    app.MainLoop()


if __name__=='__main__':
    main()
