# Generated by Django 5.0.3 on 2024-03-31 01:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='created_by',
        ),
        migrations.AddField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
