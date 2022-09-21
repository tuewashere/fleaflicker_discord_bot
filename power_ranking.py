import requests, json, yaml

league_id = {"league_id": #LEAGUE ID HERE}
yaml_path = 'high_low.yaml'

def update_yaml(team_id, score):
	sm_list = list()
	with open (yaml_path, 'r') as f:
		HL_yml = yaml.safe_load(f)
		for x in HL_yml['teams']:
			if x['id'] == team_id:
				if score > x['high']:
					x['high'] = score
					x['sum'] = (x['high'] + x['low'])
				if score < x['low']:
					x['low'] = score
					x['sum'] = (x['high'] + x['low'])
				else:
					x['sum'] = (x['high'] + x['low'])
			if len(sm_list) < 10:
				sm_list.append(x)
		HL_yml['teams'] = sm_list
	with open(yaml_path, 'w') as f:
		yaml.dump(HL_yml, f)

def update_high_low():
	for x in range(5):
		params = {"league_id": 215756, 'scoring_period': total_games}
		away_score = requests.get('https://www.fleaflicker.com/api/FetchLeagueScoreboard', params=params).json()['games'][x]['awayScore']['score']['value']
		away_id = requests.get('https://www.fleaflicker.com/api/FetchLeagueScoreboard', params=params).json()['games'][x]['away']['id']
		home_score = requests.get('https://www.fleaflicker.com/api/FetchLeagueScoreboard', params=params).json()['games'][x]['homeScore']['score']['value']
		home_id = requests.get('https://www.fleaflicker.com/api/FetchLeagueScoreboard', params=params).json()['games'][x]['home']['id']
		update_yaml(away_id, away_score)
		update_yaml(home_id, home_score)

def get_ff_values(team_id):
	values = list()
	for x in range (5):
		div_1 = requests.get('https://www.fleaflicker.com/api/FetchLeagueStandings', params=league_id).json()['divisions'][0]["teams"][x]
		div_2 = requests.get('https://www.fleaflicker.com/api/FetchLeagueStandings', params=league_id).json()['divisions'][1]["teams"][x]
		if div_1['id'] == team_id:
			winrate = float (div_1['recordOverall']['winPercentage']['formatted'])
			points_for = (div_1['pointsFor']['value'])/total_games
		elif div_2['id'] == team_id:
			winrate = float (div_2['recordOverall']['winPercentage']['formatted'])
			points_for = (div_2['pointsFor']['value'])/total_games
	values.append(winrate * 200 * 2) 
	values.append(points_for * 6)
	return values

def update_pwr():
	pwr_list = list()
	with open (yaml_path, 'r') as f:
		HL_yml = yaml.safe_load(f)
		for x in HL_yml['teams']:
			values = get_ff_values((x['id']))
			x['pr'] = (x['sum']	+ values[0] + values[1])/10
			if len(pwr_list) < 10:
				pwr_list.append(x)
		HL_yml['teams'] = pwr_list
	with open(yaml_path, 'w') as f:
		yaml.dump(HL_yml, f)

def create_pwr():
	update_high_low()
	update_pwr()
	with open (yaml_path, 'r') as f:
		ranking = {}
		RankList = list()
		HL_yml = yaml.safe_load(f)
		for x in HL_yml['teams']:
			pr = x['pr'] 
			name = x['name']
			ranking[pr] = name
		ranking = (sorted(ranking.items(), reverse=True))
		for x in range(10):
			RankList.append(ranking[x][1])
		return ('\n'.join(RankList))

with open (yaml_path, 'r') as f: 
	HL_yml = yaml.safe_load(f)
	week =  HL_yml['week']
	total_games = week - 1
	msg = create_pwr()
	print ('Week ' + str(week) + ' power rankings:')
	print (msg)
	

