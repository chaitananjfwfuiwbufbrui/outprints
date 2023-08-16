from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from TESTIITFREE import test_settings
import requests

# baseUrl = "https://powersense.co.in"
baseUrl = "http://127.0.0.1:8000"
loginurl = f"{baseUrl}/auth/jwt/create/"
Me_info = f"{baseUrl}/auth/users/me/"

DJANGO_SETTINGS_MODULE = test_settings
class UserAccountTestCase(TestCase):
    def test_user_creation(self):
        User = get_user_model()
        email = "test1@example.com"
        password = "testpassword"
        first_name = "John"
        last_name = "Doe"
        account_type = "CONSULTANT"

        # create the user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            type_of_account=account_type,
        )

        # check that the user was created with the correct data
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.type_of_account, account_type)

        # check that the user has the expected permissions
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)






class UserLoginTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            type_of_account='CONSULTANT',
        )
        self.user.is_active = True
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.save()

    def test_user_login(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }

        # Send a POST request to the login API endpoint
        response = self.client.post(loginurl, data=payload)
        data = response.data
        print(data)
        # Verify that the response has a 200 OK status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the JWT token from the response data
        access_token = data['access']

        # Add the JWT token to the Authorization header
        headers = {
            'Accept': 'application/json',
            'Authorization': f"JWT {access_token}"
        }
        payload={}
        # Send a GET request to the API endpoint that requires authentication
        response = requests.request("GET", Me_info, headers=headers, data=payload)
        print(response.text)
        # Verify that the response has a 200 OK status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       