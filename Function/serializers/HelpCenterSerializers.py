from rest_framework import serializers
from Function.models import HelpCenterContent,HelpCenterSave

class HelpCenterSaveSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpCenterSave
        fields = '__all__'

class HelpCenterContentSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpCenterContent
        fields = '__all__'