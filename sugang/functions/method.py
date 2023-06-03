from ..models import accessURL
import urllib.request
import urllib.error
import datetime
from ..views import * 
import speedtest_cli
import numpy as np
import math

def get_accessurl_by_highest_id():
    highest_id = accessURL.objects.order_by('-id').values_list('id', flat=True).first()
    if highest_id is not None:
        highest_id_accessurl = accessURL.objects.get(id=highest_id)
        return highest_id_accessurl
    else:
        return None
    
def calculate_time(targetURL):  #targetURL 은 URLtype
    response = urllib.request.urlopen(targetURL).headers['Date']
    print(response)
    datetime_obj = datetime.datetime.strptime(response, "%a, %d %b %Y %H:%M:%S %Z")
    datetime_obj += datetime.timedelta(hours=9)
    # 원하는 형식으로 포맷팅
    formatted_date = datetime_obj.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return formatted_date
    
def save_URL(request):
    testURL = request.POST.get('saveURL')
    if not testURL.startswith('https://'):
        testURL = 'https://' + testURL
    saveURL = accessURL(testURL=testURL)
    saveURL.save()


def show_server_time(saveURL):
    try:
        targetURL = saveURL.testURL
        serverTime = calculate_time(targetURL)
        print(serverTime, targetURL)
        return serverTime, targetURL
    except:
        return HttpResponse("Could not retrieve server time.")

def checkSpeed():
    st = speedtest_cli.Speedtest()
    st.get_best_server()
    up_speed = round(st.upload() / 1000000 , 2)
    down_speed = round(st.download() / 1000000 , 2)
    ping_speed = st.results.ping
    return up_speed, down_speed, ping_speed
    
def get_speed_percentile(down_speed):
    # 데이터베이스에 저장된 다운로드 속도 데이터를 가져옵니다.
    speed_data = resultInfo.objects.all().values_list('downSpeed')
    speed_data = [item[0] for item in speed_data]

    # 속도 데이터가 존재하지 않으면 0을 반환합니다.
    if not speed_data:
        return 0

    # 속도 데이터가 존재할 경우 각 속도에 대한 순위를 계산하고, down_speed의 순위를 구합니다.
    rank = sum(down_speed > s for s in speed_data)
    percentile = round(rank / len(speed_data) * 100, 2)
    percentile = round(100 - percentile, 2)
    
    return percentile

def checkUpLink():
    st = speedtest_cli.Speedtest()
    st.get_best_server()
    up_speed = round(st.upload() / 1000000 , 2)
    return up_speed

def checkDownLink():
    st = speedtest_cli.Speedtest()
    st.get_best_server()
    down_speed = round(st.download() / 1000000 , 2)
    return down_speed

def checkPing():
    st = speedtest_cli.Speedtest()
    st.get_best_server()
    return round(st.results.ping, 1)


def  get_success(downPercentile, pingSpeed, downSpeed):
    # 데이터베이스에 저장된 다운로드 속도 데이터를 가져옵니다.
    success = ''
    score = 100
    score = round(100-downPercentile, 2)
    
    if(pingSpeed <= 10):
        score += 10
    elif(pingSpeed <= 20):
        score += 5
    elif(pingSpeed <= 35):
        score += 0
    elif(pingSpeed <= 50):
        score -= 10
    elif(pingSpeed >= 80):
        score -= 18
    else:
        score -= 30
        
    if downSpeed >= 10:
        score += (10 + round(math.log(downSpeed, 3), 2))
    elif downSpeed >= 5:
        score += round(math.log10(downSpeed, 3), 2)
    elif downSpeed >= 2:
        score += 0
    elif downSpeed <= 1:
        score -= 5
        
    if score >= 90:
        success = '매우높음'
    elif score >= 75:
        success = '상당히 높음'
    elif (score >=60 and score <75):
        success = '양호함'
    elif (score >=40 and score <60):
        success = '보통'
    elif (score >=20 and score <40):
        success = '낮음'
    elif (score >=5 and score < 20):
        success = '현저히 낮음'
    else:
        success ='매우 낮음'
        
    if downSpeed < 0.5 :
        success = '측정 오류입니다.'
    
    return success, score
