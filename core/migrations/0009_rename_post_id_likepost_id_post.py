# Generated by Django 3.2.13 on 2024-03-26 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_likepost_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likepost',
            old_name='post_id',
            new_name='id_post',
        ),
    ]