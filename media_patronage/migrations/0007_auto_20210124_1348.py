# Generated by Django 3.1 on 2021-01-24 13:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('media_patronage', '0006_auto_20210124_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='who_send',
            field=models.EmailField(default='test@test.pl', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cooperationterms',
            name='date_update',
            field=models.DateField(default=datetime.datetime(2021, 1, 24, 13, 48, 31, 361240, tzinfo=utc), verbose_name='Data dodania warunków wspólpracy'),
        ),
    ]
