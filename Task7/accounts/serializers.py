# users/serializers/auth_serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db import IntegrityError


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'username')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("هذا البريد الإلكتروني مسجل بالفعل.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "كلمتا المرور غير متطابقتين"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            email=validated_data['email'],
            username=validated_data.get('username', '') ,
            role='user'
        )

        user.set_password(validated_data['password'])
        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError({"email": "هذا البريد الإلكتروني مسجل بالفعل."})
        return user



class AdminRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'username')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("هذا البريد الإلكتروني مسجل بالفعل.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "كلمتا المرور غير متطابقتين"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            email=validated_data['email'],
            username=validated_data.get('username', '') ,
            role='admin'
        )

        user.set_password(validated_data['password'])
        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError({"email": "هذا البريد الإلكتروني مسجل بالفعل."})
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed('البريد الإلكتروني أو كلمة المرور غير صحيحة')

        return {
            'user': user,
        }
