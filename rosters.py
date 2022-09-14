import os, discord, requests, json, time, datetime, asyncio

roster_message = []
def team_owners():
	for x in range (10): #modify this depending on size of league
		league_id = {"league_id": LEAGUE ID HERE}
		team_ids= {DICTIONARY OF TEAM IDs} #example: 'team1_id': 'joe', 'team2_id': 'Bob', 'team3_id': 'Josh'
		ids = (requests.get('https://www.fleaflicker.com/api/FetchLeagueRosters', params=league_id)).json()['rosters'][x]['team']['id']
		id_data = json.dumps(ids, sort_keys = True, indent = 4)
		names = (requests.get('https://www.fleaflicker.com/api/FetchLeagueRosters', params=league_id)).json()['rosters'][x]['team']['name']
		names_data = json.dumps(names, sort_keys = True, indent = 4)
		if id_data in team_ids.keys():
			roster_message.append(names_data + ' is ' + team_ids[id_data])

print ('\n'.join(roster_message))
