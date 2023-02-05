from rest_framework import permissions


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOrReadOnly(permissions.BasePermission):
    '''Права доступа на создание и изменение записей
    только у admin и superuser, у всех доступ на чтение '''

    def has_permission(self, request, view):
        '''Условия разрешения на выполнение запроса для получения
        списка объектов или создания нового объекта'''
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.is_superuser is True:
            return True
        return False

    # Если предыдущая функция вернула True, выполняеться
    # нижестоящая
    def has_object_permission(self, request, view, obj):
        '''Условия разрешения на выполнение запроса для получения,
        изменения или удаления конкретного объекта'''
        return (request.user.role == 'admin'
                or request.user.is_superuser is True)


class AuthorOrModeratorOtherwiseReadOnly(permissions.BasePermission):
    '''Право на изменение или удаление экземпляра, есть у
        admin, moderator, superuser и автора экземпляра'''
    def has_permission(self, request, view):
        '''Условия разрешения на выполнение запроса для получения
        списка объектов или создания нового объекта'''
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user == obj.author:
            return True
        if request.user.role in ('admin', 'moderator'):
            return True
        if request.user.is_superuser is True:
            return True
        return False


class AdminOnly(permissions.BasePermission):
    '''Права доступа только у admin и superuser'''
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.is_superuser is True:
            return True
        return False
