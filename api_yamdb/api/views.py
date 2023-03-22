from http import HTTPStatus
from rest_framework import viewsets, mixins, permissions, filters
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404

from api_yamdb import settings
from reviews.models import Title, Genre, Category, Review, Comment
from users.models import CustomUser

from .permissions import IsAdminOrReadOnly, IsAuMASuOrReadOnly, AuthOrAdmin
from .serializers import (
    GenreSerializer, CategorySerializer,
    ReviewSerializer, CommentSerializer,
    TitleListRetrieveSerializer, TitleCreateSerializer,
    AuthSerializer, TokenSerializer,
    UserSerializer, UserMeSerializer
)
from .filters import TitleFilter


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateSerializer
        return TitleListRetrieveSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuMASuOrReadOnly,)
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuMASuOrReadOnly,)
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title=get_object_or_404(
                Title,
                pk=self.kwargs.get("title_id")
            )
        )
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title=get_object_or_404(
                Title,
                pk=self.kwargs.get("title_id")
            )
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, create = CustomUser.objects.get_or_create(
        username=username, email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения', f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
    return Response(serializer.validated_data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(CustomUser, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=HTTPStatus.OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=HTTPStatus.BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = (AuthOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == 'GET':
            serializer = UserMeSerializer(user)
            return Response(serializer.data)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
