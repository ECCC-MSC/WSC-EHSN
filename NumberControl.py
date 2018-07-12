import math
from sigfig import * 
# import wx
# #Overwrite the TextCtrl Class in order to control the float input
# class MyTextCtrl(wx.TextCtrl):
#     def __init__(self, *args, **kwargs):
#         super(MyTextCtrl, self).__init__(*args, **kwargs)
#         self.preValue = ""

#allow only the float number type inputs
def FloatNumberControl(evt): 
    ctrl = evt.GetEventObject()
    value = ctrl.GetValue().strip()
    insertPoint = ctrl.GetInsertionPoint()
    digits = len(value) - len(ctrl.preValue)


    try:
        float(value)
        ctrl.preValue = value
        
        ctrl.ChangeValue(value)
        # ctrl.SetInsertionPoint(insertPoint + digits)
        
    except:
        if ctrl.GetValue() == '':
            ctrl.preValue = ''
            # ctrl.SetInsertionPoint(insertPoint + digits)
        elif ctrl.GetValue() == '.':
            ctrl.preValue = '.'
            # ctrl.SetInsertionPoint(insertPoint + digits)
        elif ctrl.GetValue() == '-':
            ctrl.preValue = '-'
            # ctrl.SetInsertionPoint(insertPoint + digits)
        elif ctrl.GetValue() == '-.':
            ctrl.preValue = '-.'
            # ctrl.SetInsertionPoint(insertPoint + digits)
        elif ctrl.GetValue() == '+':
            ctrl.preValue = '+'
            # ctrl.SetInsertionPoint(insertPoint + digits)
        elif ctrl.GetValue() == '+.':
            ctrl.preValue = '+.'
            # ctrl.SetInsertionPoint(insertPoint + digits)
        else:
            # insertPoint = ctrl.GetInsertionPoint() - digits
            ctrl.SetValue(ctrl.preValue)
            ctrl.SetInsertionPoint(insertPoint - digits)
            # print "go back"
    evt.Skip()

#Rounding by significant number
def RoundSigfigs(num, sig_figs):
    if num == "":
        return ""
    try:
        num = float(num)
    except:
        return 0
    if num != 0:
        # result = round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
        result = round_sig(num, sig_figs)
        return result
        # if result == int(result):
        #     return int(result)
        # else:
        #     return result
    else:
        return 0  # Can't take the log of 0

#rounding by digit
def Round(digit, ctrl):
    
    if ctrl.GetValue() == "":
        return
    if ctrl.GetValue() == "+" or ctrl.GetValue() == "-" or ctrl.GetValue() == "." \
    or ctrl.GetValue() == "+." or ctrl.GetValue() == "-.":
        ctrl.ChangeValue("")
        ctrl.preValue = ""
        return
    strDigit = '{0:.' + str(digit) + 'f}'
    val = strDigit.format(float(ctrl.GetValue()) + 10**(-10))
    # print val
    ctrl.ChangeValue(val)
    ctrl.preValue = val

def RoundByCtrl1(ctrl):
    insertPoint = ctrl.GetInsertionPoint()
    Round(1, ctrl)
    ctrl.SetInsertionPoint(insertPoint)

def RoundByCtrl2(ctrl):
    insertPoint = ctrl.GetInsertionPoint()
    Round(2, ctrl)
    ctrl.SetInsertionPoint(insertPoint)

def RoundByCtrl3(ctrl):
    insertPoint = ctrl.GetInsertionPoint()
    Round(3, ctrl)
    ctrl.SetInsertionPoint(insertPoint)

def RoundByCtrl4(ctrl):
    insertPoint = ctrl.GetInsertionPoint()
    Round(4, ctrl)
    ctrl.SetInsertionPoint(insertPoint)

def RoundByCtrl5(ctrl):
    insertPoint = ctrl.GetInsertionPoint()
    Round(5, ctrl)
    ctrl.SetInsertionPoint(insertPoint)


#round to 1 decimal points
def Round1(event):
    insertPoint = event.GetEventObject().GetInsertionPoint()
    Round(1, event.GetEventObject())
    event.GetEventObject().SetInsertionPoint(insertPoint)

    event.Skip()

#round to 2 decimal points
def Round2(event):
    insertPoint = event.GetEventObject().GetInsertionPoint()
    Round(2, event.GetEventObject())
    event.GetEventObject().SetInsertionPoint(insertPoint)
    event.Skip()

#round to 3 decimal points
def Round3(event):
    insertPoint = event.GetEventObject().GetInsertionPoint()

    Round(3, event.GetEventObject())
    event.GetEventObject().SetInsertionPoint(insertPoint)

    event.Skip()

#round to 4 decimal points
def Round4(event):
    insertPoint = event.GetEventObject().GetInsertionPoint()
    Round(4, event.GetEventObject())
    event.GetEventObject().SetInsertionPoint(insertPoint)
    event.Skip()

#round to 5 decimal points
def Round5(event):
    insertPoint = event.GetEventObject().GetInsertionPoint()
    Round(5, event.GetEventObject())
    event.GetEventObject().SetInsertionPoint(insertPoint)
    event.Skip()

#Keep 1 significant digit
def Sig1(event):
    event.GetEventObject().ChangeValue(str(RoundSigfigs(event.GetEventObject().GetValue(), 1)))
    event.GetEventObject().preValue = str(RoundSigfigs(event.GetEventObject().GetValue(), 1))
    event.Skip()

#Keep 2 significant digit
def Sig2(event):
    event.GetEventObject().ChangeValue(str(RoundSigfigs(event.GetEventObject().GetValue(), 2)))
    event.GetEventObject().preValue = str(RoundSigfigs(event.GetEventObject().GetValue(), 2))
    event.Skip()

#Keep 3 significant digit
def Sig3(event):
    event.GetEventObject().ChangeValue(str(RoundSigfigs(event.GetEventObject().GetValue(), 3)))
    event.GetEventObject().preValue = str(RoundSigfigs(event.GetEventObject().GetValue(), 3))
    event.Skip()


#Keep 4 significant digit
def Sig4(event):
    event.GetEventObject().ChangeValue(str(RoundSigfigs(event.GetEventObject().GetValue(), 4)))
    event.GetEventObject().preValue = str(RoundSigfigs(event.GetEventObject().GetValue(), 4))
    event.Skip()

def SigByCtrl1(ctrl):
    ctrl.ChangeValue(str(RoundSigfigs(ctrl.GetValue(), 1)))
    ctrl.preValue = str(RoundSigfigs(ctrl.GetValue(), 1))

def SigByCtrl2(ctrl):
    ctrl.ChangeValue(str(RoundSigfigs(ctrl.GetValue(), 2)))
    ctrl.preValue = str(RoundSigfigs(ctrl.GetValue(), 2))

def SigByCtrl3(ctrl):
    ctrl.ChangeValue(str(RoundSigfigs(ctrl.GetValue(), 3)))
    ctrl.preValue = str(RoundSigfigs(ctrl.GetValue(), 3))

def SigByCtrl4(ctrl):
    ctrl.ChangeValue(str(RoundSigfigs(ctrl.GetValue(), 4)))
    ctrl.preValue = str(RoundSigfigs(ctrl.GetValue(), 4))


#Allow only integer
def OnChar_int(event): 

    key = event.GetKeyCode() 

    acceptable_characters = "1234567890." 

    if chr(key) in acceptable_characters: 
        event.Skip() 
        return 

    else: 
        event.Skip()
        return False 