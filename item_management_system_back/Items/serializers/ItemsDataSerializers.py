from rest_framework import serializers
from Items.models import Items,Comments,Warehousing,Outbound

class ItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class WarehousingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Warehousing
        fields = '__all__'

class OutboundSerializers(serializers.ModelSerializer):
    class Meta:
        model = Outbound
        fields = '__all__'