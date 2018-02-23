from PartyInfoPanel import *


class PartyInfoManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "PartyInfoControl"

    #Party Control
    @property
    def partyCtrl(self):
        return self.gui.partyCtrl.GetValue()

    @partyCtrl.setter
    def partyCtrl(self, partyCtrl):
        self.gui.partyCtrl.SetValue(partyCtrl)


    #Completed Control
    @property
    def completeCtrl(self):
        return self.gui.completeCtrl.GetValue()

    @completeCtrl.setter
    def completeCtrl(self, completeCtrl):
        self.gui.completeCtrl.SetValue(completeCtrl)


    #Checked Control
    @property
    def checkCtrl(self):
        return self.gui.checkCtrl.GetValue()

    @checkCtrl.setter
    def checkCtrl(self, checkCtrl):
        self.gui.checkCtrl.SetValue(checkCtrl)
        
        
    # Reviewed Checked
    @property
    def reviewedCB(self):
        return self.gui.ReviewedIsChecked()
        
    @reviewedCB.setter
    def reviewedCB(self, reviewedCBVal):
        self.gui.reviewedCB.SetValue(reviewedCBVal)


    def GetPartyCtrl(self):
        return self.gui.partyCtrl
    def GetCompleteCtrl(self):
        return self.gui.completeCtrl
    def GetReviewedCB(self):
        return self.gui.reviewedCB



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 70))
    PartyInfoManager("DEBUG", PartyInfoPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
