# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
from MidSectionEdgePanel import *
from MidSectionPanelPanel import *
from MidSectionPierPanel import *
import wx.lib.scrolledpanel as scrolledpanel

# import pyHook
# import win32clipboard



# SCALING_SUB1 = wx.NewId()
# SCALING_SUB2 = wx.NewId()


class MidSectionSubPanel(scrolledpanel.ScrolledPanel):
    def __init__(self, panelNum, modify, pid, panelType=1, pos=None, nextTagMark="", *args, **kwargs):
        super(MidSectionSubPanel, self).__init__(*args, **kwargs)
        self.panelTypeLbl = ["Edge", "Panel", "Pier/Island"]
        self.type = panelType
        self.panelNum = panelNum
        # self.newPanel = newPanel
        self.pid = pid

        # self.ctrlKeyDownFlag = False


        self.pos = pos
        self.modify = modify
        self.nextTagMark = nextTagMark

        self.edgeSize = self.GetParent().GetParent().edgeSize
        self.panelSize = self.GetParent().GetParent().panelSize
        self.InitUI()
        self.SetupScrolling()

        fontSize = self.GetParent().GetParent().GetParent().header.measureSectionCtrl.GetFont().GetPointSize()
        self.ApplyFontToChildren(self, fontSize)

        self.InitData()


    def InitData(self):
        if self.windowTypeBtn1.GetValue():
            self.edge.InitData()
            self.edge.edgeTagmarkCtrl.SetFocus()
            self.edge.edgeTagmarkCtrl.SetSelection(-1,-1)
        elif self.windowTypeBtn3.GetValue():
            self.pier.InitData()
            self.pier.edgeTagmarkCtrl.SetFocus()
            self.pier.edgeTagmarkCtrl.SetSelection(-1,-1)
        else:
            self.panel.InitData()
            self.panel.panelTagMarkCtrl.SetFocus()
            self.panel.panelTagMarkCtrl.SetSelection(-1,-1)



        # hm = pyHook.HookManager()
        # hm.KeyDown = self.OnKeyDownEvent
        # hm.KeyUp = self.OnKeyUpEvent
        # hm.HookKeyboard()


    def InitUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(layout)

        panelTypeSizer = wx.BoxSizer(wx.HORIZONTAL)


        self.windowTypeBtn1 = wx.RadioButton(self, -1, self.panelTypeLbl[0], (10, 10), style = wx.RB_GROUP)
        self.windowTypeBtn2 = wx.RadioButton(self, -1, self.panelTypeLbl[1], (10, 10))
        self.windowTypeBtn3 = wx.RadioButton(self, -1, self.panelTypeLbl[2], (10, 10))

        if self.modify == 1:
            self.windowTypeBtn1.Enable(False)


        self.typeBtns = [self.windowTypeBtn1, self.windowTypeBtn2, self.windowTypeBtn3]

        panelTypeSizer.Add(self.windowTypeBtn1, 1)
        panelTypeSizer.Add(self.windowTypeBtn2, 1)
        panelTypeSizer.Add(self.windowTypeBtn3, 1)

        self.edge = EdgePanel(parent=self, modify=self.modify, style=wx.BORDER_NONE, size=self.edgeSize, nextTagMark=self.nextTagMark, pid=self.pid)
        # self.edge.Hide()
        self.pier = PierPanel(parent=self, modify=self.modify, style=wx.BORDER_NONE, size=self.edgeSize, nextTagMark=self.nextTagMark, pid=self.pid)
        # self.pier.Hide()
        self.panel = MidSectionPanelPanel(panelNum=self.panelNum, parent=self, style=wx.BORDER_NONE, size=self.panelSize, \
              modify=self.modify, nextTagMark=self.nextTagMark, pid=self.pid)
        
        #if self.pos is not None:
        #    self.Move(self.pos)
        #    self.edge.Move(self.pos)
        #    self.panel.Move(self.pos)

        # self.pier = MidSectionPierPanal(self, style=wx.BORDER_SIMPLE, size=(360, 260))
        # self.pier.Hide()

        self.subPanels = [self.edge, self.panel, self.pier]
        for btn in self.typeBtns:
            btn.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtn)


        layout.Add(panelTypeSizer, 0)
        layout.Add(self.edge, 0, wx.EXPAND)
        layout.Add(self.panel, 0, wx.EXPAND)
        layout.Add(self.pier, 0, wx.EXPAND)

        self.typeBtns[self.type].SetValue(True)

        self.UpdateSubPanel()



    def OnRadioBtn(self, event):
        self.UpdateSubPanel()
        self.InitData()
        event.Skip()

    def UpdateSubPanel(self):

        if self.windowTypeBtn1.GetValue() and self.edge.endEdgeRdBtn.GetValue():
            self.edge.saveNextBtn.Hide()
        for index, btn in enumerate(self.typeBtns):

            if btn.GetValue():
                self.type = index
                hideIndex1 = (index+1) % 3
                hideIndex2 = (index+2) % 3

                self.subPanels[index].Show()
                self.subPanels[hideIndex1].Hide()
                self.subPanels[hideIndex2].Hide()


                if index == 0 or index == 2:
                    self.GetParent().SetSize(self.edgeSize)
                    # self.subPanels[index].edgeTagmarkCtrl.SetFocus()
                    if index == 2: 

                        if self.pier.startEdgeRdBtn.GetValue(): 

                            if self.modify == 0 or self.modify == 1:
                                self.pier.saveBtn.Hide()
                                self.pier.saveNextBtn.Show()

                            else:
                                self.pier.saveBtn.Show()
                                self.pier.saveNextBtn.Hide()

                        else:
                            self.pier.saveBtn.Show()
                            if self.modify == 0:
                                self.pier.saveNextBtn.Show()
                            else:
                                self.pier.saveNextBtn.Hide()
                             
                elif index == 1:
                    self.GetParent().SetSize(self.panelSize)
                    self.subPanels[index].panelTagMarkCtrl.SetFocus()


                if self.pos is not None:
                    self.GetParent().Move(self.pos.x-4, self.pos.y-41)
                break
        self.Layout()






    def ApplyFontToChildren(self, window, fontSize):
        if len(window.GetChildren()) > 0:
            for index, child in enumerate(window.GetChildren()):
                self.ApplyFontToChildren(child, fontSize)

        else:
            font = window.GetFont()
            size = font.GetPointSize()
            font.SetPointSize(fontSize)
            window.SetFont(font)
            if isinstance(window, wx.StaticText):
                window.GetParent().Layout()


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(500, 600))
    MidSectionSubPanel(parent=frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
