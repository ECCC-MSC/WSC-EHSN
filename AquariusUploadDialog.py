# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html
import wx
import os
import sys
import datetime
from xml.etree.ElementTree import Element

from xml.etree import ElementTree
class AquariusUploadDialog(wx.Dialog):
    def __init__(self, mode, dir, *args, **kwargs):
        super(AquariusUploadDialog, self).__init__(*args, **kwargs)

        self.config_path = self.GetParent().config_path
   
        self.configFile = ElementTree.parse(self.config_path).getroot().find('AquariusUploadDialog')


        self.stage1 = self.configFile.find('stage1').text
        self.product2 = self.configFile.find('product2').text
        self.product = self.configFile.find('product').text


        self.mode = mode

        self.servers = {'1: Staging Server 1' : self.stage1, '2: Production2 Server': self.product2,
                        '3: Production Server' : self.product}

        self.serverLbl = "Server:"
        self.usernameLbl = "Username:"
        self.passwordLbl = "Password:"
        self.uploadLbl = "Upload!"
        self.cancelLbl = "Cancel"
        self.dischargeLbl = "Upload Discharge Activity"
        self.hint = """           If unchecked, the discharge activity may be created in AQUARIUS by third party discharge summary files
         (e.g. HFC 3, WinRiver II, FlowTracker)"""

        self.dir = dir if dir is not None else str(os.getcwd())
        self.header = "The survey note will be saved as xml and a pdf will be created at the time of upload"
        self.desc = "All eHSN files must be saved at the time of upload. Where would you like this file to be saved?"
        self.changeButtonDesc = "Change"
        self.changeTitleLbl = "Choose directory & change name for xml and pdf file"
        self.uploadConfirm = "Are you sure you want to upload this file?"
        self.autoOpenLbl = "Auto Open PDF?"
        self.uploadLevelNotesLbl = 'Upload Level Notes'



        self.includeDischarge = False
        self.includeLevelNote = False
        self.SetSize((610, 310))

        self.InitUI()




    def InitUI(self):
        if self.mode == "DEBUG":
            print "Aquarius Upload Dialog"

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)

        serverSizer = wx.BoxSizer(wx.HORIZONTAL)
        serverSubSizer = wx.BoxSizer(wx.HORIZONTAL)
        serverTxt = wx.StaticText(self, label=self.serverLbl)
        self.serverCmbo = wx.ComboBox(self, choices=sorted(self.servers.keys(), reverse=False),
                                      value=sorted(self.servers.keys(), reverse=False)[2], style=wx.CB_READONLY)
        # serverSubSizer.Add((-1, -1), 1, wx.EXPAND)
        serverSubSizer.Add(serverTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 6)
        serverSizer.Add(serverSubSizer, 1, wx.EXPAND)
        serverSizer.Add(self.serverCmbo, 3, wx.EXPAND)

        usernameSizer = wx.BoxSizer(wx.HORIZONTAL)
        usernameSubSizer = wx.BoxSizer(wx.HORIZONTAL)
        usernameTxt = wx.StaticText(self, label=self.usernameLbl)
        self.usernameCtrl = wx.TextCtrl(self)
        # usernameSubSizer.Add((-1, -1), 1, wx.EXPAND)
        usernameSubSizer.Add(usernameTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 6)
        usernameSizer.Add(usernameSubSizer, 1, wx.EXPAND)
        usernameSizer.Add(self.usernameCtrl, 3, wx.EXPAND)

        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordSubSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordTxt = wx.StaticText(self, label=self.passwordLbl)
        self.passwordCtrl = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        # passwordSubSizer.Add((-1, -1), 1, wx.EXPAND)
        passwordSubSizer.Add(passwordTxt, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 6)
        passwordSizer.Add(passwordSubSizer, 1, wx.EXPAND)
        passwordSizer.Add(self.passwordCtrl, 3, wx.EXPAND)

        self.errorMessage = wx.StaticText(self, label="", size=(-1, 60))

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.autoOpenCkbox = wx.CheckBox(self, label=self.autoOpenLbl)
        self.autoOpenCkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxAutoOpen)
        self.uploadButton = wx.Button(self, label=self.uploadLbl)
        self.cancelButton = wx.Button(self, label=self.cancelLbl)
        buttonSizer.Add(self.autoOpenCkbox, 0, wx.EXPAND|wx.ALL, 3)
        buttonSizer.Add((-1, -1), 1, wx.EXPAND)
        buttonSizer.Add(self.uploadButton, 0, wx.EXPAND|wx.ALL, 3)
        buttonSizer.Add(self.cancelButton, 0, wx.EXPAND|wx.ALL, 3)

        self.uploadButton.SetDefault()
        self.uploadButton.Bind(wx.EVT_BUTTON, self.UploadToAquarius)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.Cancel)

        disSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.dischargeCkbox = wx.CheckBox(self, label='')

        # self.dischargeCkbox.SetValue(True)
        self.dischargeCkbox.Bind(wx.EVT_CHECKBOX, self.OnDischargeCheckbox)
        disLabel = wx.StaticText(self, label=self.dischargeLbl)
        disLabel.Wrap(1000)
        disSizerH.Add(self.dischargeCkbox, border=5, flag=wx.ALL)
        disSizerH.Add(disLabel, border=5, flag=wx.ALL)

        self.levelNoteCkbox = wx.CheckBox(self, label=self.uploadLevelNotesLbl)
        self.levelNoteCkbox.Bind(wx.EVT_CHECKBOX, self.OnLevelNoteCheckbox)
        # disSizerH.Add(self.levelNoteCkbox, border=5, flag=wx.ALL)


        hintTxt = wx.StaticText(self, label=self.hint)





        headerTxt = wx.StaticText(self, label=self.header)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        headerTxt.SetFont(font)

        # descTxt = wx.StaticText(self, label=self.desc)
        # font2 = wx.Font(13, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        # descTxt.SetFont(font2)

        changePanel = wx.Panel(self, style=wx.BORDER_NONE)
        changeSizer = wx.BoxSizer(wx.HORIZONTAL)
        changePanel.SetSizer(changeSizer)
        self.changeCtrl = wx.TextCtrl(changePanel, style=wx.TE_READONLY)
        self.changeCtrl.SetValue(self.dir + "\\" + self.GetParent().name)
        changeBtn = wx.Button(changePanel, label=self.changeButtonDesc)
        changeBtn.Bind(wx.EVT_BUTTON, self.OnChange)
        changeSizer.Add(self.changeCtrl, 2, wx.EXPAND)
        changeSizer.Add(changeBtn, 1, wx.EXPAND)





        self.layoutSizer.Add(serverSizer, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(usernameSizer, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(passwordSizer, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(disSizerH, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(hintTxt, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.layoutSizer.Add(self.levelNoteCkbox, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add((-1, 10), 0, wx.EXPAND)
        self.layoutSizer.Add(headerTxt, 0, wx.EXPAND|wx.ALL, 5)
        self.layoutSizer.Add(changePanel, 0, wx.EXPAND|wx.ALL, 5)

        # self.layoutSizer.Add((-1, 10), 0, wx.EXPAND)
        # self.layoutSizer.Add(self.errorMessage, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        self.layoutSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.layoutSizer.Add(buttonSizer, 0, wx.EXPAND)


        self.SetSizer(self.layoutSizer)

    def OnChange(self, e):
        if self.GetParent().name=='':
            date = datetime.datetime.strptime(str(self.GetParent().manager.genInfoManager.datePicker), self.GetParent().manager.DT_FORMAT)
            date = date.strftime("%Y%m%d")
            name = str(self.GetParent().manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV.pdf"

        else:
            name = self.GetParent().name.replace("xml", "pdf")
        fileOpenDialog = wx.FileDialog(self, self.changeTitleLbl, self.GetParent().uploadSaveDir, name, style=wx.FD_SAVE | wx.FD_CHANGE_DIR)
        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        self.dir = fileOpenDialog.GetDirectory()
        self.GetParent().name = fileOpenDialog.GetFilename()
        self.GetParent().uploadSaveDir = self.dir

        # if self.GetParent().name == '':
        #     defaultName = ''
        #     if self.GetParent().manager is not None:
        #         date = datetime.datetime.strptime(str(self.GetParent().manager.genInfoManager.datePicker), self.GetParent().manager.DT_FORMAT)
        #         date = date.strftime("%Y%m%d")
        #         defaultName = str(self.GetParent().manager.genInfoManager.stnNumCmbo) + "_" + str(date) + "_FV.pdf"

        # else:
        #     defaultName = self.GetParent().name.split(".")[0] + ".pdf"


        # if path != "":
        #     path = path + '\\' + defaultName


        self.changeCtrl.SetValue(self.dir + "\\" + self.GetParent().name.replace("xml", "pdf"))

        self.layoutSizer.Layout()
        self.Update()
        self.Refresh()

    def OnDischargeCheckbox(self, event):
        self.includeDischarge = self.dischargeCkbox.IsChecked()

    def OnLevelNoteCheckbox(self, event):
        self.includeLevelNote = self.levelNoteCkbox.IsChecked()



    def EnableButtons(self, en):
        self.uploadButton.Enable(en)
        self.cancelButton.Enable(en)

    def UploadToAquarius(self, evt):
        try:
            self.EnableButtons(False)
            dlg = wx.MessageDialog(self, self.uploadConfirm, 'None', wx.YES_NO)
            res = dlg.ShowModal()
            if res == wx.ID_YES:
                # self.EndModal(wx.ID_YES)
                # self.Show(True)
                

                

                if self.GetParent().manager is not None:
                    server = self.GetServer()
                    username = self.usernameCtrl.GetValue()
                    password = self.passwordCtrl.GetValue()
                    fvDate = self.GetParent().manager.genInfoManager.datePicker
                    withDischarge = self.includeDischarge

                    withLevelNote = self.includeLevelNote


                    result = self.GetParent().manager.ExportToAquarius(server, username, password, fvDate, withDischarge, withLevelNote)
                    show_error = False
                    uploadInfo = []
                    if result is not None:
                        if "password" in result:
                            error = wx.MessageDialog(None, result, "Error",
                                                wx.OK | wx.ICON_EXCLAMATION)
                            re = error.ShowModal()
                            if re == wx.ID_OK:
                                self.EnableButtons(True)
                                # self.aquariusUploadDialog.Destroy()

                       
                                return

                        else:
                            print "Error: %s" % result
                            show_error = True
                            uploadInfo.append("Failed")
                            uploadInfo.append(str(datetime.datetime.now()))
                            uploadInfo.append(username)
                            # message = "Failed"
                            if self.GetParent().manager.uploadRecord is None:
                                self.GetParent().manager.uploadRecord = Element('AQ_Upload_Record')
                            self.GetParent().manager.UploadInfoAsXMLTree(self.GetParent().manager.uploadRecord, uploadInfo)

                            self.GetParent().SaveAsPDFAndXML4Upload(self.GetParent().uploadDir, False)
                            self.EnableButtons(True)

                            return

    #######################################################
                    

                    else:
                        self.GetParent().manager.ExportToAquariusSuccess()

                        self.EnableButtons(True)

                        self.GetParent().savedServer = self.serverCmbo.GetValue()
                        self.GetParent().savedName = username
                        self.GetParent().savedPassword = password
                        self.GetParent().ResetUploadSaveIni(self.changeCtrl.GetValue())
                        uploadInfo.append("Successful")
                        uploadInfo.append(str(datetime.datetime.now()))
                        uploadInfo.append(username)


                        if self.GetParent().manager.uploadRecord is None:
                            self.GetParent().manager.uploadRecord = Element('AQ_Upload_Record')
                        self.GetParent().manager.UploadInfoAsXMLTree(self.GetParent().manager.uploadRecord, uploadInfo)

                        self.GetParent().SaveAsPDFAndXML4Upload(self.GetParent().uploadSaveDir, True)
                        self.EndModal(wx.ID_CANCEL)

                        return

                #Re enable access to dialog
                self.EnableButtons(True)

                if show_error:
                    error = wx.MessageDialog(None, result, "Error",
                                                wx.OK | wx.ICON_EXCLAMATION)
                    error.ShowModal()
                    show_error = False
            else:

                dlg.Destroy()
                self.EnableButtons(True)


        except Exception as e:
            print str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.EnableButtons(True)



    def Cancel(self, evt):
        self.EndModal(wx.ID_CANCEL)

    # get currently selected server
    def GetServer(self):
        return self.servers[self.serverCmbo.GetValue()]


    def OnCheckBoxAutoOpen(self, evt):
        if self.autoOpenCkbox.IsChecked():
            self.GetParent().uploadOpenPdf = True
        else:
            self.GetParent().uploadOpenPdf = False





def main():
    app = wx.App()

    AUD = AquariusUploadDialog("DEBUG", None, None, title="Upload Field Visit to Aquarius")
    val = True
    while val:
        re = AUD.ShowModal()
        if re == wx.ID_YES:
            print "YES"
        else:
            print "Cancel"
            val = False
            AUD.Destroy()


    AUD.Destroy()

    app.MainLoop()

if __name__ == '__main__':
    main()
