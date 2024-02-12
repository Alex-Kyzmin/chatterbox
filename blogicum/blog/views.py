from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.forms import CommentsForm, PostForm, UserUpdateForm
from blog.models import Category, Comments, Post

PAGINATE_CONST = 10  # Константа количества вывода постов.

User = get_user_model()  # Обращаемся к встроенной модели User.


class Post_Index(ListView):
    """CBV-функция списка постов(главная страница)."""
    model = Post
    queryset = Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    ).annotate(
        comment_count=Count('comments',)
    ).order_by('-pub_date',)
    template_name = 'blog/index.html'
    paginate_by = PAGINATE_CONST


def post_detail(request, id):
    """view-функция поста(детально)"""
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'location',
            'category',
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            id=id,
        )
    )
    context = {'post': post}
    context['form'] = CommentsForm()
    context['comments'] = post.comments.all()
    return render(request, 'blog/detail.html', context)


class CreatePostView(LoginRequiredMixin, CreateView):
    """CBV-функция создания поста."""
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:profile')
    slug_url_kwarg = 'username'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.object.author])


class PostMixin:
    """Миксин для CBV-функций изменений поста."""
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class EditPostView(LoginRequiredMixin, PostMixin, UpdateView):
    """CBV-функция изменения поста."""
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.object.author])


class DeletePostView(LoginRequiredMixin, PostMixin, DeleteView):
    """CBV-функция удаления поста."""
    success_url = reverse_lazy('blog:index')


class CreateCommentsView(LoginRequiredMixin, CreateView):
    """CBV-функция создания комментария поста."""
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.object.post_id])


class CommentsMixin:
    """Миксин для CBV-функций изменений комментарий поста."""
    model = Comments
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    pk_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, pk=kwargs['comment_id'],
                                    post=kwargs['post_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.object.post_id])


class EditCommentsView(LoginRequiredMixin, CommentsMixin, UpdateView):
    """CBV-функция изменения комментария поста."""
    form_class = CommentsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)


class DeleteCommentsView(LoginRequiredMixin, CommentsMixin, DeleteView):
    """CBV-функция удаления комментария поста."""
    pass


def category_posts(request, category_slug):
    """view-функция Категории постов."""
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
            slug=category_slug,
        )
    )
    post_list = category.posts.select_related(
        'author',
        'location',
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
    ).annotate(
        comment_count=Count('comments',)
    ).order_by('-pub_date',)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


def profile(request, username):
    """view-функция профайла пользователя."""
    profile = get_object_or_404(User, username=username)
    post = Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        author=profile.id,
    ).annotate(
        comment_count=Count('comments',)
    ).order_by('-pub_date',)
    if username == request.user.username:
        post_list = post
    else:
        post_list = post.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
        )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class EditProfile(LoginRequiredMixin, UpdateView):
    """CBV-функция изменения профайла пользователя."""
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.object.username])
