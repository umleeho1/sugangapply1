from django.db import models

class accessURL(models.Model):
    testURL = models.CharField(max_length = 300)
    #사용자가 접속하고자 하는 URL 주소를 저장할 매개변수

class resultInfo(models.Model):
    toAccessURL = models.ForeignKey(accessURL, on_delete=models.CASCADE)
    #accessURL을 외부키로 받아옴.
    pingSpeed = models.FloatField()
    upSpeed = models.FloatField()
    downSpeed = models.FloatField()
    serverTime = models.TimeField()
    speedRanking = models.IntegerField()

