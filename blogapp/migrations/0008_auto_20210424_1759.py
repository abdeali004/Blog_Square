# Generated by Django 3.1.3 on 2021-04-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_article_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_comments',
            name='comment_creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
