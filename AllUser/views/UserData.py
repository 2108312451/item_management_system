from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from AllUser.models import OrdinaryUser,Regular_Administrator,Super_Administrator
from AllUser.serializers.UserDataSerializers import OrdinaryUserSerializers,Regular_AdministratorSerializers,Super_AdministratorSerializers

# 普通用户
class OrdinaryUsers(APIView):
    def get(self,request,id):
        if id == 0:
            obj = OrdinaryUser.objects.all()
            data = OrdinaryUserSerializers(instance=obj, many=True)
            return Response({"userdata": data.data}, status=status.HTTP_200_OK)
        else:
            obj = OrdinaryUser.objects.get(id=id)
            data = OrdinaryUserSerializers(instance=obj,many=False)
            return Response({"userdata":data.data},status=status.HTTP_200_OK)
    def put(self,request):
        user = OrdinaryUser.objects.get(id=request.data.get('id'))
        user.realname = request.data.get('realname')
        user.username = request.data.get('username')
        user.password = make_password(request.data.get('password'))
        user.phone = request.data.get('phone')
        user.group = request.data.get('group')
        user.status = request.data.get('status')
        user.save()
        return Response({"ok_modify": True}, status=status.HTTP_200_OK)
    def delete(self,request,id):
        try:
            user = OrdinaryUser.objects.get(id=id)
        except:
            return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
        user.delete()
        return Response({"ok_del": True}, status=status.HTTP_200_OK)

# 普通管理员
class RegularAdministrator(APIView):
    def get(self,request,id):
        if id == 0:
            try:
                obj = Regular_Administrator.objects.all()
            except:
                return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
            data = Regular_AdministratorSerializers(instance=obj,many=True)
            return Response({"userdata":data.data},status=status.HTTP_200_OK)
        else:
            try:
                obj = Regular_Administrator.objects.get(id=id)
            except:
                return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
            data = Regular_AdministratorSerializers(instance=obj,many=False)
            return Response({"userdata":data.data},status=status.HTTP_200_OK)
    def put(self,request):
        try:
            user = Regular_Administrator.objects.get(id=request.data.get('id'))
        except:
            return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
        user.realname = request.data.get('realname')
        user.username = request.data.get('username')
        user.password = make_password(request.data.get('password'))
        user.phone = request.data.get('phone')
        user.status = request.data.get('status')
        user.save()
        return Response({"ok_modify": True}, status=status.HTTP_200_OK)
    def delete(self,request,id):
        try:
            user = Regular_Administrator.objects.get(id=id)
        except:
            return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
        user.delete()
        return Response({"ok_del": True}, status=status.HTTP_200_OK)

# 超管
class SuperAdministrator(APIView):
    def get(self,request,id):
        if id == 0:
            try:
                obj = Super_Administrator.objects.all()
            except:
                return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
            data = Super_AdministratorSerializers(instance=obj,many=True)
            return Response({"userdata":data.data},status=status.HTTP_200_OK)
        else:
            try:
                obj = Super_Administrator.objects.get(id=id)
            except:
                return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
            data = Super_AdministratorSerializers(instance=obj,many=False)
            return Response({"userdata":data.data},status=status.HTTP_200_OK)
    def put(self,request):
        try:
            user = Super_Administrator.objects.get(id=request.data.get('id'))
            authuser = User.objects.get(id=user.authid)
        except:
            return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
        user.realname = request.data.get('realname')
        user.username = request.data.get('username')
        authuser.username = request.data.get('username')
        user.password = make_password(request.data.get('password'))
        authuser.password = make_password(request.data.get('password'))
        user.phone = request.data.get('phone')
        user.status = request.data.get('status')
        authuser.is_active = request.data.get('status')
        user.save()
        authuser.save()
        return Response({"ok_modify": True}, status=status.HTTP_200_OK)
    def delete(self,request,id):
        try:
            user = Super_Administrator.objects.get(id=id)
            authuser = User.objects.get(id=user.authid)
        except:
            return Response({"can_login": False, "message": "用户不存在"}, status=status.HTTP_200_OK)
        authuser.delete()
        user.delete()
        return Response({"ok_del": True}, status=status.HTTP_200_OK)