from django.contrib import admin

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')


class CategoryAdmin(CategoryGenreAdmin):
    ...


class GenreAdmin(CategoryGenreAdmin):
    ...


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category'
    )
    list_editable = ('name', 'year', 'description', 'category')
    search_fields = ('name',)


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title'
    )
    list_editable = ('genre', 'title')
    search_fields = ('genre', 'title')


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'pub_date',
        'title',
        'text',
        'score'
    )
    list_editable = ('author', 'title', 'text', 'score')
    search_fields = ('author', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'pub_date',
        'review',
        'text',
    )
    list_editable = ('author', 'review', 'text')
    search_fields = ('text',)


admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
