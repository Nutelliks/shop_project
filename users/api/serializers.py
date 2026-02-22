from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth

from ..models import User 


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id', )


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=(validate_password, ))
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 
                  'last_name', 'email', 
                  'password', 'password2')
        
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            return serializers.ValidationError("Passwords didn't match")
        return data
    

    def create(self, validated_data: dict):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserSerializer(self.user).data
        data["message"] = "Login successfully"

        return data


class UserProfileSerialier(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id', 'email',
            'first_name', 'last_name',
            'username', 'image',
        )
        read_only_fields = ('id', 'email', )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception as e:
            self.fail(e)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password, ])
    new_password2 = serializers.CharField(required=True)


    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            return serializers.ValidationError("Password fields didn't match")
        return attrs
    
