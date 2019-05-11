

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from .models import Product, Category, Question, Tag
from cart.forms import AddProductForm
from .forms import QuestionForm


def list_by_seller(request, id):
    seller = User.objects.get(id=id)
    items = Product.objects.filter(author=seller)
    context = {'items': items, 'seller': seller}
    return render(request, 'blog/list_by_seller.html', context)
    # print("id", id)



# def item_in_category(request, category_slug=None):
#
#     current_category = None
#     categories = Category.objects.all()
#     items = Post.objects.all()
#
#     if category_slug:
#         current_category = get_object_or_404(Category, slug=category_slug)
#         items = items.filter(category=current_category)
#
#     context = {
#         'current_category': current_category,
#         'category_list': categories,
#         'items': items
#     }
#     return render(request, 'blog/home.html', context)


# def item_in_tag(request, tag_slug=None):
#     if tag_slug:
#         items = tag_slug.post_set.order_by('-date_posted')
#     else:
#         items = Post.objects.all()
#
#     context = {
#         'items': items
#     }
#     return render(request, 'blog/home.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'blog/home.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()

        return context
    # context = {
    #     'posts': Post.objects.all(),
    #     'category_list': Category.objects.all()
    #
    # }
    # ordering = ['-date_posted']


class ProductListByCategory(ProductListView):

    def get_queryset(self):
        slug = self.kwargs['slug']
        # print("slug")
        # print(slug)
        category = Category.objects.get(slug=slug)
        return Product.objects.filter(category=category).order_by('-date_posted')


# class PostListByTag(ListView):
#     print('PostListByTag 실행')
#     model = Post
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#
#     def get_queryset(self):
#         print('PostListByTag getqueryset 실행')
#
#         slug = self.kwargs['slug']
#         print("slug")
#         print(slug)
#         tag = Tag.objects.get(slug=slug)
#         return tag.post_set.order_by('-date_posted')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PostListByTag, self).get_context_data(**kwargs)
#         context['category_list'] = Category.objects.all()
#
#         return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


# class ProductDetailView(DetailView):
#     model = Product


def product_detail(request, id, slug=None):
    context = {}
    product = get_object_or_404(Product, id=id, slug=slug)
    context['add_to_cart'] = AddProductForm(initial={'quantity':1})
    context['q_form'] = QuestionForm()
    context['product'] = product
    context['questions'] = product.question_set.all().order_by('-created')

    return render(request, 'blog/product_detail.html', context)


def product_question(request, slug, id):
    # model = Question
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.product = product
            question.author = request.user
            question.save()
            return redirect('/')
    else:
        return redirect('/')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'content', 'image', 'price']

    def form_valid(self, form):
        form.instance.slug = form.instance.title
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


