from django.contrib import admin

from reviews.models import User, Category, Genre


class CummonAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(CummonAdmin):
    ...


class GenreAdmin(CummonAdmin):
    ...


admin.site.register(User)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Genre, GenreAdmin)
