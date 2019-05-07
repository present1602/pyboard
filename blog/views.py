from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Category


def item_in_category(request, category_slug=None):

    current_category = None
    categories = Category.objects.all()
    items = Post.objects.all()

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=current_category)

    context = {
        'current_category': current_category,
        'category_list': categories,
        'items': items
    }
    return render(request, 'blog/home.html', context)


def home(request):
    context = {
        'posts': Post.objects.all(),
        'categories': Category.objects.all(),
    }

    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()

        return context


class PostListByCategory(PostListView):

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-date_posted')

#     return Post.objects


# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'
#     # context_object_name = 'posts'
#     context = {
#         'posts': Post.objects.all(),
#
#     }
#     ordering = ['-date_posted']



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


