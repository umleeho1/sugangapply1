from django.urls import path

from . import views

app_name = 'sugang'

urlpatterns = [
    path('', views.index, name='main'),
    path('save-data/', views.save_URL, name='save_URL'),
    path('show-server-time/<str:saveURL>/', views.show_server_time, name='show_server_time'),
]
