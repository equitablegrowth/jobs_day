from __future__ import division
import requests
import json
import datetime
import os
import csv
import pickle

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def data_scrape():
	headers = {'Content-type': 'application/json'}
	now=datetime.date.today()
	currentmonth=monthdelta(now,-1)
	year=currentmonth.year

	series=['LNS12300060','CES0500000001','CES9000000001','LNS14000003','LNS14000006','LNS14000009','LNS14000000','LNS13327709','LNS12032194','LNS12600000','CES0500000008','CES2000000001','CES3000000001','CES4200000001','CES6561000001','CES6562000001','CUUR0000SA0','CES7000000001']
	data = json.dumps({"seriesid": series,"startyear":year-1, "endyear":year})
	p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
	json_data = json.loads(p.text)

	return json_data

def manual():

	print "=== GRAPH 1 and 2 ==="
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12300060'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print "=== GRAPH 3 ==="
	print 'PRIVATE'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print 'PUBLIC'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES9000000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print "=== GRAPH 7 ==="
	print 'EARNINGS'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES0500000008'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print "=== GRAPH 8 ==="
	print 'CONSTRUCTION'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES2000000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print 'MANUFACTURING'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES3000000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print 'RETAIL'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES4200000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print 'EDUCATION'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6561000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print 'HEALTH'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES6562000001'][0]
	for row in temp['data']:
		print row

	print ''
	print ''
	print 'LEISURE'
	temp=[series for series in json_data['Results']['series'] if series['seriesID']=='CES7000000001'][0]
	for row in temp['data']:
		print row











