import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .functions import method
from django.http import JsonResponse

# Create your views here.

def index(request):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    context = {'current_servertime' : formatted_time}
    return render(request, 'mainpage.html', context)

def action(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('saveURL') == '':
            return redirect('sugang:main')
        else:
            method.save_URL(request)
            temp = method.show_server_time(method.get_accessurl_by_highest_id())
            context['current_servertime'], context['user_url'] = temp[0], temp[1]
            return render(request, 'mainpage.html', context)
    else:
        return redirect('sugang:main')

def reload_serverclock(request):
    target_url = method.get_accessurl_by_highest_id()
    server_time = method.calculate_time(target_url.testURL)
    return JsonResponse({'current_servertime':server_time})

def reload_defaultclock(request):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return JsonResponse({'current_servertime':formatted_time})

def TestUpLink(request):
    upSpeed = method.checkUpLink()
    response = {'upSpeed':upSpeed}
    return JsonResponse(response)

def TestDownLink(request):
    downSpeed = method.checkDownLink()
    result = resultInfo.objects.create(
        upSpeed = 0,
        downSpeed= downSpeed,
        pingSpeed= 0)
    down_percentile = method.get_speed_percentile(downSpeed)
    result.save()
    response = {'downSpeed':downSpeed, 'speed_ranking':down_percentile}    
    return JsonResponse(response)

def TestPing(request):
    pingSpeed = method.checkPing()
    response = {'pingSpeed':pingSpeed}
    return JsonResponse(response)


