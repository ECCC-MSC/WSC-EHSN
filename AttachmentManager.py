# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0.
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from AttachmentPanel import *


class AttachmentManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager

        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "AttachmentManager"

    def returnAttachment(self):
        boxList = [self.gui.attachBox1, self.gui.attachBox2, self.gui.attachBox3, self.gui.attachBox4, self.gui.attachBox5,
                   self.gui.attachBox6, self.gui.attachBox7]
        for box in boxList:
            if box.returnPath() != []:
                return True
        return False

    def returnLoggerData(self):
        return self.gui.attachBox1.returnPath() != []

    def returnLoggerDiagnostic(self):
        return self.gui.attachBox2.returnPath() != []

    def returnLoggerProgram(self):
        return self.gui.attachBox3.returnPath() != []

    def returnMultipleLogger(self):
        return self.gui.attachBox4.returnPath() != []

    def returnMmtFiles(self):
        return self.gui.attachBox5.returnPath() != []

    def returnMmtSummary(self):
        return self.gui.attachBox6.returnPath() != []

    def returnSIT(self):
        return self.gui.attachBox7.returnSIT() != []

    def returnSTR(self):
        return self.gui.attachBox7.returnSTR() != []

    def returnCOL(self):
        return self.gui.attachBox7.returnCOL() != []

    def returnCBL(self):
        return self.gui.attachBox7.returnCBL() != []

    def returnEQP(self):
        return self.gui.attachBox7.returnEQP() != []

    def returnCDT(self):
        return self.gui.attachBox7.returnCDT() != []

    def returnHSN(self):
        return self.gui.attachBox7.returnHSN() != []


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 700))
    AttachmentManager("DEBUG", AttachmentPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
