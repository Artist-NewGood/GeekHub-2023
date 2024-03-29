# Generated by Django 5.0 on 2024-01-13 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_string', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=15)),
                ('brand_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('discounted_price', models.CharField(max_length=10)),
                ('price_before_discount', models.CharField(max_length=10)),
                ('savings_percent', models.CharField(max_length=255)),
                ('product_link', models.CharField(max_length=255)),
            ],
        ),
    ]
