# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

from RatingCurveViewerToolFrame import *
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from datetime import *
import os
import re
import copy
import math
import json


class RatingCurveViewerToolManager(object):

    ## Constructor: (mode, path, stnNum, disMeasManager, lang, gui)
    ##      mode: displays certain print statements when set to "DEBUG"
    ##      path: file path to default folder location of rating files
    ##      stnNum: station number of the given station
    ##      disMeasManager: handle on DischargeMeasurementManager, used to send and pull data
    ##      lang: for displaying the dates in the Period of Applicability table
    ##      gui: handle on gui
    def __init__(self, mode, path, stnNum, disMeasManager, lang, gui, manager=None):
        self.manager = manager
        self.gui = gui

        if self.gui is not None:
            self.gui.manager = self

        self.mode = mode
        self.stnNum = stnNum
        self.disMeasManager = disMeasManager
        self.disMeasManager.RCVTMan = self
        self.lang = lang

        #variables to keep
        self.extension = None
        self.data = None
        self.period = None
        self.curveNum = None

        self.histData = None
        self.delHist = None # list of indexes of histData that are invalid (either no HG or Q)

        self.path = path

        # tuple structure
        self.shiftDiffDisch = None

        # Plotting vars
        self.minList = [] ## For historical min values
        self.maxList = [] ## For historical max values
        self.qrta = None  ## discharge curve points
        self.hgta = None  ## stage curve points
        self.dischargeHist = None  ## Historical Discharge values
        self.stageHist = None  ## Historical Stage values
        self.validHistPoints = None  ## Historical points (includes label, discharge, and stage
        self._obsDisch = None  ## observed Discharge value
        self._obsStage = None  ## observed Stage value
        self.qrpa = None  ## list of discharge (qr) rating points
        self.hrpa = None  ## list of stage (hg) rating points
        self.Hr = None  ## used for shift calculations
        self.Qr = None  ## used for discharge calculations
        self.Shift = None  ## shift
        self.Qdiff = None  ## discharge diff
        self.comment = "QDiff(%) > 5%."
        self.comment2 = "QDiff(%) < 5%."

        self.ratingCurveList = []
        self.rcIndex = 0

        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "RatingCurveViewerToolControl"

        # self.locale = wx.Locale(self.lang)

    @property
    def obsDisch(self):
        return self._obsDisch

    @obsDisch.setter
    def obsDisch(self, val):
        self._obsDisch = float(val) if val != "" and val is not None else None

        if self.gui is not None:
            self.gui.SetObsDisch("" if self._obsDisch is None else str(self._obsDisch))

    @property
    def obsStage(self):
        return self._obsStage

    @obsStage.setter
    def obsStage(self, val):
        self._obsStage = float(val) if val != "" and val is not None else None

        if self.gui is not None:
            self.gui.SetObsStage("" if self._obsStage is None else str(self._obsStage))


    def GetFormattedRatedDischarge(self):
        return float(format(self.Qr, ".3g"))
    

    def OpenRatingFile(self, filepath):
        #filepath formatting for gui
        splitFilepath = filepath.split("\\")
        concatenatedFilepath = "...\\"
        if len(splitFilepath) >= 2:
            concatenatedFilepath += splitFilepath[-2] + "\\"
        concatenatedFilepath += splitFilepath[-1]

        if self.gui is not None:
            self.gui.ratingInfoText.SetLabel(concatenatedFilepath)

        #determine what to do based on the extension
        extension = self.DetFileType(filepath)

        if extension is not None:
            if extension == "xml":
                self.ParseRatingXMLFile(filepath)
            elif extension == "txt":
                self.ParseRatingTXTFile(filepath)
            elif extension == 'json':
                self.ParseRatingJsonFile(filepath)

    def OpenHistDataFile(self, filepath):
        #filepath formatting for gui
        splitFilepath = filepath.split("\\")
        concatenatedFilepath = "...\\"
        if len(splitFilepath) >= 2:
            concatenatedFilepath += splitFilepath[-2] + "\\"
        concatenatedFilepath += splitFilepath[-1]

        if self.gui is not None:
            self.gui.histFieldDataText.SetLabel(concatenatedFilepath)

        extension = self.DetFileType(filepath)

        if extension is not None:
            if extension == "csv":
                self.ParseHistCSVFile(filepath)


    def FindStationFile(self):
        # try and grab station number from genInfoManager first
        # updating the RatingCurve in the Fetch function will 
        # automatically load the historical data
        self.FetchStageDischarge()

        self.LoadRatingFile()

        if self.gui is not None:
            self.LoadHistoricalData()


    def LoadRatingFile(self):
        shouldClearGui = False

        if self.stnNum is not "":
            xmlfilepath = self.path + "\\" + self.stnNum + "_ratingcurves.xml"
            jsonfilepath = self.path + "\\" + self.stnNum + "_ratingcurves.json"
            txtfilepath = self.path + "\\" + self.stnNum + "_RatingTable.txt"
            self.ratingCurveList = []

            # print xmlfilepath
            if os.path.isfile(xmlfilepath):
                self.OpenRatingFile(os.path.abspath(xmlfilepath))
            elif os.path.isfile(jsonfilepath):
                # print jsonfilepath
                self.OpenRatingFile(os.path.abspath(jsonfilepath))
            elif os.path.isfile(txtfilepath):
                self.OpenRatingFile(os.path.abspath(txtfilepath))
            else:
                shouldClearGui = True
        else:
            shouldClearGui = True

        if self.gui is not None:
            if shouldClearGui is True:
                self.gui.EnableXML(False)
                self.gui.ClearAllAppRows()
                self.gui.EmptyCalculatedFields()
                self.gui.SetRatingInfo("")
            else:
                self.gui.SetStatus("")


    def LoadHistoricalData(self):
        shouldClearGui = False

        if self.stnNum is not "":
            fvFilePath = self.path + "\\" + self.stnNum + "_FieldVisits.csv"
            jsonfvFilePath = self.path + "\\" + self.stnNum + "_FieldVisits.csv"
            csvfilepath = self.path + "\\" + self.stnNum + "_FieldVisitExport.csv"

            print fvFilePath
            if os.path.isfile(fvFilePath):
                self.OpenHistDataFile(os.path.abspath(fvFilePath))
            elif os.path.isfile(jsonfvFilePath):
                self.OpenHistDataFile(os.path.abspath(jsonfvFilePath))
            elif os.path.isfile(csvfilepath):
                self.OpenHistDataFile(os.path.abspath(csvfilepath))
            else:
                shouldClearGui = True
        else:
            shouldClearGui = True

        if self.gui is not None:
            if shouldClearGui is True:
                self.gui.ClearAllHistRows()
            else:
                self.gui.SetStatus("")


    def DetFileType(self, filepath):
        if self.mode == "DEBUG":
            print "Determining File Type"

        extension = filepath.strip().split('.')[-1]
        if self.mode == "DEBUG":
            print "RC file is ", extension

        if extension.lower() == "txt" or extension.lower() == "xml" or extension.lower() == "json":
            self.extension = extension
            return extension
        elif extension.lower() == "csv":
            return extension
        else:
            self.extension = None
            return None

    #stores the XML tree in memory
    #saved as self.data
    #called when browse button is clicked
    def ParseRatingXMLFile(self, filepath):
        if self.mode == "DEBUG":
            print "Parsing XML File"

        # Changing data stuff, reset self.data to None
        self.data = None
        self.period = None
        self.curveNum = None
        self.shiftDiffDisch = None

        #Clear old table
        if self.gui is not None:
            self.gui.ClearAllAppRows()
            self.gui.EnableXML(True)

        #Do Parsing
        Curves = ElementTree.parse(filepath).getroot()

        #Curve
        data = []
        for curveInd, curve in enumerate(Curves.findall('curve')):
            periods = []
            ps = curve.find('periods')
            if ps is not None:
                for perInd, period in enumerate(ps.findall('period')):
                    periods.append(period)

            points = []
            pts = curve.find('ratingpoints')
            if pts is not None:
                for ptsInd, pt in enumerate(pts.findall('ratingpoint')):
                    points.append(pt)

            data.append((curve, periods, points))

        data.reverse()
        self.data = data
        self.ratingCurveList = [str(x[0].get('id')) for x in data]

        if self.gui is not None:
            #Update the list on the GUI
            #First format the dates
            for i, curve in enumerate(data):
                curveNum = str(curve[0].get('id'))

                curve[1].reverse()
                for j, period in enumerate(curve[1]):
                    curveFromDate = datetime.strptime(str(period.find('start').text), "%Y-%m-%dT%H:%M:%S")
                    curveToDate = datetime.strptime(str(period.find('end').text), "%Y-%m-%dT%H:%M:%S")

                    convertedFromDate = curveFromDate.strftime("%B %d %Y")
                    convertedToDate = curveToDate.strftime("%B %d %Y")

                    #Convert to "blank"
                    convertedFromDate = "" if convertedFromDate == "December 30 2382" else convertedFromDate
                    convertedToDate = "" if convertedToDate == "December 30 2382" else convertedToDate

                    curveNumStr = curveNum
                    if j > 0:
                        curveNumStr += " (" + str(j+1) + ")"
                    self.gui.AddRowToAppRange(curveNumStr, convertedFromDate, convertedToDate)

            self.gui.SetCurveCombo(self.ratingCurveList, self.rcIndex)

    def ParseRatingTXTFile(self, filepath):
        if self.mode == "DEBUG":
            print "Parsing TXT File"

        # Changing data stuff, reset self.data to None
        self.data = None
        self.period = None
        self.curveNum = None

        if self.gui is not None:
            #Clear xml table before disabling
            self.gui.ClearAllAppRows()
            self.gui.EnableXML(False)

        textFile = open(filepath, "r")
        data = textFile.readlines()
        data = [x.split() for x in data]

        for i, row in enumerate(data):
            row[0] = float(row[0])
            row[1] = float(row[1])

        self.data = data
        self.SetupCurveFromTxt()

        self.ratingCurveList = []

        if self.gui is not None:
            self.gui.SetCurveCombo(self.ratingCurveList, self.rcIndex) # triggers hist values update

        return self.ratingCurveList

    def ParseRatingJsonFile(self, filepath):
        if self.mode == "DEBUG":
            print "Parsing Json File"
        # print"under constraction!!"
        # Changing data stuff, reset self.data to None
        self.data = None
        self.period = None
        self.curveNum = None
        self.shiftDiffDisch = None
        self.periodData = []
        self.curveIdList = []

        # Clear old table
        if self.gui is not None:
            self.gui.ClearAllAppRows()
            self.gui.EnableXML(True)

        json_filepath = str(filepath.replace('\\', '\\\\'))
        # print type(json_filepath),json_filepath
        try:
            with open(json_filepath) as curves_data:
                Curves = json.load(curves_data)
                self.data = Curves
                # print Curves
        except:
            print "Json file can't read."

        curves_data = Curves['RatingCurves']
        # print len(curves_data)
        curves_data.reverse()

        for curv in curves_data:
            curveId = str(curv['Id'])
            curvePeriod = curv['PeriodsOfApplicability']
            idNum = 1
            self.ratingCurveList.append(curveId)
            if self.gui is not None:
                for curvPeriod in curvePeriod:
                    curveFromDate = datetime.strptime(str(curvPeriod['StartTime'])[0:-14], "%Y-%m-%dT%H:%M:%S")
                    if int(curveFromDate.strftime("%Y")) < 1800 or int(curveFromDate.strftime("%Y")) > 2500:
                        convertedFromDate = ''
                    else:
                        convertedFromDate = curveFromDate.strftime("%B %d %Y")
                    # curveFromDate = curvPeriod['StartTime']

                    curveToDate = datetime.strptime(str(curvPeriod['EndTime'])[0:-14], "%Y-%m-%dT%H:%M:%S")
                    if int(curveToDate.strftime("%Y")) < 1800 or int(curveToDate.strftime("%Y")) > 2500:
                        convertedToDate = ''
                    else:
                        convertedToDate = curveToDate.strftime("%B %d %Y")
                    # curveToDate = curvPeriod['EndTime']
                    if idNum != 1:
                        curveNewId = curveId + '(' + str(idNum) + ')'
                    else:
                        curveNewId = curveId
                    idNum = idNum + 1
                    # print curveNewId,convertedFromDate,convertedToDate

                    self.gui.AddRowToAppRange(curveNewId, convertedFromDate, convertedToDate)

                    curvPeriData = []
                    curvPeriData.append(str(curveNewId))
                    curvPeriData.append(str(convertedFromDate))
                    curvPeriData.append(str(convertedToDate))

                    self.periodData.append(curvPeriData)
                    self.gui.SetCurveCombo(self.ratingCurveList, self.rcIndex)
        return self.ratingCurveList

    def OnRCUpdate(self, selectedCurveIndex):
        if self.gui is not None:
            self.gui.ClearAllHistRows()

        if self.histData is None:
            return

        print "Hist data is not None"

        # iterate through each hist value
        # for each, calc appropriate Shift and
        for i, row in enumerate(reversed(self.histData)):
            shift = None
            error = None

            # print row

            date = row[0]
            stage = row[1]
            disch = row[2]
            width = row[3]
            area = row[4]
            waterVelo = row[5]
            remarks = row[6]

            if disch == "" or stage == "":
                shift = ""
                error = ""
            else:
                if self.extension == "xml":
                    RCType = self.data[selectedCurveIndex][0].get('type')
                    points = self.data[selectedCurveIndex][2]

                    # Check bounds
                    hg_low = float(points[0].find('hg').text)
                    hg_high = float(points[-1].find('hg').text)
                    q_low = float(points[0].find('qr').text)
                    q_high = float(points[-1].find('qr').text)

                    if stage > hg_high or stage < hg_low \
                       or disch < q_low or disch > q_high:
                        shift = ""
                        error = ""

                    elif RCType == "Linear":
                        shift, error = self.CalcLinShiftQdiff(points, stage, disch)
                    elif RCType == "Logarithmic":
                        shift, error = self.CalcLogShiftQdiff(points, stage, disch)

                elif self.extension == "txt":
                    points = self.data

                    # Check bounds
                    hg_low = float(points[0][1])
                    hg_high = float(points[-1][1])
                    q_low = float(points[0][0])
                    q_high = float(points[-1][0])

                    if stage > hg_high or stage < hg_low \
                       or disch < q_low or disch > q_high:
                        shift = ""
                        error = ""
                    else:
                        shift, error = self.CalcTxtShiftQdiff(points, stage, disch)

                # json file
                else:
                    RCType = self.data['RatingCurves'][selectedCurveIndex]['Type']
                    points = self.data['RatingCurves'][selectedCurveIndex]
                    # print points
                    # print RCType

                    # Check bounds
                    hg_low = float(points['BaseRatingTable'][0]['InputValue'])
                    hg_high = float(points['BaseRatingTable'][-1]['InputValue'])
                    q_low = float(points['BaseRatingTable'][0]['OutputValue'])
                    q_high = float(points['BaseRatingTable'][-1]['OutputValue'])
                    # print i, stage, hg_high, hg_low, disch, q_low, q_high
                    if stage > hg_high or stage < hg_low \
                        or disch < q_low or disch > q_high:
                        shift = ""
                        error = ""

                    elif RCType == "LinearTable":
                        # print "Linear"
                        shift, error = self.CalcLinShiftQdiffJson(points, stage, disch)
                    elif RCType == "LogarithmicTable":
                        # print "Logarithmic"
                        shift, error = self.CalcLogShiftQdiffJson(points, stage, disch)

            self.gui.AddRowToHistData(date, str(stage), str(disch), str(width), str(area), str(waterVelo), str(error), str(shift), str(remarks))

        if self.gui is not None:
            ### TODO look at if this function will work for json too? if yes then remove the condition
            if self.extension == "xml":
                self.CalculateShiftDisch(self.obsStage, self.obsDisch, selectedCurveIndex)


    def ValidateQdiff(self, q, Qr):
        if Qr == 0 or math.isnan(Qr):
            return float('nan')

        return float(format(((q - Qr)/Qr)*100,".3g"))


    def CalcLinQrHr(self, points, hg, q):
        a = None
        b = None
        a2 = None
        b2 = None

        hgFound = False
        qFound = False

        #a and b to calculate Qdiff
        for i, point in enumerate(points):
            hgpas = float(point.find('hg').text)
            qpas = float(point.find('qr').text)

            if hg <= hgpas and not hgFound:
                equation = point.find('equation')
                if equation is not None:
                    a = float(equation.find('a').text)
                    b = float(equation.find('b').text)
                    hgFound = True

            if q <= qpas and not qFound:
                equation = point.find('equation')
                if equation is not None:
                    a2 = float(equation.find('a').text)
                    b2 = float(equation.find('b').text)
                    qFound = True

            if qFound and hgFound:
                break

        # Do Calculations
        Qr=(a * hg)+ b
        Hr=(1/a2 * (q - b2))

        return Qr, Hr

    # TODO test if this will work if yes split later
    def CalcLinShiftQdiffJson(self, points, hg, q):
        a = None
        b = None
        a2 = None
        b2 = None

        # a and b to calculate Qdiff
        # print len(points['BaseRatingTable'])
        for i in range(len(points['BaseRatingTable'])):

            hgpas = float(points['BaseRatingTable'][i]['InputValue'])
            # print hgpas, hg

            if hg < hgpas:
                lowPoint = points['BaseRatingTable'][i - 1]
                highPoint = points['BaseRatingTable'][i]
                a = (highPoint['OutputValue'] - lowPoint['OutputValue']) / (
                            highPoint['InputValue'] - lowPoint['InputValue'])
                b = highPoint['OutputValue'] - a * highPoint['InputValue']

                break

        # find a and b to calculate Shift
        for i in range(len(points['BaseRatingTable'])):
            qpas = float(points['BaseRatingTable'][i]['OutputValue'])

            if q < qpas:
                lowPoint = points['BaseRatingTable'][i - 1]
                highPoint = points['BaseRatingTable'][i]
                a2 = (highPoint['OutputValue'] - lowPoint['OutputValue']) / (
                            highPoint['InputValue'] - lowPoint['InputValue'])
                b2 = highPoint['OutputValue'] - a2 * highPoint['InputValue']
                break

        # Do Calculations
        # print a, hg, b
        if a is not None and b is not None and a2 is not None and b2 is not None:
            Qr = (a * hg) + b
            Hr = (1 / a2 * (q - b2))
            Shift = float(format(Hr - hg, ".3g"))
            Qdiff = float(format(((q - Qr) / Qr) * 100, ".3g"))
        else:
            Shift = ''
            Qdiff = ''

        return Shift, Qdiff


    def CalcLogQrHr(self, points, hg, q):
        offset = None
        beta = None
        c = None
        qoffset = None
        qbeta = None
        qc = None

        hg1 = None
        q1 = None
        qrPoints = None
        hrPoints = None

        hgFound = False
        qFound = False

        for i, point in enumerate(points):
            hg2 = float(point.find('hg').text)
            q2 = float(point.find('qr').text)

            if hg <= hg2 and not hgFound:
                equation = point.find('equation')
                if equation is not None:
                    offset = float(point.find('offset').text)
                    beta = float(equation.find('beta').text)
                    c = float(equation.find('c').text)

                    if math.isinf(beta) or math.isinf(c):
                        qrPoints = ( (hg1, q1), (hg2, q2) )

                    hgFound = True

            if q <= q2 and not qFound:
                equation = point.find('equation')
                if equation is not None:
                    qoffset = float(point.find('offset').text)
                    qbeta = float(equation.find('beta').text)
                    qc = float(equation.find('c').text)

                    if math.isinf(qbeta) or math.isinf(qc):
                        hrPoints = ( (hg1, q1), (hg2, q2) )
                    qFound = True

            if hgFound and qFound:
                break
            
            hg1 = hg2
            q1 = q2

        # Do the calculations
        if qrPoints is None:
            Qr = c * (hg - offset)**beta
        else:
            p1 = qrPoints[0]
            p2 = qrPoints[1]

            a = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b = p2[1] - a * p2[0]
            
            Qr = (a*hg) + b

        if hrPoints is None:
            Hr = qoffset+(q/qc)**(1/qbeta)
        else:
            p1 = hrPoints[0]
            p2 = hrPoints[1]

            a2 = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b2 = p2[1] - a2 * p2[0]

            Hr = (1/a2* (q-b2))

        return Qr, Hr

    def CalcLogQrHrJson(self, points, hg, q):
        offset = None
        beta = None
        c = None
        qoffset = None
        qbeta = None
        qc = None
        offsetList = []
        breakPointList = []

        for offset_val in points['Offsets']:
            offsetList.append(offset_val['Offset'])
            try:
                breakPointList.append(offset_val['InputValue'])
            except:
                pass

        for i in range(len(points['BaseRatingTable'])):
            hgpas = float(points['BaseRatingTable'][i]['InputValue'])

            if hg <= hgpas:
                lowPoint = points['BaseRatingTable'][i-1]
                highPoint = points['BaseRatingTable'][i]
                for nn in range(len(breakPointList)):
                    if highPoint['InputValue']<=breakPointList[nn]:
                        offset = offsetList[nn]
                        beta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-offset)/(lowPoint['InputValue']-offset))
                        c = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-offset, beta)
                        break
                if offset is None:
                    offset = offsetList[-1]
                    beta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-offset)/(lowPoint['InputValue']-offset))
                    c = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-offset, beta)
                break


        # find offset, beta, c to calculate Shift
        for i in range(len(points['BaseRatingTable'])):
            qpas = float(points['BaseRatingTable'][i]['OutputValue'])

            if q <= qpas:
                lowPoint = points['BaseRatingTable'][i-1]
                highPoint = points['BaseRatingTable'][i]
                for nn in range(len(breakPointList)):
                    if highPoint['InputValue']<=breakPointList[nn]:
                        qoffset = offsetList[nn]
                        qbeta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-qoffset)/(lowPoint['InputValue']-qoffset))
                        qc = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-qoffset, qbeta)
                        break
                if qoffset is None:
                    qoffset = offsetList[-1]
                    qbeta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-qoffset)/(lowPoint['InputValue']-qoffset))
                    qc = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-qoffset, qbeta)
                break

        # Do the calculations
        if c is not None and qc is not None and offset is not None and qoffset is not None and beta is not None and qbeta is not None:
            Qr=c * (hg - offset)**beta
            Hr=qoffset+(q/qc)**(1/qbeta)
        # print hgpas, qpas, offset, beta, qoffset, qbeta
        return Qr, Hr

    # TODO test it and if work maybe split it later
    def CalcLogShiftQdiffJson(self, points, hg, q):
        offset = None
        beta = None
        c = None
        qoffset = None
        qbeta = None
        qc = None
        offsetList = []
        breakPointList = []

        for offset_val in points['Offsets']:
            offsetList.append(offset_val['Offset'])
            try:
                breakPointList.append(offset_val['InputValue'])
            except:
                pass

        for i in range(len(points['BaseRatingTable'])):
            hgpas = float(points['BaseRatingTable'][i]['InputValue'])

            if hg < hgpas:
                lowPoint = points['BaseRatingTable'][i-1]
                highPoint = points['BaseRatingTable'][i]
                for nn in range(len(breakPointList)):
                    if highPoint['InputValue']<=breakPointList[nn]:
                        offset = offsetList[nn]
                        beta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-offset)/(lowPoint['InputValue']-offset))
                        c = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-offset, beta)
                if offset is None:
                    offset = offsetList[-1]
                    beta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-offset)/(lowPoint['InputValue']-offset))
                    c = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-offset, beta)
                break


        # find offset, beta, c to calculate Shift
        for i in range(len(points['BaseRatingTable'])):
            qpas = float(points['BaseRatingTable'][i]['OutputValue'])

            if q < qpas:
                lowPoint = points['BaseRatingTable'][i-1]
                highPoint = points['BaseRatingTable'][i]
                for nn in range(len(breakPointList)):
                    if highPoint['InputValue']<=breakPointList[nn]:
                        qoffset = offsetList[nn]
                        qbeta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-qoffset)/(lowPoint['InputValue']-qoffset))
                        qc = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-qoffset, beta)
                if qoffset is None:
                    qoffset = offsetList[-1]
                    qbeta = math.log10(highPoint['OutputValue']/lowPoint['OutputValue'])/math.log10((highPoint['InputValue']-qoffset)/(lowPoint['InputValue']-qoffset))
                    qc = lowPoint['OutputValue']/math.pow(lowPoint['InputValue']-qoffset, beta)
                break

        # Do the calculations
        if c is not None and qc is not None and offset is not None and qoffset is not None and beta is not None and qbeta is not None:
            Qr=c * (hg - offset)**beta
            Hr=qoffset+(q/qc)**(1/qbeta)
            Shift = float(format(Hr-hg,".3g"))
            Qdiff = float(format(((q-Qr)/Qr)*100,".3g"))

        else:
            Shift = ''
            Qdiff = ''

        # print hgpas, qpas, offset, beta, qoffset, qbeta

        return Shift, Qdiff


    def CalcLinShiftQdiff(self, points, hg, q):
        Qr, Hr = self.CalcLinQrHr(points, hg, q)

        Shift = float(format(Hr - hg,".3g"))
        Qdiff = self.ValidateQdiff(q, Qr)

        return Shift, Qdiff


    def CalcLogShiftQdiff(self, points, hg, q):
        Qr, Hr = self.CalcLogQrHr(points, hg, q)

        Shift = float(format(Hr-hg,".3g"))
        Qdiff = self.ValidateQdiff(q, Qr)

        return Shift, Qdiff


    def CalcTxtQrHr(self, points, hg, q):
        # Qr calculations
        qr_hg1 = qr_hg2 = qr_q1 = qr_q2 = None

        # Hr calculations
        hr_hg1 = hr_hg2 = hr_q1 = hr_q2 = None

        hgFound = False
        qFound = False

        for i, row in enumerate(points):
            qpas = row[0]
            hgpas = row[1]

            if hg <= hgpas and not hgFound:
                qr_hg1 = self.data[i-1][1]
                qr_q1 = self.data[i-1][0]
                qr_hg2 = row[1]
                qr_q2 = row[0]
                
                hgFound = True

            if q <= qpas and not qFound:
                hr_hg1 = self.data[i-1][1]
                hr_q1 = self.data[i-1][0]
                hr_hg2 = row[1]
                hr_q2 = row[0]
                
                qFound = True

            if hgFound and qFound:
                break

        a1 = (qr_q2 - qr_q1) / (qr_hg2 - qr_hg1)
        b1 = qr_q2 - a1 * qr_hg2

        a2 = (hr_q2 - hr_q1) / (hr_hg2 - hr_hg1)
        b2 = hr_q2 - a2 * hr_hg2

        # Do calculations
        Qr = (a1*hg)+ b1
        Hr = (1/a2* (q-b2))

        return Qr, Hr


    def CalcTxtShiftQdiff(self, points, hg, q):
        Qr, Hr = self.CalcTxtQrHr(points, hg, q)

        Shift = float(format(Hr-hg,".3g"))
        Qdiff = self.ValidateQdiff(q, Qr)

        return Shift, Qdiff


    def ParseHistCSVFile(self, filepath):
        if self.mode == "DEBUG":
            print "Parsing CSV Historical Data File"

        # Reset Historical Data
        self.histData = None
        self.delHist = None
        self.minList = []
        self.maxList = []

        if self.gui is not None:
            self.gui.ClearAllHistRows()

        csvFile = open(filepath, "r")
        histData = csvFile.readlines()[1:]
        histData = [x.strip().split(',') for x in histData]

        listToDel = []

        for i, row in enumerate(histData):
            # print "####################"
            # print row
            if row[1] == "" or row[2] == "":
                listToDel.append(i)
            row[1] = "" if row[1] == "" else float(row[1])
            row[2] = "" if row[2] == "" else float(row[2])
            if "min" in row[6].lower():
                self.minList.append(row)
            if "max" in row[6].lower():
                self.maxList.append(row)

        # delete invalid historical data values
        self.delHist = listToDel
        self.histData = histData

        if self.gui is not None:
            self.OnRCUpdate(self.gui.GetSelectedCurveIndex())


    def CalculateShiftDisch(self, Hobserved, Qobserved, selectedCurveIndex):
        if self.mode == "DEBUG":
            print "Calculating Shift and Discharge"

        errorMessage = None
        if self.extension is None:
            errorMessage = "Please use a valid Rating Curve File - it is an XML file best extracted from the ADET"

        elif Hobserved == "":
            #show error dialog
            errorMessage = "Observed Stage is empty. Please enter a value."

        elif Qobserved == "":
            #show error dialog
            errorMessage = "Observed Discharge is empty. Please enter a value."

        elif self.extension == "xml":
            if selectedCurveIndex < 0 or selectedCurveIndex >= len(self.ratingCurveList):
                errorMessage = "Rating Curve file is invalid."

        # TODO add checking for json file

        # Check if anything went wrong
        if errorMessage is not None:
            if self.gui is not None:
                self.gui.SetStatus(errorMessage)
            return errorMessage 

        # Reset shift/disch calculations
        self.shiftDiffDisch = None
        self.ResetPlotVars()

        # Store obsDisch, obsStage
        self.obsDisch = Qobserved
        self.obsStage = Hobserved
        self.rcIndex = selectedCurveIndex
        
        if self.gui is not None:
            self.gui.ratingCurveCombo.SetSelection(self.rcIndex)

        if self.extension == "xml":
            return self.CalculateXMLShiftDisch(selectedCurveIndex)
        elif self.extension == "txt":
            return self.CalculateTXTShiftDisch(selectedCurveIndex)
        elif self.extension == "json":
            return self.CalculateJSONShiftDisch(selectedCurveIndex)

    # Calculate shift and discharge for json file reading
    def CalculateJSONShiftDisch(self, selectedCurveIndex):
        RCType = self.data['RatingCurves'][selectedCurveIndex]['Type']
        self.curveNum = self.data['RatingCurves'][selectedCurveIndex]['Id']

        # points list
        points = self.data['RatingCurves'][selectedCurveIndex]['BaseRatingTable']
        calPoints = self.data['RatingCurves'][selectedCurveIndex]

        # Determine Period (for historical data only)
        start = None
        end = None
        for i, period in enumerate(self.data['RatingCurves'][selectedCurveIndex]['PeriodsOfApplicability']):
            if i == 0:
                start = datetime.strptime(str(period['StartTime'])[0:-14], "%Y-%m-%dT%H:%M:%S")
                end = datetime.strptime(str(period['EndTime'])[0:-14], "%Y-%m-%dT%H:%M:%S")
            else:
                currStart = datetime.strptime(str(period['StartTime'])[0:-14], "%Y-%m-%dT%H:%M:%S")
                currEnd = datetime.strptime(str(period['EndTime'])[0:-14], "%Y-%m-%dT%H:%M:%S")

                if start > currStart:
                    start = currStart
                if end < currEnd:
                    end = currEnd

        if start is None or end is None:
            self.period = None
        else:
            self.period = (start, end)


        # assumes that the first point is lowest, last point is highest
        # checks against high and low points first
        hg_low = float(calPoints['BaseRatingTable'][0]['InputValue'])
        hg_high = float(calPoints['BaseRatingTable'][-1]['InputValue'])
        q_low = float(calPoints['BaseRatingTable'][0]['OutputValue'])
        q_high = float(calPoints['BaseRatingTable'][-1]['OutputValue'])

        errorMessage = self.ValidateCalculations(hg_low, hg_high, q_low, q_high)
        if errorMessage is not None:
            return errorMessage
        #-----------------------Calculations: Shift and Discharge Diff(%)Shift and Discharge Diff(%)-----------------------#
        #Calculations for Logarithmic Rating Curve Type.....
        if RCType == "LinearTable":
            self.CalculateLinearRCJson(calPoints, selectedCurveIndex)

        #Calculations for Logarithmic Rating Curve Type.....
        elif RCType == "LogarithmicTable":
            self.CalculateLogRCJson(calPoints, selectedCurveIndex)


    def ValidateCalculations(self, hg_low, hg_high, q_low, q_high):
        errorMessage = None
        if self.obsStage < hg_low:
            if self.mode == "DEBUG":
                print "Observed Stage is below the minimum rating point"

            errorMessage = "Observed Stage is below the minimum rating point"

        elif self.obsStage > hg_high:
            if self.mode == "DEBUG":
                print "Observed Stage is above the maximum rating point"

            errorMessage = "Observed Stage is above the maximum rating point"
            
        if self.obsDisch < q_low:
            if self.mode == "DEBUG":
                print "Observed Discharge is below the minimum rating point"

            errorMessage = "Observed Discharge is below the minimum rating point"

        elif self.obsDisch > q_high:
            if self.mode == "DEBUG":
                print "Observed Discharge is above the maximum rating point"

            errorMessage = "Observed Discharge is above the maximum rating point"

        # if there was an error, return 
        if errorMessage is not None:
            if self.gui is not None:
                self.gui.SetCalcShift("")
                self.gui.SetRatedDisch("")
                self.gui.SetDischDiff("")

                self.gui.SetStatus(errorMessage)
            
        return errorMessage


    def CalculateXMLShiftDisch(self, selectedCurveIndex):
        RCType = self.data[selectedCurveIndex][0].get('type')
        self.curveNum = self.data[selectedCurveIndex][0].get("id")

        # points list
        points = self.data[selectedCurveIndex][2]

        # plotted rating points
        self.qrta = [float(x.find('qr').text) for x in self.data[selectedCurveIndex][2]]
        self.hgta = [float(x.find('hg').text) for x in self.data[selectedCurveIndex][2]]


        # Determine Period (for historical data only)
        start = None
        end = None
        for i, period in enumerate(self.data[selectedCurveIndex][1]):
            if i == 0:
                start = datetime.strptime(str(period.find('start').text), "%Y-%m-%dT%H:%M:%S")
                end = datetime.strptime(str(period.find('end').text), "%Y-%m-%dT%H:%M:%S")
            else:
                currStart = datetime.strptime(str(period.find('start').text), "%Y-%m-%dT%H:%M:%S")
                currEnd = datetime.strptime(str(period.find('end').text), "%Y-%m-%dT%H:%M:%S")

                if start > currStart:
                    start = currStart
                if end < currEnd:
                    end = currEnd

        if start is None or end is None:
            self.period = None
        else:
            self.period = (start, end)


        # assumes that the first point is lowest, last point is highest
        # checks against high and low points first
        hg_low = float(points[0].find('hg').text)
        hg_high = float(points[-1].find('hg').text)
        q_low = float(points[0].find('qr').text)
        q_high = float(points[-1].find('qr').text)

        errorMessage = self.ValidateCalculations(hg_low, hg_high, q_low, q_high)
        if errorMessage is not None:
            return errorMessage

        #-----------------------Calculations: Shift and Discharge Diff(%)Shift and Discharge Diff(%)-----------------------#
        #Calculations for Logarithmic Rating Curve Type.....
        if RCType == "Linear":
            self.CalculateLinearRC(points, selectedCurveIndex)

        #Calculations for Logarithmic Rating Curve Type.....
        elif RCType == "Logarithmic":
            self.CalculateLogRC(points, selectedCurveIndex)

    def CalcLinQrHrJson(self, points, hg, q):
        a = None
        b = None
        a2 = None
        b2 = None

        # a and b to calculate Qdiff
        # print len(points['BaseRatingTable'])
        for i in range(len(points['BaseRatingTable'])):

            hgpas = float(points['BaseRatingTable'][i]['InputValue'])
            # print hgpas, hg

            if hg <= hgpas:
                lowPoint = points['BaseRatingTable'][i - 1]
                highPoint = points['BaseRatingTable'][i]
                a = (highPoint['OutputValue'] - lowPoint['OutputValue']) / (
                            highPoint['InputValue'] - lowPoint['InputValue'])
                b = highPoint['OutputValue'] - a * highPoint['InputValue']

                break

        # find a and b to calculate Shift
        for i in range(len(points['BaseRatingTable'])):
            qpas = float(points['BaseRatingTable'][i]['OutputValue'])

            if q <= qpas:
                lowPoint = points['BaseRatingTable'][i - 1]
                highPoint = points['BaseRatingTable'][i]
                a2 = (highPoint['OutputValue'] - lowPoint['OutputValue']) / (
                            highPoint['InputValue'] - lowPoint['InputValue'])
                b2 = highPoint['OutputValue'] - a2 * highPoint['InputValue']
                break

        # Do Calculations
        # print a, hg, b
        if a is not None and b is not None and a2 is not None and b2 is not None:
            Qr = (a * hg) + b
            Hr = (1 / a2 * (q - b2))

        return Qr, Hr


    def CalculateLinearRC(self, points, selectedCurveIndex):
        # Do Calculations
        self.Qr, self.Hr = self.CalcLinQrHr(points, self.obsStage, self.obsDisch)

        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = self.ValidateQdiff(self.obsDisch, self.Qr)

        # Set Text Fields in the gui
        if self.gui is not None:
            self.gui.SetCalcShift(str(self.Shift))
            self.gui.SetRatedDisch(str(self.GetFormattedRatedDischarge()))
            self.gui.SetDischDiff(str(self.Qdiff))


    def CalculateLogRC(self, points, selectedCurveIndex):
        # Do the calculations
        self.Qr, self.Hr = self.CalcLogQrHr(points, self.obsStage, self.obsDisch)

        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = self.ValidateQdiff(self.obsDisch, self.Qr)

        # Set Text Fields in the gui
        if self.gui is not None:
            self.gui.SetCalcShift(str(self.Shift))
            self.gui.SetRatedDisch(str(self.GetFormattedRatedDischarge()))
            self.gui.SetDischDiff(str(self.Qdiff))


    def CalculateLinearRCJson(self, points, selectedCurveIndex):
        # Do Calculations
        self.Qr, self.Hr = self.CalcLinQrHrJson(points, self.obsStage, self.obsDisch)

        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = self.ValidateQdiff(self.obsDisch, self.Qr)

        # Set Text Fields in the gui
        if self.gui is not None:
            self.gui.SetCalcShift(str(self.Shift))
            self.gui.SetRatedDisch(str(self.GetFormattedRatedDischarge()))
            self.gui.SetDischDiff(str(self.Qdiff))


    def CalculateLogRCJson(self, points, selectedCurveIndex):
        # Do the calculations
        self.Qr, self.Hr = self.CalcLogQrHrJson(points, self.obsStage, self.obsDisch)

        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = self.ValidateQdiff(self.obsDisch, self.Qr)

        # Set Text Fields in the gui
        if self.gui is not None:
            self.gui.SetCalcShift(str(self.Shift))
            self.gui.SetRatedDisch(str(self.GetFormattedRatedDischarge()))
            self.gui.SetDischDiff(str(self.Qdiff))



    def SetupCurveFromTxt(self):
        # In the table, it's discharge, stage
        # in other words, [x][0] is discharge, [x][1] is stage
        self.qrta = [x[0] for x in self.data]
        self.hgta = [x[1] for x in self.data]


    def CalculateTXTShiftDisch(self):
        self.SetupCurveFromTxt()

        # assumes that the first point is lowest, last point is highest
        # checks against high and low points first
        hg_low = float(self.data[0][1])
        hg_high = float(self.data[-1][1])
        q_low = float(self.data[0][0])
        q_high = float(self.data[-1][0])

        errorMessage = self.ValidateCalculations(hg_low, hg_high, q_low, q_high)
        if errorMessage is not None:
            return errorMessage

        # Do calculations
        self.Qr, self.Hr = self.CalcTxtQrHr(self.data, self.obsStage, self.obsDisch)

        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = self.ValidateQdiff(self.obsDisch, self.Qr)

        # Set Text Fields in the gui
        if self.gui is not None:
            self.gui.SetCalcShift(str(self.Shift))
            self.gui.SetRatedDisch(str(self.GetFormattedRatedDischarge()))
            self.gui.SetDischDiff(str(self.Qdiff))


    def PlotData(self):
        if self.mode == "DEBUG":
            print "Plotting Data"
            return None

        # If historical data exists
        if self.histData is not None:
            histData = copy.deepcopy(self.histData)

            for i, index in enumerate(self.delHist):

                del histData[index - (i + 1)]

            for i, hd in enumerate(histData):
                hd[0] = hd[0].split()[0] # Only the YYYY-MM-DD part
                hd[0] = datetime.strptime(hd[0], "%Y-%m-%d")
                print hd
                print self.histData[i]

            if self.period is not None:
                self.validHistPoints = [x for x in histData if x[0] < self.period[1] and x[0] > self.period[0]]
                self.stageHist = [x[1] for x in histData if x[0] < self.period[1] and x[0] > self.period[0]]
                self.dischargeHist = [x[2] for x in histData if x[0] < self.period[1] and x[0] > self.period[0]]

            else:
                self.validHistPoints = [x for x in histData]
                self.stageHist = [x[1] for x in histData]
                self.dischargeHist = [x[2] for x in histData]

        # XML
        # Make QRTA and HGTA from rating points
        # need to know the equation with c, offset and beta for filling the table
        self.gui.EnablePlot(False)
        self.gui.GeneratePlot()

        self.gui.EnablePlot(True)

    def ResetPlotVars(self):
        self.qrta = None
        self.hgta = None
        self.dischargeHist = None
        self.stageHist = None
        #self.minMaxList = []
        self.validHistPoints = None
        self.obsDisch = None
        self.obsStage = None
        self.Hr = None
        self.Qr = None


    def FetchStageDischarge(self):
        if self.mode == "DEBUG":
            print "Getting Stage and Discharge"

        if self.disMeasManager is None:
            return

        if self.manager is not None:
            self.stnNum = self.manager.genInfoManager.stnNumCmbo
            self.stnNum = self.stnNum if self.stnNum != "" else ""

        self.obsStage = self.disMeasManager.mghCtrl
        self.obsDisch = self.disMeasManager.dischCtrl

        # if the rating curve index from the discharge measurement manager was valid
        # set the rcIndex to that index, if invalid then default to 0
        self.rcIndex = self.disMeasManager.GetCurrentCurveIndexInList(self.ratingCurveList)
        self.rcIndex = self.rcIndex if self.rcIndex >= 0 and self.rcIndex < len(self.ratingCurveList) else 0

        if self.gui is not None:
            self.gui.ratingCurveCombo.SetSelection(self.rcIndex)

            self.gui.SetCalcShift("" if self.Shift is None else str(self.Shift))
            self.gui.SetRatedDisch("" if self.Qr is None else str(self.GetFormattedRatedDischarge()))
            self.gui.SetDischDiff("" if self.Qdiff is None else str(self.Qdiff))


def main():
    app = wx.App()

    frame = RatingCurveViewerToolFrame("DEBUG", os.getcwd() + "\\RC docs", None, None, wx.LANGUAGE_ENGLISH, None, size=(770, 578))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
