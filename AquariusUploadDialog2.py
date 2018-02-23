import wx
import os

class AquariusUploadDialog2(wx.Dialog):
    def __init__(self, mode, dir, manager, *args, **kwargs):
        super(AquariusUploadDialog2, self).__init__(*args, **kwargs)
        self.manager = manager
        self.mode = mode
        self.dir = dir if dir is not None else str(os.getcwd())
        self.header = "Save and Upload"
        self.desc = "All eHSN files must be saved at the time of upload. Where would you like this file to be saved?"
        self.browseButtonDesc = "Browse"
        self.cancelButtonDesc = "Cancel"
        self.uploadSaveButtonDesc = "OK"
        self.browseTitleLbl = "Choose directory for xml and pdf file"


        self.SetSize((600, 230))

        self.InitUI()

    def InitUI(self):
        if self.mode == "DEBUG":
            print "Aquarius Upload Dialog 2"

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)

        headerTxt = wx.StaticText(self, label=self.header)
        font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        headerTxt.SetFont(font)


        descTxt = wx.StaticText(self, label=self.desc)
        font2 = wx.Font(13, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        descTxt.SetFont(font2)


        browsePanel = wx.Panel(self, style=wx.BORDER_NONE)
        browseSizer = wx.BoxSizer(wx.HORIZONTAL)
        browsePanel.SetSizer(browseSizer)
        self.browseCtrl = wx.TextCtrl(browsePanel, style=wx.TE_READONLY)
        self.browseCtrl.SetValue(self.dir)
        browseBtn = wx.Button(browsePanel, label=self.browseButtonDesc)
        browseBtn.Bind(wx.EVT_BUTTON, self.OnBrowse)
        browseSizer.Add(self.browseCtrl, 2, wx.EXPAND)
        browseSizer.Add(browseBtn, 1, wx.EXPAND)

        uploadPanel = wx.Panel(self, style=wx.BORDER_NONE)
        uploadSizer = wx.BoxSizer(wx.HORIZONTAL)
        uploadPanel.SetSizer(uploadSizer)
        self.uploadBtn = wx.Button(uploadPanel, label=self.uploadSaveButtonDesc)
        cancelBtn = wx.Button(uploadPanel, label=self.cancelButtonDesc)
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        uploadSizer.Add(self.uploadBtn, 1, wx.EXPAND)
        uploadSizer.Add(cancelBtn, 1, wx.EXPAND)

        self.layoutSizer.Add(headerTxt, 0, wx.EXPAND)
        self.layoutSizer.Add((-1, -1), 1)
        self.layoutSizer.Add(descTxt, 1, wx.EXPAND)
        self.layoutSizer.Add((-1, -1), 1)
        self.layoutSizer.Add(browsePanel, 0, wx.EXPAND)
        self.layoutSizer.Add(uploadPanel, 0, wx.EXPAND)


        self.SetSizer(self.layoutSizer)
        if self.manager is not None:
            self.uploadBtn.Bind(wx.EVT_BUTTON, self.manager.OnChoosePress)



    def OnCancel(self, event):
        self.Destroy()

    def OnBrowse(self, e):
        fileOpenDialog = wx.DirDialog(self, self.browseTitleLbl, self.dir)
        if fileOpenDialog.ShowModal() == wx.ID_CANCEL:
            fileOpenDialog.Destroy()
            return

        self.dir = fileOpenDialog.GetPath()
        self.browseCtrl.SetValue(self.dir)

        self.layoutSizer.Layout()
        self.Update()
        self.Refresh()


    def GetPath(self):
        return self.dir

    def GetUploadBtn(self):
        return self.uploadBtn

def main():
    app = wx.App()

    AUD = AquariusUploadDialog2("DEBUG", None, None, None, title="Upload Field Visit to Aquarius")
    val = True
    while val:
        re = AUD.ShowModal()
        if re == wx.ID_YES:
            print "YES"
        else:
            print "Cancel"
            val = False
            AUD.Destroy()

    print "TEST"

    AUD.Destroy()

    app.MainLoop()

if __name__ == '__main__':
    main()
