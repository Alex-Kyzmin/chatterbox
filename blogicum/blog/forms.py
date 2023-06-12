from django import forms
from django.contrib.auth import get_user_model

from blog.models import Comments, Post

# Получаем модель пользователя:
User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма создания/изменения поста на основе модели"""
    
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'image', 'location', 'category')
        widgets = {
            'pub_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'})
        }


class CommentsForm(forms.ModelForm):
    """Форма создания/изменения комментария на основе модели"""

    class Meta:
        model = Comments
        fields = ('text',)


class UserUpdateForm(forms.ModelForm):
    """Форма изменения профайла пользователя на основе встроенной модели"""
    
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')