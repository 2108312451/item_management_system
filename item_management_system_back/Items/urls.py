from django.urls import path, include
from Items.views import Comment,InboundAndOutbound

urlpatterns = [
    path("comment/",Comment.CommentsView.as_view(),name='comment'),
    path("inboundoutbound/",InboundAndOutbound.ItemOperateView.as_view(),name='inboundoutbound'),
    path('images/<str:imagename>/', InboundAndOutbound.ImageUrl.as_view(), name='imageurl'),
]