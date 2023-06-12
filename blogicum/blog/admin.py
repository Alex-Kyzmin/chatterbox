from django.contrib import admin

from blog.models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс для настройки админ-зоны модели Category"""
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Класс для настройки админ-зоны модели Location"""
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для настройки админ-зоны модели Post"""
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    search_fields = ('title',)
