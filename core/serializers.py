from djoser.serializers import UserCreateSerializer as BasedUserCreateSerializer
from djoser.serializers import UserSerializer as BasedUserSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User


class UserCreateSerializer(BasedUserCreateSerializer):
    class Meta(BasedUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BasedUserSerializer):
    class Meta(BasedUserSerializer.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Invalid username/password')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        return attrs
    
        
###################################################################################
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data['user'] = self.user.username  # Add username to response data
#         return data


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         user = authenticate(
#             username=attrs['username'], password=attrs['password'])

#         if not user:
#             raise serializers.ValidationError('Invalid username/password')

#         if not user.is_active:
#             raise serializers.ValidationError('User account is disabled')

#         return attrs

#     def create(self, validated_data):
#         user = authenticate(
#             username=validated_data['username'],
#             password=validated_data['password']
#         )

#         refresh = RefreshToken.for_user(user)

#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': UserSerializer(user).data
#         }
