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

def save_URL(request):
    if request.method == 'POST':
        if request.POST.get('saveURL') == '':
            return redirect('sugang:main')
        else:
            saveURL = accessURL(testURL=request.POST.get('saveURL'))
            saveURL.save()
            #print(saveURL.id)
            #데이터베이스에 사용자가 입력한 URL저장

            return show_server_time(request, saveURL)
            #저장된 saveURL을 가지고 서버시간 표시
    else:
        return redirect('sugang:main')
    
def show_server_time(request, saveURL):
    try:
        responseURL = saveURL.testURL
        serverTime = method.calculate_time(responseURL)
        context = {'current_servertime' : serverTime, 'user_url' : responseURL}
        return render(request, 'mainpage.html', context)
    except:
        return HttpResponse("Could not retrieve server time.")
    
def reload_serverclock(request):
    target_url = method.get_accessurl_by_highest_id()
    server_time = method.calculate_time(target_url.testURL)
    return JsonResponse({'current_servertime':server_time})

def reload_defaultclock(request):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return JsonResponse({'current_servertime':formatted_time})