from rest_framework import serializers
from Function.models import Lend,Approval

class LendSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lend
        fields = '__all__'

class ApprovalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'