from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'genre',
                  'category', 'description', 'rating')
        model = Title
        read_only_fields = ('rating', 'category', 'genre')


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10.')
        return value

    def validate(self, data):
        request = self.context.get('request')
        review = Review.objects.filter(
            author=self.context['request'].user,
            title=request.parser_context.get('kwargs').get('title_id')
        )
        if request.method == 'POST' and review:
            raise serializers.ValidationError(
                'Можно постить только один обзор на произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(UnicodeUsernameValidator(),),
        max_length=150
    )

    email = serializers.EmailField(max_length=254)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        if (
            CustomUser.objects.filter(username=username).exists()
            and not CustomUser.objects.filter(
                email=self.initial_data.get('email')
            ).exists()
        ):
            raise serializers.ValidationError('Данный username занят.')
        return username

    def validate_email(self, email):
        if (
            not CustomUser.objects.filter(
                username=self.initial_data.get('username')
            ).exists()
            and CustomUser.objects.filter(email=email).exists()
        ):
            raise serializers.ValidationError('Данный email уже используется.')
        return email


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role'
                  )


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = CustomUser
        read_only_fields = ('role',)
