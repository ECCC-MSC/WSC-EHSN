# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import NumberControl
from DropdownTime import *
from MidSectionSubPanelObj import *

#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

class EdgePanel(wx.Panel):
    def __init__(self, panelId, index, *args, **kwargs):
        super(EdgePanel, self).__init__(*args, **kwargs)
        self.panelId = panelId
        self.index = index
        self.titleLbl = "Edge Information"
        self.panelLbl = "Panel #:"
        self.measurementTimeLbl = "Measurement Time:"
        self.panelConditionLbl = "Panel Condition:"
        self.riverBankLbl = "River Bank:"
        self.channelEdgeLbl = "Channel Edge:"
        self.depthEdgeLbl = "Depth at Edge (m):"
        self.adjacentLbl = "Same as Adjacent"
        self.estimatedVelLbl = "Vel. at Edge (m/s):"
        self.edgeWidthLbl = "Edge Width:"
        self.edgeAreaLbl = "Edge Area:"
        self.qEdgeLbl = "Q at Edge:"
        self.edgeTypeLbl = "Edge Type"
        self.edgeTagmarkLbl = "Tagmark at Edge (m)"

        self.saveBtnLbl = "Save && Exit"
        self.cancelBtnLbl = "Cancel"
        self.nextBtnLbl = "Next"

        self.mandatoryFieldsMsg = "You are missing the field: "

        self.types = ["Edge @ Bank", "Pier/Island"]
        self.locations = ["Start", "End"]
        self.leftRight = ["","Left Bank", "Right Bank"]

        self.conditions = ["Open", "Ice"]
        self.edges = ["Triangle", "Straight", "Other"]
        self.height = 24
        self.lblWidth = 162


        self.InitUI()

    def InitUI(self):
        sizerV = wx.BoxSizer(wx.VERTICAL)
        headerTxt = wx.StaticText(self, label=self.titleLbl, size=(self.lblWidth, self.height), style=wx.ALIGN_CENTRE_HORIZONTAL)
        headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        headerTxt.SetFont(headerFont)
        headerTxt.SetBackgroundColour('grey')


        #Measurement Time
        measurementTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        measurementTimeTxt = wx.StaticText(self, label=self.measurementTimeLbl, size=(self.lblWidth, self.height))
        self.measurementTimeCtrl = DropdownTime(False, parent=self, size=(110, self.height + 9), style=wx.BORDER_NONE)
        self.measurementTimeCtrl.UpdateTime(67)
        measurementTimeSizer.Add(measurementTimeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        measurementTimeSizer.Add(self.measurementTimeCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        #Edge Type
        edgeTypeSizer = wx.BoxSizer(wx.HORIZONTAL)
        edgeTypeTxt = wx.StaticText(self, label=self.edgeTypeLbl, size=(self.lblWidth, self.height))
        self.panelNumberCtrl = wx.ComboBox(self, size=(-1, self.height), choices=self.types, style=wx.CB_READONLY)
        edgeTypeSizer.Add(edgeTypeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        edgeTypeSizer.Add(self.panelNumberCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Location Radio buttons
        locationSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.startEdgeRdBtn = wx.RadioButton(self, label=self.locations[0], style=wx.RB_GROUP)
        self.endEdgeRdBtn = wx.RadioButton(self, label=self.locations[1])
        locationSizer.Add(self.startEdgeRdBtn, 0, wx.LEFT, 170)
        locationSizer.Add(self.endEdgeRdBtn, 0, wx.LEFT|wx.RIGHT, 20)

        #River Bank
        riverBankSizer = wx.BoxSizer(wx.HORIZONTAL)
        riverBankTxt = wx.StaticText(self, label=self.riverBankLbl, size=(self.lblWidth, self.height))
        self.riverBankCtrl = wx.ComboBox(self, size=(-1, self.height), choices=self.leftRight, style=wx.CB_READONLY)
        riverBankSizer.Add(riverBankTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        riverBankSizer.Add(self.riverBankCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Tagmark at edge (m)
        edgeTagmarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        edgeTagmarkTxt = wx.StaticText(self, label=self.edgeTagmarkLbl, size=(self.lblWidth, self.height))
        self.edgeTagmarkCtrl = MyTextCtrl(self, size=(-1, self.height))
        self.edgeTagmarkCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.edgeTagmarkCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.edgeTagmarkCtrl.SetFocus()
        edgeTagmarkSizer.Add(edgeTagmarkTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        edgeTagmarkSizer.Add(self.edgeTagmarkCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        #Depth at Edge
        depthSizer = wx.BoxSizer(wx.HORIZONTAL)
        depthTxt = wx.StaticText(self, label=self.depthEdgeLbl, size=(self.lblWidth, self.height))
        self.depthCtrl = MyTextCtrl(self, size=(-1, self.height))
        self.depthCtrl.SetValue("0")
        self.depthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.depthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)
        self.depthAdjacentCkbox = wx.CheckBox(self, label=self.adjacentLbl)
        self.depthAdjacentCkbox.Bind(wx.EVT_CHECKBOX, self.OnDepthAdjacent)
        depthSizer.Add(depthTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        depthSizer.Add(self.depthCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        depthSizer.Add(self.depthAdjacentCkbox, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        #estimated vel. at edge
        estimatedVelSizer = wx.BoxSizer(wx.HORIZONTAL)
        estimatedVelTxt = wx.StaticText(self, label=self.estimatedVelLbl, size=(self.lblWidth, self.height))
        self.estimatedVelCtrl = MyTextCtrl(self, size=(-1, self.height))
        self.estimatedVelCtrl.SetValue("0")
        self.estimatedVelCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.estimatedVelCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Sig3)
        self.velAdjacentCkbox = wx.CheckBox(self, label=self.adjacentLbl)
        self.velAdjacentCkbox.Bind(wx.EVT_CHECKBOX, self.OnVelAdjacent)
        estimatedVelSizer.Add(estimatedVelTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        estimatedVelSizer.Add(self.estimatedVelCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        estimatedVelSizer.Add(self.velAdjacentCkbox, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)



        #button panel
        buttonPanel = wx.Panel(self, style=wx.BORDER_NONE)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonPanel.SetSizer(buttonSizer)

        self.saveBtn = wx.Button(buttonPanel, label=self.saveBtnLbl, size=(100, 30))
        self.nextBtn = wx.Button(buttonPanel, label=self.nextBtnLbl, size=(50, 30))
        self.cancelBtn = wx.Button(buttonPanel, label=self.cancelBtnLbl, size=(50, 30))

        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.nextBtn.Bind(wx.EVT_BUTTON, self.OnNext)

        buttonSizer.Add(self.cancelBtn, 0, wx.LEFT, 250)
        buttonSizer.Add(self.nextBtn, 0, wx.LEFT, 5)
        buttonSizer.Add(self.saveBtn, 0, wx.LEFT, 5)



        # panelNumberSizer = wx.BoxSizer(wx.HORIZONTAL)
        # panelNumberTxt = wx.StaticText(self, label=self.panelLbl, size=(self.lblWidth, self.height))
        # self.panelNumberCtrl = wx.ComboBox(self, size=(-1, self.height), choices=self.types, style=wx.CB_READONLY)
        # panelNumberSizer.Add(panelNumberTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        # panelNumberSizer.Add(self.panelNumberCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        # panelConditionSizer = wx.BoxSizer(wx.HORIZONTAL)
        # panelConditionTxt = wx.StaticText(self, label=self.panelConditionLbl, size=(self.lblWidth, self.height))
        # # self.measurementTimeCtrl = wx.TextCtrl(self, size=(-1, self.height))
        # self.measurementTimeCtrl = wx.ComboBox(self, size=(-1, self.height), choices=self.conditions, style=wx.CB_READONLY)
        # panelConditionSizer.Add(panelConditionTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        # panelConditionSizer.Add(self.measurementTimeCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        # channelSizer = wx.BoxSizer(wx.HORIZONTAL)
        # channelTxt = wx.StaticText(self, label=self.channelEdgeLbl, size=(self.lblWidth, self.height))
        # # self.channelCtrl = wx.TextCtrl(self, size=(-1, self.height))
        # self.channelCtrl = wx.ComboBox(self, size=(-1, self.height), choices=self.edges, style=wx.CB_READONLY)
        # channelSizer.Add(channelTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        # channelSizer.Add(self.channelCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        # edgeWidthSizer = wx.BoxSizer(wx.HORIZONTAL)
        # edgeWidthTxt = wx.StaticText(self, label=self.edgeWidthLbl, size=(self.lblWidth, self.height))
        # self.edgeWidthCtrl = wx.TextCtrl(self, size=(-1, self.height))
        # edgeWidthSizer.Add(edgeWidthTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        # edgeWidthSizer.Add(self.edgeWidthCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        # edgeAreaSizer = wx.BoxSizer(wx.HORIZONTAL)
        # edgeAreaTxt = wx.StaticText(self, label=self.edgeAreaLbl, size=(self.lblWidth, self.height))
        # self.edgeAreaCtrl = wx.TextCtrl(self, size=(-1, self.height))
        # edgeAreaSizer.Add(edgeAreaTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        # edgeAreaSizer.Add(self.edgeAreaCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        # qEdgeSizer = wx.BoxSizer(wx.HORIZONTAL)
        # qEdgeTxt = wx.StaticText(self, label=self.qEdgeLbl, size=(self.lblWidth, self.height))
        # self.qEdgeCtrl = wx.TextCtrl(self, size=(-1, self.height))
        # qEdgeSizer.Add(qEdgeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        # qEdgeSizer.Add(self.qEdgeCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)







        sizerV.Add(headerTxt, 0, wx.EXPAND)
        sizerV.Add(measurementTimeSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(edgeTypeSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(locationSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(riverBankSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(edgeTagmarkSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(depthSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(estimatedVelSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizerV.Add(buttonPanel, 0, wx.TOP|wx.EXPAND, 5)


        self.SetSizerAndFit(sizerV)
        #self.SetSize(100, 80)


    def OnSave(self, event):
        self.SaveToObj()
        event.Skip()

        # summaryTable = self.GetParent().GetParent().GetParent().summaryTable

    def SaveToObj(self):
        table = self.GetParent().GetParent().GetParent()

        dist = self.edgeTagmarkCtrl.GetValue()
        measurementTime = self.measurementTimeCtrl.GetValue()
        startOrEndVal = self.startEdgeRdBtn.GetValue()
        depthEdge = self.depthCtrl.GetValue()
        edgeType = self.panelNumberCtrl.GetValue()
        velEdge = self.estimatedVelCtrl.GetValue()
        depthAdjacentCkbox = self.depthAdjacentCkbox.GetValue()
        velocityAdjacentCkbox = self.velAdjacentCkbox.GetValue()

        # MANDATORY FIELDS FOR EDGE
        if edgeType=='':
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[Edge Type]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1
        if dist=='':
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[Tagmark at Edge]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1
        if depthEdge=='' and not depthAdjacentCkbox:
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[Depth at Edge]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1
        if velEdge=='' and not velocityAdjacentCkbox:
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[Vel. At Edge]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1
        if self.riverBankCtrl.GetValue()=="" and self.riverBankCtrl.IsEnabled():
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[River Bank]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1

        if len(table.panelObjs) > 0:
            for i in range(len(table.panelObjs)):
                if float(table.panelObjs[i].distance) == float(dist):
                    if self.panelId == -1:
                        dlg = wx.MessageDialog(None, "Panel tagmark value already exists", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                        dlg.ShowModal()
                        return -1
                    else:
                        if float(dist) != float(table.originalTagmark):
                            dlg = wx.MessageDialog(None, "Panel tagmark value already exists", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                            dlg.ShowModal()
                            return -1
                try:
                    if isinstance(table.panelObjs[i].panelNum, str) and isinstance(table.panelObjs[i+1].panelNum, str):
                        if "start p" in table.panelObjs[i].panelNum.lower() and "end p" in table.panelObjs[i+1].panelNum.lower():
                            if float(table.panelObjs[i].distance) < float(dist) < float(table.panelObjs[i+1].distance) or float(table.panelObjs[i].distance) > float(dist) > float(table.panelObjs[i+1].distance):
                                dlg = wx.MessageDialog(None, "Panel tagmark value is within the range of P/ISL", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return -1
                except:
                    pass

        if startOrEndVal:
            if "Edge" in edgeType:
                panelNum = "Start Edge"
            else:
                panelNum = "Start P / ISL"
        else:
            if "Edge" in edgeType:
                panelNum = "End Edge"
            else:
                panelNum = "End P / ISL"


        obj = EdgeObj(edgeType=edgeType, time=measurementTime, distance=dist, startOrEnd=startOrEndVal, panelNum=panelNum,\
            depth=depthEdge, corrMeanVelocity=velEdge, depthAdjacent=depthAdjacentCkbox, velocityAdjacent=velocityAdjacentCkbox,\
                     panelId=self.panelId, index=self.index, leftOrRight=self.riverBankCtrl.GetValue())

        print "***panelId***", obj.panelId
        if obj.panelId == -1:
            table.AddRow(obj, self.GetScreenPosition())
        else:
            table.UpdateRow(obj, self.GetScreenPosition())
        self.GetParent().GetParent().Close()

    def OnDepthAdjacent(self, event):
        if self.depthCtrl.IsEnabled():
            self.depthCtrl.Clear()
            self.depthCtrl.Disable()
        else:
            self.depthCtrl.Enable()

    def OnVelAdjacent(self, event):
        if self.estimatedVelCtrl.IsEnabled():
            self.estimatedVelCtrl.Clear()
            self.estimatedVelCtrl.Disable()
        else:
            self.estimatedVelCtrl.Enable()

    def OnNext(self, event):
        failed = self.SaveToObj()
        if not failed==-1:
            self.GetParent().GetParent().GetParent().Adding()

    def OnCancel(self, event):
        self.GetParent().GetParent().Close()
        event.Skip()



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(440, 580))
    EdgePanel(frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
