# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
import wx.lib.agw.genericmessagedialog as GMD
import sys
import os
import requests

def Check(version, parent, alwaysShow):
    # myVersion = "v1.1.4"
    print "Version Checking"
    myVersion = version
    needUpdate = False
    msg = ''
    rank = None
    currentVersion = None

    if hasattr(sys, '_MEIPASS'):
        location = os.path.join(sys._MEIPASS)
    else:
        location = os.getcwd()

    try:
        message_url = "https://raw.githubusercontent.com/ECCC-MSC/WSC-EHSN/master/message.txt"
        response = requests.get(message_url)
        print (response.status_code)
        response.raise_for_status()
        #msg = response.content.decode('Windows-1252')  # TODO: Consider encoding the message file as UTF-8
        msg = response.content.decode('UTF-8')
        print msg
        print ""

        lines = msg.splitlines()
        currentVersion = lines[0][1:]
        rank = int(lines[1])

        myVersions = myVersion[1:].split('.')
        currentVersions = currentVersion.split('.')
        # if int(myVersions[0]) < int(currentVersions[0]):
        #     print "need to be updated\n" + msg
        # elif int(myVersions[0]) == int(currentVersions[0]):
        #     if int(myVersions[1]) < int(currentVersions[1]):
        #         print "need to be updated\n" + msg
        #     elif int(myVersions[1]) == int(currentVersions[1]):
        #         if int(myVersions[2]) < int(currentVersions[2]):
        #             print "need to be updated\n" + msg
        #         else:
        #             print "No update available"
        #     else:
        #         print "No update available"
        # else:
        #     print "No update available"

        if int(myVersions[0]) < int(currentVersions[0]):
            needUpdate = True
        elif int(myVersions[0]) == int(currentVersions[0]):
            if int(myVersions[1]) < int(currentVersions[1]):
                needUpdate = True
            elif int(myVersions[1]) == int(currentVersions[1]):
                if int(myVersions[2]) < int(currentVersions[2]):
                    needUpdate = True
                else:
                    needUpdate = False
                    msg = "No update available"
                    rank = 0
            else:
                needUpdate = False
                msg = "No update available"
                rank = 0
        else:
            needUpdate = False
            msg = "No update available"
            rank = 0
    except:
        print "Version checking failed"
        msg = "Check for updates failed"






    if needUpdate or msg != '':
        if not needUpdate:
            icon = wx.ICON_INFORMATION

        else:
            # msg = "There is a new version V" + currentVersion.strip('\n') + " available on FTP server\n\n\n" + msg
            if rank < 3:
                icon = wx.ICON_WARNING
                # icon = wx.Icon('icon_transparent.ico', wx.BITMAP_TYPE_ICO)
            else:
                icon = wx.ICON_ERROR
        if alwaysShow or needUpdate:
            AMDUD = GMD.GenericMessageDialog(parent, msg, "Check Updates", agwStyle=icon|wx.OK, style=wx.DEFAULT_DIALOG_STYLE|wx.WANTS_CHARS, wrap=500)


                # ico = wx.Icon('icon_transparent.ico', wx.BITMAP_TYPE_ICO)
                # AMDUD.SetIcon(ico)
            # AMDUD.WrapMessage(_msg, 60)
            AMDUD.Show()
            re = AMDUD.ShowModal()
            if re == wx.ID_YES:
                AMDUD.Destroy()

    return rank