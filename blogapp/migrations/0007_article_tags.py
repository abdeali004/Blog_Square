# Generated by Django 3.1.3 on 2021-04-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_auto_20210423_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='article_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.TextField()),
                ('count', models.IntegerField()),
            ],
        ),
    ]