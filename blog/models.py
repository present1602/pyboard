from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return 'tag/{}/'.format(self.slug)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_in_category', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photo", default='default.jpg')
    slug = models.SlugField(max_length=200, db_index=True, unique=True,
                            allow_unicode=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.id, self.slug])
