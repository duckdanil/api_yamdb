from django.contrib import admin

from reviews.models import User, Category, Genre, Title, GenreTitle, Review, Comment


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


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


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title'
    )
    list_editable = ('genre', 'title')


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


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'pub_date',
        'review',
        'text',
    )
    list_editable = ('author', 'review', 'text')


admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
