from __future__ import division
import requests
import json
import datetime
import os
import csv
import pickle

location=os.path.dirname(os.path.realpath(__file__))
print location

# get the month and year of the *previous* month
now=datetime.date.today()
currentmonth=monthdelta(now,-1)
one_month_ago=monthdelta(currentmonth,-1)
two_month_ago=monthdelta(currentmonth,-2)
three_month_ago=monthdelta(currentmonth,-3)
three_month_future=monthdelta(currentmonth,3)
year=currentmonth.year

month=currentmonth.strftime("%B")
datestring=month+', '+str(year)
date_start_string=fourmonths+', '+str(startyear)
date_end_string=threemonthsout+', '+str(endyear)
two_string=monthdelta(currentmonth,-1).strftime("%B")+', '+monthdelta(currentmonth,-1).strftime("%Y")
three_string=monthdelta(currentmonth,-2).strftime("%B")+', '+monthdelta(currentmonth,-1).strftime("%Y")
four_string=monthdelta(currentmonth,-3).strftime("%B")+', '+monthdelta(currentmonth,-1).strftime("%Y")

# headers
headers = {'Content-type': 'application/json'}

# MAIN FUNCTIONS
# json_data=data_scrape()
# comparison=compare(json_data)
# if comparison!=json_data:
#	graph1(json_data,comparison)
#	graph2(json_data,comparison)
#	graph3(json_data,comparison)
#	graph4(json_data,comparison)
#	graph5(json_data,comparison)
#	graph6(json_data,comparison)
#	graph7(json_data,comparison)
#	graph8(json_data,comparison)

# thank god someone else wrote this: http://stackoverflow.com/a/3425124
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

# function to update all data series
def data_scrape():
	# get all series data in one go
	series=['LNS12300060','CES0500000001','CES9000000001','LNS14000003','LNS14000006','LNS14000009','LNS14000000','LNS13327709','LNS12032194','LNS12600000','CES0500000008','CES2000000001','CES3000000001','CES4200000001','CES6561000001','CES6562000001','CUUR0000SA0']
	data = json.dumps({"seriesid": series,"startyear":year-1, "endyear":year})
	p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
	json_data = json.loads(p.text)

	return json_data

def compare(json_data):
	# compare the json_data object to existing object
	temp=pickle.load(open(location+'json_data.p','wb'))

	if temp!=json_data:
		pickle.dump(json_data,open(location+'json_data.p','wb'))

	return temp

def graph1(json_data,comparison):
	# graph 1 - load existing data:
	with open(location+'jobs-g1.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]
	temp_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='LNS12300060'][0]

	if temp!=temp_compare:
		three_months=[]

		for time_period in temp['data']:
			if time_period['periodName']==month:
				data.append([time_period['value'],datestring])
				three_months.append(float(time_period['value']))

		for row in data:
			if row[1]==three_string or row[1]==two_string:
				three_months.append(float(row[0]))

		average=sum(three_months)/len(three_months)
		print 'average for graph 1: ',average

		for i,row in enumerate(data):
			if row[5]=='3-month average':
				data[i][2]=average
				data[i][3]=date_start_string
				date[i][4]=date_end_string

		with open(location+'jobs-g1.csv','w') as cfile:
			writer=csv.writer(cfile)
			for row in data:
				writer.writerow(row)

def graph2(json_data):
	# graph 2 - load existing data:
	with open(location+'jobs-g2.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]

	elapsed=8+((2016-now.year)*12)+(1/12)*(now.month-1)

	for time_period in temp['data']:
		if time_period['periodName']==month:
			epop=time_period['value']
			data.append(['December 2007-Present',epop,elapsed,float(epop)-79.7])

	with open(location+'jobs-g1.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)

def graph3(json_data):
	# graph 3 - load existing data:
	with open(location+'jobs-g3.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp_private=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000001'][0]
	temp_public=[series for series in json_data['Results']['series'] if series['seriesID']=='CES9000000001'][0]

	three_months_private=[]
	three_months_public=[]

	start_emp_private=115778
	start_emp_public=22219

	for time_period in temp_private['data']:
		if time_period['periodName']==month:
			private_emp=time_period['value']
			data.append([datestring,private_emp,100*(private_emp/start_emp_private,'Private Sector')])
			three_months_private.append(float(time_period['value']))

	for time_period in temp_public['data']:
		if time_period['periodName']==month:
			public_emp=time_period['value']
			data.append([datestring,public_emp,100*(public_emp/start_emp_public,'Public Sector')])
			three_months_public.append(float(time_period['value']))

	for row in data:
		if row[1]==three_string or row[1]==two_string:
			if row[3]=='Public Sector':
				three_months_public.append(float(row[2]))
			if row[3]=='Private Sector':
				three_months_private.append(float(row[2]))

	average=sum(three_months_public)/len(three_months_public)
	print 'average for public: ',average

	average=sum(three_months_private)/len(three_months_private)
	print 'average for private: ',average


{u'status': u'REQUEST_SUCCEEDED', u'message': [], u'Results': {u'series': [{u'seriesID': u'CES6561000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'3529.6', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'3513.7', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'3505.3', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'3484.4', u'year': u'2016'}]}, {u'seriesID': u'CES0500000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'121838', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'121667', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'121483', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'121261', u'year': u'2016'}]}, {u'seriesID': u'LNS14000000', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'5.0', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'5.0', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'4.9', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'4.9', u'year': u'2016'}]}, {u'seriesID': u'LNS12300060', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'77.7', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'78.0', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'77.8', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'77.7', u'year': u'2016'}]}, {u'seriesID': u'LNS14000003', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'4.3', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'4.3', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'4.3', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'4.3', u'year': u'2016'}]}, {u'seriesID': u'LNS14000006', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'8.8', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'9.0', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'8.8', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'8.8', u'year': u'2016'}]}, {u'seriesID': u'CES0500000008', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'21.45', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'21.40', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'21.35', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'21.33', u'year': u'2016'}]}, {u'seriesID': u'CES2000000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'6670', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'6669', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'6628', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'6615', u'year': u'2016'}]}, {u'seriesID': u'CES9000000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'22077', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'22088', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'22064', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'22053', u'year': u'2016'}]}, {u'seriesID': u'LNS14000009', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'6.1', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'5.6', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'5.4', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'5.9', u'year': u'2016'}]}, {u'seriesID': u'LNS12600000', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'27797', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'27818', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'27853', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'27364', u'year': u'2016'}]}, {u'seriesID': u'CES4200000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'15915.2', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'15918.3', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'15879.3', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'15827.3', u'year': u'2016'}]}, {u'seriesID': u'LNS13327709', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'9.7', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'9.8', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'9.7', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'9.9', u'year': u'2016'}]}, {u'seriesID': u'LNS12032194', u'data': [{u'footnotes': [{}], u'periodName': u'April', u'period': u'M04', u'value': u'5962', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'March', u'period': u'M03', u'value': u'6123', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'5988', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'5988', u'year': u'2016'}]}, {u'seriesID': u'CES6562000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'19048.3', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'19010.1', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'18976.1', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'18919.4', u'year': u'2016'}]}, {u'seriesID': u'CES3000000001', u'data': [{u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'April', u'period': u'M04', u'value': u'12297', u'year': u'2016'}, {u'footnotes': [{u'text': u'preliminary', u'code': u'P'}], u'periodName': u'March', u'period': u'M03', u'value': u'12293', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'February', u'period': u'M02', u'value': u'12322', u'year': u'2016'}, {u'footnotes': [{}], u'periodName': u'January', u'period': u'M01', u'value': u'12338', u'year': u'2016'}]}]}, u'responseTime': 185}