from unittest import result
from django.shortcuts import render
from authentications.serializers import User
from .models import  *
from django.http import HttpResponse,JsonResponse
from authentications.models import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import  permissions

from django.views import View

# <--------------Super user account creations API Started ----------->
class superuser(APIView) :
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)
    def get(self,request):
        us = UserAccount.objects.filter(email=request.user).first()
        us.is_staff = True
        us.is_superuser = True
        us.save()
        print(us.is_staff)
        message = {"message":"super user created"}
        return  JsonResponse(message,safe=False,status=200)
# <---------------super user account creations api ENDED----------->


class RedirectSocial(View):

    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        print(json_obj)
        return JsonResponse(json_obj)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context



