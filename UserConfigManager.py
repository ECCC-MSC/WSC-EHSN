# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from UserConfigPanel import *


class UserConfigManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "UserConfigControl"


    #Station Number
    @property
    def stationNumCtrl(self):
        return self.gui.stationNumCtrl.GetValue()

    @stationNumCtrl.setter
    def stationNumCtrl(self, stationNumCtrl):
        self.gui.stationNumCtrl.SetValue(stationNumCtrl)



    #Station Name
    @property
    def stationNameCtrl(self):
        return self.gui.stationNameCtrl.GetValue()

    @stationNameCtrl.setter
    def stationNameCtrl(self, stationNameCtrl):
        self.gui.stationNameCtrl.SetValue(stationNameCtrl)





def main():
    app = wx.App()

    frame = wx.Frame(None, size=(500, 400))
    UserConfigManager("DEBUG", UserConfigPanel("DEBUG", wx.LANGUAGE_FRENCH, frame))

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()