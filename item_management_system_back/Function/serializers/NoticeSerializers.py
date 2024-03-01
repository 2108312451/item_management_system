from rest_framework import serializers
from Function.models import Notice

class NoticeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'