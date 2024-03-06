from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Function.models import Repairs,Feedback
import datetime
from Function.serializers.RepairAndFeedbackSerializers import RepairsSerializers,FeedbackSerializers

# 报修
class RepairsView(APIView):
    def post(self,request):
        try:
            current_time = datetime.datetime.now()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            Repairsobj = Repairs.objects.create(item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),adress=request.data.get('adress'),username=request.data.get('username'),text=request.data.get('text'),times=time_str)
            Repairsobj.save()
            return Response({"ok_repair":True},status=status.HTTP_200_OK)
        except:
            return Response({"ok_repair":False,"message":"参数有误"},status=status.HTTP_200_OK)

    def get(self,request,username):
        if username == 'all':
            dataS = Repairs.objects.all()
            datas = RepairsSerializers(instance=dataS,many=True)
            return Response({"data":datas.data},status=status.HTTP_200_OK)
        else:
            dataS = Repairs.objects.filter(username=username)
            datas = RepairsSerializers(instance=dataS, many=True)
            return Response({"data": datas.data}, status=status.HTTP_200_OK)

    def put(self,request):
        obj = Repairs.objects.get(id=request.data.get('id'))
        obj.statics = True
        obj.save()
        return Response({"ok": True}, status=status.HTTP_200_OK)

# 反馈
class FeedbackView(APIView):
    def post(self, request):
        try:
            current_time = datetime.datetime.now()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            Feedbackobj = Feedback.objects.create(item_id=request.data.get('item_id'),
                                                item_name=request.data.get('item_name'),
                                                adress=request.data.get('adress'),
                                                username=request.data.get('username'), text=request.data.get('text'),
                                                times=time_str)
            Feedbackobj.save()
            return Response({"ok_feedback": True}, status=status.HTTP_200_OK)
        except:
            return Response({"ok_feedback": False, "message": "参数有误"}, status=status.HTTP_200_OK)

    def get(self, request, username):
        if username == 'all':
            dataS = Feedback.objects.all()
            datas = FeedbackSerializers(instance=dataS, many=True)
            return Response({"data": datas.data}, status=status.HTTP_200_OK)
        else:
            dataS = Feedback.objects.filter(username=username)
            datas = FeedbackSerializers(instance=dataS, many=True)
            return Response({"data": datas.data}, status=status.HTTP_200_OK)

    def put(self, request):
        obj = Feedback.objects.get(id=request.data.get('id'))
        obj.statics = True
        obj.save()
        return Response({"ok": True}, status=status.HTTP_200_OK)