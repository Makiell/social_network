# Generated by Django 3.2.13 on 2024-03-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_post_likepost_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]