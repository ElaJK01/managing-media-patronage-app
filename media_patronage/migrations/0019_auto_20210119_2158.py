# Generated by Django 3.1 on 2021-01-19 21:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('media_patronage', '0018_auto_20201119_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='send_from_email',
        ),
        migrations.AlterField(
            model_name='cooperationterms',
            name='date_update',
            field=models.DateField(default=datetime.datetime(2021, 1, 19, 21, 58, 7, 871518, tzinfo=utc), verbose_name='Data dodania warunków wspólpracy'),
        ),
    ]