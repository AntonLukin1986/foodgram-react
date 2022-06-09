# Generated by Django 4.0.4 on 2022-05-21 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('measurement_unit', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]