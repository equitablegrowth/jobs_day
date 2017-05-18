from __future__ import division
import requests
import json
import datetime
import os
import csv
import pickle

# thank god someone else wrote this: http://stackoverflow.com/a/3425124
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def data_scrape():
	# get all series data in one go
	series=['JTS00000000QUR','JTS00000000JOL','JTS00000000HIL','LNS13000000','LNS14000000','LNS12300060','JTS00000000JOR','LNS13008636','LNS11000000','LNS13008876','LNS13008756','LNS13008396']
	data = json.dumps({"seriesid": series,"startyear":2001, "endyear":year, "registrationKey":key})
	p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
	json_data = json.loads(p.text)
	return json_data

def graph1(json_data):
	# Job openings
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000QUR'][0]['data']
	data=[['quits rate','date']]
	# build all rows
	for item in temp:
		if(int(item['year'])>2000):
			data.append([item['value'],item['periodName']+', '+item['year']])
	with open(location+'jolts-g1.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)	

def graph2(json_data):
	# hires/openings
	temp1=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000JOL'][0]['data']
	temp2=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000HIL'][0]['data']
	data=[['vacancy yield','date']]
	# build all rows
	for i,item in enumerate(temp1):

		if(int(item['year'])>2000):
			try:
				temp2a=[item2 for item2 in temp2 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				data.append([float(temp2a['value'])/float(item['value']),item['periodName']+', '+item['year']])
			except:
				pass
	with open(location+'jolts-g2.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)	

def graph3(json_data):
	# hires/openings
	temp1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13000000'][0]['data']
	temp2=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000JOL'][0]['data']
	data=[['unemployed per opening','date']]
	# build all rows
	for i,item in enumerate(temp2):
		if(int(item['year'])>2000):
			try:
				temp1a=[item2 for item2 in temp1 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				data.append([float(temp1a['value'])/float(item['value']),item['periodName']+', '+item['year']])
			except:
				pass
	with open(location+'jolts-g3.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)

def graph4(json_data):
	# beveridge curve
	temp1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14000000'][0]['data']
	temp2=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000JOR'][0]['data']
	data=[['unemployment rate','job openings','date','datestring']]
	# build all rows
	for i,item in enumerate(temp2):
		if(int(item['year'])>2000):
			try:
				temp1a=[item2 for item2 in temp1 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				data.append([float(temp1a['value']),float(item['value']),item['periodName']+', '+item['year'],item['periodName']+' '+item['year']])
			except:
				pass
	with open(location+'jolts-g4.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)

def graph5(json_data):
	# disaggregated beveridge curve
	temp1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008636'][0]['data']
	temp2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS11000000'][0]['data']
	temp3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008876'][0]['data']
	temp4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008756'][0]['data']
	temp5=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008396'][0]['data']
	temp6=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000JOR'][0]['data']
	data=[['job opening rate','unemployment rate','type','date','datestring']]
	# build all rows
	for i,item in enumerate(temp6):
		if(int(item['year'])>2000):
			try:
				temp1a=[item2 for item2 in temp1 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				temp2a=[item2 for item2 in temp2 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				temp3a=[item2 for item2 in temp3 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				temp4a=[item2 for item2 in temp4 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				temp5a=[item2 for item2 in temp5 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				unemprate27over=100*float(temp1a['value'])/float(temp2a['value'])
				unemprate27under=100*(float(temp3a['value'])+float(temp4a['value'])+float(temp5a['value']))/float(temp2a['value'])
				data.append([float(item['value']),unemprate27over,'Unemployed for 27 weeks or longer',item['periodName']+', '+item['year'],item['periodName']+' '+item['year']])
				data.append([float(item['value']),unemprate27under,'Unemployed for less than 27 weeks',item['periodName']+', '+item['year'],item['periodName']+' '+item['year']])
			except:
				pass
	with open(location+'jolts-g5.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)

def graph6(json_data):
	# quits vs unemployment rate
	temp1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14000000'][0]['data']
	temp2=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000QUR'][0]['data']
	data=[['unemployment rate','quits','date','datestring']]
	# build all rows
	for i,item in enumerate(temp2):
		if(int(item['year'])>2000):
			try:
				temp1a=[item2 for item2 in temp1 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				data.append([float(temp1[i]['value']),float(temp2a['value']),item['periodName']+', '+item['year'],item['periodName']+' '+item['year']])
			except:
				pass
	with open(location+'jolts-g6.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)

def graph7(json_data):
	# quits vs unemployment rate
	temp1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]['data']
	temp2=[series for series in json_data['Results']['series'] if series['seriesID']=='JTS00000000QUR'][0]['data']
	data=[['epop','quits','date','datestring']]
	# build all rows
	for i,item in enumerate(temp2):
		if(int(item['year'])>2000):
			try:
				temp1a=[item2 for item2 in temp1 if item2['periodName']==item['periodName'] and item2['year']==item['year']][0]
				data.append([float(temp1a['value']),float(item['value']),item['periodName']+', '+item['year'],item['periodName']+' '+item['year']])
			except:
				pass
	with open(location+'jolts-g7.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


location=os.path.dirname(os.path.realpath(__file__))+'/'
# location='/home/eqgrowth/webapps/jobsday/data/'
print location

# get API key
key=open(location+'key.txt','r').read()

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
date_start_string=three_month_ago.strftime("%B")+', '+str(three_month_ago.year)
date_end_string=three_month_future.strftime("%B")+', '+str(three_month_future.year)
one_string=monthdelta(currentmonth,-1).strftime("%B")+', '+str(one_month_ago.year)
two_string=monthdelta(currentmonth,-2).strftime("%B")+', '+str(two_month_ago.year)
three_string=monthdelta(currentmonth,-3).strftime("%B")+', '+str(three_month_ago.year)

# headers
headers = {'Content-type': 'application/json'}

# MAIN FUNCTIONS
json_data=data_scrape()
print 'got data'

graph1(json_data)
print 'graph 1 done'
graph2(json_data)
print 'graph 2 done'
graph3(json_data)
print 'graph 3 done'
graph4(json_data)
print 'graph 4 done'
graph5(json_data)
print 'graph 5 done'
graph6(json_data)
print 'graph 6 done'
graph7(json_data)
print 'graph 7 done'










