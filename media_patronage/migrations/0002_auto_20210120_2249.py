# Generated by Django 3.1 on 2021-01-20 22:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('media_patronage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperationterms',
            name='date_update',
            field=models.DateField(default=datetime.datetime(2021, 1, 20, 22, 49, 7, 497639, tzinfo=utc), verbose_name='Data dodania warunków wspólpracy'),
        ),
    ]