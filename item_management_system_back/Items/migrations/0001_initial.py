# Generated by Django 5.0.2 on 2024-02-24 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='', max_length=100)),
                ('item_code', models.CharField(default='', max_length=100)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('specifications', models.TextField()),
                ('category', models.CharField(default='', max_length=100)),
                ('brand', models.CharField(default='', max_length=100)),
                ('inventory', models.IntegerField()),
                ('campus', models.IntegerField()),
                ('location', models.CharField(default='', max_length=100)),
                ('max_quantity', models.IntegerField()),
                ('instructions', models.TextField()),
                ('pictureUrl', models.CharField(default='', max_length=100)),
                ('approval_classification', models.IntegerField()),
                ('frequency_use', models.IntegerField()),
            ],
        ),
    ]
