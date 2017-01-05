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
	series=['CES2000000003','CES3000000003','CES5500000003','CES6000000003','CES6500000003','CEU7000000003','LNS13008397','LNS13025701','LNS13008517','LNS13023570','LNS13023558','LNS13023706','LNS13023622','LNS14027662','LNS14027660','LNS14027659','LNS14027689','LNS12327659','LNS12327660','LNS12327689','LNS12327662','LNS11000000','LNS12032197','LNS12032200','LNS12300060','CES0500000001','CES9000000001','LNS14000003','LNS14000006','LNS14000009','LNS14000000','LNS13327709','LNS12032194','LNS12600000','CES0500000008','CES2000000001','CES3000000001','CES4200000001','CES6561000001','CES6562000001','CUUR0000SA0','CES7000000001']
	data = json.dumps({"seriesid": series,"startyear":2000, "endyear":year, "registrationKey":key})
	p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
	json_data = json.loads(p.text)
	return json_data

def compare(json_data):
	# compare the json_data object to existing object
	temp=pickle.load(open(location+'json_data.p','r'))		
	return temp

def graph1(json_data):
	# graph 1. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]['data']
	data=[['EPOP','date','average','date_start','date_end','type']]

	# build all rows
	tempavg=sum([float(temp[0]['value']),float(temp[1]['value']),float(temp[2]['value'])])/3
	for item in temp:
		if(int(item['year'])>1999):
			data.append([item['value'],item['periodName']+', '+item['year']])

	data.append(['','',three_month_ago.strftime("%B")+', '+str(three_month_ago.year),three_month_future.strftime("%B")+', '+str(three_month_future.year),tempavg,'3-month average'])

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
		if time_period['periodName']==month and int(time_period['year'])==year:
			epop=float(time_period['value'])
			data.append(['December 2007-Present',epop,elapsed,float(epop)-79.7])

	with open(location+'jobs-g2.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph3(json_data):
	# graph 3. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp_private=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000001'][0]['data']
	temp_public=[series for series in json_data['Results']['series'] if series['seriesID']=='CES9000000001'][0]['data']
	data=[['date','employment','indexed','type']]

	start_emp_private=115778
	start_emp_public=22219

	# build all rows
	for item in temp_private:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],item['value'],100*float(item['value'])/start_emp_private,'Private Sector'])

	for item in temp_public:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],item['value'],100*float(item['value'])/start_emp_public,'Public Sector'])

	with open(location+'jobs-g3.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph4(json_data):
	# graph 4. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp_white=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14000003'][0]['data']
	temp_black=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14000006'][0]['data']
	temp_hispanic=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14000009'][0]['data']
	data=[['type','date','unemployment','startx','endx','3-month average']]

	# build all rows
	white_average=sum([float(temp_white[0]['value']),float(temp_white[1]['value']),float(temp_white[2]['value'])])/3
	for item in temp_white:
		if(int(item['year'])>1999):
			data.append(['white',item['periodName']+', '+item['year'],float(item['value'])])

	black_average=sum([float(temp_black[0]['value']),float(temp_black[1]['value']),float(temp_black[2]['value'])])/3
	for item in temp_black:
		if(int(item['year'])>1999):
			data.append(['black',item['periodName']+', '+item['year'],float(item['value'])])

	hispanic_average=sum([float(temp_hispanic[0]['value']),float(temp_hispanic[1]['value']),float(temp_hispanic[2]['value'])])/3
	for item in temp_hispanic:
		if(int(item['year'])>1999):
			data.append(['hispanic',item['periodName']+', '+item['year'],float(item['value'])])

	data.append(['white','','',three_month_ago.strftime("%B")+', '+str(three_month_ago.year),three_month_future.strftime("%B")+', '+str(three_month_future.year),white_average])
	data.append(['black','','',three_month_ago.strftime("%B")+', '+str(three_month_ago.year),three_month_future.strftime("%B")+', '+str(three_month_future.year),black_average])
	data.append(['hispanic','','',three_month_ago.strftime("%B")+', '+str(three_month_ago.year),three_month_future.strftime("%B")+', '+str(three_month_future.year),hispanic_average])

	with open(location+'jobs-g4.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)	


def graph5(json_data):
	# graph 5. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp_u3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14000000'][0]['data']
	temp_u6=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13327709'][0]['data']
	data=[['date','u','type']]

	# build all rows
	for item in temp_u3:
		if(int(item['year'])>1999):
			data.append([item['periodName']+', '+item['year'],item['value'],'u3'])

	for item in temp_u6:
		if(int(item['year'])>1999):
			data.append([item['periodName']+', '+item['year'],item['value'],'u6'])

	with open(location+'jobs-g5.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)	


def graph6(json_data):
	# graph 6. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp_voluntary=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12032200'][0]['data']
	temp_involuntary=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12032197'][0]['data']
	data=[['DATE','type','indexed']]

	# percentage change indexed to December of 2007
	voluntary_base=float([entry['value'] for entry in temp_voluntary if entry['year']=='2007' and entry['period']=='M12'][0])
	involuntary_base=float([entry['value'] for entry in temp_involuntary if entry['year']=='2007' and entry['period']=='M12'][0])

	# now build all rows
	for item in temp_voluntary:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],'voluntary',100*(float(item['value'])-voluntary_base)/voluntary_base])

	for item in temp_involuntary:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],'involuntary',100*(float(item['value'])-involuntary_base)/involuntary_base])

	with open(location+'jobs-g6.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)	


def graph7(json_data):
	# graph 7. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp_inflation=[series for series in json_data['Results']['series'] if series['seriesID']=='CUUR0000SA0'][0]['data']
	temp_earnings=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000008'][0]['data']
	data=[['date','value','type']]

	# build all rows
	for item in temp_earnings:
		if(int(item['year'])>2005):
			yearago=[float(new['value']) for new in temp_earnings if int(new['year'])==int(item['year'])-1 and new['period']==item['period']][0]
			data.append([item['periodName']+', '+item['year'],100*(float(item['value'])-yearago)/yearago,'earnings'])

	for item in temp_inflation:
		if(int(item['year'])>2005):
			yearago=[float(new['value']) for new in temp_inflation if int(new['year'])==int(item['year'])-1 and new['period']==item['period']][0]
			data.append([item['periodName']+', '+item['year'],100*(float(item['value'])-yearago)/yearago,'inflation'])

	with open(location+'jobs-g7.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph8(json_data):
	# graph 3. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
	# a master file, just overwrite the file every time, guarantees you always have as much data as possible and no re-writing the same thing over
	# and over.
	temp_construction=[series for series in json_data['Results']['series'] if series['seriesID']=='CES2000000001'][0]['data']
	temp_manufacturing=[series for series in json_data['Results']['series'] if series['seriesID']=='CES3000000001'][0]['data']
	temp_retail=[series for series in json_data['Results']['series'] if series['seriesID']=='CES4200000001'][0]['data']
	temp_ed=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6561000001'][0]['data']
	temp_health=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6562000001'][0]['data']
	temp_leisure=[series for series in json_data['Results']['series'] if series['seriesID']=='CES7000000001'][0]['data']

	data=[['date','index','type','raw_emp']]

	con_average=7627.3
	man_average=13877.8
	ret_average=15516.3
	edu_average=2941.7
	hea_average=15734.3
	lei_average=13427.9

	# build all rows
	for item in temp_construction:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],100*float(item['value'])/con_average,'Construction',item['value']])

	for item in temp_manufacturing:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],100*float(item['value'])/man_average,'Manufacturing',item['value']])

	for item in temp_retail:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],100*float(item['value'])/ret_average,'Retail',item['value']])

	for item in temp_ed:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],100*float(item['value'])/edu_average,'Educational services',item['value']])

	for item in temp_health:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],100*float(item['value'])/hea_average,'Health care and social assistance',item['value']])

	for item in temp_leisure:
		if(int(item['year'])>2006):
			data.append([item['periodName']+', '+item['year'],100*float(item['value'])/lei_average,'Leisure and hospitality',item['value']])

	with open(location+'jobs-g8.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph9(json_data):
	# college grads - LNS14027662
	# high school grads - LNS14027660
	# < high school - LNS14027659
	# some college - LNS14027689

	temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027659'][0]['data']
	temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027660'][0]['data']
	temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027689'][0]['data']
	temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027662'][0]['data']
	data=[['type','date','epop']]

	# build all rows
	for item in temp_1:
		if(int(item['year'])>1999):
			data.append(['<High school',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_2:
		if(int(item['year'])>1999):
			data.append(['High school graduate',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_3:
		if(int(item['year'])>1999):
			data.append(['Some college',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_4:
		if(int(item['year'])>1999):
			data.append(["Bachelor's degree or greater",item['periodName']+', '+item['year'],float(item['value'])])

	with open(location+'jobs-g9.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph10(json_data):
	# reasons for unemployment
	# new entrants: LNS13023570
	# reentrants: LNS13023558
	# job leavers: LNS13023706
	# job losers: LNS13023622

	temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023570'][0]['data']
	temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023558'][0]['data']
	temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023706'][0]['data']
	temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023622'][0]['data']
	data=[['type','date','epop']]

	# build all rows
	for item in temp_1:
		if(int(item['year'])>1999):
			data.append(['New entrants to labor force',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_2:
		if(int(item['year'])>1999):
			data.append(['Re-entering labor force',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_3:
		if(int(item['year'])>1999):
			data.append(['Leaving job',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_4:
		if(int(item['year'])>1999):
			data.append(["Lost job",item['periodName']+', '+item['year'],float(item['value'])])

	with open(location+'jobs-g10.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph11(json_data):
	# duration of unemployment
	# unemployed <5 weeks: LNS13008397
	# 5-14 weeks: LNS13025701
	# 15+: LNS13008517

	temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008397'][0]['data']
	temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13025701'][0]['data']
	temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008517'][0]['data']
	data=[['type','date','epop']]

	# build all rows
	for item in temp_1:
		if(int(item['year'])>1999):
			data.append(['Fewer than 5 weeks',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_2:
		if(int(item['year'])>1999):
			data.append(['5-14 weeks',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_3:
		if(int(item['year'])>1999):
			data.append(['More than 15 weeks',item['periodName']+', '+item['year'],float(item['value'])])

	with open(location+'jobs-g11.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph12(json_data):
	# earnings by sector
	# construction: CES2000000003
	# manufacturing: CES3000000003
	# financial: CES5500000003
	# professional: CES6000000003
	# education/health: CES6500000003
	# leisure: CEU7000000003

	temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='CES2000000003'][0]['data']
	temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='CES3000000003'][0]['data']
	temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='CES5500000003'][0]['data']
	temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6000000003'][0]['data']
	temp_5=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6500000003'][0]['data']
	temp_6=[series for series in json_data['Results']['series'] if series['seriesID']=='CEU7000000003'][0]['data']
	data=[['type','date','epop']]

	# build all rows
	for item in temp_1:
		if(int(item['year'])>1999):
			data.append(['Construction',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_2:
		if(int(item['year'])>1999):
			data.append(['Manufacturing',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_3:
		if(int(item['year'])>1999):
			data.append(['Financial',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_4:
		if(int(item['year'])>1999):
			data.append(['Professional',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_5:
		if(int(item['year'])>1999):
			data.append(['Education/Health',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_6:
		if(int(item['year'])>1999):
			data.append(['Leisure and Hospitality',item['periodName']+', '+item['year'],float(item['value'])])

	with open(location+'jobs-g12.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph13(json_data):
	# graph 13 is epop by educational attainment.
	# < high school, age 25+: LNS12327659
	# high school graduates, age 25+: LNS12327660
	# Some college or associate degree, age 25+: LNS12327689
	# bachelor's degree, age 25+: LNS12327662

	temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327659'][0]['data']
	temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327660'][0]['data']
	temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327689'][0]['data']
	temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327662'][0]['data']
	data=[['type','date','epop']]

	# build all rows
	for item in temp_1:
		if(int(item['year'])>1999):
			data.append(['Less than high school',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_2:
		if(int(item['year'])>1999):
			data.append(['High school graduate',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_3:
		if(int(item['year'])>1999):
			data.append(['Some college',item['periodName']+', '+item['year'],float(item['value'])])

	for item in temp_4:
		if(int(item['year'])>1999):
			data.append(["Bachelor's degree or greater",item['periodName']+', '+item['year'],float(item['value'])])

	with open(location+'jobs-g13.csv','w') as cfile:
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
graph8(json_data)
print 'graph 8 done'
graph9(json_data)
print 'graph 9 done'
graph10(json_data)
print 'graph 10 done'
graph11(json_data)
print 'graph 11 done'
graph12(json_data)
print 'graph 12 done'
graph13(json_data)
print 'graph 13 done'

pickle.dump(json_data,open(location+'json_data.p','wb'))











