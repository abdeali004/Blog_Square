# Generated by Django 3.1.4 on 2021-04-28 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogMain', '0008_auto_20210428_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='blogsViewed',
            field=models.TextField(default=''),
        ),
    ]