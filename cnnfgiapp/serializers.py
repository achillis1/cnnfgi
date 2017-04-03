from rest_framework import serializers
from .models import Fgi


class FgiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fgi
        fields = '__all__'
