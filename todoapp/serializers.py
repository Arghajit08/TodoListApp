from django.db.models import fields
from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User

#Created modelSerializer for each user

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

