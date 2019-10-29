# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import re
from AQUARIUSDataExtractionToolManager import *
from wx import adv
import wx.lib.agw.foldpanelbar as fpb
import socket
# import DateTimeFromDMY


class AQUARIUSDataExtractionToolFrame(wx.Frame):
    def __init__(self, mode, path, scriptLoc, EHSNGui, *args, **kwargs):
        super(AQUARIUSDataExtractionToolFrame, self).__init__(*args, **kwargs)

        self.titleLbl = "AQUARIUS Data Extraction Tool"
        self.pathTitleLbl = "Tool for Extracting Station Data from AQUARIUS"
        self.loginTitleLbl = "AQUARIUS Login"
        self.importTitleLbl = "Data to extract"
        self.usernameLbl = "Username:"
        self.passwordLbl = "Password:"
        self.pathLbl = "File Export Location "
        self.browseLbl = "Browse"
        self.browseTitleLbl = "Choose destination for extracted files"
        self.stationLbl = "Station IDs"
        self.urlLbl = "Server:"
        self.stnCkboxLbl = "Station Metadata {Station ID, Name, Time Zone} (stations.txt)"
        self.lvlCkboxLbl = "Benchmark/Reference Information {Station ID, Reference, Elevation, Description} (levels.txt)"
        self.rcCkboxLbl = 'Rating Curves (StationID_ratingcurves.xml)'
        self.dataPeriodTxtLbl = "Historical Field Visits (StationID_FieldVisits.csv)"
        self.dataPeriodFromTxtLbl = "From"
        self.dataPeriodToTxtLbl = "To"
        self.exportSubtxtLbl = "Leaving the default directory is recommended as it will allow everything to load automatically"
        self.hint = "This is a tool for extracting data from Aquarius. This is probably the first tool you want to use when \n" + \
        "you start the eHSN for the first time. If you provide a list of stations this tool will extract metadata \n" + \
        "for your stations that will help you fill in the note and make decisions in the field this includes:\n" + \
        "\t1. Station Information including Name and Time Zone\n" + \
        "\t2. All your level information and benchmarks\n" +\
        "\t3. All of the rating curves for your stations\n" +\
        "\t4. Historical measurements to compare with your current measurement and rating curve"
        self.bmReportPathLbl = "Benchmark Report(.csv)"
        self.minMaxHistLbl = "Include Hist. Min/Max?"
        self.minMaxHint = "Number of historical minimum and maximum discharge you would like to include!"
        self.ngExportLabel = "Export the Data from AQUARIUS NG?"
        self.runButtonLbl = "Run"
        self.canButtonLbl = "Close"

        self.server = 'http://hws-aipoll.mb.ec.gc.ca'
        self.ngserver = "http://wsc.aquaticinformatics.net/AQUARIUS/Publish/v2/"
        # self.server = 'http://hwp-app-stage2.to.on.ec.gc.ca'
        self.iconName = "icon_transparent.ico"

        self.isoTail = ".000"
        self.openStationHelpDesc = "The station list file can be in csv or txt format, but the first row is reserved \
for headers and the 'Station ID' should always be in the first column \n\n\
For example:\n\
        STATION ID,STATION NAME\n\
        05EF001,NORTH SASKATCHEWAN RIVER NEAR DEER CREEK\n\
        05FE004,BATTLE RIVER NEAR THE SASKATCHEWAN BOUNDARY\n\
        00XX000,----\n\
        00XX000,----\n\n(*Station name is not mandatory!)"
        self.progressIsOpen = False

        self.path = path
        self.EHSNGui = EHSNGui
        self.mode = mode
        self.titleFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        self.labelWidth = 65

        self.manager = AQUARIUSDataExtractionToolManager(self.mode, scriptLoc, self, EHSNGui)
        self.SetTitle(self.titleLbl)

        self.InitUI()


    def InitUI(self):
        if self.mode == "DEBUG":
            print "AQUARIUS Data Extraction Tool Frame"

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)
        basePanel = wx.Panel(self)

        icon_path = self.iconName
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, icon_path)

        #PNG Icon
        if os.path.exists(icon_path):
            png = wx.Image(icon_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.icon = wx.Icon(png)
            self.SetIcon(self.icon)



        # Path Title
        pathSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathTitle = wx.StaticText(basePanel, label=self.pathTitleLbl, style=wx.ALIGN_CENTER_HORIZONTAL)
        pathTitle.SetFont(self.titleFont)
        pathSizer.Add(pathTitle, 1, wx.EXPAND|wx.LEFT, 5)
        # pathSizer.Add((-1, -1), 1, wx.EXPAND)

        # Stations
        stationSizer = wx.BoxSizer(wx.HORIZONTAL)
        stationLabel = wx.StaticText(basePanel, label=self.stationLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        self.stationCtrl = wx.TextCtrl(basePanel, style=wx.TE_PROCESS_ENTER|wx.TE_BESTWRAP)
        self.stationCtrl.Bind(wx.EVT_TEXT, self.OnTextTypeStation)
        self.stationCtrl.SetHint("02KF015, 01CC002, 07EF001, ....")
        stationSizer.Add(stationLabel, 0, wx.EXPAND|wx.TOP, 5)
        stationSizer.Add(self.stationCtrl, 1, wx.EXPAND|wx.LEFT, 6)

        # stationBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.statoinBtn = wx.Button(basePanel, label="Stations List From File", size=(-1, -1))
        self.statoinBtn.Bind(wx.EVT_BUTTON, self.OnStationBrowse)

        self.stationListHelpBtn = wx.Button(basePanel, size=(15, 15), label="!")
        self.stationListHelpBtn.SetForegroundColour('red')
        self.stationListHelpBtn.Bind(wx.EVT_BUTTON, self.OnOpenStationHelp)


        stationSizer.Add(self.statoinBtn, 0, wx.EXPAND|wx.LEFT, 6)
        stationSizer.Add(self.stationListHelpBtn, 0)

        # stationBtnSizer.Add(self.statoinBtn, 0, wx.EXPAND, 5)


        # Import list
        importSizer = wx.BoxSizer(wx.HORIZONTAL)
        importTitle = wx.StaticText(basePanel, label=self.importTitleLbl, style=wx.ALIGN_LEFT)
        importTitle.SetFont(self.titleFont)
        importSizer.Add(importTitle, 1, wx.EXPAND|wx.LEFT, 4)
        importSizer.Add((-1, -1), 1, wx.EXPAND)


        # Station Information Checkbox
        stnCkboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.stnCkbox = wx.CheckBox(basePanel, label=self.stnCkboxLbl, style=wx.ALIGN_LEFT)
        self.stnCkbox.SetValue(True)
        stnCkboxSizer.Add(self.stnCkbox, 0, wx.EXPAND)

        # Levels Information Checkbox
        lvlCkboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lvlCkbox = wx.CheckBox(basePanel, label=self.lvlCkboxLbl, style=wx.ALIGN_LEFT)
        self.lvlCkbox.SetValue(True)
        lvlCkboxSizer.Add(self.lvlCkbox, 0, wx.EXPAND)


        # Rating Curve Checkbox
        rcCkboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rcCkbox = wx.CheckBox(basePanel, label=self.rcCkboxLbl, style=wx.ALIGN_LEFT)
        self.rcCkbox.SetValue(True)
        rcCkboxSizer.Add(self.rcCkbox, 0, wx.EXPAND)

        #Data period From/To
        dataPeriodSizer = wx.BoxSizer(wx.VERTICAL)

        dataperiodTextSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dataPeriodCkbox = wx.CheckBox(basePanel, label=self.dataPeriodTxtLbl, style=wx.ALIGN_LEFT)
        self.dataPeriodCkbox.Bind(wx.EVT_CHECKBOX, self.OnDataPeriodCheck)
        self.dataPeriodCkbox.SetValue(True)
        dataperiodTextSizer.Add(self.dataPeriodCkbox, 0, wx.EXPAND)
        dataperiodTextSizer.Add((-1, -1), 1, wx.EXPAND)


        self.dataPeriodFromTxt = wx.StaticText(basePanel, label=self.dataPeriodFromTxtLbl, size=(30, -1), style=wx.ALIGN_RIGHT)
        self.dataPeriodFromPicker = adv.DatePickerCtrl(basePanel, style=wx.adv.DP_DROPDOWN, size=(-1, -1))
        year = datetime.datetime.now().year - 2
        self.dataPeriodFromPicker.SetValue(wx.DateTime.FromDMY(1, 0, year))
        self.dataPeriodToTxt = wx.StaticText(basePanel, label=self.dataPeriodToTxtLbl, size=(20, -1), style=wx.ALIGN_RIGHT)
        self.dataPeriodToPicker = adv.DatePickerCtrl(basePanel, style=wx.adv.DP_DROPDOWN, size=(-1, -1))


        dataperiodTextSizer.Add(self.dataPeriodFromTxt, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        dataperiodTextSizer.Add(self.dataPeriodFromPicker, 0, wx.EXPAND)
        dataperiodTextSizer.Add(self.dataPeriodToTxt, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        dataperiodTextSizer.Add(self.dataPeriodToPicker, 0, wx.EXPAND)

        dataPeriodSizer.Add(dataperiodTextSizer, 0, wx.EXPAND)
        # dataPeriodSizer.Add(dataPeriodRangeSizer, 0, wx.EXPAND)
        self.includeMinMaxCkbox = wx.CheckBox(basePanel, label=self.minMaxHistLbl)
        self.includeMinMaxCkbox.Bind(wx.EVT_CHECKBOX, self.OnMinMaxCkBox)
        self.includeMinMaxCkbox.SetValue(True)

        self.minMaxSpinCtrl = wx.SpinCtrl(basePanel, min=0, max=10, initial=3, size=(40,-1))
        self.minMaxSpinCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnMinMaxSpinCtrl)
        self.minMaxHintBtn = wx.Button(basePanel, size=(15, 10), label="!")
        self.minMaxHintBtn.SetForegroundColour('red')
        self.minMaxHintBtn.Bind(wx.EVT_BUTTON, self.OnMinMaxHintBtn)

        minMaxSizer = wx.BoxSizer(wx.HORIZONTAL)
        minMaxSizer.Add((-1, -1), 1, wx.EXPAND)
        minMaxSizer.Add(self.includeMinMaxCkbox, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        minMaxSizer.Add(self.minMaxSpinCtrl, 0, wx.EXPAND|wx.TOP, 5)
        minMaxSizer.Add(self.minMaxHintBtn, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        dataPeriodSizer.Add(minMaxSizer, 0, wx.EXPAND)


        # Location Selector
        locSizer = wx.BoxSizer(wx.VERTICAL)
        exportSizer = wx.BoxSizer(wx.HORIZONTAL)
        browseSizer = wx.BoxSizer(wx.HORIZONTAL)
        locLabel = wx.StaticText(basePanel, label=self.pathLbl, size=(80, -1), style=wx.ALIGN_RIGHT)
        self.locText = wx.StaticText(basePanel, size=(-1, 40), label=self.path, style=wx.SIMPLE_BORDER)

        exportSubtext = wx.StaticText(basePanel, size=(-1, 35), label=self.exportSubtxtLbl)
        self.locButton = wx.Button(basePanel, label=self.browseLbl)
        self.locButton.Bind(wx.EVT_BUTTON, self.OnBrowse)

        exportSizer.Add(locLabel, 0, wx.EXPAND|wx.TOP, 0)
        exportSizer.Add(self.locText, 1, wx.EXPAND|wx.LEFT, 6)

        browseSizer.Add(exportSubtext, 1, wx.EXPAND)
        browseSizer.Add(self.locButton, 0, wx.LEFT, 6)

        locSizer.Add(exportSizer, 0, wx.EXPAND|wx.ALL, 2)
        locSizer.Add(browseSizer, 0, wx.EXPAND|wx.ALL, 2)


        #Fold panel Bar
        self.foldBool = True
        hintSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_bar = fpb.FoldPanelBar(basePanel, -1, agwStyle=fpb.FPB_VERTICAL)
        self.panel_bar.Bind(fpb.EVT_CAPTIONBAR, self.OnHint)
        fold_panel = self.panel_bar.AddFoldPanel("Show some hints")
        # thing = wx.TextCtrl(fold_panel, -1, size=(555, -1), style=wx.TE_MULTILINE)
        hintText = wx.StaticText(fold_panel, -1, size=(555, -1), label=self.hint)


        # self.panel_bar.AddFoldPanelWindow(fold_panel, thing)
        self.panel_bar.AddFoldPanelWindow(fold_panel, hintText)


        # hintSizer.Add(self.panel_bar, 1, wx.EXPAND|wx.ALL, 5)


        # #Collapsible Panel
        # hintSizer = wx.BoxSizer(wx.VERTICAL)
        # self.hintCollPane = wx.CollapsiblePane(basePanel, wx.ID_ANY, style=wx.CP_NO_TLW_RESIZE, size=(-1,40), label="Show some hints")
        # self.hintCollPane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnHint)
        # hintSizer.Add(self.hintCollPane, 0, wx.EXPAND|wx.ALL, 5)

        # self.win = self.hintCollPane.GetPane()
        # hintText = wx.StaticText(self.win, label=self.hint)
        # hintDetailsSizer = wx.BoxSizer(wx.VERTICAL)
        # self.win.SetSizer(hintDetailsSizer)
        # hintDetailsSizer.Add(hintText, 0, wx.EXPAND|wx.ALL, 5)
        # # hintDetailsSizer.SetSizeHints(self.win)


        # Login
        loginSizer = wx.BoxSizer(wx.HORIZONTAL)
        loginTitle = wx.StaticText(basePanel, label=self.loginTitleLbl, size=(140, -1))
        loginTitle.SetFont(self.titleFont)
        loginSizer.Add(loginTitle, 0, wx.EXPAND|wx.LEFT, 5)
        loginSizer.Add((-1, -1), 1, wx.EXPAND)


        # Username
        usernameSizer = wx.BoxSizer(wx.HORIZONTAL)
        usernameLabel = wx.StaticText(basePanel, label=self.usernameLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        self.usernameCtrl = wx.TextCtrl(basePanel)
        usernameSizer.Add(usernameLabel, 0, wx.EXPAND|wx.TOP, 5)
        usernameSizer.Add(self.usernameCtrl, 1, wx.EXPAND|wx.LEFT, 6)

        # Password
        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordLabel = wx.StaticText(basePanel, label=self.passwordLbl, size=(self.labelWidth, -1), style=wx.ALIGN_RIGHT)
        self.passwordCtrl = wx.TextCtrl(basePanel, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.passwordCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnRun)
        passwordSizer.Add(passwordLabel, 0, wx.EXPAND|wx.TOP, 5)
        passwordSizer.Add(self.passwordCtrl, 1, wx.EXPAND|wx.LEFT, 6)


        # Buttons
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ngExportChk = wx.CheckBox(basePanel, label=self.ngExportLabel, style=wx.ALIGN_LEFT)
        self.ngExportChk.SetValue(True)
        self.runButton = wx.Button(basePanel, label=self.runButtonLbl)
        self.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
        self.canButton = wx.Button(basePanel, label=self.canButtonLbl)
        self.canButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        buttonsSizer.Add((-1, -1), 1, wx.EXPAND)
        buttonsSizer.Add(self.ngExportChk, 0, wx.EXPAND | wx.RIGHT, 4)
        buttonsSizer.Add(self.runButton, 0, wx.EXPAND|wx.RIGHT, 4)
        buttonsSizer.Add(self.canButton, 0, wx.EXPAND|wx.LEFT, 4)


        # Layout Sizer
        self.layoutSizer.Add(pathSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 5), 0, wx.EXPAND)
        self.layoutSizer.Add(stationSizer, 0, wx.EXPAND|wx.ALL, 4)
        # self.layoutSizer.Add(stationBtnSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 10), 0, wx.EXPAND)

        self.layoutSizer.Add(importSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 1), 0, wx.EXPAND)
        self.layoutSizer.Add(stnCkboxSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 1), 0, wx.EXPAND)
        self.layoutSizer.Add(lvlCkboxSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 1), 0, wx.EXPAND)
        self.layoutSizer.Add(rcCkboxSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 1), 0, wx.EXPAND)
        self.layoutSizer.Add(dataPeriodSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add((-1, 1), 0, wx.EXPAND)
        self.layoutSizer.Add(locSizer, 0, wx.EXPAND|wx.ALL, 4)




        # self.layoutSizer.Add(dataPeriodTxt, 0, wx.EXPAND)
        # self.layoutSizer.Add(dataPeriodRangeSizer, 0, wx.EXPAND)
        self.layoutSizer.Add((-1, 15), 0, wx.EXPAND)
        self.layoutSizer.Add(loginSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add(usernameSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 4)
        self.layoutSizer.Add((-1, 5), 0, wx.EXPAND)
        self.layoutSizer.Add(passwordSizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 4)
        self.layoutSizer.Add((-1, 5), 0, wx.EXPAND)
        self.layoutSizer.Add(buttonsSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.layoutSizer.Add(self.panel_bar, 1, wx.EXPAND|wx.ALL, 4)

        basePanel.SetSizer(self.layoutSizer)
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
    def OnDataPeriodCheck(self, evt):
        if self.dataPeriodCkbox.IsChecked():
            self.dataPeriodFromPicker.Enable(True)
            self.dataPeriodToPicker.Enable(True)
            self.dataPeriodFromTxt.Enable(True)
            self.dataPeriodToTxt.Enable(True)
            self.includeMinMaxCkbox.Enable(True)
            if self.includeMinMaxCkbox.GetValue():
                self.minMaxSpinCtrl.Enable(True)
                self.minMaxHintBtn.Enable(True)
        else:
            self.dataPeriodFromPicker.Enable(False)
            self.dataPeriodToPicker.Enable(False)
            self.dataPeriodFromTxt.Enable(False)
            self.dataPeriodToTxt.Enable(False)
            self.includeMinMaxCkbox.Enable(False)
            self.minMaxSpinCtrl.Enable(False)
            self.minMaxHintBtn.Enable(False)

    def OnHint(self, event):
        # self.CacheBestSize(self.GetBestSize())
        if self.foldBool:

            self.SetSize((555, 560))
            self.foldBool = False
        else:
            self.SetSize((555, 690))
            self.foldBool = True
        self.Layout()
        event.Skip()


        # if self.hintCollPane.IsCollapsed():
        #     self.SetSize((555, 580))

        # else:
        #     self.hintCollPane.Expand()

        #     self.SetSize((555, 630))
        #     self.win.SetSize((521, 116))
        #     print self.win.GetSize()
        # print self.win
        # print self.win.GetSize()
        # event.Skip()

    def OnBrowse(self, e):
        fileOpenDialog = wx.DirDialog(self, self.browseTitleLbl, self.path)
        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        self.path = fileOpenDialog.GetPath()
        self.locText.SetLabel(self.path)

        self.layoutSizer.Layout()
        self.Update()
        self.Refresh()

    #Capitalization for station IDs
    def OnTextTypeStation(self, event):
        insertPoint = self.stationCtrl.GetInsertionPoint()
        self.stationCtrl.ChangeValue(unicode.upper(self.stationCtrl.GetValue()))
        self.stationCtrl.SetInsertionPoint(insertPoint)

    # Run Script
    def OnRun(self, e):
        if self.mode == "DEBUG":
            print "Run Script"
        ########################################################################################################
        # try:
        #     self.manager.RunScript(self.path)
        # except Exception as inst:
        #     print inst
        #     errorFile = open(self.path + r"\ErrorFile.txt","ab")
        #     errorFile.write(str(inst) + "\n")
        #     errorFile.close()
        #     self.Destroy()
        #     self.dialog.Destroy()
        #     return


        # switch the next ling for debugging################################################################
        #try maximum 3 times if disconnected from server
        if not self.ExportFromNgChecked():
            for i in range(3):
                try:

                    self.manager.RunScript(self.path)
                    break
                # except socket.error:
                except:
                    print "error detected, reconnecting"
                    self.manager.RunScript(self.path)
            else:
                print "disconnected by the server"
                print "========================================="
                print socket.error

        #######################################################################################################


        # for i in range(3):
        #     try:
        #         self.manager.RunScript(self.path)
        #         break
        #     except Exception as inst:
        #         print inst
        #         errorFile = open(self.path + r"\ErrorFile.txt","ab")
        #         errorFile.write(str(inst) + "\tRunScript attampt " + str(i+1) + "\n")
        #         errorFile.close()
        #         self.dialog.Destroy()
        # else:
        #     print "Time out. Max attempts reached"
        #     self.CreateErrorDialog("Time out...")
        #     self.Destroy()
        #     return

        #################################################################################################

            self.manager.EHSNGui.ratingFileDir = self.path
            if self.manager.EHSNGui.savedStationsPath == self.manager.EHSNGui.ratingFileDir + '\\stations.txt':

                try:
                    self.manager.EHSNGui.OpenStationFile(self.manager.EHSNGui.ratingFileDir + '\\stations.txt')
                    self.manager.EHSNGui.savedStationsPath = self.manager.EHSNGui.ratingFileDir + '\\stations.txt'
                except:
                    print "error open station file --- OnRun extraction tool frame"

            if self.manager.EHSNGui.savedLevelsPath == self.manager.EHSNGui.ratingFileDir + '\\levels.txt':

                try:
                    self.manager.EHSNGui.OpenLevelFile(self.manager.EHSNGui.ratingFileDir + '\\levels.txt')
                    self.manager.EHSNGui.savedLevelsPath = self.manager.EHSNGui.ratingFileDir + '\\levels.txt'
                except:
                    print "error open level file --- OnRun extraction tool frame"
        else:
            print("NG")
            for i in range(3):
                try:

                    self.manager.RunScriptNg(self.path)
                    break
                # except socket.error:
                except:
                    print "error detected, reconnecting"
                    self.manager.RunScriptNg(self.path)
            else:
                print "disconnected by the server"
                print "========================================="
                print socket.error


    def OnCancel(self, e):
        if self.mode == "DEBUG":
            print "Cancel"
        self.EHSNGui.ratingCurveExtraction = None
        self.Destroy()

    def OnMinMaxCkBox(self, e):
        if self.includeMinMaxCkbox.GetValue():
            self.minMaxSpinCtrl.Enable()
            self.minMaxHintBtn.Enable()
            if self.minMaxSpinCtrl.GetValue() < 1:
                self.minMaxSpinCtrl.SetValue(3)
        else:
            self.minMaxSpinCtrl.Disable()
            self.minMaxHintBtn.Disable()

    def OnMinMaxHintBtn(self, e):
        dlg = wx.MessageDialog(self, self.minMaxHint, 'Hint', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return

    def OnMinMaxSpinCtrl(self, e):
        if self.minMaxSpinCtrl.GetValue() < 1:
            self.includeMinMaxCkbox.SetValue(False)
            self.minMaxSpinCtrl.Disable()
            self.minMaxHintBtn.Disable()

    def GetUsername(self):
        return self.usernameCtrl.GetValue()

    def GetPassword(self):
        return self.passwordCtrl.GetValue()

    def GetStationList(self):
        return self.stationCtrl.GetValue()

    def StationListIsEmpty(self):
        return self.stationCtrl.GetValue().strip() == ""

    def GetURL(self):
        if not self.ExportFromNgChecked():
            return self.server
        else:
            return self.ngserver

    def GetPath(self):
        return self.locText.GetLabel()


    def CreateTryAgainDialog(self, message):
        info = wx.MessageDialog(None, message, "Error",
                                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_ERROR)
        if info.ShowModal() == wx.ID_YES:
            return 0
        else:
            return -1

    def CreateErrorDialog(self, message):
        info = wx.MessageDialog(None, message, "Error",
                                wx.OK | wx.ICON_ERROR)
        info.ShowModal()

    def CreateMessageDialog(self, message, title):
        info = wx.MessageDialog(None, message, title, wx.OK)
        info.ShowModal()

    def CreateProgressDialog(self, title, message):
        self.dialog = wx.ProgressDialog(title, message, 1, style=wx.PD_AUTO_HIDE) # |wx.PD_APP_MODAL)
        self.dialog.Pulse()
        self.progressIsOpen = True

    def UpdateProgressDialog(self, message):
        self.dialog.Pulse(message)

    def DeleteProgressDialog(self):
        self.dialog.Update(1)
        self.dialog.Destroy()
        self.progressIsOpen = False
        print 'destroyed'

    def ProgressDialogIsOpen(self):
        return self.progressIsOpen


    def StnIsChecked(self):
        return self.stnCkbox.IsChecked()

    def LvlIsChecked(self):
        return self.lvlCkbox.IsChecked()

    def RCIsChecked(self):
        return self.rcCkbox.IsChecked()

    def ExportFromNgChecked(self):
        return self.ngExportChk.IsChecked()

    def DataPeriodIsChecked(self):
        return self.dataPeriodCkbox.IsChecked()

    def GetDataPeriodFrom(self):
        return self.dataPeriodFromPicker.GetValue()

    def GetDataPeriodTo(self):
        return self.dataPeriodToPicker.GetValue()

    def IncludeMinMaxIsChecked(self):
        return self.includeMinMaxCkbox.GetValue()

    def GetNumOfMinMax(self):
        return self.minMaxSpinCtrl.GetValue()

    #Select the file contains the station IDs to be extracted
    def OnStationBrowse(self, event):
        fileOpenDialog = wx.FileDialog(self, 'Select Stations File', os.getcwd(), '',
                            'Uploading Stations (*.txt)|*.txt|Uploading Stations (*.csv)|*.csv',
                                       style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return


        path = fileOpenDialog.GetPath()

        if self.mode == "DEBUG":
            print "path open"
            print path

        if path != "":

            fileName = fileOpenDialog.GetFilename()
            self.OpenStationFile(fileName)


        fileOpenDialog.Destroy()



    #Read the station IDs from the file specisifed
    def OpenStationFile(self, file):

        self.numsRead = []

        if os.path.isfile(file):

            with open(file) as stations:
                lines = stations.readlines()
                # lines = [unicode(x) for y in lines for x in y]

            for item in lines:
                items = item.split(',')
                self.numsRead.append(items[0])


            self.numsRead = self.numsRead[1:]
            newNums = sorted(self.numsRead)

        text = ""

        for i, item in enumerate(newNums):
            if i != len(newNums) - 1:
                text += (item + ", ")
            else:
                text += item

        self.stationCtrl.SetValue(text)


    def OnOpenStationHelp(self, event):
        dlg = wx.MessageDialog(self, self.openStationHelpDesc, 'Hint', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return




def main():
    app = wx.App()

    frame = AQUARIUSDataExtractionToolFrame("DEBUG", os.getcwd() + "\\AQ_Extracted_Data",
                                           os.getcwd() + "\\EHSN_rating_curve.exe", None, None, size=(550, 470))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
