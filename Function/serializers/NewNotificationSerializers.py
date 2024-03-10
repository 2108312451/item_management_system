from rest_framework import serializers
from Function.models import NewNotifications

class NewNotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewNotifications
        fields = '__all__'