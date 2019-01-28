from rest_framework import serializers
from .models import Bt_dev, Bt_data


class Bt_dev_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bt_dev
        fields = '__all__'

class Bt_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bt_data
        fields = '__all__'

