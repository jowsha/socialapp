# Generated by Django 4.1.1 on 2023-01-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_userdetails_use_alter_userdetails_about_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]