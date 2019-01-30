# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import wx.adv as adv
# import wx.combo as cb




class GenInfoPanel(wx.Panel):
    def __init__(self, mode, *args, **kwargs):
        super(GenInfoPanel, self).__init__(*args, **kwargs)


        self.stnNumTxtLbl = "Station Number:"
        self.dateTxtLbl = "Date:"
        self.stnNameTxtLbl = "Station Name:"
        self.tzTxtLbl = "Time Zone:"
        self.timeZones = ['', 'PST', 'MST', 'CST',
                          'EST', 'AST', 'NST']
        self.numbers = []
        self.names = []
        self.mode = mode
        self.manager = None
        
        self.lang = wx.LANGUAGE_FRENCH
        self.InitUI()
		#disable the event to be triggered



    def do_nothing(self,evt):
        pass
    def OnTextTypeNum(self, event):
        insertPoint = self.stnNumCmbo.GetInsertionPoint()
        self.stnNumCmbo.ChangeValue(unicode.upper(self.stnNumCmbo.GetValue()))
        self.stnNumCmbo.SetInsertionPoint(insertPoint)
        
    def OnTextTypeName(self, event):
        insertPoint = self.stnNameCtrl.GetInsertionPoint()
        self.stnNameCtrl.ChangeValue(unicode.upper(self.stnNameCtrl.GetValue()))
        self.stnNameCtrl.SetInsertionPoint(insertPoint)
        
    def InitUI(self):
        if self.mode == "DEBUG":
            print "In GenInfoPanel"

        self.locale = wx.Locale(self.lang)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Station Number, and Date
        stnNumTxt = wx.StaticText(self, label=self.stnNumTxtLbl)
        self.stnNumCmbo = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER, choices=self.numbers)

        self.stnNumCmbo.Bind(wx.EVT_TEXT, self.OnTextTypeNum)
        self.stnNumCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)



        dateTxt = wx.StaticText(self, label=self.dateTxtLbl)
        self.datePicker = adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)

        # self.datePicker = adv.CalendarCtrl(self, style=wx.adv.CAL_SHOW_HOLIDAYS|wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        # self.datePicker.SetHeaderColours('White','Blue')
        # self.datePicker.SetHolidayColours('White','Blue')
        # Add them to sizer
        row1.Add(stnNumTxt, 0, wx.RIGHT, 5)
        row1.Add(self.stnNumCmbo, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        row1.Add(dateTxt, 0, wx.LEFT|wx.RIGHT, 5)
        row1.Add(self.datePicker, 0, wx.LEFT|wx.EXPAND, 5)
        

        # Station Name and Timezone
        stnNameTxt = wx.StaticText(self, label=self.stnNameTxtLbl)
        # self.stnNameCtrl = wx.TextCtrl(self)
        self.stnNameCtrl = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER, choices=self.names)
        self.stnNameCtrl.Bind(wx.EVT_TEXT, self.OnTextTypeName)
        tzTxt = wx.StaticText(self, label=self.tzTxtLbl)
        self.tzCmbo = wx.ComboBox(self, choices=self.timeZones, value="", style=wx.CB_READONLY)
        self.tzCmbo.Bind(wx.EVT_COMBOBOX, self.updateParentTZ)
        self.tzCmbo.Bind(wx.EVT_MOUSEWHEEL, self.do_nothing)

        # Add them to sizer
        row2.Add(stnNameTxt, 0, wx.RIGHT, 5)
        row2.Add(self.stnNameCtrl, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        row2.Add(tzTxt, 0, wx.LEFT|wx.RIGHT, 5)
        row2.Add(self.tzCmbo, 0, wx.LEFT, 5)

        self.vbox.Add(row1, 0, wx.ALL|wx.EXPAND, 5)
        self.vbox.Add(row2, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(self.vbox)


    # Upon Timezone change, update the Main GUI's timezone val
    def updateParentTZ(self, e):
        if self.GetParent() is not None:
            val = self.GetTzCmbo()
            self.GetParent().timezone = val
        e.Skip()
        


    #Reset station numbers
    def updateNumbers(self, items):

        num = ''
        if self.GetStnNumCmbo() != '':
            num = self.GetStnNumCmbo()
        self.stnNumCmbo.Clear()
        self.stnNumCmbo.AppendItems(items)
        if num != '':
            self.stnNumCmbo.ChangeValue(num)


        self.vbox.Layout()
        self.Update()

    def UpdateNames(self, names):
        name = ''
        if self.GetStnName() != '':
            name = self.GetStnName()
        self.stnNameCtrl.Clear()
        self.stnNameCtrl.AppendItems(names)
        if name != '':
            self.stnNumCmbo.ChangeValue(name)

    #vbox sizer
    def GetVbox(self):
        return self.vbox



    def GetStnNumCmboCtrl(self):
        return self.stnNumCmbo


    #Station Number Ctrl
    def GetStnNumCmbo(self):
        return self.stnNumCmbo.GetValue()


    def SetStnNumCmbo(self, stnNumCmbo):
        self.stnNumCmbo.SetValue(stnNumCmbo)

    #Date Ctrl

    def GetDatePicker(self):
        if self.manager is not None:

            fm = "%Y/%m/%d" if self.manager.manager is None else self.manager.manager.DT_FORMAT
        else:
            fm = "%Y/%m/%d"
        return self.datePicker.GetValue().Format(fm)


    def SetDatePicker(self, datePicker):
        date = wx.DateTime()
        if self.manager is not None:
            fm = "%Y/%m/%d" if self.manager.manager is None else self.manager.manager.DT_FORMAT
        else:
            fm = "%Y/%m/%d"

        date.ParseFormat(datePicker, fm)
        self.datePicker.SetValue(date)



    #Station Name Ctrl

    def GetStnName(self):
        return self.stnNameCtrl.GetValue()


    def SetStnName(self, stnName):
        self.stnNameCtrl.SetValue(stnName)






    #Time Zone ComboBox

    def GetTzCmbo(self):
        return self.tzCmbo.GetValue()

    def SetTzCmbo(self, tzCmbo):
        self.tzCmbo.SetValue(tzCmbo)











def main():
    app = wx.App()

    frame = wx.Frame(None)
    GenInfoPanel("DEBUG", frame)

    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
