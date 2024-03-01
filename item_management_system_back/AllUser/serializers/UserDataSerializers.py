from rest_framework import serializers
from AllUser.models import OrdinaryUser,Regular_Administrator,Super_Administrator

class OrdinaryUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrdinaryUser
        fields = '__all__'

class Regular_AdministratorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Regular_Administrator
        fields = '__all__'

class Super_AdministratorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Super_Administrator
        fields = '__all__'