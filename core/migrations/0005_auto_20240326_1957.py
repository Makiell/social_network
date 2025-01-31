# Generated by Django 3.2.13 on 2024-03-26 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_likepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post'),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile'),
        ),
    ]
