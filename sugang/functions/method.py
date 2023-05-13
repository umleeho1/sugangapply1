from ..models import accessURL
import urllib.request
import urllib.error
import datetime
from ..views import * 
import speedtest_cli

def get_accessurl_by_highest_id():
    highest_id = accessURL.objects.order_by('-id').values_list('id', flat=True).first()
    if highest_id is not None:
        highest_id_accessurl = accessURL.objects.get(id=highest_id)
        return highest_id_accessurl
    else:
        return None
    
def calculate_time(targetURL):  #targetURL 은 URLtype
    response = urllib.request.urlopen(targetURL).headers['Date']
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
    
    
    