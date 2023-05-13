from ..models import accessURL
import urllib.request
import urllib.error
import datetime

def get_accessurl_by_highest_id():
    highest_id = accessURL.objects.order_by('-id').values_list('id', flat=True).first()
    if highest_id is not None:
        highest_id_accessurl = accessURL.objects.get(id=highest_id)
        return highest_id_accessurl
    else:
        return None
    
def calculate_time(targetURL):
    response = urllib.request.urlopen(targetURL).headers['Date']
    datetime_obj = datetime.datetime.strptime(response, "%a, %d %b %Y %H:%M:%S %Z")
    datetime_obj += datetime.timedelta(hours=9)
    # 원하는 형식으로 포맷팅
    formatted_date = datetime_obj.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return formatted_date
    