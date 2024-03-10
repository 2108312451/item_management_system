from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from AllUser.models import OrdinaryUser,Regular_Administrator
from Function.models import Notice,NewNotifications
from Function.serializers.NoticeSerializers import NoticeSerializers

# 公告
class NoticeView(APIView):
    def get(self,request,username):
        datas = Notice.objects.filter(ns=username)
        if datas.filter(oread=False).exists():
            return Response({"read":True},status=status.HTTP_200_OK)
        else:
            return Response({"read":False},status=status.HTTP_200_OK)

    def post(self,request):
        # 发布
        if request.data.get('pk') == 0:
            current_time = datetime.datetime.now()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

            # 新建通知
            # 获取OrdinaryUser表里面所有数据的realname字段
            realnames = OrdinaryUser.objects.values_list('realname', flat=True)
            for name in realnames:
                obj = NewNotifications.objects.create(content="有新的公告发布，注意查看",times=time_str,notname=name)
                obj.save()
                # 新建公告
                objs = Notice.objects.create(content=request.data.get('content'),
                                             adminname=request.data.get('adminname'), times=time_str,ns=name)
                objs.save()
            realnamees = Regular_Administrator.objects.values_list('realname', flat=True)
            for name in realnamees:
                obj = NewNotifications.objects.create(content="有新的公告发布，注意查看", times=time_str, notname=name)
                obj.save()
                # 新建公告
                objs = Notice.objects.create(content=request.data.get('content'),
                                             adminname=request.data.get('adminname'), times=time_str, ns=name)
                objs.save()

            return Response({"ok_create": True}, status=status.HTTP_200_OK)
        # 获取
        elif request.data.get('pk') == 1:
            username = request.data.get('username')
            obj = Notice.objects.filter(ns=username)
            noticedata = NoticeSerializers(instance=obj,many=True)
            for da in obj:
                da.oread = True
                da.save()
            obj.save()
            return Response({"noticedata":noticedata.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "pk值为空"}, status=status.HTTP_200_OK)