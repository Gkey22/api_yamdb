from django.contrib import admin

from .models import Categorie, Genre, Title, User, Review, Comment, GenreTitle

admin.site.site_header = 'Панель администратора YaMDb'
admin.site.site_title = 'Панель администратора YaMDb'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year')
    # list_filter = ('year', 'genre', 'category')
    search_fields = ('name', 'description')
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'bio',
        'role',
        'email')
    search_fields = ('username',)
    list_filter = ('username',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_id',
        'author',
        'score',
        'pub_date'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review_id',
        'text',
        'pub_date'
    )


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_id',
        'genre_id'
    )


admin.site.register(GenreTitle, TitleGenreAdmin)
admin.site.register(Categorie, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
