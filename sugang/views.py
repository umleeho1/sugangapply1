from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
import requests

# Create your views here.

def index(request):
    return render(request, 'mainpage.html')


'''       
def save_URL(request):
    if request.method == 'POST':
        if(request.POST.get('saveURL') == ''):
            return redirect('sugang:main')
        else:
            saveURL = accessURL(testURL = request.POST.get('saveURL'))
            saveURL.save()
            return redirect('sugang:main')
    
def show_server_time(request, saveURL):
    try:
        response = requests.get(saveURL)
        server_time = response.headers['date']
        return HttpResponse(f"Server time: {server_time}")
    except:
        return HttpResponse("Could not retrieve server time.")  
'''
def save_URL(request):
    if request.method == 'POST':
        if request.POST.get('saveURL') == '':
            return redirect('sugang:main')
        else:
            saveURL = accessURL(testURL=request.POST.get('saveURL'))
            saveURL.save()
            
            # 서버 시간 가져오기
            try:
                response = requests.get(request.POST.get('saveURL'))
                server_time = response.headers['date']
                return HttpResponse(f"Server time: {server_time}")
            except:
                return HttpResponse("Could not retrieve server time.")
    else:
        return redirect('sugang:main')