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
            up_speed, down_speed, ping_speed = method.checkSpeed()
            #업링크 다운링크 핑스피드 변수로저장했고 context로뽑아쓰기가능
            #업링크 상위퍼센트 다운링크 상위퍼센트 핑스피드상위퍼센트 저장했고 cotext로쓰면댐
            #총상위 몇퍼인지 나오는건 다운링크속도가 가장 결정에중요하다고 나와서 다운링크 퍼센트로했음
            result = resultInfo.objects.create(
                upSpeed = up_speed,
                downSpeed= down_speed,
                pingSpeed= ping_speed
            )
            down_percentile = method.get_speed_percentile(down_speed)
            result.save()
            print(down_percentile)
            context['result'] = result
            context['speed_ranking'] = down_percentile
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