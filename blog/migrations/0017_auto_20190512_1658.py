# Generated by Django 2.2.1 on 2019-05-12 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_qna_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qna',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.Qna'),
        ),
    ]