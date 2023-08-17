from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from authentications.serializers import *
User = get_user_model()

class UserCreateSerializer_121(serializers.ModelSerializer):

   
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','user_id', 'email', 'first_name', 'last_name', 'password','type_of_account',)
class user_referals(serializers.ModelSerializer):

    referal_user_ewq = serializers.SerializerMethodField('referal_user')
    def referal_user(self,obj):
        sew = obj.referals.all()
        ser = UserCreateSerializer_121(sew,many = True)
        return  ser.data
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','user_id', 'email', 'first_name', 'last_name', 'password','type_of_account','referal_user_ewq')
