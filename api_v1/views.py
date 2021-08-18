from re import split

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.aggregates import Avg
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          ConfirmTokenSerializer, CreateUserSerializer,
                          GenreSerializer, ReviewsSerializer,
                          TitleSerializerRead, TitleSerializerWrite,
                          UserSerializer)

User = get_user_model()


class CreateListDestroyView(CreateModelMixin, ListModelMixin,
                            DestroyModelMixin, GenericViewSet):
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serialized = CreateUserSerializer(data=request.data)
    serialized.is_valid()
    username = split(r'_', serialized.data['email'])[0]
    user, created = User.objects.get_or_create(
        email=serialized.data['email'],
        defaults={'username': username})
    if created:
        user.set_unusable_password()
        user.save()
    confirmation_code = default_token_generator.make_token(user)
    user.email_user(
        subject='Confirmation code',
        message='Код подтверждения - {}'.format(confirmation_code)
    )
    return Response(serialized.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serialized = ConfirmTokenSerializer(data=request.data)
    serialized.is_valid(raise_exception=True)
    user = User.objects.get(email=serialized.validated_data['email'])
    if not default_token_generator.check_token(
        user,
        serialized.validated_data['confirmation_code']
    ):
        raise ValidationError('Data is not valid')
    access = AccessToken.for_user(user)
    return Response(
        {"token": str(access)}
    )


class UsersListCreateViewSet(ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        user = self.request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdmin | IsModerator]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs['title_id']
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdmin | IsModerator]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs['title_id'],
            id=self.kwargs['review_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs['title_id'],
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyView):
    queryset = Category.objects.all()
    permission_classes = [ReadOnly | IsAdmin]
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name']


class GenreViewSet(CreateListDestroyView):
    queryset = Genre.objects.all()
    permission_classes = [ReadOnly | IsAdmin]
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name']


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-rating')
    permission_classes = [ReadOnly | IsAdmin]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite
