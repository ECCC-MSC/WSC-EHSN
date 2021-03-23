# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import os
import sys
import shutil
from zipfile import ZipFile
from ElectronicFieldNotesGUI import *
from AttachmentTitle import *
from AttachTag import *
from AttachBox import *
from AttachFolderBox import *
from AttachPhotoBox import *
import ntpath
import tempfile
from os import chdir
from os import environ
from os.path import join
from os.path import dirname

def valid(path):
    if path != None and path != "" and not path.isspace():
        return True
    return False

class AttachmentPanel(wx.Panel):
    def __init__(self, parent, mode, lang, *args, **kwargs):
        super(AttachmentPanel, self).__init__(*args, **kwargs)
        self.parent = parent
        self.mode = mode
        self.lang = lang
        self.indent = (50, -1)
        self.indent2 = (55, -1)
        self.indent3 = (25, -1)
        self.noteIndent = (55, -1)
        self.barSize = (741, -1)
        self.tagSize = (300, -1)
        self.zipSpace = (1100, -1)
        self.missingStnNumMessage = "Station Number is missing"
        self.missingStnNumTitle = "Missing Station Number"
        self.nonexistentMessage = " does not exist"
        self.nonexistentTitle = "Target file does not exist"
        self.successMessage = "File are successfully zipped: "
        self.successTitle = "File successfully zipped"
        self.missingZipTitle = "Missing Zip Folder"
        self.missingZipMessage = "Zip Folder not Found"
        self.reviewMessage = "The notes are not reviewed"
        self.reviewTitle = "Missing Review"
        self.rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.mmtFilesTitle = "Select the MMT Files Folder"
        self.loggerFilesTitle = "Select the Logger Files Folder"
        self.zipTitle = "Choose zip file location"
        self.fm = "%Y%m%d"
        self.zipPath = ""
        self.legendHeader = "Photos and Drawings: "
        self.legend = "SIT - Site (general view of the monitoring area)\n" \
                      "STR - Structures, Site Facilities (includes construction)\n" \
                      "COL - Control Conditions (view of channel)\n" \
                      "CBL - Cableway\n" \
                      "EQP - Device (general view of monitoring equipment deployed)\n" \
                      "CDT - Device Conditions (includes details for vandalism)\n" \
                      "HSN - Hydrometric Survey Note"
        self.InitUI()

    def InitUI(self):
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.layout)

        sizerList = []
        for i in range(12):
            sizerList.append(wx.BoxSizer(wx.HORIZONTAL))

        spaceList = []
        for x in range(10):
            spaceList.append(wx.StaticText(self, label=""))
        note = wx.StaticText(self, label="The survey note will be saved as xml and a pdf will be created at the time of zipping. The xml and pdf will both be zipped into the zip file")

        TitlePanel = AttachmentTitle(self.mode, self)
        Txt1 = AttachTag("Logger Data files", "", self, size = self.tagSize)
        self.attachBox1 = AttachBox(self, "*", self, size=(860, 100), style=wx.SIMPLE_BORDER)

        Txt2 = AttachTag("Logger Diagnostic files", "", self, size=self.tagSize)
        self.attachBox2 = AttachBox(self, "*", self, size=(860, 100), style=wx.SIMPLE_BORDER)

        Txt3 = AttachTag("Logger Program files", "", self, size = self.tagSize)
        self.attachBox3 = AttachBox(self, "*", self, size=(860, 100), style=wx.SIMPLE_BORDER)

        Txt4 = AttachTag("Logger files folder", "", self, size=self.tagSize)
        self.attachBox4 = AttachFolderBox(self, "*", self, size=(860, 100), style=wx.SIMPLE_BORDER)

        Txt5 = AttachTag("Discharge Measurement files or folder", "", self, size = self.tagSize)
        self.attachBox5 = AttachFolderBox(self, "*", self, size=(860, 100), style=wx.SIMPLE_BORDER)

        Txt6 = AttachTag("Discharge Measurement Summary files", "", self, size = self.tagSize)
        self.attachBox6 = AttachBox(self, "*", self, size=(860, 100), style=wx.SIMPLE_BORDER)

        Txt7 = AttachTag("Photos and Drawings", "(.jpg, .DWG, etc.)", self, size=self.tagSize)
        self.attachBox7 = AttachPhotoBox(self, "*", self, size=(860, 200), style=wx.SIMPLE_BORDER)

        zipLoc = AttachTag("ZIP LOCATION", "", self, size=self.tagSize)
        self.zipAddr = wx.TextCtrl(self, size=self.barSize)
        self.zipChoose = wx.Button(self, label="SELECT")
        self.zipChoose.Bind(wx.EVT_BUTTON, self.BrowseZipLoc)
        self.zipAddr.SetValue(self.rootPath)

        self.zipper = wx.Button(self, label="ZIP")
        self.zipper.Bind(wx.EVT_BUTTON, self.Zip)

        legendHeader = wx.StaticText(self, label=self.legendHeader)
        legend = wx.StaticText(self, label=self.legend)

        sizerList[0].Add(self.indent)
        sizerList[0].Add(Txt1, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[0].Add(self.attachBox1)

        sizerList[1].Add(self.indent)
        sizerList[1].Add(Txt2, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[1].Add(self.attachBox2)

        sizerList[2].Add(self.indent)
        sizerList[2].Add(Txt3, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[2].Add(self.attachBox3)

        sizerList[3].Add(self.indent)
        sizerList[3].Add(Txt4, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[3].Add(self.attachBox4)

        sizerList[4].Add(self.indent)
        sizerList[4].Add(Txt5, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[4].Add(self.attachBox5)

        sizerList[5].Add(self.indent)
        sizerList[5].Add(Txt6, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[5].Add(self.attachBox6)

        sizerList[6].Add(self.indent)
        sizerList[6].Add(Txt7, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[6].Add(self.attachBox7)

        sizerList[7].Add(self.indent)
        sizerList[7].Add(zipLoc, 1, wx.EXPAND | wx.ALL, 5)
        sizerList[7].Add(self.zipAddr)
        sizerList[7].Add(self.zipChoose)

        sizerList[8].Add(self.noteIndent)
        sizerList[8].Add(note)

        sizerList[9].Add(self.zipSpace)
        sizerList[9].Add(self.zipper)

        sizerList[10].Add(self.indent2)
        sizerList[10].Add(legendHeader)
        sizerList[11].Add(self.indent2)
        sizerList[11].Add(self.indent3)
        sizerList[11].Add(legend)
        self.layout.Add(TitlePanel, 0, wx.EXPAND | wx.ALL, 3)
        for i in range(10):
            self.layout.Add(spaceList[i])
            self.layout.Add(sizerList[i])
        self.layout.Add(sizerList[10])
        self.layout.Add(sizerList[11])

    def BrowseZipLoc(self, evt):
        DirOpenDialog = wx.DirDialog(self, self.zipTitle, self.rootPath,
                                     style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if DirOpenDialog.ShowModal() == wx.ID_CANCEL:
            DirOpenDialog.Destroy()
            return

        self.zipPath = DirOpenDialog.GetPath()
        self.zipAddr.ChangeValue(self.zipPath)

        DirOpenDialog.Destroy()

    def Zip(self, evt):
        if not self.parent.partyInfo.reviewedCB.GetValue():
            info = wx.MessageDialog(None, self.reviewMessage, self.reviewTitle,
                                    wx.OK)
            info.ShowModal()
            return

        zipPath = self.zipAddr.GetValue()
        if zipPath == "" or zipPath.isspace() or not os.path.exists(zipPath):
            info = wx.MessageDialog(None, self.missingZipMessage, self.missingZipTitle,
                                    wx.OK)
            info.ShowModal()
            return

        stnNum = self.parent.genInfo.stnNumCmbo.GetValue()
        if stnNum == "" or stnNum.isspace():
            info = wx.MessageDialog(None, self.missingStnNumMessage, self.missingStnNumTitle,
                                    wx.OK)
            info.ShowModal()
            return
        date = self.parent.genInfo.datePicker.GetValue().Format(self.fm)

        Tag = stnNum + "_" + date + "_FV"
        filePath = self.parent.dir + "\\" + Tag
        boxList = [self.attachBox1, self.attachBox2, self.attachBox3, self.attachBox4, self.attachBox5, self.attachBox6, self.attachBox7]
        pathList = []
        for box in boxList:
            pathList.append(box.returnPath())

        pdfPath = filePath + ".pdf"
        xmlPath = filePath + ".xml"

        for pathGroup in pathList:
            for path in pathGroup:
                if path != "" and not os.path.exists(path) and not path.isspace():
                    info = wx.MessageDialog(None, "File Address: " + path + self.nonexistentMessage, self.nonexistentTitle,
                                            wx.OK)
                    info.ShowModal()
                    return

        loggerDownload = self.attachBox1.returnPath() + self.attachBox4.returnFilePath()
        loggerDiagnostic = self.attachBox2.returnPath()
        loggerProgram = self.attachBox3.returnPath()
        loggerFolder = self.attachBox4.returnFolderPath()
        mmtPdf = self.attachBox6.returnPath() + self.attachBox5.returnFilePath()
        mmtFolder = self.attachBox5.returnFolderPath()

        SIT = self.attachBox7.returnSIT()
        STR = self.attachBox7.returnSTR()
        COL = self.attachBox7.returnCOL()
        CBL = self.attachBox7.returnCBL()
        EQP = self.attachBox7.returnEQP()
        CDT = self.attachBox7.returnCDT()
        HSN = self.attachBox7.returnHSN()

        dir_temp = tempfile.mkdtemp()
        count = 0
        for i in range(len(loggerDownload)):
            if valid(loggerDownload[i]):
                count += 1
                name, extension = os.path.splitext(loggerDownload[i])
                rename = stnNum + "_" + date + ".LG" + str(count) + extension
                shutil.copy(loggerDownload[i], dir_temp + "\\" + rename)
                loggerDownload[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(loggerDiagnostic)):
            if valid(loggerDiagnostic[i]):
                count += 1
                name, extension = os.path.splitext(loggerDiagnostic[i])
                rename = stnNum + "_" + date + ".LD" + str(count) + extension
                shutil.copy(loggerDiagnostic[i], dir_temp + "\\" + rename)
                loggerDiagnostic[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(loggerProgram)):
            if valid(loggerProgram[i]):
                count += 1
                name, extension = os.path.splitext(loggerProgram[i])
                rename = stnNum + "_" + date + ".LP" + str(count) + extension
                shutil.copy(loggerProgram[i], dir_temp + "\\" + rename)
                loggerProgram[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(mmtPdf)):
            if valid(mmtPdf[i]):
                count += 1
                name, extension = os.path.splitext(mmtPdf[i])
                rename = stnNum + "_" + date + ".M" + str(count) + extension
                shutil.copy(mmtPdf[i], dir_temp + "\\" + rename)
                mmtPdf[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(SIT)):
            if valid(SIT[i]):
                count += 1
                name, extension = os.path.splitext(SIT[i])
                rename = stnNum + "_" + date + ".SIT (" + str(count) + ")" + extension
                shutil.copy(SIT[i], dir_temp + "\\" + rename)
                SIT[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(STR)):
            if valid(STR[i]):
                count += 1
                name, extension = os.path.splitext(STR[i])
                rename = stnNum + "_" + date + ".STR (" + str(count) + ")" + extension
                shutil.copy(STR[i], dir_temp + "\\" + rename)
                STR[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(COL)):
            if valid(COL[i]):
                count += 1
                name, extension = os.path.splitext(COL[i])
                rename = stnNum + "_" + date + ".COL (" + str(count) + ")"  + extension
                shutil.copy(COL[i], dir_temp + "\\" + rename)
                COL[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(CBL)):
            if valid(CBL[i]):
                count += 1
                name, extension = os.path.splitext(CBL[i])
                rename = stnNum + "_" + date + ".CBL (" + str(count) + ")" + extension
                shutil.copy(CBL[i], dir_temp + "\\" + rename)
                CBL[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(EQP)):
            if valid(EQP[i]):
                count += 1
                name, extension = os.path.splitext(EQP[i])
                rename = stnNum + "_" + date + ".EQP (" + str(count) + ")" + extension
                shutil.copy(EQP[i], dir_temp + "\\" + rename)
                EQP[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(CDT)):
            if valid(CDT[i]):
                count += 1
                name, extension = os.path.splitext(CDT[i])
                rename = stnNum + "_" + date + ".CDT (" + str(count) + ")" + extension
                shutil.copy(CDT[i], dir_temp + "\\" + rename)
                CDT[i] = dir_temp + "\\" + rename
        count = 0
        for i in range(len(HSN)):
            if valid(HSN[i]):
                count += 1
                name, extension = os.path.splitext(HSN[i])
                rename = stnNum + "_" + date + ".HSN (" + str(count) + ")" + extension
                shutil.copy(HSN[i], dir_temp + "\\" + rename)
                HSN[i] = dir_temp + "\\" + rename

        self.parent.manager.ExportAsXML(xmlPath, None)
        try:
            self.parent.manager.ExportAsPDFWithoutOpen(pdfPath, self.parent.viewStyleSheetFilePath)
        except:
            info = wx.MessageDialog(self, self.parent.savePDFErrorMsg, self.parent.savePDFErrorTitle,
                                    wx.OK | wx.ICON_ERROR)
            info.ShowModal()
            return

        zipfile = ZipFile(zipPath + "\\" + Tag + '.zip', 'w')
        zipfile.write(ntpath.basename(pdfPath), Tag + "\\" + ntpath.basename(pdfPath))
        zipfile.write(xmlPath, ntpath.basename(xmlPath))

        for path in loggerDownload:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in loggerProgram:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in mmtPdf:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        count = 0
        for folder in mmtFolder:
            if valid(folder):
                count += 1
                for file in os.listdir(folder):
                    zipfile.write(folder + "\\" + file, Tag + "\\" + Tag + "_M" + str(count) + "\\" + file)
        count = 0
        for folder in loggerFolder:
            if valid(folder):
                count += 1
                for file in os.listdir(folder):
                    zipfile.write(folder + "\\" + file, Tag + "\\" + Tag + "_LG" + str(count) + "\\" + file)
        for path in SIT:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in STR:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in COL:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in CBL:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in EQP:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in CDT:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))
        for path in HSN:
            if valid(path):
                zipfile.write(path, Tag + "\\" + ntpath.basename(path))

        zipfile.close()
        info = wx.MessageDialog(None, self.successMessage + Tag + " at " + zipPath, self.successTitle, wx.OK)
        self.zipPath = zipPath + "\\" + Tag + '.zip'
        info.ShowModal()

def main():
    app = wx.App()
    frame = wx.Frame(None, size=(1200, 650))
    AttachmentPanel(wx.Frame, "debug", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
