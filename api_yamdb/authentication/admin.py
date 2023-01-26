from django.contrib import admin

from authentication.models import *


class UserAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('id', 'username', 'first_name', 'last_name', 'email',
                    'bio', 'role', 'confirm_code')
    # Добавляем интерфейс для поиска
    search_fields = ('id', 'username', 'first_name', 'last_name',
                     'email', 'role')
    # Добавляем возможность фильтрации 
    list_filter = ('id', 'username', 'first_name', 'last_name',
                   'email', 'role')


admin.site.register(User, UserAdmin)
