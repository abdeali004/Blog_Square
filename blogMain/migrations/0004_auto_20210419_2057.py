# Generated by Django 3.1.4 on 2021-04-19 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogMain', '0003_auto_20210419_1243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='addressPrimary',
            new_name='fb',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='insta',
            field=models.TextField(default=''),
        ),
    ]
