from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import filters

from .serializer import *

from core.permissions import AdminOnly
from core.pagination import APIPagination


class RegistrationAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetTokenAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersAPI(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    pagination_class = APIPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',) 


class UserSelfAPI(APIView):
    """View класс для обработки информации пользователя о себе"""
    serializer_class = UserSelfSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
