# Generated by Django 4.1.13 on 2024-10-30 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0002_remove_logo_logo_image_remove_logo_uploaded_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
