"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework_jwt.views import obtain_jwt_token

from registration.views import register_user_via_facebook, get_user_details

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api-token-auth/', obtain_jwt_token),

    # Url for facebook signup
    url(r'^api/v1/user/register/facebook', register_user_via_facebook),

    # Url to fetch user details
    url(r'^api/v1/user/get/account', get_user_details),




    url(r'^$', TemplateView.as_view(template_name='home.html')),
]
