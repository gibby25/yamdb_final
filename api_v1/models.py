from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def get_unique_slug(self, model):
    slug = slugify(self.name)
    unique_slug = slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug


def validate_year(value):
    if value > int(datetime.now().year) + 2:
        raise ValidationError(
            _('До %(value)s еще далеко'),
            params={'value': value},
        )
    return value


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Категория',
        help_text='Введите название категории')
    slug = models.SlugField(
        verbose_name='URL',
        help_text='Задается автоматически или вручную',
        unique=True,
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, Category)
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        help_text='Введите название жанра',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='URL',
        help_text='Задается автоматически или вручную',
        unique=True,
        max_length=99,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, Genre)
        super().save(*args, **kwargs)


class Title(models.Model):
    name = models.CharField(
        'Наименование',
        help_text='Введите',
        max_length=50,
        blank=False,
        null=False
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        blank=True,
        null=True,
        db_index=True,
        verbose_name='Год'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Введите',
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Наименование'
    )
    text = models.TextField(
        verbose_name='Содержание'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Диапазон от 1 до 10'),
            MinValueValidator(1, 'Диапазон от 1 до 10')
        ],
        null=True,
        db_index=True,
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        unique_together = ('author', 'title',)
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        author = self.author
        text = self.text[:20]
        return f'{author}: {text}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Содержание',
        help_text='Введите'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        author = self.author
        text = self.text[:20]
        return f'{author}: {text}'
