from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UsersListCreateViewSet,
                    create_user, get_token)

v1_router = DefaultRouter()

v1_router.register('users', UsersListCreateViewSet, basename='user-list')
v1_router.register(
    'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewsViewSet,
    basename='review-list'
)
v1_router.register(
    'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='comment-list'
)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

auth_patterns = [
    path('email/', create_user, name='create_user'),
    path('token/', get_token, name='token_obtain'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
