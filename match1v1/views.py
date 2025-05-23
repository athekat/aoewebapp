from django.shortcuts import render
from .CurrentMatch1v1 import get_match_info

def my_view(request):
    match_info = {}
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        if profile_id:
            print(f"Profile ID submitted: {profile_id}")
            api_url = f"https://data.aoe2companion.com/api/matches?profile_ids={profile_id}&search=&leaderboard_ids=rm_1v1&page=1"
            civilizations_file = "match1v1/civilizationsnew.json"
            descriptions_url = "https://github.com/SiegeEngineers/aoe2techtree/raw/847a85a575b859d3a31818862483c75b17ec15d4/data/locales/en/strings.json"
            match_info = get_match_info(api_url, civilizations_file, descriptions_url)

    return render(request, 'match1v1/ramatch.html', {'match_info': match_info, 'page_title': "1v1 Matches"})