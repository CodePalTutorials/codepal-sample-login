import facebook
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

from my_project.settings import JWT_AUTH_COOKIE, JWT_EXPIRATION_DELTA
from registration.models import FbAuth


@api_view(['POST'])
def register_user_via_facebook(request):

    data = dict(request.data)

    #  Step 1: Call facebook and verify details. Make sure data is correct.
    profile = facebook.GraphAPI(access_token=data['accessToken']).get_object('me', fields='email,first_name,gender')

    if not profile or not profile.get('email'):
        raise APIException(code=status.HTTP_400_BAD_REQUEST)

    username, password, email, first_name = profile.get('email'), data['accessToken'], profile.get('email'), profile.get('first_name')
    #  Step 2: Store details. Register the user.
    try:
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
    except IntegrityError:
        user = User.objects.get(username=username, email=email)

    FbAuth.create_or_update(user, data['userID'], data['accessToken'])

    #   Step 3: Return JWT token in cookie.

    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)

    # Step 4: Set token as cookie
    response = JsonResponse({'token': token}, safe=False, status=status.HTTP_200_OK)
    response.set_cookie(JWT_AUTH_COOKIE, token, JWT_EXPIRATION_DELTA.total_seconds(), httponly=True)

    return response


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_details(request):

    facebook_profile = FbAuth.objects.get(user=request.user)

    payload = {'facebook_id': facebook_profile.facebook_id,
                 'name': request.user.first_name,
                 'email': request.user.email}

    return JsonResponse(payload, safe=False, status=status.HTTP_200_OK)

