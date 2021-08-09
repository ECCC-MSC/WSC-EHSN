# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
from datetime import datetime as dt


class MyComboBox(wx.ComboBox):
    def __init__(self, *args, **kwargs):
        super(MyComboBox, self).__init__(*args, **kwargs)
        self.preValue = ""


class DropdownTime(wx.Panel):
    def __init__(self, displaySecond, *args, **kwargs):
        super(DropdownTime, self).__init__(*args, **kwargs)
        # self.SetWindowStyle(wx.BORDER_SIMPLE)
        self.minutes = self.GenerateMinutes()
        self.hours = self.GenerateHours()
        self.seconds = self.GenerateMinutes()
        self.hasSecond = displaySecond
        self.InitUI()


    def InitUI(self):


        mySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(mySizer)

        self.hourCmbox = MyComboBox(self, style=wx.CB_DROPDOWN, choices=self.hours)
        self.hourCmbox.parent = self

        self.minuteCmbox = MyComboBox(self, style=wx.CB_DROPDOWN, choices=self.minutes)
        self.minuteCmbox.parent = self
        if self.hasSecond:
            self.secondCmbox = MyComboBox(self, style=wx.CB_DROPDOWN, choices=self.minutes)
            timeText2 = wx.StaticText(self, label=':')
        timeText1 = wx.StaticText(self, label=':')


        mySizer.Add(self.hourCmbox, 1, wx.LEFT|wx.TOP, 3)
        mySizer.Add(timeText1, 0, wx.TOP, 3)
        mySizer.Add(self.minuteCmbox, 1, wx.TOP|wx.RIGHT, 3)
        if self.hasSecond:
            mySizer.Add(timeText2, 0, wx.TOP, 3)
            mySizer.Add(self.secondCmbox, 1, wx.RIGHT|wx.TOP, 3)

        self.cBtn = wx.Button(self, label="C", size=(13, -1))
        self.cBtn.parent = self
        self.cBtn.Bind(wx.EVT_BUTTON, self.OnCurrent)
        mySizer.Add(self.cBtn, 0)

        self.hourCmbox.Bind(wx.EVT_KEY_UP, self.OnTimeKeyUp)
        self.minuteCmbox.Bind(wx.EVT_KEY_UP, self.OnTimeKeyUp)


    def HideCBtn(self):
        self.cBtn.Hide()

    def ShowCBtn(self):
        self.CBtn.Show()

    def GenerateMinutes(self):
        a = list(range(60))
        b=[""]
        for i in a:
            n = str(i)
            if len(n) == 1:
                n = '0' + n
            b.append(n)
        return b

    def GenerateHours(self):
        a = list(range(24))
        b=[""]
        for i in a:
            n = str(i)
            if len(n) == 1:
                n = '0' + n
            b.append(n)
        return b


    def OnTimeKeyUp(self, event):
        keycode = event.GetKeyCode()
        self.NumberControl(event)
        if keycode == ord('R') or keycode == ord('C'):
            self.UpdateTime(keycode)      

        event.Skip()


    def UpdateTime(self, keycode):
        if keycode == ord('R'):
            self.Clear()
        elif keycode == ord('C'):
            self.SetToCurrent()


    def Clear(self):
        self.hourCmbox.ChangeValue("")
        self.minuteCmbox.ChangeValue("")
        if self.hasSecond:
            self.secondCmbox.ChangeValue("")


    def OnCurrent(self, evt):
        self.SetToCurrent()


    def SetToCurrent(self):

        currentTime = dt.now()
        hour = str(currentTime.hour)
        minute = str(currentTime.minute)
        second = str(currentTime.second)


        hour = "0" + hour if len(hour) == 1 else hour
        minute = ("0" + minute) if len(minute) == 1 else minute
        second = ("0" + second) if len(second) == 1 else second

        
        # hourCtrl = self.GetHourCtrl()
        # minCtrl = self.GetMinuteCtrl()
        if self.hasSecond:
            self.secondCmbox.Dismiss()

        # self.hourCmbox.Dismiss()
        # self.minuteCmbox.Dismiss()
        # if keycode == ord('R'):
        #     hourCtrl.SetValue("")
        #     minCtrl.SetValue("")
        #     if self.hasSecond:
        #         secCtrl.SetValue("")
        # elif keycode == ord('C'):
        #     hourCtrl.SetValue(hour)
        #     minCtrl.SetValue(minute)
        #     if self.hasSecond:
        #         secCtrl.SetValue(second)



        self.hourCmbox.ChangeValue(hour)
        self.minuteCmbox.ChangeValue(minute)
        if self.hasSecond:
            self.secondCmbox.ChangeValue(second)


    def GetHourVal(self):
        return self.hourCmbox.GetValue()

    def GetHour(self):
        return self.hourCmbox

    def SetHourVal(self, val):
        self.hourCmbox.SetValue(val)

    def ChangeHourVal(self, val):
        self.hourCmbox.ChangeValue(val)

    def GetMinuteVal(self):
        return self.minuteCmbox.GetValue()

    def GetMinute(self):
        return self.minuteCmbox

    def SetMinuteVal(self, val):
        self.minuteCmbox.SetValue(val)

    def ChangeMinuteVal(self, val):
        self.minuteCmbox.ChangeValue(val)


    def GetSecondVal(self):
        return self.secondCmbox.GetValue()

    def GetSecond(self):
        return self.secondCmbox

    def SetSecondVal(self, val):
        self.secondCmbox.SetValue(val)

    def ChangeSecondVal(self, val):
        self.secondCmbox.ChangeValue(val)

    def GetHourCtrl(self):
        return self.hourCmbox

    def GetMinuteCtrl(self):
        return self.minuteCmbox

    def GetSecondCtrl(self):
        return self.secondCmbox

    # #return the time in string format
    # def GetValue(self):
    #     if self.hasSecond:
    #         if self.GetHourVal() == "" and self.GetMinuteVal() == "" and self.GetSecondVal() == "":
    #             return ""
    #         else:
    #             return self.GetHourVal() + ":" + self.GetMinuteVal() + ":" + self.GetSecondVal()
    #     else:
    #         if self.GetHourVal() == "" and self.GetMinuteVal() == "":
    #             return self.GetHourVal() + ":" + self.GetMinuteVal() 
    #         else:
    #             return ""


    #return the time in string format
    def GetValue(self):
        if self.hasSecond:
            return self.GetHourVal() + ":" + self.GetMinuteVal() + ":" + self.GetSecondVal()
        else:

            return self.GetHourVal() + ":" + self.GetMinuteVal() 


    def SetValue(self, val):
        if val is None:
            self.SetSecondVal("")
            self.SetHourVal("")
            self.SetMinuteVal("")
        else:
            hour = val.split(":")[0]
            minute = val.split(":")[1]
            if self.hasSecond:
                second = val.split(":")[2]
                self.SetSecondVal(second)
            self.SetHourVal(hour)
            self.SetMinuteVal(minute)

    #return the smller time object
    def FindSmallerTime(self, time2):
        if self.GetHourVal() == '' or self.GetMinuteVal() == "" or time2.GetHourVal() == '' or time2.GetMinuteVal() == "":
            return 
        if self.GetHourVal() > time2.GetHourVal() or (self.GetHourVal() == time2.GetHourVal() and self.GetMinuteVal() > time2.GetMinuteVal()):
            return time2
        else:
            return self

    def CalculateMean(start, end):
        hasSecond = start.hasSecond and end.hasSecond

        startHour = start.GetHourVal()
        startMinute = start.GetMinuteVal()
        startSecond = start.GetSecondVal()
        endHour = end.GetHourVal()
        endMinute = end.GetMinuteVal()
        endSecond = end.GetSecondVal()


        if hasSecond:
            if startSecond == "" or endSecond == "" \
                or startHour == "" or startMinute == "" \
                or endHour == "" or endMinute == "":
                return 
        elif startHour == "" or startMinute == "" or endHour == "" or endMinute == "":
            return


        startHour = int(startHour)
        startMinute = int(startMinute)
        endHour = int(endHour)
        endMinute = int(endMinute)



        if not hasSecond:

            if startHour > endHour or (startHour == endHour and startMinute > endMinute):
                endHour += 24

            totalMinute = (startHour + endHour) * 60 + startMinute + endMinute
            meanMinute = totalMinute / 2

            meanHour = meanMinute / 60 % 24
            if meanHour < 10:
                meanHour = "0" + str(meanHour)

            meanMinute = meanMinute % 60
            if meanMinute < 10:
                meanMinute = "0" + str(meanMinute)

            return (str(meanHour) + ":" + str(meanMinute))

        else:

            startSecond = int(startSecond)
            endSecond = int(endSecond)

            if startHour > endHour or (startHour == endHour and startMinute > endMinute)\
                or (startHour == endHour and startMinute == endMinute and startSecond > endSecond):
                endHour += 24

            totalMinute = (startHour + endHour) * 60 + startMinute + endMinute
            totalSecond = totalMinute * 60 + startSecond + endSecond
            meanSecond = totalSecond / 2

            meanHour = meanSecond / 3600 % 24
            meanMinute = meanSecond / 60 % 60
            meanSecond = meanSecond % 3600 % 60 

            if meanHour < 10:
                meanHour = "0" + str(meanHour)

            if meanMinute < 10:
                meanMinute = "0" + str(meanMinute)

            if meanSecond < 10:
                meanSecond = "0" + str(meanSecond)
            return (str(meanHour) + ":" + str(meanMinute) + ":" + str(meanSecond))




    #Check if the time has value for hour, minute and second
    def IsCompleted(self):
        if not self.hasSecond:
            return self.GetHourVal() != '' and self.GetMinuteVal() != ''
        else:
            return self.GetHourVal() != '' and self.GetMinuteVal() != '' and self.GetSecondVal() != ''



    def SetBackgroundColour(self, color):
        self.hourCmbox.SetBackgroundColour(color)
        self.minuteCmbox.SetBackgroundColour(color)
        self.hourCmbox.Refresh()
        self.minuteCmbox.Refresh()



    def NumberControl(self, evt): 
        ctrl = evt.GetEventObject()
        value = ctrl.GetValue().strip()
        insertPoint = ctrl.GetInsertionPoint()
        digits = len(value) - len(ctrl.preValue)

        try:

            temp = int(value)
            temp = str(temp) if temp > 9 else "0" + str(temp)
            if ((ctrl == self.hourCmbox and temp in self.hours) or ((ctrl == self.minuteCmbox or ctrl == self.secondCmbox) and temp in self.minutes)) and len(value) < 3:

                ctrl.preValue = value  
                # ctrl.ChangeValue(value)

            else:
                ctrl.ChangeValue(ctrl.preValue)
                ctrl.SetInsertionPoint(insertPoint - digits)

            
        except:
            if value == "":
                ctrl.preValue = ""
                ctrl.ChangeValue("")
        
            else:
                ctrl.ChangeValue(ctrl.preValue)
                ctrl.SetInsertionPoint(insertPoint - digits)


        evt.Skip()