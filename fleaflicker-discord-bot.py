import os, discord, requests, json, time, asyncio
import datetime as dt
from datetime import datetime
from discord.ext import commands, tasks

league_id = {"league_id": #LEAGUE ID HERE,}
DISCORD_TOKEN = #DISCORD TOKEN HERE
channel_id = # CHANNEL ID HERE
team_ids= {#LEAGUE_ID1: 'NAME OF OWNER', LEAGUE_ID2: 'NAME OF OWNER', ... }

current = int(time.time() * 1000)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
response = (requests.get('https://www.fleaflicker.com/api/FetchLeagueActivity', params=league_id)).json()['items']
data = json.dumps(response, sort_keys = True, indent = 4)
trade_ids = []
activity_wire = []
roster_message = []

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
				activity_wire.append((other['description'])) 

def add_remove_trade(obj):
	trade = obj.get('tradeId')
	if trade:
		if trade not in trade_ids:
			activity_wire.append('**TRADE**')
			trade_details(obj)
			trade_ids.append(trade)
		else:
			trade_details(obj)
	else:
		info = obj.get('player')
		owner_info = info.get('owner')
		if owner_info == None:
			activity_wire.append((info['proPlayer']['nameFull']) + ' was dropped')
		else:
			activity_wire.append(owner_info['name'] + ' added ' + info['proPlayer']['nameFull'])

def trade_details(obj):
	draftPick = obj.get('draftPick')
	player = obj.get('player')
	if draftPick:
		season = draftPick['season']
		rnd =  draftPick['round']
		activity_wire.append( obj['team']['name'] + ' receives ' + str(rnd)  + "th " + 'round pick in ' + str(season)) 
	elif player:
		activity_wire.append( player['owner']['name'] + ' receives ' + player['proPlayer']['nameFull'])
	
def trade_block(obj):
	info = obj.get('player')
	owner_info = info.get('owner')
	if obj['removed']:
		activity_wire.append(owner_info['name'] + ' removed ' + info['proPlayer']['nameFull'] + ' from the trade block')
	else:
		activity_wire.append(owner_info['name'] + ' added ' + info['proPlayer']['nameFull'] + ' to the trade block')

def reserve_change(obj):
	info = obj.get('player')
	owner_info = info.get('owner')
	status = obj.get('removed')
	if status:
		activity_wire.append(owner_info['name'] + ' removed ' + info['proPlayer']['nameFull'] + ' from IR')
	else:
		activity_wire.append(owner_info['name'] + ' added ' + info['proPlayer']['nameFull'] + ' to IR')


def team_owners():
	for x in range (10): # set to number of teams in your league
		ids = (requests.get('https://www.fleaflicker.com/api/FetchLeagueRosters', params=league_id)).json()['rosters'][x]['team']['id']
		id_data = json.dumps(ids, sort_keys = True, indent = 4)
		names = (requests.get('https://www.fleaflicker.com/api/FetchLeagueRosters', params=league_id)).json()['rosters'][x]['team']['name']
		names_data = json.dumps(names, sort_keys = True, indent = 4)
		if id_data in team_ids.keys():
			roster_message.append(names_data + ' is ' + team_ids[id_data])

@bot.event
async def on_ready():
	print ('logged in')
	msg1.start()

@tasks.loop(hours=24)
async def msg1():
	channel = bot.get_channel(channel_id)
	if (len(activity_wire)) > 0:
		await channel.send('**Transactions in the last 24 hours**')
		await channel.send('\n'.join(activity_wire))
		activity_wire.clear()
		trade_ids.clear()
		print ('scheduled message sent')
	else:
		await channel.send('**No transactions in the last 24 hours**')
		print ('scheduled message sent')

@msg1.before_loop
async def before_msg1():
	for x in range(60*60*24):
		if dt.datetime.now().hour == 17: # 24 hour clock set to when you want the message sent
			print ('its time')
			for x in range(30):
				transactions(data, x)
			return
		await asyncio.sleep(1)

@bot.command(name='teams') #
async def SendMessage(msg):
	team_owners()
	await msg.send('\n'.join(roster_message))
	roster_message.clear()

bot.run(DISCORD_TOKEN)





