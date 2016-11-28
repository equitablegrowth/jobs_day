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
return json_data

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
