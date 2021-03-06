# Generated by Django 2.2.4 on 2022-07-04 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cook_app', '0005_auto_20220704_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=225)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='cook_app.Chef')),
                ('ingredient', models.ManyToManyField(blank=True, to='cook_app.Ingredient')),
            ],
        ),
        migrations.DeleteModel(
            name='Recipe1',
        ),
    ]
