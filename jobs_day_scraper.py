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
	series=['LNS11000000','LNS12032197','LNS12032200','LNS12300060','CES0500000001','CES9000000001','LNS14000003','LNS14000006','LNS14000009','LNS14000000','LNS13327709','LNS12032194','LNS12600000','CES0500000008','CES2000000001','CES3000000001','CES4200000001','CES6561000001','CES6562000001','CUUR0000SA0','CES7000000001']
	data = json.dumps({"seriesid": series,"startyear":2000, "endyear":year, "registrationKey":key})
	p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
	json_data = json.loads(p.text)
	return json_data

def compare(json_data):
	# compare the json_data object to existing object
	temp=pickle.load(open(location+'json_data.p','r'))		
	return temp

def graph1(json_data,comparison):
	# graph 1 - load existing data:
	with open(location+'jobs-g1.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]
	temp_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='LNS12300060'][0]

	if temp!=temp_compare:
		print 'graph 1 changed'
		three_months=[]

		for time_period in temp['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				if datestring not in [row[1] for row in data]:
					data.append([float(time_period['value']),datestring])
				three_months.append(float(time_period['value']))

		for row in data:
			if row[1]==one_string or row[1]==two_string:
				three_months.append(float(row[0]))

		average=sum(three_months)/len(three_months)

		for i,row in enumerate(data):
			try:
				if row[5]=='3-month average':
					data[i][2]=average
					data[i][3]=date_start_string
					data[i][4]=date_end_string
			except:
				pass

		with open(location+'jobs-g1.csv','w') as cfile:
			writer=csv.writer(cfile)
			for row in data:
				writer.writerow(row)

def graph2(json_data,comparison):
	# graph 2 - load existing data:
	with open(location+'jobs-g2.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]
	temp_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='LNS12300060'][0]

	if temp!=temp_compare:
		print 'graph 2 changed'
		elapsed=8+((2016-now.year)*12)+(1/12)*(now.month-1)

		for time_period in temp['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				epop=float(time_period['value'])
				data.append(['December 2007-Present',epop,elapsed,float(epop)-79.7])

		with open(location+'jobs-g2.csv','w') as cfile:
			writer=csv.writer(cfile)
			for row in data:
				writer.writerow(row)

def graph3(json_data,comparison):
	# graph 3 - load existing data:
	with open(location+'jobs-g3.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp_private=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000001'][0]
	temp_public=[series for series in json_data['Results']['series'] if series['seriesID']=='CES9000000001'][0]
	temp_private_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES0500000001'][0]
	temp_public_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES9000000001'][0]

	start_emp_private=115778
	start_emp_public=22219

	if temp_private!=temp_private_compare:
		print 'graph 3 changed'
		for time_period in temp_private['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				private_emp=float(time_period['value'])
				data.append([datestring,private_emp,100*(private_emp/start_emp_private),'Private Sector'])

		print 'private prelim data for graph 3'

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==two_string and row[3]=='Private Sector':
				match=[item for item in temp_private['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				private_emp=float(match[0]['value'])
				data[i][1]=private_emp
				data[i][2]=100*(private_emp/start_emp_private)
			if row[0]==three_string and row[3]=='Private Sector':
				match=[item for item in temp_private['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				private_emp=float(match[0]['value'])
				data[i][1]=private_emp
				data[i][2]=100*(private_emp/start_emp_private)
			if row[0]==one_string and row[3]=='Private Sector':
				match=[item for item in temp_private['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				private_emp=float(match[0]['value'])
				data[i][1]=private_emp
				data[i][2]=100*(private_emp/start_emp_private)

		if temp_public!=temp_public_compare:
			for time_period in temp_public['data']:
				if time_period['periodName']==month and int(time_period['year'])==year:
					public_emp=float(time_period['value'])
					data.append([datestring,public_emp,100*(public_emp/start_emp_public),'Public Sector'])

		print 'public prelim data for graph 3'

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==two_string and row[3]=='Public Sector':
				match=[item for item in temp_public['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				public_emp=float(match[0]['value'])
				data[i][1]=public_emp
				data[i][2]=100*(public_emp/start_emp_public)

			if row[0]==three_string and row[3]=='Public Sector':
				match=[item for item in temp_public['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				public_emp=float(match[0]['value'])
				data[i][1]=public_emp
				data[i][2]=100*(public_emp/start_emp_public)

			if row[0]==one_string and row[3]=='Public Sector':
				match=[item for item in temp_public['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				public_emp=float(match[0]['value'])
				data[i][1]=public_emp
				data[i][2]=100*(public_emp/start_emp_public)

	with open(location+'jobs-g3.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph4(json_data):
	# graph 4. This is done a little differently than 1,2,3,7,8 because I fell on my head and became smarter. Instead of trying to maintain and update
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


def graph5(json_data):
	pass


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


def graph7(json_data,comparison):
	# graph 7 - load existing data:
	with open(location+'jobs-g7.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp_inflation=[series for series in json_data['Results']['series'] if series['seriesID']=='CUUR0000SA0'][0]
	temp_earnings=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000008'][0]
	temp_inflation_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CUUR0000SA0'][0]
	temp_earnings_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES0500000008'][0]

	oneyearstring=month+', '+str(year-1)
	oys_1=one_month_ago.strftime("%B")+', '+str(one_month_ago.year-1)
	oys_2=two_month_ago.strftime("%B")+', '+str(two_month_ago.year-1)
	oys_3=three_month_ago.strftime("%B")+', '+str(three_month_ago.year-1)

	if temp_earnings!=temp_earnings_compare:
		for time_period in temp_earnings['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				earnings=float(time_period['value'])
				for row in data:
					if row[0]==oneyearstring and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
						old_earnings=row[3]

				growth=100*(float(earnings)-float(old_earnings))/float(old_earnings)
				data.append([datestring,growth,'Year over year change in earnings for production and nonsupervisory workers',earnings])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==two_string and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
				match=[item for item in temp_earnings['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				earnings=float(match[0]['value'])

				for row in data:
					if row[0]==oys_2 and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
						old_earnings=row[3]

				data[i][1]=100*(float(earnings)-float(old_earnings))/float(old_earnings)
				data[i][3]=earnings

			if row[0]==three_string and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
				match=[item for item in temp_earnings['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				earnings=float(match[0]['value'])

				for row in data:
					if row[0]==oys_3 and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
						old_earnings=row[3]

				data[i][1]=100*(float(earnings)-float(old_earnings))/float(old_earnings)
				data[i][3]=earnings

			if row[0]==one_string and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
				match=[item for item in temp_earnings['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				earnings=float(match[0]['value'])

				for row in data:
					if row[0]==oys_1 and row[2]=='Year over year change in earnings for production and nonsupervisory workers':
						old_earnings=row[3]

				data[i][1]=100*(float(earnings)-float(old_earnings))/float(old_earnings)
				data[i][3]=earnings

	if temp_inflation!=temp_inflation_compare:
		for time_period in temp_inflation['data']:
			if time_period['periodName']==one_month_ago.strftime("%B") and int(time_period['year'])==one_month_ago.year:
				inflation=float(time_period['value'])

		oneyearonemonthstring=one_month_ago.strftime("%B")+', '+str(one_month_ago.year-1)
		for row in data:
			if row[0]==oneyearonemonthstring and row[2]=='Annual inflation':
				old_inflation=row[3]

		growth=100*(float(inflation)-float(old_inflation))/float(old_inflation)
		newstring=one_month_ago.strftime("%B")+', '+str(one_month_ago.year)
		data.append([newstring,growth,'Annual inflation',inflation])

	with open(location+'jobs-g7.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)


def graph8(json_data,comparison):
	# graph 8 - load existing data:
	with open(location+'jobs-g8.csv','rU') as cfile:
		reader=csv.reader(cfile)
		data=[row for row in reader]

	temp_construction=[series for series in json_data['Results']['series'] if series['seriesID']=='CES2000000001'][0]
	temp_manufacturing=[series for series in json_data['Results']['series'] if series['seriesID']=='CES3000000001'][0]
	temp_retail=[series for series in json_data['Results']['series'] if series['seriesID']=='CES4200000001'][0]
	temp_ed=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6561000001'][0]
	temp_health=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6562000001'][0]
	temp_leisure=[series for series in json_data['Results']['series'] if series['seriesID']=='CES7000000001'][0]

	temp_construction_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES2000000001'][0]
	temp_manufacturing_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES3000000001'][0]
	temp_retail_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES4200000001'][0]
	temp_ed_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES6561000001'][0]
	temp_health_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES6562000001'][0]
	temp_leisure_compare=[series for series in comparison['Results']['series'] if series['seriesID']=='CES7000000001'][0]

	con_average=7627.3
	man_average=13877.8
	ret_average=15516.3
	edu_average=2941.7
	hea_average=15734.3
	lei_average=13427.9

	print temp_construction
	print temp_construction_compare

	if temp_construction!=temp_construction_compare:
		for time_period in temp_construction['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				raw_emp=float(time_period['value'])
				data.append([datestring,100*raw_emp/con_average,'Construction',raw_emp,con_average])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==one_string and row[2]=='Construction':
				match=[item for item in temp_construction['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/con_average
				data[i][3]=raw_emp

			if row[0]==two_string and row[2]=='Construction':
				match=[item for item in temp_construction['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/con_average
				data[i][3]=raw_emp

			if row[0]==three_string and row[2]=='Construction':
				match=[item for item in temp_construction['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/con_average
				data[i][3]=raw_emp

	if temp_manufacturing!=temp_manufacturing_compare:
		for time_period in temp_manufacturing['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				raw_emp=float(time_period['value'])
				data.append([datestring,100*raw_emp/man_average,'Manufacturing',raw_emp,man_average])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==one_string and row[2]=='Manufacturing':
				match=[item for item in temp_manufacturing['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/man_average
				data[i][3]=raw_emp

			if row[0]==two_string and row[2]=='Manufacturing':
				match=[item for item in temp_manufacturing['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/man_average
				data[i][3]=raw_emp

			if row[0]==three_string and row[2]=='Manufacturing':
				match=[item for item in temp_manufacturing['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/man_average
				data[i][3]=raw_emp

	if temp_retail!=temp_retail_compare:
		for time_period in temp_retail['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				raw_emp=float(time_period['value'])
				data.append([datestring,100*raw_emp/ret_average,'Retail',raw_emp,ret_average])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==one_string and row[2]=='Retail':
				match=[item for item in temp_retail['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/ret_average
				data[i][3]=raw_emp

			if row[0]==two_string and row[2]=='Retail':
				match=[item for item in temp_retail['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/ret_average
				data[i][3]=raw_emp

			if row[0]==three_string and row[2]=='Retail':
				match=[item for item in temp_retail['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/ret_average
				data[i][3]=raw_emp

	if temp_ed!=temp_ed_compare:
		for time_period in temp_ed['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				raw_emp=float(time_period['value'])
				data.append([datestring,100*raw_emp/edu_average,'Educational Services',raw_emp,edu_average])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==one_string and row[2]=='Educational Services':
				match=[item for item in temp_ed['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/edu_average
				data[i][3]=raw_emp

			if row[0]==two_string and row[2]=='Educational Services':
				match=[item for item in temp_ed['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/edu_average
				data[i][3]=raw_emp

			if row[0]==three_string and row[2]=='Educational Services':
				match=[item for item in temp_ed['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/edu_average
				data[i][3]=raw_emp

	if temp_health!=temp_health_compare:
		for time_period in temp_health['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				raw_emp=float(time_period['value'])
				data.append([datestring,100*raw_emp/hea_average,'Health care and social assistance',raw_emp,hea_average])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==one_string and row[2]=='Health care and social assistance':
				match=[item for item in temp_health['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/hea_average
				data[i][3]=raw_emp

			if row[0]==two_string and row[2]=='Health care and social assistance':
				match=[item for item in temp_health['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/hea_average
				data[i][3]=raw_emp

			if row[0]==three_string and row[2]=='Health care and social assistance':
				match=[item for item in temp_health['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/hea_average
				data[i][3]=raw_emp

	if temp_leisure!=temp_leisure_compare:
		for time_period in temp_leisure['data']:
			if time_period['periodName']==month and int(time_period['year'])==year:
				raw_emp=float(time_period['value'])
				data.append([datestring,100*raw_emp/lei_average,'Leisure and hospitality',raw_emp,lei_average])

		# since there is preliminary data, make sure you go back three months and check those against the new data
		for i,row in enumerate(data):
			if row[0]==one_string and row[2]=='Leisure and hospitality':
				match=[item for item in temp_leisure['data'] if item['periodName']==one_month_ago.strftime("%B") and int(item['year'])==one_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/lei_average
				data[i][3]=raw_emp

			if row[0]==two_string and row[2]=='Leisure and hospitality':
				match=[item for item in temp_leisure['data'] if item['periodName']==two_month_ago.strftime("%B") and int(item['year'])==two_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/lei_average
				data[i][3]=raw_emp

			if row[0]==three_string and row[2]=='Leisure and hospitality':
				match=[item for item in temp_leisure['data'] if item['periodName']==three_month_ago.strftime("%B") and int(item['year'])==three_month_ago.year]
				raw_emp=float(match[0]['value'])
				data[i][1]=100*raw_emp/lei_average
				data[i][3]=raw_emp

	with open(location+'jobs-g8.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)

location=os.path.dirname(os.path.realpath(__file__))+'/'
# location='/home/eqgrowth/webapps/jobsday/data/'
print location

# get API key
key=open(location+'key.txt','r').read()

# get the month and year of the *previous* month
# now=datetime.date.today()
now=datetime.date(2016,6,24)
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
comparison=compare(json_data)
print 'loaded comparison'
if comparison!=json_data:
	graph1(json_data,comparison)
	print 'graph 1 done'
	graph2(json_data,comparison)
	print 'graph 2 done'
	graph3(json_data,comparison)
	print 'graph 3 done'
#	graph4(json_data,comparison)
#	graph5(json_data,comparison)
	graph6(json_data)
	print 'graph 6 done'
	graph7(json_data,comparison)
	print 'graph 7 done'
	graph8(json_data,comparison)
	print 'graph 8 done'

	pickle.dump(json_data,open(location+'json_data.p','wb'))











