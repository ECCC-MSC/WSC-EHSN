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
            print("AttachmentManager")

    def returnAttachment(self):
        boxList = [self.gui.attachBox1, self.gui.attachBox2, self.gui.attachBox3, self.gui.attachBox4, self.gui.attachBox5,
                   self.gui.attachBox6, self.gui.attachBox7]
        for box in boxList:
            if box.returnPath() != []:
                return True
        return False

    def returnLoggerFolder(self):
        return str(self.gui.attachBox1.returnPath())[1:-1].replace('\\\\', '\\')

    def returnLoggerFiles(self):
        return str(self.gui.attachBox2.returnPath())[1:-1].replace('\\\\', '\\')

    def returnLoggerDiagnostic(self):
        return str(self.gui.attachBox3.returnPath())[1:-1].replace('\\\\', '\\')

    def returnLoggerProgram(self):
        return str(self.gui.attachBox4.returnPath())[1:-1].replace('\\\\', '\\')
    
    def returnMmtFiles(self):
        return str(self.gui.attachBox5.returnFilePath())[1:-1].replace('\\\\', '\\')
    
    def returnMmtFolders(self):
        return str(self.gui.attachBox5.returnFolderPath())[1:-1].replace('\\\\', '\\')

    def returnMmtSummary(self):
        return str(self.gui.attachBox6.returnPath())[1:-1].replace('\\\\', '\\')

    def returnSIT(self):
        return str(self.gui.attachBox7.returnSIT())[1:-1].replace('\\\\', '\\')

    def returnSTR(self):
        return str(self.gui.attachBox7.returnSTR())[1:-1].replace('\\\\', '\\')

    def returnCOL(self):
        return str(self.gui.attachBox7.returnCOL())[1:-1].replace('\\\\', '\\')

    def returnCBL(self):
        return str(self.gui.attachBox7.returnCBL())[1:-1].replace('\\\\', '\\')

    def returnEQP(self):
        return str(self.gui.attachBox7.returnEQP())[1:-1].replace('\\\\', '\\')

    def returnCDT(self):
        return str(self.gui.attachBox7.returnCDT())[1:-1].replace('\\\\', '\\')

    def returnHSN(self):
        return str(self.gui.attachBox7.returnHSN())[1:-1].replace('\\\\', '\\')

    def returnZip(self):
        return self.gui.zipAddr.GetValue()

    def returnData(self):
        return self.gui.attachBox1.dataCheck.GetValue()
    
    def returnDiagnostic(self):
        return self.gui.attachBox1.diagnosticCheck.GetValue()
    
    def returnProgram(self):
        return self.gui.attachBox1.programCheck.GetValue()
    
def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 700))
    AttachmentManager("DEBUG", AttachmentPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
