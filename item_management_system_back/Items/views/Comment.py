from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Items.models import Comments
from Items.serializers.ItemsDataSerializers import CommentsSerializers
import datetime

# 评论
class CommentsView(APIView):
    def post(self,request):
        if request.data.get('pk') == 0:
            # 获取当前时间
            current_time = datetime.datetime.now()
            # 将时间转换为字符串
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

            commobj = Comments.objects.create(comment_text=request.data.get('comment_text'),comment_username=request.data.get('comment_username'),comment_itemid=request.data.get('comment_itemid'),comment_times=time_str)
            commobj.save()
            return Response({"ok_create": True}, status=status.HTTP_200_OK)
        elif request.data.get('pk') == 1:
            comments = Comments.objects.filter(comment_itemid=request.data.get('id'))
            if comments:
                commentdata = CommentsSerializers(instance=comments, many=True)
                return Response({"commentdata": commentdata.data}, status=status.HTTP_200_OK)
            else:
                return Response({"commentdata": []}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "pk值为空"}, status=status.HTTP_200_OK)
