from django.urls import path, include
from Function.views import Notices,Lends

urlpatterns = [
    path("notice/",Notices.NoticeView.as_view(),name='notice'),
    path("lends/",Lends.LendView.as_view(),name='lend'),
    path("approval/",Lends.ApprovalView.as_view(),name='approval'),
    path("getpicture/",Lends.GetPicture.as_view(),name='getpicture'),
    path("uploadimages/",Lends.UploadImages.as_view(),name='uploadimages'),
]