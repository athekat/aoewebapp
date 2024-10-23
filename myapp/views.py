from django.shortcuts import render

from django.shortcuts import render
import subprocess

def my_view(request):
    if request.method == 'POST':
        # Run the Python script and capture the output
        output = subprocess.check_output(['python', 'myapp/Aoe-CurrentMatch.py']).decode()

        # Render the template with the output
        return render(request, 'index.html', {'output': output})

    return render(request, 'index.html')