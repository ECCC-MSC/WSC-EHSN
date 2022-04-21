# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html
# Get the GUI stuff
import wx
import sys

# We're going to be handling files and directories
import os

class ConfigPanel(wx.Frame):



    def __init__(self,parent,title):

        self.titleLbl = 'Station Information, Meters and Benchmark/Reference Files'

        lbl1 = 'Station information (Station ID, Name, Time Zone)'
        lbl2 = 'Meter information (Serial #, Instrument Type, Manufacturer, Model, Frequency)'
        lbl3 = 'Benchmark/reference information (Station ID, Reference, Elevation, Desc.)'

        desc1 = """These directories point to configuration files to allow you to view Station Information, Benchmarks and Field Equipment in drop-down menus.

Station Information and Benchmarks can be extracted and created using the AQUARIUS Data Extraction Tool (next menu over), but the meters.csv 
file will have to be set up by you or your office. The AQUARIUS Data Extraction Tool should be run for every new eHSN release, as well as periodically 
to ensure that all data is up-to-date; data should be extracted using the same version of eHSN that will be used to collect data.

It is recommended to store all configuration files in the default location (i.e. alongside the eHSN exe). """


        self.stationsDefaultPath = 'stations.txt'
        self.metersDefaultPath = 'meters.csv'
        self.levelsDefaultPath = 'levels.txt'

        self.iconName = "icon_transparent.ico"



        # based on a frame, so set up the frame
        wx.Frame.__init__(self,parent,wx.ID_ANY, title)



        #Main
        self.configPanel = wx.Panel(self, style = wx.BORDER_NONE)
        self.configSizerV = wx.BoxSizer(wx.VERTICAL)
        self.configPanel.SetSizer(self.configSizerV)

        #Title
        titlePanel = wx.Panel(self.configPanel, style=wx.SIMPLE_BORDER)
        titleSizer = wx.BoxSizer(wx.VERTICAL)
        titlePanel.SetSizer(titleSizer)
        titleText = wx.StaticText(titlePanel, label=self.titleLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        titleSizer.Add(titleText,0,wx.EXPAND)

        f = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        titleText.SetFont(f)

        descTxt = wx.StaticText(titlePanel, label=desc1, style=wx.ALIGN_LEFT)
        titleSizer.Add(descTxt, 0, wx.EXPAND)
        #Stations
        self.stationsPanel = wx.Panel(self.configPanel, style=wx.SIMPLE_BORDER)
        self.stationsSizerV = wx.BoxSizer(wx.VERTICAL)
        self.stationsPanel.SetSizer(self.stationsSizerV)

        self.stationsTitlePanel = wx.Panel(self.stationsPanel, style=wx.BORDER_NONE)
        self.stationsTitleSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.stationsTitlePanel.SetSizer(self.stationsTitleSizerH)


        self.stationsPathPanel = wx.Panel(self.stationsPanel, style=wx.BORDER_NONE)
        self.stationsPathSizerV = wx.BoxSizer(wx.VERTICAL)
        self.stationsPathPanel.SetSizer(self.stationsPathSizerV)



        self.stationsTitButPanel = wx.Panel(self.stationsTitlePanel, style=wx.BORDER_NONE)
        self.stationsTitButSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.stationsTitButPanel.SetSizer(self.stationsTitButSizerH)

        stationsDescText = wx.StaticText(self.stationsTitlePanel, label=lbl1)

        self.stationsButton = wx.Button(self.stationsTitButPanel, 100, "Browse")
        self.stationsResetButton = wx.Button(self.stationsTitButPanel, 101, "Reset to Default")
        self.stationsResetButton.Hide()
        # stationPad = wx.StaticText(self.stationsTitButPanel, size=(-1,-1))
        self.stationsPathText = wx.StaticText(self.stationsPathPanel, label=self.stationsDefaultPath)
        self.stationsPathText.SetForegroundColour("#5E9811")


 
        # self.stationsTitButSizerH.Add(self.stationsResetButton, 1, wx.EXPAND)
        # self.stationsTitButSizerH.Add(stationPad, 1, wx.EXPAND)
        self.stationsTitButSizerH.Add(self.stationsButton, 1, wx.EXPAND)
        
        
        self.stationsPathSizerV.Add(self.stationsPathText, 1, wx.EXPAND)

        self.stationsTitleSizerH.Add(stationsDescText, 4, wx.EXPAND)
        self.stationsTitleSizerH.Add(self.stationsTitButPanel, 1, wx.EXPAND)



        self.stationsSizerV.Add(self.stationsTitlePanel, 1, wx.EXPAND)
        self.stationsSizerV.Add(self.stationsPathPanel, 1, wx.EXPAND)

        #Meters
        self.metersPanel = wx.Panel(self.configPanel, style=wx.SIMPLE_BORDER)
        self.metersSizerV = wx.BoxSizer(wx.VERTICAL)
        self.metersPanel.SetSizer(self.metersSizerV)

        self.metersTitlePanel = wx.Panel(self.metersPanel, style=wx.BORDER_NONE)
        self.metersTitleSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.metersTitlePanel.SetSizer(self.metersTitleSizerH)


        self.metersPathPanel = wx.Panel(self.metersPanel, style=wx.BORDER_NONE)
        self.metersPathSizerV = wx.BoxSizer(wx.VERTICAL)
        self.metersPathPanel.SetSizer(self.metersPathSizerV)

        self.metersTitDescPanel = wx.Panel(self.metersTitlePanel, style=wx.BORDER_NONE)
        self.metersTitDescSizerV = wx.BoxSizer(wx.VERTICAL)
        self.metersTitDescPanel.SetSizer(self.metersTitDescSizerV)


        self.metersTitButPanel = wx.Panel(self.metersTitlePanel, style=wx.BORDER_NONE)
        self.metersTitButSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.metersTitButPanel.SetSizer(self.metersTitButSizerH)

        metersDescText = wx.StaticText(self.metersTitDescPanel, label=lbl2)
        self.metersButton = wx.Button(self.metersTitButPanel, 102, "Browse")
        self.metersResetButton = wx.Button(self.metersTitButPanel, 103, "Reset to Default")
        # meterPad = wx.StaticText(self.metersTitButPanel, size=(-1,-1))
        self.metersResetButton.Hide()
        self.metersPathText = wx.StaticText(self.metersPathPanel, label=self.metersDefaultPath)
        self.metersPathText.SetForegroundColour("#5E9811")

        self.metersTitDescSizerV.Add(metersDescText, 1, wx.EXPAND)
        # self.metersTitButSizerH.Add(self.metersResetButton, 1, wx.EXPAND)
        # self.metersTitButSizerH.Add(meterPad, 1, wx.EXPAND)
        self.metersTitButSizerH.Add(self.metersButton, 1, wx.EXPAND)
        
        
        self.metersPathSizerV.Add(self.metersPathText, 1, wx.EXPAND)

        self.metersTitleSizerH.Add(self.metersTitDescPanel, 4, wx.EXPAND)
        self.metersTitleSizerH.Add(self.metersTitButPanel, 1, wx.EXPAND)



        self.metersSizerV.Add(self.metersTitlePanel, 1, wx.EXPAND)
        self.metersSizerV.Add(self.metersPathPanel, 1, wx.EXPAND)


        #Levels
        self.levelsPanel = wx.Panel(self.configPanel, style=wx.SIMPLE_BORDER)
        self.levelsSizerV = wx.BoxSizer(wx.VERTICAL)
        self.levelsPanel.SetSizer(self.levelsSizerV)

        self.levelsTitlePanel = wx.Panel(self.levelsPanel, style=wx.BORDER_NONE)
        self.levelsTitleSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.levelsTitlePanel.SetSizer(self.levelsTitleSizerH)


        self.levelsPathPanel = wx.Panel(self.levelsPanel, style=wx.BORDER_NONE)
        self.levelsPathSizerV = wx.BoxSizer(wx.VERTICAL)
        self.levelsPathPanel.SetSizer(self.levelsPathSizerV)

        self.levelsTitDescPanel = wx.Panel(self.levelsTitlePanel, style=wx.BORDER_NONE)
        self.levelsTitDescSizerV = wx.BoxSizer(wx.VERTICAL)
        self.levelsTitDescPanel.SetSizer(self.levelsTitDescSizerV)

        self.levelsTitButPanel = wx.Panel(self.levelsTitlePanel, style=wx.BORDER_NONE)
        self.levelsTitButSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.levelsTitButPanel.SetSizer(self.levelsTitButSizerH)

        levelsDescText = wx.StaticText(self.levelsTitDescPanel, label=lbl3)
        self.levelsButton = wx.Button(self.levelsTitButPanel, 104, "Browse")
        self.levelsResetButton = wx.Button(self.levelsTitButPanel, 105, "Reset to Default")
        # levelPad = wx.StaticText(self.levelsTitButPanel, size=(-1,-1))
        self.levelsResetButton.Hide()
        self.levelsPathText = wx.StaticText(self.levelsPathPanel, label=self.levelsDefaultPath)
        self.levelsPathText.SetForegroundColour("#5E9811")

        self.levelsTitDescSizerV.Add(levelsDescText, 1, wx.EXPAND)
        # self.levelsTitButSizerH.Add(self.levelsResetButton, 1, wx.EXPAND)
        # self.levelsTitButSizerH.Add(levelPad, 1, wx.EXPAND)
        self.levelsTitButSizerH.Add(self.levelsButton, 1, wx.EXPAND)
        
        
        self.levelsPathSizerV.Add(self.levelsPathText, 1, wx.EXPAND)

        self.levelsTitleSizerH.Add(self.levelsTitDescPanel, 4, wx.EXPAND)
        self.levelsTitleSizerH.Add(self.levelsTitButPanel, 1, wx.EXPAND)

        self.levelsSizerV.Add(self.levelsTitlePanel, 1, wx.EXPAND)
        self.levelsSizerV.Add(self.levelsPathPanel, 1, wx.EXPAND)



        self.configSizerV.Add(titlePanel, 0, wx.EXPAND)
        self.configSizerV.Add(self.stationsPanel, 1, wx.EXPAND)
        self.configSizerV.Add(self.metersPanel, 1, wx.EXPAND)
        self.configSizerV.Add(self.levelsPanel, 1, wx.EXPAND)

        self.bottomButtonPanel = wx.Panel(self, style=wx.BORDER_NONE)
        self.bottomButtonSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.bottomButtonPanel.SetSizer(self.bottomButtonSizerH)

        self.clearButton = wx.Button(self.bottomButtonPanel, 106, "Clear All Paths")
        self.closeButton = wx.Button(self.bottomButtonPanel, 107, "Done")

        self.bottomButtonSizerH.Add(self.clearButton, 1, wx.EXPAND)
        self.bottomButtonSizerH.Add(self.closeButton, 1, wx.EXPAND)
        
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.configPanel, 1, wx.EXPAND)
        self.sizer.Add(self.bottomButtonPanel, 0, wx.EXPAND)


        icon_path = self.iconName
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, icon_path)

        #PNG Icon
        if os.path.exists(icon_path):
            png = wx.Image(icon_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.icon = wx.Icon(png)
            self.SetIcon(self.icon)




        # Tell it which sizer is to be used for main frame
        # It may lay out automatically and be altered to fit window
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        # Show it !!!
        self.Show(1)

    def OnReset(self, event):
        self.stationsPathText.SetValue(self.stationsDefaultPath)



def main():
    # Set up a window based app, and create a main window in it
    app = wx.PySimpleApp()
    view = ConfigPanel(None, "User Configuration")
    # Enter event loop
    app.MainLoop()



if __name__ == "__main__":
    main()
