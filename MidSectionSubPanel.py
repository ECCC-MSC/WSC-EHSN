import wx
from MidSectionEdgePanel import *
from MidSectionPanelPanel import *
from MidSectionPierPanel import *


class MidSectionSubPanel(wx.Panel):
    def __init__(self, panelNum, panelType=1, newPanel=True, panelId=-1, index=-1, modify=False, pos=None, *args, **kwargs):
        super(MidSectionSubPanel, self).__init__(*args, **kwargs)
        self.panelTypeLbl = ["Edge", "Panel"]#, "Pier/Island"]
        self.type = panelType
        self.panelNum = panelNum
        self.newPanel = newPanel
        self.panelId = panelId
        self.index = index
        self.pos = pos
        self.modify = modify
        self.InitUI()

    def InitUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(layout)

        panelTypeSizer = wx.BoxSizer(wx.HORIZONTAL)


        self.windowTypeBtn1 = wx.RadioButton(self, -1, self.panelTypeLbl[0], (10, 10), style = wx.RB_GROUP)
        self.windowTypeBtn2 = wx.RadioButton(self, -1, self.panelTypeLbl[1], (10, 10))
        # self.windowTypeBtn3 = wx.RadioButton(self, -1, self.panelTypeLbl[2], (10, 10))



        self.typeBtns = [self.windowTypeBtn1, self.windowTypeBtn2]#, self.windowTypeBtn3]

        panelTypeSizer.Add(self.windowTypeBtn1, 1)
        panelTypeSizer.Add(self.windowTypeBtn2, 1)
        # panelTypeSizer.Add(self.windowTypeBtn3, 1)

        self.edge = EdgePanel(parent=self, panelId=self.panelId, style=wx.BORDER_SIMPLE, size=(440, 580), index=self.index)
        self.edge.Hide()
        self.panel = MidSectionPanelPanel(panelNum=self.panelNum, parent=self, style=wx.BORDER_SIMPLE, size=(540, 660), \
            panelId=self.panelId, index=self.index, modify=self.modify)
        print self.pos
        #if self.pos is not None:
        #    self.Move(self.pos)
        #    self.edge.Move(self.pos)
        #    self.panel.Move(self.pos)

        # self.pier = MidSectionPierPanal(self, style=wx.BORDER_SIMPLE, size=(360, 260))
        # self.pier.Hide()

        self.subPanels = [self.edge, self.panel]#, self.pier]
        for btn in self.typeBtns:
            btn.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtn)







        layout.Add(panelTypeSizer, 0)
        layout.Add(self.edge, 1, wx.EXPAND)
        layout.Add(self.panel, 1, wx.EXPAND)
        # layout.Add(self.pier, 1, wx.EXPAND)

        self.typeBtns[self.type].SetValue(True)



    def OnRadioBtn(self, event):
        self.UpdateSubPanel()
        event.Skip()

    def UpdateSubPanel(self):
        for index, btn in enumerate(self.typeBtns):
            if btn.GetValue():
                for i in range(2):
                    if i != index:
                        self.subPanels[i].Hide()
                    else:
                        self.subPanels[i].Show()
                        if i == 0:
                            self.GetParent().SetSize((440, 300))
                            if self.pos is not None:
                                self.GetParent().Move(self.pos.x-4, self.pos.y-41)
                            self.subPanels[i].edgeTagmarkCtrl.SetFocus()
                        elif i == 1:
                            self.GetParent().SetSize((540, 660))
                            if self.pos is not None:
                                self.GetParent().Move(self.pos.x-4, self.pos.y-41)
                            self.subPanels[i].panelTagMarkCtrl.SetFocus()
                        # elif i == 2:
                        #     self.GetParent().SetSize((360, 260))
                break
        self.Layout()




def main():
    app = wx.App()

    frame = wx.Frame(None, size=(500, 600))
    MidSectionSubPanel(parent=frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
