from django.shortcuts import render
import json
import requests

descriptions_url = "https://github.com/SiegeEngineers/aoe2techtree/raw/847a85a575b859d3a31818862483c75b17ec15d4/data/locales/en/strings.json"

def get_civilization_ids(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_civilization_description_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch civilization descriptions from URL: {url} (Status code: {response.status_code})")
        return {}

def get_match_info(api_url, civilizations_file, descriptions_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        data = json.loads(response.text)
        matches = data.get('matches', [])

        if matches:
            most_recent_match = matches[0]
            map_name = most_recent_match.get('mapName')
            match_status = most_recent_match.get("finished")
            map_icon = most_recent_match.get('mapImageUrl')
            players = most_recent_match.get('teams', [])

            if match_status is None:
                match_status_message = "Match is being played."
            else:
                match_status_message = "Match finished."

            if players and len(players) == 2 and len(players[0]['players']) == 1 and len(players[1]['players']) == 1:
                player1 = players[0]['players'][0]
                player2 = players[1]['players'][0]

                # Load civilization name to ID mapping
                civilization_ids = get_civilization_ids(civilizations_file)

                # Fetch civilization descriptions from the URL
                civilization_descriptions = get_civilization_description_from_url(descriptions_url)

                player1_civ_id = civilization_ids.get(player1['civName'])
                player2_civ_id = civilization_ids.get(player2['civName'])

                player1_description = civilization_descriptions.get(str(player1_civ_id), "Description not found.")
                player2_description = civilization_descriptions.get(str(player2_civ_id), "Description not found.")
                player1won = player1['won']
                if player1won is True:
                    player1won = "&#128081;"
                elif player1won is False:
                    player1won = "&#128128;"
                else:
                    player1won = "&#9203;"
                player2won = player2['won']
                if player2won is True:
                    player2won = "&#128081;"
                elif player2won is False:
                    player2won = "&#128128;"
                else:
                    player2won = "&#9203;"
                
                return {
                    'mapName': map_name,
                    'mapIcon': map_icon,
                    'player1Name': player1['name'],
                    'player1Rating': player1['rating'],
                    'player1CivName': player1['civName'],
                    'player1CivDescription': player1_description,
                    'player1color': player1['colorHex'],
                    'player1won': player1won,
                    'player2Name': player2['name'],
                    'player2Rating': player2['rating'],
                    'player2CivName': player2['civName'],
                    'player2CivDescription': player2_description,
                    'player2color': player2['colorHex'],
                    'player2won': player2won,
                    'match_status': match_status_message,
                }
            else:
                return {"error": "Could not extract player information."}
        else:
            return {"error": "No 1v1 matches found for this profile ID."}
    else:
        return {"error": f"API request failed with status code: {response.status_code}"}

def your_django_view(request):
    civilizations_file = "match1v1/civilizationsnew.json"
    descriptions_url = "https://github.com/SiegeEngineers/aoe2techtree/raw/847a85a575b859d3a31818862483c75b17ec15d4/data/locales/en/strings.json"
    match_info = None
    output = None

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        if profile_id:
            print(f"Profile ID submitted: {profile_id}")
            api_url = f"https://data.aoe2companion.com/api/matches?profile_ids={profile_id}&search=&leaderboard_ids=rm_1v1&page=1"
            match_data = get_match_info(api_url, civilizations_file, descriptions_url)
            if "error" in match_data:
                output = match_data["error"]
            else:
                match_info = match_data
        else:
            output = "Please enter a Profile ID."

    return render(request, 'index.html', {'match_info': match_info, 'output': output})