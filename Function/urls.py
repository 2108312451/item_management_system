from django.urls import path, include
from Function.views import Notices,Lends,Returns,Collections,RepairAndFeedback,HelpCenters

urlpatterns = [
    path("notice/",Notices.NoticeView.as_view(),name='notice'),
    path("lends/",Lends.LendView.as_view(),name='lend'),
    path("lends/<str:lenduser_realname>",Lends.LendView.as_view(),name='lend'),
    path("approval/",Lends.ApprovalView.as_view(),name='approval'),
    path("getpicture/<str:ges>/<int:id>",Lends.GetPicture.as_view(),name='getpicture'),
    path("uploadimages/",Lends.UploadImages.as_view(),name='uploadimages'),
    path("returnitem/",Returns.ReturnView.as_view(),name='returnitem'),
    path("returnitem/<str:user_realname>",Returns.ReturnView.as_view(),name='returnitem'),
    path("collection/",Collections.CollectionView.as_view(),name='collection'),
    path("collection/<int:id>",Collections.CollectionView.as_view(),name='collection'),
    path("collection/<str:username>",Collections.CollectionView.as_view(),name='collection'),
    #报修
    path("repairs/",RepairAndFeedback.RepairsView.as_view(),name='Repairs'),
    path("repairs/<str:username>",RepairAndFeedback.RepairsView.as_view(),name='Repairs'),
    #反馈
    path("feedback/",RepairAndFeedback.FeedbackView.as_view(),name='Feedback'),
    path("feedback/<str:username>",RepairAndFeedback.FeedbackView.as_view(),name='Feedback'),
#帮助中心
    path("userhelpcenter/",HelpCenters.UserHelpCenterView.as_view(),name='userhelpcenter'),
    path("userhelpcenter/<int:userid>/<str:username>",HelpCenters.UserHelpCenterView.as_view(),name='userhelpcenter'), #获取
    path("userhelpcenter/<int:id>",HelpCenters.UserHelpCenterView.as_view(),name='userhelpcenter'), #记录删除
    path("gettext/<int:id>",HelpCenters.GetText.as_view(),name='gettext'), #获取对话详情
    path("adminhelpcenter/",HelpCenters.AdminHelpCenterView.as_view(),name='adminhelpcenter'), #管理员发送消息
    path("adminhelpcenter/<int:adminid>/<str:adminname>",HelpCenters.AdminHelpCenterView.as_view(),name='adminhelpcenter'),
]