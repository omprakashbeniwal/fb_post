# Generated by Django 4.1.3 on 2022-11-11 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='react',
            name='reacted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_post.user'),
        ),
    ]
