from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Function.models import Collections
from Function.serializers.CollectionSerializers import CollectionSerializers

class CollectionView(APIView):
    def post(self,request):
        try:
            obj = Collections.objects.create(item_id=request.data.get('item_id'),item_name=request.data.get('item_name'),username=request.data.get('username'))
            obj.save()
            return Response({"ok_collection":True},status=status.HTTP_200_OK)
        except:
            return Response({"ok_collection": False,"message":"缺少参数"}, status=status.HTTP_200_OK)

    def delete(self,request,id):
        try:
            obj = Collections.objects.get(id=id)
            obj.delete()
            return Response({"del_collection": True}, status=status.HTTP_200_OK)
        except:
            return Response({"del_collection": False, "message": "id不存在"}, status=status.HTTP_200_OK)

    def get(self,request,username):
        try:
            objdata = Collections.objects.filter(username=username)
            datas = CollectionSerializers(instance=objdata,many=True)
            return Response({"data": datas.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "用户id不存在"}, status=status.HTTP_200_OK)