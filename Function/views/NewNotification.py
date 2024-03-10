from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Function.models import NewNotifications,OrNews
from Function.serializers.NewNotificationSerializers import NewNotificationSerializers

# 即将到期物品排查
class Cheacks(APIView):
    def post(self,request):
        pass

#通知
class NewNotificationView(APIView):
    def get(self,request,username):
        datas = NewNotifications.objects.filter(notname=username)
        if datas.filter(oread=False).exists():
            return Response({"read":True},status=status.HTTP_200_OK)
        else:
            return Response({"read":False},status=status.HTTP_200_OK)

    def post(self,request):
        try:
            username = request.data.get('username')
            datas = NewNotifications.objects.filter(notname=username)
            data = NewNotificationSerializers(instance=datas,many=True)
            for data in datas:
                data.oread = True
            datas.save()
            return Response({"data":data.data},status=status.HTTP_200_OK)
        except:
            return Response({"message": "用户姓名不存在"}, status=status.HTTP_200_OK)
