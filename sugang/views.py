import datetime
import time
import ntplib
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
    start_time = time.time()
    context = {}
    if request.method == 'POST':
        if request.POST.get('saveURL') == '':
            return redirect('sugang:main')
        else:
            method.save_URL(request)
            temp = method.show_server_time(method.get_accessurl_by_highest_id())
            context['current_servertime'], context['user_url'] = temp[0], temp[1]
            end_time = time.time()
            run_time = end_time - start_time
            print("Action Runtime : ", str(round(run_time * 1000, 2)))
            return render(request, 'mainpage.html', context)
    else:
        return redirect('sugang:main')

def reload_serverclock(request):
    start_time = time.time()
    target_url = method.get_accessurl_by_highest_id()
    server_time = method.calculate_time(target_url.testURL)
    end_time = time.time()
    run_time = end_time - start_time
    run_time = run_time / 2   # 2RTT가 결국 InternetDelay이기 때문에 실제 서버시간 오차는 1RTT임.
    run_time = round(run_time * 1000, 2)
    print("Load Clock time : ", str(run_time))
    return JsonResponse({'current_servertime':server_time, 'InternetDelay':run_time})

def reload_defaultclock(request):
    start_time = time.time()
    ntp_server = 'time.windows.com'
    client = ntplib.NTPClient()
    response = client.request(ntp_server)
    ntp_time = datetime.datetime.fromtimestamp(response.tx_time)
    formatted_time = ntp_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    end_time = time.time()
    run_time = end_time - start_time
    run_time = run_time / 2   # 2RTT가 결국 InternetDelay이기 때문에 실제 서버시간 오차는 1RTT임.
    run_time = round(run_time * 1000, 2)
    print("Load DefaultClock time : ", str(run_time))
    return JsonResponse({'current_servertime':formatted_time,'InternetDelay':run_time})

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


