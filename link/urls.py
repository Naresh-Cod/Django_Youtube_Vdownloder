from django.urls import path
from link.views import *
app_name = 'LIN'

urlpatterns = [
    path('', welcome),
    path('video_download/', show_cli_b, name='show_video'),
    path('download/<resolution>/', done_dow_ur, name='file'),
]
