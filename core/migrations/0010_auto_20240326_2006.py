# Generated by Django 3.2.13 on 2024-03-26 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_post_id_likepost_id_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likepost',
            name='id_post',
        ),
        migrations.AddField(
            model_name='likepost',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.post'),
            preserve_default=False,
        ),
    ]