from suds.client import Client



Server = "http://hwp-app-stage1.to.on.ec.gc.ca"

Login = "wenbin.zhang"
Password = "wenbin1"



aq = Client(Server + '/aquarius/AQAcquisitionService.svc?wsdl')
aq.set_options(headers={'AQAuthToken':aq.service.GetAuthToken(Login, Password)})

authcode = aq.service.GetAuthToken(Login, Password)

# print(authcode)


locid = aq.service.GetLocationId("02KF015")

locinf = aq.service.GetLocation(locid)


offset = str(locinf.UtcOffset).split('.')

offset = offset[0] + ':00' if len(offset[0]) > 2 else offset[0][:1] + '0' + offset[0][1:]  + ':00'
start = "2016-07-19T00:00:00.000-05:00"



# print locinf.UtcOffset
table = []

fv=aq.service.GetFieldVisitsByLocationChangedSince(locid, start)


    
for i in range(len(fv[0])):
    if fv[0][i].Measurements is not None:
        if fv[0][i].Measurements[0] is not None:
            for mea in fv[0][i].Measurements[0]:
                if 'discharge' in mea.MeasurementType.lower():
                    line = []
                    hg = None
                    qr = None
                    # print mea.Results
                    if mea.Results is not None:
                        # print mea.Results

                        for fvr in mea.Results.FieldVisitResult:
                            if fvr.ParameterID == 'HG':
            
                                if fvr.ResultType == 1 or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                # if fvr.ResultType == 1:

                                    hg = fvr.CorrectedResult
                                    startTime = fvr.StartTime
                                    if startTime != None:
                                        startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")


                            elif fvr.ParameterID == 'QR':
            
                                if fvr.ResultType == 1  or fvr.ResultType == 2147483647 or fvr.ResultType == None:
                                # if fvr.ResultType == 1 or fvr.ResultType == 2147483647:

                                    qr = fvr.CorrectedResult
                                    startTime = fvr.StartTime
                                    if startTime != None:
                                        startTimeDatetime = datetime.datetime.strptime(str(startTime)[:19], "%Y-%m-%d %H:%M:%S")

                    hg = hg if hg is not None else ''
                    qr = qr if qr is not None else ''

                    if hg != '' and qr != '':
                        if endDatetime > startTimeDatetime:
                            print fvr
                            print "========================"
                            print startTime
                            year = startTime.year
                            month = startTime.month
                            day =  startTime.day
                            newDate = wx.DateTime.FromDMY(day, month-1, year)


                            # outputfile.write(mea.MeasurementTime.strftime('%Y-%m-%d %H:%M:%S [UTC-05:00]') + ',')
                            # outputfile.write(str(qr) + ',') 
                            # outputfile.write(str(hg) + '\n') 