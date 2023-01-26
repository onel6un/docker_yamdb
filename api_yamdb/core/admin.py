from django.contrib import admin

from .models import *
from reviews.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenreInline(admin.TabularInline):
    model = GenriesOfTitle
    extra = 1
    raw_id_fields = ('genre', )


class TitleAdmin(admin.ModelAdmin):
    inlines = (
       GenreInline,
    )
    list_display = ('id', 'name', 'year', 'category')
    search_fields = ('id', 'name', 'year', 'category')
    list_filter = ('id', 'year', 'category')


class GenriesOfTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')
    search_fields = ('id', 'title', 'genre')
    list_filter = ('id', 'title', 'genre')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('id', 'text', 'author', 'score', 'pub_date')
    list_filter = ('id', 'text', 'author', 'score', 'pub_date')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review', 'text', 'created')
    search_fields = ('id', 'author', 'review', 'text', 'created')
    list_filter = ('id', 'author', 'review', 'text', 'created')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenriesOfTitle, GenriesOfTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)