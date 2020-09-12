from rest_framework import serializers
from  django.contrib.auth.models import User
from .models import Property

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'email', 'mobile')