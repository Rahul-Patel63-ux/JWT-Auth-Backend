from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        # fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(write_only=True)
    # Note : "write_only=True" means it take data from client to do operations in DB but not to return  

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'c_password']
        extra_kwargs = {'password': {'write_only': True},}

    def validate(self, data):
        if data['password'] != data['c_password']:
            raise serializers.ValidationError("Password didn't match!")
        return data 

    def create(self, validated_data):
        validated_data.pop('c_password')
        user = User.objects.create_user(**validated_data)
        return user