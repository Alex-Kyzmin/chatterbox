from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    # переводим приложение "Blog" на русский: "Блог".
    verbose_name = 'Блог'
