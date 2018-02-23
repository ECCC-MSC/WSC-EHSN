from AnnualLevellingPanel import *

class AnnualLevellingManager(object):
    def __init__(self, mode, gui, manager=None):

        self.gui = gui
        self.gui.manager = self
        self.manager = manager
        
        self.mode = mode

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "AnnualLevellingControl"


    @property
    def levelNotesSizer(self):
        return self.gui.levelNotes.levelNotesSizerV

    @levelNotesSizer.setter
    def levelNotesSizer(self, levelNotesSizer):
        self.gui.levelNotes.levelNotesSizerV = levelNotesSizer


    @property
    def closure(self):
        return self.gui.levelNotes.closureCtrl.GetValue()

    @closure.setter
    def closure(self, closure):
        self.gui.levelNotes.closureCtrl.SetValue(closure)


    #Gets table val for given row/col
    #row/col start at 0
    #row max val is defined in constructor of WaterLevelNotesPanel
    #col max val 6
    def GetTableValue(self, row, col):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.levelNotesSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.levelNotesSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1

        sizerItem = self.levelNotesSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()
        return sizerItem.GetValue()
    


    #Sets table val for given row/col
    #row/col start at 0
    #row max val is defined in constructor of WaterLevelNotesPanel
    #col max val 6
    def SetTableValue(self, row, col, val):
        if row < 0:
            row = 0
        if col < 0:
            col = 0
        
        row += 1
        maxrow = len(self.levelNotesSizer.GetChildren())
        if row >= maxrow:
            row = maxrow - 1
        
        maxcol = len(self.levelNotesSizer.GetItem(row).GetSizer().GetChildren())
        if col >= maxcol:
            col = maxcol - 1

        sizerItem = self.levelNotesSizer.GetItem(row).GetSizer().GetItem(col).GetWindow()
        sizerItem.SetValue(val)
    


    #Table Row info
    def OnEnter(self, row):
        print "\n%s" % row
        print "Station: %s" % self.GetTableValue(int(row), 0)
        print "Backsight: %s" % self.GetTableValue(int(row), 1)
        print "Height of Instr: %s" % self.GetTableValue(int(row), 2)
        print "Foresight: %s" % self.GetTableValue(int(row), 3)
        print "Elevation: %s" % self.GetTableValue(int(row), 4)
        print "Phys Desc: %s" % self.GetTableValue(int(row), 5)
        print "Comments: %s" % self.GetTableValue(int(row), 6)

    
    #On Enter in text field, set specified cell
    def OnEnterSet(self, row, col, val):
        self.SetTableValue(int(row), int(col), val)
        
        self.OnEnter(row)


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 700))
    AnnualLevellingManager("DEBUG", AnnualLevellingPanel("DEBUG", frame))
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
