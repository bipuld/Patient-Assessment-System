# Generated by Django 5.0.6 on 2024-06-05 05:29

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='user.userinfo'),
        ),
        migrations.AddField(
            model_name='patient',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]