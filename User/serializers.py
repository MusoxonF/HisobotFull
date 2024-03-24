from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import *


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user = User.objects.get(username=self.user.username)
        data['gender'] = user.gender
        data['id'] = user.id
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        # data2 = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # data2 = attrs.get('refresh')
        data['refresh'] = attrs.get('refresh') 
        # user = User.objects.get(username=self.user.username)
        # data['status'] = user.status
        # data['id'] = user.id
        # return (data, f'refresh: {data2}')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name',  'photo', 'gender', 'phone', 'is_direktor', 'is_bulim', 'is_tekshiruvchi', 'is_xodim')
        write_only_fields = ('password')
        # read_only_fields = ('is_direktor', 'is_bulim', 'is_tekshiruvchi')
        extra_kwargs = {
            'password': {
                'write_only': True,
               'style': {'input_type': 'password'}
            }
        }
    
    def update(self, instance, validated_data):
        instance.is_direktor = validated_data.get('is_direktor', instance.is_direktor)
        instance.is_bulim = validated_data.get('is_bulim', instance.is_bulim)
        instance.is_tekshiruvchi = validated_data.get('is_tekshiruvchi', instance.is_tekshiruvchi)
        instance.is_xodim = validated_data.get('is_xodim', instance.is_xodim)
        instance.username = validated_data.get('username', instance.username)
        # instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user


class XodimSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Xodim
        fields = ('id', 'user', 'ish_turi', 'bulimi')

    def update(self, instance, validated_data):
        # instance.ish_turi = validated_data.get('ish_turi', instance.ish_turi)
        instance.bulimi = validated_data.get('bulimi', instance.bulimi)
        instance.save()
        return instance
    
    # def partial_update(self, instance, validated_data):
    #     user_data = validated_data.pop('user', None)
    #     if user_data:
    #         user_instance = instance.user
    #         UserSerializer().partial_update(user_instance, user_data)
    #     instance.id_raqam = validated_data.get('id_raqam', instance.id_raqam)
    #     instance.bulimi = validated_data.get('bulimi', instance.bulimi)
    #     instance.save()
    #     return self.update(instance, validated_data)
        
        
class Ish_turiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ish_turi
        fields = ('id', 'name', 'ish_id')

class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = ('id', 'name', 'bulim_id', 'user')