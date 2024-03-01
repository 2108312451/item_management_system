from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from Function.models import Notice
from Function.serializers.NoticeSerializers import NoticeSerializers

# 公告
class NoticeView(APIView):
    def post(self,request):
        if request.data.get('pk') == 0:
            # 获取当前时间
            current_time = datetime.datetime.now()
            # 将时间转换为字符串
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            obj = Notice.objects.create(content=request.data.get('content'),adminname=request.data.get('adminname'),times=time_str)
            obj.save()
            return Response({"ok_create": True}, status=status.HTTP_200_OK)
        elif request.data.get('pk') == 1:
            obj = Notice.objects.all()
            noticedata = NoticeSerializers(instance=obj,many=True)
            return Response({"noticedata":noticedata.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "pk值为空"}, status=status.HTTP_200_OK)
