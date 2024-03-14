from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
import random
import datetime
from datetime import timedelta
from AllUser.models import OrdinaryUser,Regular_Administrator,Super_Administrator,Codes
from AllUser.serializers.UserDataSerializers import OrdinaryUserSerializers,Regular_AdministratorSerializers,Super_AdministratorSerializers
from Function.models import Lend,NewNotifications,EquipmentTimes

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

                user = OrdinaryUser.objects.create(realname=request.data.get('realname'),
                                                   username=request.data.get('username'),
                                                   password=make_password(request.data.get('password')),
                                                   phone=request.data.get('phone'), group=request.data.get('group'))
                user.save()
                return Response({"ok_create": True}, status=status.HTTP_200_OK)
            except:
                return Response({"ok_create": False,"message":"注册失败"}, status=status.HTTP_200_OK)
        # 登录
        elif request.data.get('pk') == 1:
            try:
                user = OrdinaryUser.objects.get(username=request.data.get('username'))
            except:
                return Response({"can_login": False, "message": "用户名错误"}, status=status.HTTP_200_OK)
            is_matched = check_password(request.data.get('password'), user.password)
            if is_matched:
                if user.status == False:
                    return Response({"can_login": False, "message": "账号禁止登录"}, status=status.HTTP_200_OK)

                userdata = OrdinaryUserSerializers(instance=user,many=False)
                # 用户验证成功，生成 JWT 令牌
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # 验证物品过期通知
                user = OrdinaryUser.objects.get(username=request.data.get('username'))
                realname = user.realname
                userlendatas = Lend.objects.filter(lenduser_realname=realname)
                userequipmentatas = EquipmentTimes.objects.filter(username=realname)
                current_time = datetime.datetime.now()
                time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

                # 验证设备过期通知
                for data in userequipmentatas:
                    time_objs = datetime.datetime.strptime(data.begintime, '%Y-%m-%d %H:%M:%S')
                    hours_to_add = data.longtime
                    new_time_add = time_objs + datetime.timedelta(hours=hours_to_add)
                    new_time_add_str = new_time_add.strftime('%Y-%m-%d %H:%M:%S')

                    # 将时间字符串转换为datetime对象
                    time_obj1 = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    time_obj2 = datetime.datetime.strptime(new_time_add_str, '%Y-%m-%d %H:%M:%S')

                    time_difference = time_obj2 - time_obj1
                    # 将时间差转换为小时数
                    hours_difference = time_difference.total_seconds() / 3600

                    if hours_difference <= 0:
                        pass
                    elif 0 < hours_difference < 1:
                        obj = NewNotifications.objects.create(
                            content=f"您的提交的{data.username}借用申请即将到期，请按时归还物品",
                            times=time_str, notname=data.username)
                        obj.save()

                for lend_data in userlendatas:
                    time_objs = datetime.datetime.strptime(lend_data.lendtime, '%Y-%m-%d %H:%M:%S')
                    delta = timedelta(days=lend_data.lendday)
                    new_time = time_objs + delta
                    new_time_str = new_time.strftime('%Y-%m-%d %H:%M:%S')
                    if new_time_str == time_str:
                        obj = NewNotifications.objects.create(
                            content=f"您的提交的{lend_data.lenditem_name}借用申请即将到期，请按时归还物品",
                            times=time_str, notname=lend_data.lenduser_realname)
                        obj.save()
                return Response({"can_login": True,'token': access_token,'userdata':userdata.data}, status=status.HTTP_200_OK)
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
            try:
                user = Regular_Administrator.objects.get(username=request.data.get('username'))
            except:
                return Response({"can_login": False, "message": "用户名错误"}, status=status.HTTP_200_OK)
            is_matched = check_password(request.data.get('password'), user.password)
            if is_matched:
                if user.status == False:
                    return Response({"can_login": False, "message": "账号禁止登录"}, status=status.HTTP_200_OK)
                userdata = Regular_AdministratorSerializers(instance=user, many=False)
                # 用户验证成功，生成 JWT 令牌
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # 验证物品过期通知
                user = Regular_Administrator.objects.get(username=request.data.get('username'))
                realname = user.realname
                userlendatas = Lend.objects.filter(lenduser_realname=realname)
                userequipmentatas = EquipmentTimes.objects.filter(username=realname)
                current_time = datetime.datetime.now()
                time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

                # 验证设备过期通知
                for data in userequipmentatas:
                    time_objs = datetime.datetime.strptime(data.begintime, '%Y-%m-%d %H:%M:%S')
                    hours_to_add = data.longtime
                    new_time_add = time_objs + datetime.timedelta(hours=hours_to_add)
                    new_time_add_str = new_time_add.strftime('%Y-%m-%d %H:%M:%S')

                    # 将时间字符串转换为datetime对象
                    time_obj1 = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    time_obj2 = datetime.datetime.strptime(new_time_add_str, '%Y-%m-%d %H:%M:%S')

                    time_difference = time_obj2 - time_obj1
                    # 将时间差转换为小时数
                    hours_difference = time_difference.total_seconds() / 3600

                    if hours_difference <= 0:
                        pass
                    elif 0 < hours_difference < 1:
                        obj = NewNotifications.objects.create(
                            content=f"您的提交的{data.username}借用申请即将到期，请按时归还物品",
                            times=time_str, notname=data.username)
                        obj.save()

                for lend_data in userlendatas:
                    time_objs = datetime.datetime.strptime(lend_data.lendtime, '%Y-%m-%d %H:%M:%S')
                    delta = timedelta(days=lend_data.lendday)
                    new_time = time_objs + delta
                    new_time_str = new_time.strftime('%Y-%m-%d %H:%M:%S')
                    if new_time_str == time_str:
                        obj = NewNotifications.objects.create(
                            content=f"您的提交的{lend_data.lenditem_name}借用申请即将到期，请按时归还物品",
                            times=time_str, notname=lend_data.lenduser_realname)
                        obj.save()

                return Response({"can_login": True,'token': access_token,"userdata":userdata.data}, status=status.HTTP_200_OK)
            else:
                return Response({"can_login": False, "message": "密码错误"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "pk值为空"}, status=status.HTTP_200_OK)

# 超管
class Super_AdministratorLoginView(APIView):
    def post(self,request):
        try:
            user = User.objects.get(username=request.data.get('username'))
        except:
            return Response({"can_login": False, "message": "用户名错误"}, status=status.HTTP_200_OK)
        is_matched = check_password(request.data.get('password'), user.password)
        if is_matched:
            if user.is_active == False:
                return Response({"can_login": False, "message": "账号禁止登录"}, status=status.HTTP_200_OK)
            # 创建
            is_exists = Super_Administrator.objects.filter(username=request.data.get('username')).exists()
            if is_exists:
                pass
            else:
                superuser = Super_Administrator.objects.create(username=request.data.get('username'),
                                                               password=make_password(request.data.get('password')),authid=user.id)
                superuser.save()
            user = Super_Administrator.objects.get(username=request.data.get('username'))
            userdata = Super_AdministratorSerializers(instance=user, many=False)
            # 用户验证成功，生成 JWT 令牌
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # 验证物品过期通知
            user = Super_Administrator.objects.get(username=request.data.get('username'))
            realname = user.realname
            userlendatas = Lend.objects.filter(lenduser_realname=realname)
            userequipmentatas = EquipmentTimes.objects.filter(username=realname)
            current_time = datetime.datetime.now()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

            # 验证设备过期通知
            for data in userequipmentatas:
                time_objs = datetime.datetime.strptime(data.begintime, '%Y-%m-%d %H:%M:%S')
                hours_to_add = data.longtime
                new_time_add = time_objs + datetime.timedelta(hours=hours_to_add)
                new_time_add_str = new_time_add.strftime('%Y-%m-%d %H:%M:%S')

                # 将时间字符串转换为datetime对象
                time_obj1 = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                time_obj2 = datetime.datetime.strptime(new_time_add_str, '%Y-%m-%d %H:%M:%S')

                time_difference = time_obj2 - time_obj1
                # 将时间差转换为小时数
                hours_difference = time_difference.total_seconds() / 3600

                if hours_difference <= 0:
                    pass
                elif 0 < hours_difference < 1:
                    obj = NewNotifications.objects.create(
                        content=f"您的提交的{data.username}借用申请即将到期，请按时归还物品",
                        times=time_str, notname=data.username)
                    obj.save()

            for lend_data in userlendatas:
                time_objs = datetime.datetime.strptime(lend_data.lendtime, '%Y-%m-%d %H:%M:%S')
                delta = timedelta(days=lend_data.lendday)
                new_time = time_objs + delta
                new_time_str = new_time.strftime('%Y-%m-%d %H:%M:%S')
                if new_time_str == time_str:
                    obj = NewNotifications.objects.create(
                        content=f"您的提交的{lend_data.lenditem_name}借用申请即将到期，请按时归还物品",
                        times=time_str, notname=lend_data.lenduser_realname)
                    obj.save()

            return Response({"can_login": True,'token': access_token,"userdata":userdata.data}, status=status.HTTP_200_OK)
        else:
            return Response({"can_login": False, "message": "密码错误"}, status=status.HTTP_200_OK)