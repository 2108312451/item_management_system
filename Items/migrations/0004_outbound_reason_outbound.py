# Generated by Django 5.0.2 on 2024-02-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0003_outbound_warehousing'),
    ]

    operations = [
        migrations.AddField(
            model_name='outbound',
            name='Reason_Outbound',
            field=models.IntegerField(default=0),
        ),
    ]