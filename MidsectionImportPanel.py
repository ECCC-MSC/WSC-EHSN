import wx
from wx.lib.scrolledpanel import ScrolledPanel
# import matplotlib.backends.backend_wxagg
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.widgets import Cursor

from pdb import set_trace
# import wx.lib.plot as plt
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from wx.lib.scrolledpanel import ScrolledPanel

class MidsectionImportPanel(ScrolledPanel):
    def __init__(self, *args, **kwargs):
        super(MidsectionImportPanel, self).__init__(*args, **kwargs)
        self.headerLbl = "Header"
        self.testLbl1 = "test label1"
        self.testLbl2 = "test label2"
        self.testLbl3 = "test label3"
        self.testLbl4 = "test label4"
        self.tipLbl = "velocity:       111 m\narea:        222 m^2\nsomething:   1234 u"
        self.tipLbl2 = "velocity:       999 m\narea:        888 m^2\nsomething:   7777 u"
        self.tooltipTxt = """
Vertical:               {}
---------------------------------------------
Velocity:              {}m/s
Area:                   {} m^2
Discharge:           {} m^3/s
Discharge(q/Q):   {}%
"""
        self.canvasSize = (200, 500)

        self.InitUI()


    def InitUI(self):
        self.SetupScrolling()
        self.fig = None
        self.ax2 = None
        self.tags = None
        self.depths = None
        self.tagmarkLineList = None
        self.depthTagList = None
        self.depthList = None
        self.iceTagList = None
        self.bottomIceList = None
        self.slushTagList = None
        self.bottomSlushList = None

        self.midsectionPanelSizerV = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.midsectionPanelSizerV)
        #table
        # self.panelSizerH = wx.BoxSizer(wx.HORIZONTAL)
        # tableSizerV = wx.BoxSizer(wx.VERTICAL)

        # self.table = ScrolledPanel(self, size=(self.width, 140))
        # self.table.SetSizer(tableSizerV)
        # self.table.SetupScrolling(False, True)

        # self.panelSizerH.Add((40, -1), 0, wx.EXPAND)
        # self.panelSizerH.Add(self.table, 0, wx.EXPAND)
        # self.panelSizerH.Add((10, -1), 0, wx.EXPAND)

        # self.headerPanel = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.headerPanel.SetBackgroundColour('Grey')
        # self.panel1 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel2 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel3 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel4 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel5 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel6 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel7 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel8 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel9 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)
        # self.panel10 = wx.Panel(self.table, style=wx.SIMPLE_BORDER)

        # self.background_colour = self.panel1.GetBackgroundColour()

        # sizerH0 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH1 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH2 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH3 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH4 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH5 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH6 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH7 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH8 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH9 = wx.BoxSizer(wx.HORIZONTAL)
        # sizerH10 = wx.BoxSizer(wx.HORIZONTAL)

        # self.headerPanel.SetSizer(sizerH0)
        # self.panel1.SetSizer(sizerH1)
        # self.panel2.SetSizer(sizerH2)
        # self.panel3.SetSizer(sizerH3)
        # self.panel4.SetSizer(sizerH4)
        # self.panel5.SetSizer(sizerH5)
        # self.panel6.SetSizer(sizerH6)
        # self.panel7.SetSizer(sizerH7)
        # self.panel8.SetSizer(sizerH8)
        # self.panel9.SetSizer(sizerH9)
        # self.panel10.SetSizer(sizerH10)
        
        # self.testTxt0_1 = wx.StaticText(self.headerPanel, 1, label=self.headerLbl)
        # self.testTxt0_2 = wx.StaticText(self.headerPanel, 1, label=self.headerLbl)
        # self.testTxt0_3 = wx.StaticText(self.headerPanel, 1, label=self.headerLbl)
        # self.testTxt0_4 = wx.StaticText(self.headerPanel, 1, label=self.headerLbl)

        # self.font1 = wx.Font(22, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        # self.font2 = wx.Font(48, wx.ROMAN, wx.NORMAL, wx.BOLD)

        # self.testTxt1_1 = wx.StaticText(self.panel1, 1, label=self.testLbl1)
        # self.testTxt1_2 = wx.StaticText(self.panel1, 1, label=self.testLbl1)
        # self.testTxt1_3 = wx.StaticText(self.panel1, 1, label=self.testLbl1)
        # self.testTxt1_4 = wx.StaticText(self.panel1, 1, label=self.testLbl1)

        # self.testTxt2_1 = wx.StaticText(self.panel2, 1, label=self.testLbl2)
        # self.testTxt2_2 = wx.StaticText(self.panel2, 1, label=self.testLbl2)
        # self.testTxt2_3 = wx.StaticText(self.panel2, 1, label=self.testLbl2)
        # self.testTxt2_4 = wx.StaticText(self.panel2, 1, label=self.testLbl2)

        # self.testTxt3_1 = wx.StaticText(self.panel3, 1, label=self.testLbl3)
        # self.testTxt3_2 = wx.StaticText(self.panel3, 1, label=self.testLbl3)
        # self.testTxt3_3 = wx.StaticText(self.panel3, 1, label=self.testLbl3)
        # self.testTxt3_4 = wx.StaticText(self.panel3, 1, label=self.testLbl3)

        # self.testTxt4_1 = wx.StaticText(self.panel4, 1, label=self.testLbl4)
        # self.testTxt4_2 = wx.StaticText(self.panel4, 1, label=self.testLbl4)
        # self.testTxt4_3 = wx.StaticText(self.panel4, 1, label=self.testLbl4)
        # self.testTxt4_4 = wx.StaticText(self.panel4, 1, label=self.testLbl4)
        

        # self.testTxt5_1 = wx.StaticText(self.panel5, 1, label=self.testLbl4)
        # self.testTxt5_2 = wx.StaticText(self.panel5, 1, label=self.testLbl4)
        # self.testTxt5_3 = wx.StaticText(self.panel5, 1, label=self.testLbl4)
        # self.testTxt5_4 = wx.StaticText(self.panel5, 1, label=self.testLbl4)

        
        # self.testTxt6_1 = wx.StaticText(self.panel6, 1, label=self.testLbl4)
        # self.testTxt6_2 = wx.StaticText(self.panel6, 1, label=self.testLbl4)
        # self.testTxt6_3 = wx.StaticText(self.panel6, 1, label=self.testLbl4)
        # self.testTxt6_4 = wx.StaticText(self.panel6, 1, label=self.testLbl4)


        # self.testTxt7_1 = wx.StaticText(self.panel7, 1, label=self.testLbl4)
        # self.testTxt7_2 = wx.StaticText(self.panel7, 1, label=self.testLbl4)
        # self.testTxt7_3 = wx.StaticText(self.panel7, 1, label=self.testLbl4)
        # self.testTxt7_4 = wx.StaticText(self.panel7, 1, label=self.testLbl4)


        # self.testTxt8_1 = wx.StaticText(self.panel8, 1, label=self.testLbl4)
        # self.testTxt8_2 = wx.StaticText(self.panel8, 1, label=self.testLbl4)
        # self.testTxt8_3 = wx.StaticText(self.panel8, 1, label=self.testLbl4)
        # self.testTxt8_4 = wx.StaticText(self.panel8, 1, label=self.testLbl4)


        # self.testTxt9_1 = wx.StaticText(self.panel9, 1, label=self.testLbl4)
        # self.testTxt9_2 = wx.StaticText(self.panel9, 1, label=self.testLbl4)
        # self.testTxt9_3 = wx.StaticText(self.panel9, 1, label=self.testLbl4)
        # self.testTxt9_4 = wx.StaticText(self.panel9, 1, label=self.testLbl4)


        # self.testTxt10_1 = wx.StaticText(self.panel10, 1, label=self.testLbl4)
        # self.testTxt10_2 = wx.StaticText(self.panel10, 1, label=self.testLbl4)
        # self.testTxt10_3 = wx.StaticText(self.panel10, 1, label=self.testLbl4)
        # self.testTxt10_4 = wx.StaticText(self.panel10, 1, label=self.testLbl4)


        # for index, row in enumerate(self.table.GetChildren()):
            # row_sizer = row.GetSizer()
            # for idx, widget in enumerate(row.GetChildren()):
                # if index == 0:
                    # widget.SetFont(self.font1)
                # else:
                    # widget.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
                    # widget.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)
                    # widget.SetToolTip(wx.ToolTip(self.tipLbl))
                # row_sizer.Add(widget, 1, wx.EXPAND)
            # tableSizerV.Add(row, 0, wx.EXPAND)



        #plot
        self.panel2SizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.canvasPanel = wx.Panel(self, style=wx.SIMPLE_BORDER, size=self.canvasSize)
        self.canvaSizerV = wx.BoxSizer(wx.VERTICAL)
        self.canvasPanel.SetSizer(self.canvaSizerV)

        midsecHeader = self.GetParent().header
        if midsecHeader != None:
            self.fig, \
            self.ax2, \
            self.tags, \
            self.depths, \
            self.tagmarkLineList, \
            self.depthTagList, \
            self.depthList, \
            self.iceTagList, \
            self.bottomIceList, \
            self.slushTagList, \
            self.bottomSlushList = midsecHeader.GeneratePlot()
            self.annot = self.ax2.annotate("", xy=(0, 0), xytext=(40, -45),textcoords="offset points", \
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="Fancy"))
            self.annot.set_visible(False)

            self.canvas = FigureCanvas(self.canvasPanel, -1, self.fig)
            self.fig.canvas.mpl_connect('button_press_event', self.onMouseClickAx2)
            self.fig.canvas.mpl_connect('motion_notify_event', self.onMouseOverAx2)
            self.canvaSizerV.Add(self.canvas, 0, wx.EXPAND)

        # self.panel2SizerH.Add((20, -1), 0, wx.EXPAND)
        self.panel2SizerH.Add(self.canvasPanel, 1, wx.EXPAND|wx.LEFT, 20)



        # self.midsectionPanelSizerV.Add((-1, 20), 0, wx.EXPAND)
        # self.midsectionPanelSizerV.Add(self.panelSizerH, 0, wx.EXPAND)
        # self.midsectionPanelSizerV.Add((-1, 20), 0, wx.EXPAND)
        self.midsectionPanelSizerV.Add(self.panel2SizerH, 0, wx.EXPAND)


    def onMouseOverAx2(self, event):
        if event.inaxes == self.ax2:
            x, y = event.xdata, event.ydata
            midsecHeader = self.GetParent().header
            midsecHeader.fill_ax2_mouse_over(x, y, self.tags, self.depths, self.tagmarkLineList, self.depthTagList, self.depthList, 
                                            self.iceTagList, self.bottomIceList, self.slushTagList, self.bottomSlushList)

            sumTablePanel = self.GetParent().GetSumTablePanel()
            sumTable = sumTablePanel.GetSumTable()
            vertical = ""
            velocity = ""
            area = ""
            discharge = ""
            flow = ""
            tagmark = -1
            for i, tag in enumerate(self.tags[:-1]):
                if tag <= x < self.tags[i+1]:
                    if self.depths[i] == 0:
                        tagmark = tag
                        break
                    elif self.depths[i+1] == 0:
                        tagmark = self.tags[i+1]
                        break
                    else:
                        if tag in self.depthTagList:
                            tagmark = tag
                            break
                        else:
                            tagmark = self.tags[i+1]
                            break
            for i in range(sumTable.GetNumberRows()):
                tag = sumTable.GetCellValue(i, 1)
                try:
                    tag = float(tag)
                    if tagmark == tag:
                        vertical = sumTable.GetCellValue(i, 0)
                        velocity = sumTable.GetCellValue(i, 10)
                        area = sumTable.GetCellValue(i, 11)
                        discharge = sumTable.GetCellValue(i, 12)
                        flow = sumTable.GetCellValue(i, 13)
                        break
                except:
                    continue

            self.updateAnnot((x,y), self.tooltipTxt.format(vertical, velocity, area, discharge, flow))
            self.annot.set_visible(True)
            self.fig.canvas.draw_idle()
            self.Layout()
            self.Refresh()
        else:
            self.annot.set_visible(False)
            self.fig.canvas.draw_idle()

            
    def onMouseClickAx2(self, event):
        if event.inaxes == self.ax2:
            x, y = event.xdata, event.ydata
            #hightlight plot
            midsecHeader = self.GetParent().header
            midsecHeader.fill_ax2_click(x, y, self.tags, self.depths, self.tagmarkLineList, self.depthTagList, self.depthList,
                    self.iceTagList, self.bottomIceList, self.slushTagList, self.bottomSlushList)

            #highlight table
            sumTablePanel = self.GetParent().GetSumTablePanel()
            sumTable = sumTablePanel.GetSumTable()

            increasingPolority = sumTablePanel.increasingPolority
            for i in range(sumTable.GetNumberRows()):
                name = sumTable.GetCellValue(i, 0)
                try:
                    tag = float(sumTable.GetCellValue(i, 1))
                    width = float(sumTable.GetCellValue(i, 2))
                    if "Start E" in name or "End P" in name:
                        if ((increasingPolority and tag <= x < tag+width) or 
                            (not increasingPolority and tag >= x > tag-width)):
                            sumTable.SelectRow(i)
                            return

                    elif "End E" in name or "Start P" in name:
                        if ((increasingPolority and tag >= x > tag-width) or 
                            (not increasingPolority and tag <= x < tag+width)):
                                sumTable.SelectRow(i)
                                return

                    elif tag-width/2 <= x < tag+width/2: 
                        sumTable.SelectRow(i)
                        try:
                            float(sumTable.GetCellValue(i+1, 2))
                        except:
                            sumTable.SelectRow(i+1, addToSelected=True)
                            try:
                                float(sumTable.GetCellValue(i+2, 2))
                            except:
                                sumTable.SelectRow(i+2, addToSelected=True)
                except:
                    continue

            
            
    def updateAnnot(self, pos, text):
        x, y = pos
        self.annot.xy = (x-1, y)
        self.annot.set_text(text)


    def onMouseOver(self, event):
        obj = event.GetEventObject().GetParent()
        obj.SetBackgroundColour('Green')
        obj.Refresh()
        event.Skip()

    def onMouseLeave(self, event):
        obj = event.GetEventObject().GetParent()
        obj.SetBackgroundColour(self.background_colour)
        obj.Refresh()
        event.Skip()


    def onLeftUp(self, event):
        obj = event.GetEventObject()
        tooltip = obj.GetToolTip()
        tooltip.SetTip(self.tipLbl2)
        event.Skip()

    def onRightUp(self, event):
        obj = event.GetEventObject()
        tooltip = obj.GetToolTip()
        tooltip.SetTip(self.tipLbl)
        event.Skip()

    def onLeftDown(self, event):
        obj = event.GetEventObject()
        obj.SetForegroundColour('Blue')
        obj.Refresh()
        event.Skip()

    def onRightDown(self, event):
        obj = event.GetEventObject()
        obj.SetForegroundColour('Red')
        obj.SetFont(self.font2)
        obj.Refresh()
        event.Skip()


    def GetFig(self):
        return self.fig

    def GetAx2(self):
        return self.ax2

    def GetTags(self):
        return self.tags

    def GetDepths(self):
        return self.depths

    def GetTagmarkLineList(self):
        return self.tagmarkLineList

    def GetDepthTagList(self):
        return self.depthTagList

    def GetDepthList(self):
        return self.depthList

    def GetIceTagList(self):
        return self.iceTagList

    def GetBottomIceList(self):
        return self.bottomIceList

    def GetSlushTagList(self):
        return self.slushTagList

    def GetBottomSlushList(self):
        return self.bottomSlushList

def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 1200))
    midPanel = MidsectionImportPanel(frame)

    frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()

