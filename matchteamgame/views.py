from django.shortcuts import render
from .CurrentMatch4v4 import get_match_info

def my_view(request):
    match_info = {}
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        if profile_id:
            print(f"Profile ID submitted: {profile_id}")
            api_url = f"https://data.aoe2companion.com/api/matches?profile_ids={profile_id}&search=&leaderboard_ids=rm_team&page=1"
            civilizations_file = "matchteamgame/civilizationsnew.json"
            descriptions_url = "https://github.com/SiegeEngineers/aoe2techtree/raw/847a85a575b859d3a31818862483c75b17ec15d4/data/locales/en/strings.json"
            match_info = get_match_info(api_url, civilizations_file, descriptions_url)

    return render(request, 'matchteamgame/tgmatch.html', {'match_info': match_info, 'page_title': "Team Game Matches"})