# Generated by Django 3.1 on 2020-11-19 14:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('media_patronage', '0017_auto_20201116_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperationterms',
            name='date_update',
            field=models.DateField(default=datetime.datetime(2020, 11, 19, 14, 56, 50, 721396, tzinfo=utc), verbose_name='Data dodania warunków wspólpracy'),
        ),
    ]
