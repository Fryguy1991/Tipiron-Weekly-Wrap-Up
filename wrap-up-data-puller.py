import json
import requests

class TippyMember:
	def __init__(self, userData, score, starters, bench, matchupId):
		self.userData = userData
		self.score = score
		self.starters = starters
		self.bench = bench
		self.matchupId = matchupId

class TippyUserData:
	def __init__(self, userId, rosterId, rosterName):
		self.userId = userId
		self.rosterId = rosterId
		self.rosterName = rosterName

def printTippyMember(member):
	print(member.userData)
	print(member.score)
	print(member.starters)
	print(member.bench)
	print(member.matchupId)

def printWithPlayerNames(playerScoreTuples, playerData, listName, positionsToExclude, printCount):
	listWithPlayerData = []
	for player in playerScoreTuples:
		score = player[1]
		teamName = player[2]
		currentPlayer = playerData[player[0]]
		playerPositions = currentPlayer["fantasy_positions"]
		shouldExclude = False
		for position in positionsToExclude:
			if position in playerPositions:
				shouldExclude = True
				break
		if shouldExclude:
			continue
		firstName = currentPlayer["first_name"]
		lastName = currentPlayer["last_name"]
		playerName = '{0} {1}'.format(firstName, lastName)
		listWithPlayerData.append((playerName, score, teamName))
	print("\n#########################")
	print(listName)
	print("#########################")
	if len(listWithPlayerData) == 0:
		print("NONE")
	else :
		for entry in listWithPlayerData:
			if printCount == 0:
				break
			playerOutput = '{0}, {1}, {2}'.format(entry[0], entry[1], entry[2])
			print(playerOutput)
			printCount -= 1

# Don't change the league ID unless you want to pull data from another league
tippyLeagueId = 1048437082550652928
# Set below with the number of the week you'd like to pull data
week = input("What week do you want to write a wrap up for?\n")

tippyRosterDataCall = 'https://api.sleeper.app/v1/league/{0}/rosters'.format(tippyLeagueId)
tippyUserDataCall = 'https://api.sleeper.app/v1/league/{0}/users'.format(tippyLeagueId)
weekMatchupsRequest = 'https://api.sleeper.app/v1/league/{0}/matchups/{1}'.format(tippyLeagueId, week)

rosterData = requests.get(tippyRosterDataCall).json()
tippyUserData = requests.get(tippyUserDataCall).json()

rosterOrder = []
for roster in rosterData:
	rosterOrder.append(roster["owner_id"])

# Pull the desired user data
users = []
for user in tippyUserData:
	teamName = ""
	if user["user_id"] == "1147412178325188608": # Remove Cory's ass from the wrap-up
		continue
	if "team_name" in user["metadata"]:
		teamName = user["metadata"]["team_name"]
	else: 
		teamName = user["display_name"]
	rosterId = rosterOrder.index(user["user_id"])
	users.append(TippyUserData(user["user_id"], rosterId, teamName))

# Sort the user data by roster ID
users.sort(key=lambda x: x.rosterId)

# Pull matchup data (scores, player scores, etc.) and combine with user data
matchupData = requests.get(weekMatchupsRequest).json()
members = []
for matchup in matchupData:
	userDataIndex = matchup["roster_id"] - 1
	score = matchup["points"]
	matchupId = matchup["matchup_id"]
	starters = matchup["starters"]
	bench = matchup["players"]
	for player in starters:
		bench.remove(player)
	startPoints = matchup["players_points"].copy()
	benchPoints = matchup["players_points"].copy()
	for player in starters:
		del benchPoints[player]
	for player in bench:
		del startPoints[player]
	members.append(TippyMember(users[userDataIndex], score, startPoints, benchPoints, matchupId))

# Sort all started players by points scored to get Boom Squad
boomSquad = []
for member in members:
	for starter in member.starters:
		boomSquad.append((starter, member.starters[starter], member.userData.rosterName))
boomSquad.sort(key=lambda a: a[1], reverse=True)

# Sort all benched players by points scored to get Riding Pine Squad
ridingPine = []
for member in members:
	for player in member.bench:
		ridingPine.append((player, member.bench[player], member.userData.rosterName))
ridingPine.sort(key=lambda a: a[1], reverse=True)

# Copy and reverse Boom Squad list to get Busted Boys
bustedBoys = boomSquad.copy()
bustedBoys.sort(key=lambda a: a[1])

# Get Opher Gopher candidates (zero or less points)
gophers = boomSquad.copy()
removals = []
for entry in gophers:
	if entry[1] > 0:
		removals.append(entry)
for removal in removals:
	gophers.remove(removal)

# Print title for all lists
title = '\nTippy scoring lists for week {0}'.format(week)
print(title)

# Read most recently pulled player data into a json object
playerDataFile = open('playerData.json')
playerData = json.load(playerDataFile)
# print(playerData[0])

# Print the 4 lists we care about
printWithPlayerNames(boomSquad, playerData, "Boom Squad", [], 5)
printWithPlayerNames(bustedBoys, playerData, "Busted Boys", ['DEF', 'K'], 5)
printWithPlayerNames(ridingPine, playerData, "Riding Pine", ['QB'], 5)
printWithPlayerNames(gophers, playerData, "O'pher G0pher Candidates", ['DEF', 'K'], -1)
print()

# Group matchups
matchups = []
for matchupId in range(1, 7):
	currentMatchup = []
	for member in members:
		if member.matchupId == matchupId:
			currentMatchup.append(member)
	matchups.append((currentMatchup[0], currentMatchup[1]))
print('##########')
print('Matchups')
print('##########')
for matchup in matchups:
	team1 = matchup[0]
	team2 = matchup[1]
	output = '{0} - {1} vs {2} - {3}'.format(team1.userData.rosterName, team1.score, team2.userData.rosterName, team2.score)
	print(output)

# Find winners/losers
winners = []
losers = []
for matchup in matchups:
	team1 = matchup[0]
	team2 = matchup[1]
	if team1.score > team2.score:
		winners.append(team1)
		losers.append(team2)
	else:
		winners.append(team2)
		losers.append(team1)