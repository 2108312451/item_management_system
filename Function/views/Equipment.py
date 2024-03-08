from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import FileResponse
from PIL import Image
import io
import datetime
from Function.models import Appointment,EquipmentApproval,EquipmentTimes
from Function.serializers.EquipmentSerializers import EquipmentApprovalSerializers,EquipmentTimesSerializers

# 提交预约申请
class SubmitApplication(APIView):
    # 提交申请
    def post(self,request):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%Y-%m-%d')
        # 将字符串解析为日期对象
        current_times = datetime.datetime.strptime(time_str, '%Y-%m-%d')
        # 定义一个 timedelta 对象，表示要加减的天数
        delta = timedelta(days=1)  # 加5天，如果要减去天数，将days参数改为负数即可
        # 对日期对象进行加减操作
        new_time = current_times + delta
        # 将结果转换为字符串格式
        time_strs = new_time.strftime('%Y-%m-%d')

        # 时间更迭
        one = Appointment.objects.get(item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),day=1)
        if one.time != time_strs:
            date_obj1 = datetime.datetime.strptime(one.time, '%Y-%m-%d').date()
            date_obj2 = datetime.datetime.strptime(time_str, '%Y-%m-%d').date()
            # 计算两个日期之间的差异
            diff = (date_obj2 - date_obj1).days

            #删除旧日期
            for i in range(1,diff+1):
                oldata = Appointment.objects.get(item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),day=i)
                oldata.delete()

            #更该添加新日期
            for i in range(1,6):
                try:
                    data = Appointment.objects.get(item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),day=i+diff)
                    data.day = i
                    # 将字符串解析为日期对象
                    current_time = datetime.strptime(data.time, '%Y-%m-%d')
                    # 定义一个 timedelta 对象，表示要加减的天数
                    delta = timedelta(days=-diff)  # 加5天，如果要减去天数，将days参数改为负数即可
                    # 对日期对象进行加减操作
                    new_time = current_time + delta
                    # 将结果转换为字符串格式
                    new_time_str = new_time.strftime('%Y-%m-%d')
                    data.time = new_time_str
                    data.save()
                except:
                    current_time = datetime.strptime(time_str, '%Y-%m-%d')
                    delta = timedelta(days=i)
                    newdata = current_time + delta
                    new_time_str = newdata.strftime('%Y-%m-%d')
                    data = Appointment.objects.create(item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),time=new_time_str,day=i)
                    data.save()

            # 预约
            item_id = request.data.get('item_id')
            item_name = request.data.get('item_name')
            adress = request.data.get('adress')
            username = request.data.get('username')
            item_grade = request.data.get('item_grade')

            days = request.data.get('days') #第几天
            beginhour = request.data.get('beginhour')  #第几个小时
            endhour = request.data.get('endhour')
            longtime = endhour - beginhour  #时长

            begintime = str((current_times + timedelta(days=days)).strftime('%Y-%m-%d')) + str(' ' + str(beginhour) + ':00:00')

            # 判断是否存在已预约
            daydata = Appointment.objects.get(item_id=item_id, item_name=item_name, day=days)
            # 获取第 i+4 个字段的值
            for i in range(beginhour,endhour+1):
                desired_value = getattr(daydata, f'time{i}')
                new_value = True
                setattr(daydata, f'time{i}', new_value)

                if desired_value == True:
                    return Response({"ok":False,"message":"该时间段已存在用户预约"},status=status.HTTP_200_OK)

            daydata.save()

            # 管理员审批表
            objs = EquipmentTimes.objects.create(item_id=item_id,item_name=item_name,adress=adress,username=username,begintime=begintime,longtime=longtime,item_grade=item_grade)
            objs.save()
            if item_grade != 1:
                obj = EquipmentApproval.objects.create(item_id=item_id, item_name=item_name, adress=adress,
                                                       username=username, begintime=begintime, longtime=longtime,
                                                       item_grade=item_grade)
                obj.save()
            return Response({"ok": True},status=status.HTTP_200_OK)


        # 未时间更迭，正常预约
        else:
            item_id = request.data.get('item_id')
            item_name = request.data.get('item_name')
            adress = request.data.get('adress')
            username = request.data.get('username')
            item_grade = request.data.get('item_grade')

            days = request.data.get('days')  # 第几天
            beginhour = request.data.get('beginhour')  # 第几个小时
            endhour = request.data.get('endhour')
            longtime = endhour - beginhour  # 时长

            begintime = str((current_times + timedelta(days=days)).strftime('%Y-%m-%d')) + str(
                ' ' + str(beginhour) + ':00:00')

            # 判断是否存在已预约
            daydata = Appointment.objects.get(item_id=item_id, item_name=item_name, day=days)
            for i in range(beginhour, endhour + 1):
                desired_value = getattr(daydata, f'time{i}')
                new_value = True
                setattr(daydata, f'time{i}', new_value)
                if desired_value == True:
                    return Response({"ok": False, "message": "该时间段已存在用户预约"}, status=status.HTTP_200_OK)

            daydata.save()

            # 管理员审批表
            if item_grade != 1:
                objs = EquipmentTimes.objects.create(item_id=item_id, item_name=item_name, adress=adress,
                                                     username=username,
                                                     begintime=begintime, longtime=longtime, item_grade=item_grade)
                objs.save()
                obj = EquipmentApproval.objects.create(item_id=item_id, item_name=item_name, adress=adress,
                                                       username=username, begintime=begintime, longtime=longtime,
                                                       item_grade=item_grade,equipmenttimes=objs)
                obj.save()
            else:
                objs = EquipmentTimes.objects.create(item_id=item_id, item_name=item_name, adress=adress,
                                                     username=username,
                                                     begintime=begintime, longtime=longtime, item_grade=item_grade,approval_progress='100%')
                objs.save()

            return Response({"ok": True}, status=status.HTTP_200_OK)

    # 用户获取自己的提交记录
    def get(self,request,username):
        obj = EquipmentTimes.objects.filter(username=username)
        datas = EquipmentTimesSerializers(instance=obj,many=True)
        return Response({"data":datas.data},status=status.HTTP_200_OK)


# 管理员审设备批
class ApprovalView(APIView):
    # 审批
    def post(self,request):
        privilege_level = request.data.get('privilege_level')
        Approvalobj = EquipmentApproval.objects.get(id=request.data.get('id'))
        EquipmentTimesobj = Approvalobj.equipmenttimes

        if EquipmentTimesobj.privilege_level == privilege_level:
            return Response({"ok": False, "message": "该级管理员已审核"},status=status.HTTP_200_OK)
        else:
            if Approvalobj.item_grade == 2:
                Approvalobj.approval_progress = '已审核通过'
                EquipmentTimesobj.approval_progress = '100%'
                Approvalobj.save()
                EquipmentTimesobj.save()
                return Response({"ok":True},status=status.HTTP_200_OK)
            elif Approvalobj.item_grade == 3:
                if EquipmentTimesobj.privilege_level == privilege_level:
                    return Response({"ok": False, "message": "该级管理员已审核"}, status=status.HTTP_200_OK)
                else:
                    if EquipmentTimesobj.privilege_level == -1:
                        EquipmentTimesobj.privilege_level = privilege_level
                        EquipmentTimesobj.approval_progress = '50%'
                        Approvalobj.save()
                        EquipmentTimesobj.save()
                        return Response({"ok": True}, status=status.HTTP_200_OK)
                    else:
                        Approvalobj.approval_progress = '已审核通过'
                        EquipmentTimesobj.approval_progress = '100%'
                        Approvalobj.save()
                        EquipmentTimesobj.save()
                        return Response({"ok": True}, status=status.HTTP_200_OK)

    def get(self,request):
        data = EquipmentApproval.objects.all()
        approvaldata = EquipmentApprovalSerializers(instance=data,many=True)
        return Response({"data":approvaldata.data},status=status.HTTP_200_OK)

# 2/3级设备审批通过后上传图片
class UploadImages(APIView):
    def post(self,request):
        equipmentid = request.data.get('equipmentid')
        # 获取图片数据
        image_data = request.data.get('image')
        # 将图片数据转换为文件对象
        image_file = ContentFile(image_data.read())
        # 保存图片文件到磁盘上的指定路径（比如 static/images 文件夹）
        default_storage.save('static/Equipmentimage/' + str(equipmentid) + '_equipment.jpg', image_file)
        return Response({"ok_equipment": True}, status=status.HTTP_200_OK)

# 获取设备上传图片
class GetPicture(APIView):
    def get(self,request,id):
        try:
            image_path = f'static/Equipmentimage/{id}_equipment.jpg'  # 图片文件路径
            # 打开原始图片
            image = Image.open(image_path)
            width, height = image.size  # 获取原始图片的宽度和高度

            # 计算目标宽度和高度为原来的一半
            target_width = int(width * 1)
            target_height = int(height * 1)
            # 压缩图片
            image = image.resize((target_width, target_height))
            # 创建一个内存中的临时文件
            output = io.BytesIO()
            # 将压缩后的图片保存到临时文件
            image.save(output, format='JPEG')
            # 将临时文件对象移动到开头以便读取
            output.seek(0)
            # 返回压缩后的图片作为响应
            return FileResponse(output, content_type='image/jpeg')
        except IOError:
            return Response({'message': '未找到图片'}, status=status.HTTP_404_NOT_FOUND)  # 如果未找到图片，则返回 404
