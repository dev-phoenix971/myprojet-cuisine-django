# Generated by Django 5.0.2 on 2024-04-29 17:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=120, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must be Alphanumeric or contain any of the following: " . @ + -"', regex='^[a-zA-Z0-9.+-]*$')])),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
