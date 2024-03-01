from django.urls import path, include
from Function.views import Notices

urlpatterns = [
    path("notice/",Notices.NoticeView.as_view(),name='notice')
]