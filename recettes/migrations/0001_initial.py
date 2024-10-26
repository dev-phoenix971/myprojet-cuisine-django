# Generated by Django 5.0.2 on 2024-05-13 22:15

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecetteCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='defaultcategory.png', upload_to='recettes')),
                ('coverImageCat', models.ImageField(default='defaultcover.png', upload_to='recettes')),
            ],
        ),
        migrations.CreateModel(
            name='RecetteCategoryClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleclient', models.CharField(max_length=255, unique=True, verbose_name='Titre_client')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='defaultcategory.png', upload_to='recettesclients')),
                ('coverImageCat', models.ImageField(default='defaultcover.png', upload_to='recettesclients')),
            ],
        ),
        migrations.CreateModel(
            name='Recettes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Recette')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('ingredients', models.TextField(blank=True, null=True)),
                ('preparation', models.TextField(blank=True, null=True)),
                ('tempsprepaAt', models.DurationField(default=datetime.timedelta(0))),
                ('tempscuisAt', models.DurationField(default=datetime.timedelta(0))),
                ('coverImage', models.ImageField(default='defaultcover.png', upload_to='recettes')),
                ('image', models.ImageField(default='defaultrecette.png', upload_to='recettes')),
                ('imagefondvideo', models.ImageField(default='defaultfond.jpg', upload_to='recettes')),
                ('video', models.FileField(default='videos/defaultvideo.mp4', max_length=300, upload_to='videos', verbose_name='Video_recette')),
                ('published', models.BooleanField(default=False, verbose_name='Publié')),
                ('last_udated', models.DateTimeField(auto_now=True)),
                ('createdAt', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recette_author', to=settings.AUTH_USER_MODEL)),
                ('catrecette', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recettes.recettecategory')),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='Recettesclients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameclient', models.CharField(max_length=255, unique=True, verbose_name='Recetteclient')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('ingredients', models.TextField(blank=True, null=True)),
                ('preparation', models.TextField(blank=True, null=True)),
                ('tempsprepaAt', models.DurationField(default=datetime.timedelta(0))),
                ('tempscuisAt', models.DurationField(default=datetime.timedelta(0))),
                ('coverImage', models.ImageField(default='defaultcover.png', upload_to='recettesclients')),
                ('image', models.ImageField(default='defaultrecette.png', upload_to='recettesclients')),
                ('imagefondvideo', models.ImageField(default='defaultfond.jpg', upload_to='recettesclients')),
                ('video', models.FileField(default='videos/defaultvideo.mp4', max_length=300, upload_to='videosclients', verbose_name='Video_client')),
                ('published', models.BooleanField(default=False, verbose_name='Publié')),
                ('last_udated', models.DateTimeField(auto_now=True)),
                ('createdAt', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetteclient_author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recettes.recettecategoryclient')),
            ],
            options={
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='RecetteComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
                ('recette', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recette_comment', to='recettes.recettes')),
                ('recetteclient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recetteclient_comment', to='recettes.recettesclients')),
            ],
            options={
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='VideoLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_recette', to='recettes.recettes')),
                ('recetteclient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_recetteclient', to='recettes.recettesclients')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker_recette', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
