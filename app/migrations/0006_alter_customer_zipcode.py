# Generated by Django 4.2.1 on 2023-06-04 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_customer_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='zipcode',
            field=models.CharField(max_length=8),
        ),
    ]
