from MidSectionHeader import *
from MidSectionSummaryTable import *


class MidSectionMeasurementsPanel(wx.Panel):

    def __init__(self, mode, lang, *args, **kwargs):
        super(MidSectionMeasurementsPanel, self).__init__(*args, **kwargs)
        self.mode = mode
        self.lang = lang
        # self.manager = manager

        self.InitUI()

    def InitUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(layout)

        self.header = MidSectionHeader(self)
        self.table = MidSectionSummaryTable(self)


        layout.Add(self.header, 1, wx.EXPAND)
        layout.Add(self.table, 4, wx.EXPAND|wx.ALL)



    def UpdateSummary(self, values):
        self.header.UpdateSummary(values)

def main():
    app = wx.App()

    frame = wx.Frame(None, size=(940, 850))
    MidSectionMeasurementsPanel("debug", wx.LANGUAGE_FRENCH, frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
