import json
import requests

# DON'T RUN THIS ALL THE TIME, IT PULLS ALL OF SLEEPER'S 
# NFL PLAYER DATA, SLEEPER RECOMMENDS ONCE A DAY
playerDataCall = 'https://api.sleeper.app/v1/players/nfl'
playerData = requests.get(playerDataCall).json()

with open("playerData.json", "w") as write_file:
	json.dump(playerData, write_file)
