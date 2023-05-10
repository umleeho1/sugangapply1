from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'mainpage.html')

        
def save_URL(request):
    if request.method == 'POST':
        
        saveURL = accessURL(testURL = request.POST.get('saveURL'))
        saveURL.save()
        
        return redirect('sugang:main')
    else:
        return render(request, 'my_template.html')