

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from .models import Product, Category, Qna, Tag
from cart.forms import AddProductForm
from .forms import QnaForm


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
    product_total = Product.objects.all().count()
    print("product_total : ", product_total)

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
    context['q_form'] = QnaForm()
    context['product'] = product
    context['questions'] = product.qna_set.all().order_by('-created')

    return render(request, 'blog/product_detail.html', context)


def product_delete(request, id, slug=None):
    product = Product.objects.get(id=id)
    if product.author != request.user:
        return render(request, 'blog/forbidden.html')

    if request.method == 'POST':
        Product.objects.filter(id=id).delete()
        return redirect('/')
    return render(request, 'blog/product_delete.html', {'product': product})

class ProductDetailView(DetailView):
    model = Product

def product_qna(request, slug, id):
    model = Qna
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        q_form = QnaForm(request.POST)
        if q_form.is_valid():
            qna = q_form.save(commit=False)
            qna.product = product
            reply_id = request.POST.get('qna_id')
            text = request.POST.get('text')
            # print('reply_id : ', reply_id)
            # print('text : ', text)
            qna_qs = None
            if reply_id:
                qna_qs = Qna.objects.get(id=reply_id)
            qna = Qna.objects.create(product=product, text=text, author=request.user, reply=qna_qs)
            qna.save()
            return redirect('product-detail', id=id, slug=slug)
        return redirect('product-detail', id=id, slug=slug)
    else :
        return render(request, 'blog/forbidden.html')



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'content', 'image', 'price', 'discount_price', 'category']

    def form_valid(self, form):
        form.instance.slug = form.instance.title.replace(' ', '-')
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'content', 'image', 'price', 'discount_price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False



