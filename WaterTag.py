# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class WaterTag(wx.Panel):
    def __init__(self, tag, message, siz, *args, **kwargs):
        super(WaterTag, self).__init__(*args, **kwargs)
        self.tag = tag
        self.message = message
        self.size = siz
        self.InitUI()

    def InitUI(self):

        layoutSizer = wx.BoxSizer(wx.VERTICAL)
        
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.noteHeader = wx.StaticText(self, label=self.tag, size= self.size, style=wx.ALIGN_CENTRE_HORIZONTAL)
        headerSizer.Add(self.noteHeader, 1, wx.EXPAND)
        
        if self.message != "":
            messageButton = wx.Button(self, label="!", size=(14, 18))
            messageButton.SetForegroundColour(wx.RED)
            messageButton.Bind(wx.EVT_BUTTON, self.hint)
            headerSizer.Add(messageButton)
        
        layoutSizer.Add(headerSizer, 1, wx.EXPAND)

        self.SetSizer(layoutSizer)
        
    def hint(self, event):
        dlg = wx.MessageDialog(self, self.message, 'Hint', wx.OK)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
        return


def main():
    app = wx.App()

    frame = wx.Frame(None)
    WaterTag("DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()