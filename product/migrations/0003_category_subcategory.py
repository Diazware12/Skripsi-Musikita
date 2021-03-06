# Generated by Django 3.2.1 on 2021-05-06 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_productimg'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categoryId', models.AutoField(primary_key=True, serialize=False)),
                ('categoryName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('subCategoryId', models.AutoField(primary_key=True, serialize=False)),
                ('categoryId', models.BigIntegerField()),
                ('subCategoryName', models.CharField(max_length=50)),
            ],
        ),
    ]
