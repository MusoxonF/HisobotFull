from rest_framework import serializers

from .models import *
from User.serializers import UserSerializer, XodimSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class MaxsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maxsulot
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class HisobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hisobot
        fields = ('id', 'xodim', 'user', 'xato', 'xato_soni', 'butun_soni', 'mahsulot', 'created_at', 'updated_at', 'photo', 'izoh', 'ish_vaqti', 'audio')
        read_only_fields = ['photo']
    def update(self, instance, validated_data):
        instance.xodim = validated_data.get('xodim', instance.xodim)
        # instance.user = validated_data.get('user', instance.user)
        instance.xato = validated_data.get('xato', instance.xato)
        # instance.rasm = validated_data.get('rasm', instance.rasm)
        instance.audio = validated_data.get('audio', instance.audio)
        instance.izoh = validated_data.get('izoh', instance.izoh)
        instance.mahsulot = validated_data.get('mahsulot', instance.mahsulot)
        instance.xato_soni = validated_data.get('xato_soni', instance.xato_soni)
        instance.butun_soni = validated_data.get('butun_soni', instance.butun_soni)
        instance.ish_vaqti = validated_data.get('ish_vaqti', instance.ish_vaqti)
        a = validated_data.get('photo',None)
        if a:
            for x in a:
                new_photo = Photo.objects.create(photo=x)
                instance.photo.add(new_photo)
        instance.save()
        return instance


class HisobotGetSerializer(serializers.ModelSerializer):
    xodim = XodimSerializer()
    user = UserSerializer()
    xato = ProblemSerializer()
    mahsulot = MaxsulotSerializer()
    photo = PhotoSerializer(many=True)
    class Meta:
        model = Hisobot
        fields = ('id', 'xodim', 'user', 'xato', 'xato_soni', 'butun_soni', 'mahsulot', 'created_at', 'updated_at', 'photo', 'izoh', 'ish_vaqti', 'audio')