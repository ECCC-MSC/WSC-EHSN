# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class PartyInfoPanel(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(PartyInfoPanel, self).__init__(*args, **kwargs)

        self.partyLbl = "Party:"
        self.completeLbl = "Completed by:"
        self.checkLbl=  "Checked by:"
        self.reviewedLbl = "Reviewed"

        self.mode=mode
        self.manager = None
        
        self.InitUI()

    def InitUI(self):
        if self.mode=="DEBUG":
            print("Party Info Panel")

        layoutSizer = wx.BoxSizer(wx.HORIZONTAL)

        partySizer = wx.BoxSizer(wx.HORIZONTAL)
        partyTxt = wx.StaticText(self, label=self.partyLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.partyCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        partySizer.Add(partyTxt, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 8)
        partySizer.Add(self.partyCtrl, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)

        completeSizer = wx.BoxSizer(wx.HORIZONTAL)
        completeTxt = wx.StaticText(self, label=self.completeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.completeCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        completeSizer.Add(completeTxt, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 8)
        completeSizer.Add(self.completeCtrl, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)

        checkSizer = wx.BoxSizer(wx.HORIZONTAL)
        checkTxt = wx.StaticText(self, label=self.checkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.checkCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        checkSizer.Add(checkTxt, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 8)
        checkSizer.Add(self.checkCtrl, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        for i in range(len(checkSizer.GetChildren())):
            checkSizer.Hide(i)
            
        # Reviewed Checkbox
        reviewedSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reviewedCB = wx.CheckBox(self, label=self.reviewedLbl, style=wx.ALIGN_RIGHT)
        reviewedSizer.Add((-1, -1), 1, wx.EXPAND)
        reviewedSizer.Add(self.reviewedCB, 0, wx.EXPAND)
        reviewedSizer.Add((-1, -1), 1, wx.EXPAND)
        
        controlRemarksSizer = wx.BoxSizer(wx.VERTICAL)
        
        layoutSizer.Add(partySizer, 3, wx.EXPAND)
        layoutSizer.Add(completeSizer, 2, wx.EXPAND)
        layoutSizer.Add(checkSizer, 2, wx.EXPAND)
        layoutSizer.Add(reviewedSizer, 1, wx.EXPAND|wx.ALL|wx.CENTER, 5)

        self.SetSizer(layoutSizer)
        
        
    def ReviewedIsChecked(self):
        return self.reviewedCB.IsChecked()


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 70))
    PartyInfoPanel("DEBUG", frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
