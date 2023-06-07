import datetime

response = "Tue, 31 May 2023 12:00:00 GMT"
datetime_obj = datetime.datetime.strptime(response, "%a, %d %b %Y %H:%M:%S %Z")

hour = datetime_obj.hour
minute = datetime_obj.minute
second = datetime_obj.second

hour_int = int(hour)
minute_int = int(minute)
second_int = int(second)

print(hour_int, minute_int, second_int)
