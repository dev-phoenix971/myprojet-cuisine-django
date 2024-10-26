# Generated by Django 5.0.2 on 2024-05-12 16:43

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='profilepic.jpg', force_format='WEBP', keep_meta=True, quality=75, scale=None, size=[300, 300], upload_to='accounts/'),
        ),
    ]
