from django.shortcuts import render
import json
import requests

DESCRIPTIONS_URL = "https://github.com/SiegeEngineers/aoe2techtree/raw/847a85a575b859d3a31818862483c75b17ec15d4/data/locales/en/strings.json"
CIVS_FILE = "matchteamgame/civilizationsnew.json"


def get_civilization_ids(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def get_civilization_descriptions(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch civ descriptions: {response.status_code}")
    except Exception as e:
        print(f"Error fetching civ descriptions: {e}")
    return {}


def get_match_info(api_url, civ_file, desc_url):
    response = requests.get(api_url)
    if response.status_code != 200:
        return {"error": f"API request failed with status code: {response.status_code}"}

    data = response.json()
    matches = data.get('matches', [])

    if not matches:
        return {"error": "No team matches found for this profile ID."}

    match = matches[0]
    map_name = match.get('mapName')
    map_icon = match.get('mapImageUrl')
    teams = match.get('teams', [])

    if not teams or len(teams) < 2:
        return {"error": "Could not extract full player information."}

    civ_ids = get_civilization_ids(civ_file)
    civ_descriptions = get_civilization_descriptions(desc_url)

    team_data = []
    for team in teams:
        players_in_team = []
        for player in team['players']:
            civ_name = player['civName']
            civ_id = civ_ids.get(civ_name)
            civ_description = civ_descriptions.get(str(civ_id), "Description not found.")
            players_in_team.append({
                'name': player['name'],
                'rating': player['rating'],
                'civName': civ_name,
                'colorHex': player['colorHex'],
                'description': civ_description
            })
        team_data.append(players_in_team)

    return {
        'mapName': map_name,
        'mapIcon': map_icon,
        'teams': team_data
    }



def your_django_view(request):
    match_info = ""
    output = ""

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        if profile_id:
            api_url = f"https://data.aoe2companion.com/api/matches?profile_ids={profile_id}&search=&leaderboard_ids=rm_team&page=1"
            match_data = get_match_info(api_url, CIVS_FILE, DESCRIPTIONS_URL)

            if "error" in match_data:
                output = match_data["error"]
            else:
                match_info = match_data
        else:
            output = "Please enter a Profile ID."

    return render(request, 'index.html', {
        'match_info': match_info,
        'output': output
    })
