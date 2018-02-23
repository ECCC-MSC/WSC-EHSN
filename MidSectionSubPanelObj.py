# All works in this code have been curated by ECCC and licensed under the GNU General Public License v3.0. 
# Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

class SubPanelObj():
    def __init__(self, panelNum="", time="", panelId=-1, panelType=-1, index=-1, distance="", width="", depth="", \
        area="", discharge="", corrMeanVelocity="", flow=""):

        self.panelNum = panelNum
        self.distance = distance
        self.width = width
        self.depth = depth
        # self.bottomIce = bottomIce
        # self.depthUnderIce = depthUnderIce
        # self.obervationDepth = obervationDepth
        # self.revolutions = revolutions
        self.time = time
        self.panelId = panelId
        self.panelType = panelType
        self.index = index
        self.corrMeanVelocity = corrMeanVelocity


        # self.velocityPoint = velocityPoint
        self.area = area
        self.discharge = discharge
        self.flow = flow
        # self.flow = flow

    def SetPanelId(self, num):
        self.panelId = num

    def ToString(self):
        print "===============Print the object============="
        print "panelId: ", self.panelId
        print "panelNum:", self.panelNum
        print "distance:", self.distance
        print "width:", self.width
        print "depth:", self.depth
        print "panelType:", self.panelType
        print "index:", self.index
        print "corrMeanVelocity:", self.corrMeanVelocity
        print "============================================="




class PanelObj(SubPanelObj):
    def __init__(self, currentMeter="", slop="", intercept="",  slop2="", intercept2="", panelCondition="", openDepthRead="", \
                    offset="", wldl="", dryAngle="", distWaterSurface="", dryCorrection="", wetCorrection="", \
                    openEffectiveDepth="", iceDepthRead="", iceAssembly="", aboveFoot="", belowFoot="", distAboveWeight="", \
                    wsBottomIce="", wsBottomSlush="", iceEffectiveDepth="", velocityMethod="", obliqueCorrection="", \
                    velocityCorrFactor="", reverseFlow="", depths=[], depthObs=[], revs=[], revTimes=[], pointVels=[], \
                    meanVelocity="", end=False, start=False, slopBtn1="", weight="", adjusted="", \
                    slush="", thickness="", sequence=-1, iceThickness="", iceThicknessAdjusted="", \
                    *args, **kwargs):
        SubPanelObj.__init__(self, *args, **kwargs)
        self.panelType = 1
        self.currentMeter = currentMeter
        self.slopBtn1 = slopBtn1
        self.slop = slop
        self.intercept = intercept
        self.slop2 = slop2
        self.intercept2 = intercept2
        # self.distance = distance
        self.panelCondition = panelCondition
        self.openDepthRead = openDepthRead
        self.weight = weight
        self.offset = offset
        self.wldl = wldl
        self.dryAngle = dryAngle
        self.distWaterSurface = distWaterSurface
        self.dryCorrection = dryCorrection
        self.wetCorrection = wetCorrection
        self.openEffectiveDepth = openEffectiveDepth
        self.iceDepthRead = iceDepthRead
        self.iceAssembly = iceAssembly
        self.aboveFoot = aboveFoot
        self.belowFoot = belowFoot
        self.distAboveWeight = distAboveWeight
        self.wsBottomIce = wsBottomIce
        self.adjusted = adjusted
        self.slush = slush
        self.wsBottomSlush = wsBottomSlush
        self.thickness = thickness
        self.iceEffectiveDepth = iceEffectiveDepth
        self.velocityMethod = velocityMethod
        self.obliqueCorrection = obliqueCorrection
        self.velocityCorrFactor = velocityCorrFactor
        self.reverseFlow = reverseFlow

        self.depths = depths
        self.depthObs = depthObs
        self.revs = revs
        self.revTimes = revTimes
        self.pointVels = pointVels

        self.iceThickness = iceThickness
        self.iceThicknessAdjusted = iceThicknessAdjusted

        self.meanVelocity = meanVelocity
        # self.end = end
        # self.start = start
        # self.sequence = sequence


class EdgeObj(SubPanelObj):
    def __init__(self, edgeType="", leftOrRight="", startOrEnd="", depth="", depthAdjacent="",\
        velocityAdjacent="", *args, **kwargs):
        # super(EdgeObj, self).__init__(*args, **kwargs)
        SubPanelObj.__init__(self, *args, **kwargs)
        self.panelType = 0
        self.edgeType = edgeType
        self.leftOrRight = leftOrRight
        # self.distanceFromPoint = distanceFromPoint
        self.startOrEnd = startOrEnd
        # self.estimatedVel = estimatedVel
        self.depth = depth
        self.depthAdjacent = depthAdjacent
        self.velocityAdjacent = velocityAdjacent



# class PierObj(SubPanelObj):
#     def __init__(self, start="", end="", *args, **kwargs):
#         # super(PierObj, self).__init__(*args, **kwargs)
#         SubPanelObj.__init__(self, *args, **kwargs)
#         self.start = start
#         self.end = end





# obj = SubPanelObj(panelNum="", time="")
# obj = SubPanelObj()
# obj = PanelObj(panelNum=123, distance=444)
# print obj.panelNum
# print obj.distance
