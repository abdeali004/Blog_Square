# Generated by Django 3.1.4 on 2021-04-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogMain', '0006_userinfo_commented'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='blogsCount',
            field=models.IntegerField(default=0),
        ),
    ]