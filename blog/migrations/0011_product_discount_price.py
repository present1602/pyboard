# Generated by Django 2.2.1 on 2019-05-10 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
    ]