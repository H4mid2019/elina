# Generated by Django 3.2.9 on 2022-01-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpha', '0003_alter_exchangerate_server_refreshed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='rate',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
    ]
