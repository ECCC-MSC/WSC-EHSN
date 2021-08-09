# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class WaterTag(wx.Panel):
    def __init__(self, tag, siz, *args, **kwargs):
        super(WaterTag, self).__init__(*args, **kwargs)
        self.tag = tag
        self.size = siz
        self.InitUI()

    def InitUI(self):

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        self.noteHeader = wx.StaticText(self, label=self.tag, size= self.size, style=wx.ALIGN_CENTRE_HORIZONTAL)
        layoutSizer.Add(self.noteHeader, 1, wx.EXPAND)

        self.SetSizer(layoutSizer)


def main():
    app = wx.App()

    frame = wx.Frame(None)
    WaterTag("DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()