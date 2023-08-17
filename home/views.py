from django.shortcuts import render
import json
from django.shortcuts import render
from .models import  *
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import  render
from rest_framework import  permissions
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from django.http import HttpResponse,JsonResponse
import io
from django.views.decorators.csrf import csrf_exempt
from authentications.models import *
from rest_framework.decorators import  api_view, permission_classes
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import * 
from rest_framework.response import Response

@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def hello_world(request):
    if request.method == "GET":
        msh = {'msg':'working'}
        ss = json.dumps(msh)
        
        return Response(ss)
    if request.method =="POST":
        # data =  request.data
        msh = {'msg':'post working'}
        ss = json.dumps(msh)
        
        return Response(ss)


        

from django.shortcuts import redirect
from django.urls import reverse

class generate_referral_link(APIView) :
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)
    def get(self,request):

        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            # Generate a unique referral code based on the user's ID or any other unique identifier
            # referral_code = f"REF-{request.user.id}"
            referral_code = request.user.user_id
            
            # Save the referral code to the user's model
            # request.user.referral_code = referral_code
            # request.user.save()

            # Generate the referral link using the reverse function and the referral code
            referral_link ="http://127.0.0.1:8000/auth/users/?ref="+referral_code
            json = {
                "referal":referral_link
            }
            return JsonResponse(json, status=400,safe=False)

    # else:
    #     # User is not authenticated, handle accordingly (e.g., redirect to login page)
    #     return redirect('login')  # Update this with the actual login URL
class login_with_referral(APIView) :
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)
    def get(self,request):

    # Assuming you have a custom User model with a referral_code field
        try:
            referred_user = User.objects.get(user_id=referral_code)
        except User.DoesNotExist:
            referred_user = None

        # Set a cookie or session variable to track the referral (you can also use request.user if logged in)
        if referred_user:
            request.session['referral_user_id'] = referred_user.id

        # Redirect to the login page
        return redirect('login')  # Update this with the actual login URL
class checkthereferals(APIView) :
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)
    def get(self,request):
        referred_user = User.objects.all()
        seralizer = user_referals(referred_user,many = True)
        message = {"message":"super user created"}
        return  JsonResponse(seralizer.data,safe=False,status=200)