# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx

class TransferDialog(wx.Dialog):
    def __init__(self, times, stations, elevations, estEles, closures, *args, **kwargs):
        super(TransferDialog, self).__init__(*args, **kwargs)
        self.headerCol1Lbl = "Station"
        self.headerCol2Lbl = "Difference between observed and established elevations (m)" 
        self.closureLbl = "Closure = "
        self.closureEmptyLbl = "Not Calculated"
        self.height = 22
        self.circuitHeaderLbl = "Circuit #: "
        self.buttonLbl = "OK"

        self.times = times
        self.stations = stations
        self.elevations = elevations
        self.estEles = estEles
        self.closures = closures
        self.InitUI()


    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        tableHeaderTxt = wx.StaticText(self, label="Elevation Transfer Confirmation", style=wx.ALIGN_CENTRE_HORIZONTAL)
        tableHeaderTxt.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        sizer.Add(tableHeaderTxt, 0, wx.EXPAND)

        # circuitTableSizer = wx.BoxSizer(wx.VERTICAL)




        for i in range(len(self.stations)):
            if len(self.stations[i]) > 0:
                circuitPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
                circuitSizer = wx.BoxSizer(wx.VERTICAL)
                circuitPanel.SetSizer(circuitSizer)

                circuitHeaderLbl = self.circuitHeaderLbl + str(i + 1)
                circuitHeaderTxt = wx.StaticText(circuitPanel, label=circuitHeaderLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
                circuitHeaderTxt.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                circuitSizer.Add(circuitHeaderTxt, 0, wx.EXPAND)

                tablePanel = wx.Panel(circuitPanel, style=wx.SIMPLE_BORDER)
                tableSizer = wx.BoxSizer(wx.HORIZONTAL)
                tablePanel.SetSizer(tableSizer)

                columnSizer1 = wx.BoxSizer(wx.VERTICAL)
                columnSizer2 = wx.BoxSizer(wx.VERTICAL)

                headerPanel1 = wx.Panel(tablePanel, style=wx.SIMPLE_BORDER, size=(150, self.height * 2))
                headerSizer1 = wx.BoxSizer(wx.VERTICAL)
                headerPanel1.SetSizer(headerSizer1)

                headerPanel2 = wx.Panel(tablePanel, style=wx.SIMPLE_BORDER, size=(300, self.height * 2))
                headerSizer2 = wx.BoxSizer(wx.VERTICAL)
                headerPanel2.SetSizer(headerSizer2)
                stationTxt = wx.StaticText(headerPanel1, label=self.headerCol1Lbl, size=(150, self.height))
                stationTxt.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                differenceTxt = wx.StaticText(headerPanel2, label=self.headerCol2Lbl, size=(300, self.height))
                differenceTxt.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                headerSizer1.Add(stationTxt, 1, wx.EXPAND)
                headerSizer2.Add(differenceTxt, 1, wx.EXPAND)

                columnSizer1.Add(headerPanel1, 0, wx.EXPAND)
                columnSizer2.Add(headerPanel2, 0, wx.EXPAND)

                tableSizer.Add(columnSizer1, 1, wx.EXPAND)
                tableSizer.Add(columnSizer2, 2, wx.EXPAND)

                for j in range(len(self.stations[i])):

                    #Adding first column
                    firstPanel = wx.Panel(tablePanel, style=wx.SIMPLE_BORDER, size=(-1, self.height))
                    firstSizer = wx.BoxSizer(wx.HORIZONTAL)
                    firstPanel.SetSizer(firstSizer)

                    stationTxt = wx.StaticText(firstPanel, label=self.stations[i][j], size=(-1, self.height))
                    firstSizer.Add(stationTxt, 1, wx.EXPAND)

                    #Adding second column
                    secondPanel = wx.Panel(tablePanel, style=wx.SIMPLE_BORDER, size=(-1, self.height))
                    secondSizer = wx.BoxSizer(wx.HORIZONTAL)
                    secondPanel.SetSizer(secondSizer)

                    result = ""
                    if self.elevations[i][j] != "" and self.estEles[i][j] != "":
                        try:
                            result = str(float(self.elevations[i][j]) - float(self.estEles[i][j]))
                        except:
                            result = ""
                    stationTxt = wx.StaticText(secondPanel, label=result, size=(-1, self.height))
                    secondSizer.Add(stationTxt, 1, wx.EXPAND)

                    columnSizer1.Add(firstPanel, 1, wx.EXPAND)
                    columnSizer2.Add(secondPanel, 1, wx.EXPAND)


                circuitSizer.Add(tablePanel, 0, wx.EXPAND)

                closurePanel = wx.Panel(circuitPanel)
                closureSizer = wx.BoxSizer(wx.HORIZONTAL)
                closurePanel.SetSizer(closureSizer)
                closureTxt = wx.StaticText(closurePanel, label=self.closureLbl)
                closureTxt.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                closureVal  = self.closures[i] if self.closures[i] != "" else "Not Calculated"
                closureValTxt = wx.StaticText(closurePanel, label=closureVal)
                closureValTxt.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                closureUnitTxt = wx.StaticText(closurePanel, label="   m")
                closureUnitTxt.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                if self.closures[i] == "":
                    closureUnitTxt.Hide()
                closureSizer.Add(closureTxt, 0, wx.EXPAND)
                closureSizer.Add(closureValTxt, 0, wx.EXPAND)
                closureSizer.Add(closureUnitTxt, 0, wx.EXPAND)

                circuitSizer.Add(closurePanel, 0, wx.EXPAND)

                sizer.Add(circuitPanel, 0, wx.EXPAND)

        button = wx.Button(self, label=self.buttonLbl)
        button.Bind(wx.EVT_BUTTON, self.OnOK)
        sizer.Add(button, 0, wx.EXPAND)

    def OnOK(self, event):
        self.Destroy()


