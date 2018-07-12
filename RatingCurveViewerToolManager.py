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


class RatingCurveViewerToolManager(object):

    ## Constructor: (mode, path, stnNum, disMeasManager, lang, gui)
    ##      mode: displays certain print statements when set to "DEBUG"
    ##      path: file path to default folder location of rating files
    ##      stnNum: station number of the given station
    ##      disMeasManager: handle on DischargeMeasurementManager, used to send and pull data
    ##      lang: for displaying the dates in the Period of Applicability table
    ##      gui: handle on gui
    def __init__(self, mode, path, stnNum, disMeasManager, lang, gui):
        self.gui = gui
        self.gui.manager = self
        self.mode = mode
        self.stnNum = stnNum
        self.disMeasManager = disMeasManager
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
        self.obsDisch = None  ## observed Discharge value
        self.obsStage = None  ## observed Stage value
        self.qrpa = None  ## list of discharge (qr) rating points
        self.hrpa = None  ## list of stage (hg) rating points
        self.Hr = None  ## used for shift calculations
        self.Qr = None  ## used for discharge calculations
        self.Shift = None  ## shift
        self.Qdiff = None  ## discharge diff
        self.comment = "QDiff(%) > 5%."
        self.comment2 = "QDiff(%) < 5%."


        self.Init()

    def Init(self):
        if self.mode == "DEBUG":
            print "RatingCurveViewerToolControl"

        # self.locale = wx.Locale(self.lang)

        #Set Observed Stage and Observed Discharge
        self.FetchStageDischarge()

    def FindStationFile(self):
        if self.stnNum is not None:
            xmlfilepath = self.path + "\\" + self.stnNum + "_ratingcurves.xml"
            txtfilepath = self.path + "\\" + self.stnNum + "_RatingTable.txt"
            fvFilePath = self.path + "\\" + self.stnNum + "_FieldVisits.csv"

            print xmlfilepath
            print fvFilePath
            if os.path.isfile(xmlfilepath):
                self.gui.OpenRatingFile(os.path.abspath(xmlfilepath))
            elif os.path.isfile(txtfilepath):
                self.gui.OpenRatingFile(os.path.abspath(txtfilepath))
            if os.path.isfile(fvFilePath):
                self.gui.OpenHistDataFile(os.path.abspath(fvFilePath))

            csvfilepath = self.path + "\\" + self.stnNum + "_FieldVisitExport.csv"
            if os.path.isfile(csvfilepath):
                self.gui.OpenHistDataFile(os.path.abspath(csvfilepath))



    def DetFileType(self, filepath):
        if self.mode == "DEBUG":
            print "Determining File Type"

        extension = filepath.strip().split('.')[-1]
        if self.mode == "DEBUG":
            print "RC file is ", extension

        if extension.lower() == "txt" or extension.lower() == "xml":
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

        rcList = [str(x[0].get('id')) for x in data]
        self.gui.SetCurveCombo(rcList)


    def ParseRatingTXTFile(self, filepath):
        if self.mode == "DEBUG":
            print "Parsing TXT File"

        # Changing data stuff, reset self.data to None
        self.data = None
        self.period = None
        self.curveNum = None

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
        self.gui.SetCurveCombo([]) # triggers hist values update


    def OnRCUpdate(self):
        print "Update"

        if self.histData is None:
            return

        print "Hist data is not None"

        self.gui.ClearAllHistRows()


        # iterate through each hist value
        # for each, calc appropriate Shift and
        for i, row in enumerate(reversed(self.histData)):
            shift = None
            error = None

            print row

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
                    selectedCurveIndex = self.gui.GetSelectedCurveIndex()

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

            self.gui.AddRowToHistData(date, str(stage), str(disch), str(width), str(area), str(waterVelo), str(error), str(shift), str(remarks))


    def CalcLinShiftQdiff(self, points, hg, q):
        a = None
        b = None

        #a and b to calculate Qdiff
        for i, hgpas in enumerate(points):

            hgpas = float(hgpas.find('hg').text)

            if hg < hgpas:
                equation = points[i].find('equation')
                if equation is not None:
                    a = float(equation.find('a').text)
                    b = float(equation.find('b').text)


                    break


        #find a and b to calculate Shift
        for i, qpas in enumerate(points):
            qpas = float(qpas.find('qr').text)

            if q < qpas:
                equation = points[i].find('equation')
                if equation is not None:
                    a2 = float(equation.find('a').text)
                    b2 = float(equation.find('b').text)
                    break




        # Do Calculations
        Qr=(a * hg)+ b
        Hr=(1/a2 * (q - b2))
        Shift = float(format(Hr - hg,".3g"))
        Qdiff = float(format(((q - Qr)/Qr)*100,".3g"))

        return Shift, Qdiff


    def CalcLogShiftQdiff(self, points, hg, q):
        offset = None
        beta = None
        c = None
        qoffset = None
        qbeta = None
        qc = None

        for i, hgpas in enumerate(points):
            hgpas = float(hgpas.find('hg').text)

            if hg < hgpas:
                equation = points[i].find('equation')
                if equation is not None:
                    offset = float(points[i].find('offset').text)
                    beta = float(equation.find('beta').text)
                    c = float(equation.find('c').text)
                    break



        # find offset, beta, c to calculate Shift
        for i, qpas in enumerate(points):
            qpas = float(qpas.find('hg').text)

            if hg < qpas:
                equation = points[i].find('equation')
                if equation is not None:
                    qoffset = float(points[i].find('offset').text)
                    qbeta = float(equation.find('beta').text)
                    qc = float(equation.find('c').text)
                    break

        # Do the calculations
        Qr=c * (hg - offset)**beta
        Hr=qoffset+(q/qc)**(1/qbeta)
        Shift = float(format(Hr-hg,".3g"))
        Qdiff = float(format(((q-Qr)/Qr)*100,".3g"))

        return Shift, Qdiff


    def CalcTxtShiftQdiff(self, points, hg, q):
        hg1 = None
        hg2 = None
        qr1 = None
        qr2 = None
        qhg1 = None
        qhg2 = None
        qqr1 = None
        qqr2 = None
        for i, row in enumerate(points):

            hgpas = row[1]
            if hg < hgpas:
                hg1 = self.data[i-1][1]
                qr1 = self.data[i-1][0]
                hg2 = row[1]
                qr2 = row[0]
                break

        #calculate a and b for shift

        for j, row2 in enumerate(points):

            qpas = row[0]
            if q < qpas:
                qhg1 = self.data[i-1][1]
                qqr1 = self.data[i-1][0]
                qhg2 = row[1]
                qqr2 = row[0]
                break

        a = (qr2-qr1)/(hg2-hg1)
        b = qr2 - a*hg2

        q_a = (qqr2-qqr1)/(qhg2-qhg1)
        q_b = qqr2 - q_a*qhg2

        # Do calculations
        Qr=(a*hg)+ b
        Hr=(1/q_a* (q-q_b))
        Shift = float(format(Hr-hg,".3g"))
        Qdiff = float(format(((q-Qr)/Qr)*100,".3g"))

        return Shift, Qdiff


    def ParseHistCSVFile(self, filepath):
        if self.mode == "DEBUG":
            print "Parsing CSV Historical Data File"

        # Reset Historical Data
        self.histData = None
        self.delHist = None
        self.minList = []
        self.maxList = []
        self.gui.ClearAllHistRows()

        csvFile = open(filepath, "r")
        histData = csvFile.readlines()[1:]
        histData = [x.strip().split(',') for x in histData]

        listToDel = []

        for i, row in enumerate(histData):
            print "####################"
            print row
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


        self.OnRCUpdate()


    def CalculateShiftDisch(self, Hobserved, Qobserved):

        if self.mode == "DEBUG":
            print "Calculating Shift and Discharge"

        if self.extension is None:
            self.gui.CreateErrorDialog("Please use a valid Rating Curve File - it is an XML file best extracted from the ADET")
            return

        if Hobserved == "":
            #show error dialog
            self.gui.CreateErrorDialog("Observed Stage is empty. Please enter a value.")
            return
        elif Qobserved == "":
            #show error dialog
            self.gui.CreateErrorDialog("Observed Discharge is empty. Please enter a value.")
            return

        if self.extension == "xml":
            selectedCurveIndex = self.gui.GetSelectedCurveIndex()
            if selectedCurveIndex < 0:
                self.gui.CreateErrorDialog("Rating Curve file is invalid.")
                return

        # Reset shift/disch calculations
        self.shiftDiffDisch = None
        self.ResetPlotVars()


        # Store obsDisch, obsStage
        self.obsDisch = float(Qobserved)
        self.obsStage = float(Hobserved)

        if self.extension == "xml":
            self.CalculateXMLShiftDisch()
        elif self.extension == "txt":

            self.CalculateTXTShiftDisch()


    def CalculateXMLShiftDisch(self):
        selectedCurveIndex = self.gui.GetSelectedCurveIndex()
        RCType = self.data[selectedCurveIndex][0].get('type')

        self.curveNum = self.data[selectedCurveIndex][0].get("id")

        # points list
        points = self.data[selectedCurveIndex][2]

        # plotted rating points

        self.qrpa = [float(x.find('qr').text) for x in self.data[selectedCurveIndex][2]]

        self.hgpa = [float(x.find('hg').text) for x in self.data[selectedCurveIndex][2]]
        self.qrta = self.qrpa
        self.hgta = self.hgpa


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

        if self.obsStage < hg_low:
            if self.mode == "DEBUG":
                print "Observed Stage is below the minimum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #Have error dialog appear
            self.gui.CreateErrorDialog("Observed Stage is below the minimum rating point")
            return
        elif self.obsStage > hg_high:
            if self.mode == "DEBUG":
                print "Observed Stage is above the maximum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #have error dialog appear
            self.gui.CreateErrorDialog("Observed Stage is above the maximum rating point")
            return
        if self.obsDisch < q_low:
            if self.mode == "DEBUG":
                print "Observed Discharge is below the minimum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #Have error dialog appear
            self.gui.CreateErrorDialog("Observed Discharge is below the minimum rating point")
            return
        elif self.obsDisch > q_high:
            if self.mode == "DEBUG":
                print "Observed Discharge is above the maximum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #have error dialog appear
            self.gui.CreateErrorDialog("Observed Discharge is above the maximum rating point")
            return


        #-----------------------Calculations: Shift and Discharge Diff(%)Shift and Discharge Diff(%)-----------------------#
        print ">>>>>>> Rating Parameters based on the RC selected<<<<<<<<<<<<"
        #Calculations for Logarithmic Rating Curve Type.....
        if RCType == "Linear":
            self.CalculateLinearRC(points, selectedCurveIndex)

        #Calculations for Logarithmic Rating Curve Type.....
        elif RCType == "Logarithmic":
            self.CalculateLogRC(points, selectedCurveIndex)


    def CalculateLinearRC(self, points, selectedCurveIndex):
        # self.Shift, self.Qdiff = self.CalcLinShiftQdiff(points, self.obsStage, self.obsDisch)
        a = None
        b = None
        a2 = None
        b2 = None
        for i, hgpas in enumerate(points):
            hgpas = float(hgpas.find('hg').text)

            if self.obsStage < hgpas:
                equation = points[i].find('equation')
                if equation is not None:
                    a = float(equation.find('a').text)
                    b = float(equation.find('b').text)
                    break

        for i, qpas in enumerate(points):
            qpas = float(qpas.find('qr').text)

            if self.obsDisch < qpas:
                equation = points[i].find('equation')
                if equation is not None:
                    a2 = float(equation.find('a').text)
                    b2 = float(equation.find('b').text)
                    break

        # Do Calculations
        self.Qr=(a*self.obsStage)+ b
        self.Hr=(1/a2* (self.obsDisch-b2))
        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = float(format(((self.obsDisch-self.Qr)/self.Qr)*100,".3g"))

        # Set Text Fields in the gui
        self.gui.SetCalcShift(str(self.Shift))
        self.gui.SetRatedDisch(str(float(format(self.Qr, ".3g"))))
        self.gui.SetDischDiff(str(self.Qdiff))

        # Set values in Discharge Manager
        if self.disMeasManager is not None:
            self.disMeasManager.shiftCtrl = str(self.Shift)
            self.disMeasManager.diffCtrl = str(self.Qdiff)
            self.disMeasManager.curveCtrl = str(self.curveNum)


    def CalculateLogRC(self, points, selectedCurveIndex):
        c = None
        beta = None
        offset = None
        c2 = None
        beta2 = None
        offset2 = None
        for i, hgpas in enumerate(points):
            hgpas = float(hgpas.find('hg').text)

            if self.obsStage < hgpas:
                equation = points[i].find('equation')
                if equation is not None:
                    offset = float(points[i].find('offset').text)
                    beta = float(equation.find('beta').text)
                    c = float(equation.find('c').text)
                    break




        for i, qpas in enumerate(points):
            qpas = float(qpas.find('qr').text)

            if self.obsDisch < qpas:
                equation = points[i].find('equation')
                if equation is not None:
                    offset2 = float(points[i].find('offset').text)
                    beta2 = float(equation.find('beta').text)
                    c2 = float(equation.find('c').text)
                    break


        # Do the calculations
        self.Qr=c*(self.obsStage-offset)**beta
        self.Hr=offset2+(self.obsDisch/c2)**(1/beta2)
        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = float(format(((self.obsDisch-self.Qr)/self.Qr)*100,".3g"))


        # Set Text Fields in the gui
        self.gui.SetCalcShift(str(self.Shift))
        self.gui.SetRatedDisch(str(float(format(self.Qr, ".3g"))))
        self.gui.SetDischDiff(str(self.Qdiff))

        # Set values in Discharge Manager
        if self.disMeasManager is not None:
            self.disMeasManager.shiftCtrl = str(self.Shift)
            self.disMeasManager.diffCtrl = str(self.Qdiff)
            self.disMeasManager.curveCtrl = str(self.curveNum)



    def SetupCurveFromTxt(self):
        # In the table, it's discharge, stage
        # in other words, [x][0] is discharge, [x][1] is stage
        self.qrpa = [x[0] for x in self.data]
        self.hgpa = [x[1] for x in self.data]
        self.qrta = self.qrpa
        self.hgta = self.hgpa

    def CalculateTXTShiftDisch(self):


        # assumes that the first point is lowest, last point is highest
        # checks against high and low points first
        hg_low = float(self.data[0][1])
        hg_high = float(self.data[-1][1])
        q_low = float(self.data[0][0])
        q_high = float(self.data[-1][0])

        if self.obsStage < hg_low:
            if self.mode == "DEBUG":
                print "Observed Stage is below the minimum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #Have error dialog appear
            self.gui.CreateErrorDialog("Observed Stage is below the minimum rating point")
            return
        elif self.obsStage > hg_high:
            if self.mode == "DEBUG":
                print "Observed Stage is above the maximum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #have error dialog appear
            self.gui.CreateErrorDialog("Observed Stage is above the maximum rating point")
            return
        elif self.obsDisch < q_low:
            if self.mode == "DEBUG":
                print "Observed Discharge is below the minimum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #Have error dialog appear
            self.gui.CreateErrorDialog("Observed Discharge is below the minimum rating point")
            return
        elif self.obsDisch > q_high:
            if self.mode == "DEBUG":
                print "Observed Discharge is above the maximum rating point"
            self.gui.SetCalcShift("")
            self.gui.SetDischDiff("")

            #have error dialog appear
            self.gui.CreateErrorDialog("Observed Discharge is above the maximum rating point")
            return


        # Not above or below the RC
        hg1 = None
        hg2 = None
        qr1 = None
        qr2 = None
        qhg1 = None
        qhg2 = None
        qqr1 = None
        qqr2 = None
        for i, row in enumerate(self.data):
            hg = row[1]
            if self.obsStage < hg:
                hg1 = self.data[i-1][1]
                qr1 = self.data[i-1][0]
                hg2 = row[1]
                qr2 = row[0]
                break


        for i, row in enumerate(self.data):
            q = row[0]
            if self.obsDisch < q:
                qhg1 = self.data[i-1][1]
                qqr1 = self.data[i-1][0]
                qhg2 = row[1]
                qqr2 = row[0]
                break



        a = (qr2-qr1)/(hg2-hg1)
        b = qr2 - a*hg2


        qa = (qqr2-qqr1)/(qhg2-qhg1)
        qb = qqr2 - qa*qhg2


        # Do calculations
        self.Qr=(a*self.obsStage)+ b
        self.Hr=(1/qa* (self.obsDisch-qb))
        self.Shift = float(format(self.Hr-self.obsStage,".3g"))
        self.Qdiff = float(format(((self.obsDisch-self.Qr)/self.Qr)*100,".3g"))


        # Set Text Fields in the gui
        self.gui.SetCalcShift(str(self.Shift))
        self.gui.SetRatedDisch(str(float(format(self.Qr, ".3g"))))
        self.gui.SetDischDiff(str(self.Qdiff))

        if self.disMeasManager is not None:
            self.disMeasManager.shiftCtrl = str(self.Shift)
            self.disMeasManager.diffCtrl = str(self.Qdiff)


    def PlotData(self):
        if self.mode == "DEBUG":
            print "Plotting Data"

        # if self.extension is None:
        #     self.gui.CreateErrorDialog("Please use a valid Rating Curve File")
            return None
        # if self.obsStage == "" or self.obsStage is None:
        #     #show error dialog
        #     self.gui.CreateErrorDialog("Observed Stage is empty. Please enter a value.")
        #     return None
        # elif self.obsDisch == "" or self.obsDisch is None:
        #     #show error dialog
        #     self.gui.CreateErrorDialog("Observed Discharge is empty. Please enter a value.")
        #     return None

        # print self.qrpa
        # print self.hgpa
        if (self.obsStage != "" and self.obsStage is not None) and (self.obsDisch != "" and self.obsDisch is not None):
            self.qrta = self.qrpa
            self.hgta = self.hgpa



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
        # self.qrpa = None
        self.hrpa = None
        self.Hr = None
        self.Qr = None


    def FetchStageDischarge(self):
        if self.mode == "DEBUG":
            print "Getting Stage and Discharge"

        if self.disMeasManager is None:
            return

        obsStage = self.disMeasManager.mghCtrl
        obsDisch = self.disMeasManager.dischCtrl


        self.gui.SetObsStage(obsStage)
        self.gui.SetObsDisch(obsDisch)


def main():
    app = wx.App()

    frame = RatingCurveViewerToolFrame("DEBUG", os.getcwd() + "\\RC docs", None, None, wx.LANGUAGE_ENGLISH, None, size=(770, 578))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
