# Generated by Django 3.2.1 on 2021-05-10 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20210507_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categoryId',
            field=models.BigIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='subCategoryId',
            field=models.BigIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='categoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category'),
        ),
    ]
