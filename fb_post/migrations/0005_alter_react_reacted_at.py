# Generated by Django 4.1.3 on 2022-11-23 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0004_alter_react_reacted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='react',
            name='reacted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
