from rest_framework import serializers
from Function.models import Repairs,Feedback

class RepairsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Repairs
        fields = '__all__'

class FeedbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'