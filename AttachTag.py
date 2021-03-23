# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class AttachTag(wx.Panel):
    def __init__(self, tag, subtag, *args, **kwargs):
        super(AttachTag, self).__init__(*args, **kwargs)
        self.tag = tag
        self.sub = subtag
        self.InitUI()

    def InitUI(self):

        layoutSizer = wx.BoxSizer(wx.VERTICAL)

        self.noteHeader = wx.StaticText(self, label=self.tag)
        self.subTag = wx.StaticText(self, label=self.sub)
        layoutSizer.Add(self.noteHeader)
        layoutSizer.Add(self.subTag)
        self.SetSizer(layoutSizer)


def main():
    app = wx.App()

    frame = wx.Frame(None)
    AttachTag("DEBUG", frame)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()