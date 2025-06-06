import facebook
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings # To access SIMPLE_JWT settings

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
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Step 4: Set token as cookie
    response = JsonResponse({'token': access_token}, safe=False, status=status.HTTP_200_OK)

    # Use a generic cookie name, can be configured in settings if needed
    auth_cookie_name = getattr(settings, 'SIMPLE_JWT', {}).get('AUTH_COOKIE', 'jwt_auth_token')
    # Use access token lifetime from settings
    access_token_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('ACCESS_TOKEN_LIFETIME')

    if access_token_lifetime:
        response.set_cookie(
            auth_cookie_name,
            access_token,
            max_age=access_token_lifetime.total_seconds(),
            httponly=True,
            samesite=getattr(settings, 'SIMPLE_JWT', {}).get('AUTH_COOKIE_SAMESITE', 'Lax') # Add SameSite attribute
        )

    return response


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_details(request):

    facebook_profile = FbAuth.objects.get(user=request.user)

    payload = {'facebook_id': facebook_profile.facebook_id,
                 'name': request.user.first_name,
                 'email': request.user.email}

    return JsonResponse(payload, safe=False, status=status.HTTP_200_OK)

