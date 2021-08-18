from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', '__str__', 'score', 'author', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author', 'pub_date',)
    empty_value_display = '-пусто-'


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'description', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('genre', 'year',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoriesAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Genre, GenresAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Title, TitlesAdmin)
