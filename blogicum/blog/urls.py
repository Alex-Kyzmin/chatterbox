from django.contrib.auth import views
from django.urls import path

from blog import views

app_name = 'blog'  # указываем namespace приложения.

urlpatterns = [
    path('', views.Post_Index.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.CreatePostView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', views.EditPostView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/', views.DeletePostView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/', views.CreateCommentsView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>',
         views.EditCommentsView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>',
         views.DeleteCommentsView.as_view(), name='delete_comment'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profile/<username>/edit', views.EditProfile.as_view(),
         name='edit_profile'),
]
