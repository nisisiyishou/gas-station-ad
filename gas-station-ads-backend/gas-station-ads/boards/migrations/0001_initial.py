# Generated by Django 5.1.7 on 2025-03-24 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_id', models.CharField(max_length=20, unique=True)),
                ('board_type', models.CharField(choices=[('digital', 'Digital Screen'), ('poster', 'Poster'), ('billboard', 'Billboard')], max_length=20)),
                ('location_in_station', models.CharField(choices=[('entrance', 'Entrance'), ('checkout', 'Checkout Area'), ('pump', 'Fuel Pump'), ('exterior', 'Exterior Wall'), ('interior', 'Interior Wall')], max_length=20)),
                ('width', models.DecimalField(decimal_places=2, help_text='Width in cm', max_digits=6)),
                ('height', models.DecimalField(decimal_places=2, help_text='Height in cm', max_digits=6)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_available', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='board_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gas_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='stations.gasstation')),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('original_media', models.FileField(upload_to='ad_originals/')),
                ('adjusted_media', models.FileField(blank=True, null=True, upload_to='ad_adjusted/')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='boards.commercialboard')),
            ],
        ),
    ]
