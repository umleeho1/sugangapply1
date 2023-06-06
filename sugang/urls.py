from django.urls import path
from django.contrib import admin


from . import views

app_name = 'sugang'

urlpatterns = [
    path('', views.index, name='main'),
    path('admin/', admin.site.urls, name='admin'),
    path('result/admin/', admin.site.urls),
    path('load_defaultclock/', views.reload_defaultclock, name='defaultclock'),
    path('result/', views.action, name='testURL'),
    path('result/loadclock/', views.reload_serverclock, name='loadclock'),
    path('result/checkUpLink/', views.TestUpLink),
    path('result/checkDownLink/', views.TestDownLink),
    path('result/checkPing/', views.TestPing),
    path('checkUpLink/', views.TestUpLink),
    path('checkDownLink/', views.TestDownLink),
    path('checkPing/', views.TestPing),
]
