# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
EHSN_VERSION = "v1.3.1"

class TitleHeaderPanel(wx.Panel):
    def __init__(self, mode, eHSN_Version, *args, **kwargs):
        super(TitleHeaderPanel, self).__init__(*args, **kwargs)

        self.titleLbl = "ELECTRONIC HYDROMETRIC SURVEY NOTES " + eHSN_Version
        self.enteredInHWSLbl = "Data Entered in HWS?"

        self.mode = mode
        self.manager = None

        self.InitUI()

    def InitUI(self):
        if self.mode == "DEBUG":
            print("Setup Title Header Panel")

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        self.noteHeader = wx.StaticText(self, label=self.titleLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        # print self.noteHeader.GetWindowStyleFlag()

        enteredSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.enteredInHWSCB = wx.CheckBox(self, label=self.enteredInHWSLbl)
        enteredSizer.Add((0, 0), 1, wx.EXPAND)
        enteredSizer.Add(self.enteredInHWSCB, 0, wx.EXPAND)

        layoutSizer.Add(self.noteHeader, 0, wx.EXPAND)
        layoutSizer.Add(enteredSizer, 0, wx.EXPAND)

        self.SetSizer(layoutSizer)


def main():
    app = wx.App()

    frame = wx.Frame(None)
    TitleHeaderPanel("DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
