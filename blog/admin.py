from django.contrib import admin
from .models import Product, Category, Qna, Tag


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title', 'author', 'author_id', 'date_posted']


class QnaAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'product', 'author', 'reply_id', 'created']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Qna, QnaAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

