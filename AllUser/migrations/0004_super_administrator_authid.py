# Generated by Django 5.0.2 on 2024-03-02 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AllUser', '0003_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='super_administrator',
            name='authid',
            field=models.IntegerField(default=0),
        ),
    ]
