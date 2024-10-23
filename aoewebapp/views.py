from django.shortcuts import render
import subprocess

def my_view(request):
    if request.method == 'POST':
        # Run the Python script
        subprocess.run(['python', 'fetch_info.py'])
        # Fetch the output from the script (if needed)
        # output = subprocess.check_output(['python', 'Aoe-CurrentMatch.py'])
        # Process the output as needed

    return render(request, 'myapp/index.html')