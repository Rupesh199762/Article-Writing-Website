# Generated by Django 5.0.4 on 2024-05-02 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_remove_acmodel_list_image_acmodel_subtitle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acmodel',
            name='isvalid',
            field=models.BooleanField(default=False),
        ),
    ]