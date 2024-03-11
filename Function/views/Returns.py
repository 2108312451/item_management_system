from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
from Function.models import Returns
from Function.serializers.ReturnSerializers import ReturnSerializers
from Items.models import Items
from Function.models import Lend

#物品归还
class ReturnView(APIView):
    def post(self,request):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        re = Returns.objects.create(user_realname=request.data.get('user_realname'),item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),number=request.data.get('number'),time=time_str)
        re.save()

        # 获取图片数据
        image_data = request.data.get('image')
        # 将图片数据转换为文件对象
        image_file = ContentFile(image_data.read())
        # 保存图片文件到磁盘上的指定路径
        default_storage.save('static/Retutnimage/' + str(re.id) + '_return.jpg', image_file)

        itemobj = Items.objects.get(id=request.data.get('item_id'))
        itemobj.inventory += int(request.data.get('number'))
        itemobj.save()

        lendobj = Lend.objects.get(id=request.data.get('lenditem_id'))
        lendobj.oretuen = True
        lendobj.save()

        return Response({"ok_return":True},status=status.HTTP_200_OK)
    def get(self,request,user_realname):
        if user_realname != 'all':
            try:
                redata = Returns.objects.filter(user_realname=request.data.get('user_realname'))
                datas = ReturnSerializers(instance=redata,many=True)
                return Response({"data":datas.data},status=status.HTTP_200_OK)
            except:
                return Response({"message":"user_realname不存在"},status=status.HTTP_200_OK)
        else:
            try:
                redata = Returns.objects.all()
                datas = ReturnSerializers(instance=redata, many=True)
                return Response({"data": datas.data}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "数据不存在"}, status=status.HTTP_200_OK)
