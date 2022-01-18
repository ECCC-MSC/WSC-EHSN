# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from WaterLevelNotesPanel import *

class AnnualLevellingPanel(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(AnnualLevellingPanel, self).__init__(*args, **kwargs)

        self.mode = mode
        self.manager = None
        
        self.InitUI()

    #Creates View
    def InitUI(self):
        if self.mode == "DEBUG":
            print("AnnualLevellingPanel")

        layoutSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.levelNotes = WaterLevelNotesPanel(self.mode, True, 40, self)

        layoutSizer.Add(self.levelNotes, 0, wx.EXPAND)
        self.SetSizer(layoutSizer)

        for row in range(1, len(self.levelNotes.levelNotesSizerV.GetChildren())):
            rowSizer = self.levelNotes.levelNotesSizerV.GetItem(row).GetSizer()
            physCtrl = rowSizer.GetItem(len(rowSizer.GetChildren()) - 2).GetWindow()
            commentsCtrl = rowSizer.GetItem(len(rowSizer.GetChildren()) - 1).GetWindow()

            # physCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnEnterSet)
            # commentsCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        

def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 700))
    AnnualLevellingPanel("DEBUG", frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
