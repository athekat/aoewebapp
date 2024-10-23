import json
import requests
from datetime import datetime

def get_civilization_descriptions(file_path):
  with open(file_path, 'r') as f:
    data = json.load(f)
    return {civ['name']: civ['description'] for civ in data}

def get_match_info(api_url, civilizations_file):
  response = requests.get(api_url)

  if response.status_code == 200:
    data = json.loads(response.text)
    matches = data.get('matches', [])

    if matches:
      # Get the most recent match
      most_recent_match = matches[0]

      # Extract relevant information
      map_name = most_recent_match.get('mapName')
      started = most_recent_match.get('started')
      players = most_recent_match.get('teams', [])

      if players:
        player1_name = players[0]['players'][0]['name']
        player1_rating = players[0]['players'][0]['rating']
        player1_civ_name = players[0]['players'][0]['civName']

        player2_name = players[1]['players'][0]['name']
        player2_rating = players[1]['players'][0]['rating']
        player2_civ_name = players[1]['players'][0]['civName']

        # Load civilization descriptions
        civilization_descriptions = get_civilization_descriptions(civilizations_file)

        # Access description directly from dictionary
        player1_description = civilization_descriptions.get(player1_civ_name)
        player2_description = civilization_descriptions.get(player2_civ_name)

        return {
            'mapName': map_name,
            'started': started,
            'player1Name': player1_name,
            'player1Rating': player1_rating,
            'player1CivName': player1_civ_name,
            'player1CivDescription': player1_description,
            'player2Name': player2_name,
            'player2Rating': player2_rating,
            'player2CivName': player2_civ_name,
            'player2CivDescription': player2_description,
        }
      else:
        print("No players found in the match data")
        return {}
  else:
    print("API request failed")
    return {}

api_url = "https://data.aoe2companion.com/api/matches?profile_ids=208269&search=&leaderboard_ids=&page=1"
civilizations_file = "myapp/civilizationsnew.json"
match_info = get_match_info(api_url, civilizations_file)

# Convert timestamp to date and time
started_datetime = datetime.strptime(match_info['started'], '%Y-%m-%dT%H:%M:%S.%fZ')
started_formatted = started_datetime.strftime('%Y-%m-%d %H:%M:%S')

if match_info:
  print(f"==================<br><b>Date:</b> {started_formatted} <br><b>Map:</b> {match_info['mapName']}<br>==================")
  print(f"<br><br>")
  print(f"<b>{match_info['player1Name']} ({match_info['player1Rating']}</b>) <br> {match_info['player1CivName']} <br> {match_info['player1CivDescription']}")
  print(f"<br><br>==================<br><br>")
  print(f"<b>{match_info['player2Name']} ({match_info['player2Rating']}</b>) <br> {match_info['player2CivName']} <br> {match_info['player2CivDescription']}<br>")

else:
  print("No match information found.")