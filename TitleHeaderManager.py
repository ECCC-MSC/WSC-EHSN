# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from TitleHeaderPanel import *

class TitleHeaderManager(object):
    def __init__(self, mode, gui, manager = None):
        self.gui = gui
        self.gui.manager = self
        self.manager = manager

        self.mode = mode

    def Init(self):
        if self.mode == "DEBUG":
            print "TitleHeaderManager"

    @property
    def enteredInHWSCB(self):
        return self.gui.enteredInHWSCB.GetValue()

    @enteredInHWSCB.setter
    def enteredInHWSCB(self, enteredInHWSCB):
        self.gui.enteredInHWSCB.SetValue(enteredInHWSCB)


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(-1, 400))
    TitleHeaderManager("DEBUG", TitleHeaderPanel("DEBUG", frame))

    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
