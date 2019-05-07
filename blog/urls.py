from django.urls import path
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views
from .views import *

urlpatterns = [
    path('', views.item_in_category, name='blog-home'),
    path('<slug:category_slug>/', views.item_in_category, name='item_in_category'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]

