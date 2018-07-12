import wx

FONT_COLOR = "#186F24"

class ZoomPanel(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(ZoomPanel, self).__init__(*args, **kwargs)

        self.scalDownLbl = "Zoom:        4        -"
        self.scalUpLbl = "+  "
        self.mode = mode
        self.selection = 4



        self.InitUI()

    def InitUI(self):
        zoomSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(zoomSizer)

        self.scalDownTxt = wx.StaticText(self, label=self.scalDownLbl, size=(-1, -1))
        self.scalDownTxt.SetForegroundColour(FONT_COLOR)

        self.scrollBar = wx.ScrollBar(self, size=(200, -1), style=wx.SB_HORIZONTAL)
        self.scrollBar.SetScrollbar(4, 1, 9, 1, False)
        # self.scrollBar.Bind(wx.EVT_SCROLL_PAGEDOWN, self.OnScrollBar)
        self.scrollBar.Bind(wx.EVT_SCROLL_CHANGED, self.OnScrollBar)

        scalUpTxt = wx.StaticText(self, label=self.scalUpLbl, size=(-1, -1))
        scalUpTxt.SetForegroundColour(FONT_COLOR)
   
        # self.scrollBar.SetBackgroundColour("Grey")

        zoomSizer.Add((-1,-1),1, wx.EXPAND)
        zoomSizer.Add(self.scalDownTxt, 0, wx.EXPAND)
        zoomSizer.Add(self.scrollBar, 0, wx.EXPAND)
        zoomSizer.Add(scalUpTxt, 0, wx.EXPAND)

    def OnScrollBar(self, evt):
        label = self.scalDownTxt.GetLabelText().split("        ")
        label[1] = str(evt.GetSelection())
        newLabel = ""
        for index, i in enumerate(label):
            newLabel += i + "        " if i != label[-1] else i

        self.scalDownTxt.SetLabelText(newLabel)
        # label = str((100 + 100 * evt.GetPosition())) + '%'
        # self.scalTxt.SetLabelText(label)
        self.GetParent().ApplyFontToChildren(self.GetParent().layout, evt.GetSelection() - self.selection)
        self.GetParent().ChangeFontToMidsectionGrid(evt.GetSelection() - self.selection)

        self.selection = evt.GetSelection()
        evt.Skip()


