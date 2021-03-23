# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class AttachmentTitle(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(AttachmentTitle, self).__init__(*args, **kwargs)

        self.titleLbl = "Attachment Zipper"
        self.titleSize = 12
        self.mode = mode
        self.manager = None

        self.InitUI()

    def InitUI(self):

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        self.noteHeader = wx.StaticText(self, label=self.titleLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        font = wx.Font(self.titleSize, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        self.noteHeader.SetFont(font)
        # print self.noteHeader.GetWindowStyleFlag()


        layoutSizer.Add(self.noteHeader, 0, wx.EXPAND)
        self.SetSizer(layoutSizer)


def main():
    app = wx.App()

    frame = wx.Frame(None)
    AttachmentTitle("DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()