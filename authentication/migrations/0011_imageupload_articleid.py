# Generated by Django 5.0.4 on 2024-05-04 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_acmodel_isvalid'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='articleid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.acmodel'),
            preserve_default=False,
        ),
    ]
