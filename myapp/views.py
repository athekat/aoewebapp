# from django.shortcuts import render
# import subprocess

# def my_view(request):
#     if request.method == 'POST':
#         # Run the Python script and capture the output
#         output = subprocess.check_output(['python', 'myapp/Aoe-CurrentMatch.py']).decode()

#         # Render the template with the output
#         return render(request, 'index.html', {'output': output})
#     return render(request, 'index.html')


from django.shortcuts import render
from .AoeCurrentMatch import get_match_info

def my_view(request):
    match_info = {}
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        if profile_id:
            api_url = f"https://data.aoe2companion.com/api/matches?profile_ids={profile_id}&search=&leaderboard_ids=rm_1v1&page=1"
            civilizations_file = "myapp/civilizationsnew.json"
            descriptions_url = "https://github.com/SiegeEngineers/aoe2techtree/raw/847a85a575b859d3a31818862483c75b17ec15d4/data/locales/en/strings.json"
            match_info = get_match_info(api_url, civilizations_file, descriptions_url)

    return render(request, 'index.html', {'match_info': match_info})
