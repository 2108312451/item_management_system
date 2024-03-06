from rest_framework import serializers
from Function.models import Collections

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = '__all__'