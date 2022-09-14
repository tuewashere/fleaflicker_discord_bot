import requests, json, time, datetime, os

current = int(time.time() * 1000)
parameters = {"league_id": LEAGUE ID HERE}
response = requests.get('https://www.fleaflicker.com/api/FetchLeagueActivity', params=parameters)
response = response.json()["items"]
data = json.dumps(response, sort_keys = True, indent = 4)
trade_ids = []


def transactions(obj, n):
	obj = json.loads(obj)
	if current - int(obj[n]['timeEpochMilli']) < 86400000: 
		transaction = obj[n].get('transaction')
		ir_change = obj[n].get('reserveChange')
		if transaction: 
			add_remove_trade(transaction)
		elif ir_change:
			reserve_change(ir_change) 
		else:
			other = obj[n].get('settings') 
			if other == None: 
				other = obj[n].get('tradeBlock')
				trade_block(other) 
			else:
				print (other['description']) # commish change

def add_remove_trade(obj):
	trade = obj.get('tradeId')
	if trade:
		if trade not in trade_ids:
			print ('TRADE')
			trade_details(obj)
			trade_ids.append(trade)
		else:
			trade_details(obj)
	else:
		info = obj.get('player')
		owner_info = info.get('owner')
		if owner_info == None:
			print ((info['proPlayer']['nameFull']) + ' was dropped')
		else:
			print (owner_info['name'] + ' added ' + info['proPlayer']['nameFull'])

def trade_details(obj):
	draftPick = obj.get('draftPick')
	player = obj.get('player')
	if draftPick:
		season = draftPick['season']
		rnd =  draftPick['round']
		print ( obj['team']['name'] + ' receives ' + str(rnd)  + "th " + 'round pick in ' + str(season) ) 
	elif player:
		print ( player['owner']['name'] + ' receives ' + player['proPlayer']['nameFull'] )
	
def trade_block(obj):
	info = obj.get('player')
	owner_info = info.get('owner')
	if obj['removed']:
		print (owner_info['name'] + ' removed ' + info['proPlayer']['nameFull'] + ' from the trade block')
	else:
		print (owner_info['name'] + ' added ' + info['proPlayer']['nameFull'] + ' to the trade block')

def reserve_change(obj):
	info = obj.get('player')
	owner_info = info.get('owner')
	status = obj.get('removed')
	if status:
		print (owner_info['name'] + ' removed ' + info['proPlayer']['nameFull'] + ' from IR')
	else:
		print (owner_info['name'] + ' added ' + info['proPlayer']['nameFull'] + ' to IR')

for x in range(30):
	transactions(data, x)






