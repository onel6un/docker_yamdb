from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken import views

from .views import *

APP_NAME = 'reviews'

router = routers.DefaultRouter()

router.register('v1/categories', CategoriesAPI)
router.register('v1/genres', GenriesAPI)
router.register('v1/titles', TitlesAPI)
router.register(r'v1/titles/(?P<titles_id>\d+)/reviews', ReviewsAPI, basename='titles')
router.register(r'v1/titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsAPI, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
