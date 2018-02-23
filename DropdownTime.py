# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
from datetime import datetime as dt





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

        self.hourCmbox = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.CB_READONLY, choices=self.hours)
        self.minuteCmbox = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.CB_READONLY, choices=self.minutes)
        if self.hasSecond:
            self.secondCmbox = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.CB_READONLY, choices=self.minutes)
            timeText2 = wx.StaticText(self, label=':')
        timeText1 = wx.StaticText(self, label=':')


        mySizer.Add(self.hourCmbox, 1, wx.LEFT|wx.TOP, 3)
        mySizer.Add(timeText1, 0, wx.TOP, 3)
        mySizer.Add(self.minuteCmbox, 1, wx.TOP|wx.RIGHT, 3)
        if self.hasSecond:
            mySizer.Add(timeText2, 0, wx.TOP, 3)
            mySizer.Add(self.secondCmbox, 1, wx.RIGHT|wx.TOP, 3)

        self.hourCmbox.Bind(wx.EVT_KEY_DOWN, self.OnTimeKeyDown)
        self.minuteCmbox.Bind(wx.EVT_KEY_DOWN, self.OnTimeKeyDown)

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


    def OnTimeKeyDown(self, event):
        self.UpdateTime(event.GetKeyCode())
        event.Skip()


    def UpdateTime(self, keycode):
        # print keycode
        currentTime = dt.now()
        hour = str(currentTime.hour)
        minute = str(currentTime.minute)
        second = str(currentTime.second)


        hour = "0" + hour if len(hour) == 1 else hour
        minute = ("0" + minute) if len(minute) == 1 else minute
        second = ("0" + second) if len(second) == 1 else second

        
        hourCtrl = self.GetHourCtrl()
        minCtrl = self.GetMinuteCtrl()
        if self.hasSecond:
            secCtrl = self.GetSecondCtrl()
            secCtrl.Dismiss()

        hourCtrl.Dismiss()
        minCtrl.Dismiss()
        if keycode == ord('R'):
            hourCtrl.SetValue("")
            minCtrl.SetValue("")
            if self.hasSecond:
                secCtrl.SetValue("")
        elif keycode == ord('C'):
            hourCtrl.SetValue(hour)
            minCtrl.SetValue(minute)
            if self.hasSecond:
                secCtrl.SetValue(second)



    def GetHourVal(self):
        return self.hourCmbox.GetValue()

    def SetHourVal(self, val):
        self.hourCmbox.SetValue(val)


    def GetMinuteVal(self):
        return self.minuteCmbox.GetValue()

    def SetMinuteVal(self, val):
        self.minuteCmbox.SetValue(val)

    def GetSecondVal(self):
        return self.secondCmbox.GetValue()

    def SetSecondVal(self, val):
        self.secondCmbox.SetValue(val)

    def GetHourCtrl(self):
        return self.hourCmbox

    def GetMinuteCtrl(self):
        return self.minuteCmbox

    def GetSecondCtrl(self):
        return self.secondCmbox

    #return the time in string format
    def GetValue(self):
        if self.hasSecond:
            return self.GetHourVal() + ":" + self.GetMinuteVal() + ":" + self.GetSecondVal()
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

