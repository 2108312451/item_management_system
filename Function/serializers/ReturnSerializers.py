from rest_framework import serializers
from Function.models import Returns

class ReturnSerializers(serializers.ModelSerializer):
    class Meta:
        model = Returns
        fields = '__all__'