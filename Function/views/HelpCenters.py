import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Function.models import HelpCenterContent,HelpCenterSave
from Function.serializers.HelpCenterSerializers import HelpCenterContentSerializers,HelpCenterSaveSerializers

# 用户帮助中心
class UserHelpCenterView(APIView):
    #用户对话
    def post(self,request):
        # 创建新对话
        if request.data.get('pk') == 0:
            current_time = datetime.datetime.now()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            obj = HelpCenterSave.objects.create(firsttext=request.data.get('text'),userid=request.data.get('userid'),username=request.data.get('username'),times=time_str)
            obj.save()
            objs = HelpCenterContent.objects.create(text=request.data.get('text'),identity='用户',times=time_str,HelpCenterid=obj.id)
            objs.save()
            return Response({"ok":True,"talkid":obj.id},status=status.HTTP_200_OK)
        # 继续历史对话
        elif request.data.get('pk') == 1:
            current_time = datetime.datetime.now()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            obj = HelpCenterContent.objects.create(text=request.data.get('text'),identity='用户',times=time_str,HelpCenterid=request.data.get('talkid'))
            obj.save()
            return Response({"ok": True}, status=status.HTTP_200_OK)
    # 结束对话
    def put(self,request):
        obj = HelpCenterSave.objects.get(id=request.data.get('talkid'))
        obj.statics = True
        obj.save()
        return Response({"ok": True}, status=status.HTTP_200_OK)
    # 用户获取历史对话记录
    def get(self,request,userid,username):
        datas = HelpCenterSave.objects.filter(userid=userid,username=username)
        olddata = HelpCenterSaveSerializers(instance=datas,many=True)
        return Response({"data":olddata.data},status=status.HTTP_200_OK)
    # 删除历史对话
    def delete(self,request,id):
        obj = HelpCenterSave.objects.get(id=id)
        obj.userid = 0
        obj.username = ''
        obj.save()
        return Response({"ok": True}, status=status.HTTP_200_OK)

# 获取某段对话详细内容
class GetText(APIView):
    def get(self,request,id):
        data = HelpCenterContent.objects.filter(HelpCenterid=id)
        datas = HelpCenterContentSerializers(instance=data,many=True)
        return Response({"data": datas.data}, status=status.HTTP_200_OK)

# 管理员帮助中心
class AdminHelpCenterView(APIView):
    def get(self,request,adminid,adminname):
        # 没有回复的用户对话
        nulldata = HelpCenterSave.objects.filter(handleadminid=0,handleadmin='')
        data = HelpCenterSaveSerializers(instance=nulldata,many=True)
        # 历史回复
        olddata = HelpCenterSave.objects.filter(handleadminid=adminid,handleadmin=adminname)
        datas = HelpCenterSaveSerializers(instance=olddata,many=True)
        return Response({"nulldata":data.data,"olddata":datas.data},status=status.HTTP_200_OK)
    def post(self,request):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        obj = HelpCenterContent.objects.create(text=request.data.get('text'), identity='管理员', times=time_str,
                                               HelpCenterid=request.data.get('talkid'))
        obj.save()
        objs = HelpCenterSave.objects.get(id=request.data.get('talkid'))
        objs.handleadminid = request.data.get('handleadminid')
        objs.handleadmin = request.data.get('handleadmin')
        objs.save()
        return Response({"ok": True}, status=status.HTTP_200_OK)
    def delete(self,request,id):
        obj = HelpCenterSave.objects.get(id=id)
        obj.handleadminid = 0
        obj.handleadmin = ''
        obj.save()
        return Response({"ok": True}, status=status.HTTP_200_OK)