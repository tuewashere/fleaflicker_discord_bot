import os, discord, asyncio, requests, json, time, datetime
from datetime import datetime
from discord.ext import commands, tasks

current = int(time.time() * 1000)

league_id = {"league_id": LEAGUE ID HERE,}
DISCORD_TOKEN = DISCORD TOKEN HERE
channel_id = CHANNEL ID HERE 

response = (requests.get('https://www.fleaflicker.com/api/FetchLeagueActivity', params=league_id)).json()['items']
data = json.dumps(response, sort_keys = True, indent = 4)


client = discord.Client()
trade_ids = []
transactions_message = []

def transactions(obj, n):
	obj = json.loads(obj)
	if current - int(obj[n]['timeEpochMilli']) < 86400000: #remove a 0 to make it 10days to 1 day
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
				transactions_message ((other['description'])) # commish change
	return (transactions_message)

def add_remove_trade(obj):
	trade = obj.get('tradeId')
	if trade:
		if trade not in trade_ids:
			transactions_message.append('**TRADE**')
			trade_details(obj)
			trade_ids.append(trade)
		else:
			trade_details(obj)
	else:
		info = obj.get('player')
		owner_info = info.get('owner')
		if owner_info == None:
			transactions_message.append((info['proPlayer']['nameFull']) + ' was dropped')
		else:
			transactions_message.append(owner_info['name'] + ' added ' + info['proPlayer']['nameFull'])

def trade_details(obj):
	draftPick = obj.get('draftPick')
	player = obj.get('player')
	if draftPick:
		season = draftPick['season']
		rnd =  draftPick['round']
		transactions_message.append( obj['team']['name'] + ' receives ' + str(rnd)  + "th " + 'round pick in ' + str(season)) 
	elif player:
		transactions_message.append( player['owner']['name'] + ' receives ' + player['proPlayer']['nameFull'])
	
def trade_block(obj):
	info = obj.get('player')
	owner_info = info.get('owner')
	if obj['removed']:
		transactions_message.append(owner_info['name'] + ' removed ' + info['proPlayer']['nameFull'] + ' from the trade block')
	else:
		transactions_message.append(owner_info['name'] + ' added ' + info['proPlayer']['nameFull'] + ' to the trade block')

def reserve_change(obj):
	info = obj.get('player')
	owner_info = info.get('owner')
	status = obj.get('removed')
	if status:
		transactions_message.append(owner_info['name'] + ' removed ' + info['proPlayer']['nameFull'] + ' from IR')
	else:
		transactions_message.append(owner_info['name'] + ' added ' + info['proPlayer']['nameFull'] + ' to IR')

def timer():
	while True:
		current_time = datetime.now().strftime("%H:%M")
		if current_time == '10:00': # set to what time you want message sent
			for x in range(30):
				transactions(data, x)
			break

timer()
@client.event
async def on_ready():
	for guild in client.guilds:
		channel = client.get_channel(channel_id)
		await channel.send('**Transactions in the last 24 hours**')
		if (len(transactions_message)) > 0:
			await channel.send('\n'.join(transactions_message))
			transactions_message.clear()
			trade_ids.clear()


client.run(DISCORD_TOKEN)


