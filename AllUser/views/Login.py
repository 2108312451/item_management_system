from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
import random
from AllUser.models import OrdinaryUser,Regular_Administrator,Super_Administrator,Codes
from AllUser.serializers.UserDataSerializers import OrdinaryUserSerializers,Regular_AdministratorSerializers,Super_AdministratorSerializers

# 登录
# 普通用户
class OrdinaryUserLoginView(APIView):
    def post(self,request):
        # 注册
        if request.data.get('pk') == 0:
            is_exists = OrdinaryUser.objects.filter(username=request.data.get('username')).exists()
            if is_exists:
                return Response({"ok_create": False,"message":"用户名重复"}, status=status.HTTP_200_OK)

            try:
                # 对比邀请码 # 获取表中最后一条数据
                last_record = Codes.objects.last()

                if last_record:
                    pass
                else:
                    return Response({"can_login": False,"message":"邀请码为空"}, status=status.HTTP_200_OK)

                if last_record.Code != request.data.get('code'):
                    return Response({"can_login": False,"message":"邀请码错误"},status=status.HTTP_200_OK)

                user = OrdinaryUser.objects.create(realname = request.data.get('realname'),username = request.data.get('username'),password=make_password('123456'),phone=request.data.get('phone'),group=request.data.get('group'))
                user.save()
                return Response({"ok_create": True}, status=status.HTTP_200_OK)
            except:
                return Response({"ok_create": False,"message":"注册失败"}, status=status.HTTP_200_OK)
        # 登录
        elif request.data.get('pk') == 1:
            user = OrdinaryUser.objects.get(username=request.data.get('username'))
            is_matched = check_password(request.data.get('password'), user.password)
            if is_matched:
                userdata = OrdinaryUserSerializers(instance=user,many=False)
                return Response({"can_login": True,'userdata':userdata.data}, status=status.HTTP_200_OK)
            else:
                return Response({"can_login": False, "message": "密码错误"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "pk值为空"}, status=status.HTTP_200_OK)

# 验证码(x)
class CodesView(APIView):
    def get(self,request):
        # 生成一个 6 位的随机整数
        random_number = random.randrange(100000, 999999)
        code = Codes.objects.create(Code=random_number)
        code.save()
        return Response({"ok_code":True}, status=status.HTTP_200_OK)

# 管理员
class Regular_AdministratorLoginView(APIView):
    def post(self, request):
        # 注册
        if request.data.get('pk') == 0:
            is_exists = Regular_Administrator.objects.filter(username=request.data.get('username')).exists()
            if is_exists:
                return Response({"ok_create": False, "message": "用户名重复"}, status=status.HTTP_200_OK)
            try:
                user = Regular_Administrator.objects.create(realname=request.data.get('realname'),
                                                   username=request.data.get('username'),
                                                   password=make_password('123456'), phone=request.data.get('phone'))
                user.save()
                return Response({"ok_create": True}, status=status.HTTP_200_OK)
            except:
                return Response({"ok_create": False, "message": "注册失败"}, status=status.HTTP_200_OK)
        # 登录
        elif request.data.get('pk') == 1:
            user = Regular_Administrator.objects.get(username=request.data.get('username'))
            is_matched = check_password(request.data.get('password'), user.password)
            if is_matched:
                userdata = Regular_AdministratorSerializers(instance=user, many=False)
                return Response({"can_login": True,"userdata":userdata.data}, status=status.HTTP_200_OK)
            else:
                return Response({"can_login": False, "message": "密码错误"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "pk值为空"}, status=status.HTTP_200_OK)

# 超管
class Super_AdministratorLoginView(APIView):
    def post(self,request):
        user = User.objects.get(username=request.data.get('username'))
        is_matched = check_password(request.data.get('password'), user.password)
        if is_matched:
            # 创建
            is_exists = Super_Administrator.objects.filter(username=request.data.get('username')).exists()
            if is_exists:
                pass
            else:
                superuser = Super_Administrator.objects.create(username=request.data.get('username'),
                                                               password=make_password(request.data.get('password')))
                superuser.save()
            user = Super_Administrator.objects.get(username=request.data.get('username'))
            userdata = Super_AdministratorSerializers(instance=user, many=False)
            return Response({"can_login": True,"userdata":userdata.data}, status=status.HTTP_200_OK)
        else:
            return Response({"can_login": False, "message": "密码错误"}, status=status.HTTP_200_OK)