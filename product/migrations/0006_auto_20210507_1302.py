# Generated by Django 3.2.1 on 2021-05-07 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20210506_2208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='productName',
            new_name='brandName',
        )
    ]