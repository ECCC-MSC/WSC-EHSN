# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from WaterLevelNotesPanel import *
import wx.lib.scrolledpanel as scrolledpanel
#import NumberControl
from DropdownTime import *
#import wx.lib.agw.toasterbox as tb
import pandas as pd
import os
from datetime import datetime as dt
from glob import glob
from textwrap import wrap






# ==============================================
# ==============================================
# ====  Communication device popup dialogs  ====
# ==============================================
# ==============================================


class GOESDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:22])

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        current_values = title.split('&&&&&&&&&&&&')

        # PDT
        PDTLbl = wx.StaticText(self, label="IP or PDT Address:")
        popupSizer.Add(PDTLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.PDTCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.PDTCtrl.SetValue(current_values[1])
        popupSizer.Add(self.PDTCtrl, 0, wx.EXPAND)

        # XMT rate
        XMTRateLbl = wx.StaticText(self, label="XMT Rate:")
        popupSizer.Add(XMTRateLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.XMTRateCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.XMTRateCtrl.SetValue(current_values[2])
        popupSizer.Add(self.XMTRateCtrl, 0, wx.EXPAND)

        # XMT window
        XMTWindowLbl = wx.StaticText(self, label="XMT Window:")
        popupSizer.Add(XMTWindowLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.XMTWindowCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.XMTWindowCtrl.SetValue(current_values[3])
        popupSizer.Add(self.XMTWindowCtrl, 0, wx.EXPAND)

        # XMT period
        XMTPeriodLbl = wx.StaticText(self, label="XMT Period:")
        popupSizer.Add(XMTPeriodLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.XMTPeriodCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.XMTPeriodCtrl.SetValue(current_values[4])
        popupSizer.Add(self.XMTPeriodCtrl, 0, wx.EXPAND)

        # XMT first
        XMTFirstLbl = wx.StaticText(self, label="First XMT:")
        popupSizer.Add(XMTFirstLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.XMTFirstCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.XMTFirstCtrl.SetValue(current_values[5])
        popupSizer.Add(self.XMTFirstCtrl, 0, wx.EXPAND)

        # Prime channel
        PrimeChannelLbl = wx.StaticText(self, label="Prime Channel:")
        popupSizer.Add(PrimeChannelLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.PrimeChannelCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.PrimeChannelCtrl.SetValue(current_values[6])
        popupSizer.Add(self.PrimeChannelCtrl, 0, wx.EXPAND)

        # TX Freq
        TXFreqLbl = wx.StaticText(self, label="Transmission Frequency (optional):")
        popupSizer.Add(TXFreqLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.TXFreqCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.TXFreqCtrl.SetValue(current_values[7])
        popupSizer.Add(self.TXFreqCtrl, 0, wx.EXPAND)


        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()

    def GetPDT(self):
        return self.PDTCtrl.GetValue()

    def GetXMTRate(self):
        return self.XMTRateCtrl.GetValue()
    
    def GetXMTWindow(self):
        return self.XMTWindowCtrl.GetValue()
    
    def GetXMTPeriod(self):
        return self.XMTPeriodCtrl.GetValue()
    
    def GetXMTFirst(self):
        return self.XMTFirstCtrl.GetValue()
    
    def GetPrimeChannel(self):
        return self.PrimeChannelCtrl.GetValue()
    
    def GetTXFreq(self):
        return self.TXFreqCtrl.GetValue()



class CAMERADialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:18])

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        current_values = title.split('&&&&&&&&&&&&')

        # PDT
        PDTLbl = wx.StaticText(self, label="IP or PDT Address:")
        popupSizer.Add(PDTLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.PDTCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.PDTCtrl.SetValue(current_values[1])
        popupSizer.Add(self.PDTCtrl, 0, wx.EXPAND)


        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()

    def GetPDT(self):
        return self.PDTCtrl.GetValue()



class IMAGEVELOCIMETRYDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:31])

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        current_values = title.split('&&&&&&&&&&&&')

        # PDT
        PDTLbl = wx.StaticText(self, label="IP or PDT Address:")
        popupSizer.Add(PDTLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.PDTCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.PDTCtrl.SetValue(current_values[1])
        popupSizer.Add(self.PDTCtrl, 0, wx.EXPAND)


        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()

    def GetPDT(self):
        return self.PDTCtrl.GetValue()



class NETWORKDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:17])

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        current_values = title.split('&&&&&&&&&&&&')

        # PDT
        PDTLbl = wx.StaticText(self, label="IP or PDT Address:")
        popupSizer.Add(PDTLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.PDTCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.PDTCtrl.SetValue(current_values[1])
        popupSizer.Add(self.PDTCtrl, 0, wx.EXPAND)


        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()

    def GetPDT(self):
        return self.PDTCtrl.GetValue()



class MODEMDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:14])

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        current_values = title.split('&&&&&&&&&&&&')

        # Baud Rate
        BaudLbl = wx.StaticText(self, label="Baud Rate:")
        popupSizer.Add(BaudLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.BaudCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.BaudCtrl.SetValue(current_values[1])
        popupSizer.Add(self.BaudCtrl, 0, wx.EXPAND)

        # Parity
        ParityLbl = wx.StaticText(self, label="Parity:")
        popupSizer.Add(ParityLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.ParityCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.ParityCtrl.SetValue(current_values[2])
        popupSizer.Add(self.ParityCtrl, 0, wx.EXPAND)

        # Telephone Number
        TelephoneLbl = wx.StaticText(self, label="Telephone Number:")
        popupSizer.Add(TelephoneLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.TelephoneCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.TelephoneCtrl.SetValue(current_values[3])
        popupSizer.Add(self.TelephoneCtrl, 0, wx.EXPAND)


        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()

    def GetBaud(self):
        return self.BaudCtrl.GetValue()
    
    def GetParity(self):
        return self.ParityCtrl.GetValue()
    
    def GetTelephone(self):
        return self.TelephoneCtrl.GetValue()





# ==================================
# ==================================
# ====  Transfer popup dialogs  ====
# ==================================
# ==================================


class TransferDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:16])

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        destinationLbl = wx.StaticText(self, label="Destination Location:")
        popupSizer.Add(destinationLbl, 0, wx.ALL | wx.EXPAND, 5)

        self.destinationCtrl = MyTextCtrl(self, style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
        self.destinationCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        popupSizer.Add(self.destinationCtrl, 0, wx.EXPAND)

        if len(title) > 16:
            titles = title.split('&&&&&&&&&&&&')
            self.destinationCtrl.SetValue(titles[1])
            self.destinationCtrl.Disable()

        destinationStatusLbl = wx.StaticText(self, label="Destination status:")
        popupSizer.Add(destinationStatusLbl, 0, wx.ALL | wx.EXPAND, 5)
        if len(title) > 16:
            destinationOptions = ['ACTIVE', 'INACTIVE']
            self.destinationStatusCtrl = wx.ComboBox(self, choices=destinationOptions, style=wx.CB_READONLY)
            self.destinationStatusCtrl.SetSelection(0)
        else:
            destinationOptions = ['SHELVED']
            self.destinationStatusCtrl = wx.ComboBox(self, choices=destinationOptions, style=wx.CB_READONLY)
            self.destinationStatusCtrl.SetSelection(0)
            self.destinationStatusCtrl.Disable()
        popupSizer.Add(self.destinationStatusCtrl, 0, wx.ALL | wx.EXPAND, 5)

        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()

    #convert to upper case
    def OnTextType(self, event):
        textCtr=event.GetEventObject()
        point = textCtr.GetInsertionPoint()
        textCtr.ChangeValue(str.upper(textCtr.GetValue()))
        textCtr.SetInsertionPoint(point)

    def GetDestination(self):
        return self.destinationCtrl.GetValue()

    def GetDestinationStatus(self):
        return self.destinationStatusCtrl.GetValue()



class SummaryDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title[:7])

        text_full = title.split('&&&&&&&&&&&&')
        fontTitle = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        fontItem = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        Lbl1 = wx.StaticText(self, label='Destination Station ID: ')
        Lbl2 = wx.StaticText(self, label='Original Status: ')
        Lbl11 = wx.StaticText(self, label='Status Change: ')
        Lbl12 = wx.StaticText(self, label='Deployment Status: ')
        Lbl3 = wx.StaticText(self, label='Category: ')
        Lbl4 = wx.StaticText(self, label='Make: ')
        Lbl5 = wx.StaticText(self, label='Model: ')
        Lbl6 = wx.StaticText(self, label='Serial Number: ')
        Lbl7 = wx.StaticText(self, label='Firmware/Software: ')
        Lbl8 = wx.StaticText(self, label='Installation Date: ')
        Lbl9 = wx.StaticText(self, label='Effective Date: ')
        Lbl10 = wx.StaticText(self, label='Remark: ')
        Lbl13 = wx.StaticText(self, label='New Remark: ')

        Lbl1.SetFont(fontTitle)
        Lbl2.SetFont(fontTitle)
        Lbl11.SetFont(fontTitle)
        Lbl12.SetFont(fontTitle)
        Lbl3.SetFont(fontTitle)
        Lbl4.SetFont(fontTitle)
        Lbl5.SetFont(fontTitle)
        Lbl6.SetFont(fontTitle)
        Lbl7.SetFont(fontTitle)
        Lbl8.SetFont(fontTitle)
        Lbl9.SetFont(fontTitle)
        Lbl10.SetFont(fontTitle)
        Lbl13.SetFont(fontTitle)

        Itm1 = wx.StaticText(self, label=text_full[1])
        Itm2 = wx.StaticText(self, label=text_full[2])
        Itm11 = wx.StaticText(self, label=text_full[11])
        Itm12 = wx.StaticText(self, label=text_full[12])
        Itm3 = wx.StaticText(self, label=text_full[3])
        Itm4 = wx.StaticText(self, label=text_full[4])
        Itm5 = wx.StaticText(self, label=text_full[5])
        Itm6 = wx.StaticText(self, label=text_full[6])
        Itm7 = wx.StaticText(self, label=text_full[7])
        Itm8 = wx.StaticText(self, label=text_full[8])
        Itm9 = wx.StaticText(self, label=text_full[9])
        Itm10 = wx.StaticText(self, label=text_full[10])
        Itm13 = wx.StaticText(self, label=text_full[13])
        
        # Wrapping text of both remark and new remark
        Itm10.Wrap(150)
        Itm13.Wrap(150)

        Itm1.SetFont(fontItem)
        Itm2.SetFont(fontItem)
        Itm11.SetFont(fontItem)
        Itm12.SetFont(fontItem)
        Itm3.SetFont(fontItem)
        Itm4.SetFont(fontItem)
        Itm5.SetFont(fontItem)
        Itm6.SetFont(fontItem)
        Itm7.SetFont(fontItem)
        Itm8.SetFont(fontItem)
        Itm9.SetFont(fontItem)
        Itm10.SetFont(fontItem)
        Itm13.SetFont(fontItem)

        Row1 = wx.BoxSizer(wx.HORIZONTAL)
        Row1.Add(Lbl1, 0, wx.EXPAND)
        Row1.Add(Itm1, 0, wx.EXPAND)
        Row2 = wx.BoxSizer(wx.HORIZONTAL)
        Row2.Add(Lbl2, 0, wx.EXPAND)
        Row2.Add(Itm2, 0, wx.EXPAND)
        Row11 = wx.BoxSizer(wx.HORIZONTAL)
        Row11.Add(Lbl11, 0, wx.EXPAND)
        Row11.Add(Itm11, 0, wx.EXPAND)
        Row12 = wx.BoxSizer(wx.HORIZONTAL)
        Row12.Add(Lbl12, 0, wx.EXPAND)
        Row12.Add(Itm12, 0, wx.EXPAND)
        Row3 = wx.BoxSizer(wx.HORIZONTAL)
        Row3.Add(Lbl3, 0, wx.EXPAND)
        Row3.Add(Itm3, 0, wx.EXPAND)
        Row4 = wx.BoxSizer(wx.HORIZONTAL)
        Row4.Add(Lbl4, 0, wx.EXPAND)
        Row4.Add(Itm4, 0, wx.EXPAND)
        Row5 = wx.BoxSizer(wx.HORIZONTAL)
        Row5.Add(Lbl5, 0, wx.EXPAND)
        Row5.Add(Itm5, 0, wx.EXPAND)
        Row6 = wx.BoxSizer(wx.HORIZONTAL)
        Row6.Add(Lbl6, 0, wx.EXPAND)
        Row6.Add(Itm6, 0, wx.EXPAND)
        Row7 = wx.BoxSizer(wx.HORIZONTAL)
        Row7.Add(Lbl7, 0, wx.EXPAND)
        Row7.Add(Itm7, 0, wx.EXPAND)
        Row8 = wx.BoxSizer(wx.HORIZONTAL)
        Row8.Add(Lbl8, 0, wx.EXPAND)
        Row8.Add(Itm8, 0, wx.EXPAND)
        Row9 = wx.BoxSizer(wx.HORIZONTAL)
        Row9.Add(Lbl9, 0, wx.EXPAND)
        Row9.Add(Itm9, 0, wx.EXPAND)
        Row10 = wx.BoxSizer(wx.HORIZONTAL)
        Row10.Add(Lbl10, 0, wx.EXPAND)
        Row10.Add(Itm10, 0, wx.EXPAND)
        Row13 = wx.BoxSizer(wx.HORIZONTAL)
        Row13.Add(Lbl13, 0, wx.EXPAND)
        Row13.Add(Itm13, 0, wx.EXPAND)

        popupSizer.Add(Row1, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row2, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row11, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row12, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row3, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row4, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row5, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row6, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row7, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row8, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row9, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row10, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Row13, 0, wx.ALL | wx.EXPAND, 5)

        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()





# =============================
# =============================
# ====  Help popup dialog  ====
# =============================
# =============================


class HelpDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        fontTitle = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        fontItem = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        popupSizer = wx.BoxSizer(wx.VERTICAL)

        Lbl1 = wx.StaticText(self, label='A device is installed: ')
        Itm1 = wx.StaticText(self, label='Search for the device by serial number and transfer to station. Indicate the install date.')

        Lbl2 = wx.StaticText(self, label='A device is removed: ')
        Itm2 = wx.StaticText(self, label='Transfer the device to the appropriate warehouse, set status and deployment status.')

        Lbl3 = wx.StaticText(self, label='A change to a device is required: ')
        Itm3 = wx.StaticText(self, label='Make the change to the device and set the effective date appropriately with a remark.')
        
        Lbl4 = wx.StaticText(self, label='Device at station not listed here: ')
        Itm4 = wx.StaticText(self, label='Search by serial number and transfer to station; if not found, add as new device.')

        Lbl5 = wx.StaticText(self, label='Device listed here not at station: ')
        Itm5 = wx.StaticText(self, label='Transfer to known warehouse; if unknown, set inactive with remark "location unknown".')

        Lbl6 = wx.StaticText(self, label='Communication device types: ')
        # Text field needed to allow for copy/paste
        Itm6 = wx.TextCtrl(self, size=(-1, 82), value='CAMERA - IP OR PDT\n\
EXTERNAL MODEM\n\
IMAGE VELOCIMETRY CAMERA SYSTEM\n\
NETWORK - CELL IP\n\
SATELLITE - GOES - HDR', style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL)
        Itm6.SetBackgroundColour((225, 225, 225))

        Lbl1.SetFont(fontTitle)
        Lbl2.SetFont(fontTitle)
        Lbl3.SetFont(fontTitle)
        Lbl4.SetFont(fontTitle)
        Lbl5.SetFont(fontTitle)
        Lbl6.SetFont(fontTitle)

        # Wrapping text
        Itm1.Wrap(240)
        Itm2.Wrap(240)
        Itm3.Wrap(240)
        Itm4.Wrap(240)
        Itm5.Wrap(240)

        Itm1.SetFont(fontItem)
        Itm2.SetFont(fontItem)
        Itm3.SetFont(fontItem)
        Itm4.SetFont(fontItem)
        Itm5.SetFont(fontItem)

        popupSizer.Add(Lbl1, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Itm1, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Lbl2, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Itm2, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Lbl3, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Itm3, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Lbl4, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Itm4, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Lbl5, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Itm5, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Lbl6, 0, wx.ALL | wx.EXPAND, 5)
        popupSizer.Add(Itm6, 0, wx.ALL | wx.EXPAND, 5)

        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        popupSizer.Add(buttonsSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(popupSizer)
        self.CenterOnScreen()





# ==========================
# ==========================
# ====  Custom classes  ====
# ==========================
# ==========================


class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

#----------------------------------------------------------------------
# This class is used to provide an interface between a ComboCtrl and the
# ListCtrl that is used as the popoup for the combo widget.

class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""

class ListCtrlComboPopup(wx.ComboPopup):

    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None

    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)





# ======================================
# ======================================
# ====  Inventory management panel  ====
# ======================================
# ======================================


class InventoryManagementPanel(wx.Panel):

    def __init__(self, mode, dir, *args, **kwargs):
        super(InventoryManagementPanel, self).__init__(*args, **kwargs)

        # List of keys for what to display for the print display
        # This is ordered differently than the table display
        self.keysList = ['Station ID',
                         'Status',
                         'Deployment Status',
                         'Category',
                         'Make',
                         'Model',
                         'Serial Number',
                         'Firmware Version',
                         'Installation Date',
                         'Effective Date',
                         'Remark']


        # The different communication devices and their corresponding column names
        self.commTypes = {
            'CAMERA - IP OR PDT': ['IP or PDT Address'],
            'EXTERNAL MODEM': [
                'Baud Rate',
                'Parity',
                'Telephone Number'
            ],
            'IMAGE VELOCIMETRY CAMERA SYSTEM': ['IP or PDT Address'],
            #'LOGGER': [], # For now loggers aren't considered, when they are the fields are likely the same as the external modem
            'NETWORK - CELL IP': ['IP or PDT Address'],
            'SATELLITE - GOES - HDR': [
                'IP or PDT Address',
                'XMT Rate',
                'XMT Window',
                'XMT Period',
                'First XMT',
                'Prime Channel',
                'Transmission Frequency']
        }

        # Labels for header
        self.inventoryManageLbl = "Inventory Management"
        self.helpBtnLbl = "Help"
        self.resetBtnLbl = "Reset Tables"
        self.exportBtnLbl = "Export Changes"

        # Labels for table
        self.stationIDLbl = "Station ID"
        self.deviceStatusLbl = "Device Status"
        self.deviceCategoryLbl = "Device Category" 
        self.deviceMakeLbl = "Device Make"
        self.deviceModelLbl = "Device Model"
        self.serialNumberLbl = "Serial Number"
        self.firmwareLbl = "Firmware / Software"
        self.installationDateLbl = "Installation Date"
        self.effectiveDateLbl = "Effective Date"
        self.remarkLbl = "Remark"
        self.statusChangeLbl = "Status Change"
        self.deploymentStatusLbl = "Deployment Status"
        self.newRemarkLbl = "New Remark"

        # Labels for buttons
        self.transferDownBtnLbl = "Transfer Device"
        self.transferUpBtnLbl = "Transfer Device to Station"
        self.populateBottomBtmLbl = "Search"
        self.clearBottomBtmLbl = "Clear"
        self.categoryBtnLbl = "Set Communication Details"

        # Options for dropdowns
        self.statusChangeOptions = ['N/A', 'ACTIVE', 'INACTIVE', 'REMOVED/TRANSFERRED']
        self.deploymentStatusOptions = ['DEPLOYABLE', 'NON-DEPLOYABLE', 'DESTROYED']

        # Comments label
        self.commentsLbl = 'Comments'
        
        # Directory location
        self.dir = dir

        # Count for the table rows
        self.entryNumTop = 0
        self.entryNumBottom = 0
        
        # Sizes
        self.colHeaderHeight = 60
        self.colHeaderWidth = 48
        self.rowHeight = 30

        self.manager = None
        self.mode = mode

        # The station populated in the top table
        self.topStation = ''


        '''
        The top_table_dataframe, bottom_table_dataframe, and bottom_storage_dataframe are used as storage
        for the saved states from the tables (columns shown in the tables) as well as details from popups (communication device popups)
        They are created by copying from the hydex devices report, including all columns there, most of which are unused
        When stations are transferred to warehouses or other stations, many columns specific to stations in the dataframes remain unchanged
        These include Station Name, Latitude, Longitude, etc.
        When viewing these dataframes, it may look like a discrepancy or error when the Station ID does not match other station data
        However this is not an issue as this data is not being considered and is redundant, and so can remain unmatching
        '''

        # Dataframes for storage
        self.full_hydex_dataframe = pd.DataFrame()
        self.top_table_dataframe = pd.DataFrame()
        self.bottom_table_dataframe = pd.DataFrame()
        self.bottom_storage_dataframe = pd.DataFrame()

        # Set the values of the dataframes
        hydex_reports = glob(self.dir + '\\AQ_Extracted_Data\\hydex_current_status_entire_network_devices_*.csv')
        if len(hydex_reports) > 0:

            # Populating the data from the report
            self.full_hydex_dataframe = pd.read_csv(hydex_reports[0])
            # Set an index value for each row
            self.full_hydex_dataframe['dataset_index_marker'] = self.full_hydex_dataframe.index
            # Remove nan values
            self.full_hydex_dataframe = self.full_hydex_dataframe.fillna('')

            # Set the columns of the blank dataframes
            self.top_table_dataframe = pd.DataFrame(columns=self.full_hydex_dataframe.columns.values.tolist())
            self.bottom_table_dataframe = pd.DataFrame(columns=self.full_hydex_dataframe.columns.values.tolist())
            self.bottom_storage_dataframe = pd.DataFrame(columns=self.full_hydex_dataframe.columns.values.tolist())

        self.InitUI()



    # --------------------
    # Initialize the panel
    # --------------------

    def InitUI(self):
        if self.mode == "DEBUG":
            print("InventoryManagementPanel")

        self.layoutSizer = wx.BoxSizer(wx.VERTICAL)

        #Setup scroll panel
        self.InvenScroll = scrolledpanel.ScrolledPanel(self, style=wx.SIMPLE_BORDER)
        self.InvenScroll.SetupScrolling(scrollIntoView=False)
        # self.InvenScroll.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        #Title
        self.titlePanel = wx.Panel(self.InvenScroll, style=wx.SIMPLE_BORDER)
        self.inventoryManageTxt = wx.StaticText(self.titlePanel, label=self.inventoryManageLbl, name="-1")
        self.inventoryManageTxt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.helpBtn = wx.Button(self.titlePanel, label=self.helpBtnLbl)
        self.helpBtn.Bind(wx.EVT_BUTTON, self.displayHelp)

        self.resetTabBtn = wx.Button(self.titlePanel, label=self.resetBtnLbl)
        #self.resetTabBtn.Bind(wx.EVT_BUTTON, self.printChangesOutputTesting)
        self.resetTabBtn.Bind(wx.EVT_BUTTON, self.OnReset)

        self.exportBtn = wx.Button(self.titlePanel, label=self.exportBtnLbl)
        self.exportBtn.Bind(wx.EVT_BUTTON, self.OnExport)

        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer.Add(self.inventoryManageTxt, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 130)
        titleSizer.Add(self.helpBtn, 0, wx.EXPAND|wx.ALL|wx.RIGHT, 5)
        titleSizer.Add(self.resetTabBtn, 0, wx.EXPAND|wx.ALL|wx.RIGHT, 5)
        titleSizer.Add(self.exportBtn, 0, wx.EXPAND|wx.ALL|wx.RIGHT, 5)

        self.titlePanel.SetSizer(titleSizer)

        #Sizer holds Title and Runs
        levelNotesSizer = wx.BoxSizer(wx.VERTICAL)

        self.splitter = wx.SplitterWindow(self.InvenScroll, style=wx.SP_3D|wx.SP_THIN_SASH|wx.SP_BORDER|wx.SP_NO_XP_THEME, size=(1, 410))

        #Panel parent to table
        # self.runTablePanel = scrolledpanel.ScrolledPanel(self.InvenScroll, style=wx.BORDER_NONE, size=(1, 120))
        self.runTablePanel = wx.Panel(self.splitter, style=wx.BORDER_NONE)


        runSizer = wx.BoxSizer(wx.VERTICAL)
        self.runTablePanel.SetSizer(runSizer)

        self.secondSplitPanel = wx.Panel(self.splitter)
        secondSplitSizer = wx.BoxSizer(wx.VERTICAL)
        self.secondSplitPanel.SetSizer(secondSplitSizer)

        bar = wx.Panel(self.secondSplitPanel, size=(1, 3))
        bar.SetBackgroundColour('green')


        buttonsBottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondSplitSizer.Add(bar, 0, wx.EXPAND)
        secondSplitSizer.Add(buttonsBottomSizer, 0, wx.EXPAND)

        

        # ################################
        # ################################
        # ###  Creating the top table  ###
        # ################################
        # ################################

        # Inventory Management Table (Top)
        self.invenManTopPanel = scrolledpanel.ScrolledPanel(self.runTablePanel, style=wx.BORDER_NONE)
        self.invenManTopPanel.SetupScrolling(scrollIntoView=False)
        self.invenManTopPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        self.invenManTopSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.invenManTopSizerV = wx.BoxSizer(wx.VERTICAL)


        # Entry Adding Column
        self.entryColumnSizer = wx.BoxSizer(wx.VERTICAL)

        entryColPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        wx.StaticText(entryColPanel, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.rowHeight, self.colHeaderHeight))


        # For dynamically added entries
        self.entryColButtonPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.entryColButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.entryColButtonPanel.SetSizer(self.entryColButtonSizer)


        # Add a default button
        name = "%s" % self.entryNumTop
        button = wx.Button(self.entryColButtonPanel, id=10101+self.entryNumTop, label="+", name=name, size=(self.rowHeight, self.rowHeight))
        self.entryNumTop += 1
        button.Bind(wx.EVT_BUTTON, self.OnAddPressTop)
        self.entryColButtonSizer.Add(button, 0, wx.EXPAND)

        self.entryColumnSizer.Add(entryColPanel, 0, wx.EXPAND)
        self.entryColumnSizer.Add(self.entryColButtonPanel, 0, wx.EXPAND)



        # Select Column
        self.selectTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        selectTopHeaderPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        selectTopHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        selectTopHeaderPanel.SetSizer(selectTopHeaderSizer)

        selectTopHeaderTxt = wx.StaticText(selectTopHeaderPanel, size=(15, self.colHeaderHeight))
        selectTopHeaderSizer.Add(selectTopHeaderTxt, 1, wx.EXPAND)

        # Create new panel and sizer for dynamic entries
        self.selectTopPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.selectTopSizer = wx.BoxSizer(wx.VERTICAL)
        self.selectTopPanel.SetSizer(self.selectTopSizer)

        self.selectTopColumnSizer.Add(selectTopHeaderPanel, 0, wx.EXPAND)
        self.selectTopColumnSizer.Add(self.selectTopPanel, 0, wx.EXPAND)



        #stationIDTop column
        self.stationIDTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        stationIDTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        stationIDTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        stationIDTopLabelPanel.SetSizer(stationIDTopLabelSizer)

        stationIDTopLabelTxt = wx.StaticText(stationIDTopLabelPanel, label=self.stationIDLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 15, self.colHeaderHeight))
        stationIDTopLabelSizer.Add(stationIDTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.stationIDTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.stationIDTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.stationIDTopValPanel.SetSizer(self.stationIDTopValSizer)

        #Add all to the Time
        self.stationIDTopColumnSizer.Add(stationIDTopLabelPanel, 0, wx.EXPAND)
        self.stationIDTopColumnSizer.Add(self.stationIDTopValPanel, 0, wx.EXPAND)



        #deviceStatusTop column
        self.deviceStatusTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceStatusTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        deviceStatusTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceStatusTopLabelPanel.SetSizer(deviceStatusTopLabelSizer)

        deviceStatusTopLabelTxt = wx.StaticText(deviceStatusTopLabelPanel, label=self.deviceStatusLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 25, self.colHeaderHeight))
        deviceStatusTopLabelSizer.Add(deviceStatusTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceStatusTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.deviceStatusTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceStatusTopValPanel.SetSizer(self.deviceStatusTopValSizer)

        #Add all to the Time
        self.deviceStatusTopColumnSizer.Add(deviceStatusTopLabelPanel, 0, wx.EXPAND)
        self.deviceStatusTopColumnSizer.Add(self.deviceStatusTopValPanel, 0, wx.EXPAND)



        #deviceCategoryTop column
        self.deviceCategoryTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceCategoryTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        deviceCategoryTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceCategoryTopLabelPanel.SetSizer(deviceCategoryTopLabelSizer)

        deviceCategoryTopLabelTxt = wx.StaticText(deviceCategoryTopLabelPanel, label=self.deviceCategoryLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        deviceCategoryTopLabelSizer.Add(deviceCategoryTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceCategoryTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.deviceCategoryTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceCategoryTopValPanel.SetSizer(self.deviceCategoryTopValSizer)

        #Add all to the Time
        self.deviceCategoryTopColumnSizer.Add(deviceCategoryTopLabelPanel, 0, wx.EXPAND)
        self.deviceCategoryTopColumnSizer.Add(self.deviceCategoryTopValPanel, 0, wx.EXPAND)



        #deviceMakeTop column
        self.deviceMakeTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceMakeTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        deviceMakeTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceMakeTopLabelPanel.SetSizer(deviceMakeTopLabelSizer)

        deviceMakeTopLabelTxt = wx.StaticText(deviceMakeTopLabelPanel, label=self.deviceMakeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        deviceMakeTopLabelSizer.Add(deviceMakeTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceMakeTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.deviceMakeTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceMakeTopValPanel.SetSizer(self.deviceMakeTopValSizer)

        #Add all to the Time
        self.deviceMakeTopColumnSizer.Add(deviceMakeTopLabelPanel, 0, wx.EXPAND)
        self.deviceMakeTopColumnSizer.Add(self.deviceMakeTopValPanel, 0, wx.EXPAND)



        #deviceModelTop column
        self.deviceModelTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceModelTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        deviceModelTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceModelTopLabelPanel.SetSizer(deviceModelTopLabelSizer)

        deviceModelTopLabelTxt = wx.StaticText(deviceModelTopLabelPanel, label=self.deviceModelLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        deviceModelTopLabelSizer.Add(deviceModelTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceModelTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.deviceModelTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceModelTopValPanel.SetSizer(self.deviceModelTopValSizer)

        #Add all to the Time
        self.deviceModelTopColumnSizer.Add(deviceModelTopLabelPanel, 0, wx.EXPAND)
        self.deviceModelTopColumnSizer.Add(self.deviceModelTopValPanel, 0, wx.EXPAND)



        #serialNumberTop column
        self.serialNumberTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        serialNumberTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        serialNumberTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        serialNumberTopLabelPanel.SetSizer(serialNumberTopLabelSizer)

        serialNumberTopLabelTxt = wx.StaticText(serialNumberTopLabelPanel, label=self.serialNumberLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 15, self.colHeaderHeight))
        serialNumberTopLabelSizer.Add(serialNumberTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.serialNumberTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.serialNumberTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.serialNumberTopValPanel.SetSizer(self.serialNumberTopValSizer)

        #Add all to the Time
        self.serialNumberTopColumnSizer.Add(serialNumberTopLabelPanel, 0, wx.EXPAND)
        self.serialNumberTopColumnSizer.Add(self.serialNumberTopValPanel, 0, wx.EXPAND)



        #firmwareTop column
        self.firmwareTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        firmwareTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        firmwareTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        firmwareTopLabelPanel.SetSizer(firmwareTopLabelSizer)

        firmwareTopLabelTxt = wx.StaticText(firmwareTopLabelPanel, label=self.firmwareLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 15, self.colHeaderHeight))
        firmwareTopLabelSizer.Add(firmwareTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.firmwareTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.firmwareTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.firmwareTopValPanel.SetSizer(self.firmwareTopValSizer)

        #Add all to the Time
        self.firmwareTopColumnSizer.Add(firmwareTopLabelPanel, 0, wx.EXPAND)
        self.firmwareTopColumnSizer.Add(self.firmwareTopValPanel, 0, wx.EXPAND)



        #installationDateTop column
        self.installationDateTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        installationDateTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        installationDateTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        installationDateTopLabelPanel.SetSizer(installationDateTopLabelSizer)

        installationDateTopLabelTxt = wx.StaticText(installationDateTopLabelPanel, label=self.installationDateLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 25, self.colHeaderHeight))
        installationDateTopLabelSizer.Add(installationDateTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.installationDateTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.installationDateTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.installationDateTopValPanel.SetSizer(self.installationDateTopValSizer)

        #Add all to the Time
        self.installationDateTopColumnSizer.Add(installationDateTopLabelPanel, 0, wx.EXPAND)
        self.installationDateTopColumnSizer.Add(self.installationDateTopValPanel, 0, wx.EXPAND)



        #effectiveDateTop column
        self.effectiveDateTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        effectiveDateTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        effectiveDateTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        effectiveDateTopLabelPanel.SetSizer(effectiveDateTopLabelSizer)

        effectiveDateTopLabelTxt = wx.StaticText(effectiveDateTopLabelPanel, label=self.effectiveDateLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 10, self.colHeaderHeight))
        effectiveDateTopLabelSizer.Add(effectiveDateTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.effectiveDateTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.effectiveDateTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.effectiveDateTopValPanel.SetSizer(self.effectiveDateTopValSizer)

        #Add all to the Time
        self.effectiveDateTopColumnSizer.Add(effectiveDateTopLabelPanel, 0, wx.EXPAND)
        self.effectiveDateTopColumnSizer.Add(self.effectiveDateTopValPanel, 0, wx.EXPAND)



        #remarkTop column
        self.remarkTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        remarkTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        remarkTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        remarkTopLabelPanel.SetSizer(remarkTopLabelSizer)

        remarkTopLabelTxt = wx.StaticText(remarkTopLabelPanel, label=self.remarkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 60, self.colHeaderHeight))
        remarkTopLabelSizer.Add(remarkTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.remarkTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.remarkTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.remarkTopValPanel.SetSizer(self.remarkTopValSizer)

        #Add all to the Time
        self.remarkTopColumnSizer.Add(remarkTopLabelPanel, 0, wx.EXPAND)
        self.remarkTopColumnSizer.Add(self.remarkTopValPanel, 0, wx.EXPAND)



        #statusChangeTop column
        self.statusChangeTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        statusChangeTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        statusChangeTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        statusChangeTopLabelPanel.SetSizer(statusChangeTopLabelSizer)

        statusChangeTopLabelTxt = wx.StaticText(statusChangeTopLabelPanel, label=self.statusChangeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 10, self.colHeaderHeight))
        statusChangeTopLabelSizer.Add(statusChangeTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.statusChangeTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.statusChangeTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.statusChangeTopValPanel.SetSizer(self.statusChangeTopValSizer)

        #Add all to the Time
        self.statusChangeTopColumnSizer.Add(statusChangeTopLabelPanel, 0, wx.EXPAND)
        self.statusChangeTopColumnSizer.Add(self.statusChangeTopValPanel, 0, wx.EXPAND)



        #deploymentStatusTop column
        self.deploymentStatusTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deploymentStatusTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        deploymentStatusTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deploymentStatusTopLabelPanel.SetSizer(deploymentStatusTopLabelSizer)

        deploymentStatusTopLabelTxt = wx.StaticText(deploymentStatusTopLabelPanel, label=self.deploymentStatusLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 25, self.colHeaderHeight))
        deploymentStatusTopLabelSizer.Add(deploymentStatusTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deploymentStatusTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.deploymentStatusTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deploymentStatusTopValPanel.SetSizer(self.deploymentStatusTopValSizer)

        #Add all to the Time
        self.deploymentStatusTopColumnSizer.Add(deploymentStatusTopLabelPanel, 0, wx.EXPAND)
        self.deploymentStatusTopColumnSizer.Add(self.deploymentStatusTopValPanel, 0, wx.EXPAND)



        #newRemarkTop column
        self.newRemarkTopColumnSizer = wx.BoxSizer(wx.VERTICAL)

        newRemarkTopLabelPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        newRemarkTopLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        newRemarkTopLabelPanel.SetSizer(newRemarkTopLabelSizer)

        newRemarkTopLabelTxt = wx.StaticText(newRemarkTopLabelPanel, label=self.newRemarkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 10, self.colHeaderHeight))
        newRemarkTopLabelSizer.Add(newRemarkTopLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.newRemarkTopValPanel = wx.Panel(self.invenManTopPanel, style=wx.SIMPLE_BORDER)
        self.newRemarkTopValSizer = wx.BoxSizer(wx.VERTICAL)
        self.newRemarkTopValPanel.SetSizer(self.newRemarkTopValSizer)

        #Add all to the Time
        self.newRemarkTopColumnSizer.Add(newRemarkTopLabelPanel, 0, wx.EXPAND)
        self.newRemarkTopColumnSizer.Add(self.newRemarkTopValPanel, 0, wx.EXPAND)

        

        #Add columns to table
        self.invenManTopSizerH.Add(self.entryColumnSizer, 0, wx.EXPAND)
        self.invenManTopSizerH.Add(self.selectTopColumnSizer, 0, wx.EXPAND)
        self.invenManTopSizerH.Add(self.stationIDTopColumnSizer, 0, wx.EXPAND)
        self.invenManTopSizerH.Add(self.deviceStatusTopColumnSizer, 0, wx.EXPAND)
        self.invenManTopSizerH.Add(self.deviceCategoryTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.deviceMakeTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.deviceModelTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.serialNumberTopColumnSizer, 0, wx.EXPAND)
        self.invenManTopSizerH.Add(self.firmwareTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.installationDateTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.effectiveDateTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.remarkTopColumnSizer, 2, wx.EXPAND)
        self.invenManTopSizerH.Add(self.statusChangeTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.deploymentStatusTopColumnSizer, 1, wx.EXPAND)
        self.invenManTopSizerH.Add(self.newRemarkTopColumnSizer, 2, wx.EXPAND)

        self.invenManTopSizerV.Add(self.invenManTopSizerH, 1, wx.EXPAND)
        self.invenManTopPanel.SetSizer(self.invenManTopSizerV)

        runSizer.Add(self.invenManTopPanel, 1, wx.EXPAND)


        
        # The top button
        buttonsTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        runSizer.Add(buttonsTopSizer, 0, wx.EXPAND)

        self.transferTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsTopSizer.Add(self.transferTopSizer, 5, wx.EXPAND|wx.ALL, 5)

        #Adding category setting button
        setCategoryBtn = wx.Button(self.runTablePanel, label=self.categoryBtnLbl, size=(-1, 30))
        setCategoryBtn.Bind(wx.EVT_BUTTON, self.CategorySetPopups)

        #Adding transfer button to transferTopSizer
        transferTopBtn = wx.Button(self.runTablePanel, label=self.transferDownBtnLbl, size=(-1, 30))
        transferTopBtn.Bind(wx.EVT_BUTTON, self.OnTransferFromTopToBottom)

        self.transferTopSizer.Add(setCategoryBtn, 0, wx.EXPAND|wx.ALL, 5)
        self.transferTopSizer.Add((-1, -1), 1, wx.EXPAND)
        self.transferTopSizer.Add(transferTopBtn, 0, wx.EXPAND|wx.ALL|wx.RIGHT, 5)





        # ###################################
        # ###################################
        # ###  Creating the bottom table  ###
        # ###################################
        # ###################################

        # The bottom buttons and similar
        self.transferBottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsBottomSizer.Add(self.transferBottomSizer, 5, wx.EXPAND|wx.ALL, 5)
        
        # Station text field
        stationTxtPanel = wx.Panel(self.secondSplitPanel, style=wx.SUNKEN_BORDER, size=(75, -1))
        self.stationTextCtrl = wx.TextCtrl(stationTxtPanel, style=wx.TE_PROCESS_ENTER)
        self.stationTextCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        self.stationTextCtrl.SetHint("Station ID")
        stationTxtSizer = wx.BoxSizer(wx.VERTICAL)
        stationTxtSizer.Add(self.stationTextCtrl, 1, wx.EXPAND)
        stationTxtPanel.SetSizer(stationTxtSizer)

        # Category text field
        categoryTxtPanel = wx.Panel(self.secondSplitPanel, style=wx.SUNKEN_BORDER, size=(90, -1))
        self.categoryTextCtrl = wx.TextCtrl(categoryTxtPanel, style=wx.TE_PROCESS_ENTER)
        self.categoryTextCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        self.categoryTextCtrl.SetHint("Category")
        categoryTxtSizer = wx.BoxSizer(wx.VERTICAL)
        categoryTxtSizer.Add(self.categoryTextCtrl, 1, wx.EXPAND)
        categoryTxtPanel.SetSizer(categoryTxtSizer)

        # Make text field
        makeTxtPanel = wx.Panel(self.secondSplitPanel, style=wx.SUNKEN_BORDER, size=(90, -1))
        self.makeTextCtrl = wx.TextCtrl(makeTxtPanel, style=wx.TE_PROCESS_ENTER)
        self.makeTextCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        self.makeTextCtrl.SetHint("Make")
        makeTxtSizer = wx.BoxSizer(wx.VERTICAL)
        makeTxtSizer.Add(self.makeTextCtrl, 1, wx.EXPAND)
        makeTxtPanel.SetSizer(makeTxtSizer)

        # Model text field
        modelTxtPanel = wx.Panel(self.secondSplitPanel, style=wx.SUNKEN_BORDER, size=(70, -1))
        self.modelTextCtrl = wx.TextCtrl(modelTxtPanel, style=wx.TE_PROCESS_ENTER)
        self.modelTextCtrl.Bind(wx.EVT_TEXT, self.OnTextType)
        self.modelTextCtrl.SetHint("Model")
        modelTxtSizer = wx.BoxSizer(wx.VERTICAL)
        modelTxtSizer.Add(self.modelTextCtrl, 1, wx.EXPAND)
        modelTxtPanel.SetSizer(modelTxtSizer)

        # Serial number text field
        serialNumTxtPanel = wx.Panel(self.secondSplitPanel, style=wx.SUNKEN_BORDER, size=(100, -1))
        self.serialNumTextCtrl = wx.TextCtrl(serialNumTxtPanel, style=wx.TE_PROCESS_ENTER)
        self.serialNumTextCtrl.SetHint("Serial Number")
        serialNumTxtSizer = wx.BoxSizer(wx.VERTICAL)
        serialNumTxtSizer.Add(self.serialNumTextCtrl, 1, wx.EXPAND)
        serialNumTxtPanel.SetSizer(serialNumTxtSizer)

        # Search button
        self.populateTableBtn = wx.Button(self.secondSplitPanel, label=self.populateBottomBtmLbl)
        self.populateTableBtn.Bind(wx.EVT_BUTTON, self.populateBottomTable)

        # Clear button
        self.clearTableBtn = wx.Button(self.secondSplitPanel, label=self.clearBottomBtmLbl)
        self.clearTableBtn.Bind(wx.EVT_BUTTON, self.clearBottomTable)

        #Adding transfer button to transferBottomSizer
        transferBottomBtn = wx.Button(self.secondSplitPanel, label=self.transferUpBtnLbl, size=(-1, 30))
        transferBottomBtn.Bind(wx.EVT_BUTTON, self.OnTransferFromBottomToTop)

        self.transferBottomSizer.Add(stationTxtPanel, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add(categoryTxtPanel, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add(makeTxtPanel, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add(modelTxtPanel, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add(serialNumTxtPanel, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add(self.populateTableBtn, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add(self.clearTableBtn, 0, wx.EXPAND|wx.ALL, 5)
        self.transferBottomSizer.Add((-1, -1), 1, wx.EXPAND)
        self.transferBottomSizer.Add(transferBottomBtn, 0, wx.EXPAND|wx.ALL|wx.RIGHT, 5)



        # Inventory Management Table (bottom)
        self.invenManBottomPanel = scrolledpanel.ScrolledPanel(self.secondSplitPanel, style=wx.BORDER_NONE)
        self.invenManBottomPanel.SetupScrolling(scrollIntoView=False)
        self.invenManBottomPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

        self.invenManBottomSizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.invenManBottomSizerV = wx.BoxSizer(wx.VERTICAL)

        # Add this just to keek the numbering consistent between top and bottom
        self.entryNumBottom += 1



        # Select Column
        self.selectBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        selectBottomHeaderPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        selectBottomHeaderSizer = wx.BoxSizer(wx.HORIZONTAL)
        selectBottomHeaderPanel.SetSizer(selectBottomHeaderSizer)

        selectBottomHeaderTxt = wx.StaticText(selectBottomHeaderPanel, size=(15, self.colHeaderHeight))
        selectBottomHeaderSizer.Add(selectBottomHeaderTxt, 1, wx.EXPAND)

        # Create new panel and sizer for dynamic entries
        self.selectBottomPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.selectBottomSizer = wx.BoxSizer(wx.VERTICAL)
        self.selectBottomPanel.SetSizer(self.selectBottomSizer)

        self.selectBottomColumnSizer.Add(selectBottomHeaderPanel, 0, wx.EXPAND)
        self.selectBottomColumnSizer.Add(self.selectBottomPanel, 0, wx.EXPAND)



        #stationIDBottom column
        self.stationIDBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        stationIDBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        stationIDBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        stationIDBottomLabelPanel.SetSizer(stationIDBottomLabelSizer)

        stationIDBottomLabelTxt = wx.StaticText(stationIDBottomLabelPanel, label=self.stationIDLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 15, self.colHeaderHeight))
        stationIDBottomLabelSizer.Add(stationIDBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.stationIDBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.stationIDBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.stationIDBottomValPanel.SetSizer(self.stationIDBottomValSizer)

        #Add all to the Time
        self.stationIDBottomColumnSizer.Add(stationIDBottomLabelPanel, 0, wx.EXPAND)
        self.stationIDBottomColumnSizer.Add(self.stationIDBottomValPanel, 0, wx.EXPAND)



        #deviceStatusBottom column
        self.deviceStatusBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceStatusBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        deviceStatusBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceStatusBottomLabelPanel.SetSizer(deviceStatusBottomLabelSizer)

        deviceStatusBottomLabelTxt = wx.StaticText(deviceStatusBottomLabelPanel, label=self.deviceStatusLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 25, self.colHeaderHeight))
        deviceStatusBottomLabelSizer.Add(deviceStatusBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceStatusBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.deviceStatusBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceStatusBottomValPanel.SetSizer(self.deviceStatusBottomValSizer)

        #Add all to the Time
        self.deviceStatusBottomColumnSizer.Add(deviceStatusBottomLabelPanel, 0, wx.EXPAND)
        self.deviceStatusBottomColumnSizer.Add(self.deviceStatusBottomValPanel, 0, wx.EXPAND)



        #deviceCategoryBottom column
        self.deviceCategoryBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceCategoryBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        deviceCategoryBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceCategoryBottomLabelPanel.SetSizer(deviceCategoryBottomLabelSizer)

        deviceCategoryBottomLabelTxt = wx.StaticText(deviceCategoryBottomLabelPanel, label=self.deviceCategoryLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        deviceCategoryBottomLabelSizer.Add(deviceCategoryBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceCategoryBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.deviceCategoryBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceCategoryBottomValPanel.SetSizer(self.deviceCategoryBottomValSizer)

        #Add all to the Time
        self.deviceCategoryBottomColumnSizer.Add(deviceCategoryBottomLabelPanel, 0, wx.EXPAND)
        self.deviceCategoryBottomColumnSizer.Add(self.deviceCategoryBottomValPanel, 0, wx.EXPAND)



        #deviceMakeBottom column
        self.deviceMakeBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceMakeBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        deviceMakeBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceMakeBottomLabelPanel.SetSizer(deviceMakeBottomLabelSizer)

        deviceMakeBottomLabelTxt = wx.StaticText(deviceMakeBottomLabelPanel, label=self.deviceMakeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        deviceMakeBottomLabelSizer.Add(deviceMakeBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceMakeBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.deviceMakeBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceMakeBottomValPanel.SetSizer(self.deviceMakeBottomValSizer)

        #Add all to the Time
        self.deviceMakeBottomColumnSizer.Add(deviceMakeBottomLabelPanel, 0, wx.EXPAND)
        self.deviceMakeBottomColumnSizer.Add(self.deviceMakeBottomValPanel, 0, wx.EXPAND)



        #deviceModelBottom column
        self.deviceModelBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deviceModelBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        deviceModelBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceModelBottomLabelPanel.SetSizer(deviceModelBottomLabelSizer)

        deviceModelBottomLabelTxt = wx.StaticText(deviceModelBottomLabelPanel, label=self.deviceModelLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 20, self.colHeaderHeight))
        deviceModelBottomLabelSizer.Add(deviceModelBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deviceModelBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.deviceModelBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deviceModelBottomValPanel.SetSizer(self.deviceModelBottomValSizer)

        #Add all to the Time
        self.deviceModelBottomColumnSizer.Add(deviceModelBottomLabelPanel, 0, wx.EXPAND)
        self.deviceModelBottomColumnSizer.Add(self.deviceModelBottomValPanel, 0, wx.EXPAND)



        #serialNumberBottom column
        self.serialNumberBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        serialNumberBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        serialNumberBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        serialNumberBottomLabelPanel.SetSizer(serialNumberBottomLabelSizer)

        serialNumberBottomLabelTxt = wx.StaticText(serialNumberBottomLabelPanel, label=self.serialNumberLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 15, self.colHeaderHeight))
        serialNumberBottomLabelSizer.Add(serialNumberBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.serialNumberBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.serialNumberBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.serialNumberBottomValPanel.SetSizer(self.serialNumberBottomValSizer)

        #Add all to the Time
        self.serialNumberBottomColumnSizer.Add(serialNumberBottomLabelPanel, 0, wx.EXPAND)
        self.serialNumberBottomColumnSizer.Add(self.serialNumberBottomValPanel, 0, wx.EXPAND)



        #firmwareBottom column
        self.firmwareBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        firmwareBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        firmwareBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        firmwareBottomLabelPanel.SetSizer(firmwareBottomLabelSizer)

        firmwareBottomLabelTxt = wx.StaticText(firmwareBottomLabelPanel, label=self.firmwareLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 15, self.colHeaderHeight))
        firmwareBottomLabelSizer.Add(firmwareBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.firmwareBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.firmwareBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.firmwareBottomValPanel.SetSizer(self.firmwareBottomValSizer)

        #Add all to the Time
        self.firmwareBottomColumnSizer.Add(firmwareBottomLabelPanel, 0, wx.EXPAND)
        self.firmwareBottomColumnSizer.Add(self.firmwareBottomValPanel, 0, wx.EXPAND)



        #installationDateBottom column
        self.installationDateBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        installationDateBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        installationDateBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        installationDateBottomLabelPanel.SetSizer(installationDateBottomLabelSizer)

        installationDateBottomLabelTxt = wx.StaticText(installationDateBottomLabelPanel, label=self.installationDateLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 25, self.colHeaderHeight))
        installationDateBottomLabelSizer.Add(installationDateBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.installationDateBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.installationDateBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.installationDateBottomValPanel.SetSizer(self.installationDateBottomValSizer)

        #Add all to the Time
        self.installationDateBottomColumnSizer.Add(installationDateBottomLabelPanel, 0, wx.EXPAND)
        self.installationDateBottomColumnSizer.Add(self.installationDateBottomValPanel, 0, wx.EXPAND)



        #effectiveDateBottom column
        self.effectiveDateBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        effectiveDateBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        effectiveDateBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        effectiveDateBottomLabelPanel.SetSizer(effectiveDateBottomLabelSizer)

        effectiveDateBottomLabelTxt = wx.StaticText(effectiveDateBottomLabelPanel, label=self.effectiveDateLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 10, self.colHeaderHeight))
        effectiveDateBottomLabelSizer.Add(effectiveDateBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.effectiveDateBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.effectiveDateBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.effectiveDateBottomValPanel.SetSizer(self.effectiveDateBottomValSizer)

        #Add all to the Time
        self.effectiveDateBottomColumnSizer.Add(effectiveDateBottomLabelPanel, 0, wx.EXPAND)
        self.effectiveDateBottomColumnSizer.Add(self.effectiveDateBottomValPanel, 0, wx.EXPAND)



        #remarkBottom column
        self.remarkBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        remarkBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        remarkBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        remarkBottomLabelPanel.SetSizer(remarkBottomLabelSizer)

        remarkBottomLabelTxt = wx.StaticText(remarkBottomLabelPanel, label=self.remarkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 60, self.colHeaderHeight))
        remarkBottomLabelSizer.Add(remarkBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.remarkBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.remarkBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.remarkBottomValPanel.SetSizer(self.remarkBottomValSizer)

        #Add all to the Time
        self.remarkBottomColumnSizer.Add(remarkBottomLabelPanel, 0, wx.EXPAND)
        self.remarkBottomColumnSizer.Add(self.remarkBottomValPanel, 0, wx.EXPAND)



        #statusChangeBottom column
        self.statusChangeBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        statusChangeBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        statusChangeBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        statusChangeBottomLabelPanel.SetSizer(statusChangeBottomLabelSizer)

        statusChangeBottomLabelTxt = wx.StaticText(statusChangeBottomLabelPanel, label=self.statusChangeLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 10, self.colHeaderHeight))
        statusChangeBottomLabelSizer.Add(statusChangeBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.statusChangeBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.statusChangeBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.statusChangeBottomValPanel.SetSizer(self.statusChangeBottomValSizer)

        #Add all to the Time
        self.statusChangeBottomColumnSizer.Add(statusChangeBottomLabelPanel, 0, wx.EXPAND)
        self.statusChangeBottomColumnSizer.Add(self.statusChangeBottomValPanel, 0, wx.EXPAND)



        #deploymentStatusBottom column
        self.deploymentStatusBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        deploymentStatusBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        deploymentStatusBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        deploymentStatusBottomLabelPanel.SetSizer(deploymentStatusBottomLabelSizer)

        deploymentStatusBottomLabelTxt = wx.StaticText(deploymentStatusBottomLabelPanel, label=self.deploymentStatusLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 25, self.colHeaderHeight))
        deploymentStatusBottomLabelSizer.Add(deploymentStatusBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.deploymentStatusBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.deploymentStatusBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.deploymentStatusBottomValPanel.SetSizer(self.deploymentStatusBottomValSizer)

        #Add all to the Time
        self.deploymentStatusBottomColumnSizer.Add(deploymentStatusBottomLabelPanel, 0, wx.EXPAND)
        self.deploymentStatusBottomColumnSizer.Add(self.deploymentStatusBottomValPanel, 0, wx.EXPAND)



        #newRemarkBottom column
        self.newRemarkBottomColumnSizer = wx.BoxSizer(wx.VERTICAL)

        newRemarkBottomLabelPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        newRemarkBottomLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        newRemarkBottomLabelPanel.SetSizer(newRemarkBottomLabelSizer)

        newRemarkBottomLabelTxt = wx.StaticText(newRemarkBottomLabelPanel, label=self.newRemarkLbl, style=wx.ALIGN_CENTRE_HORIZONTAL, size=(self.colHeaderWidth + 10, self.colHeaderHeight))
        newRemarkBottomLabelSizer.Add(newRemarkBottomLabelTxt, 1, wx.EXPAND)

        #Create new panel and sizer for dynamic entries
        self.newRemarkBottomValPanel = wx.Panel(self.invenManBottomPanel, style=wx.SIMPLE_BORDER)
        self.newRemarkBottomValSizer = wx.BoxSizer(wx.VERTICAL)
        self.newRemarkBottomValPanel.SetSizer(self.newRemarkBottomValSizer)

        #Add all to the Time
        self.newRemarkBottomColumnSizer.Add(newRemarkBottomLabelPanel, 0, wx.EXPAND)
        self.newRemarkBottomColumnSizer.Add(self.newRemarkBottomValPanel, 0, wx.EXPAND)

        

        #Add columns to table
        self.invenManBottomSizerH.Add(self.selectBottomColumnSizer, 0, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.stationIDBottomColumnSizer, 0, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.deviceStatusBottomColumnSizer, 0, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.deviceCategoryBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.deviceMakeBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.deviceModelBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.serialNumberBottomColumnSizer, 0, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.firmwareBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.installationDateBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.effectiveDateBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.remarkBottomColumnSizer, 2, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.statusChangeBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.deploymentStatusBottomColumnSizer, 1, wx.EXPAND)
        self.invenManBottomSizerH.Add(self.newRemarkBottomColumnSizer, 2, wx.EXPAND)

        self.invenManBottomSizerV.Add(self.invenManBottomSizerH, 1, wx.EXPAND)
        self.invenManBottomPanel.SetSizer(self.invenManBottomSizerV)



        #comments
        commentsPanel = wx.Panel(self.InvenScroll, style=wx.BORDER_NONE, size=(-1, 75))
        commentsSizer = wx.BoxSizer(wx.HORIZONTAL)
        commentsPanel.SetSizer(commentsSizer)

        commentsTxt = wx.StaticText(commentsPanel, label=self.commentsLbl, style=wx.ALIGN_CENTRE_HORIZONTAL)
        commentsSizer.Add(commentsTxt, 0, wx.EXPAND|wx.LEFT, 5)

        self.commentsCtrl = wx.TextCtrl(commentsPanel, style=wx.TE_MULTILINE|wx.TE_BESTWRAP)
        commentsSizer.Add(self.commentsCtrl, 1, wx.EXPAND|wx.ALL, 5)



        secondSplitSizer.Add(self.invenManBottomPanel, 1, wx.EXPAND)

        self.splitter.SplitHorizontally(self.runTablePanel, self.secondSplitPanel, 280)
        self.splitter.SetMinimumPaneSize(2)



        #Add to the Bigger Sizer
        levelNotesSizer.Add(self.titlePanel, 0, wx.EXPAND)
        levelNotesSizer.Add(self.splitter, 1, wx.EXPAND)
        levelNotesSizer.Add((-1, 10), 0, wx.EXPAND)
        levelNotesSizer.Add(commentsPanel, 0, wx.EXPAND)
        levelNotesSizer.Add((-1, 5), 0, wx.EXPAND)


        self.InvenScroll.SetSizer(levelNotesSizer)

        self.layoutSizer.Add(self.InvenScroll, 1, wx.EXPAND)
        self.SetSizer(self.layoutSizer)

        # Update and refresh
        runSizer.Layout()
        levelNotesSizer.Layout()
        self.layoutSizer.Layout()
        self.Update()
        self.Refresh()





    # ====================================
    # ====================================
    # ====  Delete and add functions  ====
    # ====================================
    # ====================================


    # On '+' button click, add a new entry into the top table
    # Only for the top table as there no longer is a + button option in the bottom table
    def OnAddPressTop(self, e):
        if self.mode == "DEBUG":
            print("add")
        
        if self.top_table_dataframe.empty:
            dlg = wx.MessageDialog(self, "No Station selected above, please choose a station on the front page", 'Error', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
            return

        self.AddEntryTop(True)

        # Add an empty blank row to the dataframe for the top table
        # Set the station ID and set the new index
        self.top_table_dataframe.loc[self.top_table_dataframe.shape[0]] = [""] * self.top_table_dataframe.shape[1]
        self.top_table_dataframe.at[self.top_table_dataframe.shape[0]-1, 'Station ID'] = self.topStation
        self.top_table_dataframe.at[self.top_table_dataframe.shape[0]-1, 'dataset_index_marker'] = str(self.top_table_dataframe.shape[0]-1) + '_new'
        if self.mode == "DEBUG":
            print(self.top_table_dataframe)

        # Update and refresh
        self.invenManTopSizerV.Layout()
        self.invenManTopPanel.Layout()
        self.invenManTopPanel.Update()
        self.layoutSizer.Layout()
        #self.Layout()
        #self.Update()
        self.Refresh()

        # Get to the bottom of the scrollbar
        self.invenManTopPanel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
        max_scroll = self.invenManTopPanel.GetScrollRange(wx.VERTICAL)
        self.invenManTopPanel.Scroll(0, max_scroll)
        

    # When the '-' is clicked, remove that row
    def OnRemovePressTop(self, e):
        button = e.GetEventObject()
        index = int(button.GetName())
        if self.mode=="DEBUG":
            print("index %s" % index)
        dlg = wx.MessageDialog(self, "Do you want to remove the entry?", 'Remove',
                              wx.YES_NO | wx.ICON_QUESTION)

        res = dlg.ShowModal()
        if res == wx.ID_YES:
            dlg.Destroy()

        elif res == wx.ID_NO:
            dlg.Destroy()
            return

        else:
            dlg.Destroy()
            return
        
        self.RemoveEntryTop(index)

        # Remove the row from the dataframe for the top table
        if not self.top_table_dataframe.empty:
            self.top_table_dataframe = self.top_table_dataframe.drop(index)
            self.top_table_dataframe.reset_index(drop=True, inplace=True)
            if self.mode == "DEBUG":
                print(self.top_table_dataframe)

        # Update and refresh
        self.invenManTopSizerV.Layout()
        self.invenManTopPanel.Layout()
        self.invenManTopPanel.Update()
        self.layoutSizer.Layout()
        #self.Layout()
        #self.Update()
        self.Refresh()



    # Add a row to the top table that can then be populated with data
    # Add a new item in each of the column sizers
    # Set name based on entryNum
    # Name is used for deletion and ordering
    # add_minus_button indicates whether the row is an empty row for user entry or a full row to be populated
    def AddEntryTop(self, add_minus_button):
        name = "%s" % self.entryNumTop
        otherName = "%s" % (self.entryNumTop - 1)
        newButton = wx.Button(self.entryColButtonPanel, id=10101 + self.entryNumTop, label="+", name=name, size=(self.rowHeight, self.rowHeight))

        oldButton = self.entryColButtonSizer.GetItem(self.entryNumTop - 1).GetWindow()
        if add_minus_button:
            oldButton.SetLabel('-')
            oldButton.Bind(wx.EVT_BUTTON, self.OnRemovePressTop)
        else:
            oldButton.SetLabel('')
            oldButton.Disable()

        self.entryNumTop += 1
        newButton.Bind(wx.EVT_BUTTON, self.OnAddPressTop)
        self.entryColButtonSizer.Add(newButton, 0, wx.EXPAND)

        #select col
        selectCBTop = wx.CheckBox(self.selectTopPanel, name=otherName, size=(15,self.rowHeight))
        #selectCBTop.Bind(wx.EVT_CHECKBOX, self.OnDataCheckTop)
        self.selectTopSizer.Add(selectCBTop, 0, wx.EXPAND)

        #stationIDTop col
        if add_minus_button:
            stationIDTop = MyTextCtrl(self.stationIDTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            stationIDTop.Bind(wx.EVT_TEXT, self.OnTextType)
            self.stationIDTopValSizer.Add(stationIDTop, 0, wx.EXPAND)
            stationIDTop.SetValue(self.topStation)
        else:
            stationIDTop = MyTextCtrl(self.stationIDTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            stationIDTop.SetBackgroundColour((204,204,204))
            self.stationIDTopValSizer.Add(stationIDTop, 0, wx.EXPAND)

        #deviceStatusTop col
        if add_minus_button:
            deviceStatusTop = MyTextCtrl(self.deviceStatusTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceStatusTop.Bind(wx.EVT_TEXT, self.OnTextType)
            self.deviceStatusTopValSizer.Add(deviceStatusTop, 0, wx.EXPAND)
        else:
            deviceStatusTop = MyTextCtrl(self.deviceStatusTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceStatusTop.SetBackgroundColour((204,204,204))
            self.deviceStatusTopValSizer.Add(deviceStatusTop, 0, wx.EXPAND)

        #deviceCategoryTop col
        if add_minus_button:
            deviceCategoryTop = MyTextCtrl(self.deviceCategoryTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceCategoryTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            deviceCategoryTop.Bind(wx.EVT_TEXT, self.OnTextType)
            self.deviceCategoryTopValSizer.Add(deviceCategoryTop, 0, wx.EXPAND)
        else:
            deviceCategoryTop = MyTextCtrl(self.deviceCategoryTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceCategoryTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            deviceCategoryTop.SetBackgroundColour((204,204,204))
            self.deviceCategoryTopValSizer.Add(deviceCategoryTop, 0, wx.EXPAND)

        #deviceMakeTop col
        if add_minus_button:
            deviceMakeTop = MyTextCtrl(self.deviceMakeTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceMakeTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            deviceMakeTop.Bind(wx.EVT_TEXT, self.OnTextType)
            self.deviceMakeTopValSizer.Add(deviceMakeTop, 0, wx.EXPAND)
        else:
            deviceMakeTop = MyTextCtrl(self.deviceMakeTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceMakeTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            deviceMakeTop.SetBackgroundColour((204,204,204))
            self.deviceMakeTopValSizer.Add(deviceMakeTop, 0, wx.EXPAND)

        #deviceModelTop col
        if add_minus_button:
            deviceModelTop = MyTextCtrl(self.deviceModelTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceModelTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            self.deviceModelTopValSizer.Add(deviceModelTop, 0, wx.EXPAND)
        else:
            deviceModelTop = MyTextCtrl(self.deviceModelTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            deviceModelTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            deviceModelTop.SetBackgroundColour((204,204,204))
            self.deviceModelTopValSizer.Add(deviceModelTop, 0, wx.EXPAND)

        #serialNumberTop col
        serialNumberTop = MyTextCtrl(self.serialNumberTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #serialNumberTop.Bind(wx.EVT_TEXT, self.OnTextEnterSerialNumberTop)
        serialNumberTop.Bind(wx.EVT_ENTER_WINDOW, self.warningTooltip)
        self.serialNumberTopValSizer.Add(serialNumberTop, 0, wx.EXPAND)

        #firmwareTop col
        firmwareTop = MyTextCtrl(self.firmwareTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #firmwareTop.Bind(wx.EVT_TEXT, self.OnTextEnterFirmwareTop)
        self.firmwareTopValSizer.Add(firmwareTop, 0, wx.EXPAND)

        #installationDateTop col
        installationDateTop = MyTextCtrl(self.installationDateTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #installationDateTop.Bind(wx.EVT_TEXT, self.OnTextEnterInstallationDateTop)
        self.installationDateTopValSizer.Add(installationDateTop, 0, wx.EXPAND)

        #effectiveDateTop col
        effectiveDateTop = MyTextCtrl(self.effectiveDateTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #effectiveDateTop.Bind(wx.EVT_TEXT, self.OnTextEnterEffectiveDateTop)
        self.effectiveDateTopValSizer.Add(effectiveDateTop, 0, wx.EXPAND)

        #remarkTop col
        if add_minus_button:
            remarkTop = MyTextCtrl(self.remarkTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            remarkTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            self.remarkTopValSizer.Add(remarkTop, 0, wx.EXPAND)
        else:
            remarkTop = MyTextCtrl(self.remarkTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
            remarkTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
            remarkTop.SetBackgroundColour((204,204,204))
            self.remarkTopValSizer.Add(remarkTop, 0, wx.EXPAND)

        #statusChangeTop col
        statusChangeTop = wx.ComboCtrl(self.statusChangeTopValPanel, style=wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        statusChangeTop.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        statusChangeTopCmboPopup = ListCtrlComboPopup()
        statusChangeTop.SetPopupControl(statusChangeTopCmboPopup)
        for option in self.statusChangeOptions:
            statusChangeTopCmboPopup.AddItem(option)
        statusChangeTop.SetPopupMinWidth(self.colHeaderWidth)
        statusChangeTop.SetPopupMaxHeight(85)
        statusChangeTop.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.SetDeploymentStatusTop)
        #statusChangeTop.Bind(wx.EVT_KILL_FOCUS, self.OnEnterValue)
        if add_minus_button:
            statusChangeTop.SetValue('')
            statusChangeTop.Disable()
        self.statusChangeTopValSizer.Add(statusChangeTop, 0, wx.EXPAND)

        #deploymentStatusTop col
        deploymentStatusTop = wx.ComboCtrl(self.deploymentStatusTopValPanel, style=wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        deploymentStatusTop.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        deploymentStatusTopCmboPopup = ListCtrlComboPopup()
        deploymentStatusTop.SetPopupControl(deploymentStatusTopCmboPopup)
        for option in self.deploymentStatusOptions:
            deploymentStatusTopCmboPopup.AddItem(option)
        deploymentStatusTop.SetPopupMinWidth(self.colHeaderWidth)
        deploymentStatusTop.SetPopupMaxHeight(85)
        #deploymentStatusTop.Bind(wx.EVT_KILL_FOCUS, self.OnEnterValue)
        if add_minus_button:
            deploymentStatusTop.SetValue('DEPLOYED')
            deploymentStatusTop.Disable()
        self.deploymentStatusTopValSizer.Add(deploymentStatusTop, 0, wx.EXPAND)

        #newRemarkTop col
        newRemarkTop = MyTextCtrl(self.newRemarkTopValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #newRemarkTop.Bind(wx.EVT_TEXT, self.OnTextEnterNewRemarkTop)
        newRemarkTop.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
        if add_minus_button:
            newRemarkTop.SetValue('')
            newRemarkTop.Disable()
        self.newRemarkTopValSizer.Add(newRemarkTop, 0, wx.EXPAND)

        if self.manager is not None:

            selectCBTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)

            stationIDTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceStatusTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceCategoryTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceMakeTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceModelTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            serialNumberTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            firmwareTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            installationDateTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            effectiveDateTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            remarkTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            statusChangeTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deploymentStatusTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            newRemarkTop.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)

            # self.layoutSizer.Layout()
            # print self.runTablePanel.GetSizer().GetItem(0).GetWindow().GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(0).GetWindow().GetSizer().GetItem(0).GetSizer().GetItem(0).GetSizer().GetItem(1).GetWindow().GetValue()
            # self.runTablePanel.GetSizer().Layout()



    # Add a row to the bottom table that can then be populated with data
    # Add a new item in each of the column sizers
    # Set name based on entryNum
    # Name is used for deletion and ordering
    def AddEntryBottom(self):
        otherName = "%s" % (self.entryNumBottom - 1)
        self.entryNumBottom += 1

        #select col
        selectCBBottom = wx.CheckBox(self.selectBottomPanel, name=otherName, size=(15,self.rowHeight))
        selectCBBottom.Bind(wx.EVT_CHECKBOX, self.OnDataCheckBottom)
        self.selectBottomSizer.Add(selectCBBottom, 0, wx.EXPAND)

        #stationIDBottom col
        stationIDBottom = MyTextCtrl(self.stationIDBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        stationIDBottom.SetBackgroundColour((204,204,204))
        self.stationIDBottomValSizer.Add(stationIDBottom, 0, wx.EXPAND)

        #deviceStatusBottom col
        deviceStatusBottom = MyTextCtrl(self.deviceStatusBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        deviceStatusBottom.SetBackgroundColour((204,204,204))
        self.deviceStatusBottomValSizer.Add(deviceStatusBottom, 0, wx.EXPAND)

        #deviceCategoryBottom col
        deviceCategoryBottom = MyTextCtrl(self.deviceCategoryBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        deviceCategoryBottom.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
        deviceCategoryBottom.SetBackgroundColour((204,204,204))
        self.deviceCategoryBottomValSizer.Add(deviceCategoryBottom, 0, wx.EXPAND)

        #deviceMakeBottom col
        deviceMakeBottom = MyTextCtrl(self.deviceMakeBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        deviceMakeBottom.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
        deviceMakeBottom.SetBackgroundColour((204,204,204))
        self.deviceMakeBottomValSizer.Add(deviceMakeBottom, 0, wx.EXPAND)

        #deviceModelBottom col
        deviceModelBottom = MyTextCtrl(self.deviceModelBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        deviceModelBottom.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
        deviceModelBottom.SetBackgroundColour((204,204,204))
        self.deviceModelBottomValSizer.Add(deviceModelBottom, 0, wx.EXPAND)

        #serialNumberBottom col
        serialNumberBottom = MyTextCtrl(self.serialNumberBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        serialNumberBottom.SetBackgroundColour((204,204,204))
        self.serialNumberBottomValSizer.Add(serialNumberBottom, 0, wx.EXPAND)

        #firmwareBottom col
        firmwareBottom = MyTextCtrl(self.firmwareBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        firmwareBottom.SetBackgroundColour((204,204,204))
        self.firmwareBottomValSizer.Add(firmwareBottom, 0, wx.EXPAND)

        #installationDateBottom col
        installationDateBottom = MyTextCtrl(self.installationDateBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        installationDateBottom.SetBackgroundColour((204,204,204))
        self.installationDateBottomValSizer.Add(installationDateBottom, 0, wx.EXPAND)

        #effectiveDateBottom col
        effectiveDateBottom = MyTextCtrl(self.effectiveDateBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        effectiveDateBottom.SetBackgroundColour((204,204,204))
        self.effectiveDateBottomValSizer.Add(effectiveDateBottom, 0, wx.EXPAND)

        #remarkBottom col
        remarkBottom = MyTextCtrl(self.remarkBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        remarkBottom.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
        remarkBottom.SetBackgroundColour((204,204,204))
        self.remarkBottomValSizer.Add(remarkBottom, 0, wx.EXPAND)

        #statusChangeBottom col
        #statusChangeBottom = wx.ComboCtrl(self.statusChangeBottomValPanel, style=wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #statusChangeBottom.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        #statusChangeBottomCmboPopup = ListCtrlComboPopup()
        #statusChangeBottom.SetPopupControl(statusChangeBottomCmboPopup)
        #for option in self.statusChangeOptions:
        #    statusChangeBottomCmboPopup.AddItem(option)
        #statusChangeBottom.SetPopupMinWidth(self.colHeaderWidth)
        #statusChangeBottom.SetPopupMaxHeight(65)
        #statusChangeBottom.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.SetDeploymentStatusBottom)
        ##statusChangeBottom.Bind(wx.EVT_KILL_FOCUS, self.OnEnterValue)
        #self.statusChangeBottomValSizer.Add(statusChangeBottom, 0, wx.EXPAND)
        statusChangeBottom = MyTextCtrl(self.statusChangeBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        self.statusChangeBottomValSizer.Add(statusChangeBottom, 0, wx.EXPAND)

        #deploymentStatusBottom col
        #deploymentStatusBottom = wx.ComboCtrl(self.deploymentStatusBottomValPanel, style=wx.TE_READONLY, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #deploymentStatusBottom.Bind(wx.EVT_MOUSEWHEEL, self.NoScrolling)
        #deploymentStatusBottomCmboPopup = ListCtrlComboPopup()
        #deploymentStatusBottom.SetPopupControl(deploymentStatusBottomCmboPopup)
        #for option in self.deploymentStatusOptions:
        #    deploymentStatusBottomCmboPopup.AddItem(option)
        #deploymentStatusBottom.SetPopupMinWidth(self.colHeaderWidth)
        #deploymentStatusBottom.SetPopupMaxHeight(65)
        ##deploymentStatusBottom.Bind(wx.EVT_KILL_FOCUS, self.OnEnterValue)
        #self.deploymentStatusBottomValSizer.Add(deploymentStatusBottom, 0, wx.EXPAND)
        deploymentStatusBottom = MyTextCtrl(self.deploymentStatusBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        self.deploymentStatusBottomValSizer.Add(deploymentStatusBottom, 0, wx.EXPAND)

        #newRemarkBottom col
        newRemarkBottom = MyTextCtrl(self.newRemarkBottomValPanel, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT, size=(self.colHeaderWidth, self.rowHeight), name=otherName)
        #newRemarkBottom.Bind(wx.EVT_KILL_FOCUS, self.OnEnterValue)
        newRemarkBottom.Bind(wx.EVT_ENTER_WINDOW, self.textTooltip)
        self.newRemarkBottomValSizer.Add(newRemarkBottom, 0, wx.EXPAND)

        if self.manager is not None:

            selectCBBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)

            stationIDBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceStatusBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceCategoryBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceMakeBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deviceModelBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            serialNumberBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            firmwareBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            installationDateBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            effectiveDateBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            remarkBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            statusChangeBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            deploymentStatusBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)
            newRemarkBottom.Bind(wx.EVT_KILL_FOCUS, self.manager.manager.gui.OnAutoSave)

            # self.layoutSizer.Layout()
            # print self.runTablePanel.GetSizer().GetItem(0).GetWindow().GetSizer().GetItem(1).GetWindow().GetSizer().GetItem(0).GetWindow().GetSizer().GetItem(0).GetSizer().GetItem(0).GetSizer().GetItem(1).GetWindow().GetValue()
            # self.runTablePanel.GetSizer().Layout()



    # Delete a row of the top table
    # Reorder the list of entries
    def RemoveEntryTop(self, index):
        if self.mode=="DEBUG":
            print("remove %s" % index)
        
        # THIS IS ONLY IN THE TOP VERSION
        self.entryColButtonSizer.Hide(index)
        self.entryColButtonSizer.Remove(index)
        self.entryNumTop -= 1

        #select col stuff
        self.selectTopSizer.Hide(index)
        self.selectTopSizer.Remove(index)

        #stationIDTop col stuff
        self.stationIDTopValSizer.Hide(index)
        self.stationIDTopValSizer.Remove(index)

        #deviceStatusTop col stuff
        self.deviceStatusTopValSizer.Hide(index)
        self.deviceStatusTopValSizer.Remove(index)

        #deviceCategoryTop col stuff
        self.deviceCategoryTopValSizer.Hide(index)
        self.deviceCategoryTopValSizer.Remove(index)

        #deviceMakeTop col stuff
        self.deviceMakeTopValSizer.Hide(index)
        self.deviceMakeTopValSizer.Remove(index)

        #deviceModelTop col stuff
        self.deviceModelTopValSizer.Hide(index)
        self.deviceModelTopValSizer.Remove(index)

        #serialNumberTop col stuff
        self.serialNumberTopValSizer.Hide(index)
        self.serialNumberTopValSizer.Remove(index)

        #firmwareTop col stuff
        self.firmwareTopValSizer.Hide(index)
        self.firmwareTopValSizer.Remove(index)

        #installationDateTop col stuff
        self.installationDateTopValSizer.Hide(index)
        self.installationDateTopValSizer.Remove(index)

        #effectiveDateTop col stuff
        self.effectiveDateTopValSizer.Hide(index)
        self.effectiveDateTopValSizer.Remove(index)

        #remarkTop col stuff
        self.remarkTopValSizer.Hide(index)
        self.remarkTopValSizer.Remove(index)

        #statusChangeTop col stuff
        self.statusChangeTopValSizer.Hide(index)
        self.statusChangeTopValSizer.Remove(index)

        #deploymentStatusTop col stuff
        self.deploymentStatusTopValSizer.Hide(index)
        self.deploymentStatusTopValSizer.Remove(index)

        #newRemarkTop col stuff
        self.newRemarkTopValSizer.Hide(index)
        self.newRemarkTopValSizer.Remove(index)
        
        for index, col in enumerate(self.invenManTopSizerH.GetChildren()):
            for rowIndex, child in enumerate(col.GetSizer().GetItem(1).GetWindow().GetSizer().GetChildren()):
                i = int(child.GetWindow().GetName())
                if i > rowIndex:
                    child.GetWindow().SetName("%s" % (i - 1))



    # Delete all the rows of the top table
    def RemoveFullTop(self):
        if self.mode=="DEBUG":
            print("remove full top")
        
        # THIS IS ONLY IN THE TOP VERSION
        self.entryColButtonSizer.Clear(delete_windows=True)

        # Add a default button back in (ONLY IN TOP)
        self.entryNumTop = 0
        name = "%s" % self.entryNumTop
        button = wx.Button(self.entryColButtonPanel, id=10101+self.entryNumTop, label="+", name=name, size=(self.rowHeight, self.rowHeight))
        button.Bind(wx.EVT_BUTTON, self.OnAddPressTop)
        self.entryColButtonSizer.Add(button, 0, wx.EXPAND)
        self.entryNumTop += 1

        #select col stuff
        self.selectTopSizer.Clear(delete_windows=True)

        #stationIDTop col stuff
        self.stationIDTopValSizer.Clear(delete_windows=True)

        #deviceStatusTop col stuff
        self.deviceStatusTopValSizer.Clear(delete_windows=True)

        #deviceCategoryTop col stuff
        self.deviceCategoryTopValSizer.Clear(delete_windows=True)

        #deviceMakeTop col stuff
        self.deviceMakeTopValSizer.Clear(delete_windows=True)

        #deviceModelTop col stuff
        self.deviceModelTopValSizer.Clear(delete_windows=True)

        #serialNumberTop col stuff
        self.serialNumberTopValSizer.Clear(delete_windows=True)

        #firmwareTop col stuff
        self.firmwareTopValSizer.Clear(delete_windows=True)

        #installationDateTop col stuff
        self.installationDateTopValSizer.Clear(delete_windows=True)

        #effectiveDateTop col stuff
        self.effectiveDateTopValSizer.Clear(delete_windows=True)

        #remarkTop col stuff
        self.remarkTopValSizer.Clear(delete_windows=True)

        #statusChangeTop col stuff
        self.statusChangeTopValSizer.Clear(delete_windows=True)

        #deploymentStatusTop col stuff
        self.deploymentStatusTopValSizer.Clear(delete_windows=True)

        #newRemarkTop col stuff
        self.newRemarkTopValSizer.Clear(delete_windows=True)

        self.invenManTopSizerV.Layout()
        self.invenManTopPanel.Layout()
        self.invenManTopPanel.Update()
        self.layoutSizer.Layout()
        self.Layout()
        self.Update()
        self.Refresh()
        self.invenManTopPanel.SetupScrolling(scrollIntoView=False)
        self.invenManTopPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)



    # Delete a row of the bottom table
    # Reorder the list of entries
    def RemoveEntryBottom(self, index):
        if self.mode=="DEBUG":
            print("remove %s" % index)

        self.entryNumBottom -= 1

        #select col stuff
        self.selectBottomSizer.Hide(index)
        self.selectBottomSizer.Remove(index)

        #stationIDBottom col stuff
        self.stationIDBottomValSizer.Hide(index)
        self.stationIDBottomValSizer.Remove(index)

        #deviceStatusBottom col stuff
        self.deviceStatusBottomValSizer.Hide(index)
        self.deviceStatusBottomValSizer.Remove(index)

        #deviceCategoryBottom col stuff
        self.deviceCategoryBottomValSizer.Hide(index)
        self.deviceCategoryBottomValSizer.Remove(index)

        #deviceMakeBottom col stuff
        self.deviceMakeBottomValSizer.Hide(index)
        self.deviceMakeBottomValSizer.Remove(index)

        #deviceModelBottom col stuff
        self.deviceModelBottomValSizer.Hide(index)
        self.deviceModelBottomValSizer.Remove(index)

        #serialNumberBottom col stuff
        self.serialNumberBottomValSizer.Hide(index)
        self.serialNumberBottomValSizer.Remove(index)

        #firmwareBottom col stuff
        self.firmwareBottomValSizer.Hide(index)
        self.firmwareBottomValSizer.Remove(index)

        #installationDateBottom col stuff
        self.installationDateBottomValSizer.Hide(index)
        self.installationDateBottomValSizer.Remove(index)

        #effectiveDateBottom col stuff
        self.effectiveDateBottomValSizer.Hide(index)
        self.effectiveDateBottomValSizer.Remove(index)

        #remarkBottom col stuff
        self.remarkBottomValSizer.Hide(index)
        self.remarkBottomValSizer.Remove(index)

        #statusChangeBottom col stuff
        self.statusChangeBottomValSizer.Hide(index)
        self.statusChangeBottomValSizer.Remove(index)

        #deploymentStatusBottom col stuff
        self.deploymentStatusBottomValSizer.Hide(index)
        self.deploymentStatusBottomValSizer.Remove(index)

        #newRemarkBottom col stuff
        self.newRemarkBottomValSizer.Hide(index)
        self.newRemarkBottomValSizer.Remove(index)
        
        for index, col in enumerate(self.invenManBottomSizerH.GetChildren()):
            for rowIndex, child in enumerate(col.GetSizer().GetItem(1).GetWindow().GetSizer().GetChildren()):
                i = int(child.GetWindow().GetName())
                if i > rowIndex:
                    child.GetWindow().SetName("%s" % (i - 1))



    # Delete all the rows of the bottom table
    def RemoveFullBottom(self):
        if self.mode=="DEBUG":
            print("remove full bottom")

        # Maybe this should be different?
        self.entryNumBottom = 1

        #select col stuff
        self.selectBottomSizer.Clear(delete_windows=True)

        #stationIDBottom col stuff
        self.stationIDBottomValSizer.Clear(delete_windows=True)

        #deviceStatusBottom col stuff
        self.deviceStatusBottomValSizer.Clear(delete_windows=True)

        #deviceCategoryBottom col stuff
        self.deviceCategoryBottomValSizer.Clear(delete_windows=True)

        #deviceMakeBottom col stuff
        self.deviceMakeBottomValSizer.Clear(delete_windows=True)

        #deviceModelBottom col stuff
        self.deviceModelBottomValSizer.Clear(delete_windows=True)

        #serialNumberBottom col stuff
        self.serialNumberBottomValSizer.Clear(delete_windows=True)

        #firmwareBottom col stuff
        self.firmwareBottomValSizer.Clear(delete_windows=True)

        #installationDateBottom col stuff
        self.installationDateBottomValSizer.Clear(delete_windows=True)

        #effectiveDateBottom col stuff
        self.effectiveDateBottomValSizer.Clear(delete_windows=True)

        #remarkBottom col stuff
        self.remarkBottomValSizer.Clear(delete_windows=True)

        #statusChangeBottom col stuff
        self.statusChangeBottomValSizer.Clear(delete_windows=True)

        #deploymentStatusBottom col stuff
        self.deploymentStatusBottomValSizer.Clear(delete_windows=True)

        #newRemarkBottom col stuff
        self.newRemarkBottomValSizer.Clear(delete_windows=True)

        self.invenManBottomSizerV.Layout()
        self.invenManBottomPanel.Layout()
        self.invenManBottomPanel.Update()
        self.layoutSizer.Layout()
        self.Layout()
        self.Update()
        self.Refresh()
        self.invenManBottomPanel.SetupScrolling(scrollIntoView=False)
        self.invenManBottomPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)



    # ===============================
    # ===============================
    # ====  Getters and Setters  ====
    # ===============================
    # ===============================

    #checkbox window
    '''
    def GetCheckbox(self, row, position):
        if position == 'Top':
            maxrow = len(self.selectTopSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return  self.selectTopSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.selectBottomSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return  self.selectBottomSizer.GetItem(row).GetWindow()
    '''    


    #stationID window
    def GetstationID(self, row, position):
        if position == 'Top':
            maxrow = len(self.stationIDTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.stationIDTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.stationIDBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.stationIDBottomValSizer.GetItem(row).GetWindow()

    #stationID Val Getter
    def GetstationIDVal(self, row, position):
        return self.GetstationID(row, position).GetValue()

    #stationID Val Setter
    def SetstationIDVal(self, row, val, position):
        self.GetstationID(row, position).SetValue(val)



    #deviceStatus window
    def GetdeviceStatus(self, row, position):
        if position == 'Top':
            maxrow = len(self.deviceStatusTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceStatusTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.deviceStatusBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceStatusBottomValSizer.GetItem(row).GetWindow()

    #deviceStatus Val Getter
    def GetdeviceStatusVal(self, row, position):
        return self.GetdeviceStatus(row, position).GetValue()

    #deviceStatus Val Setter
    def SetdeviceStatusVal(self, row, val, position):
        self.GetdeviceStatus(row, position).SetValue(val)



    #deviceCategory window
    def GetdeviceCategory(self, row, position):
        if position == 'Top':
            maxrow = len(self.deviceCategoryTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceCategoryTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.deviceCategoryBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceCategoryBottomValSizer.GetItem(row).GetWindow()

    #deviceCategory Val Getter
    def GetdeviceCategoryVal(self, row, position):
        return self.GetdeviceCategory(row, position).GetValue()

    #deviceCategory Val Setter
    def SetdeviceCategoryVal(self, row, val, position):
        self.GetdeviceCategory(row, position).SetValue(val)



    #deviceMake window
    def GetdeviceMake(self, row, position):
        if position == 'Top':
            maxrow = len(self.deviceMakeTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceMakeTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.deviceMakeBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceMakeBottomValSizer.GetItem(row).GetWindow()

    #deviceMake Val Getter
    def GetdeviceMakeVal(self, row, position):
        return self.GetdeviceMake(row, position).GetValue()

    #deviceMake Val Setter
    def SetdeviceMakeVal(self, row, val, position):
        self.GetdeviceMake(row, position).SetValue(val)



    #deviceModel window
    def GetdeviceModel(self, row, position):
        if position == 'Top':
            maxrow = len(self.deviceModelTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceModelTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.deviceModelBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deviceModelBottomValSizer.GetItem(row).GetWindow()

    #deviceModel Val Getter
    def GetdeviceModelVal(self, row, position):
        return self.GetdeviceModel(row, position).GetValue()

    #deviceModel Val Setter
    def SetdeviceModelVal(self, row, val, position):
        self.GetdeviceModel(row, position).SetValue(val)



    #serialNumber window
    def GetserialNumber(self, row, position):
        if position == 'Top':
            maxrow = len(self.serialNumberTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.serialNumberTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.serialNumberBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.serialNumberBottomValSizer.GetItem(row).GetWindow()

    #serialNumber Val Getter
    def GetserialNumberVal(self, row, position):
        return self.GetserialNumber(row, position).GetValue()

    #serialNumber Val Setter
    def SetserialNumberVal(self, row, val, position):
        self.GetserialNumber(row, position).SetValue(val)



    #firmware window
    def Getfirmware(self, row, position):
        if position == 'Top':
            maxrow = len(self.firmwareTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.firmwareTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.firmwareBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.firmwareBottomValSizer.GetItem(row).GetWindow()

    #firmware Val Getter
    def GetfirmwareVal(self, row, position):
        return self.Getfirmware(row, position).GetValue()

    #firmware Val Setter
    def SetfirmwareVal(self, row, val, position):
        self.Getfirmware(row, position).SetValue(val)



    #installationDate window
    def GetinstallationDate(self, row, position):
        if position == 'Top':
            maxrow = len(self.installationDateTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.installationDateTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.installationDateBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.installationDateBottomValSizer.GetItem(row).GetWindow()

    #installationDate Val Getter
    def GetinstallationDateVal(self, row, position):
        return self.GetinstallationDate(row, position).GetValue()

    #installationDate Val Setter
    def SetinstallationDateVal(self, row, val, position):
        self.GetinstallationDate(row, position).SetValue(val)



    #effectiveDate window
    def GeteffectiveDate(self, row, position):
        if position == 'Top':
            maxrow = len(self.effectiveDateTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.effectiveDateTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.effectiveDateBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.effectiveDateBottomValSizer.GetItem(row).GetWindow()

    #effectiveDate Val Getter
    def GeteffectiveDateVal(self, row, position):
        return self.GeteffectiveDate(row, position).GetValue()

    #effectiveDate Val Setter
    def SeteffectiveDateVal(self, row, val, position):
        self.GeteffectiveDate(row, position).SetValue(val)



    #remark window
    def Getremark(self, row, position):
        if position == 'Top':
            maxrow = len(self.remarkTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.remarkTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.remarkBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.remarkBottomValSizer.GetItem(row).GetWindow()

    #remark Val Getter
    def GetremarkVal(self, row, position):
        return self.Getremark(row, position).GetValue()

    #remark Val Setter
    def SetremarkVal(self, row, val, position):
        self.Getremark(row, position).SetValue(val)



    #statusChange window
    def GetstatusChange(self, row, position):
        if position == 'Top':
            maxrow = len(self.statusChangeTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.statusChangeTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.statusChangeBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.statusChangeBottomValSizer.GetItem(row).GetWindow()

    #statusChange Val Getter
    def GetstatusChangeVal(self, row, position):
        return self.GetstatusChange(row, position).GetValue()

    #statusChange Val Setter
    def SetstatusChangeVal(self, row, val, position):
        self.GetstatusChange(row, position).SetValue(val)



    #deploymentStatus window
    def GetdeploymentStatus(self, row, position):
        if position == 'Top':
            maxrow = len(self.deploymentStatusTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deploymentStatusTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.deploymentStatusBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.deploymentStatusBottomValSizer.GetItem(row).GetWindow()

    #deploymentStatus Val Getter
    def GetdeploymentStatusVal(self, row, position):
        return self.GetdeploymentStatus(row, position).GetValue()

    #deploymentStatus Val Setter
    def SetdeploymentStatusVal(self, row, val, position):
        self.GetdeploymentStatus(row, position).SetValue(val)



    #newRemark window
    def GetnewRemark(self, row, position):
        if position == 'Top':
            maxrow = len(self.newRemarkTopValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.newRemarkTopValSizer.GetItem(row).GetWindow()
        else:
            maxrow = len(self.newRemarkBottomValSizer.GetChildren())
            if row >= maxrow:
                row = maxrow - 1

            return self.newRemarkBottomValSizer.GetItem(row).GetWindow()

    #newRemark Val Getter
    def GetnewRemarkVal(self, row, position):
        return self.GetnewRemark(row, position).GetValue()

    #newRemark Val Setter
    def SetnewRemarkVal(self, row, val, position):
        self.GetnewRemark(row, position).SetValue(val)




    # ============================
    # ============================
    # ====  Helper functions  ====
    # ============================
    # ============================

    #Disable scrolling function for combobox
    def NoScrolling(self, evt):
        pass

    
    # Display the help popup
    def displayHelp(self, evt):
        dlg = HelpDialog(self, 'Help Page')
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            dlg.Destroy()
        elif res == wx.ID_NO:
            dlg.Destroy()
        else:
            dlg.Destroy()


    # Set the deployment status based on the current status
    def SetDeploymentStatusTop(self, event):
        for index, ckbox in enumerate(self.selectTopSizer.GetChildren()):
            currentDeploymentStatus = self.GetdeploymentStatusVal(index, 'Top')
            currentStatusChange = self.GetstatusChangeVal(index, 'Top')
            if currentStatusChange == 'ACTIVE' or currentStatusChange == 'INACTIVE':
                self.SetdeploymentStatusVal(index, 'DEPLOYED', 'Top')
                self.GetdeploymentStatus(index, 'Top').Enable(False)
            elif currentStatusChange == '':
                # Do nothing if the row is an empty row for user entry
                pass
            else:
                if currentDeploymentStatus == 'DEPLOYED':
                    self.SetdeploymentStatusVal(index, '', 'Top')
                else:
                    self.SetdeploymentStatusVal(index, currentDeploymentStatus, 'Top')
                self.GetdeploymentStatus(index, 'Top').Enable(True)
        self.Refresh()


    # Set the deployment status based on the current status
    # Currently unused
    '''
    def SetDeploymentStatusBottom(self, event):
        for index, ckbox in enumerate(self.selectBottomSizer.GetChildren()):
            currentDeploymentStatus = self.GetdeploymentStatusVal(index, 'Bottom')
            currentStatusChange = self.GetstatusChangeVal(index, 'Bottom')
            if currentStatusChange == 'ACTIVE' or currentStatusChange == 'INACTIVE':
                self.SetdeploymentStatusVal(index, 'DEPLOYED', 'Bottom')
                self.GetdeploymentStatus(index, 'Bottom').Enable(False)
            else:
                if currentDeploymentStatus == 'DEPLOYED':
                    self.SetdeploymentStatusVal(index, '', 'Bottom')
                else:
                    self.SetdeploymentStatusVal(index, currentDeploymentStatus, 'Bottom')
                self.GetdeploymentStatus(index, 'Bottom').Enable(True)
        self.Refresh()
    '''


    #convert to upper case
    def OnTextType(self, event):
        textCtr=event.GetEventObject()
        point = textCtr.GetInsertionPoint()
        textCtr.ChangeValue(str.upper(textCtr.GetValue()))
        textCtr.SetInsertionPoint(point)
    

    def getCurrentTime(self):
        timestamp = dt.now()
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def getFormattedTime(self):
        timestamp = dt.now()
        return timestamp.strftime('%Y%m%d')

    def valid(self, path):
        if path != None and path != "" and not path.isspace():
            return True
        return False

    def textTooltip(self, event):
        textCtr=event.GetEventObject()
        textCtr.SetToolTip(textCtr.GetValue())

    # Warning popup for serial number
    def warningTooltip(self, event):
        textCtr=event.GetEventObject()
        textCtr.SetToolTip('Warning: Ensure Serial Number is accurate')

    #convert to white background
    # Currently unused
    '''
    def OnEnterValue(self, event):
        textCtr=event.GetEventObject()
        point = textCtr.GetInsertionPoint()
        textCtr.SetBackgroundColour((255,255,255))
        textCtr.SetInsertionPoint(point)
    '''

    # Part of the process of setting some backgrounds to red
    # Currently unused
    '''
    def OnDataCheckTop(self, event):
        for index, ckbox in enumerate(self.selectTopSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():

                currentStatusChange = self.GetstatusChangeVal(index, 'Top')
                currentDeploymentStatus = self.GetdeploymentStatusVal(index, 'Top')
                currentNewRemark = self.GetnewRemarkVal(index, 'Top')

                if currentStatusChange == 'N/A' or currentDeploymentStatus == '':
                    self.GetstatusChange(index, 'Top').SetBackgroundColour((255,0,0))
                else:
                    self.GetstatusChange(index, 'Top').SetBackgroundColour((255,255,255))

                if currentDeploymentStatus == '':
                    self.GetdeploymentStatus(index, 'Top').SetBackgroundColour((255,0,0))
                else:
                    self.GetdeploymentStatus(index, 'Top').SetBackgroundColour((255,255,255))
                
                if currentNewRemark == '':
                    self.GetnewRemark(index, 'Top').SetBackgroundColour((255,0,0))
                else:
                    self.GetnewRemark(index, 'Top').SetBackgroundColour((255,255,255))
            
            else:
                self.GetstatusChange(index, 'Top').SetBackgroundColour((255,255,255))
                self.GetdeploymentStatus(index, 'Top').SetBackgroundColour((255,255,255))
                self.GetnewRemark(index, 'Top').SetBackgroundColour((255,255,255))

        self.Refresh()
    '''
    
    # Part of the process of setting some backgrounds to red
    # Currently unused (and has modified version in use below)
    '''
    def OnDataCheckBottom(self, event):
        for index, ckbox in enumerate(self.selectBottomSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():

                currentStatusChange = self.GetstatusChangeVal(index, 'Bottom')
                currentDeploymentStatus = self.GetdeploymentStatusVal(index, 'Bottom')
                currentNewRemark = self.GetnewRemarkVal(index, 'Bottom')

                if currentStatusChange == 'N/A' or currentDeploymentStatus == '':
                    self.GetstatusChange(index, 'Bottom').SetBackgroundColour((255,0,0))
                else:
                    self.GetstatusChange(index, 'Bottom').SetBackgroundColour((255,255,255))

                if currentDeploymentStatus == '':
                    self.GetdeploymentStatus(index, 'Bottom').SetBackgroundColour((255,0,0))
                else:
                    self.GetdeploymentStatus(index, 'Bottom').SetBackgroundColour((255,255,255))
                
                if currentNewRemark == '':
                    self.GetnewRemark(index, 'Bottom').SetBackgroundColour((255,0,0))
                else:
                    self.GetnewRemark(index, 'Bottom').SetBackgroundColour((255,255,255))
            
            else:
                self.GetstatusChange(index, 'Bottom').SetBackgroundColour((255,255,255))
                self.GetdeploymentStatus(index, 'Bottom').SetBackgroundColour((255,255,255))
                self.GetnewRemark(index, 'Bottom').SetBackgroundColour((255,255,255))

        self.Refresh()
    '''



    # =================================
    # =================================
    # ====  Functions for buttons  ====
    # =================================
    # =================================


    # Setting the values for communication devices
    # This sets values in the dataframes based on the cateogry of the device
    # All of the data is set behind the scenes
    def CategorySetPopups(self, evt):

        # Check if more than 1 checkbox is clicked
        counter = 0
        for index, ckbox in enumerate(self.selectTopSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                counter += 1
        if counter > 1:
            dlg = wx.MessageDialog(self, "Multiple checkboxes selected, please choose a single row", 'Error', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
            return
        
        else:

            for index, ckbox in enumerate(self.selectTopSizer.GetChildren()):
                if ckbox.GetWindow().IsChecked():
                    
                    # Get the saved index
                    dataset_index = self.top_table_dataframe.at[index, 'dataset_index_marker']

                    # If the user is setting communication details for a new row (_new)
                    # then update the row in the dataframe based on the current values in the table
                    if 'new' in str(dataset_index):
                        self.updateDataframeRow(index)
                    
                    # Get the saved cateogry type
                    device_type = self.top_table_dataframe.at[index, 'Category']

                    # If a device has been transferred to a warehouse, then it shouldn't be modifiable
                    if 'bottom' in str(dataset_index):
                        dlg = wx.MessageDialog(self, "Device transferred to warehouse, cannot modify further", 'Error', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return

                    # If the device is newly added, then check if its category matches a communication device
                    if 'new' in str(dataset_index):
                        if device_type == '':
                            dlg = wx.MessageDialog(self, "Please enter Device Category to continue", 'Error', wx.OK)
                            res = dlg.ShowModal()
                            if res == wx.ID_OK:
                                dlg.Destroy()
                            return
                        
                        elif device_type not in self.commTypes.keys():
                            dlg = wx.MessageDialog(self, "Device is not a communication device, see Help for communication device types", 'Error', wx.OK)
                            res = dlg.ShowModal()
                            if res == wx.ID_OK:
                                dlg.Destroy()
                            return
                        
                        # Set the communication info status to yes if the new device is a communication device
                        elif device_type in self.commTypes.keys():
                            self.top_table_dataframe.at[index, 'Communication Information'] = 'Yes'

                    # Get the communication info status
                    comm_device = self.top_table_dataframe.at[index, 'Communication Information']
                    if comm_device != 'Yes' and device_type not in self.commTypes.keys():
                        dlg = wx.MessageDialog(self, "Device is not a communication device", 'Error', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return
                    

                    ########################
                    ## CAMERA - IP OR PDT ##
                    ########################
                    if device_type == 'CAMERA - IP OR PDT':
                        title_details = "CAMERA - IP OR PDT&&&&&&&&&&&&"
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'IP or PDT Address'])

                        dlg = CAMERADialog(self, title_details)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            self.top_table_dataframe.at[index, 'IP or PDT Address'] = dlg.GetPDT()
                        else:
                            return
                        dlg.Destroy()

                    ####################
                    ## EXTERNAL MODEM ##
                    ####################
                    elif device_type == 'EXTERNAL MODEM':
                        title_details = "EXTERNAL MODEM&&&&&&&&&&&&"
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'Baud Rate']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'Parity']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'Telephone Number'])

                        dlg = MODEMDialog(self, title_details)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            self.top_table_dataframe.at[index, 'Baud Rate'] = dlg.GetBaud()
                            self.top_table_dataframe.at[index, 'Parity'] = dlg.GetParity()
                            self.top_table_dataframe.at[index, 'Telephone Number'] = dlg.GetTelephone()
                        else:
                            return
                        dlg.Destroy()

                    #####################################
                    ## IMAGE VELOCIMETRY CAMERA SYSTEM ##
                    #####################################
                    elif device_type == 'IMAGE VELOCIMETRY CAMERA SYSTEM':
                        title_details = "IMAGE VELOCIMETRY CAMERA SYSTEM&&&&&&&&&&&&"
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'IP or PDT Address'])

                        dlg = IMAGEVELOCIMETRYDialog(self, title_details)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            self.top_table_dataframe.at[index, 'IP or PDT Address'] = dlg.GetPDT()
                        else:
                            return
                        dlg.Destroy()

                    #######################
                    ## NETWORK - CELL IP ##
                    #######################
                    elif device_type == 'NETWORK - CELL IP':
                        title_details = "NETWORK - CELL IP&&&&&&&&&&&&"
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'IP or PDT Address'])

                        dlg = NETWORKDialog(self, title_details)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            self.top_table_dataframe.at[index, 'IP or PDT Address'] = dlg.GetPDT()
                        else:
                            return
                        dlg.Destroy()

                    ############################
                    ## SATELLITE - GOES - HDR ##
                    ############################
                    elif device_type == 'SATELLITE - GOES - HDR':
                        title_details = "SATELLITE - GOES - HDR&&&&&&&&&&&&"
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'IP or PDT Address']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'XMT Rate']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'XMT Window']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'XMT Period']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'First XMT']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'Prime Channel']) + '&&&&&&&&&&&&'
                        title_details = title_details + str(self.top_table_dataframe.at[index, 'Transmission Frequency'])

                        dlg = GOESDialog(self, title_details)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            self.top_table_dataframe.at[index, 'IP or PDT Address'] = dlg.GetPDT()
                            self.top_table_dataframe.at[index, 'XMT Rate'] = dlg.GetXMTRate()
                            self.top_table_dataframe.at[index, 'XMT Window'] = dlg.GetXMTWindow()
                            self.top_table_dataframe.at[index, 'XMT Period'] = dlg.GetXMTPeriod()
                            self.top_table_dataframe.at[index, 'First XMT'] = dlg.GetXMTFirst()
                            self.top_table_dataframe.at[index, 'Prime Channel'] = dlg.GetPrimeChannel()
                            self.top_table_dataframe.at[index, 'Transmission Frequency'] = dlg.GetTXFreq()
                        else:
                            return
                        dlg.Destroy()
                    

                    else:
                        dlg = wx.MessageDialog(self, "Unable to match category", 'Error', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return



    # Reset the tables
    def OnReset(self, evt):
        
        # Reset the scrollbars
        self.invenManTopPanel.Scroll(0, 0)
        self.invenManBottomPanel.Scroll(0, 0)

        # Clear all the existing tables
        self.RemoveFullTop()
        self.RemoveFullBottom()

        # Update the hydex details
        self.updateSavedHydexDetails()

        # Populate the top table
        # The returned value isn't used here
        returned_val = self.inputStationData(True, self.topStation, "", "", "", "", 'Top')



    # Export the saved state
    def OnExport(self, evt):
        self.exportChangesOutput("")



    # Set the values of status change and deployment status when checkbox is clicked
    # For the bottom table
    def OnDataCheckBottom(self, event):
        for index, ckbox in enumerate(self.selectBottomSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                
                self.SetstatusChangeVal(index, 'REMOVED/TRANSFERRED', 'Bottom')
                self.SetdeploymentStatusVal(index, 'DEPLOYED', 'Bottom')
                self.statusChangeBottomValSizer.GetItem(index).GetWindow().Disable()
                self.deploymentStatusBottomValSizer.GetItem(index).GetWindow().Disable()

            else:
                self.SetstatusChangeVal(index, '', 'Bottom')
                self.SetdeploymentStatusVal(index, '', 'Bottom')
                self.statusChangeBottomValSizer.GetItem(index).GetWindow().Enable()
                self.deploymentStatusBottomValSizer.GetItem(index).GetWindow().Enable()

        self.Refresh()
    


    # Do a refresh of the data tables behind the scenes
    def updateSavedHydexDetails(self):

        # Setting the stored dataframes back to original
        self.full_hydex_dataframe = pd.DataFrame()
        self.top_table_dataframe = pd.DataFrame()
        self.bottom_table_dataframe = pd.DataFrame()
        self.bottom_storage_dataframe = pd.DataFrame()

        # Set the values of the dataframes
        hydex_reports = glob(self.dir + '\\AQ_Extracted_Data\\hydex_current_status_entire_network_devices_*.csv')
        if len(hydex_reports) > 0:

            # Populating the data from the report
            self.full_hydex_dataframe = pd.read_csv(hydex_reports[0])
            # Set an index value for each row
            self.full_hydex_dataframe['dataset_index_marker'] = self.full_hydex_dataframe.index
            # Remove nan values
            self.full_hydex_dataframe = self.full_hydex_dataframe.fillna('')

            # Set the columns of the blank dataframes
            self.top_table_dataframe = pd.DataFrame(columns=self.full_hydex_dataframe.columns.values.tolist())
            self.bottom_table_dataframe = pd.DataFrame(columns=self.full_hydex_dataframe.columns.values.tolist())
            self.bottom_storage_dataframe = pd.DataFrame(columns=self.full_hydex_dataframe.columns.values.tolist())

            # Setting the warning message that the data is too old
            split_hydex_name = hydex_reports[0].split('_')
            saved_date = split_hydex_name[len(split_hydex_name)-2]
            saved_datetime = dt.strptime(saved_date, '%Y-%m-%d')
            current_datetime = dt.now()
            time_difference = current_datetime - saved_datetime
            if time_difference.days > 28:
                self.inventoryManageTxt.SetLabel(self.inventoryManageLbl + ' (Hydex Device report > 28 days old)')
                self.inventoryManageTxt.SetForegroundColour((255,0,0))
            else:
                self.inventoryManageTxt.SetLabel(self.inventoryManageLbl)
                self.inventoryManageTxt.SetForegroundColour((0,0,0))
            


    # Clear the search fields and the bottom table
    def clearBottomTable(self, event):

        # Change all the search fields to be empty
        self.stationTextCtrl.SetValue('')
        self.makeTextCtrl.SetValue('')
        self.modelTextCtrl.SetValue('')
        self.serialNumTextCtrl.SetValue('')
        self.categoryTextCtrl.SetValue('')

        # Clear the bottom table
        self.RemoveFullBottom()



    # Populate the bottom table based on the search parameters provided by the user
    def populateBottomTable(self, event):

        # Get whether or not there are current values
        stationCheck = self.stationTextCtrl.GetValue() != ""
        categoryCheck = self.categoryTextCtrl.GetValue() != ""
        makeCheck = self.makeTextCtrl.GetValue() != ""
        modelCheck = self.modelTextCtrl.GetValue() != ""
        serialCheck = self.serialNumTextCtrl.GetValue() != ""
        
        # If the user has entered search values in certain pairs or just serial number
        # Category is required, alongside any number of the others
        if serialCheck or \
            (stationCheck and categoryCheck) or \
            (stationCheck and makeCheck) or \
            (stationCheck and modelCheck) or \
            (categoryCheck and makeCheck) or \
            (categoryCheck and modelCheck) or \
            (makeCheck and modelCheck):

            if (self.stationTextCtrl.GetValue() != "" and self.stationTextCtrl.GetValue() == self.topStation):
                dlg = wx.MessageDialog(self, "Cannot search for station already populated in top table", 'Unable to populate', wx.OK)
                res = dlg.ShowModal()
                if res == wx.ID_OK:
                    dlg.Destroy()
                return
            
            # Attempt to populate the table
            returned_value = self.inputStationData(False, self.stationTextCtrl.GetValue(), self.categoryTextCtrl.GetValue(), self.makeTextCtrl.GetValue(), self.modelTextCtrl.GetValue(), self.serialNumTextCtrl.GetValue(), 'Bottom')

            if returned_value == 0:
                dlg = wx.MessageDialog(self, "No data found from provided filters", 'Unable to populate', wx.OK)
                res = dlg.ShowModal()
                if res == wx.ID_OK:
                    dlg.Destroy()
                return
            elif returned_value == 2:
                dlg = wx.MessageDialog(self, "Found >500 results, please provide additional filters", 'Unable to populate', wx.OK)
                res = dlg.ShowModal()
                if res == wx.ID_OK:
                    dlg.Destroy()
                return

        else:
            dlg = wx.MessageDialog(self, "Please input Serial Number and/or any pair of Station ID/Category/Make/Model", 'Unable to populate', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
            return


    
    # Populate the given table
    # This takes in many search field results (station_id, category, model, serialNum)
    # However all of these fields do not have to be used, for populating the top table only station_id is used
    # start_refresh is used when initially populating the top table from the front page of eHSN
    # table specifies the table to be populated
    def inputStationData(self, start_refresh, station_id, category, make, model, serialNum, table):
        
        # The populating of the top table initially (start_refresh = true) is done with an empty station in the front page of eHSN
        # In this case, this has to return without reading anything otherwise it'll keep trying and there will be a memory error
        if start_refresh and station_id == "":
            return 0
        
        # Get the data if the base dataframe is not empty
        if not self.full_hydex_dataframe.empty:
            
            # Filter the data
            specific_data = self.full_hydex_dataframe.copy()
            if station_id != "":
                # This is an exact string match only
                specific_data = specific_data[specific_data['Station ID'] == station_id]
            if category != "":
                #specific_data = specific_data[specific_data['Category'] == category]
                specific_data = specific_data[specific_data['Category'].str.startswith(category)]
            if make != "":
                #specific_data = specific_data[specific_data['Make'] == make]
                specific_data = specific_data[specific_data['Make'].str.startswith(make)]
            if model != "":
                #specific_data = specific_data[specific_data['Model'] == model]
                # Some models (Eon2, Bubbler, cs107, cs109) are lower case and must be converted
                specific_data = specific_data[specific_data['Model'].str.upper().str.startswith(model)]
            if serialNum != "":
                #specific_data = specific_data[specific_data['Serial Number'] == serialNum]
                specific_data = specific_data[specific_data['Serial Number'].str.contains(serialNum)]
            
            # If there is no data found from filtering, return
            if specific_data.empty:
                return 0

            # Get the data in the right format
            filtered_data = specific_data.to_dict(orient='records')

            # If the amount of data is greater than 500, return
            if len(filtered_data) > 500:
                return 2

            # Adding to the top table
            if table == 'Top':
                
                # Set the top table station
                self.topStation = station_id

                # Set the dataframe for these station values
                self.top_table_dataframe = specific_data.copy()
                self.top_table_dataframe.reset_index(drop=True, inplace=True)
                if self.mode == "DEBUG":
                    print(self.top_table_dataframe)
                
                # Reset the scrollbar
                self.invenManTopPanel.Scroll(0, 0)

                # Delete all other rows of the table
                self.RemoveFullTop()

                # Add all the rows to the table
                for row in filtered_data:
                    self.AddEntryTop(False) 

                    self.SetstationIDVal(self.entryNumTop-2, row['Station ID'], 'Top')
                    self.SetdeviceStatusVal(self.entryNumTop-2, row['Status'], 'Top')
                    self.SetdeviceCategoryVal(self.entryNumTop-2, row['Category'], 'Top')
                    self.SetdeviceMakeVal(self.entryNumTop-2, row['Make'], 'Top')
                    self.SetdeviceModelVal(self.entryNumTop-2, row['Model'], 'Top')
                    self.SetserialNumberVal(self.entryNumTop-2, row['Serial Number'], 'Top')
                    self.SetfirmwareVal(self.entryNumTop-2, row['Firmware Version'], 'Top')
                    if 'Installation Date' in row:
                        self.SetinstallationDateVal(self.entryNumTop-2, row['Installation Date'], 'Top')
                    else:
                        self.SetinstallationDateVal(self.entryNumTop-2, '', 'Top')
                    self.SeteffectiveDateVal(self.entryNumTop-2, row['Effective Date'], 'Top')
                    self.SetremarkVal(self.entryNumTop-2, row['Remark'], 'Top')
                    
                    self.SetstatusChangeVal(self.entryNumTop-2, 'N/A', 'Top')
                    self.SetdeploymentStatusVal(self.entryNumTop-2, '', 'Top')
                    self.SetnewRemarkVal(self.entryNumTop-2, '', 'Top')
                
                # Previously these functions were in the Add Entry Top and Remove Entry Top function
                self.invenManTopSizerV.Layout()
                self.invenManTopPanel.Layout()
                self.invenManTopPanel.Update()
                self.layoutSizer.Layout()
                self.Layout()
                self.Update()
                self.Refresh()
                self.invenManTopPanel.SetupScrolling(scrollIntoView=False)
                self.invenManTopPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)

            # Adding to the bottom table
            else:
                
                # Set the dataframe for these station values
                self.bottom_table_dataframe = specific_data.copy()
                self.bottom_table_dataframe.reset_index(drop=True, inplace=True)
                if self.mode == "DEBUG":
                    print(self.bottom_table_dataframe)
                
                # Reset the scrollbar
                self.invenManBottomPanel.Scroll(0, 0)

                # Delete all other rows of the table
                self.RemoveFullBottom()

                # Add all the rows to the table
                for row in filtered_data:
                    self.AddEntryBottom()
                    
                    self.SetstationIDVal(self.entryNumBottom-2, row['Station ID'], 'Bottom')
                    self.SetdeviceStatusVal(self.entryNumBottom-2, row['Status'], 'Bottom')
                    self.SetdeviceCategoryVal(self.entryNumBottom-2, row['Category'], 'Bottom')
                    self.SetdeviceMakeVal(self.entryNumBottom-2, row['Make'], 'Bottom')
                    self.SetdeviceModelVal(self.entryNumBottom-2, row['Model'], 'Bottom')
                    self.SetserialNumberVal(self.entryNumBottom-2, row['Serial Number'], 'Bottom')
                    self.SetfirmwareVal(self.entryNumBottom-2, row['Firmware Version'], 'Bottom')
                    if 'Installation Date' in row:
                        self.SetinstallationDateVal(self.entryNumBottom-2, row['Installation Date'], 'Bottom')
                    else:
                        self.SetinstallationDateVal(self.entryNumBottom-2, '', 'Bottom')
                    self.SeteffectiveDateVal(self.entryNumBottom-2, row['Effective Date'], 'Bottom')
                    self.SetremarkVal(self.entryNumBottom-2, row['Remark'], 'Bottom')
                    
                    self.SetstatusChangeVal(self.entryNumBottom-2, '', 'Bottom')
                    self.SetdeploymentStatusVal(self.entryNumBottom-2, '', 'Bottom')
                    self.SetnewRemarkVal(self.entryNumBottom-2, '', 'Bottom')
                
                # Previously these functions were in the Add Entry Bottom and Remove Entry Bottom function
                self.invenManBottomSizerV.Layout()
                self.invenManBottomPanel.Layout()
                self.invenManBottomPanel.Update()
                self.layoutSizer.Layout()
                self.Layout()
                self.Update()
                self.Refresh()
                self.invenManBottomPanel.SetupScrolling(scrollIntoView=False)
                self.invenManBottomPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
            
            return 1
        
        else:
            return 0


    
    # Transferring a device from the bottom table to the top table
    def OnTransferFromBottomToTop(self, evt):

        # Check if more than 1 checkbox is clicked
        counter = 0
        for index, ckbox in enumerate(self.selectBottomSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                counter += 1
        if counter > 1:
            dlg = wx.MessageDialog(self, "Multiple checkboxes selected, please choose a single row", 'Unable to transfer', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
            return

        elif self.topStation == "":
            dlg = wx.MessageDialog(self, "No Station selected above, please choose a station on the front page", 'Unable to transfer', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
            return
        
        else:

            for index, ckbox in enumerate(self.selectBottomSizer.GetChildren()):
                if ckbox.GetWindow().IsChecked():
                    
                    # Save the data from the row
                    row = {}
                    row['Station ID'] = self.topStation
                    row['Status'] = self.GetdeviceStatusVal(index, 'Bottom')
                    row['Category'] = self.GetdeviceCategoryVal(index, 'Bottom')
                    row['Make'] = self.GetdeviceMakeVal(index, 'Bottom')
                    row['Model'] = self.GetdeviceModelVal(index, 'Bottom')
                    row['Serial Number'] = self.GetserialNumberVal(index, 'Bottom')
                    row['Firmware Version'] = self.GetfirmwareVal(index, 'Bottom')
                    row['Installation Date'] = self.GetinstallationDateVal(index, 'Bottom')
                    row['Effective Date'] = self.GeteffectiveDateVal(index, 'Bottom')
                    row['Remark'] = self.GetremarkVal(index, 'Bottom')
                    row['Status Change'] = self.GetstatusChangeVal(index, 'Bottom')
                    row['Deployment Status'] = self.GetdeploymentStatusVal(index, 'Bottom')
                    row['New Remark'] = self.GetnewRemarkVal(index, 'Bottom')
                    row['Old Status Change'] = self.GetstatusChangeVal(index, 'Bottom')
                    timestamp = self.getCurrentTime()

                    #if row['Status Change'] == "" or row['Status Change'] == "N/A":
                    #    dlg = wx.MessageDialog(self, "Please choose the Status Change", 'Unable to transfer', wx.OK)
                    #    res = dlg.ShowModal()
                    #    if res == wx.ID_OK:
                    #        dlg.Destroy()
                    #    return

                    #if row['Deployment Status'] == "":
                    #    dlg = wx.MessageDialog(self, "Please choose the Deployment Status", 'Unable to transfer', wx.OK)
                    #    res = dlg.ShowModal()
                    #    if res == wx.ID_OK:
                    #        dlg.Destroy()
                    #    return
                
                    if row['New Remark'] == "":
                        dlg = wx.MessageDialog(self, "Please add the New Remark", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return

                    #if row['Status Change'] != "REMOVED/TRANSFERRED":
                    #    dlg = wx.MessageDialog(self, "Cannot transfer if status change is not REMOVED/TRANSFERRED", 'Unable to transfer', wx.OK)
                    #    res = dlg.ShowModal()
                    #    if res == wx.ID_OK:
                    #        dlg.Destroy()
                    #    return
                    
                    #if row['Deployment Status'] == "DESTROYED":
                    #    dlg = wx.MessageDialog(self, "Cannot transfer if deployment status is DESTROYED", 'Unable to transfer', wx.OK)
                    #    res = dlg.ShowModal()
                    #    if res == wx.ID_OK:
                    #        dlg.Destroy()
                    #    return
                    

                    # Show the transfer popup
                    dlg = TransferDialog(self, "Transfer Details&&&&&&&&&&&&" + self.topStation)
                    res = dlg.ShowModal()
                    if res == wx.ID_OK:
                        row['Status Change'] = dlg.GetDestinationStatus()
                    else:
                        return
                    dlg.Destroy()

                    # Show the summary popup
                    summary_full = "Summary&&&&&&&&&&&&"
                    for key in row:
                        summary_full = summary_full + row[key] + '&&&&&&&&&&&&'
                    dlg = SummaryDialog(self, summary_full[:-1])
                    res = dlg.ShowModal()
                    if res == wx.ID_OK:
                        dlg.Destroy()
                    else:
                        return


                    # Copy the dataframe from bottom to storage
                    saved_row = self.bottom_table_dataframe.iloc[index]
                    len_bottom_storage = self.bottom_storage_dataframe.shape[0]
                    self.bottom_storage_dataframe.loc[len_bottom_storage] = saved_row.values.tolist()
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'Effective Date'] = timestamp
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'Status'] = row['Old Status Change']
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'Deployment Status'] = row['Deployment Status']
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'Remark'] = row['New Remark']
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'dataset_index_marker'] = str(self.bottom_storage_dataframe.at[len_bottom_storage, 'dataset_index_marker']) + '_transfer_top'                    

                    # Copy the dataframe from bottom to top
                    len_top_table = self.top_table_dataframe.shape[0]
                    self.top_table_dataframe.loc[len_top_table] = saved_row.values.tolist()
                    self.top_table_dataframe.at[len_top_table, 'Station ID'] = row['Station ID']
                    self.top_table_dataframe.at[len_top_table, 'Effective Date'] = timestamp
                    self.top_table_dataframe.at[len_top_table, 'Status'] = row['Status Change']
                    self.top_table_dataframe.at[len_top_table, 'Deployment Status'] = row['Deployment Status']
                    self.top_table_dataframe.at[len_top_table, 'Remark'] = row['New Remark']
                    self.top_table_dataframe.at[len_top_table, 'dataset_index_marker'] = str(self.top_table_dataframe.at[len_top_table, 'dataset_index_marker']) + '_transfer_top'                    
                    
                    # Remove the row from the bottom
                    self.RemoveEntryBottom(index)
                    self.bottom_table_dataframe = self.bottom_table_dataframe.drop(index)
                    self.bottom_table_dataframe.reset_index(drop=True, inplace=True)
                    if self.mode == "DEBUG":
                        print(self.bottom_table_dataframe)
                    self.invenManBottomSizerV.Layout()
                    self.invenManBottomPanel.Layout()
                    self.invenManBottomPanel.Update()

                    # Add the new row in the top table
                    self.AddEntryTop(False)
                    
                    # Set the values
                    self.SetstationIDVal(self.entryNumTop-2, row['Station ID'], 'Top')
                    self.SetdeviceStatusVal(self.entryNumTop-2, row['Status'], 'Top')
                    self.SetdeviceCategoryVal(self.entryNumTop-2, row['Category'], 'Top')
                    self.SetdeviceMakeVal(self.entryNumTop-2, row['Make'], 'Top')
                    self.SetdeviceModelVal(self.entryNumTop-2, row['Model'], 'Top')
                    self.SetserialNumberVal(self.entryNumTop-2, row['Serial Number'], 'Top')
                    self.SetfirmwareVal(self.entryNumTop-2, row['Firmware Version'], 'Top')
                    self.SetinstallationDateVal(self.entryNumTop-2, row['Installation Date'], 'Top')
                    self.SeteffectiveDateVal(self.entryNumTop-2, timestamp, 'Top')
                    self.SetremarkVal(self.entryNumTop-2, row['Remark'], 'Top')
                    self.SetstatusChangeVal(self.entryNumTop-2, row['Status Change'], 'Top')
                    self.SetdeploymentStatusVal(self.entryNumTop-2, row['Deployment Status'], 'Top')
                    self.SetnewRemarkVal(self.entryNumTop-2, row['New Remark'], 'Top')

                    # Change the colour of the text
                    self.GetstationID(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetdeviceStatus(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetdeviceCategory(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetdeviceMake(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetdeviceModel(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetserialNumber(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.Getfirmware(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetinstallationDate(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GeteffectiveDate(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.Getremark(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetstatusChange(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetdeploymentStatus(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))
                    self.GetnewRemark(self.entryNumTop-2, 'Top').SetForegroundColour((255,0,0))

                    # Update and refresh
                    self.invenManTopSizerV.Layout()
                    self.invenManTopPanel.Layout()
                    self.invenManTopPanel.Update()
                    self.Layout()
                    self.Update()
                    self.Refresh()

                    # Set the scrollbar for the top table to be at the bottom
                    self.invenManTopPanel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
                    max_scroll = self.invenManTopPanel.GetScrollRange(wx.VERTICAL)
                    self.invenManTopPanel.Scroll(0, max_scroll)
                    


    # Transferring a device from the top table to the bottom table
    def OnTransferFromTopToBottom(self, evt):

        # Check if more than 1 checkbox is clicked
        counter = 0
        for index, ckbox in enumerate(self.selectTopSizer.GetChildren()):
            if ckbox.GetWindow().IsChecked():
                counter += 1
        if counter > 1:
            dlg = wx.MessageDialog(self, "Multiple checkboxes selected, please choose a single row", 'Unable to transfer', wx.OK)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                dlg.Destroy()
            return
        
        else:

            for index, ckbox in enumerate(self.selectTopSizer.GetChildren()):
                if ckbox.GetWindow().IsChecked():
                    
                    # Save the data from the row
                    row = {}
                    row['Station ID'] = self.GetstationIDVal(index, 'Top')
                    row['Status'] = self.GetdeviceStatusVal(index, 'Top')
                    row['Category'] = self.GetdeviceCategoryVal(index, 'Top')
                    row['Make'] = self.GetdeviceMakeVal(index, 'Top')
                    row['Model'] = self.GetdeviceModelVal(index, 'Top')
                    row['Serial Number'] = self.GetserialNumberVal(index, 'Top')
                    row['Firmware Version'] = self.GetfirmwareVal(index, 'Top')
                    row['Installation Date'] = self.GetinstallationDateVal(index, 'Top')
                    row['Effective Date'] = self.GeteffectiveDateVal(index, 'Top')
                    row['Remark'] = self.GetremarkVal(index, 'Top')
                    row['Status Change'] = self.GetstatusChangeVal(index, 'Top')
                    row['Deployment Status'] = self.GetdeploymentStatusVal(index, 'Top')
                    row['New Remark'] = self.GetnewRemarkVal(index, 'Top')
                    row['Old Status Change'] = self.GetstatusChangeVal(index, 'Top')
                    timestamp = self.getCurrentTime()

                    if row['Status Change'] == "" or row['Status Change'] == "N/A":
                        dlg = wx.MessageDialog(self, "Please choose the Status Change", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return

                    if row['Deployment Status'] == "":
                        dlg = wx.MessageDialog(self, "Please choose the Deployment Status", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return
                
                    if row['New Remark'] == "":
                        dlg = wx.MessageDialog(self, "Please add the New Remark", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return
                    
                    if row['Status Change'] != "REMOVED/TRANSFERRED":
                        dlg = wx.MessageDialog(self, "Cannot transfer if status change is not REMOVED/TRANSFERRED", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return
                    
                    if row['Deployment Status'] == "DESTROYED":
                        dlg = wx.MessageDialog(self, "Cannot transfer if deployment status is DESTROYED", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return
                    
                    # Show the transfer popup
                    dlg = TransferDialog(self, "Transfer Details")
                    res = dlg.ShowModal()
                    if res == wx.ID_OK:
                        row['Station ID'] = dlg.GetDestination()
                        row['Status Change'] = 'SHELVED'
                    else:
                        return
                    dlg.Destroy()

                    # Check that the destination location exists
                    if not self.full_hydex_dataframe.empty:
                        specific_data = self.full_hydex_dataframe[self.full_hydex_dataframe['Station ID'] == row['Station ID']].copy()
                        if specific_data.empty:
                            dlg = wx.MessageDialog(self, "Destination location does not match any known locations", 'Unable to transfer', wx.OK)
                            res = dlg.ShowModal()
                            if res == wx.ID_OK:
                                dlg.Destroy()
                            return    
                    
                    # Restrict to warehouses only
                    if not row['Station ID'].startswith('30'):
                        dlg = wx.MessageDialog(self, "Must choose a warehouse as destination location", 'Unable to transfer', wx.OK)
                        res = dlg.ShowModal()
                        if res == wx.ID_OK:
                            dlg.Destroy()
                        return
                    
                    # Show the summary popup
                    summary_full = "Summary&&&&&&&&&&&&"
                    for key in row:
                        summary_full = summary_full + row[key] + '&&&&&&&&&&&&'
                    dlg = SummaryDialog(self, summary_full[:-1])
                    res = dlg.ShowModal()
                    if res == wx.ID_OK:
                        dlg.Destroy()
                    else:
                        return

    
                    # Update values in the top dataframe
                    self.top_table_dataframe.at[index, 'Serial Number'] = row['Serial Number']
                    self.top_table_dataframe.at[index, 'Firmware Version'] = row['Firmware Version']
                    if 'Installation Date' in self.top_table_dataframe.columns:
                        self.top_table_dataframe.at[index, 'Installation Date'] = row['Installation Date']
                    self.top_table_dataframe.at[index, 'Effective Date'] = timestamp
                    self.top_table_dataframe.at[index, 'Status'] = row['Old Status Change']
                    self.top_table_dataframe.at[index, 'Deployment Status'] = row['Deployment Status']
                    self.top_table_dataframe.at[index, 'Remark'] = row['New Remark']
                    self.top_table_dataframe.at[index, 'dataset_index_marker'] = str(self.top_table_dataframe.at[index, 'dataset_index_marker']) + '_transfer_bottom'                    

                    # Copy the dataframe from top to storage
                    saved_row = self.top_table_dataframe.iloc[index]
                    len_bottom_storage = self.bottom_storage_dataframe.shape[0]
                    self.bottom_storage_dataframe.loc[len_bottom_storage] = saved_row.values.tolist()
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'Station ID'] = row['Station ID']
                    #self.bottom_storage_dataframe.at[len_bottom_storage, 'Effective Date'] = timestamp
                    self.bottom_storage_dataframe.at[len_bottom_storage, 'Status'] = row['Status Change']
                    #self.bottom_storage_dataframe.at[len_bottom_storage, 'Deployment Status'] = row['Deployment Status']
                    #self.bottom_storage_dataframe.at[len_bottom_storage, 'Remark'] = row['New Remark']
                    #self.bottom_storage_dataframe.at[len_bottom_storage, 'dataset_index_marker'] = str(self.bottom_storage_dataframe.at[len_bottom_storage, 'dataset_index_marker']) + '_transfer_bottom'                    
                    
                    # Set the colour and edit options of the top row
                    self.GetstationID(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetdeviceStatus(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetdeviceCategory(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetdeviceMake(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetdeviceModel(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetserialNumber(index, 'Top').SetBackgroundColour((255,153,51))
                    self.Getfirmware(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetinstallationDate(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GeteffectiveDate(index, 'Top').SetBackgroundColour((255,153,51))
                    self.Getremark(index, 'Top').SetBackgroundColour((255,153,51))
                    self.GetstatusChange(index, 'Top').SetForegroundColour((255,153,51))
                    self.GetdeploymentStatus(index, 'Top').SetForegroundColour((255,153,51))
                    self.GetnewRemark(index, 'Top').SetBackgroundColour((255,153,51))

                    # Turn off the ability to modify further
                    self.GetserialNumber(index, 'Top').Disable()
                    self.Getfirmware(index, 'Top').Disable()
                    self.GetinstallationDate(index, 'Top').Disable()
                    self.GeteffectiveDate(index, 'Top').Disable()
                    self.GetstatusChange(index, 'Top').Disable()
                    self.GetdeploymentStatus(index, 'Top').Disable()
                    self.GetnewRemark(index, 'Top').Disable()

                    # Add the new row in the bottom table
                    self.AddEntryBottom()

                    # Set the values
                    self.SetstationIDVal(self.entryNumBottom-2, row['Station ID'], 'Bottom')
                    self.SetdeviceStatusVal(self.entryNumBottom-2, row['Status Change'], 'Bottom')
                    self.SetdeviceCategoryVal(self.entryNumBottom-2, row['Category'], 'Bottom')
                    self.SetdeviceMakeVal(self.entryNumBottom-2, row['Make'], 'Bottom')
                    self.SetdeviceModelVal(self.entryNumBottom-2, row['Model'], 'Bottom')
                    self.SetserialNumberVal(self.entryNumBottom-2, row['Serial Number'], 'Bottom')
                    self.SetfirmwareVal(self.entryNumBottom-2, row['Firmware Version'], 'Bottom')
                    self.SetinstallationDateVal(self.entryNumBottom-2, row['Installation Date'], 'Bottom')
                    self.SeteffectiveDateVal(self.entryNumBottom-2, timestamp, 'Bottom')
                    self.SetremarkVal(self.entryNumBottom-2, row['Remark'], 'Bottom')
                    self.SetstatusChangeVal(self.entryNumBottom-2, row['Status Change'], 'Bottom')
                    self.SetdeploymentStatusVal(self.entryNumBottom-2, row['Deployment Status'], 'Bottom')
                    self.SetnewRemarkVal(self.entryNumBottom-2, row['New Remark'], 'Bottom')

                    # Turn off the ability to make changes
                    self.GetstatusChange(self.entryNumBottom-2, 'Bottom').Disable()
                    self.GetdeploymentStatus(self.entryNumBottom-2, 'Bottom').Disable()
                    self.GetnewRemark(self.entryNumBottom-2, 'Bottom').Disable()

                    # Set the new effective date in the top table
                    self.SeteffectiveDateVal(index, timestamp, 'Top')

                    # Turn off the checkbox
                    ckbox.GetWindow().SetValue(False)

                    # Update and refresh
                    self.invenManBottomSizerV.Layout()
                    self.invenManBottomPanel.Layout()
                    self.invenManBottomPanel.Update()
                    self.Layout()
                    self.Update()
                    self.Refresh()

                    # Set the scrollbar for the bottom table to be at the bottom
                    self.invenManBottomPanel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
                    max_scroll = self.invenManBottomPanel.GetScrollRange(wx.VERTICAL)
                    self.invenManBottomPanel.Scroll(0, max_scroll)




    # =======================================
    # =======================================
    # ====  Functions for print display  ====
    # =======================================
    # =======================================


    # Update a specific value of the top dataframe
    # Only if the value is not empty or N/A or if the value is not the same
    def updateDataframeVal(self, col, row, val):
        if val != "" and val != 'N/A':
            prev_val = self.top_table_dataframe.at[row, col]
            if prev_val != val:
                self.top_table_dataframe.at[row, col] = val

    
    # Update a row of the top dataframe based on index
    # This saves the edited state of a given row of the top table to the top dataframe
    # Despite the fact that many of these columns are not editable in the top table
    # All of them are still grabbed otherwise user created rows are missed
    def updateDataframeRow(self, index):

        self.updateDataframeVal('Station ID', index, self.GetstationIDVal(index, 'Top'))
        self.updateDataframeVal('Status', index, self.GetdeviceStatusVal(index, 'Top'))
        self.updateDataframeVal('Category', index, self.GetdeviceCategoryVal(index, 'Top'))
        self.updateDataframeVal('Make', index, self.GetdeviceMakeVal(index, 'Top'))
        self.updateDataframeVal('Model', index, self.GetdeviceModelVal(index, 'Top'))
        self.updateDataframeVal('Serial Number', index, self.GetserialNumberVal(index, 'Top'))
        self.updateDataframeVal('Firmware Version', index, self.GetfirmwareVal(index, 'Top'))
        if 'Installation Date' in self.top_table_dataframe.columns:
            self.updateDataframeVal('Installation Date', index, self.GetinstallationDateVal(index, 'Top'))
        self.updateDataframeVal('Effective Date', index, self.GeteffectiveDateVal(index, 'Top'))
        self.updateDataframeVal('Remark', index, self.GetremarkVal(index, 'Top'))

        # Status and Remark are overwritten again here
        self.updateDataframeVal('Status', index, self.GetstatusChangeVal(index, 'Top'))
        self.updateDataframeVal('Deployment Status', index, self.GetdeploymentStatusVal(index, 'Top'))
        self.updateDataframeVal('Remark', index, self.GetnewRemarkVal(index, 'Top'))


    # Handle wrapping text for remarks when considering devices that have been transferred
    # This sets bold text based on comparason with original dataframe
    def wrapMultipleTrasnfer(self, key, text_array, remark_0, remark_1, remark_2):
        
        # If both are not empty strings, then continue forward
        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') != '' or str(remark_2).replace(" ", "").replace('\r', '').replace('\n', '') != '':
            
            # Get the wrapped lists for both remarks
            remark_list_1 = wrap(remark_1, width=20)
            remark_list_2 = wrap(remark_2, width=20)

            # If the first remark is larger than the second
            if len(remark_list_1) >= len(remark_list_2):
                
                # Iterate over the first remark
                for index, substring in enumerate(remark_list_1):

                    # If there are still sections of the second remark left
                    if index <= len(remark_list_2)-1:

                        displayVal1 = ''
                        displayVal2 = ''
                        if str(remark_0).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_1).replace(" ", "").replace('\r', '').replace('\n', ''):
                            displayVal1 = str(substring)
                        else:
                            displayVal1 = '**'+str(substring)+'**'
                        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            displayVal2 = str(remark_list_2[index])
                        else:
                            displayVal2 = '**'+str(remark_list_2[index])+'**'
                        
                        # Account for the distance being off because the **** have been removed in the markup file writing
                        if "**" in displayVal1:
                            displayVal2 = ' ' + ' ' + ' ' + ' ' + displayVal2
                        
                        if index == 0:
                            text_array.append([key+': ', displayVal1, displayVal2])
                        else:
                            text_array.append(['.', displayVal1, displayVal2])
                    
                    # Otherwise the second remark is now blank
                    # There's no accounting for bold characters with a blank string
                    else:

                        displayVal1 = ''
                        if str(remark_0).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_1).replace(" ", "").replace('\r', '').replace('\n', ''):
                            displayVal1 = str(substring)
                        else:
                            displayVal1 = '**'+str(substring)+'**'

                        if index == 0:
                            text_array.append([key+': ', displayVal1, ' '])
                        else:
                            text_array.append(['.', displayVal1, ' '])

            # Otherwise the second remark is larger than the first      
            else:
                
                # Iterate over the second remark
                for index, substring in enumerate(remark_list_2):

                    # If there are still sections of the first remark left
                    if index <= len(remark_list_1)-1:

                        displayVal1 = ''
                        displayVal2 = ''
                        if str(remark_0).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_1).replace(" ", "").replace('\r', '').replace('\n', ''):
                            displayVal1 = str(remark_list_1[index])
                        else:
                            displayVal1 = '**'+str(remark_list_1[index])+'**'
                        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            displayVal2 = str(substring)
                        else:
                            displayVal2 = '**'+str(substring)+'**'
                        
                        # Account for the distance being off because the **** have been removed in the markup file writing
                        if "**" in displayVal1:
                            displayVal2 = ' ' + ' ' + ' ' + ' ' + displayVal2

                        if index == 0:
                            text_array.append([key+': ', displayVal1, displayVal2])
                        else:
                            text_array.append(['.', displayVal1, displayVal2])
                    
                    # Otherwise the first remark is now blank
                    else:
                        
                        displayVal2 = ''
                        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            displayVal2 = str(substring)
                        else:
                            displayVal2 = '**'+str(substring)+'**'
                        
                        if index == 0:
                            text_array.append([key+': ', ' ', displayVal2])
                        else:
                            text_array.append(['.', ' ', displayVal2])
        
        # Otherwise add an empty result
        else:
            text_array.append([key+': ', ' ', ' '])

        return text_array


    # Handle wrapping text for remarks when considering devices that have been updated
    # This sets bold text based on comparason with original dataframe
    def wrapMultipleDiff(self, key, text_array, remark_1, remark_2):
                
        # If both are not empty strings, then continue forward
        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') != '' or str(remark_2).replace(" ", "").replace('\r', '').replace('\n', '') != '':
            
            # Get the wrapped lists for both remarks
            remark_list_1 = wrap(remark_1, width=20)
            remark_list_2 = wrap(remark_2, width=20)

            # If the first remark is larger than the second
            if len(remark_list_1) >= len(remark_list_2):
                
                # Iterate over the first remark
                for index, substring in enumerate(remark_list_1):

                    # If there are still sections of the second remark left
                    if index <= len(remark_list_2)-1:

                        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            if index == 0:
                                text_array.append([key+': ', str(substring), str(remark_list_2[index])])
                            else:
                                text_array.append(['.', str(substring), str(remark_list_2[index])])
                        else:
                            if index == 0:
                                text_array.append([key+': ', str(substring), '**'+str(remark_list_2[index])+'**'])
                            else:
                                text_array.append(['.', str(substring), '**'+str(remark_list_2[index])+'**'])
                    
                    # Otherwise the second remark is now blank
                    # There's no accounting for bold characters with a blank string
                    else:
                        if index == 0:
                            text_array.append([key+': ', str(substring), ' '])
                        else:
                            text_array.append(['.', str(substring), ' '])

            # Otherwise the second remark is larger than the first      
            else:
                
                # Iterate over the second remark
                for index, substring in enumerate(remark_list_2):

                    # If there are still sections of the first remark left
                    if index <= len(remark_list_1)-1:

                        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            if index == 0:
                                text_array.append([key+': ', str(remark_list_1[index]), str(substring)])
                            else:
                                text_array.append(['.', str(remark_list_1[index]), str(substring)])
                        else:
                            if index == 0:
                                text_array.append([key+': ', str(remark_list_1[index]), '**'+str(substring)+'**'])
                            else:
                                text_array.append(['.', str(remark_list_1[index]), '**'+str(substring)+'**'])
                    
                    # Otherwise the first remark is now blank
                    else:
                        
                        if str(remark_1).replace(" ", "").replace('\r', '').replace('\n', '') == str(remark_2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            if index == 0:
                                text_array.append([key+': ', ' ', str(substring)])
                            else:
                                text_array.append(['.', ' ', str(substring)])
                        else:
                            if index == 0:
                                text_array.append([key+': ', ' ', '**'+str(substring)+'**'])
                            else:
                                text_array.append(['.', ' ', '**'+str(substring)+'**'])
        
        # Otherwise add an empty result
        else:
            text_array.append([key+': ', ' ', ' '])

        return text_array

    
    # Format text to be in columns
    # Type 1 is two columns, type 2 is three columns
    def columnsTextFormat(self, text_table, text_list, type):
        if type == 1:
            len_1 = 0
            len_2 = 0
            for row in text_table:
                if len(row[0]) > len_1:
                    len_1 = len(row[0])
                if len(row[1]) > len_2:
                    len_2 = len(row[1])

            len_1 += 3
            len_2 += 3
            for row in text_table:
                formattingStyle = "{: <" + str(len_1) + "} {: <" + str(len_2) + "}"
                text_list.append(formattingStyle.format(*row) + '\n')
        
        else:
            len_1 = 0
            len_2 = 0
            len_3 = 0
            for row in text_table:
                if len(row[0]) > len_1:
                    len_1 = len(row[0])
                if len(row[1]) > len_2:
                    len_2 = len(row[1])
                if len(row[2]) > len_3:
                    len_3 = len(row[2])
            
            len_1 += 3
            len_2 += 3
            len_3 += 3
            for row in text_table:
                formattingStyle = "{: <" + str(len_1) + "} {: <" + str(len_2) + "} {: <" + str(len_2) + "}"
                text_list.append(formattingStyle.format(*row) + '\n')
        
        return text_list


    # Display the results of a user updating a device
    # This records the changed values in bold
    def displayDiff(self, original_list, new_list, textOut):
        # Has to be compared as strings
        has_changed = False
        for key in original_list:
            if str(original_list[key]).replace(" ", "").replace('\r', '').replace('\n', '') != str(new_list[key]).replace(" ", "").replace('\r', '').replace('\n', ''):
                has_changed = True
        
        if has_changed:
            textOut.append('**Device Updated:**\n')
            text_array = []
            for key in self.keysList:
                if key in original_list:
                    if key == "Remark":
                        text_array = self.wrapMultipleDiff(key, text_array, original_list[key], new_list[key])
                    else:
                        val1 = original_list[key]
                        val2 = new_list[key]
                        if str(val1).replace(" ", "").replace('\r', '').replace('\n', '') == str(val2).replace(" ", "").replace('\r', '').replace('\n', ''):
                            text_array.append([key+': ', str(val1), str(val2)])
                        else:
                            text_array.append([key+': ', str(val1), '**'+str(val2)+'**'])

            # Currently loggers are excluded
            if new_list['Communication Information'] == 'Yes' and new_list['Category'] != 'LOGGER':
                keys = self.commTypes[new_list['Category']]
                total = []
                changed = False
                for key in keys:
                    val1 = original_list[key]
                    val2 = new_list[key]
                    if str(val1).replace(" ", "").replace('\r', '').replace('\n', '') == str(val2).replace(" ", "").replace('\r', '').replace('\n', ''):
                        total.append([key+': ', str(val1), str(val2)])
                    else:
                        total.append([key+': ', str(val1), '**'+str(val2)+'**'])
                        changed = True
                if changed:
                    for val in total:
                        text_array.append(val)

            textOut = self.columnsTextFormat(text_array, textOut, 2)
        return textOut


    # Display the results of a user transferring a device
    # This records the changed values in bold
    def displayTransfer(self, title, base_list, original_list, new_list, textOut):
        textOut.append('**'+title+'**\n')
        text_array = []
        for key in self.keysList:
            if key in base_list:
                if key == "Remark":
                    text_array = self.wrapMultipleTrasnfer(key, text_array, base_list[key], original_list[key], new_list[key])
                else:
                    val0 = base_list[key]
                    val1 = original_list[key]
                    val2 = new_list[key]
                    displayVal1 = ''
                    displayVal2 = ''
                    if str(val0).replace(" ", "").replace('\r', '').replace('\n', '') == str(val1).replace(" ", "").replace('\r', '').replace('\n', ''):
                        displayVal1 = str(val1)
                    else:
                        displayVal1 = '**'+str(val1)+'**'
                    if str(val1).replace(" ", "").replace('\r', '').replace('\n', '') == str(val2).replace(" ", "").replace('\r', '').replace('\n', ''):
                        displayVal2 = str(val2)
                    else:
                        displayVal2 = '**'+str(val2)+'**'
                    
                    # Account for the distance being off because the **** have been removed in the markup file writing
                    if "**" in displayVal1:
                        displayVal2 = ' ' + ' ' + ' ' + ' ' + displayVal2
                    text_array.append([key+': ', displayVal1, displayVal2])

        # Currently loggers are excluded
        if (base_list['Communication Information'] == 'Yes' and base_list['Category'] != 'LOGGER') or \
            (new_list['Communication Information'] == 'Yes' and new_list['Category'] != 'LOGGER'):
            keys = self.commTypes[new_list['Category']]
            total = []
            changed = False
            for key in keys:
                val0 = base_list[key]
                val1 = original_list[key]
                val2 = new_list[key]
                displayVal1 = ''
                displayVal2 = ''
                if str(val0).replace(" ", "").replace('\r', '').replace('\n', '') == str(val1).replace(" ", "").replace('\r', '').replace('\n', ''):
                    displayVal1 = str(val1)
                else:
                    displayVal1 = '**'+str(val1)+'**'
                if str(val1).replace(" ", "").replace('\r', '').replace('\n', '') == str(val2).replace(" ", "").replace('\r', '').replace('\n', ''):
                    displayVal2 = str(val2)
                else:
                    displayVal2 = '**'+str(val2)+'**'
                
                # Account for the distance being off because the **** have been removed in the markup file writing
                if "**" in displayVal1:
                    displayVal2 = ' ' + ' ' + ' ' + ' ' + displayVal2
                total.append([key+': ', displayVal1, displayVal2])
                    
                if "**" in displayVal1 or "**" in displayVal2:    
                    changed = True
            if changed:
                for val in total:
                    text_array.append(val)

        textOut = self.columnsTextFormat(text_array, textOut, 2)
        return textOut
    

    # Display the results of a user adding a new device
    # This records the changed values in bold
    def displayNew(self, list, textOut):
        textOut.append('**Device Added:**\n')
        text_array = []
        for key in self.keysList:
            if key in list:            
                if key == "Remark":
                    if str(list[key]).replace(" ", "").replace('\r', '').replace('\n', '') != '':
                        wrapped_remark = wrap(str(list[key]), width=20)
                        for index, substring in enumerate(wrapped_remark):
                            if index == 0:
                                text_array.append([key+': ', str(substring)])
                            else:
                                text_array.append(['.', str(substring)])
                    else:
                        text_array.append([key+': ', ' '])
                else:
                    text_array.append([key+': ', str(list[key])])
        
        # Currently loggers are excluded
        if list['Communication Information'] == 'Yes' and list['Category'] != 'LOGGER':
            keys = self.commTypes[list['Category']]
            total = []
            changed = False
            for key in keys:
                val = list[key]
                total.append([key+': ', str(val)])
                if val != '':
                    changed = True
            if changed:
                for val in total:
                    text_array.append(val)
        
        textOut = self.columnsTextFormat(text_array, textOut, 1)
        return textOut



    def printChangesOutput(self):
        #self.Layout()
        #self.Update()
        #self.Refresh()
        
        # -------------------------------------------------------------------------
        # Get the saved state from the top table and update the saved top dataframe
        # -------------------------------------------------------------------------
        text_for_file = []
        if not self.top_table_dataframe.empty:
            
            # Get all the ID values
            table_ids = self.top_table_dataframe['dataset_index_marker'].tolist()
            for index in table_ids:

                start_len_text = len(text_for_file)
                top_row = self.top_table_dataframe[self.top_table_dataframe['dataset_index_marker'] == index].copy()

                # Case where the user has added a new row (_new)
                if 'new' in str(index):
                    self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                    text_for_file = self.displayNew(top_row.to_dict(orient='records')[0], text_for_file)
                    # Communication info is already obtained here in displayNew()

                # Case where this is a transfer
                elif 'transfer' in str(index):
                    bottom_row = self.bottom_storage_dataframe[self.bottom_storage_dataframe['dataset_index_marker'] == index].copy()
                    original_row = self.full_hydex_dataframe[self.full_hydex_dataframe['dataset_index_marker'] == int(index.split('_')[0])].copy()

                    # Transfered from top to bottom (_transfer_bottom)
                    if 'bottom' in str(index):
                        #self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                        text_for_file = self.displayTransfer('**Device Transferred to Warehouse:**', original_row.to_dict(orient='records')[0], top_row.to_dict(orient='records')[0], bottom_row.to_dict(orient='records')[0], text_for_file)
                
                    # Transfered from bottom to top (_transfer_top)
                    else:
                        self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                        text_for_file = self.displayTransfer('**Device Transferred to Station:**', original_row.to_dict(orient='records')[0], bottom_row.to_dict(orient='records')[0], top_row.to_dict(orient='records')[0], text_for_file)                
                    
                else:
                    # Case where the user has just changed values and nothing else
                    original_row = self.full_hydex_dataframe[self.full_hydex_dataframe['dataset_index_marker'] == index].copy()
                    self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                    text_for_file = self.displayDiff(original_row.to_dict(orient='records')[0], top_row.to_dict(orient='records')[0], text_for_file)
                
                # If there is details to add from this row, add a spacer
                if start_len_text < len(text_for_file):
                    text_for_file.append('\n\n')
                
            # Handle the comments box
            comments_txt = self.commentsCtrl.GetValue()
            if comments_txt != "":
                text_for_file.append('**Comments:**\n')
                comments_txt_wrapped = wrap(comments_txt, width=60)
                for line in comments_txt_wrapped:
                    text_for_file.append(line + '\n')
                text_for_file.append('\n\n')

            if len(text_for_file) > 0:

                # Delete the saved file if there is a previous copy
                if os.path.exists(self.dir + '\\AQ_Extracted_Data\\inventory_changes.md'):
                    os.remove(self.dir + '\\AQ_Extracted_Data\\inventory_changes.md')

                # Write the details to the markup file
                with open(self.dir + '\\AQ_Extracted_Data\\inventory_changes.md', "w") as saved_file:
                    for row in text_for_file:
                        saved_file.write(row)
                
                # Return the path to the file
                return self.dir + '\\AQ_Extracted_Data\\inventory_changes.md'
            
            else:
                return ""
        
        else:
            return ""
    


    def exportChangesOutput(self, savedFilePath):

        # This generates a markdown file and returns the filepath
        # Running this three times deliberately as some changes are not caught in initial call
        inventory_text_filepath = self.printChangesOutput()
        inventory_text_filepath = self.printChangesOutput()
        inventory_text_filepath = self.printChangesOutput()

        # If the filepath is not empty (nothing to save) and is a valid filepath
        if inventory_text_filepath != "":
            if self.valid(inventory_text_filepath):

                default_filename = self.topStation + "_" + self.getFormattedTime() + "_Inventory.md"
                
                if savedFilePath == "":
                    # Save file dialog box
                    FileSaveDialog = wx.FileDialog(self, "Inventory Management File save location", os.path.dirname(os.path.realpath(sys.argv[0])), default_filename, 'Markdown File (*.md)|*.md',
                                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)

                    # If the user cancels the choice, destroy the dialog and remove the saved file
                    if FileSaveDialog.ShowModal() == wx.ID_CANCEL:
                        FileSaveDialog.Destroy()
                        if os.path.exists(inventory_text_filepath):
                            os.remove(inventory_text_filepath)
                        return

                    # Get the saved filename and filepath
                    savedFilePath = FileSaveDialog.GetPath()

                    FileSaveDialog.Destroy()
                
                else:
                    savedFilePath = os.path.join(savedFilePath, default_filename)

                # If a filename of the same name exists at the location, then delete this first
                if os.path.exists(savedFilePath):
                    os.remove(savedFilePath)

                # Transfer the file from the prior location to the new location
                os.rename(inventory_text_filepath, savedFilePath)

                # Remove the old file
                if os.path.exists(inventory_text_filepath):
                    os.remove(inventory_text_filepath)

                return


    ########################################################################
    ########### This is a modified version of printChangesOutput ###########
    ########################################################################
    # This is used solely for testing purposes
    def printChangesOutputTesting(self, evt):
        #self.Layout()
        #self.Update()
        #self.Refresh()
        
        # -------------------------------------------------------------------------
        # Get the saved state from the top table and update the saved top dataframe
        # -------------------------------------------------------------------------
        text_for_file = []
        if not self.top_table_dataframe.empty:
            
            # Get all the ID values
            table_ids = self.top_table_dataframe['dataset_index_marker'].tolist()
            for index in table_ids:

                start_len_text = len(text_for_file)
                top_row = self.top_table_dataframe[self.top_table_dataframe['dataset_index_marker'] == index].copy()

                # Case where the user has added a new row (_new)
                if 'new' in str(index):
                    self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                    text_for_file = self.displayNew(top_row.to_dict(orient='records')[0], text_for_file)
                    # Communication info is already obtained here in displayNew()

                # Case where this is a transfer
                elif 'transfer' in str(index):
                    bottom_row = self.bottom_storage_dataframe[self.bottom_storage_dataframe['dataset_index_marker'] == index].copy()
                    original_row = self.full_hydex_dataframe[self.full_hydex_dataframe['dataset_index_marker'] == int(index.split('_')[0])].copy()

                    # Transfered from top to bottom (_transfer_bottom)
                    if 'bottom' in str(index):
                        #self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                        text_for_file = self.displayTransfer('**Device Transferred to Warehouse:**', original_row.to_dict(orient='records')[0], top_row.to_dict(orient='records')[0], bottom_row.to_dict(orient='records')[0], text_for_file)
                
                    # Transfered from bottom to top (_transfer_top)
                    else:
                        self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                        text_for_file = self.displayTransfer('**Device Transferred to Station:**', original_row.to_dict(orient='records')[0], bottom_row.to_dict(orient='records')[0], top_row.to_dict(orient='records')[0], text_for_file)                
                    
                else:
                    # Case where the user has just changed values and nothing else
                    original_row = self.full_hydex_dataframe[self.full_hydex_dataframe['dataset_index_marker'] == index].copy()
                    self.updateDataframeRow(top_row.index[top_row['dataset_index_marker'] == index].tolist()[0])
                    text_for_file = self.displayDiff(original_row.to_dict(orient='records')[0], top_row.to_dict(orient='records')[0], text_for_file)
                
                # If there is details to add from this row, add a spacer
                if start_len_text < len(text_for_file):
                    text_for_file.append('\n\n')
                
            # Handle the comments box
            comments_txt = self.commentsCtrl.GetValue()
            if comments_txt != "":
                text_for_file.append('**Comments:**\n')
                comments_txt_wrapped = wrap(comments_txt, width=60)
                for line in comments_txt_wrapped:
                    text_for_file.append(line + '\n')
                text_for_file.append('\n\n')

            # Print for display
            for line in text_for_file:
                print(line, end='')

            if len(text_for_file) > 0:

                # Delete the saved file if there is a previous copy
                if os.path.exists(self.dir + '\\AQ_Extracted_Data\\inventory_changes.md'):
                    os.remove(self.dir + '\\AQ_Extracted_Data\\inventory_changes.md')

                # Write the details to the markup file
                with open(self.dir + '\\AQ_Extracted_Data\\inventory_changes.md', "w") as saved_file:
                    for row in text_for_file:
                        saved_file.write(row)
                


def main():
    app = wx.App()

    frame = wx.Frame(None, size=(800, 800))
    InventoryManagementPanel("DEBUG", frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()
