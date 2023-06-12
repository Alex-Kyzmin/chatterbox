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


User = get_user_model()


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
        comment_count=Count('comments')
    ).order_by('-pub_date',)
    template_name = 'blog/index.html'
    paginate_by = 10


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


class PostMixin:
    """Миксин для CBV-функций изменений поста."""
    model = Post
    template_name = 'blog/create.html'


class CreatePostView(LoginRequiredMixin, PostMixin, CreateView):
    """CBV-функция создания поста."""
    form_class = PostForm
    success_url = reverse_lazy('blog:profile')
    slug_url_kwarg = 'username'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.author})


class EditPostView(LoginRequiredMixin, PostMixin, UpdateView):
    """CBV-функция изменения поста."""
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if post.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.author})


class DeletePostView(LoginRequiredMixin, PostMixin, DeleteView):
    """CBV-функция удаления поста."""
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'])
        if post.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


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
        comment_count=Count('comments')
    ).order_by('-pub_date',)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


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
        return reverse_lazy('blog:post_detail',
                            kwargs={'id': self.object.post_id})


class EditCommentsView(LoginRequiredMixin, UpdateView):
    """CBV-функция изменения комментария поста."""
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    pk_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, id=kwargs['comment_id'],
                                    post=kwargs['post_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'id': self.object.post_id})


class DeleteCommentsView(LoginRequiredMixin, DeleteView):
    """CBV-функция удаления комментария поста."""
    model = Comments
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    pk_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, id=kwargs['comment_id'],
                                    post=kwargs['post_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'id': self.object.post_id})


def profile(request, username):
    """view-функция профайла пользователя."""
    profile = get_object_or_404(User, username=username)
    post = Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        author=profile.id
    ).annotate(
        comment_count=Count('comments')
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
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.username})
