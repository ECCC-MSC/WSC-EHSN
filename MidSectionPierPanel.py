import wx
from DropdownTime import *

class MidSectionPierPanal(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(MidSectionPierPanal, self).__init__(*args, **kwargs)
        self.headerLbl = "Pier/Island Information"
        self.typeLbl = "Type:"
        self.MeasureTimeLbl = "Measurement Time:"
        self.distanceStartLbl = "Distance from Initial Point to Start of the Pier/Island (m):"
        self.distanceEndLbl = "Distance from Initial Point to End of the Pier/Island (m):"
        self.types = ["Pier", "Island"]
        self.backColour = "grey"
        self.fontColour = "blue"
        self.ctrlHeight = 22
        self.txtWidth = 180
        self.ctrlWidth = 120

        self.InitUI()

    def InitUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(layout)

        headerTxt = wx.StaticText(self, label=self.headerLbl, size=(-1, 40), style=wx.ALIGN_CENTRE_HORIZONTAL)
        headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        headerTxt.SetFont(headerFont)
        headerTxt.SetBackgroundColour(self.backColour)

        typeSizer = wx.BoxSizer(wx.HORIZONTAL)
        typeTxt = wx.StaticText(self, label=self.typeLbl, size=(self.txtWidth, self.ctrlHeight))
        self.typeCmbox = wx.ComboBox(self, choices=self.types, size=(self.ctrlWidth, self.ctrlHeight), style=wx.CB_READONLY)
        typeSizer.Add(typeTxt, 0, wx.ALL, 10)
        typeSizer.Add(self.typeCmbox, 0, wx.ALL, 10)




        timeSizer = wx.BoxSizer(wx.HORIZONTAL)
        measureTimeTxt = wx.StaticText(self, label=self.MeasureTimeLbl, size=(self.txtWidth, self.ctrlHeight))
        self.measureTimeCtrl = DropdownTime(False, parent=self, size=(self.ctrlWidth, self.ctrlHeight), style=wx.BORDER_NONE)
        self.measureTimeCtrl.UpdateTime(67)
        timeSizer.Add(measureTimeTxt, 0, wx.ALL, 10)
        timeSizer.Add(self.measureTimeCtrl, 0, wx.ALL|wx.EXPAND, 5)

        distanceStartSizer = wx.BoxSizer(wx.HORIZONTAL)
        distanceStartTxt = wx.StaticText(self, label=self.distanceStartLbl, size=(self.txtWidth, self.ctrlHeight + 20))
        self.distanceStartCtrl = wx.TextCtrl(self, size=(self.ctrlWidth, self.ctrlHeight))
        distanceStartSizer.Add(distanceStartTxt, 0, wx.LEFT|wx.RIGHT, 10)
        distanceStartSizer.Add(self.distanceStartCtrl, 0, wx.LEFT|wx.TOP, 10)


        distanceEndSizer = wx.BoxSizer(wx.HORIZONTAL)
        distanceEndTxt = wx.StaticText(self, label=self.distanceEndLbl, size=(self.txtWidth, self.ctrlHeight + 20))
        self.distanceEndCtrl = wx.TextCtrl(self, size=(self.ctrlWidth, self.ctrlHeight))
        distanceEndSizer.Add(distanceEndTxt, 0, wx.LEFT|wx.RIGHT, 10)
        distanceEndSizer.Add(self.distanceEndCtrl, 0, wx.LEFT|wx.TOP, 10)




        layout.Add(headerTxt, 0, wx.EXPAND)
        layout.Add(typeSizer, 0)
        layout.Add(timeSizer, 0)
        layout.Add(distanceStartSizer, 0)
        layout.Add(distanceEndSizer, 0)









def main():
    app = wx.App()

    frame = wx.Frame(None, size=(360, 260))
    MidSectionPierPanal(frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
