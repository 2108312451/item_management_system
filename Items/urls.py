from django.urls import path, include
from Items.views import Comment,InboundAndOutbound

urlpatterns = [
    path("comment/",Comment.CommentsView.as_view(),name='comment'),
    path("inboundoutbound/",InboundAndOutbound.ItemOperateView.as_view(),name='inboundoutbound'),
    path("getitemdata/<int:pk>",InboundAndOutbound.GetItemData.as_view(),name='getitemdata'),
    path("delitem/<int:pk>/<int:id>",InboundAndOutbound.DeleteItem.as_view(),name='delitem'),
    path('images/<str:imagename>/', InboundAndOutbound.ImageUrl.as_view(), name='imageurl'),
    path('additemmore/',InboundAndOutbound.MoreAdd.as_view(),name='additemmore')
]