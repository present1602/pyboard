# Generated by Django 2.2.1 on 2019-05-13 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20190514_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qna',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.Qna'),
        ),
    ]