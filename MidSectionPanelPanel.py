# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

import wx
from wx.grid import *
import math
import NumberControl
import sigfig
from DropdownTime import *
from MidSectionSubPanelObj import *
from win32api import GetSystemMetrics
# import win32gui

from time import clock

import time
import threading


class ThreadingControl(threading.Thread):
    def __init__(self, panel):
        threading.Thread.__init__(self)
        #flag to pause thread
        self.paused = False
        self.startRun = False
        self.panel = panel
        # Explicitly using Lock over RLock since the use of self.paused
        # break reentrancy anyway, and I believe using Lock could allow
        # one thread to pause the worker, while another resumes; haven't
        # checked if Condition imposes additional limitations that would 
        # prevent that. In Python 2, use of Lock instead of RLock also
        # boosts performance.
        self.pause_cond = threading.Condition(threading.Lock())
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.startRun = True
        while True:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()

                #thread should do the thing if
                #not paused
                # print 'do the thing'
             
                self.panel.timeTextCtrl.SetValue('%.1f' %(self.panel.MySW.Time() * 0.001))
            time.sleep(0.1)

    def pause(self):
        self.paused = True
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()

    #should just resume the thread
    def resume(self):
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()

#Overwrite the TextCtrl Class in order to control the float input
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(MyTextCtrl, self).__init__(*args, **kwargs)
        self.preValue = ""


class MidSectionPanelPanel(wx.Panel):
    def __init__(self, panelNum, modify, pid, nextTagMark="", *args, **kwargs):
        super(MidSectionPanelPanel, self).__init__(*args, **kwargs)
        self.nextTagMark = nextTagMark
        self.pid = pid
  
        self.panelNum = panelNum
        self.modify = modify
        self.titleLbl = "Panel #:"
        self.panelLbl = "Panel #:"
        self.currentMeterLbl = "Current Meter:"
        self.meterEquationLbl = "Meter Equation:"
        self.slopeLbl1 = "Slope #1:"
        self.interceptLbl1 = "Intercept #1:"
        self.slopeLbl2 = "Slope #2:"
        self.interceptLbl2 = "Intercept #2:"
        self.measurementTimeLbl = "Measurement Time:"
        self.panelTagMarkLbl = "Panel Tagmark (m):"
        self.panelConditionLbl = "Panel Condition:"
        self.openWaterLbl = "Open Water"
        self.IceLbl = "Ice"
        self.depthLbl = "Depth Reading (m):"
        self.amountWeightLbl = "Amount of Weight (lb):"
        self.weightOffsetLbl = "Weight to Meter Offset (m):"
        self.wldlLbl = "WL/DL Correction:"
        self.dryLineAngleLbl = "Dry Line Angle (deg.):"
        self.distSurfaceLbl = "Dist. to Water Surface (m):"
        self.dryCorrectionLbl = "Dry Line Correction:"
        self.wetCorretionLbl = "Wet Line Correction:"
        self.effectiveDepthLbl = "Effective Depth (m):"
        self.corrections = ["No", "Yes", "Yes_w_Tags"]

        self.iceAssemblyLbl = "Ice Assembly:"
        self.meterAboveLbl = "Meter Above Footing:"
        self.meterBelowLbl = "Meter Below Footing:"
        self.distanceAboveLbl = "Distance Above Weight (m):"
        self.iceThickLbl = "Ice Thickness (m):"
        self.waterSurfaceIceLbl = "WS to Bottom of Ice (m):"
        self.adjustedLbl = "Adjusted:"
        self.waterSurfaceSlushLbl = "WS to Bottom of Slush (m):"
        self.slushThicknessLbl = "Slush Thickness (m):"
        self.slushLbl = "Slush:                                                    "

        self.velocityMethodLbl = "Velocity Method:"
        self.obliqueLbl = "Angle of Flow Coefficient:"
        self.velocityCorrLbl = "Velocity Corr. Factor:"
        self.reverseFlowLbl = "Reverse Flow:"
        # self.depthPanelLockLbl = "Lock the Depth Panel"

        self.mandatoryFieldsMsg = "You are missing the field: "

        self.panelConditions = ["Open", "Ice"]
        self.velocityMethods = ["0.5", "0.6", "0.2/0.8", "0.2/0.6/0.8", "Surface"]
        self.iceAssemblySelections = ["No_Weight", "NACA", "Pancake", "Slush", "USGS_Tipup", "Ice_Rod"]
        self.weights = ["0", "15", "30", "50", "75", "100", "150", "300"]
        self.meterOffsets = ["0", "0.21", "0.22", "0.31", "0.32", "0.33", "0.55", "0.55"]
        self.velocityCorrFactors = ["1.0", "0.88", "0.92"]
        self.currentMeters = []

        self.rawAtPointVel = ["", "", ""]
        self.rawMeanVal = ""

        self.preVel02 = None
        self.preVel08 = None

        self.height = 21
        self.headerHeight = 28
        self.ctrlWidth = 60
        self.lblWidth = 150
        self.panelNumber = -1

        self.summaryLblWidth = 132
        self.summaryHeight = 20
        self.summaryCtrlWidth = 70

        self.openWidth = 150



        self.backgrounColour = (242,242,242)
        self.textColour = (54,96,146)

        self.saveBtnLbl = "Save && Exit"
        self.preBtnLbl = "<<<"
        self.cancelBtnLbl = "Cancel"
        self.nextBtnLbl = ">>>"
        self.saveNextBtnLbl = "Save && Next"

        self.newPanel = True

        self.MySW = None
        self.threadingControl = None


        self.InitUI()


        # GridUpdateLocker(self.velocityGrid)


    def InitUI(self):
        #Header
        sizerV = wx.BoxSizer(wx.VERTICAL)
        self.headerTxt = wx.StaticText(self, label=self.titleLbl + " " + str(self.panelNum), size=(-1, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        if GetSystemMetrics(11) < 33:
            headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        else:
            headerFont = wx.Font(15, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        self.headerTxt.SetFont(headerFont)
        self.headerTxt.SetBackgroundColour('grey')

        #Depth Summary
        summarySizer = wx.BoxSizer(wx.HORIZONTAL)
        summaryLeftSizer = wx.BoxSizer(wx.VERTICAL)
        summaryRightSizer = wx.BoxSizer(wx.VERTICAL)
        summarySizer.Add(summaryLeftSizer, 0, wx.EXPAND)
        summarySizer.Add(summaryRightSizer, 0, wx.EXPAND|wx.LEFT, 20)



        #Panel #
        panelNumberSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelNumberTxt = wx.StaticText(self, label=self.panelLbl, size=(self.summaryLblWidth, self.summaryHeight))
        self.panelNumberCtrl = MyTextCtrl(self, size=(self.summaryCtrlWidth, self.summaryHeight))
        self.panelNumberCtrl.SetValue(str(self.panelNum))
        self.panelNumberCtrl.Disable()

        panelNumberSizer.Add(panelNumberTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        panelNumberSizer.Add(self.panelNumberCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Measurement Time
        measurementTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        measurementTimeTxt = wx.StaticText(self, label=self.measurementTimeLbl, size=(self.summaryLblWidth, self.headerHeight))
        # self.measurementTimeCtrl = MyTextCtrl(self, size=(-1, self.height))
        self.measurementTimeCtrl = DropdownTime(False, parent=self, size=(-1, self.headerHeight), style=wx.BORDER_NONE)
        # self.measurementTimeCtrl.SetToCurrent()
        
        # self.measurementTimeCtrl.hourCmbox.SetSelection(-1, -1)
        # self.Refresh()
        # self.Layout()
        measurementTimeSizer.Add(measurementTimeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        measurementTimeSizer.Add(self.measurementTimeCtrl, 0, wx.EXPAND)


        #panel TagMark Distance (m)
        panelTagMarkSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelTagMarkTxt = wx.StaticText(self, label=self.panelTagMarkLbl, size=(self.summaryLblWidth, self.summaryHeight))
        self.panelTagMarkCtrl = MyTextCtrl(self, size=(self.summaryCtrlWidth, self.summaryHeight), style=wx.TE_PROCESS_ENTER)#|wx.TE_PROCESS_TAB)
        # self.panelTagMarkCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnTagmarkTabEnter)
        # self.panelTagMarkCtrl.Bind(wx.EVT_NAVIGATION_KEY, self.OnTagmarkTabEnter)
        self.panelTagMarkCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.panelTagMarkCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        
        # self.panelTagMarkCtrl.SetSelection(-1, -1)






        panelTagMarkSizer.Add(panelTagMarkTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        panelTagMarkSizer.Add(self.panelTagMarkCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        self.openWaterPanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(220, -1))
        self.openWaterPanel.Bind(wx.EVT_NAVIGATION_KEY, self.OnNavigate2Velocity)

        self.icePanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(340, -1))
        self.icePanel.Bind(wx.EVT_NAVIGATION_KEY, self.OnNavigate2Velocity)

        self.velocityPanel = wx.Panel(self)
        self.velocityPanel.Bind(wx.EVT_NAVIGATION_KEY, self.OnNavigate2Velocity)
        #First Panel
        if self.panelNum == 1:

            #############################START##############################           
            #Open
            

            # self.openDepthReadCtrl = wx.lib.masked.numctrl.NumCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            # self.openDepthReadCtrl.SetFractionWidth(2)
            # self.openDepthReadCtrl.SetAllowNone(True)
            self.openDepthReadCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.UpdateWetLineCorrection)
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.openDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

            self.amountWeightCmbox = wx.ComboBox(self.openWaterPanel, size=(self.ctrlWidth, self.height), choices=self.weights, style=wx.CB_READONLY)               
            self.wldlCorrectionCmbox = wx.ComboBox(self.openWaterPanel, size = (self.ctrlWidth, self.height), choices=self.corrections, style=wx.CB_READONLY)
            self.dryLineAngleCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.distWaterCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            

            
            #Ice
            
            self.iceAssemblyCmbbox = wx.ComboBox(self.icePanel, size = (90, self.height), choices=self.iceAssemblySelections, style=wx.CB_READONLY)            
            self.iceThickCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.waterSurfaceIceCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))


            # self.iceDepthReadCtrl = wx.lib.masked.numctrl.NumCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            # self.iceDepthReadCtrl.SetFractionWidth(2)
            # self.iceDepthReadCtrl.SetAllowNone(True)
            self.iceDepthReadCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.iceDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.iceDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        
            #Velocity Method

            self.velocityCombo = wx.ComboBox(self.velocityPanel, style=wx.CB_READONLY, choices=self.velocityMethods, size=(-1, self.height))

            #Velocity table
            self.velocityGrid = Grid(self.velocityPanel, size=(1, -1))
            self.velocityGrid.CreateGrid(3, 7)
            self.velocityGrid.TabBehaviour(Grid.Tab_Leave)

            #####################After Grid######################
            #Open
            self.weightOffsetCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.dryLineCorrectionCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.wetLineCorrectionCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))



            # self.OpenEffectiveDepthCtrl = wx.lib.masked.numctrl.NumCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            # self.OpenEffectiveDepthCtrl.SetFractionWidth(2)
            # self.OpenEffectiveDepthCtrl.SetAllowNone(True)
            self.OpenEffectiveDepthCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.OpenEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.OpenEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

            #Ice

            # self.iceEffectiveDepthCtrl = wx.lib.masked.numctrl.NumCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            # self.iceEffectiveDepthCtrl.SetFractionWidth(2)
            # self.iceEffectiveDepthCtrl.SetAllowNone(True)
            self.iceEffectiveDepthCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.iceEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.iceEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

            self.meterAboveCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.meterBelowCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.distanceAboveCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.slushCkbox = wx.CheckBox(self.icePanel, label=self.slushLbl, style=wx.ALIGN_RIGHT)
            self.waterSurfaceSlushCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

            self.iceThickAdjustedCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.waterIceAdjustCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.slushThicknessCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

            ###########################END#################################


        #Quick
        else:
            #############################START##############################
            #Privious Panel

            # tabOrderWldl = True
            # for index, obj in enumerate(self.GetParent().GetParent().GetParent().panelObjs):
            #     if isinstance(obj, PanelObj) and obj.panelNum == self.panelNum - 1:
            #         if obj.panelCondition == "Open" and obj.wldl == "No":
            #             tabOrderWldl = False
            #         break




            #Open
            # self.openWaterPanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(220, -1))
            # self.openDepthReadCtrl = wx.lib.masked.numctrl.NumCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            # self.openDepthReadCtrl.SetFractionWidth(2)
            # self.openDepthReadCtrl.SetAllowNone(True)
            self.openDepthReadCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.UpdateWetLineCorrection)
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
            self.openDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.openDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
            # if tabOrderWldl:
            self.wldlCorrectionCmbox = wx.ComboBox(self.openWaterPanel, size = (self.ctrlWidth, self.height), choices=self.corrections, style=wx.CB_READONLY)
            self.dryLineAngleCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.distWaterCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))

            
            #Ice
            # self.icePanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(340, -1))   

            self.iceThickCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.waterSurfaceIceCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

            self.iceDepthReadCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.iceDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.iceDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
            
        
            #Velocity Method
            # self.velocityPanel = wx.Panel(self)
            self.velocityCombo = wx.ComboBox(self.velocityPanel, style=wx.CB_READONLY, choices=self.velocityMethods, size=(-1, self.height))

            #Velocity table
            self.velocityGrid = Grid(self.velocityPanel, size=(1, -1))
            self.velocityGrid.CreateGrid(3, 7)
            self.velocityGrid.TabBehaviour(Grid.Tab_Leave)

            #####################After Grid######################
            #Open
            self.amountWeightCmbox = wx.ComboBox(self.openWaterPanel, size=(self.ctrlWidth, self.height), choices=self.weights, style=wx.CB_READONLY)               
            self.weightOffsetCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.dryLineCorrectionCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.wetLineCorrectionCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            

            # self.OpenEffectiveDepthCtrl = wx.lib.masked.numctrl.NumCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            # self.OpenEffectiveDepthCtrl.SetFractionWidth(2)
            # self.OpenEffectiveDepthCtrl.SetAllowNone(True)
            self.OpenEffectiveDepthCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
            self.OpenEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.OpenEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
            

            # if not tabOrderWldl:
                # self.wldlCorrectionCmbox = wx.ComboBox(self.openWaterPanel, size = (self.ctrlWidth, self.height), choices=self.corrections, style=wx.CB_READONLY)
                # self.dryLineAngleCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
                # self.distWaterCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))

            #Ice
            self.iceAssemblyCmbbox = wx.ComboBox(self.icePanel, size = (90, self.height), choices=self.iceAssemblySelections, style=wx.CB_READONLY)
            

            # self.iceDepthReadCtrl = wx.lib.masked.numctrl.NumCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            # self.iceDepthReadCtrl.SetFractionWidth(2)
            # self.iceDepthReadCtrl.SetAllowNone(True)
            
            

            # self.iceEffectiveDepthCtrl = wx.lib.masked.numctrl.NumCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            # self.iceEffectiveDepthCtrl.SetFractionWidth(2)
            # self.iceEffectiveDepthCtrl.SetAllowNone(True)
            self.iceEffectiveDepthCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

            self.iceEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
            self.iceEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)


            self.meterAboveCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.meterBelowCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.distanceAboveCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.slushCkbox = wx.CheckBox(self.icePanel, label=self.slushLbl, style=wx.ALIGN_RIGHT)
            self.waterSurfaceSlushCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

            self.iceThickAdjustedCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.waterIceAdjustCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
            self.slushThicknessCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))

            ###########################END#################################




        #Panel Condition
        self.panelConditionCombox = wx.ComboBox(self, style=wx.CB_READONLY, choices=self.panelConditions, size=(self.summaryCtrlWidth, self.summaryHeight))
        panelConditionSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelConditionTxt = wx.StaticText(self, label=self.panelConditionLbl, size=(self.summaryLblWidth, self.summaryHeight))


        panelConditionSizer.Add(panelConditionTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        panelConditionSizer.Add(self.panelConditionCombox, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        self.panelConditionCombox.SetSelection(0)

        summaryLeftSizer.Add(panelNumberSizer, 1, wx.EXPAND)
        summaryLeftSizer.Add(measurementTimeSizer, 1, wx.EXPAND)
        summaryLeftSizer.Add(panelTagMarkSizer, 1, wx.EXPAND)
        summaryLeftSizer.Add(panelConditionSizer, 1, wx.EXPAND)



        #Current Meter
        currentMeterSizer = wx.BoxSizer(wx.HORIZONTAL)
        currentMeterTxt = wx.StaticText(self, label=self.currentMeterLbl, size=(-1, self.summaryHeight))
        # self.currentMeterCtrl = MyTextCtrl(self, size=(-1, self.summaryHeight))
        self.currentMeterCtrl = wx.ComboBox(self, size=(-1, self.summaryHeight), choices=self.currentMeters)
        self.currentMeterCtrl.Bind(wx.EVT_COMBOBOX, self.OnCurrMeterCtrl)
        currentMeterSizer.Add(currentMeterTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        currentMeterSizer.Add(self.currentMeterCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        # #Meter Equation
        # meterEquationSizer = wx.BoxSizer(wx.HORIZONTAL)
        # meterEquationTxt = wx.StaticText(self, label=self.meterEquationLbl, size=(-1, self.summaryHeight))
        # meterEquationSizer.Add(meterEquationTxt, 1, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        slopeInterceptSizer = wx.BoxSizer(wx.HORIZONTAL)
        #Radio button 1
        self.slopBtn1 = wx.RadioButton(self, style=wx.RB_GROUP)
        self.slopBtn1.Bind(wx.EVT_RADIOBUTTON, self.OnSlopeRadioBtn)


        #Slope
        slopeSizer = wx.BoxSizer(wx.HORIZONTAL)
        slopeTxt = wx.StaticText(self, label=self.slopeLbl1, size=(50, self.summaryHeight))
        self.slopeCtrl = MyTextCtrl(self, size=(50, self.summaryHeight))
        self.slopeCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.slopeCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)

        slopeSizer.Add(slopeTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        slopeSizer.Add(self.slopeCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Intercept
        interceptSizer = wx.BoxSizer(wx.HORIZONTAL)
        interceptTxt = wx.StaticText(self, label=self.interceptLbl1, size=(70, self.summaryHeight))
        self.interceptCtrl = MyTextCtrl(self, size=(50, self.summaryHeight))
        self.interceptCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.interceptCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)

        interceptSizer.Add(interceptTxt, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        interceptSizer.Add(self.interceptCtrl, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        slopeInterceptSizer.Add(self.slopBtn1, 0)
        slopeInterceptSizer.Add(slopeSizer, 0)
        slopeInterceptSizer.Add(interceptSizer, 0)

        #second slop and intercept pair
        slopeInterceptSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        #Radio button 2
        self.slopBtn2 = wx.RadioButton(self)
        self.slopBtn2.Bind(wx.EVT_RADIOBUTTON, self.OnSlopeRadioBtn)
        # self.slopBtn2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)


        #Slop
        slopeSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        slopeTxt2 = wx.StaticText(self, label=self.slopeLbl2, size=(50, self.summaryHeight))
        self.slopeCtrl2 = MyTextCtrl(self, size=(50, self.summaryHeight))
        self.slopeCtrl2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.slopeCtrl2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.slopeCtrl2.Enable(False)

        slopeSizer2.Add(slopeTxt2, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        slopeSizer2.Add(self.slopeCtrl2, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)

        #Intercept
        interceptSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        interceptTxt2 = wx.StaticText(self, label=self.interceptLbl2, size=(70, self.summaryHeight))
        self.interceptCtrl2 = MyTextCtrl(self, size=(50, self.summaryHeight))
        self.interceptCtrl2.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.interceptCtrl2.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round4)
        self.interceptCtrl2.Enable(False)

        interceptSizer2.Add(interceptTxt2, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)
        interceptSizer2.Add(self.interceptCtrl2, 0, wx.LEFT|wx.RIGHT, 4, wx.EXPAND)


        slopeInterceptSizer2.Add(self.slopBtn2, 0)
        slopeInterceptSizer2.Add(slopeSizer2, 0)
        slopeInterceptSizer2.Add(interceptSizer2, 0)



        # meterEquationSizer.Add(slopeSizer, 1, wx.EXPAND)
        # meterEquationSizer.Add(interceptSizer, 1, wx.EXPAND)

        summaryRightSizer.Add(currentMeterSizer, 0, wx.EXPAND)
        # summaryRightSizer.Add(meterEquationSizer, 1, wx.EXPAND)
        summaryRightSizer.Add(slopeInterceptSizer, 0, wx.EXPAND|wx.TOP, 5)
        summaryRightSizer.Add(slopeInterceptSizer2, 0, wx.EXPAND|wx.TOP, 5)
        # summaryRightSizer.Add(interceptSizer, 1, wx.EXPAND)





        #Depth table for open water
        # self.openWaterPanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(220, -1))
        openWaterSizer = wx.BoxSizer(wx.VERTICAL)
        self.openWaterPanel.SetSizer(openWaterSizer)

        openDepthReadSizer = wx.BoxSizer(wx.HORIZONTAL)
        openDepthReadTxt = wx.StaticText(self.openWaterPanel, label=self.depthLbl, size = (self.openWidth, self.height))

        


        openDepthReadSizer.Add(openDepthReadTxt, 0, wx.EXPAND)
        openDepthReadSizer.Add(self.openDepthReadCtrl, 0, wx.EXPAND)

        amountWeightSizer = wx.BoxSizer(wx.HORIZONTAL)
        amountWeightTxt = wx.StaticText(self.openWaterPanel, label=self.amountWeightLbl, size = (self.openWidth, self.height))
        # self.amountWeightCmbox = wx.ComboBox(self.openWaterPanel, size=(self.ctrlWidth, self.height), choices=self.weights, style=wx.CB_READONLY)

        
        amountWeightSizer.Add(amountWeightTxt, 0, wx.EXPAND)
        amountWeightSizer.Add(self.amountWeightCmbox, 0, wx.EXPAND)

        weightOffsetSizer = wx.BoxSizer(wx.HORIZONTAL)
        weightOffsetTxt = wx.StaticText(self.openWaterPanel, label=self.weightOffsetLbl, size = (self.openWidth, self.height))

        # self.weightOffsetCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        
        self.weightOffsetCtrl.SetBackgroundColour(self.backgrounColour)
        self.weightOffsetCtrl.SetForegroundColour(self.textColour)
        weightOffsetSizer.Add(weightOffsetTxt, 0, wx.EXPAND)
        weightOffsetSizer.Add(self.weightOffsetCtrl, 0, wx.EXPAND)

        wldlCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        wldlCorrectionTxt = wx.StaticText(self.openWaterPanel, label=self.wldlLbl, size = (self.openWidth, self.height))
        # self.wldlCorrectionCmbox = wx.ComboBox(self.openWaterPanel, size = (self.ctrlWidth, self.height), choices=self.corrections, style=wx.CB_READONLY)

        wldlCorrectionSizer.Add(wldlCorrectionTxt, 0, wx.EXPAND)
        wldlCorrectionSizer.Add(self.wldlCorrectionCmbox, 0, wx.EXPAND)

        dryLineSizer = wx.BoxSizer(wx.HORIZONTAL)
        dryLineTxt = wx.StaticText(self.openWaterPanel, label=self.dryLineAngleLbl, size = (self.openWidth, self.height))
        # self.dryLineAngleCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.dryLineAngleCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl) 
        self.dryLineAngleCtrl.Enable(False)

 
        dryLineSizer.Add(dryLineTxt, 0, wx.EXPAND)
        dryLineSizer.Add(self.dryLineAngleCtrl, 0, wx.EXPAND)

        distWaterSizer = wx.BoxSizer(wx.HORIZONTAL)
        distWaterTxt = wx.StaticText(self.openWaterPanel, label=self.distSurfaceLbl, size = (self.openWidth, self.height))
        # self.distWaterCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.distWaterCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.distWaterCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        self.distWaterCtrl.Enable(False)

        distWaterSizer.Add(distWaterTxt, 0, wx.EXPAND)
        distWaterSizer.Add(self.distWaterCtrl, 0, wx.EXPAND)

        dryLineCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        dryLineCorrectionTxt = wx.StaticText(self.openWaterPanel, label=self.dryCorrectionLbl, size = (self.openWidth, self.height))
        # self.dryLineCorrectionCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.dryLineCorrectionCtrl.Enable(False)
        self.dryLineCorrectionCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.dryLineCorrectionCtrl.SetBackgroundColour(self.backgrounColour)
        self.dryLineCorrectionCtrl.SetForegroundColour(self.textColour)
        dryLineCorrectionSizer.Add(dryLineCorrectionTxt, 0, wx.EXPAND)
        dryLineCorrectionSizer.Add(self.dryLineCorrectionCtrl, 0, wx.EXPAND)

        wetLineCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        wetLineCorrectionTxt = wx.StaticText(self.openWaterPanel, label=self.wetCorretionLbl, size = (self.openWidth, self.height))
        # self.wetLineCorrectionCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        self.wetLineCorrectionCtrl.Enable(False)
        self.wetLineCorrectionCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.wetLineCorrectionCtrl.SetBackgroundColour(self.backgrounColour)
        self.wetLineCorrectionCtrl.SetForegroundColour(self.textColour)
        wetLineCorrectionSizer.Add(wetLineCorrectionTxt, 0, wx.EXPAND)
        wetLineCorrectionSizer.Add(self.wetLineCorrectionCtrl, 0, wx.EXPAND)

        effectiveDepthSizer = wx.BoxSizer(wx.HORIZONTAL)
        effectiveDepthLbl = wx.StaticText(self.openWaterPanel, label=self.effectiveDepthLbl, size = (self.openWidth, self.height))
        # self.OpenEffectiveDepthCtrl = MyTextCtrl(self.openWaterPanel, size = (self.ctrlWidth, self.height))
        
        self.OpenEffectiveDepthCtrl.SetBackgroundColour(self.backgrounColour)
        self.OpenEffectiveDepthCtrl.SetForegroundColour(self.textColour)
        effectiveDepthSizer.Add(effectiveDepthLbl, 0, wx.EXPAND)
        effectiveDepthSizer.Add(self.OpenEffectiveDepthCtrl, 0, wx.EXPAND)

        openWaterSizer.Add(openDepthReadSizer, 0, wx.EXPAND)
        openWaterSizer.Add(amountWeightSizer, 0, wx.EXPAND)
        openWaterSizer.Add(weightOffsetSizer, 0, wx.EXPAND)
        openWaterSizer.Add(wldlCorrectionSizer, 0, wx.EXPAND)
        openWaterSizer.Add(dryLineSizer, 0, wx.EXPAND)
        openWaterSizer.Add(distWaterSizer, 0, wx.EXPAND)
        openWaterSizer.Add(dryLineCorrectionSizer, 0, wx.EXPAND)
        openWaterSizer.Add(wetLineCorrectionSizer, 0, wx.EXPAND)
        openWaterSizer.Add(effectiveDepthSizer, 0, wx.EXPAND)

        # self.openWaterPanel.Hide()

        #Depth table for Ice
        # self.icePanel = wx.Panel(self, style=wx.BORDER_SIMPLE, size=(340, -1))
        iceSizer = wx.BoxSizer(wx.VERTICAL)
        self.icePanel.SetSizer(iceSizer)

        iceDepthReadSizer = wx.BoxSizer(wx.HORIZONTAL)
        iceDepthReadTxt = wx.StaticText(self.icePanel, label=self.depthLbl, size = (self.lblWidth, self.height))
        # self.iceDepthReadCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        # self.iceDepthReadCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        # self.iceDepthReadCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round3)

        iceDepthReadSizer.Add(iceDepthReadTxt, 0, wx.EXPAND)
        iceDepthReadSizer.Add(self.iceDepthReadCtrl, 0, wx.EXPAND)

        iceAssemblySizer = wx.BoxSizer(wx.HORIZONTAL)
        iceAssemblyTxt = wx.StaticText(self.icePanel, label=self.iceAssemblyLbl, size = (self.lblWidth, self.height))
        # self.iceAssemblyCmbbox = wx.ComboBox(self.icePanel, size = (90, self.height), choices=self.iceAssemblySelections, style=wx.CB_READONLY)
        # self.iceAssemblyCmbbox.MoveAfterInTabOrder(self.panelConditionCombox)
        iceAssemblySizer.Add(iceAssemblyTxt, 0, wx.EXPAND)
        iceAssemblySizer.Add(self.iceAssemblyCmbbox, 0, wx.EXPAND)

        meterAboveSizer = wx.BoxSizer(wx.HORIZONTAL)
        meterAboveTxt = wx.StaticText(self.icePanel, label=self.meterAboveLbl, size = (self.lblWidth, self.height))
        # self.meterAboveCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.meterAboveCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        

        self.meterAboveCtrl.SetBackgroundColour(self.backgrounColour)
        self.meterAboveCtrl.SetForegroundColour(self.textColour)

        meterAboveSizer.Add(meterAboveTxt, 0, wx.EXPAND)
        meterAboveSizer.Add(self.meterAboveCtrl, 0, wx.EXPAND)

        meterBelowSizer = wx.BoxSizer(wx.HORIZONTAL)
        meterBelowTxt = wx.StaticText(self.icePanel, label=self.meterBelowLbl, size = (self.lblWidth, self.height))
        # self.meterBelowCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.meterBelowCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        
        self.meterBelowCtrl.SetBackgroundColour(self.backgrounColour)
        self.meterBelowCtrl.SetForegroundColour(self.textColour)
        meterBelowSizer.Add(meterBelowTxt, 0, wx.EXPAND)
        meterBelowSizer.Add(self.meterBelowCtrl, 0, wx.EXPAND)

        distanceAboveSizer = wx.BoxSizer(wx.HORIZONTAL)
        distanceAboveTxt = wx.StaticText(self.icePanel, label=self.distanceAboveLbl, size = (self.lblWidth, self.height))
        # self.distanceAboveCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.distanceAboveCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        
        self.distanceAboveCtrl.SetBackgroundColour(self.backgrounColour)
        self.distanceAboveCtrl.SetForegroundColour(self.textColour)
        distanceAboveSizer.Add(distanceAboveTxt, 0, wx.EXPAND)
        distanceAboveSizer.Add(self.distanceAboveCtrl, 0, wx.EXPAND)

        iceThickRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        iceThickSizer = wx.BoxSizer(wx.HORIZONTAL)
        iceThickTxt = wx.StaticText(self.icePanel, label=self.iceThickLbl, size=(self.lblWidth, self.height))
        iceThickAdjustedSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.iceThickCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.iceThickCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

        iceThickAdjustedTxt = wx.StaticText(self.icePanel, label=self.adjustedLbl)
        # self.iceThickAdjustedCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.iceThickAdjustedCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        self.iceThickAdjustedCtrl.SetBackgroundColour(self.backgrounColour)
        self.iceThickAdjustedCtrl.SetForegroundColour(self.textColour)


        iceThickAdjustedSizer.Add(iceThickAdjustedTxt, 0, wx.EXPAND)
        iceThickAdjustedSizer.Add(self.iceThickAdjustedCtrl, 0, wx.EXPAND)

        iceThickSizer.Add(iceThickTxt, 0, wx.EXPAND)
        iceThickSizer.Add(self.iceThickCtrl, 0, wx.EXPAND)

        iceThickRowSizer.Add(iceThickSizer, 1, wx.EXPAND)
        iceThickRowSizer.Add(iceThickAdjustedSizer, 1, wx.EXPAND)


        waterSufaceRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        waterSurfaceIceSizer = wx.BoxSizer(wx.HORIZONTAL)
        waterSurfaceIceTxt = wx.StaticText(self.icePanel, label=self.waterSurfaceIceLbl, size = (self.lblWidth, self.height))
        waterAdjustSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.waterSurfaceIceCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.waterSurfaceIceCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)



        waterIceAdjustTxt = wx.StaticText(self.icePanel, label=self.adjustedLbl, size = (-1, self.height))
        # self.waterIceAdjustCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.waterIceAdjustCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        self.waterIceAdjustCtrl.SetBackgroundColour(self.backgrounColour)
        self.waterIceAdjustCtrl.SetForegroundColour(self.textColour)


        waterAdjustSizer.Add(waterIceAdjustTxt, 0, wx.EXPAND)
        waterAdjustSizer.Add(self.waterIceAdjustCtrl, 0, wx.EXPAND)



        waterSurfaceIceSizer.Add(waterSurfaceIceTxt, 0, wx.EXPAND)
        waterSurfaceIceSizer.Add(self.waterSurfaceIceCtrl, 0, wx.EXPAND)



        waterSufaceRowSizer.Add(waterSurfaceIceSizer, 1, wx.EXPAND)
        waterSufaceRowSizer.Add(waterAdjustSizer, 1, wx.EXPAND)



        # self.slushCkbox = wx.CheckBox(self.icePanel, label=self.slushLbl, style=wx.ALIGN_RIGHT)
        self.slushCkbox.Bind(wx.EVT_CHECKBOX, self.OnSlushCkbox)



        waterSurfaceSlushSizer = wx.BoxSizer(wx.HORIZONTAL)
        waterSurfaceSlushTxt = wx.StaticText(self.icePanel, label=self.waterSurfaceSlushLbl, size = (self.lblWidth, self.height))

        # self.waterSurfaceSlushCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.waterSurfaceSlushCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        self.waterSurfaceSlushCtrl.Enable(False)

        waterSurfaceSlushSizer.Add(waterSurfaceSlushTxt, 0, wx.EXPAND)
        waterSurfaceSlushSizer.Add(self.waterSurfaceSlushCtrl, 0, wx.EXPAND)

        slushThicknessSizer = wx.BoxSizer(wx.HORIZONTAL)
        slushThicknessTxt = wx.StaticText(self.icePanel, label=self.slushThicknessLbl, size = (self.lblWidth, self.height))
        # self.slushThicknessCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        self.slushThicknessCtrl.SetBackgroundColour(self.backgrounColour)
        self.slushThicknessCtrl.SetForegroundColour(self.textColour)

        slushThicknessSizer.Add(slushThicknessTxt, 0, wx.EXPAND)
        slushThicknessSizer.Add(self.slushThicknessCtrl, 0, wx.EXPAND)

        effectiveDepthSizer = wx.BoxSizer(wx.HORIZONTAL)
        effectiveDepthLbl = wx.StaticText(self.icePanel, label=self.effectiveDepthLbl, size = (self.lblWidth, self.height))
        # self.iceEffectiveDepthCtrl = MyTextCtrl(self.icePanel, size = (self.ctrlWidth, self.height))
        # self.iceEffectiveDepthCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        # self.iceEffectiveDepthCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)
        self.iceEffectiveDepthCtrl.SetBackgroundColour(self.backgrounColour)
        self.iceEffectiveDepthCtrl.SetForegroundColour(self.textColour)
        effectiveDepthSizer.Add(effectiveDepthLbl, 0, wx.EXPAND)
        effectiveDepthSizer.Add(self.iceEffectiveDepthCtrl, 0, wx.EXPAND)

        
        iceSizer.Add(iceAssemblySizer, 0, wx.EXPAND)
        iceSizer.Add(meterAboveSizer, 0, wx.EXPAND)
        iceSizer.Add(meterBelowSizer, 0, wx.EXPAND)
        iceSizer.Add(distanceAboveSizer, 0, wx.EXPAND)
        iceSizer.Add(iceThickRowSizer, 0, wx.EXPAND)
        iceSizer.Add(waterSufaceRowSizer, 0, wx.EXPAND)
        # iceSizer.Add(waterAdjustSizer, 0, wx.EXPAND)
        iceSizer.Add(self.slushCkbox, 0)
        iceSizer.Add(waterSurfaceSlushSizer, 0, wx.EXPAND)
        iceSizer.Add(slushThicknessSizer, 0, wx.EXPAND)
        iceSizer.Add(iceDepthReadSizer, 0, wx.EXPAND)
        iceSizer.Add(effectiveDepthSizer, 0, wx.EXPAND)

        self.icePanel.Hide()
        #################################


        #Velocity Summary
        

        velocitySummarySizer = wx.BoxSizer(wx.HORIZONTAL)

        velocityLeftSizer = wx.BoxSizer(wx.VERTICAL)

        velocityMethodSizer = wx.BoxSizer(wx.HORIZONTAL)

        velocitySizer = wx.BoxSizer(wx.VERTICAL)
        self.velocityPanel.SetSizer(velocitySizer)
        velocityLbl = wx.StaticText(self.velocityPanel, label=self.velocityMethodLbl, size = (-1, self.height))
        

        velocityMethodSizer.Add(velocityLbl, 0, wx.EXPAND)
        velocityMethodSizer.Add(self.velocityCombo, 0, wx.EXPAND|wx.LEFT, 10)


        # self.depthPanelLockCkbox = wx.CheckBox(self.velocityPanel, label=self.depthPanelLockLbl)
        # self.depthPanelLockCkbox.Bind(wx.EVT_CHECKBOX, self.OnDepthPanelLockCkbox)


        # velocityLeftSizer.Add(self.depthPanelLockCkbox, 1, wx.EXPAND|wx.TOP, 5)
        velocityLeftSizer.Add((-1, -1), 1, wx.EXPAND|wx.TOP, 5)
        velocityLeftSizer.Add((-1, -1), 1, wx.EXPAND|wx.TOP, 5)
        velocityLeftSizer.Add(velocityMethodSizer, 1, wx.EXPAND|wx.TOP, 5)

        velocityRightSizer = wx.BoxSizer(wx.VERTICAL)

        obliqueSizer = wx.BoxSizer(wx.HORIZONTAL)
        obliqueLbl = wx.StaticText(self.velocityPanel, label=self.obliqueLbl, size = (self.lblWidth, self.height))
        self.obliqueCtrl = MyTextCtrl(self.velocityPanel, size = (self.ctrlWidth, self.height))
        self.obliqueCtrl.Bind(wx.EVT_TEXT, NumberControl.FloatNumberControl)
        self.obliqueCtrl.Bind(wx.EVT_KILL_FOCUS, NumberControl.Round2)

        obliqueSizer.Add(obliqueLbl, 0, wx.EXPAND)
        obliqueSizer.Add(self.obliqueCtrl, 0, wx.EXPAND)

        velocityCorrectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        velocityCorrectionLbl = wx.StaticText(self.velocityPanel, label=self.velocityCorrLbl, size = (self.lblWidth, self.height))
        # self.velocityCorrectionCtrl = wx.ComboBox(self.velocityPanel, size = (-1, self.height), choices=self.velocityCorrFactors, style=wx.CB_DROPDOWN)
        self.velocityCorrectionCtrl = MyTextCtrl(self.velocityPanel, size = (self.ctrlWidth, self.height))
        self.velocityCorrectionCtrl.SetBackgroundColour(self.backgrounColour)
        self.velocityCorrectionCtrl.SetForegroundColour(self.textColour)
        velocityCorrectionSizer.Add(velocityCorrectionLbl, 0, wx.EXPAND)
        velocityCorrectionSizer.Add(self.velocityCorrectionCtrl, 0, wx.EXPAND)

        reverseSizer = wx.BoxSizer(wx.HORIZONTAL)
        # reverseLbl = wx.StaticText(self.velocityPanel, label=self.reverseFlowLbl, size = (-1, self.height))
        self.reverseCkbox = wx.CheckBox(self.velocityPanel, label=self.reverseFlowLbl)#, style=wx.ALIGN_RIGHT)

        # reverseSizer.Add(reverseLbl, 1, wx.EXPAND)
        reverseSizer.Add(self.reverseCkbox, 1, wx.EXPAND|wx.ALIGN_LEFT)

        velocityRightSizer.Add(obliqueSizer, 1, wx.EXPAND|wx.TOP, 5)
        velocityRightSizer.Add(velocityCorrectionSizer, 1, wx.EXPAND|wx.TOP, 5)
        velocityRightSizer.Add(reverseSizer, 1, wx.EXPAND|wx.TOP|wx.ALIGN_LEFT, 5)

        velocitySummarySizer.Add(velocityLeftSizer, 1, wx.EXPAND|wx.RIGHT, 30)
        velocitySummarySizer.Add(velocityRightSizer, 1, wx.EXPAND)

        velocitySizer.Add(velocitySummarySizer, 0, wx.EXPAND)


        

        self.velocityGrid.SetColLabelValue(0, "%Depth")
        self.velocityGrid.SetColLabelValue(1, "Depth\n of Obs (m)")
        self.velocityGrid.SetColLabelValue(2, "Revs.")
        self.velocityGrid.SetColLabelValue(3, "Time (s)")
        self.velocityGrid.SetColLabelValue(4, "At point\n vel. (m/s)")
        self.velocityGrid.SetColLabelValue(5, "Mean vel.\n(m/s)")
        self.velocityGrid.SetColLabelValue(6, "Corr. mean vel.\n (m/s)")

        self.velocityGrid.SetColSize(0, 50)
        self.velocityGrid.SetColSize(1, 70)
        self.velocityGrid.SetColSize(2, 50)
        self.velocityGrid.SetColSize(3, 50)
        self.velocityGrid.SetColSize(4, 70)
        self.velocityGrid.SetColSize(5, 70)
        self.velocityGrid.SetColSize(6, 85)


        self.velocityGrid.SetCellBackgroundColour(0, 4, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(1, 4, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(2, 4, self.backgrounColour)


        self.velocityGrid.SetCellTextColour(0, 4, self.textColour)
        self.velocityGrid.SetCellTextColour(1, 4, self.textColour)
        self.velocityGrid.SetCellTextColour(2, 4, self.textColour)


        self.velocityGrid.SetCellBackgroundColour(0, 1, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(1, 1, self.backgrounColour)
        self.velocityGrid.SetCellBackgroundColour(2, 1, self.backgrounColour)


        self.velocityGrid.SetCellTextColour(0, 1, self.textColour)
        self.velocityGrid.SetCellTextColour(1, 1, self.textColour)
        self.velocityGrid.SetCellTextColour(2, 1, self.textColour)

        self.velocityGrid.SetCellBackgroundColour(0, 5, self.backgrounColour)
        self.velocityGrid.SetCellTextColour(0, 5, self.textColour)

        self.velocityGrid.SetCellBackgroundColour(0, 6, self.backgrounColour)
        self.velocityGrid.SetCellTextColour(0, 6, self.textColour)


        self.velocityGrid.SetCellSize(0, 5, 3, 1)
        self.velocityGrid.SetCellSize(0, 6, 3, 1)

        self.velocityGrid.SetColFormatFloat(1, precision=2)
        self.velocityGrid.SetColFormatFloat(2, precision=0)
        self.velocityGrid.SetColFormatFloat(3, precision=1)
        # Below are now commented out because I manually put 3sigfig each time I set values for those columns
        self.velocityGrid.SetColFormatFloat(4, precision=3)
        self.velocityGrid.SetColFormatFloat(5, precision=3)
        self.velocityGrid.SetColFormatFloat(6, precision=3)

        # self.velocityGrid.GetCellEditor(2, 0).SetControl(wx.Control(self))


        #This line is the contoller for the timer(Muluken)
        self.velocityGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.StopWatchTimer)




        self.velocityGrid.SetRowLabelSize(0)
        velocitySizer.Add(self.velocityGrid, 0, wx.EXPAND|wx.TOP, 5)



        #button panel
        buttonPanel = wx.Panel(self, style=wx.BORDER_NONE)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonPanel.SetSizer(buttonSizer)

        self.cancelBtn = wx.Button(buttonPanel, label=self.cancelBtnLbl, size=(50, 30))
        self.preBtn = wx.Button(buttonPanel, label=self.preBtnLbl, size=(50, 30))
        self.nextBtn = wx.Button(buttonPanel, label=self.nextBtnLbl, size=(50, 30))
        self.saveNextBtn = wx.Button(buttonPanel, label=self.saveNextBtnLbl, size=(100, 30))
        self.saveBtn = wx.Button(buttonPanel, label=self.saveBtnLbl, size=(100, 30))



        if self.modify == 0 or self.modify == 1:
            self.preBtn.Hide()
            self.nextBtn.Hide()
        if self.modify == 1 or self.modify == 2:
            self.saveNextBtn.Hide()

                

        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.nextBtn.Bind(wx.EVT_BUTTON, self.OnNext)
        self.preBtn.Bind(wx.EVT_BUTTON, self.OnPrevious)
        self.saveNextBtn.Bind(wx.EVT_BUTTON, self.OnSaveAddNext)

        buttonSizer.Add(self.cancelBtn, 0, wx.LEFT, 200)
        buttonSizer.Add(self.preBtn, 0, wx.LEFT, 5)
        buttonSizer.Add(self.nextBtn, 0, wx.LEFT, 5)
        buttonSizer.Add(self.saveNextBtn, 0, wx.LEFT, 5)
        buttonSizer.Add(self.saveBtn, 0, wx.LEFT, 5)

        sizerV.Add(self.headerTxt, 0, wx.EXPAND)
        sizerV.Add(summarySizer, 0, wx.EXPAND)
        sizerV.Add(self.openWaterPanel, 0, wx.TOP|wx.LEFT|wx.RIGHT, 15)
        sizerV.Add(self.icePanel, 0, wx.TOP|wx.LEFT|wx.RIGHT, 15)
        sizerV.Add(self.velocityPanel, 0, wx.ALL|wx.EXPAND, 15)
        sizerV.Add(buttonPanel, 0, wx.ALL|wx.EXPAND, 15)


        self.SetSizer(sizerV)
        # self.SetSize(100, 80)


        # self.BindingEvents()

        self.wldlCorrectionCmbox.SetValue(self.corrections[0])
        self.iceAssemblyCmbbox.SetValue(self.iceAssemblySelections[5])

    def StopWatchTimer(self,evt):
        self.currow = evt.GetRow()
        self.curcol = evt.GetCol()
        position = wx.GetMousePosition()
        posX = position.x
        posY = position.y

        position = (posX - 50, posY - 50)

        # print position

 
        

        if self.curcol == 3:
            self.dlg = wx.Dialog(self, title="Timer", size=(150, 170), pos=position)
            dlgSizer = wx.BoxSizer(wx.VERTICAL)
            timeTitle = wx.StaticText(self.dlg, label = 'Time(/s)',style=wx.ALIGN_LEFT, size=(-1, 20))
            self.timeTextCtrl = wx.TextCtrl(self.dlg, size=(-1, 60), style=wx.TE_CENTRE)
            self.timeTextCtrl.SetForegroundColour("Blue")
            font1 = wx.Font(26, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
            self.timeTextCtrl.SetFont(font1)
            self.timeBtn = wx.Button(self.dlg, size = (-1, 20), label = 'Start')
            confirmBtn = wx.Button(self.dlg, size = (-1, 20), label = 'Transfer')

            self.timeBtn.Bind(wx.EVT_BUTTON, self.OnTimeBtn)
            confirmBtn.Bind(wx.EVT_BUTTON, self.OnConfirmBtn)
            self.dlg.Bind(wx.EVT_CLOSE, self.OnDlgClose)



            dlgSizer.Add(timeTitle, 0.5, wx.EXPAND)
            dlgSizer.Add(self.timeTextCtrl, 0.5, wx.EXPAND)
            dlgSizer.Add(self.timeBtn, 1, wx.EXPAND)
            dlgSizer.Add(confirmBtn, 1, wx.EXPAND)


            self.dlg.SetSizer(dlgSizer)
            self.dlg.ShowModal()

        # print "OnLabelLeftDClick: (%d,%d)\n" % (evt.GetRow(),
        #                                            evt.GetCol())
        evt.Skip()

    def OnDlgClose(self, event):
        # print "OnDlgClose"
        if self.threadingControl is not None and self.threadingControl.startRun:
            if not self.threadingControl.paused:
                # print "pause the thread"
                self.threadingControl.pause()

        event.Skip()


    def OnConfirmBtn(self, evt):
        if self.threadingControl is not None and self.threadingControl.startRun:
            # print self.threadingControl.paused
            # print self.threadingControl.startRun
            if not self.threadingControl.paused:
                self.threadingControl.pause()
            times = self.timeTextCtrl.GetValue()
            if times != 'Timing...':
                self.velocityGrid.SetCellValue (self.currow, self.curcol, times)
            self.dlg.Destroy()
            self.threadingControl.stop()
        evt.Skip()

    def OnTimeBtn(self, evt):
        label = self.timeBtn.GetLabel()
        if label == 'Start' or label == 'Restart':
            self.timeBtn.SetLabel(label = 'Stop')
            # self.clockRec = clock()
            self.MySW = wx.StopWatch()
            if self.threadingControl is not None and not self.threadingControl.stopped():
                self.threadingControl.stop()
            self.threadingControl = ThreadingControl(self)
            self.threadingControl.start()
            # self.timeTextCtrl.SetValue('Timing...')
        # elif label == 'Restart':
        #     self.timeBtn.SetLabel(label = 'Stop')
        #     self.threadingControl.resume
        elif label == 'Stop':
            self.timeBtn.SetLabel(label = 'Restart')

            self.threadingControl.pause()
            # timeSec = clock()-self.clockRec
            # timeSec = str(timeSec-timeSec%0.1)
            # self.timeTextCtrl.SetValue(timeSec)
            # print timeSec
        evt.Skip()



    def BindingEvents(self):
        self.obliqueCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAdjVelocity)
        self.velocityCombo.Bind(wx.EVT_COMBOBOX, self.OnUpdateMeanVel)
        self.slopeCtrl.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)
        self.slopeCtrl2.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)
        self.interceptCtrl.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)
        self.velocityCorrectionCtrl.Bind(wx.EVT_TEXT, self.OnUpdateMeanVel)

        self.panelNumberCtrl.Bind(wx.EVT_TEXT, self.OnPanelNumber)
        self.panelConditionCombox.Bind(wx.EVT_COMBOBOX, self.OnUpdateVelocityCorrection)
        self.panelConditionCombox.Bind(wx.EVT_COMBOBOX, self.OnPanelCondition)
        self.slopeCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAllPointVel)
        self.slopeCtrl2.Bind(wx.EVT_TEXT, self.OnUpdateAllPointVel)
        self.interceptCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAllPointVel)

        self.amountWeightCmbox.Bind(wx.EVT_COMBOBOX, self.OnUpdateMeterOffset)
        self.weightOffsetCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.waterIceAdjustCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.iceEffectiveDepthCtrl.Bind(wx.EVT_TEXT, self.OnUpdateDepthOfObs)
        self.weightOffsetCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.wldlCorrectionCmbox.Bind(wx.EVT_COMBOBOX, self.OnWLDLCorrection)
        self.wldlCorrectionCmbox.Bind(wx.EVT_COMBOBOX, self.UpdateWetLineCorrection)
        self.dryLineAngleCtrl.Bind(wx.EVT_TEXT, self.UpdateDryLineCorrection)
        self.dryLineAngleCtrl.Bind(wx.EVT_TEXT, self.UpdateWetLineCorrection)
        self.dryLineCorrectionCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.wetLineCorrectionCtrl.Bind(wx.EVT_TEXT, self.OnUpdateOpenEffectiveDepth)
        self.distWaterCtrl.Bind(wx.EVT_TEXT, self.UpdateDryLineCorrection)
        self.iceDepthReadCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.iceAssemblyCmbbox.Bind(wx.EVT_COMBOBOX, self.OnIceAssembly)
        self.meterBelowCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAdjusted)
        self.meterBelowCtrl.Bind(wx.EVT_TEXT, self.OnUpdateIceThickAdjusted)
        self.meterAboveCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.waterSurfaceIceCtrl.Bind(wx.EVT_TEXT, self.OnUpdateAdjusted)
        self.waterSurfaceIceCtrl.Bind(wx.EVT_TEXT, self.UpdateSlushThickness)
        self.waterSurfaceIceCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.slushCkbox.Bind(wx.EVT_CHECKBOX, self.UpdateSlushThickness)
        self.slushCkbox.Bind(wx.EVT_CHECKBOX, self.UpdateIceEffectiveDepth)
        self.waterSurfaceSlushCtrl.Bind(wx.EVT_TEXT, self.UpdateSlushThickness)
        self.slushThicknessCtrl.Bind(wx.EVT_TEXT, self.UpdateIceEffectiveDepth)
        self.velocityCombo.Bind(wx.EVT_COMBOBOX, self.OnUpdateVelocityCorrection)
        self.velocityCombo.Bind(wx.EVT_COMBOBOX, self.OnVelMethod)
        self.reverseCkbox.Bind(wx.EVT_CHECKBOX, self.OnUpdateAllPointVel)
        self.iceThickCtrl.Bind(wx.EVT_TEXT, self.OnUpdateIceThickAdjusted)


        self.velocityGrid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnUpdateAtPointVel)
        self.velocityGrid.Bind(wx.grid.EVT_GRID_TABBING, self.OnRevTimeTab)
        # self.velocityGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnDoubleClick)
        # self.velocityGrid.Bind(wx.grid.EVT_GRID_CELL_CHANGING, self.OnDoubleClick)

    # def OnDoubleClick(self, evt):
    #     # if evt.GetCellValue() == "0":
    #     #     evt.SetCellValue()
    #     print evt.GetCol()
    #     print evt.GetRow()
    #     print evt.GetEventObject()
    #     print evt.Selecting()

    #     grid = evt.GetEventObject()
    #     row = evt.GetRow()
    #     col = evt.GetCol()

    #     if grid.GetCellValue(row, col) != "" and float(grid.GetCellValue(row, col)) == 0.0:
    #         grid.SetCellValue(row, col, "")

    #     evt.Skip()


    def InitData(self):
        self.measurementTimeCtrl.SetToCurrent()
        self.panelTagMarkCtrl.SetValue(self.nextTagMark)
        self.amountWeightCmbox.SetValue("0")
        self.weightOffsetCtrl.SetValue("0")
        self.meterAboveCtrl.SetValue("0")
        self.meterBelowCtrl.SetValue("0")
        self.distanceAboveCtrl.SetValue("0")
        self.obliqueCtrl.SetValue("1")

    def OnRevTimeTab(self, event):

        totalRows = self.velocityGrid.GetNumberRows()
        col = event.GetCol()
        row = event.GetRow()
        if col==2:
            self.velocityGrid.GoToCell(row,3)
        elif col==3:
            if row!=totalRows-1:
                self.velocityGrid.GoToCell(row+1,2)

    # def OnTagmarkTabEnter(self, event):
    #     if "open" in self.panelConditionCombox.GetValue().lower():
    #         self.openDepthReadCtrl.SetFocus()
    #     if "ice" in self.panelConditionCombox.GetValue().lower():
    #         self.iceDepthReadCtrl.SetFocus()
    #     event.Skip()

    def OnUpdateIceThickAdjusted(self, event):
        self.UpdateIceThickAdjusted()
        event.Skip()

    def UpdateIceThickAdjusted(self):
        iceThickness = self.iceThickCtrl.GetValue()
        meterBelowFoot = self.meterBelowCtrl.GetValue()
        if iceThickness!="" and meterBelowFoot!="":
            adjustedIceThickness = float(iceThickness) - float(meterBelowFoot)
            self.iceThickAdjustedCtrl.SetValue(str(adjustedIceThickness))

    def OnUpdateDepthOfObs(self, event):
        for i in range(3):
            self.UpdateDepthOfObs(i)
        event.Skip()

    def UpdateDepthOfObs(self, row):

        coef = self.velocityGrid.GetCellValue(row, 0)
        if self.velocityCombo.GetValue() == "Surface" or coef == "":
            val = ""

        elif self.panelConditionCombox.GetValue() == "Open":
            if self.openDepthReadCtrl.GetValue() == "":
                val = ""
            else:
                offset = self.weightOffsetCtrl.GetValue() if self.weightOffsetCtrl.GetValue() != "" else "0"
                val = float(coef) * (float(self.openDepthReadCtrl.GetValue()) + float(offset))
        elif self.panelConditionCombox.GetValue() == "Ice":
            effectiveDepth = self.iceEffectiveDepthCtrl.GetValue()

            if effectiveDepth == "":
                    val = ""
            elif self.slushCkbox.IsChecked():
                slush = self.waterSurfaceSlushCtrl.GetValue() if self.waterSurfaceSlushCtrl.GetValue() != '' else "0"
                val = float(effectiveDepth) * float(coef) + float(slush)

            else:
                adjusted = self.waterIceAdjustCtrl.GetValue() if self.waterIceAdjustCtrl.GetValue() != '' else "0"
                val = float(effectiveDepth) * float(coef) + float(adjusted)

        else:
            val = ""
        if val == "":
            self.velocityGrid.SetCellValue(row, 1, val)
        else:
            self.velocityGrid.SetCellValue(row, 1, str(round(val,2)))






    def OnUpdateAtPointVel(self, event):

        for i in range(3):
            if self.velocityGrid.GetCellValue(i, 1) == "0.00":
                self.velocityGrid.SetCellValue(i, 1, "")

            if self.velocityGrid.GetCellValue(i, 2) == "0":
                self.velocityGrid.SetCellValue(i, 2, "")

            if self.velocityGrid.GetCellValue(i, 3) == "0.0":
                self.velocityGrid.SetCellValue(i, 3, "")

            if self.velocityGrid.GetCellValue(i, 4) == "0.000":
                self.velocityGrid.SetCellValue(i, 4, "")

        if event.GetCol() == 2 or event.GetCol() == 3:
            row = event.GetRow()
            if self.UpdateAtPointVelByRow(row):

                self.ShowWarning()

        if event.GetCol() == 0:
            self.OnUpdateDepthOfObs(event)

        self.UpdateMeanVel()

        event.Skip()


    def CalculateVel(self, rev, time, slope, intercept, reverse):

        if rev == "0":
            return "0"
        if rev == "" or time == "" or slope == "" or intercept == "":
            return ""
        elif reverse:
            return - (float(rev) / float(time) * float(slope) + float(intercept))
        else:
            return float(rev) / float(time) * float(slope) + float(intercept)


    def UpdateAtPointVelByRow(self, row):
        temp02 = self.preVel02
        temp08 = self.preVel08


        rev = self.velocityGrid.GetCellValue((row, 2))
        time = self.velocityGrid.GetCellValue((row, 3))
        if self.slopBtn1.GetValue():
            slope = self.slopeCtrl.GetValue()
            intercept = self.interceptCtrl.GetValue()
        else:
            slope = self.slopeCtrl2.GetValue()
            intercept = self.interceptCtrl2.GetValue()
        reverse = self.reverseCkbox.IsChecked()

        if rev != "" and time != "" and slope != '' and intercept != "":
            val = self.CalculateVel(rev, time, slope, intercept, reverse)

            # apply 3sigfig

            if isinstance(val, str):
                self.velocityGrid.SetCellValue((row, 4), val)
                self.rawAtPointVel[row] = val

            else:
                self.velocityGrid.SetCellValue((row, 4), sigfig.round_sig(val,3))
                self.rawAtPointVel[row] = val
                #self.velocityGrid.SetCellValue((row, 4), str(val))
            # self.openWaterPanel.Disable()
            # self.icePanel.Disable()
            # self.depthPanelLockCkbox.SetValue(True)
        else:
            self.velocityGrid.SetCellValue((row, 4), "")
            self.rawAtPointVel[row] = ""

        if self.velocityCombo.GetValue() == self.velocityMethods[2] and self.velocityGrid.GetCellValue((0, 4)) != "" and self.velocityGrid.GetCellValue((1, 4)) != "":
            vel02 = float(self.velocityGrid.GetCellValue((0, 4)))
            vel08 = float(self.velocityGrid.GetCellValue((1, 4)))
            self.preVel02 = vel02
            self.preVel08 = vel08
            if vel02 / vel08 > 2 and (temp02 != vel02 or temp08 != vel08):

                return True
                

    def UpdateAllPointVel(self):

        showWarning = False
        for i in range(3):
            showWarning = self.UpdateAtPointVelByRow(i) if not showWarning else True

        if showWarning:
            self.ShowWarning()
        self.UpdateMeanVel()


    def ShowWarning(self):
        dlg = wx.MessageDialog(None, "Warning\nIt is highly recommended to use 0.2/0.6/0.8 method.", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()

    def OnUpdateAllPointVel(self, event):
      
        self.UpdateAllPointVel()
        event.Skip()


    def OnPanelCondition(self, event):


        self.PanelConditionUpdate()
        self.OnVelMethod(event)
        self.OnUpdateDepthOfObs(event)
        self.OnIceAssembly(event)
        self.Layout()
        event.Skip()


    def PanelConditionUpdate(self):
        if self.panelConditionCombox.GetValue() == "Ice":
            self.openWaterPanel.Hide()
            self.icePanel.Show()

            self.openDepthReadCtrl.SetValue("")
            self.amountWeightCmbox.SetValue(self.weights[0])
            self.weightOffsetCtrl.SetValue("")
            self.wldlCorrectionCmbox.SetValue(self.corrections[0])
            self.dryLineAngleCtrl.SetValue("")
            self.distWaterCtrl.SetValue("")
            self.dryLineCorrectionCtrl.SetValue("")
            self.wetLineCorrectionCtrl.SetValue("")
            self.OpenEffectiveDepthCtrl.SetValue("")

            self.velocityCombo.SetItems(self.velocityMethods)
            self.velocityCombo.SetValue("0.5")

        else:
            self.icePanel.Hide()
            self.openWaterPanel.Show()

            if self.weightOffsetCtrl.GetValue()=="":
                self.weightOffsetCtrl.SetValue("0")
            self.iceDepthReadCtrl.SetValue("")
            self.iceAssemblyCmbbox.SetValue(self.iceAssemblySelections[5])
            self.meterAboveCtrl.SetValue("")
            self.meterBelowCtrl.SetValue("")
            self.distanceAboveCtrl.SetValue("")
            self.waterSurfaceIceCtrl.SetValue("")
            self.waterIceAdjustCtrl.SetValue("")
            self.slushThicknessCtrl.SetValue("")
            self.slushCkbox.SetValue(False)
            self.waterSurfaceSlushCtrl.SetValue("")

            self.velocityCombo.SetItems(self.velocityMethods[1:])
            self.velocityCombo.SetValue("0.6")

    def OnPanelNumber(self, event):
        val = self.panelNumberCtrl.GetValue()
        self.headerTxt.SetLabel(self.titleLbl + "  " + val)
        self.Layout()
        event.Skip()

    def VelMethod(self):

        self.UpdateGrid()
        for i in range(3):
            self.UpdateDepthOfObs(i)


        self.UpdateAllPointVel()
        self.Layout()

    def OnVelMethod(self, event):
        self.VelMethod()
        event.Skip()

    def UpdateGrid(self):
        row0 = [self.velocityGrid.GetCellValue(0,0), self.velocityGrid.GetCellValue(0,2), self.velocityGrid.GetCellValue(0,3)]
        row1 = [self.velocityGrid.GetCellValue(1,0), self.velocityGrid.GetCellValue(1,2), self.velocityGrid.GetCellValue(1,3)]
        row2 = [self.velocityGrid.GetCellValue(2,0), self.velocityGrid.GetCellValue(2,2), self.velocityGrid.GetCellValue(2,3)]
        rows = [row0, row1, row2]
        if self.velocityCombo.GetValue() == "0.5":
            self.velocityGrid.SetCellValue((0,0), "0.5")
            self.velocityGrid.SetCellValue((1,0), "")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "3.05")
            # self.velocityGrid.SetCellValue((1,1), "")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.HideRow(1)
            self.velocityGrid.HideRow(2)

        elif self.velocityCombo.GetValue() == "0.6":
            self.velocityGrid.SetCellValue((0,0), "0.6")
            self.velocityGrid.SetCellValue((1,0), "")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "3.26")
            # self.velocityGrid.SetCellValue((1,1), "")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.HideRow(1)
            self.velocityGrid.HideRow(2)

        elif self.velocityCombo.GetValue() == "0.2/0.8":
            self.velocityGrid.SetCellValue((0,0), "0.2")
            self.velocityGrid.SetCellValue((1,0), "0.8")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "2.42")
            # self.velocityGrid.SetCellValue((1,1), "3.68")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.ShowRow(1)
            self.velocityGrid.HideRow(2)

        elif self.velocityCombo.GetValue() == "0.2/0.6/0.8":
            self.velocityGrid.SetCellValue((0,0), "0.2")
            self.velocityGrid.SetCellValue((1,0), "0.6")
            self.velocityGrid.SetCellValue((2,0), "0.8")

            # self.velocityGrid.SetCellValue((0,1), "2.42")
            # self.velocityGrid.SetCellValue((1,1), "3.26")
            # self.velocityGrid.SetCellValue((2,1), "3.68")

            self.velocityGrid.ShowRow(1)
            self.velocityGrid.ShowRow(2)

        elif self.velocityCombo.GetValue() == "Surface":
            self.velocityGrid.SetCellValue((0,0), "Surface")
            self.velocityGrid.SetCellValue((1,0), "")
            self.velocityGrid.SetCellValue((2,0), "")

            # self.velocityGrid.SetCellValue((0,1), "")
            # self.velocityGrid.SetCellValue((1,1), "")
            # self.velocityGrid.SetCellValue((2,1), "")

            self.velocityGrid.HideRow(1)
            self.velocityGrid.HideRow(2)

        for i in range(3):
            for index, val in enumerate(rows):
                self.velocityGrid.SetCellValue((i, 2), "")
                self.velocityGrid.SetCellValue((i, 3), "")
                if self.velocityGrid.GetCellValue(i, 0) == val[0]:
                    self.velocityGrid.SetCellValue((i, 2), val[1])
                    self.velocityGrid.SetCellValue((i, 3), val[2])
                    break



    def OnIceAssmeblyNoEvent(self):
        iceVal = self.iceAssemblyCmbbox.GetValue()
        if iceVal == self.iceAssemblySelections[0]:
            self.meterAboveCtrl.SetValue("0.1")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0")
        elif iceVal == self.iceAssemblySelections[1]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.25")
        elif iceVal == self.iceAssemblySelections[2]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.26")
        elif iceVal == self.iceAssemblySelections[3]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.32")
        elif iceVal == self.iceAssemblySelections[4]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0.36")
        elif iceVal == self.iceAssemblySelections[5]:
            self.meterAboveCtrl.SetValue("0")
            self.meterBelowCtrl.SetValue("0")
            self.distanceAboveCtrl.SetValue("0")
        self.UpdateIceThickAdjusted()

    def OnIceAssembly(self, event):
        self.OnIceAssmeblyNoEvent()
        event.Skip()


    def UpdateSlushThickness(self, event):
        if self.slushCkbox.IsChecked():
            if self.waterSurfaceIceCtrl.GetValue() != "" and self.waterSurfaceSlushCtrl.GetValue() != "":
                self.slushThicknessCtrl.SetValue(str(float(self.waterSurfaceSlushCtrl.GetValue()) - float(self.waterSurfaceIceCtrl.GetValue())))
            else:
                self.slushThicknessCtrl.SetValue(self.waterSurfaceSlushCtrl.GetValue())

        event.Skip()

    def UpdateIceEffectiveDepth(self, event):
        iceDepth = self.iceDepthReadCtrl.GetValue()
        meterAbove = self.meterAboveCtrl.GetValue()
        meterBelow = self.meterBelowCtrl.GetValue()
        waterIce = self.waterSurfaceIceCtrl.GetValue()
        slushThick = self.slushThicknessCtrl.GetValue()
        if iceDepth != "" and meterAbove != "" and waterIce != "":
            if self.slushCkbox.IsChecked():
                if slushThick != "":
                    self.iceEffectiveDepthCtrl.SetValue(str(round(float(iceDepth) + float(meterAbove) - float(waterIce) + float(meterBelow) - float(slushThick),2)))
                else:
                    self.iceEffectiveDepthCtrl.SetValue(str(round(float(iceDepth) + float(meterAbove) - float(waterIce) + float(meterBelow),2)))
            else:
                self.iceEffectiveDepthCtrl.SetValue(str(round(float(iceDepth) + float(meterAbove) - float(waterIce) + float(meterBelow),2)))
        else:
            self.iceEffectiveDepthCtrl.SetValue("")

        if self.iceEffectiveDepthCtrl.GetValue() != "" and self.modify != 2:
            if float(self.iceEffectiveDepthCtrl.GetValue()) < 0.75 and "open" in self.panelConditionCombox.GetValue().lower():
                self.velocityCombo.SetValue("0.6")
                self.UpdateMeanVel()
                self.UpdateVelocityCorrection()
                self.VelMethod()
            if float(self.iceEffectiveDepthCtrl.GetValue()) < 0.75 and "ice" in self.panelConditionCombox.GetValue().lower():
                self.velocityCombo.SetValue("0.5")
                self.UpdateMeanVel()
                self.UpdateVelocityCorrection()
                self.VelMethod()
            elif float(self.iceEffectiveDepthCtrl.GetValue()) >= 0.75:
                self.velocityCombo.SetValue("0.2/0.8")
                self.UpdateMeanVel()
                self.UpdateVelocityCorrection()
                self.VelMethod()

        event.Skip()

    def UpdateMeterOffset(self):
        val = self.amountWeightCmbox.GetValue()
        key = self.weights.index(val)
        self.weightOffsetCtrl.SetValue(self.meterOffsets[key])
        self.UpdateOpenEffectiveDepth()

    def OnUpdateMeterOffset(self, event):
        self.UpdateMeterOffset()
        event.Skip()

    def WLDLCorrection(self):
        if self.wldlCorrectionCmbox.GetValue() == "No":
            self.dryLineAngleCtrl.Enable(False)
            self.distWaterCtrl.Enable(False)
            self.dryLineCorrectionCtrl.Enable(False)
            self.wetLineCorrectionCtrl.Enable(False)
        elif self.wldlCorrectionCmbox.GetValue() == "Yes":
            self.dryLineAngleCtrl.Enable(True)
            self.distWaterCtrl.Enable(True)
            self.dryLineCorrectionCtrl.Enable(True)
            self.wetLineCorrectionCtrl.Enable(True)
        else:
            self.dryLineAngleCtrl.Enable(True)
            self.distWaterCtrl.Enable(False)
            self.dryLineCorrectionCtrl.Enable(False)
            self.wetLineCorrectionCtrl.Enable(True)
        self.UpdateDryLineCorrectionNoEvent()

    def OnWLDLCorrection(self, event):
        self.WLDLCorrection()
        event.Skip()

    def UpdateOpenEffectiveDepth(self):
        depthRead = self.openDepthReadCtrl.GetValue()
        offset = self.weightOffsetCtrl.GetValue()
        dryLine = self.dryLineCorrectionCtrl.GetValue()
        wetLine = self.wetLineCorrectionCtrl.GetValue()


        if depthRead != "":
            offset = float(offset) if offset != "" else 0
            dryLine = float(dryLine) if dryLine != ""  and self.dryLineCorrectionCtrl.IsEnabled() else 0
            wetLine = float(wetLine) if wetLine != "" and self.wetLineCorrectionCtrl.IsEnabled() else 0
            effectiveDepth = str(round(float(depthRead) + offset - dryLine - wetLine,2))

        else:
            effectiveDepth = ""
        if effectiveDepth != "" and self.modify != 2:
            if offset < 0.2:
                if float(effectiveDepth) < 0.75:
                    self.velocityCombo.SetValue("0.6")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()
                elif float(effectiveDepth) >= 0.75:
                    self.velocityCombo.SetValue("0.2/0.8")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()
            else:
                cutOffDepth = offset/0.2

                if float(effectiveDepth) < cutOffDepth:
                    self.velocityCombo.SetValue("0.6")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()
                elif float(effectiveDepth) >= cutOffDepth:
                    self.velocityCombo.SetValue("0.2/0.8")
                    self.UpdateMeanVel()
                    self.UpdateVelocityCorrection()
                    self.VelMethod()


        self.OpenEffectiveDepthCtrl.SetValue(effectiveDepth)

    def OnUpdateOpenEffectiveDepth(self, event):
        self.UpdateOpenEffectiveDepth()
        event.Skip()

    def UpdateDryLineCorrectionNoEvent(self):
        dryLine = self.dryLineAngleCtrl.GetValue()
        distWater = self.distWaterCtrl.GetValue()
        if self.wldlCorrectionCmbox.GetValue() == "Yes" and dryLine != "" and distWater != "":
            dryCorrection = str(((1 / math.cos(math.radians(float(dryLine)))) - 1) * float(distWater))
        else:

            dryCorrection = ""
            # self.dryLineAngleCtrl.ChangeValue("")
            # self.distWaterCtrl.ChangeValue("")
            # self.wetLineCorrectionCtrl.ChangeValue("")
        self.dryLineCorrectionCtrl.SetValue(dryCorrection)

    def UpdateDryLineCorrection(self, event):
        self.UpdateDryLineCorrectionNoEvent()
        event.Skip()

    def UpdateWetLineCorrectionNoEvent(self):
        angle = self.dryLineAngleCtrl.GetValue()
        depthRead = self.openDepthReadCtrl.GetValue()
        if self.wldlCorrectionCmbox.GetValue() == "Yes" or self.wldlCorrectionCmbox.GetValue() == "Yes_w_Tags":
            if angle != "" and depthRead != "":
                angle = float(angle)
                depthRead = float(depthRead)
                wetLineCorrection = depthRead - (depthRead * ((0.000313*angle) + (0.000075*angle*angle) + (0.998015*(math.cos(math.radians(angle))))))

            else:
                wetLineCorrection = ""

        else:
            wetLineCorrection = 0
            # self.dryLineAngleCtrl.ChangeValue("")
            # self.distWaterCtrl.ChangeValue("")
            # self.wetLineCorrectionCtrl.ChangeValue("")

        self.wetLineCorrectionCtrl.SetValue(str(wetLineCorrection))

    def UpdateWetLineCorrection(self, event):
        self.UpdateWetLineCorrectionNoEvent()
        event.Skip()

    def OnUpdateAdjusted(self, event):
        waterBottom = self.waterSurfaceIceCtrl.GetValue()
        meterBelow = self.meterBelowCtrl.GetValue()
        if waterBottom == "":
            self.waterIceAdjustCtrl.SetValue("")
        else:
            if meterBelow == "":
                self.waterIceAdjustCtrl.SetValue(waterBottom)
            else:
                self.waterIceAdjustCtrl.SetValue(str(float(waterBottom) - float(meterBelow)))
        event.Skip()

    def OnUpdateVelocityCorrection(self, event):
        self.UpdateVelocityCorrection()
        event.Skip()

    def UpdateVelocityCorrection(self):
        panelCondition = self.panelConditionCombox.GetValue()
        velocityMethod = self.velocityCombo.GetValue()

        if panelCondition == "Ice" and velocityMethod == self.velocityMethods[0]:
            vcf = "0.88"
            self.velocityCorrectionCtrl.Enable(True)
        elif panelCondition == "Ice" and velocityMethod == self.velocityMethods[1]:
            vcf = "0.92"
            self.velocityCorrectionCtrl.Enable(True)
        elif velocityMethod == self.velocityMethods[4]:
            vcf = "0.85"
            self.velocityCorrectionCtrl.Enable(True)
        else:
            vcf = "1.0"
            self.velocityCorrectionCtrl.Enable(False)
        self.velocityCorrectionCtrl.SetValue(vcf)

    def UpdateMeanVel(self):

        try:

            #self.velocityMethods = ["0.5", "0.6", "0.2/0.8", "0.2/0.6/0.8", "Surface"]
            if self.velocityCombo.GetValue() == self.velocityMethods[0] \
                or self.velocityCombo.GetValue() == self.velocityMethods[1]\
                or self.velocityCombo.GetValue() == self.velocityMethods[4]:


                meanVal = self.rawAtPointVel[0] * float(self.velocityCorrectionCtrl.GetValue())
    
            elif self.velocityCombo.GetValue() == self.velocityMethods[2]:
 


                meanVal = (self.rawAtPointVel[0] + self.rawAtPointVel[1]) / 2 * float(self.velocityCorrectionCtrl.GetValue())
            else:
            

                meanVal = ((self.rawAtPointVel[0] + self.rawAtPointVel[1] * 2 + self.rawAtPointVel[2])) / 4 * float(self.velocityCorrectionCtrl.GetValue())
            self.rawMeanVal = meanVal

            ## apply 3 sigfigs
            self.velocityGrid.SetCellValue(0, 5, sigfig.round_sig(meanVal,3))
            #self.velocityGrid.SetCellValue(0, 5, str(meanVal))
        except:

            self.velocityGrid.SetCellValue(0, 5, "")


        self.UpdateAdjVelocity()

    def UpdateAdjVelocity(self):

        try:
            #meanVal = self.velocityGrid.GetCellValue(0, 5)
            obliqueCorrection = self.obliqueCtrl.GetValue()

            rawMeanVal = self.velocityGrid.GetCellValue(0, 5)
            if rawMeanVal != "" and obliqueCorrection:

                try:
                    self.velocityGrid.SetCellValue(0, 6, sigfig.round_sig(float(rawMeanVal) * float(obliqueCorrection),3))

                except:
                    self.velocityGrid.SetCellValue(0, 6, "")

                #self.velocityGrid.SetCellValue(0, 6, str(float(meanVal) * float(obliqueCorrection)))
            else:

                self.velocityGrid.SetCellValue(0, 6, "")
        except Exception as e:
    
            self.velocityGrid.SetCellValue(0, 6, "")




    def OnUpdateMeanVel(self, event):
        self.UpdateMeanVel()
        event.Skip()

    def OnUpdateAdjVelocity(self, event):
        self.UpdateAdjVelocity()
        event.Skip()

    def OnSlushCkbox(self, event):
        if self.slushCkbox.IsChecked():
            self.waterSurfaceSlushCtrl.Enable(True)
        else:
            self.waterSurfaceSlushCtrl.SetValue("")
            self.waterSurfaceSlushCtrl.Enable(False)
        event.Skip()

    def OnSave(self, event):

        self.SaveToObj()
        event.Skip()

    def OnPrevious(self, event):
        failed = self.SaveToObj()
        table = self.GetParent().GetParent().GetParent()
        if failed != -1:
            for index, obj in enumerate(table.panelObjs):
                if float(obj.distance) == float(self.panelTagMarkCtrl.GetValue()):
                    table.modifiedPanelArrayIndex = index
                    break
            table.modifiedPanelArrayIndex -= 1
            table.Modify()

    def OnNext(self, event):
        failed = self.SaveToObj()
        table = self.GetParent().GetParent().GetParent()
        if failed != -1:
            for index, obj in enumerate(table.panelObjs):
                if float(obj.distance) == float(self.panelTagMarkCtrl.GetValue()):
                    table.modifiedPanelArrayIndex = index
                    break

            table.modifiedPanelArrayIndex += 1
            table.Modify()



    def OnSaveAddNext(self, event):
        failed = self.SaveToObj()
        table = self.GetParent().GetParent().GetParent()
        if failed != -1:
            table.Adding()
        

        
            

        

    def SaveToObj(self):
        # self.UpdateAllPointVel()

        table = self.GetParent().GetParent().GetParent()

        num = self.panelNumberCtrl.GetValue()
        dist = self.panelTagMarkCtrl.GetValue()
        velocityMethod = self.velocityCombo.GetValue()

        if dist=="":
            dlg = wx.MessageDialog(None, self.mandatoryFieldsMsg + "[Panel Tagmark (m)]", "Warning!", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return -1

        arrayIndex = -1
        for index, obj in enumerate(table.panelObjs):
            if obj.pid == self.pid:
                arrayIndex = index
                break

        if table.IsValidTagMark(dist, arrayIndex=arrayIndex, modify=self.modify) != 0:
            return -1

        if len(table.panelObjs) > 0:
            for i in range(len(table.panelObjs)):
                if float(table.panelObjs[i].distance) == float(dist):
                    if self.modify != 2:
                        dlg = wx.MessageDialog(None, "Panel tagmark value already exists", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                        dlg.ShowModal()
                        return -1
                    else:
                        if float(dist) != float(table.originalTagmark):
                            dlg = wx.MessageDialog(None, "Panel tagmark value already exists", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                            dlg.ShowModal()
                            return -1
                try:
                    if isinstance(table.panelObjs[i].panelNum, str) and isinstance(table.panelObjs[i+1].panelNum, str):
                        if "start p" in table.panelObjs[i].panelNum.lower() and "end p" in table.panelObjs[i+1].panelNum.lower():
                            if float(table.panelObjs[i].distance) < float(dist) < float(table.panelObjs[i+1].distance) or float(table.panelObjs[i].distance) > float(dist) > float(table.panelObjs[i+1].distance):
                                dlg = wx.MessageDialog(None, "Panel tagmark value is within the range of P/ISL", "Invalid Tagmark value!", wx.OK | wx.ICON_EXCLAMATION)
                                dlg.ShowModal()
                                return -1
                except:
                    pass




        myDepths = []
        myObs = []
        myRevs = []
        myRevTimes = []
        myPointVels = []
        if self.velocityCombo.GetValue() == self.velocityMethods[0] or \
                self.velocityCombo.GetValue() == self.velocityMethods[1] or \
                self.velocityCombo.GetValue() == self.velocityMethods[4]:

            myDepths.append(self.velocityGrid.GetCellValue(0, 0))
            myObs.append(self.velocityGrid.GetCellValue(0, 1))
            myRevs.append(self.velocityGrid.GetCellValue(0, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(0, 3))
            if self.velocityGrid.GetCellValue(0, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(0, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(0, 4)),3))

        elif self.velocityCombo.GetValue() == self.velocityMethods[2]:

            myDepths.append(self.velocityGrid.GetCellValue(0, 0))
            myObs.append(self.velocityGrid.GetCellValue(0, 1))
            myRevs.append(self.velocityGrid.GetCellValue(0, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(0, 3))
            if self.velocityGrid.GetCellValue(0, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(0, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(0, 4)),3))

            myDepths.append(self.velocityGrid.GetCellValue(1, 0))
            myObs.append(self.velocityGrid.GetCellValue(1, 1))
            myRevs.append(self.velocityGrid.GetCellValue(1, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(1, 3))
            if self.velocityGrid.GetCellValue(1, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(1, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(1, 4)),3))

        elif self.velocityCombo.GetValue() == self.velocityMethods[3]:

            myDepths.append(self.velocityGrid.GetCellValue(0, 0))
            myObs.append(self.velocityGrid.GetCellValue(0, 1))
            myRevs.append(self.velocityGrid.GetCellValue(0, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(0, 3))
            if self.velocityGrid.GetCellValue(0, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(0, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(0, 4)),3))

            myDepths.append(self.velocityGrid.GetCellValue(1, 0))
            myObs.append(self.velocityGrid.GetCellValue(1, 1))
            myRevs.append(self.velocityGrid.GetCellValue(1, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(1, 3))
            if self.velocityGrid.GetCellValue(1, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(1, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(1, 4)),3))

            myDepths.append(self.velocityGrid.GetCellValue(2, 0))
            myObs.append(self.velocityGrid.GetCellValue(2, 1))
            myRevs.append(self.velocityGrid.GetCellValue(2, 2))
            myRevTimes.append(self.velocityGrid.GetCellValue(2, 3))
            if self.velocityGrid.GetCellValue(2, 4) == "":
                myPointVels.append(self.velocityGrid.GetCellValue(2, 4))
            else:
                myPointVels.append(round(float(self.velocityGrid.GetCellValue(2, 4)),3))

        if self.velocityGrid.GetCellValue(0, 5)=="":
            meanVelocity = ""
        else:
            meanVelocity = sigfig.round_sig(float(self.velocityGrid.GetCellValue(0, 5)),3)
        if self.panelConditionCombox.GetValue() == "Open":
            # depth = self.openDepthReadCtrl.GetValue()
            # effetiveDepth = self.OpenEffectiveDepthCtrl.GetValue()
            obj = PanelObj(panelNum=num, distance=dist, depth=self.openDepthReadCtrl.GetValue(), \
                depths=myDepths, depthObs=myObs, revs=myRevs, revTimes=myRevTimes, pointVels=myPointVels,\
                meanVelocity=meanVelocity, corrMeanVelocity=self.velocityGrid.GetCellValue(0, 6),\
                velocityMethod=self.velocityCombo.GetValue(), panelCondition=self.panelConditionCombox.GetValue(),\
                currentMeter=self.currentMeterCtrl.GetValue(), time=self.measurementTimeCtrl.GetValue(),\
                slop=self.slopeCtrl.GetValue(), intercept=self.interceptCtrl.GetValue(), slop2=self.slopeCtrl2.GetValue(),\
                intercept2=self.interceptCtrl2.GetValue(), slopBtn1=self.slopBtn1.GetValue(),\
                openDepthRead=self.openDepthReadCtrl.GetValue(), weight=self.amountWeightCmbox.GetValue(), \
                offset=self.weightOffsetCtrl.GetValue(), wldl=self.wldlCorrectionCmbox.GetValue(), \
                dryAngle=self.dryLineAngleCtrl.GetValue(), distWaterSurface=self.distWaterCtrl.GetValue(), \
                dryCorrection=self.dryLineCorrectionCtrl.GetValue(), wetCorrection=self.wetLineCorrectionCtrl.GetValue(), \
                openEffectiveDepth=self.OpenEffectiveDepthCtrl.GetValue(),\
                obliqueCorrection=self.obliqueCtrl.GetValue(), velocityCorrFactor=self.velocityCorrectionCtrl.GetValue(), \
                reverseFlow=self.reverseCkbox.GetValue(), pid=self.pid)#, depthPanelLock=self.depthPanelLockCkbox.GetValue())


        else:
            depth = self.iceDepthReadCtrl.GetValue()
            effetiveDepth = self.iceEffectiveDepthCtrl.GetValue()
            bottomIce = self.waterSurfaceIceCtrl.GetValue()

            obj = PanelObj(panelNum=num, distance=dist, depth=depth, \
            depths=myDepths, depthObs=myObs, revs=myRevs, revTimes=myRevTimes, pointVels=myPointVels,\
            meanVelocity=meanVelocity, corrMeanVelocity=self.velocityGrid.GetCellValue(0, 6),\
            velocityMethod=self.velocityCombo.GetValue(),\
            panelCondition=self.panelConditionCombox.GetValue(),\
            currentMeter=self.currentMeterCtrl.GetValue(), time=self.measurementTimeCtrl.GetValue(),\
            slop=self.slopeCtrl.GetValue(), intercept=self.interceptCtrl.GetValue(), slop2=self.slopeCtrl2.GetValue(),\
            intercept2=self.interceptCtrl2.GetValue(), slopBtn1=self.slopBtn1.GetValue(),\
            iceDepthRead=self.iceDepthReadCtrl.GetValue(), iceAssembly=self.iceAssemblyCmbbox.GetValue(), \
            aboveFoot=self.meterAboveCtrl.GetValue(), belowFoot=self.meterBelowCtrl.GetValue(), \
            distAboveWeight=self.distanceAboveCtrl.GetValue(), wsBottomIce=self.waterSurfaceIceCtrl.GetValue(), \
            adjusted=self.waterIceAdjustCtrl.GetValue(), slush=self.slushCkbox.GetValue(), \
            wsBottomSlush=self.waterSurfaceSlushCtrl.GetValue(), thickness=self.slushThicknessCtrl.GetValue(), \
            iceEffectiveDepth=self.iceEffectiveDepthCtrl.GetValue(),\
            obliqueCorrection=self.obliqueCtrl.GetValue(), velocityCorrFactor=self.velocityCorrectionCtrl.GetValue(), \
            reverseFlow=self.reverseCkbox.GetValue(), #depthPanelLock=self.depthPanelLockCkbox.GetValue(), \
            iceThickness = self.iceThickCtrl.GetValue(), iceThicknessAdjusted = self.iceThickAdjustedCtrl.GetValue(), pid=self.pid)


        if self.modify != 2:

            table.AddRow(obj, self.GetScreenPosition())
            table.nextPanelNum += 1
        else:

            table.UpdateRow(obj, self.GetScreenPosition())
        self.GetParent().GetParent().Close()



    def OnCancel(self, event):
        self.GetParent().GetParent().Close()

        event.Skip()

    def OnSlopeRadioBtn(self, event):

        self.SlopeRadioUpdate()
        event.Skip()

    def SlopeRadioUpdate(self):

        if self.slopBtn1.GetValue():
            self.slopeCtrl.Enable(True)
            self.interceptCtrl.Enable(True)
            self.slopeCtrl2.Enable(False)
            self.interceptCtrl2.Enable(False)

        else:
            self.slopeCtrl.Enable(False)
            self.interceptCtrl.Enable(False)
            self.slopeCtrl2.Enable(True)
            self.interceptCtrl2.Enable(True)

        self.UpdateMeanVel()
        self.UpdateAllPointVel()

        #event.Skip()

    def OnCurrMeterCtrl(self, event):
        index = event.GetSelection()
        header = self.GetParent().GetParent().GetParent().GetParent().header
        if index==0:
            if header.meter1MeterNoCtrl.GetValue()!="":
                self.slopeCtrl.SetValue(header.meter1SlopeCtrl1.GetValue())
                self.interceptCtrl.SetValue(header.meter1InterceptCtrl1.GetValue())
                self.slopeCtrl2.SetValue(header.meter1SlopeCtrl2.GetValue())
                self.interceptCtrl2.SetValue(header.meter1InterceptCtrl2.GetValue())
            else:
                self.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
                self.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
                self.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
                self.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())
        if index==1:
            self.slopeCtrl.SetValue(header.meter2SlopeCtrl1.GetValue())
            self.interceptCtrl.SetValue(header.meter2InterceptCtrl1.GetValue())
            self.slopeCtrl2.SetValue(header.meter2SlopeCtrl2.GetValue())
            self.interceptCtrl2.SetValue(header.meter2InterceptCtrl2.GetValue())


    def OnNavigate2Velocity(self, evt):
        evtProc = False
        if evt.IsFromTab():
            if (self.wldlCorrectionCmbox.GetValue() == self.corrections[0] and evt.GetEventObject().FindFocus() == self.wldlCorrectionCmbox)\
                or (self.wldlCorrectionCmbox.GetValue() == self.corrections[1] and evt.GetEventObject().FindFocus() == self.distWaterCtrl)\
                or (self.wldlCorrectionCmbox.GetValue() == self.corrections[2] and evt.GetEventObject().FindFocus() == self.dryLineAngleCtrl)\
                or (evt.GetEventObject().FindFocus() == self.iceDepthReadCtrl):# and self.panelNum == 1)\
                # or (evt.GetEventObject().FindFocus() == self.waterSurfaceIceCtrl and self.panelNum != 1):
                self.velocityCombo.SetFocus()
                evtProc = True
            elif self.panelNum != 1 and evt.GetEventObject().FindFocus() == self.openDepthReadCtrl:
                for index, obj in enumerate(self.GetParent().GetParent().GetParent().panelObjs):
                    if isinstance(obj, PanelObj) and obj.panelNum == self.panelNum - 1:
                        if obj.panelCondition == "Open" and obj.wldl == "No":
                            self.velocityCombo.SetFocus()
                            evtProc = True
            elif evt.GetEventObject().FindFocus() == self.velocityCombo:
                self.velocityGrid.SetFocus()
                self.velocityGrid.GoToCell(0,2)
                evtProc = True


        if (not evtProc):
            evt.Skip()



    # def OnDepthPanelLockCkbox(self, evt):
    #     if self.depthPanelLockCkbox.GetValue():
    #         self.openWaterPanel.Disable()
    #         self.icePanel.Disable()
    #     else:
    #         self.openWaterPanel.Enable()
    #         self.icePanel.Enable()
    #     evt.Skip()



def main():
    app = wx.App()

    frame = wx.Frame(None, size=(540, 660))
    MidSectionPanelPanel(panelNum=1, parent=frame)
    frame.Centre()
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
