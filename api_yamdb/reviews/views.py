from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins



from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from core import filter_sets
from core.pagination import APIPagination
from core.permissions import *


class CategoriesAPI(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 
    pagination_class = APIPagination


class GenriesAPI(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 
    pagination_class = APIPagination


class TitlesAPI(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filter_sets.TitlesFilterSet
    # filterset_fields = ('name', 'year', 'category__slug')
    pagination_class = APIPagination

    # использование двух сериализаторов диктуеться ТЗ,
    # для записи поля genre и category используеться slugRelatedField
    # для чтения поля genre в виде списка словарей используеться вложенный сериализатор,
    # для чтения поля category в виде словаря используеться вложенный сериализатор,
    # что и требует отдельных сериализаторов для чтения и записи
    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list' or self.action == 'retrieve':
            return TitlesSerializerForRead
        return TitlesSerializerForCreate


class ReviewsAPI(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = APIPagination
    permission_classes = (AuthorOrModeratorOtherwiseReadOnly,)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте или лист
        if self.action in ('retrieve', 'list'):
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('titles_id')
        queryset = Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('titles_id')
        title_for_review = Title.objects.get(pk=title_id)
        serializer.save(
            author=self.request.user,
            title=title_for_review
        )


class CommentsAPI(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = APIPagination
    permission_classes = (AuthorOrModeratorOtherwiseReadOnly,)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте или лист
        if self.action in ('retrieve', 'list'):
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(review=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review_for_comment = Review.objects.get(pk=review_id)
        serializer.save(
            author=self.request.user,
            review=review_for_comment
        )
