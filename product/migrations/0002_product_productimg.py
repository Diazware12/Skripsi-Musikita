# Generated by Django 3.2.1 on 2021-05-05 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productIMG',
            field=models.ImageField(default='none', upload_to=''),
        ),
    ]