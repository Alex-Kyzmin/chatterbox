from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    # переводим название приложения в интерфейсе.
    verbose_name = 'Блог'
