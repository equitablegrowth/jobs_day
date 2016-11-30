def graph9(json_data):
	temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327659'][0]['data']
	temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327660'][0]['data']
	temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327689'][0]['data']
	temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS12327662'][0]['data']
	data=[['type','date','epop']]
	for item in temp_1:
		if(int(item['year'])>1999):
			data.append(['< High school',item['periodName']+', '+item['year'],float(item['value'])])
	for item in temp_2:
		if(int(item['year'])>1999):
			data.append(['High school graduate',item['periodName']+', '+item['year'],float(item['value'])])
	for item in temp_3:
		if(int(item['year'])>1999):
			data.append(['Some college',item['periodName']+', '+item['year'],float(item['value'])])
	for item in temp_4:
		if(int(item['year'])>1999):
			data.append(["Bachelor's degree or greater",item['periodName']+', '+item['year'],float(item['value'])])
	with open('/Users/austinclemens/Desktop/jobs-g9.csv','w') as cfile:
		writer=csv.writer(cfile)
		for row in data:
			writer.writerow(row)	



#UNEMPLOYMENT

# college grads - LNS14027662
# high school grads - LNS14027660
# < high school - LNS14027659
# some college - LNS14027689

series=['LNS14027662','LNS14027660','LNS14027659','LNS14027689']
data = json.dumps({"seriesid": series,"startyear":2000, "endyear":year, "registrationKey":key})
p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027659'][0]['data']
temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027660'][0]['data']
temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027689'][0]['data']
temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS14027662'][0]['data']
data=[['type','date','epop']]
for item in temp_1:
	if(int(item['year'])>1999):
		data.append(['< High school',item['periodName']+', '+item['year'],float(item['value'])])
for item in temp_2:
	if(int(item['year'])>1999):
		data.append(['High school graduate',item['periodName']+', '+item['year'],float(item['value'])])
for item in temp_3:
	if(int(item['year'])>1999):
		data.append(['Some college',item['periodName']+', '+item['year'],float(item['value'])])
for item in temp_4:
	if(int(item['year'])>1999):
		data.append(["Bachelor's degree or greater",item['periodName']+', '+item['year'],float(item['value'])])
with open('/Users/austinclemens/Desktop/jobs-g9.csv','w') as cfile:
	writer=csv.writer(cfile)
	for row in data:
		writer.writerow(row)




series=['LNS13023570','LNS13023558','LNS13023706','LNS13023622']
data = json.dumps({"seriesid": series,"startyear":2000, "endyear":year, "registrationKey":key})
p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023570'][0]['data']
temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023558'][0]['data']
temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023706'][0]['data']
temp_4=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13023622'][0]['data']
data=[['type','date','epop']]
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
with open('/Users/austinclemens/Desktop/jobs-g10.csv','w') as cfile:
	writer=csv.writer(cfile)
	for row in data:
		writer.writerow(row)





series=['LNS13008397','LNS13025701','LNS13008517']
data = json.dumps({"seriesid": series,"startyear":2000, "endyear":year, "registrationKey":key})
p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
temp_1=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008397'][0]['data']
temp_2=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13025701'][0]['data']
temp_3=[series for series in json_data['Results']['series'] if series['seriesID']=='LNS13008517'][0]['data']
data=[['type','date','epop']]

for item in temp_1:
	if(int(item['year'])>1999):
		data.append(['Fewer than 5 weeks',item['periodName']+', '+item['year'],float(item['value'])])
for item in temp_2:
	if(int(item['year'])>1999):
		data.append(['5-14 weeks',item['periodName']+', '+item['year'],float(item['value'])])
for item in temp_3:
	if(int(item['year'])>1999):
		data.append(['More than 15 weeks',item['periodName']+', '+item['year'],float(item['value'])])
with open('/Users/austinclemens/Desktop/jobs-g11.csv','w') as cfile:
	writer=csv.writer(cfile)
	for row in data:
		writer.writerow(row)


series=['CES2000000003','CES3000000003','CES5500000003','CES6000000003','CES6500000003','CEU7000000003']
data = json.dumps({"seriesid": series,"startyear":2000, "endyear":year, "registrationKey":key})
p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
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

with open('/Users/austinclemens/Desktop/jobs-g12.csv','w') as cfile:
	writer=csv.writer(cfile)
	for row in data:
		writer.writerow(row)





