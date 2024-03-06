from django.urls import path, include
from Function.views import Notices,Lends,Returns

urlpatterns = [
    path("notice/",Notices.NoticeView.as_view(),name='notice'),
    path("lends/",Lends.LendView.as_view(),name='lend'),
    path("lends/<str:lenduser_realname>",Lends.LendView.as_view(),name='lend'),
    path("approval/",Lends.ApprovalView.as_view(),name='approval'),
    path("getpicture/<str:ges>/<int:id>",Lends.GetPicture.as_view(),name='getpicture'),
    path("uploadimages/",Lends.UploadImages.as_view(),name='uploadimages'),
    path("returnitem/",Returns.ReturnView.as_view(),name='returnitem'),
    path("returnitem/<str:user_realname>",Returns.ReturnView.as_view(),name='returnitem'),
]