# Generated by Django 2.2.6 on 2020-10-19 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('units', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('cooking_time', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(null=True, upload_to='recipes/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('colour', models.CharField(blank=True, max_length=100)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag'),
        ),
    ]
