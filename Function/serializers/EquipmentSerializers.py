from rest_framework import serializers
from Function.models import EquipmentTimes,EquipmentApproval

class EquipmentTimesSerializers(serializers.ModelSerializer):
    class Meta:
        model = EquipmentTimes
        fields = '__all__'

class EquipmentApprovalSerializers(serializers.ModelSerializer):
    class Meta:
        model = EquipmentApproval
        fields = '__all__'