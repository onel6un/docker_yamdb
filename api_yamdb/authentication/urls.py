from django.urls import path, include
from rest_framework import routers
from authentication.views import *

APP_NAME = 'auth'

router = routers.DefaultRouter()
router.register('v1/users', UsersAPI, basename='users')

urlpatterns = [
    path('v1/auth/register/', RegistrationAPI.as_view()),
    path('v1/auth/token/', GetTokenAPI.as_view()),
    path('v1/users/me/', UserSelfAPI.as_view()),
    path('', include(router.urls))
]
