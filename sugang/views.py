import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
import urllib.request
import urllib.error
import time
import requests
from .functions import method
from django.http import JsonResponse

# Create your views here.

def index(request):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    context = {'current_servertime' : formatted_time}
    return render(request, 'mainpage.html', context)

def action(request):
    context = {'current_servertime' : None, 'user_url': None, 'uplink' : None,
               'downlink': None, 'pingspeed': None}
    if request.method == 'POST':
        if request.POST.get('saveURL') == '':
            return redirect('sugang:main')
        else:
            method.save_URL(request)
            temp = method.show_server_time(method.get_accessurl_by_highest_id())
            context['current_servertime'], context['user_url'] = temp[0], temp[1]
            temp = method.checkSpeed()
            context['uplink'], context['downlink'], context['pingspeed'] = temp[0], temp[1], temp[2]
            
            return render(request, 'mainpage.html', context)
    else:
        return redirect('sugang:main')
        
    return render()

    
'''
    def show_server_time(request, saveURL):
    try:
        targetURL = saveURL.testURL
        serverTime = method.calculate_time(targetURL)
        context = {'current_servertime' : serverTime, 'user_url' : targetURL}
        return render(request, 'mainpage.html', context)
    except:
        return HttpResponse("Could not retrieve server time.")
'''
    
def reload_serverclock(request):
    target_url = method.get_accessurl_by_highest_id()
    server_time = method.calculate_time(target_url.testURL)
    return JsonResponse({'current_servertime':server_time})

def reload_defaultclock(request):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return JsonResponse({'current_servertime':formatted_time})