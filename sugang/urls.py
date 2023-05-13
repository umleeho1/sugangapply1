from django.urls import path

from . import views

app_name = 'sugang'

urlpatterns = [
    path('', views.index, name='main'),
    path('result/', views.save_URL, name='testURL'),
    path('result/loadclock/', views.reload_serverclock, name='loadclock'),
]
