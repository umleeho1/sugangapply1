import datetime
import time
import ntplib
import ping3
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
    '''
    ntp_server = request.POST.get('targetURL')
    client = ntplib.NTPClient()
    response = client.request(ntp_server)
    ntp_time = datetime.datetime.fromtimestamp(response.tx_time)
    formatted_time = ntp_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    
    '''
    target_url = request.POST.get('targetURL')
    print(target_url)
    server_time = method.calculate_time(target_url)
    end_time = time.time()
    run_time = end_time - start_time
    run_time = run_time / 4   # 2RTT가 결국 InternetDelay이기 때문에 실제 서버시간 오차는 1RTT임.
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
    run_time = run_time / 4   # 2RTT가 결국 InternetDelay이기 때문에 실제 서버시간 오차는 1RTT임.
    run_time = round(run_time * 1000, 2)
    print("Load DefaultClock time : ", str(run_time))
    return JsonResponse({'current_servertime':formatted_time,'InternetDelay':run_time})

def TestUpLink(request):
    upSpeed = method.checkUpLink()
    response = {'upSpeed':upSpeed}
    return JsonResponse(response)

def TestDownLink(request):
    pingSpeed = request.POST.get('pingSpeed')
    try:
        pingSpeed = float(pingSpeed)    # 시도하여 float으로 변환
    except ValueError:
        pingSpeed = 30
    print(pingSpeed)
    
    downSpeed = method.checkDownLink()  # 다운로드속도 확인
    result = resultInfo.objects.create(
        upSpeed = 0,
        downSpeed= downSpeed,
        pingSpeed= 0)
    
    down_percentile = method.get_speed_percentile(downSpeed)    # 다운로드속도 순위 측정
    probability_success, score = method.get_success(down_percentile, pingSpeed, downSpeed)
    down_percentile_str = "상위 {:.2f}%입니다.".format(down_percentile)
    score_str = "종합점수:{:.2f}".format(score)
    result.save()
    response = {'downSpeed':downSpeed, 'speed_ranking':down_percentile_str, 'success':probability_success, 'score':score_str}    
    return JsonResponse(response)

def TestPing(request):
    hostname = 'time.bora.net'
    response_time = round(ping3.ping(hostname) * 1000, 2)
    response = {'pingSpeed':response_time}
    return JsonResponse(response)

def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message_content')
        # Comment 모델을 사용하여 댓글 저장
        print("입력" + message)
        comment = Comment(content=message)
        comment.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
def read_message(request):
    Comment_lists = Comment.objects.order_by('-created_at')[:30]
    Comment_lists_str = ''
    for data in Comment_lists:
        Comment_lists_str += ">>{}<br>".format(data.content)
    response = {'Comment_list':Comment_lists_str}
    return JsonResponse(response)
