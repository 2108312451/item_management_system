# Generated by Django 5.0.2 on 2024-02-24 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AllUser', '0002_alter_ordinaryuser_reputation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(default='', max_length=10)),
            ],
        ),
    ]
