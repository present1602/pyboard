from django.urls import path
# from . import views
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='blog-home'),
    # path('tag/?P<slug>[가-힣a-zA-Z]/', PostListByTag.as_view(), name='item_in_tag'),
    # path('tag/<slug:slug>/', PostListByTag.as_view(), name='item_in_tag'),
    # path('category/<slug:slug>/', PostListByCategory.as_view(), name='item_in_category'),
    # path('category/<slug:category_slug>/', views.item_in_category, name='item_in_category'),
    path('category/<slug>/', ProductListByCategory.as_view(), name='item_in_category'),
    path('product/<int:id>/<slug>/', product_detail, name='product-detail'),
    # path('product/<int:id>/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:id>/<slug>/question/', product_question, name='product-question'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:id>/<slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:id>/<slug>/delete/', product_delete, name='product-delete'),
    path('seller/<int:id>/', list_by_seller, name='list-by-seller'),
]

# pattern(s) tried: ['category\\/(?P<slug>[-a-zA-Z0-9_]+)\\/$']

# /^[가-힣a-zA-Z]+$/
#
# ?P<year>[0-9]{4})/$
#
# (?P<year>[0-9]{4})