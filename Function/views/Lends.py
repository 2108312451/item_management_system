from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
from Function.models import Lend,Approval
from Function.serializers.LendSerializers import LendSerializers,ApprovalSerializers

# 借用
class LendView(APIView):
    # 提交借用
    def post(self,request):
        # 借用
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        # 物品等级判断，1级直接上传图片
        if request.data.get('lenditem_grade') == '1':
            lend = Lend.objects.create(lenduser_realname=request.data.get('lenduser_realname'),
                                       lenditem_id=request.data.get('lenditem_id'),
                                       lenditem_name=request.data.get('lenditem_name'),
                                       lendnumber=request.data.get('lendnumber'),
                                       lenditem_grade=request.data.get('lenditem_grade'), lendtime=time_str,
                                       lendday=request.data.get('lendday'),approval_progress='100%')
            lend.save()

            # 获取图片数据
            image_data = request.data.get('image')
            # 将图片数据转换为文件对象
            image_file = ContentFile(image_data.read())
            # 保存图片文件到磁盘上的指定路径（比如 static/images 文件夹）
            default_storage.save('static/images/' + str(lend.id) + '_lend.jpg', image_file)

            #审批
            approval = Approval.objects.create(
                lenduser_realname=lend.lenduser_realname,
                lenditem_id=lend.lenditem_id,
                lenditem_name=lend.lenditem_name,
                lendnumber=lend.lendnumber,
                lenditem_grade=lend.lenditem_grade,
                lendtime=lend.lendtime,
                lendday=lend.lendday,
                lend=lend,
                static='已审核通过'
            )
            approval.save()

        elif request.data.get('lenditem_grade') == '2' or request.data.get('lenditem_grade') == '3':
            lend = Lend.objects.create(lenduser_realname=request.data.get('lenduser_realname'),
                                       lenditem_id=request.data.get('lenditem_id'),
                                       lenditem_name=request.data.get('lenditem_name'),
                                       lendnumber=request.data.get('lendnumber'),
                                       lenditem_grade=request.data.get('lenditem_grade'), lendtime=time_str,
                                       lendday=request.data.get('lendday'))
            lend.save()

            # 审批
            approval = Approval.objects.create(
                lenduser_realname=lend.lenduser_realname,
                lenditem_id=lend.lenditem_id,
                lenditem_name=lend.lenditem_name,
                lendnumber=lend.lendnumber,
                lenditem_grade=lend.lenditem_grade,
                lendtime=lend.lendtime,
                lendday=lend.lendday,
                lend=lend
            )
            approval.save()

        return Response({"ok_lend":True},status=status.HTTP_200_OK)

    # 用户查询自己已提交借用记录
    def get(self,request):
        lendobj = Lend.objects.filter(lenduser_realname=request.data.get('lenduser_realname'))
        lenddata = LendSerializers(instance=lendobj,many=True)
        return Response({"lenddatas":lenddata.data},status=status.HTTP_200_OK)

# 管理员审批
class ApprovalView(APIView):
    # 审批
    def post(self,request):
        privilege_level = request.data.get('privilege_level')

        Approvalobj = Approval.objects.get(id=request.data.get('id'))
        lendobj = Approvalobj.lend

        if lendobj.approved_adminname == privilege_level:
            return Response({"ok": False, "message": "该级管理员已审核"},status=status.HTTP_200_OK)
        else:
            if Approvalobj.lenditem_grade == 2:
                Approvalobj.static = '已审核通过'
                lendobj.approval_progress = '100%'
                Approvalobj.save()
                lendobj.save()
                return Response({"ok":True},status=status.HTTP_200_OK)
            elif Approvalobj.lenditem_grade == 3:
                if lendobj.approved_adminname == privilege_level:
                    return Response({"ok": False, "message": "该级管理员已审核"}, status=status.HTTP_200_OK)
                else:
                    if lendobj.approved_adminname == -1:
                        lendobj.approved_adminname = privilege_level
                        lendobj.approval_progress = '50%'
                        Approvalobj.save()
                        lendobj.save()
                        return Response({"ok": True}, status=status.HTTP_200_OK)
                    else:
                        Approvalobj.static = '已审核通过'
                        lendobj.approval_progress = '100%'
                        Approvalobj.save()
                        lendobj.save()
                        return Response({"ok": True}, status=status.HTTP_200_OK)

    def get(self,request):
        data = Approval.objects.all()
        approvaldata = ApprovalSerializers(instance=data,many=True)
        return Response({"data":approvaldata.data},status=status.HTTP_200_OK)

# 获取借用归还上传图片

# 2/3级物品审批通过上传图片
